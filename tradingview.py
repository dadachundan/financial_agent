from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
chrome_options = Options()
# Use a separate profile directory to avoid conflicts with running Chrome
# You'll need to log in manually the first time this runs
chrome_options.add_argument("user-data-dir=/Users/x/projects/financial_agent/chrome_profile")

# Initialize the Chrome driver with automatic driver management
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to TradingView
    driver.get("https://www.tradingview.com/")

    # Wait for the page to load
    time.sleep(3)

    # Look for watchlist link/button
    try:
        # Try to find watchlist by common selectors
        watchlist_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Watchlist')]"))
        )
        watchlist_button.click()
        print("Watchlist found and clicked")

        # Wait for watchlist to load
        time.sleep(2)

        # Print current URL to confirm navigation
        print(f"Current URL: {driver.current_url}")

    except Exception as e:
        print(f"Could not find watchlist button: {e}")
        print("You may need to log in first or the watchlist is in a different location")

    # Extract and print watchlist items
    try:
        # Wait for watchlist items to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'watchlist')]//tr"))
        )

        # Get all watchlist items
        watchlist_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'watchlist')]//tr")
        print(f"\nWatchlist items ({len(watchlist_items)}):")
        for item in watchlist_items:
            print(f"  - {item.text}")
    except Exception as e:
        print(f"Could not extract watchlist items: {e}")

    # Keep browser open for inspection
    print("Browser will stay open for 60 seconds...")
    print(f"Current URL: {driver.current_url}")
    time.sleep(360)

except Exception as e:
    print(f"Error occurred: {e}")
    time.sleep(10)

finally:
    driver.quit()
    print("Browser closed.")
