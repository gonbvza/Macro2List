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
    driver = webdriver.Chrome()
    driver.get("https://www.dirk.nl/boodschappen")

    driver.implicitly_wait(10)  # Wait for JS content to load

    wait = WebDriverWait(driver, 10)

    product_links = []

    for category in categories:
        print(category)

        link = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"a.department[href='/boodschappen/{category}']")
            )
        )
        link.click()

        # Wait until the 'right' div is present
        inner_elems = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='right']//a[@href]")
            )
        )
        # Find all links inside the right div
        try:
            elems = driver.find_element(By.CLASS_NAME, "right")
            inner_elems = elems.find_elements(By.XPATH, ".//a[@href]")

            for elem in inner_elems:
                href = elem.get_attribute("href")
                if href:
                    product_links.append(href)
        except Exception as e:
            print(f"Error scraping {category}: {e}")

        # Go back to main category page by reloading
        driver.get("https://www.dirk.nl/boodschappen")

    with open("output.txt", "w") as txt_file:
        for line in product_links:
            txt_file.write(line + "\n")


def parse_product(product_specs):
    """
    Converts a product list into a dictionary with keys:
    - name: product name
    - price: price as string
    - qty: quantity/weight
    """
    items_remove = []
    for item in product_specs:
        if "ACTIE" in item:
            items_remove.append(item)
        if "van" in item and len(item.split(" ")) == 2:
            items_remove.append(item)

    for item in items_remove:
        product_specs.remove(item)

    product_price = ""
    product_name = ""
    product_weight = ""
    quantity_type = QuantityType.GRAMS
    try:
        if len(product_specs) > 3:
            product_price = f"{product_specs[0]}.{product_specs[1]}"
            product_name = product_specs[2]
            product_weight = product_specs[3]
        else:
            product_price = f"0.{product_specs[0]}"
            product_name = product_specs[1]
            product_weight = product_specs[2]
    except IndexError:
        print(product_specs)
        return product_specs

    if "stuk" in product_weight and "g" not in product_weight:
        quantity_type = QuantityType.STUK
    elif "ml" in product_weight:
        quantity_type = QuantityType.MILILITERS
    else:
        quantity_type = QuantityType.GRAMS

    return {
        "name": product_name,
        "price": product_price,
        "qty": product_weight,
        "quantity_type": quantity_type.name,
    }


def scrap_products(product_links):
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
            # nothing found, just continue
            print("continue")
            continue
        products_articles = driver.find_elements(By.XPATH, ".//article")

        for product in products_articles:
            product_specs = product.text.split("\n")
            # print(product_specs)
            parsed_product = parse_product(product_specs)
            products.append(parsed_product)

    with open("products.txt", "w") as txt_file:
        for line in products:  # line is a dict
            txt_file.write(json.dumps(line) + "\n")
    driver.quit()
