import csv, json, re


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


def main():
    # en open el 'r' significa lectura y lo de encoding utf-8 detecta carasteres latinoamericano
    with open('hotels.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)  # lee todas las filas
        first_row = next(reader)  # Lee todas las columnas

        json_output = {}
        for key, value in first_row.items():
            if key == 'asociate_location':
                json_output[key] = obtener_localicaciones_cercanas(value)
            elif key == 'price':
                json_output[key] = extraer_precio(value)
            elif key == 'feats':
                json_output[key] = modificar_caracteristicas(value)
            else:
                json_output[key] = value

        json_str = json.dumps(json_output, indent=4, ensure_ascii=False)
        print(json_str)


if __name__ == "__main__":
    main()
