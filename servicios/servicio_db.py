"""
servicios/servicio_db.py
────────────────────────
Servicio concreto: registro en base de datos.

POO  : Polimorfismo (implementa Servicio)
SOLID: SRP — única responsabilidad: simular escritura en DB
       LSP — sustituye a Servicio sin romper el contrato
"""

from __future__ import annotations
from servicios.servicio import Servicio


class ServicioDb(Servicio):
    """Simula el registro de la transacción en base de datos."""

    def ejecutar(self, cliente: str, descripcion: str, monto: float) -> None:
        print(f"  [DB]       {cliente} | {descripcion} = ${monto:.2f}")
