# Programación Tradicional
# Gestión de temperaturas semanales

# Lista global para almacenar las temperaturas
temperaturas = []

# Función para ingresar las temperaturas diarias
def ingresar_temperaturas():
    for dia in range(1, 8):  # 7 días de la semana
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        temperaturas.append(temp)

# Función para calcular el promedio semanal
def calcular_promedio():
    total = sum(temperaturas)
    promedio = total / len(temperaturas)
    return promedio

# Uso del programa tradicional
ingresar_temperaturas()
promedio = calcular_promedio()
print(f"Temperatura promedio semanal (Tradicional): {promedio:.2f}°C")