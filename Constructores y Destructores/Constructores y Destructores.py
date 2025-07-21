class Maquillaje:
    def __init__(self, nombre, marca, tipo):
        """
        Constructor de la clase Maquillaje.
        Inicializa los atributos del objeto: nombre del producto, marca y tipo.
        """
        self.nombre = nombre    # Ej: "Base líquida"
        self.marca = marca      # Ej: "Maybelline"
        self.tipo = tipo        # Ej: "Rostro", "Ojos", "Labios", etc.
        print(f"[+] Producto agregado: '{self.nombre}' - Marca: {self.marca} ({self.tipo})")

    def mostrar_detalles(self):
        """
        Muestra la información detallada del producto de maquillaje.
        """
        print(f"📦 Producto: {self.nombre}")
        print(f"🏷️  Marca: {self.marca}")
        print(f"🧴 Tipo: {self.tipo}")

    def __del__(self):
        """
        Destructor de la clase Maquillaje.
        Este metodo se ejecuta automáticamente cuando el objeto es eliminado o
        sale del alcance. Simula el retiro del producto del inventario.
        """
        print(f"[x] Producto eliminado: '{self.nombre}' de la marca {self.marca}")


# -------------------- EJEMPLO DE USO --------------------

print("== INICIO DEL INVENTARIO ==")

# Crear instancias de productos de maquillaje
producto1 = Maquillaje("Base líquida Fit Me", "Maybelline", "Rostro")
producto2 = Maquillaje("Máscara de pestañas Lash Sensational", "Maybelline", "Ojos")

# Mostrar detalles de los productos
producto1.mostrar_detalles()
print()
producto2.mostrar_detalles()

# Eliminar un producto del inventario (se activa el destructor)
del producto1

print("== INVENTARIO ACTUALIZADO ==")

# El destructor de producto2 se activará automáticamente al final del programa si no se elimina manualmente