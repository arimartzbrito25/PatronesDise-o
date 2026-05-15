"""
reserva.py
──────────
Clase Reserva: coordina boletos, pago y servicios post-pago.

POO  : Encapsulamiento (lista privada), Composición
SOLID: SRP — gestiona boletos y orquesta el flujo; no implementa pagos ni servicios
       OCP — nuevos servicios se inyectan sin modificar esta clase
       DIP — depende de Boleto, Pagable y Servicio (abstracciones)
Smells eliminados:
  - Exposed Internals → _lista_boletos privada
  - Missing Guard     → validación de lista vacía
  - SRP violation     → detalle_boletos() retorna strings, no imprime
"""

from __future__ import annotations
from boleto_base import Boleto
from pagos.pagable import Pagable
from servicios.servicio import Servicio


class Reserva:
    """
    Gestiona una colección de boletos para un cliente y delega:
      - el cobro al método de pago inyectado (Pagable)
      - las acciones post-pago a los servicios inyectados (Servicio)

    Todos los colaboradores se inyectan desde afuera (DIP).
    """

    def __init__(self, cliente: str) -> None:
        self._cliente: str = cliente
        self._lista_boletos: list[Boleto] = []          # encapsulamiento (POO)
        self._servicios: list[Servicio] = []            # servicios post-pago

    # ── Configuración ────────────────────────────────────────────
    def agregar_boleto(self, boleto: Boleto) -> None:
        """Añade un boleto validado a la reserva."""
        if not isinstance(boleto, Boleto):
            raise TypeError("Solo se pueden agregar instancias de Boleto.")
        self._lista_boletos.append(boleto)

    def agregar_servicio(self, servicio: Servicio) -> None:
        """Registra un servicio post-pago (DB, Email, SMS…)."""
        if not isinstance(servicio, Servicio):
            raise TypeError("Solo se pueden agregar instancias de Servicio.")
        self._servicios.append(servicio)

    # ── Consultas ────────────────────────────────────────────────
    @property
    def cliente(self) -> str:
        return self._cliente

    def calcular_total_reserva(self) -> float:
        """
        Suma los precios usando polimorfismo sobre calcular_precio().
        Guard: retorna 0.0 si la lista está vacía.
        """
        if not self._lista_boletos:
            return 0.0
        return sum(boleto.calcular_precio() for boleto in self._lista_boletos)

    def detalle_boletos(self) -> list[str]:
        """
        Retorna el detalle de cada boleto como lista de strings.
        SRP: produce datos; quien llama decide cómo mostrarlos.
        """
        return [str(boleto) for boleto in self._lista_boletos]

    def _descripcion_reserva(self) -> str:
        """Genera una descripción compacta del contenido de la reserva."""
        from collections import Counter
        conteo = Counter(b.__class__.__name__.replace("Boleto", "") for b in self._lista_boletos)
        partes = [f"{tipo} x{cant}" for tipo, cant in conteo.items()]
        return " + ".join(partes)

    # ── Flujo principal ──────────────────────────────────────────
    def realizar_pago(self, metodo_pago: Pagable) -> None:
        """
        Orquesta el flujo completo:
          1. Cobra usando el método de pago inyectado.
          2. Ejecuta cada servicio post-pago registrado.
        DIP: Reserva no sabe si el pago es tarjeta o efectivo,
             ni si los servicios son DB, Email o SMS.
        """
        total = self.calcular_total_reserva()
        descripcion = self._descripcion_reserva()

        # 1. Pago
        metodo_pago.procesar_pago(total, self._cliente)

        # 2. Servicios post-pago (polimorfismo sobre Servicio)
        for servicio in self._servicios:
            servicio.ejecutar(self._cliente, descripcion, total)

        print(f"  Total: ${total:.2f}")
