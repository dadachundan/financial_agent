"""
YouTube Video Analysis - Transcript Chunker + MiniMax Summarizer
Fetches transcript, splits into 3-minute chunks, summarizes each chunk via MiniMax,
and stores results in a local SQLite database.

Usage:
    python analysis_video.py                        # analyze default video
    python analysis_video.py <video_id>             # analyze specific video
    python analysis_video.py <video_id> --no-api    # fetch transcript only, skip MiniMax
"""

import sys
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

# Allow importing minimax.py from project root
SCRIPT_DIR = Path(__file__).parent
_root = next((p for p in [SCRIPT_DIR, *SCRIPT_DIR.parents] if (p / "minimax.py").exists()), None)
if _root and str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from minimax import call_minimax, MINIMAX_API_KEY  # type: ignore

DEFAULT_VIDEO_ID = "YFjfBk8HI5o"
CHUNK_SECONDS    = 3 * 60  # 3-minute chunks
DB_PATH          = SCRIPT_DIR / "video_summaries.db"

CHUNK_SUMMARY_SYSTEM = (
    "You are an expert content analyst. Given a portion of a YouTube video transcript "
    "with timestamps, write a concise summary of what is discussed in this segment.\n\n"
    "Be specific about the topics, ideas, and key points covered.\n"
    "Keep your summary to 3-5 sentences."
)


# ── Database ──────────────────────────────────────────────────────────────────

def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS video_chunks (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id       TEXT    NOT NULL,
            chunk_index    INTEGER NOT NULL,
            start_seconds  INTEGER NOT NULL,
            end_seconds    INTEGER NOT NULL,
            start_label    TEXT    NOT NULL,
            end_label      TEXT    NOT NULL,
            transcript     TEXT    NOT NULL,
            summary        TEXT,
            analyzed_at    TEXT,
            UNIQUE(video_id, chunk_index)
        )
    """)
    conn.commit()
    return conn


def upsert_chunk(conn: sqlite3.Connection, video_id: str, chunk_index: int,
                 start_seconds: int, end_seconds: int,
                 start_label: str, end_label: str,
                 transcript: str, summary: str | None) -> None:
    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO video_chunks
            (video_id, chunk_index, start_seconds, end_seconds, start_label, end_label,
             transcript, summary, analyzed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id, chunk_index) DO UPDATE SET
            start_seconds = excluded.start_seconds,
            end_seconds   = excluded.end_seconds,
            start_label   = excluded.start_label,
            end_label     = excluded.end_label,
            transcript    = excluded.transcript,
            summary       = excluded.summary,
            analyzed_at   = excluded.analyzed_at
    """, (video_id, chunk_index, start_seconds, end_seconds,
          start_label, end_label, transcript, summary, now))
    conn.commit()


# ── Transcript Fetching ───────────────────────────────────────────────────────

def fetch_raw_transcript(video_id: str) -> list[dict]:
    """Return list of {start, duration, text} dicts."""
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=["en"])
    except Exception:
        transcript_list = api.list(video_id)
        fetched = next(iter(transcript_list)).fetch()
    return [{"start": e.start, "duration": e.duration, "text": e.text} for e in fetched]


def seconds_to_label(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 60:02d}:{s % 60:02d}"


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_transcript(entries: list[dict], chunk_seconds: int = CHUNK_SECONDS) -> list[dict]:
    """
    Split transcript entries into fixed-duration chunks.
    Returns list of:
        {chunk_index, start_seconds, end_seconds, start_label, end_label, transcript}
    """
    if not entries:
        return []

    chunks = []
    chunk_idx = 0
    current_lines: list[str] = []
    chunk_start = entries[0]["start"]
    chunk_end_limit = chunk_start + chunk_seconds

    for entry in entries:
        start = entry["start"]
        # Start a new chunk when we've exceeded the time window
        if start >= chunk_end_limit:
            if current_lines:
                end_sec = int(start)
                chunks.append({
                    "chunk_index":   chunk_idx,
                    "start_seconds": int(chunk_start),
                    "end_seconds":   end_sec,
                    "start_label":   seconds_to_label(chunk_start),
                    "end_label":     seconds_to_label(end_sec),
                    "transcript":    "\n".join(current_lines),
                })
                chunk_idx += 1
                current_lines = []
                chunk_start = start
                chunk_end_limit = chunk_start + chunk_seconds

        timestamp = seconds_to_label(start)
        current_lines.append(f"[{timestamp}] {entry['text']}")

    # Last chunk
    if current_lines:
        last_start = entries[-1]["start"]
        last_dur   = entries[-1].get("duration", 0)
        end_sec    = int(last_start + last_dur)
        chunks.append({
            "chunk_index":   chunk_idx,
            "start_seconds": int(chunk_start),
            "end_seconds":   end_sec,
            "start_label":   seconds_to_label(chunk_start),
            "end_label":     seconds_to_label(end_sec),
            "transcript":    "\n".join(current_lines),
        })

    return chunks


# ── Summarization ─────────────────────────────────────────────────────────────

def summarize_chunk(chunk: dict, video_url: str) -> str:
    text, elapsed, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": CHUNK_SUMMARY_SYSTEM},
            {"role": "user",   "name": "User",
             "content": (
                 f"Video: {video_url}\n"
                 f"Segment: {chunk['start_label']} – {chunk['end_label']}\n\n"
                 f"Transcript:\n{chunk['transcript']}"
             )},
        ],
        temperature=0.3,
        max_completion_tokens=400,
    )
    print(f"    responded in {elapsed:.1f}s")
    return text


# ── Main ──────────────────────────────────────────────────────────────────────

def analyze_video(video_id: str, use_api: bool = True) -> None:
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Video: {video_url}")

    # 1. Fetch transcript
    print("\nFetching transcript...")
    entries = fetch_raw_transcript(video_id)
    print(f"  {len(entries)} transcript entries fetched")

    # Save raw transcript
    raw_lines = [f"[{seconds_to_label(e['start'])}] {e['text']}" for e in entries]
    transcript_file = SCRIPT_DIR / "transcript.txt"
    transcript_file.write_text(f"Video: {video_url}\n\n" + "\n".join(raw_lines), encoding="utf-8")
    print(f"  Saved → {transcript_file}")

    # 2. Chunk into 3-minute intervals
    chunks = chunk_transcript(entries)
    print(f"\nChunked into {len(chunks)} segments of ~{CHUNK_SECONDS//60} minutes each")

    # 3. Open database
    conn = init_db()
    print(f"Database: {DB_PATH}")

    # 4. Summarize each chunk
    for chunk in chunks:
        idx   = chunk["chunk_index"]
        label = f"{chunk['start_label']} – {chunk['end_label']}"
        print(f"\n  Chunk {idx+1}/{len(chunks)}  [{label}]")

        summary = None
        if use_api and MINIMAX_API_KEY:
            print(f"    Summarizing via MiniMax...", end=" ", flush=True)
            summary = summarize_chunk(chunk, video_url)
        elif not MINIMAX_API_KEY:
            print("    Skipping MiniMax (MINIMAX_API_KEY not set)")
        else:
            print("    Skipping MiniMax (--no-api flag)")

        upsert_chunk(
            conn,
            video_id     = video_id,
            chunk_index  = idx,
            start_seconds= chunk["start_seconds"],
            end_seconds  = chunk["end_seconds"],
            start_label  = chunk["start_label"],
            end_label    = chunk["end_label"],
            transcript   = chunk["transcript"],
            summary      = summary,
        )

    conn.close()
    total = len(chunks)
    print(f"\nDone. {total} chunk(s) stored in {DB_PATH}")
    print(f"Run the viewer:  python {SCRIPT_DIR}/viewer.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube transcript chunker + MiniMax summarizer")
    parser.add_argument("video_id", nargs="?", default=DEFAULT_VIDEO_ID,
                        help=f"YouTube video ID (default: {DEFAULT_VIDEO_ID})")
    parser.add_argument("--no-api", action="store_true",
                        help="Fetch transcript only, skip MiniMax summarization")
    args = parser.parse_args()

    analyze_video(args.video_id, use_api=not args.no_api)
