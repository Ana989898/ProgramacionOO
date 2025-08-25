# main.py
# -*- coding: utf-8 -*-
"""
Interfaz de usuario en consola.
Permite interactuar con el Inventario mediante un menú.
"""

from typing import Optional
from inventory import Inventario
from product import Producto


# --- Funciones auxiliares para entrada de datos ---
def input_no_vacio(mensaje: str) -> str:
    """Valida que la entrada no esté vacía."""
    while True:
        s = input(mensaje).strip()
        if s:
            return s
        print("Entrada vacía. Intente nuevamente.")


def input_entero(mensaje: str, minimo: Optional[int] = None) -> int:
    """Valida que la entrada sea un número entero >= mínimo."""
    while True:
        try:
            v = int(input(mensaje))
            if minimo is not None and v < minimo:
                print(f"Debe ser un entero >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingrese un número entero válido.")


def input_float(mensaje: str, minimo: Optional[float] = None) -> float:
    """Valida que la entrada sea un número decimal >= mínimo."""
    while True:
        try:
            v = float(input(mensaje))
            if minimo is not None and v < minimo:
                print(f"Debe ser un número >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingrese un número válido (use punto decimal).")


def mostrar_producto(p: Producto) -> None:
    """Muestra un producto en formato legible."""
    print(f"- ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: ${p.precio:.2f}")


# --- Menú interactivo ---
def menu() -> None:
    try:
        inventario = Inventario()
        cargados = len(inventario.obtener_todos())
        print(f"📂 Archivo: '{inventario.ruta_archivo}'. Productos cargados: {cargados}.")
    except PermissionError as e:
        print(f"✖ Error de permisos al abrir el inventario: {e}")
        return
    except OSError as e:
        print(f"✖ Error al acceder al archivo de inventario: {e}")
        return

    opciones = {
        "1": "Añadir producto",
        "2": "Eliminar producto por ID",
        "3": "Actualizar cantidad por ID",
        "4": "Actualizar precio por ID",
        "5": "Buscar producto(s) por nombre",
        "6": "Mostrar todos los productos",
        "0": "Salir",
    }

    while True:
        print("\n" + "=" * 60)
        print(" SISTEMA DE GESTIÓN DE INVENTARIO ")
        print("=" * 60)
        for k, v in opciones.items():
            print(f"{k}. {v}")
        eleccion = input("Seleccione una opción: ").strip()

        if eleccion == "1":
            # Crear producto
            try:
                id_ = input_no_vacio("ID único: ")
                nombre = input_no_vacio("Nombre: ")
                cantidad = input_entero("Cantidad (entero >= 0): ", minimo=0)
                precio = input_float("Precio (>= 0): ", minimo=0.0)
                producto = Producto(id_, nombre, cantidad, precio)
                inventario.anadir(producto)
                print(f"✔ Producto añadido y guardado en '{inventario.ruta_archivo}'.")
            except ValueError as e:
                print(f"✖ Datos inválidos: {e}")
            except PermissionError as e:
                print(f"✖ No se pudo escribir el archivo: {e}")
            except OSError as e:
                print(f"✖ Error al guardar en archivo: {e}")

        elif eleccion == "2":
            # Eliminar producto
            id_ = input_no_vacio("ID a eliminar: ")
            try:
                if inventario.eliminar_por_id(id_):
                    print(f"✔ Producto eliminado y cambios guardados en '{inventario.ruta_archivo}'.")
                else:
                    print("✖ No existe un producto con ese ID.")
            except PermissionError as e:
                print(f"✖ No se pudo escribir el archivo: {e}")
            except OSError as e:
                print(f"✖ Error al guardar en archivo: {e}")

        elif eleccion == "3":
            # Actualizar cantidad
            id_ = input_no_vacio("ID a actualizar (cantidad): ")
            if not inventario.obtener_por_id(id_):
                print("✖ No existe un producto con ese ID.")
                continue
            nueva_cantidad = input_entero("Nueva cantidad (>= 0): ", minimo=0)
            try:
                if inventario.actualizar_cantidad(id_, nueva_cantidad):
                    print(f"✔ Cantidad actualizada y guardada en '{inventario.ruta_archivo}'.")
            except PermissionError as e:
                print(f"✖ No se pudo escribir el archivo: {e}")
            except OSError as e:
                print(f"✖ Error al guardar en archivo: {e}")

        elif eleccion == "4":
            # Actualizar precio
            id_ = input_no_vacio("ID a actualizar (precio): ")
            if not inventario.obtener_por_id(id_):
                print("✖ No existe un producto con ese ID.")
                continue
            nuevo_precio = input_float("Nuevo precio (>= 0): ", minimo=0.0)
            try:
                if inventario.actualizar_precio(id_, nuevo_precio):
                    print(f"✔ Precio actualizado y guardado en '{inventario.ruta_archivo}'.")
            except PermissionError as e:
                print(f"✖ No se pudo escribir el archivo: {e}")
            except OSError as e:
                print(f"✖ Error al guardar en archivo: {e}")

        elif eleccion == "5":
            # Buscar por nombre
            termino = input_no_vacio("Buscar por nombre (parcial): ")
            resultados = inventario.buscar_por_nombre(termino)
            if resultados:
                print(f"✔ Se encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    mostrar_producto(p)
            else:
                print("✖ No se encontraron productos que coincidan.")

        elif eleccion == "6":
            # Mostrar todos
            productos = inventario.obtener_todos()
            if not productos:
                print("Inventario vacío.")
            else:
                print("Productos en inventario:")
                for p in productos:
                    mostrar_producto(p)

        elif eleccion == "0":
            # Salida
            print("Hasta pronto 👋")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == '__main__':
    menu()
