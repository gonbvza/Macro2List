"""
shopping_list.py

Main script for generating a shopping list with total prices.

Workflow:
1. Reads a CSV file containing food items and nutritional information.
2. Cleans and converts CSV data into a structured dictionary.
3. Optionally scrapes product links and product details from a website.
4. Translates product names to English.
5. Calculates the total prices for the shopping list based on the scraped product prices.

Usage:
    python shopping_list.py <file.csv>

Dependencies:
- Selenium for web scraping
- deep_translator for translation
"""

import sys
from pathlib import Path

from src import read_csv
from src.csv_to_hash import csv_to_hash, pretty_print_hash
from src.list_prices import add_prices
from src.scrapper.scrap import scrap, scrap_products
from src.scrapper.translate import translate


def main():
    """
    Main entry point for the shopping list workflow.

    Steps:
    1. Checks command line arguments for CSV input file.
    2. Reads and cleans CSV data using read_csv and csv_to_hash.
    3. Pretty prints the nutritional information.
    4. Scrapes product links and product details from the website.
    5. Translates product names to English.
    6. Calculates needed quantities and total prices, writing the results to a file.

    Raises:
        SystemExit: If no CSV file is provided or the file does not exist.
    """
    if len(sys.argv) < 2:
        print("Usage: python shopping_list.py <file.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"Error: File {file_path} not found")
        sys.exit(1)

    # Step 1: Read and clean CSV
    data = read_csv(file_path)
    shopping_list = csv_to_hash(data)

    # Step 2: Pretty print nutritional info
    pretty_print_hash(shopping_list)

    # Step 3: Scrape product links
    scrap()
    with open("links.txt", "r", encoding="utf-8") as file:
        product_links = [line.strip() for line in file]

    # Step 4: Scrape product details
    scrap_products(product_links)
    with open("products.txt", "r", encoding="utf-8") as file:
        product_array = [line.strip() for line in file]

    # Step 5: Translate products
    translate(product_array)

    # Step 6: Calculate total prices
    add_prices(shopping_list)


if __name__ == "__main__":
    main()
