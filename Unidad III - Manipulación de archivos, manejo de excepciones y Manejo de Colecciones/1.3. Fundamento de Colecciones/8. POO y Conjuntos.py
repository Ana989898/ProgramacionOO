"""POO con SETS para etiquetas/alérgenos por producto."""
class InventarioSets:
def __init__(self):
self._items: dict[str, Producto] = {}
self._tags: dict[str, set[str]] = {} # tags por ID (p.ej., {"mariscos","picante"})

def anadir(self, p: Producto, tags: set[str] | None = None):
if p.id in self._items:
raise KeyError("ID duplicado")
self._items[p.id] = p
self._tags[p.id] = set(tags) if tags else set()

def eliminar(self, id_):
self._items.pop(str(id_), None)
self._tags.pop(str(id_), None)

def actualizar(self, id_, cantidad=None, precio=None):
p = self._items.get(str(id_))
if not p:
raise KeyError("No existe")
if cantidad is not None: p.cantidad = int(cantidad)
if precio is not None: p.precio = float(precio)

def agregar_tag(self, id_, *tags):
self._tags.setdefault(str(id_), set()).update(tags)

def buscar_nombre(self, texto):
q = texto.lower()
return [p for p in self._items.values() if q in p.nombre.lower()]

def mostrar(self):
for p in self._items.values():
tags = ", ".join(sorted(self._tags.get(p.id, set())))
print(f"{p} | Tags: {tags}")

invS = InventarioSets()
invS.anadir(Producto("6","Ceviche Mixto",10,7.5), {"mariscos","frío"})
invS.agregar_tag("6","limón")
print("\n[InventarioSets] Todos:")
invS.mostrar()