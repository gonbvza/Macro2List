import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.scrapper.enums import QuantityType

categories = [
    "aardappelen-groente-fruit",
    "vlees-vis",
    "brood-beleg-koek",
    "zuivel-kaas",
    "dranken-sap-koffie-thee",
    "voorraadkast",
    "maaltijden-salades-tapas",
    "diepvries",
    "huishoud-huisdieren",
    "kind-drogisterij",
    "non-food",
    "snacks-snoep",
]


def scrap():
    """Scrape all product links from Dirk.nl by category and save to 'output.txt'."""
    driver = webdriver.Chrome()
    driver.get("https://www.dirk.nl/boodschappen")
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)
    product_links = []

    for category in categories:
        print(f"Scraping category: {category}")
        try:
            link = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"a.department[href='/boodschappen/{category}']")
                )
            )
            link.click()

            elems = driver.find_element(By.CLASS_NAME, "right")
            inner_elems = elems.find_elements(By.XPATH, ".//a[@href]")

            for elem in inner_elems:
                href = elem.get_attribute("href")
                if href:
                    product_links.append(href)
        except Exception as e:
            print(f"Error scraping {category}: {e}")

        driver.get("https://www.dirk.nl/boodschappen")  # reload main page

    with open("output.txt", "w", encoding="utf-8") as f:
        for link in product_links:
            f.write(link + "\n")


def parse_product(product_specs):
    """
    Parse product details into a structured dictionary.

    Returns keys: name, price, qty, quantity_type.
    """
    # Remove unwanted items
    to_remove = [
        i for i in product_specs if "ACTIE" in i or ("van" in i and len(i.split()) == 2)
    ]
    for item in to_remove:
        product_specs.remove(item)

    try:
        if len(product_specs) > 3:
            price = f"{product_specs[0]}.{product_specs[1]}"
            name = product_specs[2]
            qty = product_specs[3]
        else:
            price = f"0.{product_specs[0]}"
            name = product_specs[1]
            qty = product_specs[2]
    except IndexError:
        print("Failed to parse:", product_specs)
        return {}

    if "stuk" in qty and "g" not in qty:
        quantity_type = QuantityType.STUK
    elif "ml" in qty:
        quantity_type = QuantityType.MILILITERS
    else:
        quantity_type = QuantityType.GRAMS

    return {
        "name": name,
        "price": price,
        "qty": qty,
        "quantity_type": quantity_type.name,
    }


def scrap_products(product_links):
    """Scrape product details from given links and save to 'products.txt'."""
    driver = webdriver.Chrome()
    driver.get("https://www.dirk.nl/boodschappen")
    driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 1)

    products = []

    for link in product_links:
        driver.get(link)
        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
        except TimeoutException:
            print("No products found, skipping link.")
            continue

        articles = driver.find_elements(By.XPATH, ".//article")
        for article in articles:
            specs = article.text.split("\n")
            parsed = parse_product(specs)
            if parsed:
                products.append(parsed)

    with open("products.txt", "w", encoding="utf-8") as f:
        for product in products:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")

    driver.quit()
