"""
pagos/pagable.py
────────────────
Interfaz (contrato) que toda forma de pago debe cumplir.

POO  : Abstracción
SOLID: ISP — interfaz mínima y cohesiva, un solo método
       DIP — Reserva depende de esta abstracción, no de clases concretas
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Pagable(ABC):
    """
    Interfaz de pago.
    Obliga a cada implementación a definir procesar_pago(monto, cliente).
    cliente es opcional para mantener compatibilidad (LSP).
    """

    @abstractmethod
    def procesar_pago(self, monto: float, cliente: str = "") -> None:
        """Procesa el cobro del monto indicado."""
