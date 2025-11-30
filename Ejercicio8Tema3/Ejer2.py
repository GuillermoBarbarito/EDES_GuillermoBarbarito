import tkinter as tk
import math
import time
import random

# --- Sonido opcional con pygame ---
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

SOUNDS = {
    "misil_aa": "sounds/misil_aa.wav",
    "misil_antibuque": "sounds/misil_antibuque.wav",
    "torpedo": "sounds/torpedo.wav",
    "ping": "sounds/ping.wav",
    "deteccion": "sounds/deteccion.wav",
    "explosion": "sounds/explosion.wav"
}

def play_sound(name):
    if not SOUND_AVAILABLE:
        return
    path = SOUNDS.get(name)
    if not path:
        return
    try:
        pygame.mixer.Sound(path).play()
    except Exception:
        pass

# ----- CONFIGURACIÓN -----
ANCHO, ALTO = 900, 600

ARMAS_CONFIG = {
    "Misil AA": {"alcance": 280, "recarga_s": 3.0, "daño": 60, "color": "#ffd166"},
    "Misil Antibuque": {"alcance": 340, "recarga_s": 4.0, "daño": 80, "color": "#ef476f"},
    "Torpedo": {"alcance": 220, "recarga_s": 5.0, "daño": 70, "color": "#06d6a0"},
}

# ----- CLASE PLATAFORMA -----
class PlataformaNaval:
    def __init__(self, nombre, pais, tipo, x, y, color, sensores=None, armas=None, velocidad_max=28):
        self.nombre = nombre
        self.pais = pais
        self.tipo = tipo
        self.x = x
        self.y = y
        self.color = color

        self.estado = "OK"
        self.radar = sensores.get("radar", False) if sensores else False
        self.sonar = sensores.get("sonar", False) if sensores else False
        self.rango = sensores.get("rango", 150) if sensores else 150

        self.armas = armas or {}
        self.rumbo = 0
        self.vel_kn = 0
        self.vel_max = velocidad_max
        self.target = None

        self.size = 26
        self.icon = None
        self.text = None
        self.last_fire_time = {}
        self.sumergido = False  # exclusivo para submarinos

    def set_target(self, tx, ty):
        self.target = (tx, ty)

    def actualizar_cinematica(self, dt=0.033):
        if self.estado == "Hundido":
            return

        if self.target:
            dx = self.target[0] - self.x
            dy = self.target[1] - self.y
            dist = math.hypot(dx, dy)

            if dist < 5:
                self.target = None
                self.vel_kn = 0
                return

            self.rumbo = (math.degrees(math.atan2(dy, dx))) % 360
            self.vel_kn = min(self.vel_max, self.vel_kn + 0.4)
            self.x += self.vel_kn * math.cos(math.radians(self.rumbo)) * dt * 30
            self.y += self.vel_kn * math.sin(math.radians(self.rumbo)) * dt * 30
        else:
            self.vel_kn = max(0, self.vel_kn - 0.2)

    def aplicar_danio(self, daño):
        if self.estado == "Hundido":
            return
        if self.estado == "OK":
            self.estado = "Dañado"
        elif self.estado == "Dañado":
            self.estado = "Hundido"

    def puede_disparar(self, arma_tipo):
        muni = self.armas.get(arma_tipo, 0)
        if muni <= 0:
            return False, "Sin munición"

        cfg = ARMAS_CONFIG[arma_tipo]
        now = time.time()
        t0 = self.last_fire_time.get(arma_tipo, 0)
        if now - t0 < cfg["recarga_s"]:
            return False, f"Recargando ({cfg['recarga_s']}s)"

        return True, ""

    def registrar_disparo(self, arma_tipo):
        self.armas[arma_tipo] -= 1
        self.last_fire_time[arma_tipo] = time.time()

    def recargar_armamento(self):
        for k, v in self.armas.items():
            # recarga completa (por ejemplo, max 6 para cada tipo)
            if k == "Misil AA": self.armas[k] = 6
            if k == "Misil Antibuque": self.armas[k] = 4
            if k == "Torpedo": self.armas[k] = 5

    def draw(self, canvas):
        if self.icon: canvas.delete(self.icon)
        if self.text: canvas.delete(self.text)

        ang = math.radians(self.rumbo)
        nose = (self.x + 26 * math.cos(ang), self.y + 26 * math.sin(ang))
        left = (self.x + 18 * math.cos(ang + 2.6), self.y + 18 * math.sin(ang + 2.6))
        right = (self.x + 18 * math.cos(ang - 2.6), self.y + 18 * math.sin(ang - 2.6))

        if self.tipo == "Submarino" and self.sumergido:
            # solo contorno cuando sumergido
            self.icon = canvas.create_oval(self.x-13, self.y-13, self.x+13, self.y+13, outline=self.color, width=2)
        else:
            self.icon = canvas.create_polygon(*nose, *left, *right, fill=self.color, outline="white", width=2)

        self.text = canvas.create_text(self.x, self.y + 22,
                                       text=f"{self.nombre}",
                                       fill="#F1FAEE", font=("Segoe UI", 9, "bold"))
# ----- APLICACIÓN PRINCIPAL -----
class App:
    def __init__(self, root):
        self.root = root
        root.title("Simulación Naval Mejorada")

        # MAPA
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#061A2B")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        # PANEL LATERAL
        self.panel = tk.Frame(root, width=300, bg="#0D1B2A")
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_title = tk.Label(self.panel, text="📘 Información de Flota",
                                   bg="#0D1B2A", fg="#E0E1DD",
                                   font=("Segoe UI", 13, "bold"))
        self.info_title.pack(pady=(10, 0))

        self.info_text = tk.Text(self.panel, width=35, height=16,
                                 bg="#1B263B", fg="#E0E1DD", bd=0,
                                 font=("Consolas", 10))
        self.info_text.pack(padx=10, pady=5)

        self.log_title = tk.Label(self.panel, text="📡 Registro de Eventos",
                                  bg="#0D1B2A", fg="#E0E1DD",
                                  font=("Segoe UI", 13, "bold"))
        self.log_title.pack(pady=(10, 0))

        self.log_text = tk.Text(self.panel, width=35, height=10,
                                bg="#1B263B", fg="#A8DADC", bd=0,
                                font=("Consolas", 10))
        self.log_text.pack(padx=10, pady=5)

        self.btns_frame = tk.Frame(self.panel, bg="#0D1B2A")
        self.btns_frame.pack()

        # Crear flota
        self.fragata = PlataformaNaval("Fragata F-100", "España", "Fragata",
                                       140, 160, "#4cc9f0",
                                       sensores={"radar": True, "rango": 220},
                                       armas={"Misil AA": 6})

        self.corbeta = PlataformaNaval("Corbeta C-80", "España", "Corbeta",
                                       260, 360, "#f72585",
                                       sensores={"radar": True, "rango": 200},
                                       armas={"Misil Antibuque": 4})

        self.submarino = PlataformaNaval("Submarino S-80", "España", "Submarino",
                                         520, 240, "#bde0fe",
                                         sensores={"sonar": True, "rango": 180},
                                         armas={"Torpedo": 5})

        self.flota = [self.fragata, self.corbeta, self.submarino]
        self.seleccionada = None

        # Botones
        self.add_button("🔎 Escanear sensores", self.escanear_sensores)
        self.add_button("🎯 Lanzar arma", self.lanzar_arma_dialog)
        self.add_button("🔥 Ataque coordinado", self.ordenar_ataque)
        self.add_button("💥 Simular daño", self.simular_danio_dialog)
        self.add_button("🚢 Mostrar flota", self.mostrar_flota)
        self.add_button("🔄 Recargar armamento", self.recargar_armamento)
        self.add_button("🌊 Sumergir submarino", self.sumergir_submarino)
        self.add_button("⬆️ Emerger submarino", self.emergir_submarino)

        # Binding
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Loop inicial
        self.redibujar()
        self.actualizar_panel()
        self.loop()

    # ----- botones -----
    def add_button(self, label, cmd):
        b = tk.Button(self.btns_frame, text=label, command=cmd,
                      width=28, bg="#415A77", fg="white",
                      activebackground="#778DA9", bd=0,
                      font=("Segoe UI", 10, "bold"))
        b.pack(pady=3)

    # ----- utilidades -----
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def redibujar(self):
        self.canvas.delete("all")
        for p in self.flota:
            p.draw(self.canvas)
        if self.seleccionada:
            x, y = self.seleccionada.x, self.seleccionada.y
            self.canvas.create_oval(x-30, y-30, x+30, y+30, outline="#FFD166", width=3)

    def actualizar_panel(self, extra=""):
        self.info_text.delete("1.0", tk.END)

        for p in self.flota:
            self.info_text.insert(tk.END,
                f"🔹 {p.nombre} ({p.tipo})\n", "title")
            self.info_text.insert(tk.END,
                f"  Estado: {p.estado}\n"
                f"  Posición: ({int(p.x)}, {int(p.y)})\n"
                f"  Rumbo: {int(p.rumbo)}° | Vel: {int(p.vel_kn)} kn\n"
                f"  Armamento: {', '.join(f'{k}:{v}' for k,v in p.armas.items())}\n"
                f"  Sumergido: {'Sí' if getattr(p,'sumergido',False) else 'No'}\n\n"
            )

        if extra:
            self.info_text.insert(tk.END, "\nEVENTOS:\n" + extra)

    # ----- eventos y sensores -----
    def on_canvas_click(self, ev):
        sel = None
        for p in self.flota:
            if abs(ev.x - p.x) < 25 and abs(ev.y - p.y) < 25:
                sel = p
                break
        if sel:
            self.seleccionada = sel
            self.log(f"Seleccionado: {sel.nombre}")
        else:
            if self.seleccionada:
                self.seleccionada.set_target(ev.x, ev.y)
                self.log(f"Moviendo {self.seleccionada.nombre} → ({ev.x},{ev.y})")
        self.redibujar()
        self.actualizar_panel()

    def distancia(self, a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

    def escanear_sensores(self):
        detect = []
        for a in self.flota:
            if getattr(a, 'sumergido', False):
                continue  # submarino sumergido no se detecta
            for b in self.flota:
                if a == b:
                    continue
                if getattr(b, 'sumergido', False):
                    continue
                d = self.distancia(a, b)
                if d <= a.rango:
                    detect.append(f"{a.nombre} detecta a {b.nombre} ({int(d)}px)")

        if detect:
            play_sound("ping")
            play_sound("deteccion")
            msg = "\n".join(detect)
            self.log(msg)
            self.actualizar_panel(extra=msg)
        else:
            self.log("Sin contactos detectados.")

    # ----- recarga -----
    def recargar_armamento(self):
        if self.seleccionada:
            self.seleccionada.recargar_armamento()
            self.log(f"{self.seleccionada.nombre} ha recargado su armamento.")
            self.actualizar_panel()
        else:
            self.log("Selecciona una plataforma para recargar.")

    # ----- sumergir/emerger -----
    def sumergir_submarino(self):
        if self.submarino.estado != "Hundido":
            self.submarino.sumergido = True
            self.log(f"{self.submarino.nombre} se ha sumergido.")
            self.redibujar()
            self.actualizar_panel()

    def emergir_submarino(self):
        if self.submarino.estado != "Hundido":
            self.submarino.sumergido = False
            self.log(f"{self.submarino.nombre} ha emergido.")
            self.redibujar()
            self.actualizar_panel()
    # ----- misiles -----
    def crear_misil(self, x, y, ang, color):
        largo = 16
        ancho = 6

        nose = (x + largo * math.cos(ang), y + largo * math.sin(ang))
        left = (x + ancho * math.cos(ang + 2.4), y + ancho * math.sin(ang + 2.4))
        right = (x + ancho * math.cos(ang - 2.4), y + ancho * math.sin(ang - 2.4))

        return self.canvas.create_polygon(
            *nose, *left, *right, fill=color, outline="white", width=1
        )

    def animar_misil(self, misil, ang, dx, dy, pasos, objetivo, cfg, atacante):
        if pasos <= 0:
            self.canvas.delete(misil)
            play_sound("explosion")
            objetivo.aplicar_danio(cfg["daño"])
            self.log(f"{atacante.nombre} impactó a {objetivo.nombre} → {objetivo.estado}")
            self.actualizar_panel()
            self.redibujar()
            return

        # mover misil
        self.canvas.move(misil, dx, dy)

        coords = self.canvas.coords(misil)
        mx = (coords[0] + coords[2] + coords[4]) / 3
        my = (coords[1] + coords[3] + coords[5]) / 3

        # defensa AA
        if atacante != self.fragata:
            if self.defensa_antiaerea(objetivo, {"x": mx, "y": my}):
                self.canvas.delete(misil)
                return

        # redibujar el misil para que apunte hacia el objetivo
        self.canvas.delete(misil)
        misil = self.crear_misil(mx, my, ang, cfg["color"])

        self.root.after(33, lambda:
                        self.animar_misil(misil, ang, dx, dy, pasos - 1, objetivo, cfg, atacante)
                        )

    def defensa_antiaerea(self, objetivo, proyectil):
        frag = self.fragata
        if frag.estado == "Hundido":
            return False
        if frag.armas.get("Misil AA", 0) <= 0:
            return False

        d = math.hypot(frag.x - proyectil["x"], frag.y - proyectil["y"])
        if d <= frag.rango:
            if random.random() < 0.7:
                frag.armas["Misil AA"] -= 1
                play_sound("misil_aa")
                play_sound("explosion")
                self.log(f"{frag.nombre} interceptó un misil enemigo.")
                return True
        return False

    # ----- lanzar armas -----
    def lanzar_arma(self, atacante, objetivo):
        if atacante.estado == "Hundido" or objetivo.estado == "Hundido":
            self.log("No se puede atacar")
            return

        if getattr(objetivo, "sumergido", False):
            self.log(f"{objetivo.nombre} está sumergido y no puede ser atacado.")
            return

        if atacante.tipo == "Fragata":
            arma = "Misil AA"
            sonido = "misil_aa"
        elif atacante.tipo == "Corbeta":
            arma = "Misil Antibuque"
            sonido = "misil_antibuque"
        else:
            arma = "Torpedo"
            sonido = "torpedo"

        cfg = ARMAS_CONFIG[arma]

        ok, motivo = atacante.puede_disparar(arma)
        if not ok:
            self.log(f"{atacante.nombre}: {motivo}")
            return

        d = self.distancia(atacante, objetivo)
        if d > cfg["alcance"]:
            self.log("Objetivo fuera de alcance.")
            return

        atacante.registrar_disparo(arma)
        play_sound(sonido)

        ang = math.atan2(objetivo.y - atacante.y, objetivo.x - atacante.x)

        mx = atacante.x + 26 * math.cos(ang)
        my = atacante.y + 26 * math.sin(ang)

        misil = self.crear_misil(mx, my, ang, cfg["color"])

        pasos = 28
        dx = (objetivo.x - mx) / pasos
        dy = (objetivo.y - my) / pasos

        self.animar_misil(misil, ang, dx, dy, pasos, objetivo, cfg, atacante)

    def lanzar_arma_dialog(self):
        if not self.seleccionada:
            self.log("Selecciona una plataforma")
            return

        objetivos = [p for p in self.flota if p is not self.seleccionada and p.estado != "Hundido" and not getattr(p,'sumergido',False)]
        objetivos.sort(key=lambda o: self.distancia(self.seleccionada, o))

        if not objetivos:
            self.log("No hay objetivos disponibles")
            return

        self.lanzar_arma(self.seleccionada, objetivos[0])

    def ordenar_ataque(self):
        self.lanzar_arma(self.fragata, self.submarino)
        self.lanzar_arma(self.corbeta, self.fragata)
        self.lanzar_arma(self.submarino, self.corbeta)

    # ----- simular daño -----
    def simular_danio_dialog(self):
        if not self.seleccionada:
            self.log("Selecciona una plataforma")
            return

        self.seleccionada.aplicar_danio(50)
        self.log(f"Daño simulado en {self.seleccionada.nombre}")
        self.redibujar()
        self.actualizar_panel()

    # ----- mostrar flota -----
    def mostrar_flota(self):
        w = tk.Toplevel(self.root)
        w.title("Flota Completa")
        t = tk.Text(w, width=60, height=18, bg="#1B263B", fg="white", font=("Consolas", 10))
        t.pack(padx=10, pady=10)

        for p in self.flota:
            t.insert(tk.END,
                     f"{p.nombre} ({p.tipo})\n"
                     f" Estado: {p.estado}\n"
                     f" Pos: ({int(p.x)}, {int(p.y)}) Rumbo {int(p.rumbo)}°\n"
                     f" Armamento: {', '.join(f'{k}:{v}' for k,v in p.armas.items())}\n"
                     f" Sumergido: {'Sí' if getattr(p,'sumergido',False) else 'No'}\n\n"
                     )

    # ----- loop principal -----
    def loop(self):
        for p in self.flota:
            p.actualizar_cinematica()

        self.redibujar()
        self.root.after(33, self.loop)


# ----- MAIN -----
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()