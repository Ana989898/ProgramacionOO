# Clase que representa un vehículo
class Carro:
    def __init__(self, modelo, anio):
        self.modelo = modelo        # Modelo del carro (str)
        self.anio = anio            # Año del carro (int)
        self.conductor = None       # Al principio, sin conductor asignado

    def asignar_conductor(self, persona):
        # Verifica que el objeto recibido sea de tipo Persona
        if isinstance(persona, Persona):
            self.conductor = persona

    def __str__(self):
        # Muestra información del carro y el conductor, si existe
        nombre_conductor = self.conductor.nombre if self.conductor else "nadie"
        return f'Carro {self.modelo} del año {self.anio}, conducido por {nombre_conductor}.'


# Clase que representa una persona con licencia de conducir
class Persona:
    def __init__(self, nombre, licencia):
        self.nombre = nombre        # Nombre del conductor (str)
        self.licencia = licencia    # Número de licencia (int)

    def __str__(self):
        # Devuelve una descripción de la persona
        return f'Persona {self.nombre} con licencia número {self.licencia}.'


# ----------- Ejecución del programa -----------

# Crear dos carros
carro1 = Carro('Corolla', 1998)
carro2 = Carro('Blazer', 1997)

# Crear una persona con licencia
persona = Persona('Laura', 3)

# Asignar conductor al primer carro
carro1.asignar_conductor(persona)

# Mostrar información por consola
print(carro1)   # Muestra que Laura conduce el Corolla
print(carro2)   # Muestra que la Blazer no tiene conductor
print(persona)  # Muestra la información de Laura
