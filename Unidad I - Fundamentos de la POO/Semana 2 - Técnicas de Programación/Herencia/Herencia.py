class Animal:
    def hablar(self):
        print("Hace un sonido")

class Perro(Animal):
    def hablar(self):
        print("Guau guau")

mi_perro = Perro()
mi_perro.hablar()  # Guau guau (usa su propia versión del método)
