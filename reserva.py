"""
reserva.py
──────────
Clase Reserva: coordina boletos y delega el cobro al método de pago.

POO  : Encapsulamiento (lista privada), Composición
SOLID: SRP — solo gestiona la colección de boletos y delega el pago
       DIP — depende de Boleto y Pagable (abstracciones), nunca de concretos
Smells eliminados:
  - Exposed Internals → _lista_boletos privada
  - Missing Guard     → validación de lista vacía
  - SRP violation     → detalle_boletos() retorna strings, no imprime
"""

from __future__ import annotations
from boleto_base import Boleto
from pagos.pagable import Pagable


class Reserva:
    """
    Gestiona una colección de boletos y delega el cobro
    al método de pago inyectado desde afuera (Dependency Injection).
    """

    def __init__(self) -> None:
        self._lista_boletos: list[Boleto] = []      # encapsulamiento (POO)

    # ── Mutación controlada ──────────────────────────────────────
    def agregar_boleto(self, boleto: Boleto) -> None:
        """Añade un boleto validado a la reserva."""
        if not isinstance(boleto, Boleto):
            raise TypeError("Solo se pueden agregar instancias de Boleto.")
        self._lista_boletos.append(boleto)

    # ── Consultas ────────────────────────────────────────────────
    def calcular_total_reserva(self) -> float:
        """
        Suma los precios usando polimorfismo sobre calcular_precio().
        Guard: retorna 0.0 si la lista está vacía.
        (Smell eliminado: Missing Guard)
        """
        if not self._lista_boletos:
            return 0.0
        return sum(boleto.calcular_precio() for boleto in self._lista_boletos)

    def detalle_boletos(self) -> list[str]:
        """
        Retorna el detalle de cada boleto como lista de strings.
        SRP: produce datos; quien llama decide cómo mostrarlos.
        (Smell eliminado: SRP violation — no imprime directamente)
        """
        return [str(boleto) for boleto in self._lista_boletos]

    # ── Pago ─────────────────────────────────────────────────────
    def realizar_pago(self, metodo_pago: Pagable) -> None:
        """
        Delega el cobro al objeto Pagable recibido.
        DIP: Reserva no sabe ni le importa si es efectivo o tarjeta.
        """
        total = self.calcular_total_reserva()
        metodo_pago.procesar_pago(total)
