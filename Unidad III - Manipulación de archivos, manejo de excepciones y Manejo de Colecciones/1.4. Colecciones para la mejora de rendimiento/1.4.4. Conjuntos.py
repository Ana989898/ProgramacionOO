class RegistroUsuarios:
    def __init__(self) -> None:
        self.ids = set()  # CONJUNTO

    def registrar(self, user_id: str) -> None:
        if user_id in self.ids:
            raise ValueError("ID ya utilizado")
        self.ids.add(user_id)

    def dar_baja(self, user_id: str) -> None:
        try:
            self.ids.remove(user_id)
        except KeyError:
            print("ID no existe")

if __name__ == "__main__":
    r = RegistroUsuarios()
    r.registrar("U001")
    r.registrar("U002")
    print("Usuarios:", r.ids)
    try:
        r.registrar("U001")
    except ValueError as e:
        print("Error esperado:", e)
    r.dar_baja("U002")
    print("Usuarios tras baja:", r.ids)
