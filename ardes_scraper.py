import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import json


async def visit_pages_and_scrape(hrefs, page, laptops, scraped_items):
    """Visit each href and scrape additional data from each laptop's page."""
    for link in hrefs:
        # Navigate to each href (laptop detail page)
        href = "https://ardes.bg/" + link
        await page.goto(
            href, {"waitUntil": "networkidle2"}
        )  # Wait until network is idle

        # Get the content of the new page
        content = await page.content()

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        # Initialize a dictionary to hold the laptop data for this page
        laptop = {}

        # Extract laptop name (first part of h1 content before the comma)
        name = soup.find("h1").text.split(",")[0].strip()
        laptop["Име"] = name

        # Find the table body which contains all the laptop specifications
        tbody = soup.find("tbody")
        for tr in tbody.find_all("tr"):
            # Find each <th> (header) and <td> (data) pair inside the <tr>
            header = tr.find("th").text.strip(":").strip()
            if header not in headers:  # Skip headers not in our list
                continue
            data = tr.find_all("td")[-1].text.strip()  # Get the last <td> data (value)

            # Store each <th> and <td> pair in the laptop dictionary
            laptop[header] = data

        # Append the fully constructed laptop dictionary to the laptops list
        laptops.append(laptop)
        scraped_items += 1  # Increment the count of scraped items

        # Print progress for every successfully scraped item
        print(f"Successfully scraped item {scraped_items}: {href}")

    return laptops, scraped_items


async def get_browser_and_page(chrome_path: str, url: str):
    """Launch the browser, navigate to URL, and return the page object."""
    # Launch the browser with specified options
    browser = await launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-images",  # Disable images for faster loading
            "--disable-features=site-per-process",  # Reduces multi-process overhead
            "--disable-infobars",
        ],
        executablePath=chrome_path,  # Path to the Chrome executable
    )
    page = await browser.newPage()  # Open a new browser page
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    )  # Set a custom user-agent to simulate a real browser
    await page.setViewport({"width": 1280, "height": 800})  # Set viewport size

    # Navigate to the provided URL and wait until the page is fully loaded
    await page.goto(url, {"waitUntil": "networkidle2"})

    return browser, page


async def scrape_anchors(page):
    """Scrape all anchor tags containing a div with the 'image hint' class."""
    global next_button, next_link  # Declare as global so they can be accessed in the main function
    content = await page.content()  # Get the page content

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find the "next" button (pagination)
    next_button = soup.find(class_="next")  # Find the 'next' button element
    next_link = (
        next_button.find("a").get("href") if next_button else None
    )  # Get the href of the next page

    # Select all anchor tags containing a div with the 'image hint' class
    anchor_tags = soup.select("a > .image.hint")

    # Initialize a list to store all the hrefs of laptop product pages
    hrefs = []
    for anchor_tag in anchor_tags:
        parent_anchor = anchor_tag.find_parent("a")  # Find the parent anchor tag
        if parent_anchor:
            href = parent_anchor.get(
                "href"
            )  # Extract the href attribute (link to laptop details)
            hrefs.append(href)

    return hrefs


async def main():
    """Main function to orchestrate the scraping process."""
    scraped_items = 0  # Keep track of how many items have been scraped
    laptops = []  # List to store the scraped laptop data

    # Specify the path to your Chrome or Chromium executable
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Replace with your Chrome path

    # Define the target URL for the first page of laptops
    url = "https://ardes.bg/laptopi/laptopi"  # URL of the page to scrape

    # Launch the browser and get the page object
    browser, page = await get_browser_and_page(chrome_path, url)

    while True:
        # Scrape anchor links (links to individual laptop detail pages) from the current page
        hrefs = await scrape_anchors(page)

        # Scrape each linked page and retrieve laptop data
        laptops, scraped_items = await visit_pages_and_scrape(
            hrefs, page, laptops, scraped_items
        )

        # If no "next" button is found, break the loop (no more pages to scrape)
        if not next_link:
            print("No more pages to scrape.")
            break

        # Navigate to the next page using the next link found in the "next" button
        next_page_url = f"https://ardes.bg{next_link}"
        await page.goto(
            next_page_url, {"waitUntil": "networkidle2"}
        )  # Go to the next page
        print(f"Navigated to next page: {next_page_url}")

    # Save the scraped laptop data to a JSON file
    with open("laptops_data.json", "w", encoding="utf-8") as json_file:
        json.dump(laptops, json_file, ensure_ascii=False, indent=4)

    # Close the browser after the scraping is complete
    await browser.close()


# Global variables for next button and next link (used for pagination)
next_button = ""
next_link = ""

# Define headers for laptop specifications to extract
headers = [
    "Подходящ",
    "Процесор",
    "Видео карта",
    "Памет",
    "Твърд диск",
    "SSD диск",
    "Дисплей",
    "Камера",
    "Аудио",
    "Батерия",
    "Тегло",
    "Размери",
    "Цвят",
    "Операционна система",
]

# Run the main async function to start the scraping process
if __name__ == "__main__":
    asyncio.run(main())
