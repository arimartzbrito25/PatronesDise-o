"""
servicios/servicio_email.py
───────────────────────────
Servicio concreto: envío de confirmación por email.

POO  : Polimorfismo (implementa Servicio)
SOLID: SRP — única responsabilidad: simular envío de email
       LSP — sustituye a Servicio sin romper el contrato
"""

from __future__ import annotations
from servicios.servicio import Servicio


class ServicioEmail(Servicio):
    """Simula el envío de un email de confirmación al cliente."""

    def ejecutar(self, cliente: str, descripcion: str, monto: float) -> None:
        print(f"  [EMAIL]    Confirmacion enviada a {cliente} por ${monto:.2f}")
