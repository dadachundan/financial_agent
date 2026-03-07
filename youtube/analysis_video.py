"""
YouTube Video Analysis - Transcript Extractor + MiniMax Key Points
Video: https://www.youtube.com/watch?v=YFjfBk8HI5o
"""

import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

# Allow importing minimax.py from project root
SCRIPT_DIR = Path(__file__).parent
_root = next((p for p in [SCRIPT_DIR, *SCRIPT_DIR.parents] if (p / "minimax.py").exists()), None)
if _root and str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from minimax import call_minimax, MINIMAX_API_KEY  # type: ignore

VIDEO_ID  = "YFjfBk8HI5o"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"

KEY_POINTS_SYSTEM = (
    "You are an expert content analyst. Given a YouTube video transcript, extract "
    "the most important insights, key points, and takeaways from the video.\n\n"
    "Structure your response as:\n"
    "## Summary\n"
    "A 3-5 sentence overview of what the video is about.\n\n"
    "## Key Points\n"
    "A numbered list of the most important points (8-12 items).\n\n"
    "## Notable Quotes\n"
    "2-3 memorable direct quotes from the speaker(s).\n\n"
    "## Takeaways\n"
    "3-5 actionable or thought-provoking conclusions."
)


def fetch_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=["en"])
    except Exception:
        transcript_list = api.list(video_id)
        fetched = next(iter(transcript_list)).fetch()

    lines = []
    for entry in fetched:
        start   = entry.start
        minutes = int(start // 60)
        seconds = int(start % 60)
        lines.append(f"[{minutes:02d}:{seconds:02d}] {entry.text}")
    return "\n".join(lines)


def extract_key_points(transcript: str, video_url: str) -> str:
    text, elapsed, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": KEY_POINTS_SYSTEM},
            {"role": "user",   "name": "User",
             "content": f"Video URL: {video_url}\n\nTranscript:\n{transcript}"},
        ],
        temperature=0.3,
        max_completion_tokens=1500,
    )
    print(f"  MiniMax responded in {elapsed:.1f}s")
    return text


if __name__ == "__main__":
    print(f"Fetching transcript for: {VIDEO_URL}\n")
    transcript = fetch_transcript(VIDEO_ID)

    transcript_file = SCRIPT_DIR / "transcript.txt"
    transcript_file.write_text(f"Video: {VIDEO_URL}\n\n{transcript}", encoding="utf-8")
    print(f"Transcript saved → {transcript_file}  ({len(transcript.splitlines())} lines)\n")

    if not MINIMAX_API_KEY:
        print("Skipping MiniMax: MINIMAX_API_KEY not found in config.py")
    else:
        print("Extracting key points via MiniMax...")
        key_points = extract_key_points(transcript, VIDEO_URL)

        key_points_file = SCRIPT_DIR / "key_points.md"
        key_points_file.write_text(
            f"# YouTube Video Analysis\n\nVideo: {VIDEO_URL}\n\n{key_points}\n",
            encoding="utf-8",
        )
        print(f"Key points saved → {key_points_file}\n")
        print(key_points)
