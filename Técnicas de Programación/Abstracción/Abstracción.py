class Cafetera:
    def preparar_cafe(self):
        self.moler_granos()
        self.hervir_agua()
        self.servir_cafe()

    def moler_granos(self):
        print("Moliento los granos...")

    def hervir_agua(self):
        print("Hirviendo el agua...")

    def servir_cafe(self):
        print("Sirviendo café...")

cafetera = Cafetera()
cafetera.preparar_cafe()  # El usuario solo necesita llamar a una función, sin saber los detalles.
