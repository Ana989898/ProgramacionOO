"""Sets de ingredientes y operaciones de conjunto."""
ceviche = {"pescado", "limón", "cebolla", "cilantro"}
encebollado = {"pescado", "yuca", "cebolla", "orégano"}
print("Unión:", ceviche | encebollado)
print("Intersección:", ceviche & encebollado)
print("Diferencia (ceviche - encebollado):", ceviche - encebollado)
print("Simétrica:", ceviche ^ encebollado)
ceviche.add("maní")
ceviche.discard("pulpo")
print("Ceviche actualizado:", ceviche)
print("¿Intersección ⊆ Ceviche?", (ceviche & encebollado).issubset(ceviche))