"""
boleto.py
─────────
Clase abstracta base para toda la jerarquía de boletos.

POO  : Abstracción, Encapsulamiento
SOLID: OCP — nuevos tipos de boleto no modifican este archivo
       LSP — cualquier subclase puede sustituir a Boleto
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Boleto(ABC):
    """
    Clase abstracta base para todo tipo de boleto.

    Atributos encapsulados como propiedades de solo lectura
    para evitar mutación accidental desde fuera.
    (Smell eliminado: Exposed Internals)
    """

    def __init__(self, pelicula: str, precio_base: float) -> None:
        # Atributos privados → encapsulamiento (POO)
        self._pelicula: str = pelicula
        self._precio_base: float = precio_base

    # ── Properties de solo lectura ──────────────────────────────
    @property
    def pelicula(self) -> str:
        return self._pelicula

    @property
    def precio_base(self) -> float:
        return self._precio_base

    # ── Contrato que toda subclase DEBE cumplir (OCP + LSP) ─────
    @abstractmethod
    def calcular_precio(self) -> float:
        """Cada subclase define su propia lógica de precio."""

    # ── Representación textual: solo presentación, sin lógica ───
    # (Smell eliminado: Inappropriate Intimacy / SRP)
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__:<18} "
            f"- {self._pelicula} "
            f"- ${self.calcular_precio():.2f}"
        )
