import sys
from pathlib import Path

from src import read_csv
from src.csv_to_hash import csv_to_hash, pretty_print_hash
from src.scrapper.scrap import scrap, scrap_products
from src.scrapper.translate import translate


def main():
    if len(sys.argv) < 2:
        print("Usage: python shopping_list.py <file.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"Error: File {file_path} not found")
        sys.exit(1)

    data = read_csv(file_path)
    shopping_list = csv_to_hash(data)
    # pretty_print_hash(shopping_list)

    with open("./links.txt", "r") as file:
        product_links = [line.rstrip() for line in file]

    with open("./products.txt", "r") as file:
        product_array = [line.rstrip() for line in file]

    translate(product_array)


if __name__ == "__main__":
    main()
