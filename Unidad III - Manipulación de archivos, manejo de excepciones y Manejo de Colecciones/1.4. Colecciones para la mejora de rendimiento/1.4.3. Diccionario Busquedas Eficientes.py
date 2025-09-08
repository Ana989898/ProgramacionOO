
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass(frozen=True)
class Libro:
    autor_titulo: Tuple[str, str]
    isbn: str
    categoria: str

    @property
    def autor(self) -> str:
        return self.autor_titulo[0]

    @property
    def titulo(self) -> str:
        return self.autor_titulo[1]

class Catalogo:
    def __init__(self) -> None:
        self.libros: Dict[str, Libro] = {}  # DICCIONARIO por ISBN

    def agregar(self, libro: Libro) -> None:
        if libro.isbn in self.libros:
            raise ValueError("ISBN duplicado")
        self.libros[libro.isbn] = libro

    def buscar(self, titulo: Optional[str] = None,
               autor: Optional[str] = None,
               categoria: Optional[str] = None) -> List[Libro]:
        def match(campo: str, patron: Optional[str]) -> bool:
            return True if patron is None else patron.lower() in campo.lower()
        res: List[Libro] = []
        for l in self.libros.values():
            if (match(l.titulo, titulo) and match(l.autor, autor) and match(l.categoria, categoria)):
                res.append(l)
        return res

if __name__ == "__main__":
    c = Catalogo()
    c.agregar(Libro(("Ursula K. Le Guin", "The Left Hand of Darkness"),
                    "9780441478125", "Ciencia ficción"))
    c.agregar(Libro(("Yuval Noah Harari", "Sapiens"),
                    "9780099590088", "Historia"))
    print([f"{l.titulo} — {l.autor}" for l in c.buscar(autor="Yuval")])
