import os
import json
import time
from dotenv import load_dotenv, find_dotenv

from selenium import webdriver
from bs4 import BeautifulSoup


def get_page_source(catalog_url):
    """Get page html"""
    load_dotenv(find_dotenv())
    browser = webdriver.Chrome(os.environ.get("BROWSER_URL"))
    try:
        browser.get(catalog_url)
        time.sleep(5)

        with open("data/page_source.html", "w", encoding='utf-8') as file:
            file.write(browser.page_source)

    except Exception as _ex:
        print(_ex)

    finally:
        browser.close()
        browser.quit()
        print("[INFO] Page source collected!")


def get_page_items():
    """Get items from source page"""
    with open("data/page_source.html", encoding='utf-8') as file:
        page = file.read()

    soup = BeautifulSoup(page, "lxml")
    products = soup.find_all("div", class_="product-card")

    data = []
    for item in products:
        url = "https://street-beat.ru" + item.find("a", class_="product-card__info").get('href')
        name = item.find("a", class_="product-card__info").text.strip()
        new_price = item.find("span", class_="product-card__price-new").text.strip()
        old_price = item.find("span", class_="product-card__price-old").text.strip()
        sizes = [s.text.strip() for s in item.find_all("label", class_="radio__label")]

        data.append(
            {
                "url": url,
                "name": name,
                "new_price": new_price,
                "old_price": old_price,
                "sizes": sizes
            }
        )

    with open("data/data.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("[INFO] Data collected!")
