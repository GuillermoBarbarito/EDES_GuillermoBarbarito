class Vivienda:
    def __init__(self, calle, numero, ciudad, metrosCuadrados, precioAlquiler, estado, inquilino):
        self.calle = calle
        self.numero = numero
        self.ciudad = ciudad
        self.metrosCuadrados = metrosCuadrados
        self.precioAlquiler = precioAlquiler
        self.estado = estado
        self.inquilino = inquilino
    def calle_donde_vive(self):
        self.calle
    def numero_de_vivienda(self):
        self.numero
    def ciudad_de_vivienda(self):
        self.ciudad
    def metros_cuadrados(self):
        self.metros_cuadrados
    def precio_del_alquiler(self):
        self.precioAlquiler
    def estado_actual(self):
        self.estado
    def inquilino_actual(self):
        self.inquilino
    
    def __str__(self):
        return(f"Calle: {self.calle}"
        f"Número: {self.numero}"
        f"Ciudad: {self.ciudad}"
        f"Metros cuadrados: {self.metrosCuadrados}"
        f"Precio del alquiler: {self.precioAlquiler}"
        f"Estado: {self.estado}"
        f"Inquilino actual {self.inquilino}")