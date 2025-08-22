def convert_to_grams(quantity: str) -> float:
    """
    Convert a quantity string to grams.

    Examples:
    "100 g" -> 100
    "2.5 kg" -> 2500
    """
    quantity = quantity.strip().lower()
    if "kg" in quantity:
        return float(quantity.replace("kg", "").strip()) * 1000
    elif "g" in quantity:
        return float(quantity.replace("g", "").strip())
    else:
        raise ValueError("Unsupported unit. Only 'g' and 'kg' are allowed.")
