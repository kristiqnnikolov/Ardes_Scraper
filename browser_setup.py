from pyppeteer import launch

async def get_browser_and_page(chrome_path: str, url: str):
    """Launch the browser, navigate to URL, and return the page object."""
    browser = await launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-images",  # Disable images for faster loading
            "--disable-features=site-per-process",
            "--disable-infobars",
        ],
        executablePath=chrome_path,
    )
    page = await browser.newPage()
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    )
    await page.setViewport({"width": 1280, "height": 800})
    await page.goto(url, {"waitUntil": "networkidle2"})
    
    return browser, page
