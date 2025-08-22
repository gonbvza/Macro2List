import json
import math

from src.utils import convert_to_grams


def calculate_from_grams(price, weight):
    """Calculate how many units are needed based on weight in grams."""
    price_amount = convert_to_grams(price["qty"])
    return weight / price_amount


def get_product_by_name(name, products_prices):
    """Return the product dict from the list matching the given name (case-insensitive)."""
    for product in products_prices:
        if product["name"].lower() == name.lower():
            return product
    return {"name": "", "price": "", "qty": "", "quantity_type": ""}


def add_prices(shopping_list):
    """
    Calculate needed quantities and total prices for a shopping list.
    Writes a neatly aligned summary to 'list.txt'.
    """
    with open("./translated.txt", "r") as file:
        products_prices = [json.loads(line.strip()) for line in file]

    finished_list = []

    for name, details in shopping_list.items():
        price = get_product_by_name(name, products_prices)
        if price["quantity_type"] == "GRAMS":
            needed_amount = calculate_from_grams(price, details["weight"])
            buy_amount = math.ceil(needed_amount)
            total_price = buy_amount * float(price["price"])
            finished_list.append(
                {
                    "name": name,
                    "amount": f"{round(details['weight'], 2)} g",
                    "needed": f"{round(needed_amount, 2)} packet",
                    "buy": f"{buy_amount} packet(s)",
                    "total_price": round(total_price, 2),
                }
            )

    total_buy_price = sum(item["total_price"] for item in finished_list)

    # Determine max lengths for proper alignment
    name_len = max(len(item["name"]) for item in finished_list) + 2
    amount_len = max(len(item["amount"]) for item in finished_list) + 2
    needed_len = max(len(item["needed"]) for item in finished_list) + 2
    buy_len = max(len(item["buy"]) for item in finished_list) + 2

    # Write aligned table
    with open("list.txt", "w") as txt_file:
        for item in finished_list:
            line = (
                f"{item['name']:<{name_len}}"
                f"{item['amount']:<{amount_len}}"
                f"Needed: {item['needed']:<{needed_len}}"
                f"Buy: {item['buy']:<{buy_len}}"
                f"Total Price: €{item['total_price']:.2f}"
            )
            txt_file.write(line + "\n")

        txt_file.write("\n")
        txt_file.write(f"Total price: €{total_buy_price:.2f}\n")
