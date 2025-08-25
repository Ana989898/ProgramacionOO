# Inventario.py
# -*- coding: utf-8 -*-
"""
Clase Inventario: administra un conjunto de productos.
Persistencia en archivo CSV (inventario.txt por defecto, delimitador ';').
"""

from typing import List, Optional
from product import Producto
import csv
import os


class Inventario:
    """Gestiona productos con operaciones CRUD y persistencia en archivo."""

    def __init__(self, ruta_archivo: str = "inventario.txt") -> None:
        # Estructuras en memoria
        self._productos: List[Producto] = []
        self._index_by_id: dict[str, Producto] = {}

        # Archivo
        self._ruta_archivo = ruta_archivo
        self._delim = ";"
        self._headers = ["id", "nombre", "cantidad", "precio"]

        # Carga inicial (si no existe, intenta crearlo vacío)
        self._cargar_desde_archivo()

    # ---------- Persistencia ----------
    def _asegurar_archivo(self) -> None:
        """Crea el archivo con cabecera si no existe."""
        if not os.path.exists(self._ruta_archivo):
            try:
                with open(self._ruta_archivo, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=self._delim)
                    writer.writerow(self._headers)
            except PermissionError as e:
                raise PermissionError(
                    f"No se pudo crear el archivo de inventario por permisos: {self._ruta_archivo}"
                ) from e
            except OSError as e:
                raise OSError(
                    f"Error del sistema al crear el archivo de inventario: {self._ruta_archivo}"
                ) from e

    def _cargar_desde_archivo(self) -> None:
        """Reconstruye el inventario desde el archivo."""
        # Limpia estructuras actuales (por si se recarga)
        self._productos.clear()
        self._index_by_id.clear()

        try:
            self._asegurar_archivo()
            with open(self._ruta_archivo, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=self._delim)
                rows = list(reader)
        except FileNotFoundError:
            # Debería estar cubierto por _asegurar_archivo, pero contemplamos carrera
            self._asegurar_archivo()
            rows = []
        except PermissionError as e:
            raise PermissionError(
                f"Sin permisos para leer '{self._ruta_archivo}'."
            ) from e
        except OSError as e:
            raise OSError(
                f"Error al leer el archivo '{self._ruta_archivo}'."
            ) from e

        if not rows:
            return

        # Detecta cabecera
        start_idx = 0
        if rows and rows[0] == self._headers:
            start_idx = 1

        # Parsea filas
        for r in rows[start_idx:]:
            if not r:
                continue
            # Soporta filas con o sin delimitador correcto
            if len(r) != 4:
                # Saltamos filas corruptas de forma segura
                continue
            data = {
                "id": r[0],
                "nombre": r[1],
                "cantidad": r[2],
                "precio": r[3],
            }
            try:
                p = Producto.from_dict(data)
            except Exception:
                # Si una fila está corrupta, la omitimos
                continue
            self._productos.append(p)
            self._index_by_id[p.id] = p

    def _persistir(self) -> None:
        """Escribe el estado actual del inventario al archivo."""
        try:
            # Asegura existencia del archivo y permisos
            self._asegurar_archivo()
            with open(self._ruta_archivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=self._delim)
                writer.writerow(self._headers)
                for p in self._productos:
                    writer.writerow([p.id, p.nombre, p.cantidad, f"{p.precio:.2f}"])
        except PermissionError as e:
            raise PermissionError(
                f"Sin permisos para escribir en '{self._ruta_archivo}'."
            ) from e
        except OSError as e:
            raise OSError(
                f"Error al escribir en el archivo '{self._ruta_archivo}'."
            ) from e

    # ---------- CRUD ----------
    def anadir(self, producto: Producto) -> None:
        """Añade un nuevo producto, validando que el ID sea único y persiste."""
        if producto.id in self._index_by_id:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos.append(producto)
        self._index_by_id[producto.id] = producto
        self._persistir()

    def eliminar_por_id(self, id_: str) -> bool:
        """Elimina un producto por ID. Devuelve True si se eliminó y persiste."""
        prod = self._index_by_id.pop(id_, None)
        if not prod:
            return False
        self._productos = [p for p in self._productos if p.id != id_]
        self._persistir()
        return True

    def actualizar_cantidad(self, id_: str, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto por ID y persiste."""
        prod = self._index_by_id.get(id_)
        if not prod:
            return False
        prod.cantidad = nueva_cantidad
        self._persistir()
        return True

    def actualizar_precio(self, id_: str, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto por ID y persiste."""
        prod = self._index_by_id.get(id_)
        if not prod:
            return False
        prod.precio = nuevo_precio
        self._persistir()
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

    # --- Utilidad ---
    @property
    def ruta_archivo(self) -> str:
        return self._ruta_archivo
