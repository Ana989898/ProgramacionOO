from dataclasses import dataclass, field
from typing import List

@dataclass
class Usuario:
    nombre: str
    user_id: str
    libros_prestados: List[str] = field(default_factory=list)  # LISTA

    def prestar(self, isbn: str) -> None:
        self.libros_prestados.append(isbn)

    def devolver(self, isbn: str) -> None:
        try:
            self.libros_prestados.remove(isbn)
        except ValueError:
            print("El usuario no tiene ese ISBN.")

if __name__ == "__main__":
    u = Usuario("Ana Villón", "U001")
    u.prestar("9780099590088")   # Sapiens
    u.prestar("9780307474728")   # Cien años de soledad
    print("Prestados:", u.libros_prestados)
    u.devolver("9780307474728")
    print("Tras devolución:", u.libros_prestados)
