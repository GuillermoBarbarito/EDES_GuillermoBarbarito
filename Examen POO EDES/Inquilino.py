from Vivienda import Vivienda

class Inquilino:
    def __init__(self, nombre, dni, telefono, vivienda):
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono
        self.vivienda = Vivienda(vivienda)
    def name(self):
        self.nombre
    def DNI(self):
        self.dni
    def TELÉFONO(self):
        self.telefono
    def casita_en_la_que_vive(self):
        self.vivienda
    
    def __str__(self):
        return(f"Nombre: {self.nombre}"
        f"DNI: {self.dni}"
        f"Teléfono: {self.telefono}"
        f"Vivienda actual: {self.vivienda}")