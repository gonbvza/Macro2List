import json
import sys

from deep_translator import GoogleTranslator


def translate(products_array, output_file="translated_products.txt"):
    """
    Translate product names to English and save to a file.

    Args:
        products_array (list): List of product JSON strings.
        output_file (str): Path to save translated products.
    """
    translated_products = []
    phrases_to_replace = ["1 the best"]

    try:
        for product in products_array:
            product_json = json.loads(product)
            translated_name = (
                GoogleTranslator(source="auto", target="en")
                .translate(product_json["name"])
                .lower()
            )

            for phrase in phrases_to_replace:
                if phrase in translated_name:
                    translated_name = translated_name.replace(phrase, "").strip()
                    translated_name = f"{translated_name} dirk"

            translated_product = {
                "name": translated_name,
                "price": product_json["price"],
                "qty": product_json["qty"],
                "quantity_type": product_json["quantity_type"],
            }

            print(translated_product)
            translated_products.append(translated_product)

    # Adding this to save progess as progess was to long so i needed to work in between
    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C). Saving progress...")

    finally:
        # Save all translations so far
        with open(output_file, "a", encoding="utf-8") as f:
            for line in translated_products:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")

        print(f"Progress saved to {output_file}")
        sys.exit(0)
