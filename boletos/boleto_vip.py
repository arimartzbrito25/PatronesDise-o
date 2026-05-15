"""
boletos/boleto_vip.py
─────────────────────
Boleto de precio premium (VIP).

POO  : Herencia, Polimorfismo
SOLID: LSP — sustituye a Boleto sin alterar el comportamiento esperado
       SRP — única responsabilidad: calcular precio VIP
       OCP — cambiar el multiplicador no toca ninguna otra clase
Smell: Magic number eliminado → constante MULTIPLICADOR_VIP
"""

from __future__ import annotations
from boleto_base import Boleto


class BoletoVIP(Boleto):
    """
    Precio premium: duplica el precio base.
    Ejemplo: precio_base=$5.00 → calcular_precio()=$10.00
    """

    MULTIPLICADOR_VIP: float = 2.0      # OCP: ajustar aquí no toca nada más

    def calcular_precio(self) -> float:
        return self._precio_base * self.MULTIPLICADOR_VIP   # $10.00
