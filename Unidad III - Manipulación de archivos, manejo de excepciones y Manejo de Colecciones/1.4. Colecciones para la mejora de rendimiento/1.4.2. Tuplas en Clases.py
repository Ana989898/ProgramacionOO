from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Libro:
    autor_titulo: Tuple[str, str]   # TUPLA (autor, título)
    isbn: str
    categoria: str

    @property
    def autor(self) -> str:
        return self.autor_titulo[0]

    @property
    def titulo(self) -> str:
        return self.autor_titulo[1]

if __name__ == "__main__":
    l = Libro(("Gabriel García Márquez", "Cien años de soledad"),
              "9780307474728", "Literatura")
    print("Autor:", l.autor)
    print("Título:", l.titulo)
    print("Tupla:", l.autor_titulo)
