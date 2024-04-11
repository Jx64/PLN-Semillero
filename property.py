class Property:
    def __init__(self):
        self.url = None
        self.nombre = None
        self.sector = None
        self.tipo = None
        self.precio= 0 #validar
        self.descripcion = None #validar
        self.habitaciones = 0
        self.baños = 0
        self.parqueaderos = 0
        self.address = None
        self.ciudad= None #validar
        self.departamento= None #validar
        self.pais= "colombia"  #validar
        self.areaPrivada = None
        self.antiguedad = None
        self.precioM2 = 0.0 #validar
        self.estrato = 0
        self.areaConstruida = None
        self.piso = 0
        self.estado = None
        self.administracion = 0.0
        self.caracteristicasDelExterior= None
        self.caracteristicasDelInterior= None
        self.caracteristicasDelSector= None

    def get_caracteristicas(self):
        json = []
            
        if self.caracteristicasDelExterior != None:     
            for item in self.caracteristicasDelExterior:
                    json_data = {
                        "tipoDeCaracteristica": {
                            "nombre": "Caracteristicas del exterior"
                        },
                        "nombre": item
                    }
                    json.append(json_data)
                    
        if self.caracteristicasDelInterior != None:     
            for item in self.caracteristicasDelInterior:
                json_data = {
                    "tipoDeCaracteristica": {
                        "nombre": "Caracteristicas del interior"
                    },
                    "nombre": item
                }
                json.append(json_data)
                    
        if self.caracteristicasDelSector != None:     
            for item in self.caracteristicasDelSector:
                json_data = {
                    "tipoDeCaracteristica": {
                        "nombre": "Caracteristicas del sector"
                    },
                    "nombre": item
                }
                json.append(json_data)       
            
        if(len(json)!=0):       
            return json
        else:
            return None    

    def json_out(self):
        if self.ciudad is not None:
            jsonUnic = {
                "sector": {
                    "nombre": self.sector
                },
                "ciudad": {
                    "departamento": {
                        "pais": {
                            "nombre": self.pais
                        },
                        "nombre": self.departamento
                    },
                    "nombre": self.ciudad
                },
                "tipoDeInmueble": {
                    "nombre": self.tipo
                },
                "caracteristicas": self.get_caracteristicas(),
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "estrato": (self.estrato),
                "cantidadDeHabitaciones": (self.habitaciones),
                "cantidadDeBaños": (self.baños),
                "cantidadDeParqueaderos": (self.parqueaderos),
                "piso": (self.piso),
                "antiguedad": self.antiguedad,
                "precioM2": self.precioM2,
                "url": self.url,
                "areaPrivada": self.areaPrivada,
                "areaConstruida": self.areaConstruida,
                "precioAdministracion": self.administracion,
                "precio": self.precio,
                "estado": self.estado,
                "direccion": self.address    
            }    
        else:
            jsonUnic = {
                "sector": {
                    "nombre": self.sector
                },
                "ciudad": None,
                "tipoDeInmueble": {
                    "nombre": self.tipo
                },
                "caracteristicas": self.get_caracteristicas(),
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "estrato": (self.estrato),
                "cantidadDeHabitaciones": (self.habitaciones),
                "cantidadDeBaños": (self.baños),
                "cantidadDeParqueaderos": (self.parqueaderos),
                "piso": (self.piso),
                "antiguedad": self.antiguedad,
                "precioM2": self.precioM2,
                "url": self.url,
                "areaPrivada": self.areaPrivada,
                "areaConstruida": self.areaConstruida,
                "precioAdministracion": self.administracion,
                "precio": self.precio,
                "estado": self.estado,
                "direccion": self.address
            }
            
        return jsonUnic         