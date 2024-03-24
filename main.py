import csv, json, re

import fix_csv
from property import Property


def modificar_caracteristicas(caracteristicas_str):
    print(caracteristicas_str)
    caracteristicas = caracteristicas_str.split('}, ')
    caracteristicas = [re.sub(r"[\[\]{}']", '', carac) for carac in caracteristicas]
    caracteristicas = [carac.split(",") for carac in caracteristicas]
    print(caracteristicas)

    dict_caracteristicas = {}
    for carac in caracteristicas:
        pass
    return caracteristicas


def extraer_precio(precio_str):
    # hacer expresion regular
    precio = re.findall(r'\d+', precio_str)
    if precio:
        return int(''.join(precio))
    else:
        return None


def obtener_localicaciones_cercanas(locaciones_cercanas):
    nuevas_locaciones = locaciones_cercanas.lower().split(", ")
    for locacion in nuevas_locaciones:
        if "d.c." == locacion:
            nuevas_locaciones.remove(locacion)
    return nuevas_locaciones


def getValues(file):
    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        first_row = next(reader)

        json_output = {}
        for key, value in first_row.items():
            # if key == 'row':
            #   json_output[key] = value
            json_output[key] = value

        print(json.dumps(json_output, indent=4, ensure_ascii=False))


def main(file):
    fix_csv.characters(file)
    getValues(file)


if __name__ == "__main__":
    main("hotels.csv")
