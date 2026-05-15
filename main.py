"""
main.py
───────
Punto de entrada del sistema de reservas de cine.

Responsabilidad: componer objetos y mostrar resultados.
No contiene lógica de negocio — solo composición y presentación.
(SRP: la presentación vive aquí, no dentro de Reserva)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from boletos import BoletoGeneral, BoletoVIP, BoletoEstudiante
from pagos import PagoEfectivo, PagoTarjeta
from servicios import ServicioDb, ServicioEmail
from reserva import Reserva


def main() -> None:

    # ── Reserva 1: Ana Garcia — 2 boletos VIP, pago con tarjeta ──
    reserva_ana = Reserva(cliente="Ana Garcia")
    reserva_ana.agregar_boleto(BoletoVIP("Dune", 75.00))
    reserva_ana.agregar_boleto(BoletoVIP("Dune", 75.00))
    reserva_ana.agregar_servicio(ServicioDb())
    reserva_ana.agregar_servicio(ServicioEmail())

    descripcion_ana = "VIP x2 -- Ana Garcia"
    print(descripcion_ana)
    reserva_ana.realizar_pago(PagoTarjeta())

    print()

    # ── Reserva 2: Luis Perez — 3 boletos Estudiante, pago efectivo
    reserva_luis = Reserva(cliente="Luis Perez")
    reserva_luis.agregar_boleto(BoletoEstudiante("Dune", 25.00))
    reserva_luis.agregar_boleto(BoletoEstudiante("Dune", 25.00))
    reserva_luis.agregar_boleto(BoletoEstudiante("Dune", 25.00))
    reserva_luis.agregar_servicio(ServicioDb())
    reserva_luis.agregar_servicio(ServicioEmail())

    descripcion_luis = "Estudiante x3 -- Luis Perez"
    print(descripcion_luis)
    reserva_luis.realizar_pago(PagoEfectivo())


if __name__ == "__main__":
    main()
