import csv

def read_csv(file):
    data = []
    try:
        with open(file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"El archivo {file} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
    return data


def convert_to_lowercase(data):
    for row in data:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.lower()
    return data


def write_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Ocurrió un error al escribir en el archivo CSV: {e}")


def process_csv(input_file):
    try:
        data = read_csv(input_file)
        if data:
            lowercase_data = convert_to_lowercase(data)
            write_csv(lowercase_data, input_file)
        else:
            raise ValueError("No hay datos para procesar en el archivo CSV.")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo CSV: {e}")