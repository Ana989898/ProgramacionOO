class CuentaBancaria:
    def __init__(self, saldo):
        self.__saldo = saldo  # atributo privado

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto

    def mostrar_saldo(self):
        print(f"Saldo actual: ${self.__saldo}")

cuenta = CuentaBancaria(100)
cuenta.depositar(50)
cuenta.mostrar_saldo()     # Saldo actual: $150
# print(cuenta.__saldo)    # Error: el atributo está encapsulado
