# Programación Orientada a Objetos
# Gestión de temperaturas semanales

class RegistroClima:
    def __init__(self):
        self._temperaturas = []  # Encapsulamiento

    def ingresar_temperaturas(self):
        for dia in range(1, 8):
            temp = float(input(f"Ingrese la temperatura del día {dia}: "))
            self._temperaturas.append(temp)

    def calcular_promedio(self):
        if not self._temperaturas:
            return 0
        return sum(self._temperaturas) / len(self._temperaturas)

    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        print(f"Temperatura promedio semanal (POO): {promedio:.2f}°C")

# Uso del programa con POO
registro = RegistroClima()
registro.ingresar_temperaturas()
registro.mostrar_resultado()
