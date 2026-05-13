from abc import ABC, abstractmethod

class Boleto(ABC):
    def __init__(self, pelicula, precio_base):
        self.pelicula = pelicula
        self.precio_base = precio_base

    @abstractmethod
    def calcular_precio(self):
        pass


class BoletoGeneral(Boleto):
    def calcular_precio(self):
        return self.precio_base


class BoletoVIP(Boleto):
    def calcular_precio(self):
        return self.precio_base * 2


class BoletoEstudiante(Boleto):
    def calcular_precio(self):
        return self.precio_base * 0.5
