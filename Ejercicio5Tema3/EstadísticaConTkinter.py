import tkinter as tk
from tkinter import messagebox, filedialog
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


# Validación avanzada para las entradas
def validar_entrada(valor, tipo="int"):
    try:
        if tipo == "int":
            return int(valor)
        elif tipo == "float":
            return float(valor)
    except ValueError:
        return None


# Función para calcular estadísticas y graficar resultados
def calcular():
    try:
        n = validar_entrada(entry.get(), "int")
        if n is None or n < 1000:
            messagebox.showerror("Error", "Introduce un número entero mayor a 1000.")
            return

        # Generar números aleatorios entre 0 y 1
        numeros = [random.random() for _ in range(n)]
        suma = sum(numeros)
        suma2 = sum(x * x for x in numeros)
        media = suma / n
        varianza = (suma2 - n * media ** 2) / (n - 1)
        desviacion = varianza ** 0.5
        label_media_valor.config(text=f"{media:.6f}")
        label_varianza_valor.config(text=f"{varianza:.6f}")
        label_desviacion_valor.config(text=f"{desviacion:.6f}")
        resultados_frame.pack(pady=15)

        # Actualizar gráfico existente
        ax1.clear()
        ax1.bar(['Media', 'Varianza', 'Desviación'], [media, varianza, desviacion], color=['#2e7d32', '#1565c0', '#c62828'])
        ax1.set_title('Resultados Estadísticos')
        ax1.set_ylim(0, 1)
        for i, v in enumerate([media, varianza, desviacion]):
            ax1.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=10)

        ax2.clear()
        ax2.hist(numeros, bins=20, color='#4a90e2', edgecolor='black')
        ax2.set_title('Distribución de Números')
        ax2.set_xlabel('Valor')
        ax2.set_ylabel('Frecuencia')

        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# Función para guardar resultados en un archivo
def guardar_resultados():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt"), ("CSV", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            if file_path.endswith(".csv"):
                writer = csv.writer(file)
                writer.writerow(["Media", "Varianza", "Desviación estándar"])
                writer.writerow([label_media_valor["text"], label_varianza_valor["text"], label_desviacion_valor["text"]])
            else:
                file.write("Resultados Estadísticos\n")
                file.write(f"Media: {label_media_valor['text']}\n")
                file.write(f"Varianza: {label_varianza_valor['text']}\n")
                file.write(f"Desviación estándar: {label_desviacion_valor['text']}\n")
        messagebox.showinfo("Éxito", "Resultados guardados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")


# Función para guardar el gráfico como imagen
def guardar_grafico():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos los archivos", "*.*")])
    if not file_path:
        return

    try:
        # Crear una nueva figura para guardar
        fig = Figure(figsize=(6, 4), dpi=100)
        ax1 = fig.add_subplot(121)
        nombres = ['Media', 'Varianza', 'Desviación']
        valores = [float(label_media_valor["text"]), float(label_varianza_valor["text"]), float(label_desviacion_valor["text"])]
        colores = ['#2e7d32', '#1565c0', '#c62828']
        ax1.bar(nombres, valores, color=colores)
        ax1.set_title('Resultados Estadísticos')
        ax1.set_ylim(0, 1)
        for i, v in enumerate(valores):
            ax1.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=10)

        ax2 = fig.add_subplot(122)
        ax2.hist([random.uniform(0, 1) for _ in range(1000)], bins=20, color='#4a90e2', edgecolor='black')
        ax2.set_title('Distribución de Números')
        ax2.set_xlabel('Valor')
        ax2.set_ylabel('Frecuencia')

        fig.tight_layout()
        fig.savefig(file_path)
        messagebox.showinfo("Éxito", "Gráfico guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el gráfico: {e}")


# Función para reiniciar la aplicación
def reiniciar():
    entry.delete(0, tk.END)
    label_media_valor.config(text="-")
    label_varianza_valor.config(text="-")
    label_desviacion_valor.config(text="-")

    # Limpiar el contenido del gráfico pero mantenerlo visible
    ax1.clear()
    ax1.set_title('Resultados Estadísticos')
    ax1.set_ylim(0, 1)

    ax2.clear()
    ax2.set_title('Distribución de Números')
    ax2.set_xlabel('Valor')
    ax2.set_ylabel('Frecuencia')

    canvas.draw()

    resultados_frame.pack_forget()


# Función para mostrar instrucciones
def mostrar_ayuda():
    instrucciones = (
        "Instrucciones de uso:\n"
        "1. Introduce un número mayor a 1000 en el campo principal.\n"
        "2. Haz clic en 'Calcular' para obtener los resultados.\n"
        "3. Usa 'Guardar Resultados' para exportar los datos a un archivo.\n"
        "4. Haz clic en 'Reiniciar' para limpiar la interfaz y empezar de nuevo."
    )
    messagebox.showinfo("Ayuda", instrucciones)


root = tk.Tk()
root.title("Estadística Aleatoria")
root.geometry("500x500")
azul_claro = "#d0e6fa"
azul_clarito = "#e3f2fd"
root.configure(bg=azul_claro)

tk.Label(root, text="Introduce un número (>1000):", font=("Arial", 12, "bold"), bg=azul_claro).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 12), bg=azul_clarito)
entry.pack()

tk.Button(root, text="Calcular", command=calcular, font=("Arial", 12, "bold"), bg="#4a90e2", fg="white", relief="raised").pack(pady=10)

# Botón para guardar resultados
tk.Button(root, text="Guardar Resultados", command=guardar_resultados, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", relief="raised").pack(pady=10)

# Botón para guardar gráfico
tk.Button(root, text="Guardar Gráfico", command=guardar_grafico, font=("Arial", 12, "bold"), bg="#2196f3", fg="white", relief="raised").pack(pady=10)

# Botón para reiniciar
tk.Button(root, text="Reiniciar", command=reiniciar, font=("Arial", 12, "bold"), bg="#f44336", fg="white", relief="raised").pack(pady=10)

resultados_frame = tk.Frame(root, bg=azul_clarito, bd=2, relief="groove")
tk.Label(resultados_frame, text="Resultados", font=("Arial", 14, "bold"), bg=azul_clarito).pack(pady=5)

fila1 = tk.Frame(resultados_frame, bg=azul_clarito)
tk.Label(fila1, text="Media:", font=("Arial", 12), bg=azul_clarito).pack(side="left", padx=5)
label_media_valor = tk.Label(fila1, text="-", font=("Arial", 16, "bold"), fg="#2e7d32", bg=azul_clarito)
label_media_valor.pack(side="left", padx=5)
fila1.pack(pady=5)

fila2 = tk.Frame(resultados_frame, bg=azul_clarito)
tk.Label(fila2, text="Varianza:", font=("Arial", 12), bg=azul_clarito).pack(side="left", padx=5)
label_varianza_valor = tk.Label(fila2, text="-", font=("Arial", 16, "bold"), fg="#1565c0", bg=azul_clarito)
label_varianza_valor.pack(side="left", padx=5)
fila2.pack(pady=5)

fila3 = tk.Frame(resultados_frame, bg=azul_clarito)
tk.Label(fila3, text="Desviación estándar:", font=("Arial", 12), bg=azul_clarito).pack(side="left", padx=5)
label_desviacion_valor = tk.Label(fila3, text="-", font=("Arial", 16, "bold"), fg="#c62828", bg=azul_clarito)
label_desviacion_valor.pack(side="left", padx=5)
fila3.pack(pady=5)

# El frame de resultados se muestra solo tras calcular
resultados_frame.pack_forget()

# Frame para el gráfico
grafico_frame = tk.Frame(root, bg=azul_claro)
grafico_frame.pack(pady=10)

# Crear gráfico vacío al inicio
fig = Figure(figsize=(6, 4), dpi=100)
ax1 = fig.add_subplot(121)
ax1.set_title('Resultados Estadísticos')
ax1.set_ylim(0, 1)  # Fijar eje Y entre 0 y 1
ax2 = fig.add_subplot(122)
ax2.set_title('Distribución de Números')
ax2.set_xlabel('Valor')
ax2.set_ylabel('Frecuencia')

canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Añadir menú de ayuda
menu_bar = tk.Menu(root)
menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Mostrar Ayuda", command=mostrar_ayuda)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
root.config(menu=menu_bar)

root.mainloop()