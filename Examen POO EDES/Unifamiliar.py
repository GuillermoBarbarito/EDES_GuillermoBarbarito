from Vivienda import Vivienda

class Unifamiliar(Vivienda):
    def __init__(self, calle, numero, ciudad, metrosCuadrados, precioAlquiler, estado, inquilino):
        super().__init__(calle, numero, ciudad, metrosCuadrados, precioAlquiler, estado, inquilino)
        self.plazaAparcamiento = True
        self.tienePatio = True
        self.tieneJardín = True
        self.estáAdosada = True
    def aparcamiento(self):
        if self.plazaAparcamiento == False:
            print(f"La unifamiliar número {self.numero} de la calle {self.calle} no tiene una plaza"
                "de aparcamiento propia.")
    def patio(self):
        if self.tienePatio == False:
            print(f"La unifamiliar número {self.numero} de la calle {self.calle} no tiene una patio.")
    def jardín(self):
        if self.tieneJardín == False:
            print(f"La unifamiliar número {self.numero} de la calle {self.calle} no tiene un jardín.")
    def adosada(self):
        if self.estáAdosada == False:
            print(f"La unifamiliar número {self.numero} de la calle {self.calle} es una vivienda aislada.")
    
    def __str__(self):
        base = super().__str__()
        base + "\n"
        return (f"Tipo: Unifamiliar"
                f"Aparcamiento: {self.aparcamiento}"
                f"Patio: {self.patio}"
                f"Jardín: {self.jardín}"
                f"Adosada: {self.adosada}")