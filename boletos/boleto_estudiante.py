"""
boletos/boleto_estudiante.py
────────────────────────────
Boleto con descuento para estudiantes.

POO  : Herencia, Polimorfismo
SOLID: LSP — sustituye a Boleto sin alterar el comportamiento esperado
       SRP — única responsabilidad: calcular precio con descuento
       OCP — cambiar el descuento no toca ninguna otra clase
Smell: Magic number eliminado → constante DESCUENTO
"""

from __future__ import annotations
from boleto_base import Boleto


class BoletoEstudiante(Boleto):
    """
    Precio con descuento: aplica 20 % de rebaja sobre el precio base.
    Ejemplo: precio_base=$5.00 → calcular_precio()=$4.00
    """

    DESCUENTO: float = 0.20             # OCP: ajustar aquí no toca nada más

    def calcular_precio(self) -> float:
        return self._precio_base * (1 - self.DESCUENTO)     # $4.00
