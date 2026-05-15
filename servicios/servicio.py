"""
servicios/servicio.py
─────────────────────
Interfaz para servicios post-pago (DB, Email, etc.).

POO  : Abstracción
SOLID: ISP — contrato mínimo de un solo método
       OCP — agregar ServicioSMS no toca ninguna clase existente
       DIP — Reserva depende de esta abstracción, no de concretos
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Servicio(ABC):
    """
    Contrato que todo servicio post-pago debe cumplir.
    Permite inyectar cualquier combinación de servicios en Reserva.
    """

    @abstractmethod
    def ejecutar(self, cliente: str, descripcion: str, monto: float) -> None:
        """Ejecuta la acción del servicio con los datos de la transacción."""
