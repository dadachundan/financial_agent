from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import anthropic
from config import MINIMAX_API_KEY

# Set up Minimax as Anthropic-compatible API
os.environ["ANTHROPIC_BASE_URL"] = "https://api.minimax.io/anthropic"
os.environ["ANTHROPIC_API_KEY"] = MINIMAX_API_KEY

# Initialize Anthropic client
client = anthropic.Anthropic()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/Users/x/projects/financial_agent/chrome_profile")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to TopHub
    driver.get("https://tophub.today/")

    # Wait for the page to load
    time.sleep(3)

    # Get page content
    page_content = driver.find_element(By.TAG_NAME, "body").text
    print(f"Content length: {len(page_content)} characters")
    print("\n--- TopHub Content ---")
    print(page_content[:1000])  # Print first 1000 chars

    # Send to Minimax for summarization using Anthropic-compatible API
    try:
        message = client.messages.create(
            model="MiniMax-M2.5",
            max_tokens=1024,
            system="You are a financial news analyst. Provide concise, actionable insights.",
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following news content in 3-5 key points:\n\n{page_content[:5000]}"
                }
            ]
        )

        print("\n--- Minimax Summary ---")
        for content_block in message.content:
            if content_block.type == "text":
                print(content_block.text)

    except Exception as e:
        print(f"Could not send to Minimax: {e}")

    # Keep browser open for inspection
    print("\nBrowser will stay open for 60 seconds...")
    time.sleep(600)

except Exception as e:
    print(f"Error occurred: {e}")
    time.sleep(10)

finally:
    driver.quit()
    print("Browser closed.")
