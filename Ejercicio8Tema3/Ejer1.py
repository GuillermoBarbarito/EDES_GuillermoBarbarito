class PlataformaNaval:
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima):
        self.nombre = nombre
        self.pais = pais
        self.eslora = eslora
        self.desplazamiento = desplazamiento
        self.velocidadMaxima = velocidadMaxima
        self.velocidad = 0
        self.rumbo = 0
        self.danio = False
        self.esta_detenido = False
        self.operativa = True
        self.destruida = False

    def navegar(self):
        if 0 <= self.rumbo <= 359:
            self.rumbo = (self.rumbo + 1) % 360
        else:
            print("Error: rumbo fuera de rango")
        self.velocidad += 1
        print(f"{self.nombre} navega a {self.velocidad} nudos con rumbo {self.rumbo}°.")

    def detenerse(self):
        if self.velocidad == 0:
            self.esta_detenido = True
            print(f"{self.nombre} se ha detenido")
        else:
            print(f"{self.nombre} aún se mueve a {self.velocidad} nudos.")

    def recibirdanio(self):
        self.danio = True
        print(f"¡{self.nombre} ha recibido un impacto directo!")

    def comprobar_operativa(self):
        if self.destruida:
            self.operativa = False
            print(f"¡{self.nombre} ha sido destruido!")


class Fragata(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima,
                misilesAntiaereos, helicopterosEmb, rolPrincipal, municion):
        super().__init__(nombre, pais, eslora, desplazamiento, velocidadMaxima)
        self.misilesAntiaereos = misilesAntiaereos
        self.helicopterosEmb = helicopterosEmb
        self.rolPrincipal = rolPrincipal
        self.municion = municion
        self.capitan = None

    def disparar(self):
        if self.municion > 0:
            self.municion -= 1
            print(f"{self.nombre} ha disparado un misil AA. Munición restante: {self.municion}")
        else:
            print(f"{self.nombre} no tiene munición")

    def despegar(self):
        if self.helicopterosEmb > 0:
            self.helicopterosEmb -= 1
            print(f"Ha despegado un helicóptero en {self.nombre}, ahora quedan {self.helicopterosEmb}")
        else:
            print(f"{self.nombre} no tiene helicópteros disponibles")

    def asignar_capitan(self, capitan):
        self.capitan = capitan
        print(f"Se ha asignado al capitán {capitan.nombre} a {self.nombre}")


class Corbeta(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima, rolPrincipal):
        super().__init__(nombre, pais, eslora, desplazamiento, velocidadMaxima)
        self.rolPrincipal = rolPrincipal

    def patrullar(self, costera=True):
        tipo = "costera" if costera else "oceánica"
        print(f"{self.nombre} está patrullando en zona {tipo}.")


class Submarino(PlataformaNaval):
    def __init__(self, nombre, pais, eslora, desplazamiento, velocidadMaxima, rolPrincipal, torpedos):
        super().__init__(nombre, pais, eslora, desplazamiento, velocidadMaxima)
        self.rolPrincipal = rolPrincipal
        self.torpedos = torpedos

    def sumergirse(self):
        print(f"{self.nombre} se sumerge en las profundidades.")

    def detectar_contacto(self):
        print(f"{self.nombre} detecta un contacto enemigo.")

    def lanzar_torpedo(self):
        if self.torpedos > 0:
            self.torpedos -= 1
            print(f"{self.nombre} lanza un torpedo. Torpedos restantes: {self.torpedos}")
        else:
            print(f"{self.nombre} no tiene torpedos disponibles.")


class Capitan:
    def __init__(self, nombre):
        self.nombre = nombre


class Flota:
    def __init__(self):
        self.plataformas = []

    def agregar(self, plataforma):
        self.plataformas.append(plataforma)

    def mostrar_info(self):
        for p in self.plataformas:
            print(f"\n--- {p.nombre} ---")
            print(f"País: {p.pais}, Eslora: {p.eslora}m, Desplazamiento: {p.desplazamiento}t, Velocidad máxima: {p.velocidadMaxima}kn")
            print(f"Rol: {getattr(p, 'rolPrincipal', 'N/A')}")
            if isinstance(p, Fragata) and p.capitan:
                print(f"Capitán: {p.capitan.nombre}")
            print(f"Daño: {'Sí' if p.danio else 'No'}")
            print(f"Detenido: {'Sí' if p.esta_detenido else 'No'}")
            if isinstance(p, Fragata):
                print(f"Misiles AA: {p.misilesAntiaereos}, Munición: {p.municion}, Helicópteros: {p.helicopterosEmb}")
            if isinstance(p, Submarino):
                print(f"Torpedos: {p.torpedos}")


# --- Simulación ---
fragata = Fragata("Fragata F-100", "España", 146, 5800, 28, misilesAntiaereos=48, helicopterosEmb=2, rolPrincipal="Defensa aérea", municion=10)
corbeta = Corbeta("Corbeta C-80", "España", 90, 2500, 25, rolPrincipal="Patrulla costera")
submarino = Submarino("Submarino S-80", "España", 81, 3000, 20, rolPrincipal="Guerra submarina", torpedos=6)

capitan = Capitan("Juan Pérez")
fragata.asignar_capitan(capitan)

flota = Flota()
flota.agregar(fragata)
flota.agregar(corbeta)
flota.agregar(submarino)

print("\n=== Información inicial de la Flota ===")
flota.mostrar_info()
# Acciones
fragata.disparar()
fragata.despegar()
corbeta.patrullar(costera=True)
submarino.sumergirse()
submarino.detectar_contacto()
submarino.lanzar_torpedo()

# Daño y cambios
corbeta.recibirdanio()
corbeta.destruida = True
corbeta.comprobar_operativa()

print("\n=== Información final de la Flota ===")
flota.mostrar_info()