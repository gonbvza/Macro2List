# Macro2List

Macro2List is a Python project designed to process a CSV-based nutrition plan, scrape product prices from an online grocery store, translate product names, and generate a shopping list with aligned quantities and prices.

## Overview

The workflow is:

1. ### CSV Reading and Cleaning

`read_csv.py` reads a CSV file with nutritional data.

`clean_csv` removes irrelevant rows (like headers, totals, or weekdays) and formats numbers.

`csv_to_hash` converts the cleaned CSV rows into a dictionary of items with accumulated nutrition values.

`pretty_print_hash` allows a nicely formatted console output of the nutrition summary.

2. ### Weight and Quantity Calculations

`weight_utils.py` provides conversion between grams and kilograms.

`list_prices.py` contains:

- calculate_from_grams: computes how many product units are needed based on weight.

- get_product_by_name: retrieves a product from the scraped prices by name.

- add_prices: calculates total cost, needed quantities, and outputs a neatly aligned shopping list.

3. ### Web Scraping

`scrap.py` uses Selenium to:

- Navigate a grocery website.

- Collect all product links by category (scrap).

- Parse product details like name, price, and quantity (parse_product).

- Save product data to a JSON file (scrap_products).

4. ### Translation

`translate.py` uses GoogleTranslator to translate product names from Dutch to English.

- Handles specific phrases and saves translated products to a file.

`shopping_list.py`:

- Reads the CSV nutrition plan.

- Generates a nutrition hash.

- Runs scraping and translation of products.

- Calculates and prints the shopping list with required quantities and total prices.

5. ### Output

```
Bread:          1120.0 g  Needed: 1.87 packet  Buy: 2 packet(s)  Total Price: €2.96
Minced Meat:    1000.0 g  Needed: 1.0 packet   Buy: 1 packet(s)  Total Price: €10.99
...
Total price: €72.45
´´´
```
