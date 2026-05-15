"""
boletos/boleto_general.py
─────────────────────────
Boleto de precio estándar.

POO  : Herencia, Polimorfismo
SOLID: LSP — sustituye a Boleto sin alterar el comportamiento esperado
       SRP — única responsabilidad: calcular precio general
"""

from __future__ import annotations
from boleto_base import Boleto


class BoletoGeneral(Boleto):
    """
    Precio estándar: retorna el precio base sin modificación.
    Ejemplo: precio_base=$5.00 → calcular_precio()=$5.00
    """

    def calcular_precio(self) -> float:
        return self._precio_base        # $5.00
