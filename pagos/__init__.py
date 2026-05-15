"""
pagos/__init__.py
─────────────────
Re-exporta la interfaz y las implementaciones concretas de pago
para que los importadores puedan escribir:
    from pagos import Pagable, PagoEfectivo, PagoTarjeta
"""

from pagos.pagable import Pagable
from pagos.pago_efectivo import PagoEfectivo
from pagos.pago_tarjeta import PagoTarjeta

__all__ = ["Pagable", "PagoEfectivo", "PagoTarjeta"]
