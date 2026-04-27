import os
import time
import re
import pathlib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# ── CONFIG ────────────────────────────────────────────────────────────────────
CSV_IN  = os.path.join(os.path.dirname(__file__), "../Data/clean/airbnb_cleaningdata.csv")
CSV_OUT = os.path.join(os.path.dirname(__file__), "../Data/clean/airbnb_cleaningdata.csv")

DELAY_BETWEEN_PAGES = 3   # seconds to wait after loading each listing page
SAVE_EVERY          = 20  # save progress to CSV every N listings (crash protection)
# ─────────────────────────────────────────────────────────────────────────────


def setup_driver():
    """Set up Chrome in a way that looks like a real browser to Airbnb."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")               # Linux-compatible headless flag
    options.add_argument("--no-sandbox")             # required on Linux
    options.add_argument("--disable-dev-shm-usage")  # required on Linux VMs
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def parse_bedroom_bathroom(text: str):
    """
    Given a string like '· 2 bedrooms · 1 bathroom ·' or '· Studio · 1 bath ·'
    return (bedrooms, bathrooms) as strings, or None if not found.
    """
    text = text.lower()

    # --- bedrooms ---
    bedrooms = None
    if re.search(r'\bstudio\b', text):
        bedrooms = "0 (studio)"
    else:
        m = re.search(r'(\d+)\s+bedroom', text)
        if m:
            bedrooms = m.group(1)

    # --- bathrooms ---
    bathrooms = None
    m = re.search(r'([\d.]+)\s+(?:private\s+|shared\s+|attached\s+|half-)?bath', text)   
    if m:
        bathrooms = m.group(1)

    return bedrooms, bathrooms


def scrape_bedrooms_bathrooms(driver, wait, url: str):
    """
    Visit a single Airbnb listing page and extract bedrooms + bathrooms.
    Returns (bedrooms, bathrooms) — either a number string or None.
    """
    try:
        driver.get(url)
        time.sleep(DELAY_BETWEEN_PAGES)

        # Strategy 1 — the overview list items (most reliable)
        selectors = [
            "ol.lgx66tx",
            "ol[class*='lgx66tx']",
            "div[data-section-id='OVERVIEW_DEFAULT'] ol",
            "div[data-section-id='OVERVIEW_DEFAULT_V2'] ol",
        ]

        raw_text = None
        for sel in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            if elements:
                raw_text = elements[0].text
                break

        # Strategy 2 — grab ALL <li> inside overview section
        if not raw_text:
            overview_divs = driver.find_elements(
                By.XPATH,
                "//div[contains(@data-section-id,'OVERVIEW')]//li"
            )
            if overview_divs:
                raw_text = " · ".join(el.text for el in overview_divs)

        # Strategy 3 — scan page for bedroom/bath keywords
        if not raw_text:
            candidates = driver.find_elements(
                By.XPATH,
                "//*[contains(text(),'bedroom') or contains(text(),'bath') or contains(text(),'studio')]"
            )
            for el in candidates:
                t = el.text.strip()
                if len(t) < 200:
                    raw_text = t
                    break

        if raw_text:
            bedrooms, bathrooms = parse_bedroom_bathroom(raw_text)
            return bedrooms, bathrooms

    except Exception as e:
        print(f"    !! Error on {url}: {e}")

    return None, None


def main():
    # ── Load CSV ──────────────────────────────────────────────────────────────
    df = pd.read_csv(CSV_IN)
    print(f"Loaded {len(df)} listings from CSV.")
    print(f"Columns: {list(df.columns)}")

    # Add columns if they don't exist yet (so we can resume a crashed run)
    if "bedrooms" not in df.columns:
        df["bedrooms"] = None
    if "bathrooms" not in df.columns:
        df["bathrooms"] = None

    # Only scrape rows that haven't been filled yet — lets you resume safely
    pending = df[df["bedrooms"].isna()].index.tolist()
    print(f"{len(pending)} listings still need bedrooms/bathrooms.\n")

    if not pending:
        print("Nothing to scrape — all rows already have bedrooms/bathrooms!")
        return

    # ── Start browser ─────────────────────────────────────────────────────────
    print("Starting Chrome... (this may take a moment the first time)")
    driver = setup_driver()
    wait   = WebDriverWait(driver, 15)

    try:
        for i, idx in enumerate(pending, start=1):
            url = df.at[idx, "url"]
            listing_id = df.at[idx, "id"]

            print(f"[{i}/{len(pending)}] Scraping listing {listing_id} ...")
            bedrooms, bathrooms = scrape_bedrooms_bathrooms(driver, wait, url)

            df.at[idx, "bedrooms"]  = bedrooms
            df.at[idx, "bathrooms"] = bathrooms
            print(f"    → bedrooms={bedrooms}, bathrooms={bathrooms}")

            # Save progress every SAVE_EVERY listings so a crash doesn't lose everything
            if i % SAVE_EVERY == 0:
                df.to_csv(CSV_OUT, index=False)
                print(f"    💾 Progress saved ({i} done so far).")

            time.sleep(1)

    finally:
        driver.quit()

    # ── Final save ────────────────────────────────────────────────────────────
    df.to_csv(CSV_OUT, index=False)
    filled = df["bedrooms"].notna().sum()
    print(f"\nDone! {filled}/{len(df)} listings now have bedrooms/bathrooms.")
    print(f"Updated CSV saved to: {os.path.abspath(CSV_OUT)}")


if __name__ == "__main__":
    main()