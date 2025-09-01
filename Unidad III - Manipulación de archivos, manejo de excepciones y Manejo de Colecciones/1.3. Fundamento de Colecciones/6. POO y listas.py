"""POO con LISTAS como contenedor del inventario."""
class Producto:
def __init__(self, id_, nombre, cantidad, precio):
self._id = str(id_)
self.nombre = nombre
self.cantidad = int(cantidad)
self.precio = float(precio)
@property
def id(self):
return self._id
def __str__(self):
return f"[{self.id}] {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"
class InventarioListas:
def __init__(self):
self._items: list[Producto] = []
def anadir(self, p: Producto):
# Evitar IDs duplicados
if any(x.id == p.id for x in self._items):
raise KeyError("ID duplicado")
self._items.append(p)
def eliminar(self, id_):
self._items = [x for x in self._items if x.id != str(id_)]
def actualizar(self, id_, cantidad=None, precio=None):
for x in self._items:
if x.id == str(id_):
if cantidad is not None: x.cantidad = int(cantidad)
if precio is not None: x.precio = float(precio)
return
raise KeyError("Producto no encontrado")
def buscar_nombre(self, texto):
q = texto.lower()
return [x for x in self._items if q in x.nombre.lower()]
def mostrar(self):
for x in self._items:
print(x)
invL = InventarioListas()
invL.anadir(Producto("1","Ceviche",10,6.0))
invL.anadir(Producto("2","Encebollado",12,4.5))
invL.actualizar("2", precio=5.0)
print("\n[InventarioListas] Todos:")
invL.mostrar()
print("Buscar 'cevi':", [str(p) for p in invL.buscar_nombre("cevi")])