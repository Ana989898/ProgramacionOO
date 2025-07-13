import os

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            print(f"\n--- Código de {ruta_script} ---\n")
            print(archivo.read())
    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

def mostrar_menu():
    ruta_base = os.path.dirname(__file__)

    opciones = {
        '1': 'Unidad I - Fundamentos de la POO/Semana 2 - Técnicas de Programación/Abstracción/Abstracción.py',
        '2': 'Unidad I - Fundamentos de la POO/Semana 2 - Técnicas de Programación/Encapsulación/Encapsulación.py',
        '3': 'Unidad I - Fundamentos de la POO/Semana 2 - Técnicas de Programación/Herencia/Herencia.py',
        '4': 'Unidad I - Fundamentos de la POO/Semana 2 - Técnicas de Programación/Polimorfismo/Polimorfismo.py',
        '5': 'Unidad I - Fundamentos de la POO/Semana 3 - Programación tradicional frente a POO/Programación Tradicional.py',
        '6': 'Unidad I - Fundamentos de la POO/Semana 3 - Programación tradicional frente a POO/Programación Orientada a Objetos (POO).py',
        '7': 'Unidad I - Fundamentos de la POO/Semana 4 - Ejemplos del Mundo Real POO/EjemplosMundoReal_POO.py',
        '8': 'Unidad II - Objetos, clases, Herencia, Polimorfismo/Semana 5 - Tipos de datos e identificadores/semana 5.py',
        '9': 'Unidad II - Objetos, clases, Herencia, Polimorfismo/Semana 6 - Clases, objetos, herencia, encapsulamiento y polimorfismo/POO.py',
        '10': 'Unidad II - Objetos, clases, Herencia, Polimorfismo/Semana 7 - Constructores y Destructores/Constructores y Destructores.py'
    }

    while True:
        print("\n=== Menú Principal - Dashboard ===")
        for key in opciones:
            print(f"{key} - {opciones[key]}")
        print("0 - Salir")

        eleccion = input("Elige un número para ver el código o '0' para salir: ")

        if eleccion == '0':
            break
        elif eleccion in opciones:
            ruta_script = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo(ruta_script)
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
