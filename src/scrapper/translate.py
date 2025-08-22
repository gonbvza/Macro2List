import json
import sys

from deep_translator import GoogleTranslator


def translate(products_array, output_file="translated_products.txt"):
    translated_products = []
    phrases_to_replace = ["1 the best"]

    try:
        for product in products_array:
            product_json = json.loads(product)

            translated = (
                GoogleTranslator(source="auto", target="en")
                .translate(product_json["name"])
                .lower()
            )

            for phrase in phrases_to_replace:
                if phrase in translated:
                    translated = translated.replace(phrase, "").strip()
                    translated = f"{translated} dirk"

            translated_product = {
                "name": translated,
                "price": product_json["price"],
                "qty": product_json["qty"],
                "quantity_type": product_json["quantity_type"],
            }

            print(translated_product)
            translated_products.append(translated_product)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user (Ctrl+C). Saving progress...")

    finally:
        # Always save what we have so far
        with open(output_file, "a", encoding="utf-8") as txt_file:
            for line in translated_products:
                txt_file.write(json.dumps(line, ensure_ascii=False) + "\n")

        print(f"✅ Progress saved to {output_file}")
        sys.exit(0)
