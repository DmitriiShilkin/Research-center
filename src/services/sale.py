import asyncio
import json
from typing import Tuple, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from constants.sale import (
    WEB_DRIVER_WAIT_MAX_TIMEOUT,
    KEYWORD_SEND_TIMEOUT,
    PAGE_LOAD_WAIT_MAX_TIMEOUT,
    URLS,
    KEY_WORDS,
)

clicked_once = False

# Настройка WebDriver для работы с браузером (например, Chrome)
options = webdriver.ChromeOptions()
# Включает режим без открывания окна браузера
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


async def keyword_check(keyword: str) -> str:
    if keyword == 'копье':
        keyword = f'{keyword} оружие'

    if keyword == 'красные носки':
        keyword = f'"{keyword}"'

    return keyword


async def get_wildberries_data(url: str, keyword: str) -> Tuple:
    keyword = await keyword_check(keyword)
    # Перейти на сайт и выполнить поиск
    driver.get(url)
    search_box = WebDriverWait(driver, WEB_DRIVER_WAIT_MAX_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, 'searchInput'))
    )
    await asyncio.sleep(KEYWORD_SEND_TIMEOUT)
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    # Ждем загрузки страницы
    await asyncio.sleep(PAGE_LOAD_WAIT_MAX_TIMEOUT)

    # Парсинг страницы с BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # селектор для карточек товара
    products = soup.select('.product-card')
    min_price = float('inf')
    min_product = None

    for product in products:
        # селектор для цены товара
        price_text = product.select_one('ins.price__lower-price').text
        price = float(price_text.replace('\xa0', '').replace('₽', '').strip())

        if price < min_price:
            min_price = price
            min_product = product

    # селектор для заголовка товара
    title = min_product.select_one('a').get('aria-label')
    # селектор для ссылки на товар
    link = min_product.select_one('a').get('href')

    return title, min_price, link


async def get_ozon_data(url: str, keyword: str) -> Tuple:
    global clicked_once
    keyword = await keyword_check(keyword)
    # Перейти на сайт и выполнить поиск
    driver.get(url)
    if not clicked_once:
        refresh_button = WebDriverWait(driver, WEB_DRIVER_WAIT_MAX_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "reload-button"))
        )
        refresh_button.click()
        clicked_once = True
    search_box = WebDriverWait(driver, WEB_DRIVER_WAIT_MAX_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"]'))
    )
    await asyncio.sleep(KEYWORD_SEND_TIMEOUT)
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    await asyncio.sleep(PAGE_LOAD_WAIT_MAX_TIMEOUT)

    # Парсинг страницы с BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # селектор для данных о товарах
    data_states = soup.select('div[data-state]')
    products = []
    for div in data_states:
        data_state = div.get('data-state')
        if 'tileLayout' in data_state:
            try:
                data_state_json = json.loads(data_state)
                for item in data_state_json['items']:
                    products.append((item['action']['link'], item['mainState']))
            except json.JSONDecodeError:
                # Игнорировать, если data-state не является корректным JSON
                continue
    min_price = float('inf')
    min_product = None
    title = None
    price_index = None
    title_index = None

    for product in products:
        for i in range(len(product[1])):
            if 'priceV2' in product[1][i]['atom']:
                price_index = i
            if 'textAtom' in product[1][i]['atom']:
                title_index = i
        # селектор для цены товара
        price_text = product[1][price_index]['atom']['priceV2']['price'][0]['text']
        price = float(price_text.replace('\u2009', '').replace('₽', '').strip())

        if price < min_price:
            min_price = price
            min_product = product
            # селектор для заголовка товара
            title = min_product[1][title_index]['atom']['textAtom']['text']

    # селектор для ссылки на товар
    link = f"{url}{min_product[0].split('?')[0]}"

    return title, min_price, link


async def get_yandex_data(url: str, keyword: str) -> Tuple:
    keyword = await keyword_check(keyword)
    # Перейти на сайт и выполнить поиск
    driver.get(url)
    search_box = WebDriverWait(driver, WEB_DRIVER_WAIT_MAX_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, 'header-search'))
    )
    await asyncio.sleep(KEYWORD_SEND_TIMEOUT)
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    await asyncio.sleep(PAGE_LOAD_WAIT_MAX_TIMEOUT)

    # Парсинг страницы с BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # селектор для карточек товара
    product_snippets = soup.select('div[data-baobab-name="productSnippet"]')
    products = []
    product_snippet_json = None
    link = None
    title = None

    for div in product_snippets:
        product_snippet = div.find('div', class_='cia-vs cia-cs').get('data-zone-data')

        if 'title' in product_snippet:
            try:
                product_snippet_json = json.loads(product_snippet)
            except json.JSONDecodeError:
                # Игнорировать, если product_snippet не является корректным JSON
                continue

        # селектор для ссылки на товар
        link_div = div.find('div', class_='m4M-1')
        if link_div:
            link = link_div.select_one('a').get('href')

        # селектор для заголовка товара
        title_div = div.find('div', class_='_1hTHv _1bekK _1MOwX _1bCJz')
        if title_div:
            title = title_div.select_one('img').get('alt')

        if product_snippet_json:
            # селектор для цены товара
            price = product_snippet_json['price']['value']
            products.append((price, title, link))

    min_price = float('inf')
    min_product = None

    for product in products:
        price_text = product[0]
        price = float(price_text)

        if price < min_price:
            min_price = price
            min_product = product

    title = min_product[1]
    link = f"{url}{min_product[2].split('?')[0]}"

    return title, min_price, link


async def find_min_price_products(data: Dict) -> Dict:
    result = {}

    if data:
        products = set(key.split('-', 1)[1] for key in data)
        for product in products:
            result[product] = min(
                (value for key, value in data.items() if key.split('-', 1)[1] == product),
                key=lambda item: item['price']
            )

    return result


async def check_prices() -> Dict:
    result = {}
    title = None
    price = None
    link = None

    for site, url in URLS.items():
        for keyword in KEY_WORDS:
            if site == 'wildberries':
                title, price, link = await get_wildberries_data(url, keyword)

            if site == 'ozon':
                title, price, link = await get_ozon_data(url, keyword)

            if site == 'yandex':
                title, price, link = await get_yandex_data(url, keyword)

            result.update({
                f'{site}-{keyword}': {
                    'title': title,
                    'price': price,
                    'link': link
                }
            })

    min_price_products = await find_min_price_products(result)

    return min_price_products
