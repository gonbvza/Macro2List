import csv

keywords = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
keywords_to_remove = {
    "Calorías",
    "Proteína",
    "Proteínas",
    "Calorias",
    "Carbohidratos",
    "Grasas",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "Total",
    "Comida",
    "Cuanto comes?",
    "Totals",
    "3100",
    "100 g",
    "\ufeffMonday",
}


def read_csv(path: str):
    with open(path, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        return clean_csv(spamreader)


def clean_csv(spamreader):
    clean_rows = []
    for row in spamreader:
        line = ";".join(row)
        if line.strip("; \n") == "":
            continue
        line = line.replace(",", ".")
        parts = [p.strip() for p in line.split(";") if p.strip()]
        if parts[0] in keywords_to_remove:
            continue
        if parts[0] in keywords:
            del parts[0]
        if parts:
            clean_rows.append(parts)

    return clean_rows
