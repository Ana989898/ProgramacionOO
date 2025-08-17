# inventory.py
# -*- coding: utf-8 -*-
"""
Clase Inventario: administra un conjunto de productos.
"""

from typing import List, Optional
from product import Producto


class Inventario:
    """Gestiona productos en memoria, permitiendo operaciones CRUD."""

    def __init__(self) -> None:
        # Lista → mantiene el orden de inserción
        self._productos: List[Producto] = []
        # Diccionario → acceso rápido por ID
        self._index_by_id: dict[str, Producto] = {}

    # --- Crear ---
    def anadir(self, producto: Producto) -> None:
        """Añade un nuevo producto, validando que el ID sea único."""
        if producto.id in self._index_by_id:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos.append(producto)
        self._index_by_id[producto.id] = producto

    # --- Eliminar ---
    def eliminar_por_id(self, id_: str) -> bool:
        """Elimina un producto por ID. Devuelve True si se eliminó."""
        prod = self._index_by_id.pop(id_, None)
        if not prod:
            return False
        self._productos = [p for p in self._productos if p.id != id_]
        return True

    # --- Actualizar ---
    def actualizar_cantidad(self, id_: str, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto por ID."""
        prod = self._index_by_id.get(id_)
        if not prod:
            return False
        prod.cantidad = nueva_cantidad
        return True

    def actualizar_precio(self, id_: str, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto por ID."""
        prod = self._index_by_id.get(id_)
        if not prod:
            return False
        prod.precio = nuevo_precio
        return True

    # --- Consultar ---
    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """Busca productos cuyo nombre contenga el término (no sensible a mayúsculas)."""
        t = termino.strip().lower()
        return [p for p in self._productos if t in p.nombre.lower()]

    def obtener_todos(self) -> List[Producto]:
        """Devuelve todos los productos en el inventario."""
        return list(self._productos)

    def obtener_por_id(self, id_: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        return self._index_by_id.get(id_)

