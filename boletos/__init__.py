"""
boletos/__init__.py
───────────────────
Re-exporta las tres subclases concretas para que los importadores
puedan escribir:  from boletos import BoletoGeneral, BoletoVIP, BoletoEstudiante
"""

from boletos.boleto_general import BoletoGeneral
from boletos.boleto_vip import BoletoVIP
from boletos.boleto_estudiante import BoletoEstudiante

__all__ = ["BoletoGeneral", "BoletoVIP", "BoletoEstudiante"]
