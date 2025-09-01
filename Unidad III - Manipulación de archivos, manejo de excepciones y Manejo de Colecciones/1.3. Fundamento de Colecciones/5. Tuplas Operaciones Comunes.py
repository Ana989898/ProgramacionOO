"""Tuplas como combos inmutables (plato, bebida, postre, precio)."""
combo1 = ("Encebollado", "Cola", "Gelatina", 5.50)
combo2 = ("Seco de Pollo", "Jugo", "Flan", 5.75)
plato, bebida, postre, precio = combo1
print(f"Combo1: {plato} + {bebida} + {postre} = ${precio:.2f}")
print("Posición del precio en combo2:", combo2.index(5.75))
print("Veces 'Flan' en combo2:", combo2.count("Flan"))