"""
YouTube Video Analysis - Transcript Extractor
Video: https://www.youtube.com/watch?v=YFjfBk8HI5o
"""

from youtube_transcript_api import YouTubeTranscriptApi

VIDEO_ID = "YFjfBk8HI5o"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def fetch_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    # Try English first, fall back to any available language
    try:
        fetched = api.fetch(video_id, languages=["en"])
    except Exception:
        transcript_list = api.list(video_id)
        fetched = next(iter(transcript_list)).fetch()

    lines = []
    for entry in fetched:
        start = entry.start
        text = entry.text
        minutes = int(start // 60)
        seconds = int(start % 60)
        lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"Fetching transcript for: {VIDEO_URL}\n")
    transcript = fetch_transcript(VIDEO_ID)
    print(transcript)

    output_file = "transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Video: {VIDEO_URL}\n\n")
        f.write(transcript)
    print(f"\nTranscript saved to youtube/{output_file}")
