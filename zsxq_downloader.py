#!/usr/bin/env python3
"""
zsxq_downloader.py — Download latest PDFs from a 知识星球 (zsxq.com) group.

Usage:
    python zsxq_downloader.py --count 10 --out ~/Downloads/zsxq_reports

Uses chrome_profile/ (same as tradingview.py / fetch_news.py) so no manual
cookie setup is needed — just make sure you're logged in to wx.zsxq.com in that profile.

API pattern:
    List files:    GET https://api.zsxq.com/v2/groups/{group_id}/files?count=N
    Download URL:  GET https://api.zsxq.com/v2/files/{file_id}/download_url
    File CDN:      https://files.zsxq.com/{hash}?attname={name}&e={expiry}&token={token}
"""

import argparse
import json
import os
import sys
import time
import re
import requests
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

API_BASE = "https://api.zsxq.com/v2"
SCRIPT_DIR = Path(__file__).parent
DEFAULT_CHROME_PROFILE = SCRIPT_DIR / "chrome_profile"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://wx.zsxq.com/",
    "Origin": "https://wx.zsxq.com",
}


def get_session_via_selenium(chrome_profile: Path) -> requests.Session:
    """Launch Chrome with the existing profile, visit zsxq, extract cookies into a requests Session."""
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={chrome_profile}")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("Starting Chrome to load session cookies...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    try:
        driver.get("https://wx.zsxq.com")
        time.sleep(2)  # let cookies load

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain", ""))
    finally:
        driver.quit()

    print(f"Loaded {len(session.cookies)} cookies from Chrome profile.\n")
    return session


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def get_files(session: requests.Session, group_id: str, count: int) -> list[dict]:
    url = f"{API_BASE}/groups/{group_id}/files"
    resp = session.get(url, params={"count": count}, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("succeeded"):
        raise RuntimeError(f"API error: {data.get('info') or data.get('error')}")
    return data["resp_data"]["files"]


def get_download_url(session: requests.Session, file_id: int) -> str | None:
    url = f"{API_BASE}/files/{file_id}/download_url"
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("succeeded"):
        return None
    return data["resp_data"]["download_url"]


def download_file(session: requests.Session, download_url: str, dest_path: Path) -> int:
    resp = session.get(download_url, stream=True, headers=HEADERS)
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
            written += len(chunk)
    return written


def load_tracker(tracker_path: Path) -> dict:
    if tracker_path.exists():
        return json.loads(tracker_path.read_text())
    return {}


def save_tracker(tracker_path: Path, tracker: dict):
    tracker_path.write_text(json.dumps(tracker, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Download latest PDFs from a zsxq group.")
    parser.add_argument("--group-id", default="51111812185184", help="zsxq group ID")
    parser.add_argument("--count", type=int, default=10, help="Number of files to download")
    parser.add_argument("--out", default="~/Downloads/zsxq_reports", help="Output directory")
    parser.add_argument("--chrome-profile", default=str(DEFAULT_CHROME_PROFILE),
                        help="Path to Chrome profile directory (default: ./chrome_profile)")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip already-downloaded files")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between downloads")
    args = parser.parse_args()

    chrome_profile = Path(args.chrome_profile).expanduser()
    if not chrome_profile.exists():
        print(f"ERROR: Chrome profile not found at {chrome_profile}")
        print("Make sure chrome_profile/ exists and you've logged into wx.zsxq.com with it.")
        sys.exit(1)

    session = get_session_via_selenium(chrome_profile)

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    tracker_path = out_dir / "downloaded.json"
    tracker = load_tracker(tracker_path)

    print(f"Fetching latest {args.count} files from group {args.group_id}...")
    files = get_files(session, args.group_id, args.count)
    print(f"Found {len(files)} files.\n")

    results = []
    for i, entry in enumerate(files, 1):
        f = entry["file"]
        file_id = f["file_id"]
        name = f["name"]
        size_mb = f["size"] / 1024 / 1024
        safe_name = sanitize_filename(name)
        dest = out_dir / safe_name

        print(f"[{i}/{len(files)}] {name[:70]}")
        print(f"         size={size_mb:.1f}MB  id={file_id}")

        if args.skip_existing and str(file_id) in tracker:
            print(f"         → already downloaded, skipping.\n")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
            continue

        dl_url = get_download_url(session, file_id)
        if not dl_url:
            print(f"         → failed to get download URL.\n")
            results.append({"file_id": file_id, "name": name, "status": "no_url"})
            continue

        try:
            written = download_file(session, dl_url, dest)
            tracker[str(file_id)] = {
                "name": name,
                "path": str(dest),
                "size": written,
                "downloaded_at": datetime.now().isoformat(),
            }
            save_tracker(tracker_path, tracker)
            print(f"         → saved {written/1024/1024:.1f}MB to {dest.name}\n")
            results.append({"file_id": file_id, "name": name, "status": "ok", "size": written})
        except Exception as e:
            print(f"         → download error: {e}\n")
            results.append({"file_id": file_id, "name": name, "status": "error", "error": str(e)})

        time.sleep(args.delay)

    ok = sum(1 for r in results if r["status"] == "ok")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] not in ("ok", "skipped"))
    print(f"Done: {ok} downloaded, {skipped} skipped, {failed} failed.")
    print(f"Output: {out_dir}")
    print(f"Tracker: {tracker_path}")


if __name__ == "__main__":
    main()
