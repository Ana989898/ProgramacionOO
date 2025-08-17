# product.py
# -*- coding: utf-8 -*-
"""
Clase Producto: representa un artículo dentro del inventario.
"""

from typing import Any


class Producto:
    """Representa un producto del inventario con ID, nombre, cantidad y precio."""

    def __init__(self, id_: str, nombre: str, cantidad: int, precio: float) -> None:
        # Los atributos son privados para obligar al uso de getters y setters
        self._id = None
        self._nombre = None
        self._cantidad = None
        self._precio = None

        # Se asignan valores a través de los setters (validación incluida)
        self.id = id_
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # --- ID (único) ---
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("El ID debe ser una cadena no vacía.")
        self._id = value.strip()

    # --- Nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("El nombre debe ser una cadena no vacía.")
        self._nombre = value.strip()

    # --- Cantidad ---
    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int) -> None:
        # Validamos que sea un número entero mayor o igual a 0
        if not isinstance(value, int) or value < 0:
            raise ValueError("La cantidad debe ser un entero >= 0.")
        self._cantidad = value

    # --- Precio ---
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float) -> None:
        # Validamos que sea numérico y mayor a 0
        try:
            value = float(value)
        except Exception as e:
            raise ValueError("El precio debe ser numérico.") from e
        if value < 0:
            raise ValueError("El precio debe ser >= 0.")
        # Redondeamos a 2 decimales
        self._precio = round(value, 2)

    # --- Conversión a diccionario (útil para persistencia) ---
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    # --- Representación en consola ---
    def __repr__(self) -> str:
        return f"Producto(id='{self.id}', nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"
