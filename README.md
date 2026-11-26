# IU-SOFT Icons

Librería vectorial de **260 iconos × 4 estilos (`1,040` SVGs)** en `viewBox="0 0 24 24"`, diseñada para sistemas de punto de venta, comercio digital y aplicaciones web/móviles de alto contraste. Combina geometría analítica propia para iconos de dominio con el **compilador geométrico determinista Glass v2 (`0 tokens`, sin IA generativa)** y un motor de **8 paletas ópticas de refracción cromática contextual** sobre `@phosphor-icons/core` (`MIT`).

- **Galería interactiva en vivo:** [https://iusoft-icons.vercel.app](https://iusoft-icons.vercel.app)
- **Laboratorio de refracción cromática:** [`./examples/05-contextual-color-glass.html`](./examples/05-contextual-color-glass.html)
- **Vista en superficies Sarchi POS:** [`./examples/04-sarchi-surfaces-preview.html`](./examples/04-sarchi-surfaces-preview.html)
- **Licencia:** `MIT` (`IU-SOFT` + atribución `@phosphor-icons/core`)

---

## Novedades de Glass v2.2 · Refracción Cromática Contextual

1. **Separación óptica de 2 canales (`obs-back` + `obs-front`) y cristal tintado (`8–14%`):** Cada uno de los `260` iconos recibe determinísticamente una de las **8 familias cromáticas contextuales** calibradas para superficie clara (`#FFFFFF` / `#FAFAFA`) y modo oscuro OLED (`#09090B` / `#18181B`), conmutable en tiempo real con `tone="contextual" | "mono"`:
   - `gastronomia` (*Terracota y queso horneado*)
   - `horno-calor` (*Ámbar-carmesí*)
   - `mensajeria` (*Verde jade*)
   - `tesoreria` (*Esmeralda tesorería*)
   - `ruta-logistica` (*Azul cobalto*)
   - `clientes-equipo` (*Índigo zafiro*)
   - `alerta-peligro` (*Rubí sobrio*)
   - `sistema-grafito` (*Cuarzo grafito*)
2. **Cero comodines *squircle* y refracción trasera garantizada:** El compilador preserva vértices agudos (`> 46°`), calcula tangentes circulares exactas $\frac{4}{3}\tan(\theta/4)$ y genera capa trasera refractada bajo `feGaussianBlur stdDeviation="1.6"` con bisel especular `0.75u`.
3. **Adaptador directo para Sarchi POS (`dist/sarchi-icons.tsx`):** Exporta **`281` símbolos** compatibles 1 a 1 con `lucide-react` (`Pizza`, `Bike`, `Flame`, `Printer`, `ArrowLeftRight`, `Loader2`, etc.) junto con `<SarchiIconProvider tone="contextual" />`.

---

## Resumen de Arquitectura

| Bloque | Cantidad | Origen | Variantes incluidas |
| :--- | ---: | :--- | :--- |
| **Giro Pizzería y POS** | `6` iconos (`24` SVGs) | Primitivas analíticas (`compiler/domain_dsl.py`) | `glass`, `outline`, `solid`, `duotone` |
| **Esenciales Base** | `80` iconos (`320` SVGs) | Compilador v2 `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Operación POS Extendida** | `174` iconos (`696` SVGs) | Compilador v2 `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Total librería** | **`260` iconos (`1,040` SVGs)** | **100% reproducible desde código (`npm run build`)** | **`281` símbolos `lucide-react` exportados** |

---

## Estructura del Repositorio

```text
iusoft-icons/
├── index.html                            # Catálogo web con conmutador Color Contextual | Monocromo + Claro | OLED
├── vercel.json                           # Configuración de despliegue estático en Vercel
├── package.json                          # Scripts npm (build, verify, serve) + @phosphor-icons/core@2.1.1
├── requirements.txt                      # Dependencia Python del compilador (Pillow>=10.0.0)
├── icons/
│   ├── glass/*.svg                       # 260 SVGs con refracción de 2 canales, bisel 0.75u y tokens --iusoft-*
│   ├── outline/*.svg                     # 260 SVGs lineales (peso óptico 1.5u)
│   ├── solid/*.svg                       # 260 SVGs sólidos
│   └── duotone/*.svg                     # 260 SVGs en doble tono (opacidad secundaria 0.20)
├── dist/
│   ├── catalog.json                      # Catálogo estructurado de los 260 iconos + palette / paletteLabel
│   ├── iusoft-icons-react.tsx            # Componente <IuSoftIcon /> con tone="contextual" | "mono"
│   └── sarchi-icons.tsx                  # 281 componentes compatibles con lucide-react + <SarchiIconProvider />
├── compiler/
│   ├── manifest.json                     # Declaración de los 260 iconos (punto único para agregar nuevos)
│   ├── contextual_palettes.py            # Clasificador determinista 0-tokens de las 8 paletas ópticas
│   ├── domain_dsl.py                     # Primitivas analíticas G¹/C¹ con offset interior exacto de 0.75u
│   ├── glass_compiler.py                 # Motor v2: EDT + Apertura/Cierre Morfológico + Taubin con Esquinas + Bézier
│   ├── template.html                     # Plantilla HTML limpia de la galería web
│   ├── build_suite.py                    # CLI de compilación (--only <slug>, --recolor-only)
│   └── verify_suite.py                   # Auditor determinista de los 1,040 SVGs, TSX e higiene pública
├── examples/
│   ├── 01-pizza-glass-lab.html           # Laboratorio óptico de 3 iconos base (Rebanada, Entera, Cortador)
│   ├── 02-domain-suite-lab.html          # Laboratorio de giro (Moto reparto, Ticket impresora, Horno y fuego)
│   ├── 03-compiler-before-after.html     # Comparativa en vivo: SVG Duotone crudo vs. salida compilada Glass
│   ├── 04-sarchi-surfaces-preview.html   # Comparador v1 vs v2 y prueba en las 3 superficies reales de Sarchi POS
│   └── 05-contextual-color-glass.html    # Laboratorio de 5 iconos con desglose anatómico de 4 capas a 72px
└── docs/
    ├── 01-ARQUITECTURA-OPTICA-GLASS.md
    ├── 02-ALGORITMO-COMPILADOR-0-TOKENS.md
    ├── 03-GUIA-DE-MANTENIMIENTO-Y-EXTENSION.md
    └── 04-INVENTARIO-COBERTURA-POS.md
```

---

## Inicio Rápido

### 1. Instalar dependencias y verificar integridad

```bash
npm install
pip install -r requirements.txt
npm run verify
```

### 2. Servir la galería y los laboratorios localmente

```bash
npm run serve
# Galería principal:           http://localhost:4321/
# Laboratorio Color (05):      http://localhost:4321/examples/05-contextual-color-glass.html
# Vista Sarchi POS (04):       http://localhost:4321/examples/04-sarchi-surfaces-preview.html
```

### 3. Reasignar paletas o compilar iconos en `< 2 segundos` (`0 tokens`)

```bash
# Regenerar las 8 paletas contextuales, 1,040 SVGs, SDK React e index.html en <2s:
python3 compiler/build_suite.py --recolor-only

# Compilar únicamente un icono nuevo agregado a compiler/manifest.json:
python3 compiler/build_suite.py --only credit-card
```

---

## Uso en Proyectos Web, React y Sarchi POS

### A. Archivo SVG directo (`<img>`, Figma o HTML estático)

```html
<img src="/icons/glass/pizza.svg" width="32" height="32" alt="Pizza" />
<img src="/icons/glass/printer.svg" width="32" height="32" alt="Impresora térmica" />
<img src="/icons/outline/credit-card.svg" width="24" height="24" alt="Pago con tarjeta" />
```

### B. Reemplazo directo de `lucide-react` (`dist/sarchi-icons.tsx`)

```tsx
import {
  SarchiIconProvider,
  Pizza,
  Bike,
  Flame,
  ArrowLeftRight,
  Loader2,
} from "./dist/sarchi-icons";

export function CabeceraTurno() {
  return (
    <SarchiIconProvider defaultVariant="auto" tone="contextual">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-900" data-iusoft-surface="dark">
          <Pizza size={22} animate="hover" />
        </div>
        <Bike size={22} animate="hover" />
        <Flame size={22} />

        {/* Conmutación opcional a monocromo o trazos outline 0-blur */}
        <ArrowLeftRight size={16} tone="mono" variant="outline" />
        <Loader2 size={16} className="animate-spin" />
      </div>
    </SarchiIconProvider>
  );
}
```

> **Regla de rendimiento en producción:** Mantén un máximo de **`12–15` iconos `glass` simultáneos por pantalla** (barra lateral, insignias de cabecera, tarjetas de indicadores o estados principales). En tablas densas o animaciones continuas (`Loader2`) usa `variant="outline"` (`defaultVariant="auto"` aplica automáticamente `outline` en tamaños `<= 15px` y `animate-spin`).

---

## Documentación Técnica Detallada

1. [**01 · Arquitectura Óptica Glass (`24×24`)**](./docs/01-ARQUITECTURA-OPTICA-GLASS.md): Receta de las 4 capas vectoriales, gradientes, máscaras duales `userSpaceOnUse`, bisel `evenodd` de `0.75 u`, física de resortes y presupuesto de GPU.
2. [**02 · Algoritmo del Compilador Geométrico `0-Tokens` (v2)**](./docs/02-ALGORITMO-COMPILADOR-0-TOKENS.md): Transformada de Distancia Euclidiana `O(N)`, descomposición morfológica v2 (`0` squircles), preservación de vértices agudos y paralaje gemelo autoencuadrado.
3. [**03 · Guía de Mantenimiento, Superficies `--iusoft-*` y Extensión**](./docs/03-GUIA-DE-MANTENIMIENTO-Y-EXTENSION.md): Cómo agregar iconos de Phosphor, configurar superficies ópticas, integrar `dist/sarchi-icons.tsx` y publicar en Vercel.
4. [**04 · Inventario de Cobertura POS**](./docs/04-INVENTARIO-COBERTURA-POS.md): Mapa completo 1 a 1 contra los símbolos de `lucide-react`.
