def convertir_temperatura(valor: float, unidad_origen: str, unidad_destino: str) -> float:
    if unidad_origen == "celsius":
        if unidad_destino == "fahrenheit":
            return valor * 9/5 + 32
        elif unidad_destino == "kelvin":
            return valor + 273.15
    elif unidad_origen == "fahrenheit":
        if unidad_destino == "celsius":
            return (valor - 32) * 5/9
        elif unidad_destino == "kelvin":
            return (valor - 32) * 5/9 + 273.15
    elif unidad_origen == "kelvin":
        if unidad_destino == "celsius":
            return valor - 273.15
        elif unidad_destino == "fahrenheit":
            return (valor - 273.15) * 9/5 + 32
    return valor  # Si unidad_origen y unidad_destino son iguales

def main():
    print("=== Conversor de Temperatura ===")
    valor_input = input("Ingresa el valor de temperatura: ")
    unidad_origen = input("Ingresa la unidad de origen (celsius/fahrenheit/kelvin): ").lower()
    unidad_destino = input("Ingresa la unidad de destino (celsius/fahrenheit/kelvin): ").lower()

    # Tipos de datos
    temperatura = float(valor_input)  # float
    conversion_exitosa = True         # boolean

    if unidad_origen not in ["celsius", "fahrenheit", "kelvin"] or unidad_destino not in ["celsius", "fahrenheit", "kelvin"]:
        print("Unidad no válida.")
        conversion_exitosa = False
    else:
        resultado = convertir_temperatura(temperatura, unidad_origen, unidad_destino)
        print(f"\n{temperatura}° {unidad_origen.capitalize()} equivalen a {resultado:.2f}° {unidad_destino.capitalize()}.")

    print(f"\n¿Conversión realizada exitosamente? {conversion_exitosa}")  # boolean output

if __name__ == "__main__":
    main()
