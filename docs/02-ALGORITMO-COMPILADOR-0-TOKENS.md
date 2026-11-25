# 02 · Algoritmo del Compilador Geométrico `0-Tokens` (Glass v2)

Este documento detalla cómo `compiler/glass_compiler.py` convierte automáticamente cualquier icono vectorial estándar de `@phosphor-icons/core` (`MIT`, `viewBox="0 0 256 256"`) en un icono **Glass v2 `24×24` de 4 capas** de manera `100%` determinista, en local y consumiendo **`0 tokens` de modelos de IA**.

---

## 1. Equivalencia de Escala entre Phosphor (`256×256`) y `24×24`

Los iconos de Phosphor están diseñados sobre una cuadrícula de `256×256` unidades con un grosor de trazo uniforme de `16 u` (medio trazo = `8 u`). Al escalar al lienzo estándar de `24×24`:

$$\text{Factor de escala} = \frac{24}{256} = 0.09375$$

$$\text{Grosor de trazo} = 16 \times 0.09375 = 1.50\text{ u}, \qquad \text{Medio trazo} = 8 \times 0.09375 = 0.75\text{ u}$$

Esta identidad geométrica es la base del compilador: **el medio trazo de Phosphor (`8 u`) equivale exactamente al ancho del bisel especular `0.75 u` de nuestra arquitectura Glass**.

---

## 2. Etapas Matemáticas del Compilador v2 (`compiler/glass_compiler.py`)

### Etapa 1 · Muestreo de Curvas y Rasterización Antialiasing `4×4`
1. `parse_svg_subpaths(d)` interpreta la gramática completa de `<path d="...">` (`M,m,L,l,H,h,V,v,C,c,S,s,Q,q,A,a,Z,z`), convirtiendo arcos elípticos a parametrización por centro según W3C SVG 1.1.
2. Cada sub-camino cerrado se rasteriza con regla par-impar (`ImageChops.logical_xor`) a `1536×1536 px` y se promedia por caja `4×4` (`Resampling.BOX`) hacia una rejilla de trabajo de `384×384 px` (`1.5 px` por unidad de `256`, o `16 px` por unidad de `24×24`).

### Etapa 2 · Transformada de Distancia Euclidiana Exacta 2D (`EDT` `O(N)`)
Implementamos en Python puro el algoritmo separable en dos pasadas (envolvente inferior de parábolas) de **Felzenszwalb y Huttenlocher (2012)**:
- Calcula en tiempo lineal exacto $O(W \times H)$ el campo de distancia con signo $\text{SDF}(x, y)$ tanto para la región de tono `opacity="0.2"` ($P_{\text{seed}}$) como para el trazo principal ($P_{\text{primary}}$).
- `edt_1d_proj` conserva simultáneamente el índice del píxel frontera más cercano $\Pi_{\partial G}(p)$, necesario para extruir piezas traseras bajo el cristal siguiendo la normal exacta del borde sin abultar su grosor lateral.

---

## 3. Clasificación Topológica v2 (`0` Squircles y `243/243` con Refracción)

En los `237` iconos compilados, la capa `opacity="0.2"` ($P_{\text{seed}}$) cumple funciones distintas según el icono. El compilador v2 clasifica cada icono **sin ningún `if` por nombre**, midiendo la cobertura perimetral `perim_cov` y aplicando **descomposición morfológica real** en lugar del antiguo comodín *squircle* (`rx=5`) de v1:

| Patrón Topológico | Condición Determinista | Ejemplos Reales | Regla de Compilación Óptica en v2 |
| :--- | :--- | :--- | :--- |
| **Patrón A · Vasija Bordeada** | `perim_cov >= 0.89` | `Trash2`, `CreditCard`, `ShoppingBag`, `Search`, `Receipt`, `Clock`, `MapPin`, `Key` | $P_{\text{primary}}$ cierra el perímetro de $P_{\text{seed}}$. v2 aplica **apertura morfológica por cuello** ($\text{SDF} \le -r$) para separar asas, paletones o tapas unidas a un cuerpo voluminoso (`Key`, `ShoppingBag`) y extruye la pieza trasera dentro del cristal. Si no existe apéndice externo (`Receipt`, `Clock`, `MapPin`), genera un núcleo/gemelo desplazado autoencuadrado para garantizar refracción `back` real. |
| **Patrón B · Placa de Fondo Abierta** | `perim_cov < 0.89` | `RefreshCw`, `RotateCw`, `History`, `ExternalLink`, `ArrowRightLeft`, `Plus`, `Check`, `X`, `Loader2` | $P_{\text{seed}}$ actúa como lente de fondo y $P_{\text{primary}}$ es un glifo abierto. v2 conserva $G_{\text{glass}}$ suavizado, pasa los trazos nítidos al frente e inyecta paralaje refractado bajo la lente para mantener profundidad óptica en las 4 capas. |
| **Patrón C · Silueta Pura o Multicuerpo** | Sin $P_{\text{seed}}$ o silueta monolítica | `Star`, `Zap`, `Home`, `Shield`, `Phone`, `Wifi`, `LayoutGrid`, `Filter`, `Navigation` | **Cero *squircles* (`0/243`):** si hay múltiples componentes (`Wifi`, `LayoutGrid`) separa piezas entre cristal y masa trasera refractada; si es una silueta única (`Star`, `Zap`, `Home`, `Shield`, `Phone`) aplica cierre selectivo de alcobas cóncavas, usa la **silueta real del icono** como lente esmerilada con bisel `0.75 u` y proyecta una **silueta gemela desplazada y autoencuadrada dentro de `[1.2, 22.8]`** en la capa `back` bajo `feGaussianBlur`. |

---

## 4. Mejoras Geométricas Clave de v1 a v2

1. **Preservación de vértices agudos (`> 46°`) durante el suavizado Taubin:** En v1, el filtro pasabajas $\lambda/\mu$ redondeaba las puntas de estrellas (`Star`), rayos (`Zap`) y techos (`Home`). En v2, los nodos con giro angular $> 46^\circ$ quedan anclados durante las iteraciones de Taubin, eliminando dientes de sierra en tramos curvos sin achatar puntas vivas.
2. **Tangentes circulares exactas $\frac{4}{3}\tan(\theta/4)$ en curvas de Bézier:** Al ajustar arcos entre nodos suaves, v2 pondera la longitud de los manejadores cúbicos con la fórmula analítica exacta de aproximación circular $\alpha = \frac{4}{3}\tan(\theta/4)$ en lugar del tercio fijo, logrando círculos (`Clock`, `Search`, `RefreshCw`) y escudos (`Shield`) geométricamente redondos.
3. **Paralaje gemelo direccional autoencuadrado:** Cuando una silueta necesita gemelo trasero refractado, el vector de desplazamiento $(\Delta x, \Delta y)$ se calcula hacia el cuadrante con mayor holgura dentro de `viewBox="0 0 24 24"` respetando un margen seguro `[1.2, 22.8]`, evitando cualquier recorte contra los bordes del lienzo.
4. **Salvaguardas de cavidades internas (`CalendarDays`, `Blend`, `MapPin`):** `fill_small_exterior_holes` solo cierra ojales diminutos cuya frontera toque una única componente conexa, preservando intactas las ventanas de calendarios y diagramas entrelazados.

---

## 5. Cuándo Usar el Compilador Automático vs. `compiler/domain_dsl.py`

- **Compilador v2 (`0 tokens`):** Cubre con fidelidad geométrica y `100%` de refracción trasera el catálogo operativo completo (`237` iconos desde `@phosphor-icons/core`: navegación, cobro, alertas, mapas, dispositivos, inventario y usuarios).
- **DSL analítico (`compiler/domain_dsl.py`):** Resérvalo para los **`4` a `8` iconos insignia propios de tu giro comercial** (`Pizza`, `PizzaWhole`, `PizzaCutter`, `Bike`, `Printer`, `Flame`), donde diseñas piezas mecánicas específicas de marca con coordenadas exactas.
