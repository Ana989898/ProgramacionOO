"""POO + TUPLAS: combos del día inmutables que referencian productos por ID."""
from typing import NamedTuple

class Combo(NamedTuple):
id_combo: str
id_plato: str
bebida: str
postre: str
precio_combo: float

class InventarioTuplas:
def __init__(self):
self._items: dict[str, Producto] = {}
self._combos: tuple[Combo, ...] = tuple()

# CRUD productos
def anadir(self, p: Producto):
if p.id in self._items:
raise KeyError("ID duplicado")
self._items[p.id] = p

def eliminar(self, id_):
self._items.pop(str(id_), None)

def actualizar(self, id_, cantidad=None, precio=None):
p = self._items.get(str(id_))
if not p:
raise KeyError("No existe")
if cantidad is not None: p.cantidad = int(cantidad)
if precio is not None: p.precio = float(precio)

def buscar_nombre(self, texto):
q = texto.lower()
return [p for p in self._items.values() if q in p.nombre.lower()]

def mostrar(self):
for p in self._items.values():
print(p)
if self._combos:
print("-- Combos --")
for c in self._combos:
base = self._items.get(c.id_plato)
nombre = base.nombre if base else "(desconocido)"
print(f"[{c.id_combo}] {nombre} + {c.bebida} + {c.postre} -> ${c.precio_combo:.2f}")

# Gestión de combos usando tuplas inmutables
def definir_combos(self, combos: tuple[Combo, ...]):
self._combos = combos

invT = InventarioTuplas()
invT.anadir(Producto("7","Seco de Pollo", 9, 5.75))
invT.anadir(Producto("8","Yaguarlocro", 6, 4.75))
invT.definir_combos((
Combo("C1","7","Jugo de naranjilla","Flan", 6.50),
Combo("C2","8","Cola","Gelatina", 5.50),
))
print("\n[InventarioTuplas] Productos y combos:")
invT.mostrar()