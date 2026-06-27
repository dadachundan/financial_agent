#!/usr/bin/env python3
"""
login_zsxq.py — Interactive login script for ZSXQ (知识星球).

Launches a Chrome window using the workspace-local Chrome profile so the user
can log in (e.g., via WeChat QR scan). Once logged in, it detects the session
cookie, closes Chrome, and flushes the cookies to disk.
"""

import os
import sys
import time
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("ERROR: Missing required dependencies.")
    print("Please run: pip install selenium webdriver-manager")
    sys.exit(1)

def main():
    script_dir = Path(__file__).parent.absolute()
    chrome_profile_dir = script_dir / "chrome_profile"
    chrome_profile_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Using Chrome profile directory: {chrome_profile_dir}")
    
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={chrome_profile_dir}")
    # Disable automation banners to reduce detection risk
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    print("Launching Chrome browser...")
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    except Exception as e:
        print(f"\nERROR: Failed to launch Chrome: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Google Chrome is installed on your Mac.")
        print("2. Ensure any other Chrome instances using the profile directory are closed:")
        print(f"   Profile path: {chrome_profile_dir}")
        sys.exit(1)
        
    try:
        print("\nOpening 知识星球 (ZSXQ) login page...")
        driver.get("https://wx.zsxq.com/dweb2/index/")
        
        print("\n" + "=" * 60)
        print(" ACTION REQUIRED:")
        print(" Please log in to ZSXQ in the Chrome window that just opened.")
        print(" (e.g. by scanning the QR code with WeChat or the ZSXQ app)")
        print("=" * 60 + "\n")
        
        print("Waiting for login session...")
        logged_in = False
        while not logged_in:
            try:
                # Retrieve cookies from driver
                cookies = driver.get_cookies()
                token_cookie = next((c for c in cookies if c['name'] == 'zsxq_access_token'), None)
                if token_cookie:
                    print(f"\nSuccess! Found 'zsxq_access_token' cookie.")
                    
                    # Extract and save cookies to local JSON file
                    import json
                    zsxq_cookies = {c['name']: c['value'] for c in cookies if 'zsxq.com' in c.get('domain', '')}
                    cookie_json_path = chrome_profile_dir / "zsxq_cookies.json"
                    with open(cookie_json_path, "w", encoding="utf-8") as f:
                        json.dump(zsxq_cookies, f, indent=2)
                    print(f"Saved {len(zsxq_cookies)} cookies to {cookie_json_path}")
                    
                    logged_in = True
                    break
            except Exception as e:
                # Browser might have been closed by user
                print(f"\nBrowser closed or error check failed: {e}")
                break
            time.sleep(2)
            
        if logged_in:
            print("Session cookie detected. Closing Chrome in 3 seconds to flush cookies to disk...")
            time.sleep(3)
            
    finally:
        print("Closing Chrome browser...")
        try:
            driver.quit()
            print("Chrome closed successfully. Cookies have been saved!")
        except Exception:
            pass

if __name__ == "__main__":
    main()
