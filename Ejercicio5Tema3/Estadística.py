import random

def estadística():
    n = int(input("Introduce un número (mayor a 1000):\n"))
    if n < 1000:
        print("Error, el número tiene que ser superior a 1000")
    else:
        numeros = [random.random() for _ in range (n)]

        media = sum(numeros) / n

        suma_cuadrados = sum((x - media) ** 2 for x in numeros)
        varianza = suma_cuadrados / (n - 1)

        desviacion = varianza ** 0.5

        print(f"\nResultados:")
        print(f"Media: {media}")
        print(f"Varianza: {varianza}")
        print(f"Desviación estándar: {desviacion}")

if __name__ == "__main__":
    estadística()