from Vivienda import Vivienda
from Inquilino import Inquilino
from Piso import Piso
from Unifamiliar import Unifamiliar

if __name__=="__main__":
    inquilino1 = Inquilino("Fran", "43458721F", 956359854, Unifamiliar)
    inquilino2 = Inquilino("Pepe", "84759210P", 685490341, Unifamiliar)
    inquilino3 = Inquilino("Will", "28950393W", 920517424, Piso)

    Unifamiliar1 = Unifamiliar("Calle España", 3, "San Francisco", 500, 3000, "Ocupada0", inquilino1)
    Unifamiliar2 = Unifamiliar("Calle Mayorquín", 9, "Chiclana", 250, 1200, "Libre")
    Unifamiliar3 = Unifamiliar("Calle Fruta", 5, "San Fernando", 125, 800, "Ocupada", inquilino2)

    piso1 = Piso("Calle Pepa", 1, "Cádiz", 200, 600, "Ocupada", inquilino3, 9, 2)
    piso2 = Piso("Calle Pepa", 1, "Cádiz", 150, 400, "Libre", 4, 1)

print(inquilino1)
print(inquilino2)
print(inquilino3)