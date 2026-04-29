import json
import os
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_reviews_ui(driver, wait):
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(1)

    locator = (By.CSS_SELECTOR, "[data-testid='pdp-show-all-reviews-button']")
    items = []
    if driver.find_elements(*locator):
        b = driver.find_element(*locator)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", b)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", b)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[@data-review-id]")))
            items = driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@data-review-id]")
        except TimeoutException:
            try:
                driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            except Exception:
                pass
            items = driver.find_elements(By.XPATH, "//div[@data-review-id]")
    else:
        items = driver.find_elements(By.XPATH, "//div[@data-review-id]")

    seen, out = set(), []
    for it in items:
        rid = it.get_attribute("data-review-id") or ""
        if rid in seen:
            continue
        seen.add(rid)

        rating = "N/A"
        try:
            rs = it.find_element(By.XPATH, ".//span[contains(@aria-label,'out of 5') or contains(text(),'Rating') or contains(text(),'out of 5')]")
            rating = re.sub(r"[^0-9.]", "", rs.get_attribute("aria-label") or rs.text)
        except Exception:
            pass

        text = ""
        try:
            text = it.find_element(By.XPATH, ".//*[self::span or self::div][string-length(normalize-space(text())) > 30]").get_attribute("textContent")
        except Exception:
            text = it.text or it.get_attribute("textContent") or ""
        text = text.replace("Show more", "").strip()
        if len(text) > 10:
            out.append({"text": text, "rating": rating or "N/A"})

    try:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    except Exception:
        pass
    return out

def main():
    # Load your scraped data
    json_path = os.path.join(os.path.dirname(__file__), r'..\\Data\\clean\\airbnbdata.json')
    if not os.path.exists(json_path):
        print(f"Could not find {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        listings = json.load(f)

    # Extract just the room IDs
    room_ids = [str(listing['id']) for listing in listings]
    print(f"Extracted {len(room_ids)} room IDs.")

    all_reviews = []
    
    print("Starting Selenium to fetch reviews... (This may take a while)")
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        for room_id in room_ids:
            try:
                url = f"https://www.airbnb.com/rooms/{room_id}?locale=en-US"
                print(f"Scraping reviews for room: {room_id}")
                driver.get(url)
                time.sleep(3)  # let page load
                
                # Use the exact same logic you built in Crawler.py
                reviews = get_reviews_ui(driver, wait)
                
                for rev in reviews:
                    all_reviews.append({
                        "room_id": room_id,
                        "rating": rev.get("rating"),
                        "comments": rev.get("text")
                    })
                    
                print(f"  -> Got {len(reviews)} reviews for {room_id}")
                
            except Exception as e:
                print(f"  -> Error fetching reviews for {room_id}: {e}")
                
            # small delay between properties
            time.sleep(2)
            
    finally:
        driver.quit()

    # Save all reviews to a CSV
    reviews_df = pd.DataFrame(all_reviews)
    csv_out = os.path.join(os.path.dirname(__file__), "airbnb_reviews.csv")
    reviews_df.to_csv(csv_out, index=False)
    print(f"\nFinished saving {len(all_reviews)} total reviews into {csv_out}.")

if __name__ == "__main__":
    main()