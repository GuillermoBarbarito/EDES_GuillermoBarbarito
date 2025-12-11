import tkinter as tk
import math
import random
from tkinter import simpledialog

# =============================================================
#                    UTILIDAD: CONTRASTE DE COLOR
# =============================================================

def contrasting_color(bg):
    try:
        bg = bg.lstrip("#")
        r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
        luminancia = (0.299*r + 0.587*g + 0.114*b)
        return "white" if luminancia < 128 else "black"
    except:
        return "white"


# =============================================================
#                    MODELOS DE OBJETOS
# =============================================================

class OrbitalObject:
    def __init__(self, name, radius, color, distance=0, angular_speed=0):
        self.name = name
        self.radius = radius
        self.color = color
        self.text_color = contrasting_color(color)

        self.distance = distance
        self.angular_speed = angular_speed
        self.angle = random.random() * 2 * math.pi

        self.x = 0
        self.y = 0
        self.manual_position = True
        self.dragging = False

        self.orbiting = None  # nuevo: planeta al que orbita
        self.fixed_on = None  # nuevo: planeta donde está acoplado

    def update(self, dt):
        if self.fixed_on:
            # cohete pegado al planeta
            self.x = self.fixed_on.x
            self.y = self.fixed_on.y
            return

        if self.orbiting:
            # órbita local
            self.angle += self.angular_speed * dt
            self.x = self.orbiting.x + math.cos(self.angle)*self.distance
            self.y = self.orbiting.y + math.sin(self.angle)*self.distance
            return

        if not self.manual_position:
            # órbita normal alrededor del sol
            self.angle += self.angular_speed * dt
            self.x = math.cos(self.angle) * self.distance
            self.y = math.sin(self.angle) * self.distance



class StaticBody:
    def __init__(self, name, radius, color):
        self.name = name
        self.radius = radius
        self.color = color
        self.text_color = contrasting_color(color)
        self.x = 0
        self.y = 0


# =============================================================
#                    INTERFAZ PRINCIPAL
# =============================================================

class SolarSystemGUI:
    def __init__(self, root):
        self.root = root
        root.title("Sistema Solar Interactivo – NASA Style")

        # --- CANVAS ---
        self.canvas = tk.Canvas(root, width=1050, height=800, bg="black")
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- PANEL NASA ---
        self.info_frame = tk.Frame(root, width=250, bg="#111")
        self.info_frame.pack(side="right", fill="y")

        title = tk.Label(self.info_frame, text="📡 PANEL NASA", bg="#111",
                         fg="#4fc3ff", font=("Consolas", 14, "bold"))
        title.pack(fill="x", pady=10)

        self.info_label = tk.Label(self.info_frame, text="Selecciona un objeto",
                                   bg="#111", fg="white", justify="left",
                                   font=("Consolas", 11), anchor="nw")
        self.info_label.pack(fill="both", expand=True, padx=10)

        # === PANEL SUPERIOR ===
        top = tk.Frame(root, bg="#222")
        top.place(x=0, y=0, width=1050)

        tk.Button(top, text="Añadir planeta", command=self.add_planet).pack(side="left")
        tk.Button(top, text="Añadir satélite", command=self.add_satellite).pack(side="left")
        tk.Button(top, text="Añadir cometa", command=self.add_comet).pack(side="left")
        tk.Button(top, text="Añadir cohete", command=self.add_rocket).pack(side="left")
        tk.Button(top, text="Borrar objeto", command=self.delete_object).pack(side="left")
        tk.Button(top, text="Nuevo sistema (con Sol)", command=self.new_solar_system).pack(side="left")
        tk.Button(top, text="Sistema vacío", command=self.empty_system).pack(side="left")

        # Cámara
        self.zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0

        # Estados
        self.objects = []
        self.dragged_object = None
        self.dragging_view = False
        self.selected_object = None

        # Eventos
        self.canvas.bind("<MouseWheel>", self.zoom_event)  # ← ERROR FIXED
        self.canvas.bind("<ButtonPress-1>", self.view_drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.view_drag_stop)
        self.canvas.bind("<B1-Motion>", self.view_drag_move)
        self.canvas.bind("<Button-1>", self.select_object)

        self.canvas.bind("<ButtonPress-3>", self.object_drag_start)
        self.canvas.bind("<B3-Motion>", self.object_drag_move)
        self.canvas.bind("<ButtonRelease-3>", self.object_drag_stop)

        self.create_default_system()
        self.animate()

    # ================================================================
    #                        CÁMARA
    # ================================================================

    def zoom_event(self, event):
        if event.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom *= 0.9

    def view_drag_start(self, event):
        self.dragging_view = True
        self.last_x = event.x
        self.last_y = event.y

    def view_drag_stop(self, event):
        self.dragging_view = False

    def view_drag_move(self, event):
        if self.dragging_view:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.camera_x += dx
            self.camera_y += dy
            self.last_x = event.x
            self.last_y = event.y

    # ================================================================
    #                     PANEL NASA – SELECCIÓN
    # ================================================================

    def select_object(self, event):
        wx = (event.x - self.camera_x - 525) / self.zoom
        wy = (event.y - self.camera_y - 400) / self.zoom

        for obj in reversed(self.objects):
            if (obj.x - wx)**2 + (obj.y - wy)**2 <= (obj.radius * self.zoom)**2:
                self.selected_object = obj
                self.update_info_panel()
                return

    def update_info_panel(self):
        obj = self.selected_object
        if obj is None:
            self.info_label.config(text="Selecciona un objeto")
            return

        tipo = "Estrella" if isinstance(obj, StaticBody) else "Objeto orbital"
        orbit_info = ""

        if hasattr(obj, "orbiting") and obj.orbiting:
            orbit_info = f"\nOrbitando: {obj.orbiting.name}"

        if hasattr(obj, "fixed_on") and obj.fixed_on:
            orbit_info = f"\nAcoplado a: {obj.fixed_on.name}"

        info = (
            f"=== INFORMACIÓN ===\n"
            f"Nombre: {obj.name}\n"
            f"Tipo: {tipo}\n\n"
            f"Radio: {obj.radius}\n"
            f"Color: {obj.color}\n"
            f"{orbit_info}\n\n"
            f"Posición actual:\n"
            f"  x = {obj.x:.1f}\n"
            f"  y = {obj.y:.1f}\n"
        )

        self.info_label.config(text=info)

    # ================================================================
    #                       CREACIÓN DE OBJETOS
    # ================================================================

    def delete_object(self):
        name = simpledialog.askstring("Eliminar", "Nombre del objeto a borrar:")
        if not name:
            return

        for obj in list(self.objects):
            if obj.name == name:
                self.objects.remove(obj)

                if self.selected_object == obj:
                    self.selected_object = None
                    self.update_info_panel()

                return

    def new_solar_system(self):
        self.objects = []
        self.sun = StaticBody("Sol", 40, "yellow")
        self.objects.append(self.sun)
        self.selected_object = None
        self.update_info_panel()

    def empty_system(self):
        self.objects = []
        self.selected_object = None
        self.update_info_panel()

    def create_default_system(self):
        self.new_solar_system()

        planets = [
            ("Mercurio", 6, "#b1b1b1", 90, 0.03),
            ("Venus", 10, "#d4a76a", 150, 0.02),
            ("Tierra", 12, "#4fa3ff", 210, 0.018),
            ("Marte", 9, "#ff7240", 270, 0.015),
        ]

        for name, r, c, d, s in planets:
            obj = OrbitalObject(name, r, c, d, s)
            obj.manual_position = False
            obj.x = d
            obj.y = 0
            self.objects.append(obj)

    def create_free_object(self, name, radius, color):
        obj = OrbitalObject(name, radius, color)
        obj.x = 0
        obj.y = 0
        self.objects.append(obj)
        self.dragged_object = obj
        return obj

    def add_planet(self):
        name = simpledialog.askstring("Planeta", "Nombre:")
        if name:
            self.create_free_object(name, random.randint(10, 20), "#4fa3ff")

    def add_satellite(self):
        name = simpledialog.askstring("Satélite", "Nombre:")
        if name:
            self.create_free_object(name, 6, "#cccccc")

    def add_comet(self):
        name = simpledialog.askstring("Cometa", "Nombre:")
        if name:
            self.create_free_object(name, 5, "#ffffff")

    def add_rocket(self):
        name = simpledialog.askstring("Cohete", "Nombre:")
        if name:
            self.create_free_object(name, 7, "red")

    # ================================================================
    #                    ARRASTRE DE OBJETOS
    # ================================================================

    def object_drag_start(self, event):
        wx = (event.x - self.camera_x - 525) / self.zoom
        wy = (event.y - self.camera_y - 400) / self.zoom

        for obj in reversed(self.objects):
            if isinstance(obj, StaticBody):
                continue
            if (obj.x - wx)**2 + (obj.y - wy)**2 <= obj.radius**2 * 4:
                self.dragged_object = obj
                obj.manual_position = True
                return

    def object_drag_move(self, event):
        if not self.dragged_object:
            return

        self.dragged_object.x = (event.x - self.camera_x - 525) / self.zoom
        self.dragged_object.y = (event.y - self.camera_y - 400) / self.zoom

    def object_drag_stop(self, event):
        if not self.dragged_object:
            return

        obj = self.dragged_object

        # mirar si se colocó sobre un planeta
        for target in self.objects:
            if isinstance(target, StaticBody):
                continue
            if obj == target:
                continue

            dist = math.dist((obj.x, obj.y), (target.x, target.y))
            if dist <= target.radius * 2:

                if obj.radius <= 7:  # satélite
                    obj.orbiting = target
                    obj.fixed_on = None
                    obj.distance = target.radius + 20
                    obj.angle = random.random()*2*math.pi
                    obj.angular_speed = 0.04
                elif obj.radius == 7:  # cohete
                    obj.fixed_on = target
                    obj.orbiting = None

                self.dragged_object = None
                return

        # órbita normal si no está sobre un planeta
        dx = obj.x
        dy = obj.y
        dist = math.sqrt(dx*dx + dy*dy)
        dist = max(dist, 5)

        obj.distance = dist
        obj.angular_speed = 0.02 / (dist / 150 + 0.5)
        obj.manual_position = False
        obj.fixed_on = None
        obj.orbiting = None
        self.dragged_object = None

    # ================================================================
    #                        ANIMACIÓN
    # ================================================================

    def animate(self):
        self.canvas.delete("all")

        # Dibujar órbitas
        for obj in self.objects:
            if isinstance(obj, OrbitalObject):
                if obj.orbiting:
                    d = obj.distance * self.zoom
                    ox = 525 + self.camera_x + obj.orbiting.x * self.zoom
                    oy = 400 + self.camera_y + obj.orbiting.y * self.zoom
                elif not obj.manual_position:
                    d = obj.distance * self.zoom
                    ox = 525 + self.camera_x
                    oy = 400 + self.camera_y
                else:
                    continue

                self.canvas.create_oval(
                    ox - d, oy - d, ox + d, oy + d,
                    outline="#444"
                )

        # Update
        for obj in self.objects:
            if isinstance(obj, OrbitalObject):
                obj.update(0.5)

        # Dibujar objetos
        for obj in self.objects:
            px = 525 + self.camera_x + obj.x * self.zoom
            py = 400 + self.camera_y + obj.y * self.zoom
            r = obj.radius * self.zoom

            self.canvas.create_oval(px-r, py-r, px+r, py+r,
                                    fill=obj.color, outline="#222")

            self.canvas.create_text(px, py, text=obj.name,
                                    fill=obj.text_color)

        if self.selected_object:
            self.update_info_panel()

        self.root.after(16, self.animate)


# =============================================================
#                           EJECUCIÓN
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()
    SolarSystemGUI(root)
    root.mainloop()