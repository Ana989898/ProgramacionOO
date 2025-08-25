# test.py
# -*- coding: utf-8 -*-
"""Pruebas básicas para validar el correcto funcionamiento del Inventario con archivo."""
import os
from inventory import Inventario
from product import Producto


def run():
    ruta_test = "inventario_test.txt"
    # Limpieza previa por si quedó del intento anterior
    try:
        if os.path.exists(ruta_test):
            os.remove(ruta_test)
    except Exception:
        pass

    inv = Inventario(ruta_archivo=ruta_test)
    # Creamos dos productos de prueba
    p1 = Producto("A1", "Arroz", 10, 1.25)
    p2 = Producto("B2", "Azúcar", 5, 1.10)
    inv.anadir(p1)
    inv.anadir(p2)

    # Verificar búsqueda y actualizaciones
    assert inv.obtener_por_id("A1") is not None
    assert len(inv.buscar_por_nombre("ar")) == 2  # Coincide con 'Arroz' y 'Azúcar'
    assert inv.actualizar_cantidad("A1", 20)
    assert inv.obtener_por_id("A1").cantidad == 20
    assert inv.eliminar_por_id("B2")
    assert inv.obtener_por_id("B2") is None

    # Verificar carga desde archivo (reconstrucción)
    inv2 = Inventario(ruta_archivo=ruta_test)
    assert inv2.obtener_por_id("A1") is not None
    assert inv2.obtener_por_id("B2") is None

    print("✔ Pruebas básicas OK (con archivo)")

    # Limpieza final
    try:
        os.remove(ruta_test)
    except Exception:
        pass


if __name__ == "__main__":
    run()
