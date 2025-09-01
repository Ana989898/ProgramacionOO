"""Colecciones básicas para un restaurante ecuatoriano con precios."""


# Lista del menú (ordenada, mutable)
menu = ["Ceviche", "Encebollado", "Hornado", "Locro de Papa", "Fritada", "Bolón"]


# Diccionario de precios (clave = nombre del plato)
precios = {
"Ceviche": 6.00,
"Encebollado": 4.50,
"Hornado": 7.00,
"Locro de Papa": 3.50,
"Fritada": 5.50,
"Bolón": 2.50,
}


# Conjunto de ingredientes base
ingredientes_base = {"pescado", "yuca", "plátano", "maíz", "cerdo", "papa", "limón"}


# Tuplas como registros inmutables
plato_destacado = ("Seco de Pollo", 5.75)


print(menu)
print(precios)
print(ingredientes_base)
print(plato_destacado)