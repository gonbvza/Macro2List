def csv_to_hash(clean_rows):
    items = {}

    for row in clean_rows:
        # expected format: [item, weight(g), calories, protein, carbs, fat]
        if len(row) < 6:
            continue  # skip malformed rows

        item = row[0]
        try:
            weight = float(row[1].replace(" g", "").strip())
            calories = float(row[2])
            protein = float(row[3])
            carbs = float(row[4])
            fat = float(row[5])
        except ValueError:
            continue  # skip if conversion fails

        if item not in items:
            items[item] = {
                "weight": 0.0,
                "calories": 0.0,
                "protein": 0.0,
                "carbs": 0.0,
                "fat": 0.0,
            }

        # accumulate values
        items[item]["weight"] += weight
        items[item]["calories"] += calories
        items[item]["protein"] += protein
        items[item]["carbs"] += carbs
        items[item]["fat"] += fat

    return items


def pretty_print_hash(nutrition_hash):
    print(
        f"{'Item':<20} {'Weight(g)':>10} {'Calories':>10} {'Protein':>10} {'Carbs':>10} {'Fat':>10}"
    )
    print("-" * 70)
    for item, values in nutrition_hash.items():
        print(
            f"{item:<20} "
            f"{values['weight']:>10.1f} "
            f"{values['calories']:>10.1f} "
            f"{values['protein']:>10.1f} "
            f"{values['carbs']:>10.1f} "
            f"{values['fat']:>10.1f}"
        )
