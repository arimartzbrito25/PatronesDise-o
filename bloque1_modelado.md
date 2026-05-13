# Bloque 1 — Modelado en papel
## Sistema de Reservas de Cine

> Antes de escribir una sola línea de código, respondemos las 4 preguntas de diseño.

---

## 1. ¿Qué clases necesitamos? ¿Cuáles son abstractas?

| Clase | Tipo | Razón |
|---|---|---|
| `Boleto` | **Abstracta** | Define el contrato común; nunca se instancia un "boleto genérico". |
| `BoletoGeneral` | Concreta | Hereda de `Boleto`. Precio base $5.00. |
| `BoletoVIP` | Concreta | Hereda de `Boleto`. Precio = doble del general. |
| `BoletoEstudiante` | Concreta | Hereda de `Boleto`. 20% de descuento sobre general. |
| `Pagable` | **Interfaz (ABC)** | Contrato "algo que procesa un pago". Sin estado. |
| `PagoEfectivo` | Concreta | Implementa `Pagable`. |
| `PagoTarjeta` | Concreta | Implementa `Pagable`. |
| `Reserva` *(opcional, recomendada)* | Concreta | Agrupa boletos, calcula total, dispara pago. |

---

## 2. Atributos y métodos

### `Boleto` (abstracta)
- **Atributos:** `pelicula: str`
- **Métodos:**
  - `calcular_precio() -> float`  *(abstracto — cada hijo decide)*
  - `__str__()`  *(concreto, reutilizable: `"Tipo - Pelicula - $X.XX"`)*

### `BoletoGeneral(Boleto)`
- `calcular_precio()` → `5.00`

### `BoletoVIP(Boleto)`
- `calcular_precio()` → `BoletoGeneral().calcular_precio() * 2`  → `10.00`

### `BoletoEstudiante(Boleto)`
- `calcular_precio()` → `BoletoGeneral().calcular_precio() * 0.80` → `4.00`

### `Pagable` (interfaz / ABC)
- `procesar_pago(monto: float) -> str`  *(abstracto)*

### `PagoEfectivo(Pagable)`
- `procesar_pago(monto)` → `"Pago en efectivo procesado: $XX.XX"`

### `PagoTarjeta(Pagable)`
- `procesar_pago(monto)` → `"Pago con tarjeta procesado: $XX.XX"`

### `Reserva` (opcional)
- **Atributos:** `boletos: list[Boleto]`, `metodo_pago: Pagable`
- **Métodos:** `agregar_boleto(b)`, `calcular_total()`, `procesar()`

---

## 3. ¿Dónde aplica herencia? ¿Dónde polimorfismo?

### Herencia (relación "es-un")
- `BoletoGeneral`, `BoletoVIP`, `BoletoEstudiante` **son-un** `Boleto`.
- `BoletoVIP` y `BoletoEstudiante` calculan su precio **en términos de** `BoletoGeneral` → evita hardcodear "doble" o "20%" como números mágicos.

### Polimorfismo (mismo mensaje, distinto comportamiento)
- `boleto.calcular_precio()` sobre una lista mixta → sin `if isinstance(...)`. Cada subclase responde distinto.
- `metodo_pago.procesar_pago(total)` → la `Reserva` no sabe ni le importa si es efectivo o tarjeta. Polimorfismo por **interfaz**.

---

## 4. ¿Qué contratos (interfaces) conviene definir?

- **`Pagable`** → el contrato clave. Permite que `Reserva` dependa de una abstracción, no de implementaciones concretas. Mañana agregamos `PagoTransferencia`, `PagoQR`, `PagoCripto`… y `Reserva` **no se toca**. *(OCP + DIP)*
- **`Boleto`** → ya cumple rol de contrato vía clase abstracta (impone `calcular_precio()`). No hace falta una interfaz separada porque hay estado compartido (`pelicula`).

> **Regla práctica:**
> - Hay **estado/atributos comunes** + relación "es-un" → **clase abstracta** (`Boleto`).
> - Solo **comportamiento común**, sin estado → **interfaz** (`Pagable`).

---

## Diagrama conceptual (UML simplificado)

```
        <<abstract>>                       <<interface>>
          Boleto                              Pagable
        ----------                          ------------
        pelicula                            + procesar_pago(monto)
        + calcular_precio()*
        + __str__()
            ▲                                    ▲
   ┌────────┼────────┐                  ┌────────┴────────┐
   │        │        │                  │                 │
BoletoGen  BoletoVIP  BoletoEst    PagoEfectivo      PagoTarjeta


           Reserva
        ------------
        boletos: List<Boleto>
        metodo_pago: Pagable
        + agregar_boleto(b)
        + calcular_total()
        + procesar()
```

---

## Respuesta anticipada — Discusión final pregunta 3

> *"Si el cine agrega `BoletoAdultoMayor` con 30% de descuento… ¿cuántas clases hay que modificar?"*

**Cero clases existentes.** Solo **se agrega** `BoletoAdultoMayor(Boleto)` con su `calcular_precio()`. Ni `Reserva`, ni `Pagable`, ni los demás boletos se tocan.

Esa es exactamente la ganancia frente a la alternativa procedural:

```python
# MAL — esto se rompe con cada nuevo tipo
if tipo == "general": precio = 5
elif tipo == "vip": precio = 10
elif tipo == "estudiante": precio = 4
# ...y ahora hay que tocar este if en N lugares
```
