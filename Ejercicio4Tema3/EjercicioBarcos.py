class Barco:
    def __init__(self,nombre,posiciónX,posiciónY,velocidad,rumbo,munición):
        self.nombre = nombre
        self.posiciónX = posiciónX
        self.posiciónY = posiciónY
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.munición = munición

    def moverse(self):
        """Se desplaza en la posición X"""
        self.posiciónX += 1
        self.posiciónY += 1

    def aumento_velocidad(self):
        """Posee una velocidad"""
        self.velocidad += 1

    def cambiar_rumbo(self):
        """Rumbo"""
        if (self.rumbo < 359) and (self.rumbo > 0):
            self.rumbo += 1
        else:
            print("Error")

    def disparar(self):
        "Munición restante"
        if (self.munición > 0):
            self.munición -= 1
        else:
            print(f"{self.nombre} se ha quedado sin balas.")

    def __str__(self):
        return (f"{self.nombre} se desplaza. Nueva posición: X = {self.posiciónX}\n"
        f"{self.nombre} se desplaza. Nueva posición: Y = {self.posiciónY}\n"
        f"{self.nombre} tiene ahora una velocidad de {self.velocidad} nudos.\n"
        f"{self.nombre} se mueve {self.rumbo} grados\n"
        f"{self.nombre} ha disparado! Munición restante: {self.munición}\n")

#----------PROGRAMA PRINCIPAL----------#
if __name__ == "__main__":
#CREAR BARCOS
    Barco1 = Barco(nombre = "Titanic", posiciónX = 100, posiciónY = 200, velocidad = 70, rumbo = 189, munición = 10)
    Barco2 = Barco(nombre = "SpeedStar", posiciónX = 360, posiciónY = 100, velocidad = 130, rumbo = 302, munición = 5)
    Barco3 = Barco(nombre = "BlindWall", posiciónX = 230, posiciónY = 178, velocidad = 50, rumbo = 67, munición = 20)

#ESTABLECER ACCIONES
print("Opciones del barco 1")
Barco1.moverse()
Barco1.aumento_velocidad()
Barco1.cambiar_rumbo()
Barco1.disparar()
print(Barco1)
print("----------------------------------------------------------")
print("Opciones del barco 2")
Barco2.moverse()
Barco2.aumento_velocidad()
Barco2.cambiar_rumbo()
Barco2.disparar()
print(Barco2)
print("----------------------------------------------------------")
print("Opciones del barco 3")
Barco3.moverse()
Barco3.aumento_velocidad()
Barco3.cambiar_rumbo()
Barco3.disparar()
print(Barco3)