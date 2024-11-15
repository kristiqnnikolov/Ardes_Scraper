import asyncio
from browser_setup import get_browser_and_page
from page_scraper import scrape_anchors, visit_pages_and_scrape
import json


async def main():
    """Main function to orchestrate the scraping process."""
    scraped_items = 0  # Track how many items have been scraped
    laptops = []  # Store scraped laptop data

    # Path to Chrome or Chromium executable
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # Initial URL for the first page
    url = "https://ardes.bg/laptopi/laptopi"

    # Launch the browser and get the page object
    browser, page = await get_browser_and_page(chrome_path, url)

    while True:
        # Scrape anchor links (links to individual laptop detail pages) from the current page
        hrefs, next_link = await scrape_anchors(page)

        # Scrape each linked page and retrieve laptop data
        laptops, scraped_items = await visit_pages_and_scrape(
            hrefs, page, laptops, scraped_items
        )

        # If no "next" button is found, end the loop
        if not next_link:
            print("No more pages to scrape.")
            break

        # Navigate to the next page
        next_page_url = f"https://ardes.bg{next_link}"
        await page.goto(next_page_url, {"waitUntil": "networkidle2"})
        print(f"Navigated to next page: {next_page_url}")

    # Save the scraped data to a JSON file
    with open("laptops_data.json", "w", encoding="utf-8") as json_file:
        json.dump(laptops, json_file, ensure_ascii=False, indent=4)

    # Close the browser
    await browser.close()


# Run the main async function to start the scraping process
if __name__ == "__main__":
    asyncio.run(main())
