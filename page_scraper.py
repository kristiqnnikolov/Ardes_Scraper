from bs4 import BeautifulSoup
from utils import headers

async def scrape_anchors(page):
    """Scrape all anchor tags containing a div with the 'image hint' class."""
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    # Find the "next" button for pagination
    next_button = soup.find(class_="next")
    next_link = next_button.find("a").get("href") if next_button else None

    # Find all laptop detail page links
    anchor_tags = soup.select("a > .image.hint")
    hrefs = [anchor_tag.find_parent("a").get("href") for anchor_tag in anchor_tags if anchor_tag.find_parent("a")]

    return hrefs, next_link


async def visit_pages_and_scrape(hrefs, page, laptops, scraped_items):
    """Visit each href and scrape additional data from each laptop's page."""
    for link in hrefs:
        href = "https://ardes.bg/" + link
        await page.goto(href, {"waitUntil": "networkidle2"})

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Initialize a dictionary to hold the laptop data
        laptop = {}

        # Get laptop name (first part of h1 content before the comma)
        name = soup.find("h1").text.split(",")[0].strip()
        laptop["Име"] = name

        # Find table body with specifications
        tbody = soup.find("tbody")
        for tr in tbody.find_all("tr"):
            header = tr.find("th").text.strip(":").strip()
            if header not in headers:  # Skip unwanted headers
                continue
            data = tr.find_all("td")[-1].text.strip()
            laptop[header] = data

        laptops.append(laptop)
        scraped_items += 1
        print(f"Successfully scraped item {scraped_items}: {href}")

    return laptops, scraped_items
