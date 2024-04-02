import csv, json, re
import fix_csv
from property import Property
import unicodedata

def normalize_string(s):
    return unicodedata.normalize("NFD", s).casefold()

def extraer_caracteristicas(caracteristicas_str:str):
    caracteristicas_list = caracteristicas_str.split("\n")
    bandera_exterior = False
    bandera_interior = False
    bandera_sector = False

    exterior = []
    interior = []
    sector = []

    for value in range(1,len(caracteristicas_list)):
        if caracteristicas_list[value] == "características del exterior":
            bandera_exterior = True
            bandera_interior =False
            bandera_sector =False
        elif caracteristicas_list[value] == "características del interior":
            bandera_interior = True
            bandera_exterior =False
            bandera_sector =False
        elif caracteristicas_list[value] == "características del sector":
            bandera_sector = True
            bandera_interior =False
            bandera_exterior =False
        else:
            if bandera_exterior == True:
                exterior.append(caracteristicas_list[value])
            elif bandera_interior == True:
                interior.append(caracteristicas_list[value])
            elif bandera_sector == True:
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
    precio = re.findall(r'\d+', precio_str)
    if precio:
        return float(''.join(precio))
    else:
        return None


def get_location(fila:str):
    location = fila.split('-')

    for i in range(0,len(location)):
        location[i] = location[i].strip()
        location[i] = location[i].lower()
        location[i] = (location[i])

    return location

def clean_string(s):
    return s.strip(' \'"')

def descomponer_informacion(info:str):
    converted_list = eval(info)
    data_dict = {}

    for item in converted_list:
        if isinstance(item, dict):
            data_dict.update({clean_string(k): clean_string(v) for k, v in item.items()})

    return data_dict

def existe(llave, dicc):
    if llave in dicc:
        return (dicc[llave])
    else:
        return None

def limitar_cadena(cadena, max_longitud=600):
    if len(cadena) > max_longitud:
        cadena = cadena[:max_longitud]
        cadena = (cadena)
        
    return cadena

def validar_ciudad(list):
    try:
        return (list[1])
    except:
        return None
    
def validar_departamento(list):
    try:
        return (list[2])
    except:
        return None


def getValues(file):
    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)
        manejador = 0
        jsonResult = []

        while row != None:
            propiedades = Property()
            
            contador = 0
            for key,value in row.items():
                if contador == 0:
                    propiedades.url = value
                elif contador == 1:
                    propiedades.nombre = value
                elif contador == 2:
                    location = get_location(value)
                    propiedades.sector = location[0]
                    propiedades.ciudad = validar_ciudad(location) 
                    propiedades.departamento = validar_departamento(location)
                elif contador == 4:
                    propiedades.tipo = value
                elif contador == 5:
                    propiedades.descripcion = limitar_cadena(value)
                elif contador == 6:
                    propiedades.precio = extraer_precio(value)
                elif contador == 7:  
                    # print(value)
                    informacion = descomponer_informacion(value)                    
                    propiedades.habitaciones= existe('habitaciones',informacion)
                    propiedades.parqueaderos= existe('parqueaderos',informacion)
                    propiedades.baños=existe('baños',informacion)
                    propiedades.areaPrivada=existe('área privada',informacion)
                    propiedades.areaConstruida=existe('área construída',informacion)
                    propiedades.estrato=existe('estrato',informacion)
                    propiedades.antiguedad=existe('antigüedad',informacion)
                    propiedades.piso=existe('piso n°',informacion)
                    propiedades.administracion=existe('administración',informacion)
                    propiedades.precioM2=existe('precio m²',informacion)
                    propiedades.estado=existe('estado',informacion)
                    propiedades.tipo=existe('tipo de apartamento',informacion)
                elif contador == 8:
                    propiedades.address = value
                elif contador == 10:
                    caracteristicas = extraer_caracteristicas(value)
                    if caracteristicas != None:
                        propiedades.caracteristicasDelExterior = caracteristicas[0]
                        propiedades.caracteristicasDelInterior = caracteristicas[1]
                        propiedades.caracteristicasDelSector = caracteristicas[2]
                    else:
                        propiedades.caracteristicasDelExterior = None
                        propiedades.caracteristicasDelInterior = None
                        propiedades.caracteristicasDelSector = None
                
                contador+=1
                
            manejador+=1
            # if manejador == 10:
            #     break
            
            try:
                row = next(reader)
            except:
                break
            
            jsonResult.append(propiedades.json_out())
            

    with open('hotels.json', 'w',encoding="utf-8") as file:
        json.dump(jsonResult,file, indent=4, ensure_ascii=False)


def main(file):
    fix_csv.characters(file)
    getValues(file)


if __name__ == "__main__":
    main("hotels.csv")
