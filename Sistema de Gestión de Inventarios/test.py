# test.py
# -*- coding: utf-8 -*-
"""Pruebas básicas para validar el correcto funcionamiento del Inventario."""

from inventory import Inventario
from product import Producto


def run():
    inv = Inventario()
    # Creamos dos productos de prueba
    p1 = Producto("A1", "Arroz", 10, 1.25)
    p2 = Producto("B2", "Azúcar", 5, 1.10)
    inv.anadir(p1)
    inv.anadir(p2)

    # Verificar búsqueda y actualizaciones
    assert inv.obtener_por_id("A1") is p1
    assert len(inv.buscar_por_nombre("ar")) == 2  # Coincide con 'Arroz' y 'Azúcar'
    assert inv.actualizar_cantidad("A1", 20)
    assert inv.obtener_por_id("A1").cantidad == 20
    assert inv.eliminar_por_id("B2")
    assert inv.obtener_por_id("B2") is None

    print("✔ Pruebas básicas OK")


if __name__ == "__main__":
    run()
