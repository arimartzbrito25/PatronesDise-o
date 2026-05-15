"""
pagos/pago_tarjeta.py
─────────────────────
Implementación concreta: pago con tarjeta bancaria.

POO  : Polimorfismo (implementa Pagable)
SOLID: SRP — única responsabilidad: simular cobro bancario
       LSP — sustituye a Pagable sin romper el contrato
       OCP — agregar PagoCripto no modifica este archivo
"""

from __future__ import annotations
from pagos.pagable import Pagable


class PagoTarjeta(Pagable):
    """Simula una conexión bancaria y confirma el cobro procesado."""

    def procesar_pago(self, monto: float) -> None:
        print(f"[TARJETA]  Pago con tarjeta procesado: ${monto:.2f}")
