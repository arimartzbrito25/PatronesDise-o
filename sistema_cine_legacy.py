
PRECIO_GENERAL = 5.00
PRECIO_VIP = 10.00
PRECIO_ESTUDIANTE = 4.00

TIPOS_BOLETO_VALIDOS = ("general", "vip", "estudiante")
METODOS_PAGO_VALIDOS = ("efectivo", "tarjeta")


def obtener_precio_por_tipo(tipo_boleto):
    """Calcula precio según tipo. Cada nuevo tipo = otro elif aquí."""
    tipo = tipo_boleto.lower().strip()

    if tipo == "general":
        return PRECIO_GENERAL
    elif tipo == "vip":
        return PRECIO_VIP
    elif tipo == "estudiante":
        return PRECIO_ESTUDIANTE
    else:
        raise ValueError(f"Tipo de boleto no soportado: {tipo_boleto}")


def etiqueta_tipo(tipo_boleto):
    """Nombre para imprimir. Duplicamos el conocimiento del tipo otra vez."""
    tipo = tipo_boleto.lower().strip()

    if tipo == "general":
        return "Boleto General"
    elif tipo == "vip":
        return "Boleto VIP"
    elif tipo == "estudiante":
        return "Boleto Estudiante"
    else:
        return "Boleto Desconocido"


def crear_boleto(tipo_boleto, pelicula):
    """
    Los boletos son diccionarios, no objetos.
    El precio no vive en el boleto: se recalcula con if/elif cada vez.
    """
    tipo = tipo_boleto.lower().strip()
    if tipo not in TIPOS_BOLETO_VALIDOS:
        raise ValueError(f"Tipo de boleto no soportado: {tipo_boleto}")

    return {
        "tipo": tipo,
        "pelicula": pelicula,
        "precio": obtener_precio_por_tipo(tipo),
    }


def calcular_precio_boleto(boleto):
    """Mismo if/elif que obtener_precio_por_tipo — duplicación."""
    return obtener_precio_por_tipo(boleto["tipo"])


def imprimir_linea_boleto(boleto):
    etiqueta = etiqueta_tipo(boleto["tipo"])
    precio = calcular_precio_boleto(boleto)
    print(f"{etiqueta} - {boleto['pelicula']} - ${precio:.2f}")


def calcular_total_reserva(lista_boletos):
    total = 0.0
    for b in lista_boletos:
        total += calcular_precio_boleto(b)
    return total


def procesar_pago(metodo_pago, monto):
    """
    Pagos con if/elif. No hay interfaz Pagable.
    Nuevo método (transferencia, QR) = modificar esta función.
    """
    metodo = metodo_pago.lower().strip()

    if metodo == "efectivo":
        return f"Pago en efectivo procesado: ${monto:.2f}"
    elif metodo == "tarjeta":
        return f"Pago con tarjeta procesado: ${monto:.2f}"
    else:
        raise ValueError(f"Método de pago no soportado: {metodo_pago}")


def ejecutar_reserva(boletos_config, metodo_pago):
    """
    Orquesta todo en funciones sueltas (sin clase Reserva).
    boletos_config: lista de tuplas (tipo, pelicula)
      Ej: [("general", "Dune"), ("vip", "Dune"), ("estudiante", "Dune")]
    """
    boletos = []
    for tipo, pelicula in boletos_config:
        boletos.append(crear_boleto(tipo, pelicula))

    for b in boletos:
        imprimir_linea_boleto(b)

    total = calcular_total_reserva(boletos)
    print(f"Total: ${total:.2f}")

    mensaje_pago = procesar_pago(metodo_pago, total)
    print(mensaje_pago)

    return total


def main():
    ejecutar_reserva(
        [
            ("general", "Dune"),
            ("vip", "Dune"),
            ("estudiante", "Dune"),
        ],
        metodo_pago="tarjeta",
    )


if __name__ == "__main__":
    main()
