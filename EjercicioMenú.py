import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# Inicializar pygame
pygame.mixer.init()

# 🎵 Música de fondo
def reproducir_musica_inicio():
    pygame.mixer.music.load("super_mario.mp3")  # Música de fondo
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Repetir indefinidamente

# 🎤 Sonidos de entrada y salida
def sonido_hello():
    try:
        efecto = pygame.mixer.Sound("hello_mario.mp3")  # Recomendado: usar .wav
        efecto.set_volume(1.0)
        efecto.play()
    except pygame.error:
        print("Error al cargar hello_mario.mp3")

def sonido_bye():
    try:
        efecto = pygame.mixer.Sound("bye_mario.mp3")  # Recomendado: usar .wav
        efecto.set_volume(1.0)
        efecto.play()
    except pygame.error:
        print("Error al cargar bye_mario.mp3")

# 🧙‍♂️ Animación del caballerito
def animar_caballerito(etiqueta, frames, frame=0):
    etiqueta.config(image=frames[frame])
    etiqueta.image = frames[frame]
    frame = (frame + 1) % len(frames)
    etiqueta.after(300, animar_caballerito, etiqueta, frames, frame)

# Pantalla de bienvenida
def pantalla_inicio():
    ventana = tk.Tk()
    ventana.title("Bienvenido al Portal Escolar")
    ventana.geometry("600x500")
    ventana.configure(bg="#0d0d0d")

    reproducir_musica_inicio()
    sonido_hello()

    tk.Label(ventana, text="¡Hola, aventurero del IES Rafael Alberti!", font=("Courier New", 16), fg="#00ffcc", bg="#0d0d0d").pack(pady=20)

    # Cargar frames del caballerito con manejo de errores
    frames = []
    for i in range(1, 5):  # caballero1.png a caballero4.png
        try:
            img = Image.open(f"caballero{i}.png").resize((100, 100))
            frames.append(ImageTk.PhotoImage(img))
        except FileNotFoundError:
            print(f"Imagen caballero{i}.png no encontrada.")

    etiqueta = tk.Label(ventana, bg="#0d0d0d")
    etiqueta.pack(pady=10)
    if frames:
        animar_caballerito(etiqueta, frames)

    tk.Button(ventana, text="Entrar al menú", font=("Arial", 14), bg="#4caf50", fg="white", command=lambda:[ventana.destroy(), mostrar_menu()]).pack(pady=30)

    ventana.protocol("WM_DELETE_WINDOW", lambda:[sonido_bye(), ventana.destroy()])
    ventana.mainloop()

# Menú principal
def mostrar_menu():
    ventana = tk.Tk()
    ventana.title("IES Rafael Alberti - Portal Escolar")
    ventana.geometry("700x600")
    ventana.configure(bg="#0d0d0d")

    try:
        img = Image.open("alberti.jpg").resize((300, 300))
        imagen = ImageTk.PhotoImage(img)
        label_img = tk.Label(ventana, image=imagen, bg="#0d0d0d")
        label_img.image = imagen
        label_img.pack(pady=10)
    except FileNotFoundError:
        print("Imagen alberti.jpg no encontrada.")

    tk.Label(ventana, text="UTILIDADES ESCOLARES", font=("Courier New", 20, "bold"), fg="#00ffcc", bg="#0d0d0d").pack(pady=10)

    tk.Button(ventana, text="🌡️ Convertir temperatura", font=("Arial", 14), bg="#00bcd4", fg="black", command=lambda:[ventana.destroy(), ventana_temperatura()]).pack(pady=10)
    tk.Button(ventana, text="📊 Tabla de multiplicar", font=("Arial", 14), bg="#8bc34a", fg="black", command=lambda:[ventana.destroy(), ventana_tabla()]).pack(pady=10)
    tk.Button(ventana, text="❌ Salir", font=("Arial", 14), bg="#f44336", fg="white", command=lambda:[sonido_bye(), ventana.destroy()]).pack(pady=20)

    ventana.protocol("WM_DELETE_WINDOW", lambda:[sonido_bye(), ventana.destroy()])
    ventana.mainloop()

# Pantalla de temperatura
def ventana_temperatura():
    ventana = tk.Tk()
    ventana.title("Conversión de temperatura")
    ventana.geometry("500x400")
    ventana.configure(bg="#1a1a1a")

    tk.Label(ventana, text="Celsius a Fahrenheit", font=("Courier New", 18), fg="#ff9800", bg="#1a1a1a").pack(pady=20)
    entrada = tk.Entry(ventana, font=("Arial", 14))
    entrada.pack(pady=10)
    resultado = tk.Label(ventana, text="", font=("Arial", 14), fg="#ffffff", bg="#1a1a1a")
    resultado.pack(pady=10)

    def convertir():
        valor = entrada.get()
        if valor.replace('.', '', 1).isdigit() or (valor.startswith('-') and valor[1:].replace('.', '', 1).isdigit()):
            fahrenheit = (float(valor) * 9/5) + 32
            resultado.config(text=f"{valor}°C = {fahrenheit:.2f}°F")
        else:
            messagebox.showerror("Error", "Introduce un número válido.")

    tk.Button(ventana, text="Convertir", font=("Arial", 12), bg="#00bcd4", fg="black", command=convertir).pack(pady=5)
    tk.Button(ventana, text="🔙 Volver", font=("Arial", 12), bg="#9e9e9e", command=lambda:[ventana.destroy(), mostrar_menu()]).pack(pady=10)

    ventana.mainloop()

# Pantalla de tabla
def ventana_tabla():
    ventana = tk.Tk()
    ventana.title("Tabla de multiplicar")
    ventana.geometry("500x500")
    ventana.configure(bg="#212121")

    tk.Label(ventana, text="Tabla de multiplicar", font=("Courier New", 18), fg="#4caf50", bg="#212121").pack(pady=20)
    entrada = tk.Entry(ventana, font=("Arial", 14))
    entrada.pack(pady=10)
    resultado = tk.Label(ventana, text="", font=("Courier", 12), fg="#ffffff", bg="#212121", justify="left")
    resultado.pack(pady=10)

    def mostrar_tabla():
        valor = entrada.get()
        if valor.isdigit() or (valor.startswith('-') and valor[1:].isdigit()):
            tabla = "\n".join([f"{valor} x {i} = {int(valor) * i}" for i in range(1, 11)])
            resultado.config(text=tabla)
        else:
            messagebox.showerror("Error", "Introduce un número entero válido.")

    tk.Button(ventana, text="Generar tabla", font=("Arial", 12), bg="#8bc34a", fg="black", command=mostrar_tabla).pack(pady=5)
    tk.Button(ventana, text="🔙 Volver", font=("Arial", 12), bg="#9e9e9e", command=lambda:[ventana.destroy(), mostrar_menu()]).pack(pady=10)

    ventana.mainloop()

# Iniciar
pantalla_inicio()