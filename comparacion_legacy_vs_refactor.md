# Comparación: `sistema_cine_legacy.py` vs. Solución Refactorizada

## Resumen ejecutivo

| | Legacy | Refactorizado |
|---|---|---|
| Archivos | 1 (`sistema_cine_legacy.py`) | 13 módulos organizados en paquetes |
| Paradigma | Procedural (funciones + dicts) | POO (clases, herencia, interfaces) |
| Extensibilidad | Modificar código existente | Agregar archivos nuevos |
| Principios SOLID | ✗ Ninguno aplicado | ✓ Los 5 principios aplicados |
| Code smells | 6 identificados | 0 — todos eliminados |

---

## 1. Estructura de archivos

### Legacy — todo en un solo archivo

```
sistema_cine_legacy.py   ← funciones globales + dicts + if/elif
```

### Refactorizado — un módulo por responsabilidad

```
boleto_base.py                  ← clase abstracta Boleto
boletos/
    boleto_general.py           ← BoletoGeneral
    boleto_vip.py               ← BoletoVIP
    boleto_estudiante.py        ← BoletoEstudiante
pagos/
    pagable.py                  ← interfaz Pagable
    pago_efectivo.py            ← PagoEfectivo
    pago_tarjeta.py             ← PagoTarjeta
servicios/
    servicio.py                 ← interfaz Servicio
    servicio_db.py              ← ServicioDb
    servicio_email.py           ← ServicioEmail
reserva.py                      ← clase Reserva
main.py                         ← punto de entrada
```

---

## 2. Code Smells identificados y eliminados

### Smell 1 — Switch Statements / Cadenas if/elif

**Legacy** — el mismo patrón `if/elif` aparece en tres funciones distintas:

```python
# obtener_precio_por_tipo()
if tipo == "general":
    return PRECIO_GENERAL
elif tipo == "vip":
    return PRECIO_VIP
elif tipo == "estudiante":
    return PRECIO_ESTUDIANTE

# etiqueta_tipo() — mismo patrón repetido
if tipo == "general":
    return "Boleto General"
elif tipo == "vip":
    ...

# procesar_pago() — mismo patrón para métodos de pago
if metodo == "efectivo":
    return f"Pago en efectivo procesado: ${monto:.2f}"
elif metodo == "tarjeta":
    ...
```

**Refactorizado** — cada clase sabe su propio comportamiento, sin condiciones:

```python
class BoletoGeneral(Boleto):
    def calcular_precio(self) -> float:
        return self._precio_base          # sin if/elif

class BoletoVIP(Boleto):
    def calcular_precio(self) -> float:
        return self._precio_base * 2.0    # sin if/elif

class PagoTarjeta(Pagable):
    def procesar_pago(self, monto, cliente=""):
        print(f"  [TARJETA]  Cobrando ${monto:.2f} a {cliente}")  # sin if/elif
```

---

### Smell 2 — Duplicate Code (código duplicado)

**Legacy** — `calcular_precio_boleto()` repite exactamente la lógica de `obtener_precio_por_tipo()`:

```python
def obtener_precio_por_tipo(tipo_boleto):
    if tipo == "general": return PRECIO_GENERAL
    elif tipo == "vip":   return PRECIO_VIP
    ...

def calcular_precio_boleto(boleto):
    return obtener_precio_por_tipo(boleto["tipo"])  # llama a la misma lógica
```

**Refactorizado** — el precio vive en el objeto, se calcula una sola vez:

```python
# Reserva llama polimórficamente, sin duplicar lógica
sum(boleto.calcular_precio() for boleto in self._lista_boletos)
```

---

### Smell 3 — Primitive Obsession / Data Class

**Legacy** — los boletos son diccionarios sin comportamiento:

```python
def crear_boleto(tipo_boleto, pelicula):
    return {
        "tipo": tipo,
        "pelicula": pelicula,
        "precio": obtener_precio_por_tipo(tipo),   # dato sin lógica propia
    }
```

**Refactorizado** — los boletos son objetos con estado y comportamiento encapsulados:

```python
class BoletoVIP(Boleto):
    MULTIPLICADOR_VIP: float = 2.0

    def calcular_precio(self) -> float:
        return self._precio_base * self.MULTIPLICADOR_VIP
```

---

### Smell 4 — God Function (función dios)

**Legacy** — `ejecutar_reserva()` tiene cuatro responsabilidades en una sola función:

```python
def ejecutar_reserva(boletos_config, metodo_pago):
    # 1. Crea boletos
    boletos = [crear_boleto(tipo, pelicula) for tipo, pelicula in boletos_config]
    # 2. Imprime detalle
    for b in boletos: imprimir_linea_boleto(b)
    # 3. Calcula total
    total = calcular_total_reserva(boletos)
    print(f"Total: ${total:.2f}")
    # 4. Procesa pago
    mensaje_pago = procesar_pago(metodo_pago, total)
    print(mensaje_pago)
```

**Refactorizado** — cada responsabilidad vive en su clase:

```python
# Reserva: gestiona boletos y orquesta
reserva.agregar_boleto(BoletoVIP("Dune", 75.00))
reserva.realizar_pago(PagoTarjeta())   # delega el cobro

# main(): solo presenta
for linea in reserva.detalle_boletos():
    print(linea)
```

---

### Smell 5 — Divergent Change (cambio divergente)

**Legacy** — agregar `BoletoPlus` obliga a tocar **4 lugares** en el mismo archivo:

```python
TIPOS_BOLETO_VALIDOS = ("general", "vip", "estudiante", "plus")  # 1

def obtener_precio_por_tipo(tipo):
    ...
    elif tipo == "plus": return PRECIO_PLUS                        # 2

def etiqueta_tipo(tipo):
    ...
    elif tipo == "plus": return "Boleto Plus"                      # 3

def crear_boleto(tipo_boleto, pelicula):
    if tipo not in TIPOS_BOLETO_VALIDOS: ...                       # 4
```

**Refactorizado** — agregar `BoletoPlus` = **un archivo nuevo**, cero cambios en existentes:

```python
# boletos/boleto_plus.py  ← único archivo nuevo
class BoletoPlus(Boleto):
    MULTIPLICADOR_PLUS: float = 1.5

    def calcular_precio(self) -> float:
        return self._precio_base * self.MULTIPLICADOR_PLUS
```

---

### Smell 6 — Exposed Internals (datos expuestos)

**Legacy** — los datos del boleto son accesibles y mutables directamente:

```python
boleto = crear_boleto("vip", "Dune")
boleto["precio"] = 0.00   # cualquiera puede corromper el estado
```

**Refactorizado** — atributos privados con properties de solo lectura:

```python
class Boleto(ABC):
    def __init__(self, pelicula: str, precio_base: float) -> None:
        self._precio_base: float = precio_base   # privado

    @property
    def precio_base(self) -> float:
        return self._precio_base                 # solo lectura
```

---

## 3. Principios SOLID aplicados

### S — Single Responsibility Principle

| Clase / Función | Legacy | Refactorizado |
|---|---|---|
| `ejecutar_reserva()` | Crea, imprime, calcula y cobra | ✗ Eliminada |
| `Reserva` | No existe | Gestiona boletos y orquesta el flujo |
| `PagoTarjeta` | No existe | Solo cobra con tarjeta |
| `ServicioDb` | No existe | Solo registra en DB |
| `main()` | No existe | Solo compone objetos y presenta |

---

### O — Open/Closed Principle

**Legacy** — cerrado a extensión, abierto a modificación:

```python
# Para agregar PagoQR hay que modificar esta función existente
def procesar_pago(metodo_pago, monto):
    if metodo == "efectivo": ...
    elif metodo == "tarjeta": ...
    elif metodo == "qr": ...   # ← modificación de código existente
```

**Refactorizado** — abierto a extensión, cerrado a modificación:

```python
# Para agregar PagoQR solo se crea un archivo nuevo
class PagoQR(Pagable):
    def procesar_pago(self, monto: float, cliente: str = "") -> None:
        print(f"  [QR]  Escaneando código para ${monto:.2f}")
# Reserva, PagoTarjeta, PagoEfectivo → ninguno se toca
```

---

### L — Liskov Substitution Principle

**Legacy** — no hay jerarquía; los boletos son dicts, no se puede sustituir nada.

**Refactorizado** — cualquier subclase de `Boleto` o `Pagable` puede reemplazar a la base sin romper el sistema:

```python
def calcular_total_reserva(self) -> float:
    # Funciona con BoletoGeneral, BoletoVIP, BoletoEstudiante
    # o cualquier subclase futura — sin cambiar esta línea
    return sum(boleto.calcular_precio() for boleto in self._lista_boletos)
```

---

### I — Interface Segregation Principle

**Legacy** — no hay interfaces; `procesar_pago()` es una función global que mezcla todos los métodos.

**Refactorizado** — dos interfaces mínimas y cohesivas:

```python
class Pagable(ABC):
    @abstractmethod
    def procesar_pago(self, monto: float, cliente: str = "") -> None: ...
    # Un solo método — nada innecesario

class Servicio(ABC):
    @abstractmethod
    def ejecutar(self, cliente: str, descripcion: str, monto: float) -> None: ...
    # Un solo método — nada innecesario
```

---

### D — Dependency Inversion Principle

**Legacy** — `ejecutar_reserva()` depende directamente del string `"tarjeta"` o `"efectivo"`:

```python
def ejecutar_reserva(boletos_config, metodo_pago):
    mensaje_pago = procesar_pago(metodo_pago, total)  # depende de un string
```

**Refactorizado** — `Reserva` depende de abstracciones inyectadas desde afuera:

```python
class Reserva:
    def realizar_pago(self, metodo_pago: Pagable) -> None:
        metodo_pago.procesar_pago(total, self._cliente)  # depende de Pagable
        for servicio in self._servicios:
            servicio.ejecutar(...)                        # depende de Servicio
```

---

## 4. Output comparado

### Legacy

```
Boleto General - Dune - $5.00
Boleto VIP - Dune - $10.00
Boleto Estudiante - Dune - $4.00
Total: $19.00
Pago con tarjeta procesado: $19.00
```

### Refactorizado

```
VIP x2 -- Ana Garcia
  [TARJETA]  Cobrando $300.00 a Ana Garcia
  [DB]       Ana Garcia | VIP x2 = $300.00
  [EMAIL]    Confirmacion enviada a Ana Garcia por $300.00
  Total: $300.00

Estudiante x3 -- Luis Perez
  [EFECTIVO] Recibiendo $60.00 de Luis Perez
  [DB]       Luis Perez | Estudiante x3 = $60.00
  [EMAIL]    Confirmacion enviada a Luis Perez por $60.00
  Total: $60.00
```

---

## 5. Pregunta de validación

> **"Si mañana llega un `PlatinumTicket`, ¿cuántos archivos tienes que modificar?"**

| | Legacy | Refactorizado |
|---|---|---|
| Archivos a modificar | `sistema_cine_legacy.py` en 4 lugares | **0** archivos modificados |
| Archivos a crear | 0 | **1** (`boletos/boleto_platinum.py`) |
| Riesgo de romper algo | Alto — cada `if/elif` existente puede introducir un bug | Ninguno |

```python
# boletos/boleto_platinum.py — único cambio necesario
class BoletoPlatinum(Boleto):
    MULTIPLICADOR: float = 3.0

    def calcular_precio(self) -> float:
        return self._precio_base * self.MULTIPLICADOR
```
