import csv


def characters(file):
    new_csv = []
    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        for row in reader:
            new_row = {key: value.lower() if isinstance(value, str) else value for key, value in row.items()}
            new_csv.append(new_row)

    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_csv)

    return new_csv

