import csv
import json
import re
import unicodedata
from propiedades.fix_csv import process_csv
from propiedades.property import Property
from excepciones.exception import ValueNotFound


def normalize_string(s):
    return unicodedata.normalize("NFD", s).casefold()


def extraer_caracteristicas(caracteristicas_str: str):
    caracteristicas_list = caracteristicas_str.split("\n")
    bandera_exterior = False
    bandera_interior = False
    bandera_sector = False

    exterior = []
    interior = []
    sector = []

    for value in range(1, len(caracteristicas_list)):
        if caracteristicas_list[value] == "características del exterior":
            bandera_exterior = True
            bandera_interior = False
            bandera_sector = False
        elif caracteristicas_list[value] == "características del interior":
            bandera_interior = True
            bandera_exterior = False
            bandera_sector = False
        elif caracteristicas_list[value] == "características del sector":
            bandera_sector = True
            bandera_interior = False
            bandera_exterior = False
        else:
            if bandera_exterior:
                exterior.append(caracteristicas_list[value])
            elif bandera_interior:
                interior.append(caracteristicas_list[value])
            elif bandera_sector:
                sector.append(caracteristicas_list[value])

    resultado = []

    exterior = [item for item in exterior if item]
    interior = [item for item in interior if item]
    sector = [item for item in sector if item]

    resultado.append(exterior)
    resultado.append(interior)
    resultado.append(sector)

    if all(not sublist for sublist in resultado):
        resultado = None
    else:
        resultado = resultado

    return resultado


def extraer_precio(precio_str):
    try:
        precio = re.findall(r'\d+', precio_str)
        return float(''.join(precio))
    except IndexError:
        ValueNotFound("There's not house price in the row")
        return None


def get_location(fila: str):
    try:
        location = [part.strip().lower() for part in fila.split('-')]
        return location
    except IndexError:
        ValueNotFound("There's not an location in the row")
        return None
    


def clean_string(s):
    return s.strip(' \'"')


def descomponer_informacion(info: str) -> dict:
    converted_list = eval(info)
    data_dict = {}
    for item in converted_list:
        items = item.split("\n")
        try:
            if items[0].isdigit():
                clave = items[1]
                valor = items[0]
            else:
                clave = items[0]
                valor = items[0]

            data_dict[clave] = valor
        except IndexError as e:
            raise ValueNotFound(f"Se encontró un elemento sin índice suficiente: {item}") from e

    # Mostrar las llaves y valores de cada inmueble
    for key, value in data_dict.items():
        print(f"{key}: {value}")
    print()

    return data_dict


def existe(llave, dicc):
    return dicc.get(llave)


def limitar_cadena(cadena, max_longitud=600):
    return cadena[:max_longitud]


def validar_ciudad(lst):
    try:
        lst[1]
    except IndexError:
        return None


def validar_departamento(lst):
    try:
        return lst[2]
    except IndexError:
        return None


def get_values(file, json_name):
    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        manejador = 0
        json_result = []

        while row is not None:
            propiedades = Property()

            contador = 0
            for key, value in row.items():
                if contador == 0:
                    propiedades.url = value
                elif contador == 1:
                    propiedades.nombre = value
                elif contador == 2:
                    propiedades.tipo = value
                elif contador == 3:
                    location = get_location(value)
                    propiedades.sector = location[0]
                    propiedades.ciudad = validar_ciudad(location)
                    propiedades.departamento = validar_departamento(location)
                elif contador == 4:
                    propiedades.descripcion = limitar_cadena(value)
                elif contador == 5:
                    propiedades.precio = extraer_precio(value)
                elif contador == 6:
                    informacion = descomponer_informacion(value)
                    propiedades.habitaciones = existe('habitaciones', informacion)
                    propiedades.parqueaderos = existe('parqueaderos', informacion)
                    propiedades.banos = existe('baños', informacion)
                    propiedades.estrato = existe('estrato', informacion)
                    propiedades.piso = existe('piso n°', informacion)
                    propiedades.administracion = existe('administración', informacion)
                    propiedades.precioM2 = existe('precio m²', informacion)
                    propiedades.estado = existe('estado', informacion)
                    propiedades.barrio_comun = existe('barrio_comun', informacion)
                elif contador == 8:
                    propiedades.antiguedad = value
                elif contador == 9:
                    propiedades.areaConstruida = value
                elif contador == 10:
                    propiedades.areaPrivada = value
                elif contador == 11:
                    var = None
                elif contador == 12:
                    var = None
                elif contador == 13:
                    var = None
                elif contador == 15:
                     caracteristicas = extraer_caracteristicas(value)
                     if caracteristicas is not None:
                         propiedades.caracteristicasDelExterior = caracteristicas[0]
                         propiedades.caracteristicasDelInterior = caracteristicas[1]
                         propiedades.caracteristicasDelSector = caracteristicas[2]
                     else:
                         propiedades.caracteristicasDelExterior = None
                         propiedades.caracteristicasDelInterior = None
                         propiedades.caracteristicasDelSector = None

                contador += 1

            manejador += 1
            try:
                row = next(reader)
            except StopIteration:
                break

            json_result.append(propiedades.json_out())

    with open(f'json_files/{json_name}.json', 'w', encoding="utf-8") as file:
        json.dump(json_result, file, indent=4, ensure_ascii=False)


def main(file, json_name):
    process_csv(file)
    get_values(file, json_name)


if __name__ == "__main__":
    main("csv_files/hotels_stmarta_bucaramanga_valledupar.csv", "hotels")
