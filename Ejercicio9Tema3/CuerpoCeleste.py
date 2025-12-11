# CUERPOS NATURALES

import random
import time


class CuerpoCeleste:
    def __init__(self, nombre, tipo, sistemaEstelar, masa, velocidadActual,
                atraccion, radiacion, observacion, evolucion, año):
        self.nombre = nombre
        self.tipo = tipo
        self.sistemaEstelar = sistemaEstelar
        self.masa = masa
        self.velocidadActual = velocidadActual
        self.atraccion = atraccion
        self.radiacion = radiacion
        self.observacion = observacion
        self.evolucion = evolucion
        self.año = año
        self.satelites = []

    def __str__(self):
        return (f"{self.tipo} {self.nombre}, que se encuentra en {self.sistemaEstelar}, "
                f"tiene una masa de {self.masa} Kg y una velocidad de {self.velocidadActual}.")

    def cambiar_velocidad(self):
        self.velocidadActual += 1

    def atraccion_gravedad(self, gravedad):
        self.atraccion = float(gravedad)

    def observar(self):
        return self.observacion

    def evolucionar_tiempo(self):
        self.año += 1

    def tipo_radiacion(self):
        print(f"Tiene radiación {self.radiacion}")


class Planeta(CuerpoCeleste):
    def __init__(self, nombre, tipo, sistemaEstelar, masa, velocidadActual,
                atraccion, radiacion, observacion, evolucion, año, radio,
                numero_max_satelites, tipo_atmosfera):
        super().__init__(nombre, tipo, sistemaEstelar, masa, velocidadActual,
                        atraccion, radiacion, observacion, evolucion, año)
        self.radio = radio
        self.numero_max_satelites = numero_max_satelites
        self.tipo_atmosfera = tipo_atmosfera
        self.habitabilidad = False
        self.ente = 0

    def agregar_satelite(self, satelite):
        if len(self.satelites) < self.numero_max_satelites:
            self.satelites.append(satelite)
        else:
            print("Este planeta no puede tener más satélites.")

    def generarClima(self):
        opciones = ["tropical", "seco", "templado", "polar", "continental"]
        self.clima = random.choice(opciones)

    def temperatura(self):
        opciones = ["gélido", "frío", "templado", "calor", "ardiente"]
        self.temperatura = random.choice(opciones)

    def vida(self):
        if self.habitabilidad:
            self.ente += 1


class Satelite_Natural(CuerpoCeleste):
    def __init__(self, nombre, tipo, sistemaEstelar, masa, velocidadActual,
                atraccion, radiacion, observacion, evolucion, año, planeta, distanciaCuerpo):
        super().__init__(nombre, tipo, sistemaEstelar, masa, velocidadActual,
                        atraccion, radiacion, observacion, evolucion, año)
        self.orbita = planeta
        self.distanciaCuerpo = distanciaCuerpo
        self.eclipse = False

    def analizar(self):
        print(f"Nombre del satélite: {self.nombre}. "
            f"Orbitando al planeta {self.orbita} a una distancia de {self.distanciaCuerpo} km.")

    def generarEclipse(self):
        if self.eclipse:
            print(f"{self.nombre} está eclipsando el planeta {self.orbita}.")


class Cometa(CuerpoCeleste):
    def __init__(self, nombre, tipo, sistemaEstelar, masa, velocidadActual,
                atraccion, radiacion, observacion, evolucion, año, periodoOrbital, planeta):
        super().__init__(nombre, tipo, sistemaEstelar, masa, velocidadActual,
                        atraccion, radiacion, observacion, evolucion, año)
        self.visibilidad = False
        self.materiaDesprendida = 0
        self.impacto = False
        self.cola = True
        self.planeta = planeta
        self.periodoOrbital = periodoOrbital

    def materiales(self):
        self.materiaDesprendida += 1

    def visible(self):
        if self.visibilidad:
            print(f"El cometa {self.nombre} es visible desde {self.planeta}.")

    def colita(self):
        if not self.cola:
            print(f"El cometa {self.nombre} no tiene ninguna cola visible.")

    def destruccion(self):
        if self.impacto:
            print(f"¡El cometa {self.nombre} ha impactado en el planeta {self.planeta}!")

    def frecuenciaAparicion(self):
        self.periodoOrbital += 1


class SistemaPlanetario:
    def __init__(self, nombre, cuerpoPrincipal):
        self.nombre = nombre
        self.cuerpoPrincipal = cuerpoPrincipal
        self.cuerpos = []

    def añadir_cuerpo(self, cuerpo):
        self.cuerpos.append(cuerpo)

    def eliminar_cuerpo(self, cuerpo):
        if cuerpo in self.cuerpos:
            self.cuerpos.remove(cuerpo)



# CUERPOS ARTIFICIALES


class EstructurasArtificiales:
    def __init__(self, id, agencia, pais, posicionX, posicionY, velocidad, estado="Operativo"):
        self.id = id
        self.agencia = agencia
        self.pais = pais
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.velocidad = velocidad
        self.estado = estado

    def mover_X(self):
        self.posicionX += 1

    def mover_Y(self):
        self.posicionY += 1

    def aumentarVelocidad(self):
        self.velocidad += 1

    def Estado(self):
        print(f"La máquina {self.id} se encuentra {self.estado}.")


class SistemaPropulsion:
    def __init__(self, tipoCombustible, cantidad, empujeMaximo):
        self.tipoCombustible = tipoCombustible
        self.cantidad = cantidad
        self.empujeMaximo = empujeMaximo
        self.encendido = True

    def apagar(self):
        self.encendido = False
        print("Motores apagados")


class SistemaComunicacion:
    def __init__(self, potenciaMaxima, frecuenciaSoportada, estado="Activo"):
        self.potenciaMaxima = potenciaMaxima
        self.frecuenciaSoportada = frecuenciaSoportada
        self.estado = estado

    def enviarMensaje(self):
        mensaje = input("Escriba un mensaje:\n")
        print("Mensaje enviado:", mensaje)


class Cohete(EstructurasArtificiales):
    def __init__(self, id, agencia, pais, posicionX, posicionY, velocidad, estado,
                empujeTotal, capacidadMaxima):
        super().__init__(id, agencia, pais, posicionX, posicionY, velocidad, estado)
        self.empujeTotal = empujeTotal
        self.capacidadMaxima = capacidadMaxima
        self.contadorLanzamientos = 0
        self.lanzamiento = False
        self.motores = False
        self.etapa = 3

    def lanzar(self):
        if self.lanzamiento:
            self.contadorLanzamientos += 1

    def cuentaAtras(self):
        print(f"El cohete {self.id} se está preparando para el lanzamiento.")
        for s in range(10, 0, -1):
            print(s)
            time.sleep(1)
        print("¡Despegue! 🚀")

    def encenderMotores(self):
        self.motores = True
        print("Motores encendidos")

    def apagarMotores(self):
        self.motores = False
        print("Motores apagados")

    def separarEtapa(self):
        if self.etapa > 0:
            self.etapa -= 1

    def trayectoria(self):
        self.posicionX += 1
        self.posicionY += 1

    def estado_cohete(self):
        print(f"El cohete {self.id} está {self.estado} en la etapa {self.etapa}.")

    def abortarMision(self):
        if self.estado != "Operativo":
            print("¡Hay que abortar misión!")


class SateliteArtificial(EstructurasArtificiales):
    def __init__(self, id, agencia, pais, posicionX, posicionY, velocidad, estado,
                cuerpoQueOrbita, alturaQueOrbita, funcion):
        super().__init__(id, agencia, pais, posicionX, posicionY, velocidad, estado)
        self.cuerpoQueOrbita = cuerpoQueOrbita
        self.alturaQueOrbita = alturaQueOrbita
        self.funcion = funcion
        self.operatividad = True
        self.capturarImagen = False

    def trayectoria(self):
        self.posicionX += 1
        self.posicionY += 1

    def Operatividad(self):
        if not self.operatividad:
            print(f"El satélite {self.id} está fuera de servicio.")

    def capturarImagenes(self):
        if self.capturarImagen:
            print("Se ha tomado una imagen.")


class ConstelacionesArtificiales:
    def __init__(self, nombre, orbitaComun):
        self.nombre = nombre
        self.orbitaComun = orbitaComun
        self.satelitesQueLaComponen = []
        self.centrosQueLaComponen = []

    def añadirSatélite(self, satelite):
        self.satelitesQueLaComponen.append(satelite)

    def quitarSatélite(self, satelite):
        if satelite in self.satelitesQueLaComponen:
            self.satelitesQueLaComponen.remove(satelite)

    def añadirCentro(self, centro):
        self.centrosQueLaComponen.append(centro)

    def quitarCentro(self, centro):
        if centro in self.centrosQueLaComponen:
            self.centrosQueLaComponen.remove(centro)


class centroControl:
    def __init__(self, nombre, pais, humanosDisponibles):
        self.nombre = nombre
        self.pais = pais
        self.humanosDisponibles = humanosDisponibles
        self.estado = "Operativo"
        self.estructurasArtificiales = []

    def agregar_estructura(self, estructuraArtificial):
        self.estructurasArtificiales.append(estructuraArtificial)

    def estado_actual(self):
        if self.estado != "Operativo":
            print(f"Algo sucede con el centro de control {self.nombre}.")

    def enviarOrdenes(self):
        orden = input("Envía órdenes:\n")
        print("Orden enviada:", orden)




# MUESTRA DE DATOS


print("\n=== MUESTRA DE DATOS ===\n")

# Crear planeta
tierra = Planeta("Tierra", "Planeta", "Sistema Solar", 5.97e24, 30,
                9.8, "Moderada", "Alta", "Lenta", 2025, 6371, 1, "Nitrogenada")

# Crear satélite natural
luna = Satelite_Natural("Luna", "Satélite", "Sistema Solar", 7.35e22, 1,
                        1.6, "Baja", "Media", "Lenta", 2025, "Tierra", 384400)
tierra.agregar_satelite(luna)

# Crear cometa
halley = Cometa("Halley", "Cometa", "Sistema Solar", 2.2e14, 55, 0.5,
                "Alta", "Variable", "Rápida", 2025, 76, "Tierra")

# Crear cohete
falcon9 = Cohete("F9-001", "SpaceX", "EEUU", 0, 0, 0, "Operativo", 7600, 22800)

# Crear satélite artificial
hubble = SateliteArtificial("HST-01", "NASA", "EEUU", 100, 200, 7.5,
                            "Operativo", "Tierra", 540, "Observación")

# Crear constelación
starlink = ConstelacionesArtificiales("Starlink", 550)
starlink.añadirSatélite(hubble)

# Crear centro de control
nasa_cc = centroControl("NASA Control", "EEUU", 120)
nasa_cc.agregar_estructura(hubble)


# ==== IMPRIMIR INFORMACIÓN COMPLETA ====

print("PLANETA")
print("-------")
print(f"Nombre: {tierra.nombre}")
print(f"Tipo: {tierra.tipo}")
print(f"Sistema Estelar: {tierra.sistemaEstelar}")
print(f"Masa: {tierra.masa} kg")
print(f"Velocidad: {tierra.velocidadActual} km/s")
print(f"Gravedad: {tierra.atraccion}")
print(f"Atmósfera: {tierra.tipo_atmosfera}")
print(f"Satélites: {[s.nombre for s in tierra.satelites]}\n")

print("SATÉLITE NATURAL")
print("-----------------")
print(f"Nombre: {luna.nombre}")
print(f"Orbita: {luna.orbita}")
print(f"Distancia al planeta: {luna.distanciaCuerpo} km")
print(f"Radiación: {luna.radiacion}")
print(f"Masa: {luna.masa}\n")

print("COMETA")
print("------")
print(f"Nombre: {halley.nombre}")
print(f"Periodo orbital: {halley.periodoOrbital} años")
print(f"Visible: {halley.visibilidad}")
print(f"Visto desde el planeta: {halley.planeta}")
print(f"Materia desprendida: {halley.materiaDesprendida}\n")

print("COHETE")
print("------")
print(f"ID: {falcon9.id}")
print(f"Agencia: {falcon9.agencia}")
print(f"Estado: {falcon9.estado}")
print(f"Empuje Total: {falcon9.empujeTotal}")
print(f"Capacidad Máxima: {falcon9.capacidadMaxima} kg")
print(f"Etapas restantes: {falcon9.etapa}\n")

print("SATÉLITE ARTIFICIAL")
print("--------------------")
print(f"ID: {hubble.id}")
print(f"Función: {hubble.funcion}")
print(f"Orbita: {hubble.cuerpoQueOrbita}")
print(f"Altura de órbita: {hubble.alturaQueOrbita} km")
print(f"Velocidad: {hubble.velocidad}\n")

print("CONSTELACIÓN")
print("------------")
print(f"Nombre: {starlink.nombre}")
print(f"Órbita común: {starlink.orbitaComun} km")
print(f"Satelites que la componen: {[s.id for s in starlink.satelitesQueLaComponen]}\n")

print("CENTRO DE CONTROL")
print("------------------")
print(f"Nombre: {nasa_cc.nombre}")
print(f"País: {nasa_cc.pais}")
print(f"Humanos disponibles: {nasa_cc.humanosDisponibles}")
print(f"Estructuras controladas: {[e.id for e in nasa_cc.estructurasArtificiales]}\n")

print("\n=== FIN DE MUESTRA ===\n")