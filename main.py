"""
main.py
───────
Punto de entrada del sistema de reservas de cine.

Responsabilidad: orquestar objetos e imprimir resultados.
No contiene lógica de negocio — solo composición y presentación.
(SRP: la presentación vive aquí, no dentro de Reserva)
"""

import sys
import os

# Asegura que la raíz del proyecto esté en el path para que
# los imports absolutos funcionen sin instalar el paquete.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from boletos import BoletoGeneral, BoletoVIP, BoletoEstudiante
from pagos import PagoEfectivo, PagoTarjeta
from reserva import Reserva


def main() -> None:
    # ── Construir reserva ────────────────────────────────────────
    reserva = Reserva()
    reserva.agregar_boleto(BoletoGeneral("Dune", 5.00))
    reserva.agregar_boleto(BoletoVIP("Dune", 5.00))
    reserva.agregar_boleto(BoletoEstudiante("Dune", 5.00))

    # ── Presentación (responsabilidad del cliente, no de Reserva) ─
    for linea in reserva.detalle_boletos():
        print(linea)

    print(f"Total: ${reserva.calcular_total_reserva():.2f}")

    # ── Pago con tarjeta ─────────────────────────────────────────
    reserva.realizar_pago(PagoTarjeta())

    print()

    # ── Demostración de intercambiabilidad (DIP / polimorfismo) ───
    print("--- Mismo total, método de pago diferente ---")
    reserva.realizar_pago(PagoEfectivo())


if __name__ == "__main__":
    main()
