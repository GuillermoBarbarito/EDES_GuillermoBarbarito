import tkinter as tk
from tkinter import ttk
import math
import random

ANCHO = 800
ALTO = 600
modo_jugadores = 2
raton_presionado = False
balas = []
icebergs = []
kits = []

def seleccionar_modo():
    ventana_modo = tk.Tk()
    ventana_modo.title("Seleccionar modo de juego")
    ventana_modo.geometry("300x150")
    ventana_modo.configure(bg="#001122")

    def iniciar(jugadores):
        global modo_jugadores
        modo_jugadores = jugadores
        ventana_modo.destroy()

    tk.Label(ventana_modo, text="¿Cuántos jugadores?", bg="#001122", fg="white", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana_modo, text="1 Jugador", command=lambda: iniciar(1), font=("Arial", 12)).pack(pady=5)
    tk.Button(ventana_modo, text="2 Jugadores", command=lambda: iniciar(2), font=("Arial", 12)).pack(pady=5)

    ventana_modo.mainloop()

seleccionar_modo()

class Barco:
    def __init__(self, nombre, x, y, velocidad, rumbo, munición, canvas, color, vida_max=100):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.munición = min(munición, 20)
        self.vida_max = vida_max
        self.vida = vida_max
        self.canvas = canvas
        self.color = color
        self.cañón_ángulo = rumbo
        self.objetivo_x = None
        self.objetivo_y = None
        self.triángulo = None
        self.rumbo_linea = None
        self.cañón_linea = None
        self.barra_fondo = None
        self.barra_vida = None
        self.dibujar()

    def dibujar(self):
        puntos = self.get_puntos()
        self.triángulo = self.canvas.create_polygon(puntos, fill=self.color, outline="white", width=3)
        self.rumbo_linea = self.canvas.create_line(self.x, self.y, *self.get_punta(self.rumbo, 50), fill="black", width=2)
        self.cañón_linea = self.canvas.create_line(self.x, self.y, *self.get_punta(self.cañón_ángulo, 60), fill="red", width=3)
        self.barra_fondo = self.canvas.create_rectangle(self.x - 25, self.y - 35, self.x + 25, self.y - 30, fill="white")
        self.barra_vida = self.canvas.create_rectangle(self.x - 25, self.y - 35, self.x + 25, self.y - 30, fill="green")

    def get_punta(self, ángulo, largo):
        rad = math.radians(ángulo)
        return (self.x + largo * math.cos(rad), self.y + largo * math.sin(rad))

    def get_puntos(self):
        ang = math.radians(self.rumbo)
        punta = (self.x + 30 * math.cos(ang), self.y + 30 * math.sin(ang))
        base1 = (self.x + 20 * math.cos(ang + 2.5), self.y + 20 * math.sin(ang + 2.5))
        base2 = (self.x + 20 * math.cos(ang - 2.5), self.y + 20 * math.sin(ang - 2.5))
        return [punta, base1, base2]

    def mover_a_objetivo(self):
        if self.objetivo_x is None or self.objetivo_y is None:
            return

        dx = self.objetivo_x - self.x
        dy = self.objetivo_y - self.y
        distancia = math.hypot(dx, dy)

        if distancia < 5:
            self.objetivo_x = None
            self.objetivo_y = None
            self.velocidad = 0
            return

        self.rumbo = math.degrees(math.atan2(dy, dx)) % 360
        self.velocidad = 2

    def actualizar(self):
        self.mover_a_objetivo()

        dx = self.velocidad * math.cos(math.radians(self.rumbo))
        dy = self.velocidad * math.sin(math.radians(self.rumbo))
        self.x += dx
        self.y += dy

        if self.x < 30 or self.x > ANCHO - 30:
            self.rumbo = (180 - self.rumbo) % 360
        if self.y < 30 or self.y > ALTO - 30:
            self.rumbo = (-self.rumbo) % 360

        self.canvas.coords(self.triángulo, *self.get_puntos())
        self.canvas.coords(self.rumbo_linea, self.x, self.y, *self.get_punta(self.rumbo, 50))
        self.canvas.coords(self.cañón_linea, self.x, self.y, *self.get_punta(self.cañón_ángulo, 60))

        vida_ratio = self.vida / self.vida_max
        color = "green" if vida_ratio > 0.5 else "orange" if vida_ratio > 0.2 else "red"
        self.canvas.coords(self.barra_fondo, self.x - 25, self.y - 35, self.x + 25, self.y - 30)
        self.canvas.coords(self.barra_vida, self.x - 25, self.y - 35, self.x - 25 + 50 * vida_ratio, self.y - 30)
        self.canvas.itemconfig(self.barra_vida, fill=color)

    def apuntar_con_raton(self, x_mouse, y_mouse):
        dx = x_mouse - self.x
        dy = y_mouse - self.y
        self.cañón_ángulo = (math.degrees(math.atan2(dy, dx))) % 360

    def disparar(self):
        if self.munición >= 1 and self.vida > 0:
            self.munición -= 1
            dx = 10 * math.cos(math.radians(self.cañón_ángulo))
            dy = 10 * math.sin(math.radians(self.cañón_ángulo))
            bala = self.canvas.create_oval(self.x - 4, self.y - 4, self.x + 4, self.y + 4, fill="black")
            balas.append({"obj": bala, "dx": dx, "dy": dy, "origen": self})
            return f"{self.nombre} disparó hacia {int(self.cañón_ángulo)}°"
        return f"{self.nombre} no puede disparar"

    def __str__(self):
        return (f"📍 {self.nombre}\n"
                f"Posición: X = {int(self.x)}, Y = {int(self.y)}\n"
                f"Velocidad: {self.velocidad} nudos\n"
                f"Rumbo: {self.rumbo}°\n"
                f"Cañón: {int(self.cañón_ángulo)}°\n"
                f"Munición: {int(self.munición)}/20\n"
                f"Vida: {self.vida}/{self.vida_max}\n")

def generar_iceberg(canvas):
    if len(icebergs) >= 10:
        return
    y = random.randint(50, ALTO - 50)
    lado = random.choice(["izquierda", "derecha"])
    x = 0 if lado == "izquierda" else ANCHO
    dx = 2 if lado == "izquierda" else -2
    obj = canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white", outline="#99ccff", width=2)
    icebergs.append({"x": x, "y": y, "dx": dx, "obj": obj})

def generar_kit(canvas):
    if len(kits) >= 5:
        return
    y = random.randint(50, ALTO - 50)
    lado = random.choice(["izquierda", "derecha"])
    x = 0 if lado == "izquierda" else ANCHO
    dx = 2 if lado == "izquierda" else -2
    obj = canvas.create_rectangle(x - 8, y - 8, x + 8, y + 8, fill="#00ff00", outline="white", width=2)
    kits.append({"x": x, "y": y, "dx": dx, "obj": obj})
# --- Ventana principal ---
root = tk.Tk()
root.title("🚢 Barquitos Deluxe")
root.configure(bg="#002244")

canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#66ccff", highlightthickness=0)
canvas.pack(side="left", padx=10, pady=10)

# --- Fondo decorativo del agua ---
for i in range(0, ANCHO, 40):
    for j in range(0, ALTO, 40):
        canvas.create_oval(i, j, i+20, j+20, fill="#88ccff", outline="")

# --- Panel de eventos ---
registro = tk.Text(root, width=35, height=30, bg="#001122", fg="white", font=("Consolas", 10))
registro.pack(side="right", padx=10, pady=10)

# --- Panel de ayuda con controles ---
manual = tk.Text(root, width=35, height=30, bg="#001122", fg="#00ffff", font=("Consolas", 10))
manual.pack(side="right", padx=10, pady=10)
manual.insert("end", "📘 CONTROLES DEL JUEGO\n\n")
manual.insert("end", "🧑 JUGADOR 1 (Ratón)\n")
manual.insert("end", "• Clic derecho: Mover barco\n")
manual.insert("end", "• Mantener clic izquierdo: Apuntar cañón\n")
manual.insert("end", "• Botón 'Disparar': Disparar\n")
manual.insert("end", "• Botón 'Recargar': Recargar munición\n\n")
manual.insert("end", "🎮 JUGADOR 2 (Teclado)\n")
manual.insert("end", "• Flechas ← ↑ ↓ →: Mover barco\n")
manual.insert("end", "• Tecla A: Girar cañón\n")
manual.insert("end", "• Tecla Enter: Disparar\n")
manual.insert("end", "• Tecla R: Recargar munición\n")
manual.config(state="disabled")

# --- Lista de barcos ---
barcos = [
    Barco("Titanic", 100, 100, 2, 0, 10, canvas, "#003366", vida_max=150),
    Barco("SpeedStar", 200, 200, 3, 90, 5, canvas, "#cc0000", vida_max=100),
    Barco("BlindWall", 300, 300, 1, 180, 20, canvas, "#009933", vida_max=200)
]

combo = ttk.Combobox(root, values=[b.nombre for b in barcos], font=("Arial", 12))
combo.current(0)
combo.pack(pady=5)

tk.Button(root, text="Disparar", command=lambda: disparar(), bg="#004466", fg="white", font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Recargar", command=lambda: recargar_manual(), bg="#006600", fg="white", font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Salir del juego", command=lambda: salir(), bg="darkred", fg="white", font=("Arial", 12)).pack(pady=5)

estado = tk.StringVar()
estado.set(str(barcos[0]))
tk.Label(root, textvariable=estado, bg="#002244", fg="white", font=("Consolas", 11), justify="left").pack(pady=5)

# --- Eventos del canvas ---
def presionar_raton(event):
    global raton_presionado
    raton_presionado = True

def soltar_raton(event):
    global raton_presionado
    raton_presionado = False

def mover_cañón():
    if raton_presionado:
        x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        y = canvas.winfo_pointery() - canvas.winfo_rooty()
        barco = barcos[combo.current()]
        barco.apuntar_con_raton(x, y)
    root.after(50, mover_cañón)

def click_derecho(event):
    barco = barcos[combo.current()]
    barco.objetivo_x = event.x
    barco.objetivo_y = event.y
    registro.insert("end", f"🧭 {barco.nombre} se dirige a ({event.x}, {event.y})\n")
    registro.see("end")

canvas.bind("<Button-3>", click_derecho)
canvas.bind("<ButtonPress-1>", presionar_raton)
canvas.bind("<ButtonRelease-1>", soltar_raton)

# --- Teclado para jugador 2 ---
def mover_jugador2(event):
    barco = barcos[1]
    if barco.vida <= 0:
        return

    if event.keysym == "Up":
        barco.objetivo_y = barco.y - 50
        barco.objetivo_x = barco.x
    elif event.keysym == "Down":
        barco.objetivo_y = barco.y + 50
        barco.objetivo_x = barco.x
    elif event.keysym == "Left":
        barco.objetivo_x = barco.x - 50
        barco.objetivo_y = barco.y
    elif event.keysym == "Right":
        barco.objetivo_x = barco.x + 50
        barco.objetivo_y = barco.y
    elif event.keysym == "Return":
        resultado = barco.disparar()
        registro.insert("end", f"🎯 J2: {resultado}\n")
        registro.see("end")
    elif event.keysym == "r":
        barco.munición = min(20, barco.munición + 5)
        registro.insert("end", f"🔋 J2: {barco.nombre} recargó munición\n")
        registro.see("end")
    elif event.keysym == "a":
        barco.cañón_ángulo = (barco.cañón_ángulo + 10) % 360

root.bind("<Key>", mover_jugador2)
def disparar():
    barco = barcos[combo.current()]
    resultado = barco.disparar()
    estado.set(resultado)
    registro.insert("end", f"🧨 {resultado}\n")
    registro.see("end")

def recargar_manual():
    barco = barcos[combo.current()]
    barco.munición = min(20, barco.munición + 5)
    estado.set(f"{barco.nombre} recargó munición")
    registro.insert("end", f"🔋 {barco.nombre} recargó munición\n")
    registro.see("end")

def salir():
    root.destroy()

def recargar():
    for barco in barcos:
        if barco.vida > 0 and barco.munición < 20:
            barco.munición = min(20, barco.munición + 0.1)
    root.after(1000, recargar)

def IA_disparo():
    if modo_jugadores == 1:
        for barco in barcos:
            if barco.nombre != "Titanic" and barco.vida > 0:
                objetivo = barcos[0]
                dx = objetivo.x - barco.x
                dy = objetivo.y - barco.y
                distancia = math.hypot(dx, dy)
                if distancia < 200:
                    barco.apuntar_con_raton(objetivo.x, objetivo.y)
                    resultado = barco.disparar()
                    registro.insert("end", f"🤖 {resultado}\n")
                    registro.see("end")
    root.after(1000, IA_disparo)

def mover_objetos():
    # Icebergs
    for iceberg in list(icebergs):
        iceberg["x"] += iceberg["dx"]
        canvas.move(iceberg["obj"], iceberg["dx"], 0)
        if iceberg["x"] < -20 or iceberg["x"] > ANCHO + 20:
            canvas.delete(iceberg["obj"])
            icebergs.remove(iceberg)

    # Kits
    for kit in list(kits):
        kit["x"] += kit["dx"]
        canvas.move(kit["obj"], kit["dx"], 0)
        if kit["x"] < -20 or kit["x"] > ANCHO + 20:
            canvas.delete(kit["obj"])
            kits.remove(kit)

    # Generar nuevos
    if random.random() < 0.02:
        generar_iceberg(canvas)
    if random.random() < 0.01:
        generar_kit(canvas)

    root.after(100, mover_objetos)

def actualizar():
    for barco in barcos:
        if barco.vida > 0:
            barco.actualizar()

    # Colisiones entre barcos
    for i in range(len(barcos)):
        for j in range(i + 1, len(barcos)):
            b1, b2 = barcos[i], barcos[j]
            if b1.vida > 0 and b2.vida > 0:
                dist = math.hypot(b1.x - b2.x, b1.y - b2.y)
                if dist < 40:
                    b1.vida = max(0, b1.vida - 50)
                    b2.vida = max(0, b2.vida - 50)
                    registro.insert("end", f"💥 Choque entre {b1.nombre} y {b2.nombre} (-50 vida)\n")
                    registro.see("end")

    # Colisiones con icebergs
    for barco in barcos:
        if barco.vida > 0:
            for iceberg in list(icebergs):
                dx = barco.x - iceberg["x"]
                dy = barco.y - iceberg["y"]
                if math.hypot(dx, dy) < 25:
                    barco.vida = max(0, barco.vida - 50)
                    registro.insert("end", f"🧊 {barco.nombre} chocó con un iceberg (-50 vida)\n")
                    registro.see("end")

    # Colisiones con kits
    for barco in barcos:
        if barco.vida > 0:
            for kit in list(kits):
                dx = barco.x - kit["x"]
                dy = barco.y - kit["y"]
                if math.hypot(dx, dy) < 25:
                    barco.vida = min(barco.vida_max, barco.vida + 50)
                    canvas.delete(kit["obj"])
                    kits.remove(kit)
                    registro.insert("end", f"🛠️ {barco.nombre} recogió un kit (+50 vida)\n")
                    registro.see("end")

    # Movimiento de balas y colisiones
    for bala in list(balas):
        canvas.move(bala["obj"], bala["dx"], bala["dy"])
        x1, y1, x2, y2 = canvas.coords(bala["obj"])
        impactado = False
        for barco in barcos:
            if barco != bala["origen"] and barco.vida > 0:
                bx1, by1, bx2, by2 = canvas.bbox(barco.triángulo)
                if bx1 < x1 < bx2 and by1 < y1 < by2:
                    daño = 30 if bala["origen"].nombre == "SpeedStar" else 20
                    barco.vida = max(0, barco.vida - daño)
                    if barco.vida == 0:
                        canvas.itemconfig(barco.triángulo, fill="gray")
                    explosión = canvas.create_oval(x1 - 12, y1 - 12, x1 + 12, y1 + 12, fill="yellow", outline="orange")
                    canvas.after(300, lambda: canvas.delete(explosión))
                    registro.insert("end", f"🎯 {bala['origen'].nombre} impactó a {barco.nombre} (-{daño})\n")
                    registro.see("end")
                    impactado = True
                    break
        if impactado or x2 < 0 or x1 > ANCHO or y2 < 0 or y1 > ALTO:
            canvas.delete(bala["obj"])
            balas.remove(bala)

    estado.set(str(barcos[combo.current()]))
    root.after(33, actualizar)

# --- Lanzar juego ---
actualizar()
recargar()
IA_disparo()
mover_cañón()
mover_objetos()
root.mainloop()