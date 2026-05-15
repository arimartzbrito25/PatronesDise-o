"""
pagos/pago_efectivo.py
──────────────────────
Implementación concreta: pago en efectivo.

POO  : Polimorfismo (implementa Pagable)
SOLID: SRP — única responsabilidad: confirmar cobro en efectivo
       LSP — sustituye a Pagable sin romper el contrato
       OCP — agregar PagoCripto no modifica este archivo
"""

from __future__ import annotations
from pagos.pagable import Pagable


class PagoEfectivo(Pagable):
    """Confirma la recepción de dinero en efectivo."""

    def procesar_pago(self, monto: float, cliente: str = "") -> None:
        origen = f" de {cliente}" if cliente else ""
        print(f"  [EFECTIVO] Recibiendo ${monto:.2f}{origen}")
