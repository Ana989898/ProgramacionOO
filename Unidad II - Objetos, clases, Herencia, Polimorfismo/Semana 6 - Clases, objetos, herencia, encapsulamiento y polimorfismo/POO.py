# Sistema de inventario para productos de maquillaje

# Clase base: Producto
class Producto:
    def __init__(self, nombre, precio, stock):
        # Encapsulamos atributos sensibles
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock

    # Getters
    def get_nombre(self):
        return self.__nombre

    def get_precio(self):
        return self.__precio

    def get_stock(self):
        return self.__stock

    # Setters
    def set_precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.__precio = nuevo_precio

    def set_stock(self, nuevo_stock):
        if nuevo_stock >= 0:
            self.__stock = nuevo_stock

    # Método polimórfico que se sobrescribirá
    def mostrar_detalle(self):
        print(f"Producto: {self.__nombre}")
        print(f"Precio: ${self.__precio}")
        print(f"Stock disponible: {self.__stock} unidades")

    # Método polimórfico con *args: recibir características variables
    def agregar_caracteristicas(self, *caracteristicas):
        print(f"\n📌 Características de {self.__nombre}:")
        for c in caracteristicas:
            print("-", c)


# Clase derivada: BaseMaquillaje
class BaseMaquillaje(Producto):
    def __init__(self, nombre, precio, stock, tono):
        super().__init__(nombre, precio, stock)
        self.tono = tono

    def mostrar_detalle(self):
        super().mostrar_detalle()
        print(f"Tono: {self.tono}")


# Clase derivada: Labial
class Labial(Producto):
    def __init__(self, nombre, precio, stock, tipo_acabado):
        super().__init__(nombre, precio, stock)
        self.tipo_acabado = tipo_acabado  # mate, gloss, satinado

    def mostrar_detalle(self):
        super().mostrar_detalle()
        print(f"Acabado: {self.tipo_acabado}")


# Clase derivada: PaletaSombras
class PaletaSombras(Producto):
    def __init__(self, nombre, precio, stock, numero_colores):
        super().__init__(nombre, precio, stock)
        self.numero_colores = numero_colores

    def mostrar_detalle(self):
        super().mostrar_detalle()
        print(f"Número de colores: {self.numero_colores}")


# Función para mostrar todos los productos
def mostrar_inventario(productos):
    print("\n🛍️ INVENTARIO DE MAQUILLAJE 🛍️\n")
    for p in productos:
        p.mostrar_detalle()
        print("-" * 40)


# Función principal
def main():
    # Crear productos
    base1 = BaseMaquillaje("Base líquida FitMe", 12.5, 30, "Natural Beige")
    labial1 = Labial("Labial Matte Red", 8.0, 50, "Mate")
    sombra1 = PaletaSombras("Paleta Nude", 18.5, 20, 12)

    # Lista de productos
    inventario = [base1, labial1, sombra1]

    # Mostrar todos los productos
    mostrar_inventario(inventario)

    # Aplicamos encapsulación: cambiar precio y stock del labial
    print("\n🔄 Modificando precio y stock del labial...\n")
    labial1.set_precio(9.0)
    labial1.set_stock(45)

    # Mostrar detalles actualizados
    labial1.mostrar_detalle()

    # Demostramos polimorfismo por argumentos variables
    sombra1.agregar_caracteristicas(
        "Tonos cálidos y fríos",
        "Pigmentación alta",
        "Incluye espejo y brocha"
    )


# Ejecutar programa
if __name__ == "__main__":
    main()
