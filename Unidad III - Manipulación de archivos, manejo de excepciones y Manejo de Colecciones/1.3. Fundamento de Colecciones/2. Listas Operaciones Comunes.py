"""Operaciones frecuentes de listas con el menú."""
menu = ["Ceviche", "Encebollado", "Hornado"]
menu.append("Guatita")
menu.extend(["Locro de Papa", "Bolón"])
menu.insert(1, "Seco de Pollo")
menu.remove("Hornado")
ultimo = menu.pop() # elimina Bolón
print("Menú actual:", menu)
print("Eliminado con pop:", ultimo)
print("Índice de Ceviche:", menu.index("Ceviche"))
print("Cuántas veces Encebollado:", menu.count("Encebollado"))
menu.sort()
print("Ordenado:", menu)
print("Primeros 3:", menu[:3])