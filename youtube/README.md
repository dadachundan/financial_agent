# YouTube Video Analyzer

A two-script toolkit that fetches YouTube transcripts, splits them into 3-minute chunks, summarizes each chunk with MiniMax LLM, and lets you browse everything in a local web UI.

---

## Files

| File | Purpose |
|------|---------|
| `analysis_video.py` | Fetch transcript → chunk → summarize → save to SQLite |
| `viewer.py` | Flask web UI to browse and search saved summaries |
| `video_summaries.db` | SQLite database (auto-created on first run) |
| `transcript.txt` | Raw transcript export from the last analyzed video |

---

## Prerequisites

```bash
pip install youtube-transcript-api flask jinja2
```

MiniMax API key must be present in `config.py` at the project root (already set up).

---

## Step 1 — Analyze a video

```bash
cd /Users/x/projects/financial_agent/youtube

# Analyze a specific video (replace VIDEO_ID with the YouTube ID, e.g. dQw4w9WgXcQ)
python analysis_video.py VIDEO_ID

# Analyze the built-in default video (YFjfBk8HI5o)
python analysis_video.py

# Fetch transcript only — skip MiniMax summarization
python analysis_video.py VIDEO_ID --no-api

# Re-run synthesis only (video already in DB, skip re-fetching)
python analysis_video.py VIDEO_ID --synthesize-only
```

### What it does

1. Fetches the video transcript via `youtube_transcript_api` (English preferred, falls back to any available language).
2. Saves the raw transcript to `transcript.txt`.
3. Splits the transcript into **3-minute chunks**, each labelled with a `MM:SS – MM:SS` timestamp range.
4. **Pass 1** — sends every chunk to **MiniMax** (3–5 sentence summary per chunk).
5. Upserts all chunks + summaries into `video_summaries.db`.
6. **Pass 2 (synthesis)** — sends all chunk summaries together to MiniMax in a single call and produces a structured `key_points_<video_id>.md` file with:
   - **Summary** — one paragraph overview of the whole video
   - **Key Themes** — 3–6 high-level themes
   - **Key Insights** — 6–10 numbered, self-contained insights
   - **Notable Quotes** — 2–5 verbatim quotes with timestamps
   - **Takeaways** — 3–5 practical bullets

### Example output

```
Video: https://www.youtube.com/watch?v=kwSVtQ7dziU
Fetching transcript...
  2231 transcript entries fetched
  Saved → transcript.txt
Chunked into 23 segments of ~3 minutes each
Database: video_summaries.db

  Chunk 1/23  [00:00 – 03:00]
    Summarizing via MiniMax... responded in 6.4s
  Chunk 2/23  [03:00 – 06:01]
    Summarizing via MiniMax... responded in 7.5s
  ...
  Chunk 23/23  [66:25 – 66:30]
    Summarizing via MiniMax... responded in 2.2s

Synthesis pass — combining 23 chunk summaries via MiniMax...
  responded in 18.3s
  Saved → key_points_kwSVtQ7dziU.md

Done. 23 chunk(s) stored in video_summaries.db
```

---

## Step 2 — Browse summaries in the web UI

```bash
python viewer.py              # http://localhost:8081
python viewer.py --port 8082  # custom port
```

Open **http://localhost:8081** in your browser.

### Pages

| URL | What you see |
|-----|-------------|
| `/` | Grid of all analyzed videos with chunk counts and summarization progress bars |
| `/video/<video_id>` | All chunks for a video: timestamp range, MiniMax summary, collapsible raw transcript |

### Features

- **Clickable timestamps** — every `⏱ MM:SS – MM:SS` link opens YouTube at that exact moment.
- **▶ Play button** per chunk — same deep link, styled as a YouTube red button.
- **Search bar** — live filters chunks by summary or transcript text as you type.
- **Collapsible transcripts** — click `📄 transcript` to expand the raw timestamped text for any chunk.

### JSON API

```
GET /api/videos              → list of all videos with stats
GET /api/video/<video_id>    → all chunks for a video (id, timestamps, transcript, summary)
```

---

## Database schema

**Table: `video_chunks`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `video_id` | TEXT | YouTube video ID |
| `chunk_index` | INTEGER | 0-based chunk number |
| `start_seconds` | INTEGER | Chunk start time in seconds |
| `end_seconds` | INTEGER | Chunk end time in seconds |
| `start_label` | TEXT | Human-readable start (MM:SS) |
| `end_label` | TEXT | Human-readable end (MM:SS) |
| `transcript` | TEXT | Raw timestamped transcript lines |
| `summary` | TEXT | MiniMax-generated summary (NULL if `--no-api`) |
| `analyzed_at` | TEXT | ISO UTC timestamp of last processing |

Re-running `analysis_video.py` on the same video **upserts** (updates existing rows), so you can re-summarize or fill in missing summaries safely.

---

## Output files

| File | Created by | Contents |
|------|-----------|----------|
| `transcript.txt` | Every run | Raw timestamped transcript of the last analyzed video |
| `video_summaries.db` | Every run | All chunks + per-chunk summaries for all videos |
| `key_points_<video_id>.md` | Pass 2 (synthesis) | Structured doc: summary, themes, insights, quotes, takeaways |

---

## Common workflows

### Analyze multiple videos

```bash
python analysis_video.py abc123XYZ
python analysis_video.py def456UVW
python analysis_video.py ghi789RST
```

All results accumulate in the same `video_summaries.db`.

### Transcript only (no API cost)

```bash
python analysis_video.py VIDEO_ID --no-api
# transcript.txt is saved and chunks are stored without summaries
# Re-run without --no-api later to fill in summaries
```

### Re-generate the synthesis doc without re-fetching

```bash
python analysis_video.py VIDEO_ID --synthesize-only
# Reads existing chunk summaries from DB, calls MiniMax once, overwrites key_points_<VIDEO_ID>.md
```

### Quick inspection via SQLite

```bash
sqlite3 video_summaries.db "SELECT video_id, chunk_index, start_label, substr(summary,1,80) FROM video_chunks LIMIT 20;"
```

---

## How a YouTube video ID is found

Given a URL like `https://www.youtube.com/watch?v=YFjfBk8HI5o`, the video ID is the value of the `v=` parameter: **`YFjfBk8HI5o`**.

For short URLs like `https://youtu.be/YFjfBk8HI5o`, the ID is the path segment after `/`.
