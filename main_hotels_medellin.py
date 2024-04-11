import csv, json, re
import fix_csv
from property import Property
import unicodedata

def normalize_string(s):
    return unicodedata.normalize("NFD", s).casefold()

def extraer_caracteristicas(caracteristicas:str):
    for key in caracteristicas:
        print(key)
        print(caracteristicas[key])

    # bandera_exterior = False
    # bandera_interior = False
    # bandera_sector = False

    # exterior = []
    # interior = []
    # sector = []

    # for value in range(1,len(caracteristicas_list)):
    #     if caracteristicas_list[value] == "características del exterior":
    #         bandera_exterior = True
    #         bandera_interior =False
    #         bandera_sector =False
    #     elif caracteristicas_list[value] == "características del interior":
    #         bandera_interior = True
    #         bandera_exterior =False
    #         bandera_sector =False
    #     elif caracteristicas_list[value] == "características del sector":
    #         bandera_sector = True
    #         bandera_interior =False
    #         bandera_exterior =False
    #     else:
    #         if bandera_exterior == True:
    #             exterior.append(caracteristicas_list[value])
    #         elif bandera_interior == True:
    #             interior.append(caracteristicas_list[value])
    #         elif bandera_sector == True:
    #             sector.append(caracteristicas_list[value])

    # resultado = []

    # exterior = [item for item in exterior if item]
    # interior = [item for item in interior if item]
    # sector = [item for item in sector if item]
    
    # resultado.append(exterior)
    # resultado.append(interior)
    # resultado.append(sector)

    # if all(not sublist for sublist in resultado):
    #     resultado = None
    # else:
    #     resultado = resultado

    # return resultado

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
    diccionario = {}
    for value in converted_list:
        if type(value) == dict:
            caracteristicas = value
        else:
            value_list = value.split("\n")
            if value_list[0].isdigit():
                numero = value_list[0]
                text = value_list[1]
            else:
                numero = value_list[1]
                text = value_list[0]
            
            diccionario[text] = numero
        
    descomposicion = []
    descomposicion.append(caracteristicas)
    descomposicion.append(diccionario)

    return descomposicion


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
                # print(value)
                if contador == 0:
                    propiedades.url = value
                elif contador == 1:
                    propiedades.nombre = value
                elif contador == 3:
                    propiedades.descripcion = limitar_cadena(value)
                elif contador == 4:
                    propiedades.precio = extraer_precio(value)
                elif contador == 5:  
                    informacion = (descomponer_informacion(value))[1]
                    # print(str(informacion))    
                    propiedades.habitaciones= existe('valor administración',informacion)
                    propiedades.parqueaderos= existe('parqueaderos',informacion)
                    propiedades.baños=existe('habitaciones',informacion)
                    propiedades.areaPrivada=existe('baños',informacion)
                    propiedades.estrato=existe('estrato',informacion)
                    propiedades.antiguedad=existe('valor arriendo',informacion)
            
                    caracteristicas = extraer_caracteristicas((descomponer_informacion(value))[0])
                    # if caracteristicas != None:
                        # propiedades.caracteristicasDelExterior = caracteristicas[0]
                        # propiedades.caracteristicasDelInterior = caracteristicas[1]
                        # propiedades.caracteristicasDelSector = caracteristicas[2]
                    # else:
                        # propiedades.caracteristicasDelExterior = None
                        # propiedades.caracteristicasDelInterior = None
                        # propiedades.caracteristicasDelSector = None
                elif contador == 6:
                    propiedades.sector = value
                    propiedades.ciudad = validar_ciudad("medellin") 
                    propiedades.departamento = validar_departamento("antioquia")
                elif contador == 7:
                    propiedades.antiguedad = (value)
                elif contador == 8:
                    propiedades.areaConstruida = value
                elif contador == 9:
                    propiedades.areaPrivada = value
                
                
                contador+=1
                
            manejador+=1
            if manejador == 3:
                break
            
            try:
                row = next(reader)
            except:
                break
            
            jsonResult.append(propiedades.json_out())
            

    with open('hotels_medellin.json', 'w',encoding="utf-8") as file:
        json.dump(jsonResult,file, indent=4, ensure_ascii=False)


def main(file):
    fix_csv.characters(file)
    getValues(file)


if __name__ == "__main__":
    main("hotels_Medellin_metrocuadrado.csv")
