This project is a web scraping tool that uses Pyppeteer and BeautifulSoup to extract data about laptops from https://ardes.bg/laptopi/laptopi.

The scraped data is stored in JSON format for easy use and further analysis.
The project is specifically set up to run with Google Chrome.

Setup is pretty straight forward:

Install Required Packages:
```bash
pip install -r requirements.txt
```

Run the Scraper:
```bash
python ardes_scraper.py
```

Each laptop info is stored in a JSON file with the following structure:
```json
{
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
}
```
