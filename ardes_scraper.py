import asyncio
from browser_setup import get_browser_and_page
from page_scraper import scrape_anchors, visit_pages_and_scrape
import json


async def main():
    scraped_items = 0  
    laptops = [] 

    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    url = "https://ardes.bg/laptopi/laptopi"

    browser, page = await get_browser_and_page(chrome_path, url)

    while True:
        hrefs, next_link = await scrape_anchors(page)

        laptops, scraped_items = await visit_pages_and_scrape(
            hrefs, page, laptops, scraped_items
        )

        if not next_link:
            print("No more pages to scrape.")
            break

        next_page_url = f"https://ardes.bg{next_link}"
        await page.goto(next_page_url, {"waitUntil": "networkidle2"})
        print(f"Navigated to next page: {next_page_url}")

    with open("laptops_data.json", "w", encoding="utf-8") as json_file:
        json.dump(laptops, json_file, ensure_ascii=False, indent=4)

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
