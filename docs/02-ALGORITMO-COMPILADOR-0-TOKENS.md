# 02 · Algoritmo del Compilador Geométrico `0-Tokens`

Este documento detalla cómo `compiler/glass_compiler.py` convierte automáticamente cualquier icono vectorial estándar de `@phosphor-icons/core` (`MIT`, `viewBox="0 0 256 256"`) en un icono **Glass `24×24` de 4 capas** de manera `100%` determinista, en local y consumiendo **`0 tokens` de modelos de IA**.

---

## 1. Equivalencia de Escala entre Phosphor (`256×256`) y `24×24`

Los iconos de Phosphor están diseñados sobre una cuadrícula de `256×256` unidades con un grosor de trazo uniforme de `16 u` (medio trazo = `8 u`). Al escalar al lienzo estándar de `24×24`:

$$\text{Factor de escala} = \frac{24}{256} = 0.09375$$

$$\text{Grosor de trazo} = 16 \times 0.09375 = 1.50\text{ u}, \qquad \text{Medio trazo} = 8 \times 0.09375 = 0.75\text{ u}$$

Esta identidad geométrica es clave: **el medio trazo de Phosphor (`8 u`) equivale exactamente al ancho del bisel especular `0.75 u` de nuestra arquitectura Glass**.

---

## 2. Etapas Matemáticas del Compilador (`compiler/glass_compiler.py`)

### Etapa 1 · Muestreo de Curvas y Rasterización Antialiasing `4×4`
1. `parse_svg_subpaths(d)` interpreta la gramática completa de `<path d="...">` (`M,m,L,l,H,h,V,v,C,c,S,s,Q,q,A,a,Z,z`), convirtiendo arcos elípticos a parametrización por centro según la especificación W3C SVG 1.1.
2. Cada sub-camino cerrado se rasteriza con regla par-impar (`ImageChops.logical_xor`) a `1536×1536 px` y se promedia por caja `4×4` (`Resampling.BOX`) hacia una rejilla de trabajo de `384×384 px` (`1.5 px` por unidad de `256`, o `16 px` por unidad de `24×24`).

### Etapa 2 · Transformada de Distancia Euclidiana Exacta 2D (`EDT` `O(N)`)
Implementamos en Python puro el algoritmo separable en dos pasadas (envolvente inferior de parábolas) de **Felzenszwalb y Huttenlocher (2012)**:
- Calcula en tiempo lineal exacto $O(W \times H)$ el campo de distancia con signo $\text{SDF}(x, y)$ tanto para la región de tono `opacity="0.2"` ($P_{\text{seed}}$) como para el trazo principal ($P_{\text{primary}}$).
- `edt_1d_proj` conserva simultáneamente el índice del píxel frontera más cercano $\Pi_{\partial G}(p)$, necesario para extruir piezas traseras bajo el cristal siguiendo la normal exacta del borde sin abultar su grosor lateral.

---

## 3. Los 3 Patrones Topológicos en Iconos Duotone (Lección Clave)

Al auditar los `237` iconos compilados descubrimos que en una librería Duotone profesional la capa `opacity="0.2"` ($P_{\text{seed}}$) **no cumple siempre el mismo papel topológico**. Tratar todos los iconos con una sola fórmula produce siluetas lavadas o flechas recortadas.

El compilador los clasifica automáticamente **sin ningún `if` por nombre de icono** midiendo la **cobertura del anillo perimetral** de $P_{\text{seed}}$ por el trazo principal $P_{\text{primary}}$:

$$\text{perim\_cov} = \frac{\left|\{p : |\text{SDF}(P_{\text{seed}})(p)| \le 3\text{ px} \;\wedge\; P_{\text{primary}}(p) = 1\}\right|}{\left|\{p : |\text{SDF}(P_{\text{seed}})(p)| \le 3\text{ px}\}\right|}$$

| Patrón Topológico | Condición Determinista | Ejemplos Reales | Regla de Compilación Óptica |
| :--- | :--- | :--- | :--- |
| **Patrón A · Vasija Bordeada** | `perim_cov >= 0.89` y `exposed_obs_px >= 900` | `Trash2`, `CreditCard`, `ShoppingBag`, `Search`, `Truck`, `CalendarDays`, `Blend`, `MapPin` | $P_{\text{primary}}$ cierra el perímetro completo de $P_{\text{seed}}$. El cristal absorbe ese borde perimetral ($G_{\text{glass}} = \text{dilate}(P_{\text{seed}}, +8\text{ u})$). Las islas internas van nítidas a `front`, y los apéndices exteriores (`D_back`) se extruyen `18 u` hacia adentro del cristal siguiendo $\Pi_{\partial G}$ para generar refracción real bajo `feGaussianBlur`. |
| **Patrón B · Placa de Fondo Abierta** | `perim_cov < 0.89` | `RefreshCw`, `RotateCw`, `History`, `ExternalLink`, `ArrowRightLeft`, `ArrowUpDown`, `Type`, `Menu`, `Plus`, `Check`, `X`, `Loader2`, `LogOut`, `Link2` | $P_{\text{seed}}$ es un disco, cápsula o tarjeta de fondo y $P_{\text{primary}}$ es un glifo abierto que **no** cierra su perímetro. $G_{\text{glass}}$ es $P_{\text{seed}}$ suavizado (`+3.5 px`) y el **`100%` de $P_{\text{primary}}$ pasa íntegro con sus curvas nativas a `front`** (obsidiana nítida), sin recortar flechas ni letras. |
| **Patrón C · Silueta Simple sin Obsidiana Expuesta** | Sin $P_{\text{seed}}$, o tras Patrón A queda `exposed_obs_px < 900` | `Filter`, `Shield`, `ChevronUp`, `ChevronDown`, `Ban`, `Navigation`, `Wifi`, `LayoutGrid`, `SplitSquareHorizontal` | Evita siluetas pálidas de puro cristal sin ancla oscura: si tiene `>= 2` piezas conexas (`LayoutGrid`, `SplitSquareHorizontal`) alterna `50/50` piezas en obsidiana y cristal; si es `1` sola pieza (`Filter`, `Shield`, `Chevron*`) coloca una placa *squircle* de cristal (`rx=5`) con bisel `0.75 u` detrás y centra el glifo nativo al `72%` en obsidiana nítida al frente (`contraste > 9:1`). |

### Dos salvaguardas topológicas adicionales en el Patrón A

1. **Relleno selectivo de huecos en `P_seed` (`MapPin`, `Settings`):** Si $P_{\text{seed}}$ tiene un hueco interior cerrado (como el aro central de un pin de mapa o un engrane), el compilador rellena ese hueco en $G_{\text{glass}}$ para que el cristal sea continuo y el aro interior de $P_{\text{primary}}$ quede nítido encima en `front`.
2. **Protección de cavidades multicontorno (`CalendarDays`, `Blend`):** Al preparar $D_{\text{back}}$, `fill_small_exterior_holes` solo cierra ojales diminutos (`<= 1.2%` del área) cuya frontera toque **una única componente conexa** de $P_{\text{primary}}$. Jamás rellena la caja interior de un calendario con puntos de días adentro (`CalendarDays`) ni las lunas exteriores de dos círculos entrelazados (`Blend`).

---

## 4. Vectorización Suave (`Marching Squares` -> `Taubin` -> `RDP` -> `Bézier C¹`)

Para convertir los campos SDF de vuelta a caminos SVG limpios y ligeros:
1. **Marching Squares con interpolación lineal sub-píxel** extrae lazos cerrados sobre las isocurvas $\text{SDF} = 0$ y $\text{SDF} = -12\text{ px}$.
2. **Filtro pasabajas $\lambda/\mu$ de Taubin** (`4` iteraciones con $\lambda = 0.33, \mu = -0.34$) elimina el escalonamiento de la rejilla **sin encoger el radio de los círculos ni redondear en exceso** (a diferencia del suavizado Laplaciano simple).
3. **Ramer-Douglas-Peucker (`eps = 0.28 px`)** reduce los vértices redundantes conservando tramos rectos (`>= 0.47 u` emitidos como comandos `L` exactos).
4. **Ajuste de Bézier cúbicas `C¹`** calcula tangentes unitarias promediadas en nodos suaves y quiebra tangentes en esquinas vivas (`> 65°`), produciendo archivos `.svg` compactos (`~2–5 KB`).

---

## 5. Límites Geométricos Honestos y Cuándo Usar `domain_dsl.py`

El compilador `0-tokens` resuelve con calidad de producción (`~88%–95%` de cercanía al trazo manual) iconos generales de interfaz, finanzas, flechas, dispositivos y documentos. Su límite físico natural aparece en un único caso:

- **Piezas que se tocan en el dibujo original:** En `trash-duotone.svg`, la tapa horizontal de la papelera toca directamente el borde superior del bote sin espacio vacío en medio. Como en el SVG fuente son una sola masa continua en $P_{\text{primary}}$, el compilador mantiene la tapa unida al cuerpo trasero en lugar de flotarla con separación de aire como haría un ilustrador humano.
- **Criterio práctico:** Usa el compilador automático para el `95%+` del catálogo funcional y reserva `compiler/domain_dsl.py` únicamente para los **4 a 8 iconos emblema de tu giro comercial** donde quieras separar piezas mecánicas o dar personalidad propia de marca.
