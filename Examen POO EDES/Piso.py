from Vivienda import Vivienda

class Piso(Vivienda):
    def __init__(self, calle, numero, ciudad, metrosCuadrados, precioAlquiler, estado, inquilino,
                planta, puerta):
        super().__init__(calle, numero, ciudad, metrosCuadrados, precioAlquiler, estado, inquilino)
        self.planta = planta
        self.puerta = puerta
        self.tieneGaraje = True
        self.tieneTrastero = True
    def PLANTA(self):
        self.planta
    def PUERTA(self):
        self.puerta
    def garaje(self):
        if self.tieneGaraje == False:
            print(f"El piso {self.puerta} de la planta {self.planta} de la calle {self.calle}"
                "no tiene garaje.")
    def trastero(self):
        if self.tieneTrastero == False:
            print(f"El piso {self.puerta} de la planta {self.planta} de la calle {self.calle}"
                "no tiene trastero.")
    
    def __str__(self):
        base = super().__str__()
        base + "\n"
        return(f"Tipo: Piso"
            f"Planta: {self.planta}"
            f"Puerta: {self.puerta}"
            f"Garaje: {self.garaje}"
            f"Trastero: {self.trastero}")