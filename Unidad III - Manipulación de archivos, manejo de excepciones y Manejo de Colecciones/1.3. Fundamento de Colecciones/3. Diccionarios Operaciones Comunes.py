"""Diccionario de precios: altas, bajas, cambios y consultas."""
precios = {"Ceviche": 6.0, "Encebollado": 4.5, "Guatita": 4.75}
print("Precio Hornado (get):", precios.get("Hornado", "No disponible"))
precios.setdefault("Hornado", 7.0)
precios.update({"Ceviche": 6.5, "Locro de Papa": 3.5})
baja = precios.pop("Guatita")
print("Se dio de baja Guatita a $", baja)
for plato, valor in precios.items():
print(f"- {plato}: ${valor:.2f}")
# Comprensión: aumentar 12% por temporada alta
precios_temporada = {k: round(v * 1.12, 2) for k, v in precios.items()}
print("Temporada alta:", precios_temporada)