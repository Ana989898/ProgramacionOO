class Gato:
    def hablar(self):
        return "Miau"

class Pato:
    def hablar(self):
        return "Cuac"

animales = [Gato(), Pato()]
for animal in animales:
    print(animal.hablar())  # Miau, luego Cuac
