"""POO con DICCIONARIO para acceso O(1) por ID."""
class InventarioDict:
def __init__(self):
self._items: dict[str, Producto] = {}

def anadir(self, p: Producto):
if p.id in self._items:
raise KeyError("ID duplicado")
self._items[p.id] = p

def eliminar(self, id_):
if str(id_) not in self._items:
raise KeyError("No existe")
del self._items[str(id_)]

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

invD = InventarioDict()
for d in [("3","Hornado",8,7.0),("4","Locro de Papa",15,3.5),("5","Fritada",9,5.5)]:
invD.anadir(Producto(*d))
invD.actualizar("4", cantidad=18)
print("\n[InventarioDict] Todos:")
invD.mostrar()
print("Buscar 'lo':", [str(p) for p in invD.buscar_nombre("lo")])