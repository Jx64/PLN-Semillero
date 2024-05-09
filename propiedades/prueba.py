import re

cadena = "ascensor baños de servicio circuito cerrado de tv parqueadero visitantes piscina vista panorámica conjunto cerrado portería terraza/balcón balcón cancha(s) de basket cancha(s) de fútbol gimnasio zona de bbq zona para niños zonas verdes"
palabras_clave = re.findall(r'\b\w+(?:\(s\))*\b', cadena)

print(palabras_clave)