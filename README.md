# IU-SOFT Icons

Librería vectorial de **243 iconos × 4 estilos (`972` SVGs)** en `viewBox="0 0 24 24"`, diseñada para sistemas de punto de venta, comercio digital y aplicaciones web/móviles de alto contraste. Combina geometría analítica propia para iconos de dominio con el **compilador geométrico determinista Glass v2 (`0 tokens`, sin IA generativa)** sobre `@phosphor-icons/core` (`MIT`).

- **Galería interactiva en vivo:** [https://iusoft-icons.vercel.app](https://iusoft-icons.vercel.app)
- **Vista en superficies Sarchi POS:** [`./examples/04-sarchi-surfaces-preview.html`](./examples/04-sarchi-surfaces-preview.html)
- **Licencia:** `MIT` (`IU-SOFT` + atribución `@phosphor-icons/core`)

---

## Novedades de Glass v2 y Superficies Adaptativas

1. **Cero comodines *squircle* (`0/243`) y refracción garantizada (`243/243`):** El compilador v2 elimina por completo los marcos genéricos `rx=5` de v1, preserva vértices agudos (`> 46°` en estrellas, rayos, casas y llaves), calcula tangentes circulares exactas $\frac{4}{3}\tan(\theta/4)$ y genera capa trasera refractada bajo `feGaussianBlur` en el `100%` del catálogo.
2. **Cuatro paletas ópticas adaptativas (`--iusoft-*`):** Todos los iconos `glass` leen variables CSS semánticas que conmutan automáticamente por cascada entre mostrador claro (`light`), cabeceras oscuras y modo nocturno OLED (`dark`), estado activo de reparto (`emerald`) e insignias sobre blanco (`emerald-light`).
3. **Adaptador directo para Sarchi POS (`dist/sarchi-icons.tsx`):** Exporta **`215/215` símbolos** compatibles 1 a 1 con las importaciones de `lucide-react` (`Pizza`, `Bike`, `Flame`, `Printer`, `ArrowLeftRight`, `Loader2`, etc.) junto con `<SarchiIconProvider />`.

---

## Resumen de Arquitectura

| Bloque | Cantidad | Origen | Variantes incluidas |
| :--- | ---: | :--- | :--- |
| **Giro Pizzería y POS** | `6` iconos (`24` SVGs) | Primitivas analíticas (`compiler/domain_dsl.py`) | `glass`, `outline`, `solid`, `duotone` |
| **Esenciales Base** | `80` iconos (`320` SVGs) | Compilador v2 `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Operación POS Extendida** | `157` iconos (`628` SVGs) | Compilador v2 `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Total librería** | **`243` iconos (`972` SVGs)** | **100% reproducible desde código (`npm run build`)** | **`215/215` símbolos `lucide-react` exportados** |

---

## Estructura del Repositorio

```text
iusoft-icons/
├── index.html                            # Galería web interactiva con selector de superficie óptica
├── vercel.json                           # Configuración de despliegue estático en Vercel
├── package.json                          # Scripts npm (build, verify, serve) + @phosphor-icons/core@2.1.1
├── requirements.txt                      # Dependencia Python del compilador (Pillow>=10.0.0)
├── icons/
│   ├── glass/*.svg                       # 243 SVGs con refracción feGaussianBlur, bisel 0.75u y tokens --iusoft-*
│   ├── outline/*.svg                     # 243 SVGs lineales (peso óptico 1.5u)
│   ├── solid/*.svg                       # 243 SVGs sólidos
│   └── duotone/*.svg                     # 243 SVGs en doble tono (opacidad secundaria 0.20)
├── dist/
│   ├── catalog.json                      # Catálogo estructurado v2 de los 243 iconos
│   ├── iusoft-icons-react.tsx            # Componente <IuSoftIcon /> + IUSOFT_SURFACE_TOKENS
│   └── sarchi-icons.tsx                  # 215 componentes compatibles con lucide-react + <SarchiIconProvider />
├── compiler/
│   ├── manifest.json                     # Declaración de los 243 iconos (punto único para agregar nuevos)
│   ├── domain_dsl.py                     # Primitivas analíticas G¹/C¹ con offset interior exacto de 0.75u
│   ├── glass_compiler.py                 # Motor v2: EDT + Apertura/Cierre Morfológico + Taubin con Esquinas + Bézier
│   ├── template.html                     # Plantilla HTML limpia de la galería web
│   ├── build_suite.py                    # CLI de compilación completa o incremental (--only <slug>)
│   └── verify_suite.py                   # Auditor determinista v2 de los 972 SVGs, TSX e higiene pública
├── examples/
│   ├── 01-pizza-glass-lab.html           # Laboratorio óptico de 3 iconos base (Rebanada, Entera, Cortador)
│   ├── 02-domain-suite-lab.html          # Laboratorio de giro (Moto reparto, Ticket impresora, Horno y fuego)
│   ├── 03-compiler-before-after.html     # Comparativa en vivo: SVG Duotone crudo vs. salida compilada Glass
│   └── 04-sarchi-surfaces-preview.html   # Comparador v1 vs v2 y prueba en las 3 superficies reales de Sarchi POS
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
# Laboratorio 01 (Pizza):      http://localhost:4321/examples/01-pizza-glass-lab.html
# Laboratorio 02 (Giro POS):   http://localhost:4321/examples/02-domain-suite-lab.html
# Laboratorio 03 (Compilador): http://localhost:4321/examples/03-compiler-before-after.html
# Vista Sarchi POS (v1 vs v2): http://localhost:4321/examples/04-sarchi-surfaces-preview.html
```

### 3. Agregar o recompilar un icono en menos de 1 segundo (`0 tokens`)

Edita `compiler/manifest.json` agregando cualquier icono de `@phosphor-icons/core` y ejecuta:

```bash
python3 compiler/build_suite.py --only credit-card
```

Para regenerar los `972` archivos `.svg`, `dist/catalog.json`, `dist/iusoft-icons-react.tsx`, `dist/sarchi-icons.tsx` e `index.html` desde cero en paralelo:

```bash
npm run build
```

---

## Uso en Proyectos Web, React y Sarchi POS

### A. Archivo SVG directo (`<img>`, Figma o HTML estático)

Todos los archivos dentro de `icons/{glass,outline,solid,duotone}/` incluyen definiciones `<defs>` autocontenidas con valores de respaldo para fondo claro y variables `--iusoft-*`:

```html
<img src="/icons/glass/pizza.svg" width="32" height="32" alt="Pizza" />
<img src="/icons/glass/printer.svg" width="32" height="32" alt="Impresora térmica" />
<img src="/icons/outline/credit-card.svg" width="24" height="24" alt="Pago con tarjeta" />
```

### B. Reemplazo directo de `lucide-react` (`dist/sarchi-icons.tsx`)

Envuelve tu árbol raíz con `<SarchiIconProvider />` para inyectar la hoja CSS de superficies adaptativas (`light`, `dark`, `emerald`, `emerald-light`) e importa cualquiera de los `215` símbolos con la misma firma de propiedades (`size`, `variant`, `surface`, `animate`):

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
    <SarchiIconProvider defaultVariant="glass">
      <div className="flex items-center gap-3">
        {/* Insignia oscura (#18181B): activa plata-cromo automáticamente */}
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-900" data-iusoft-surface="dark">
          <Pizza size={22} animate="hover" />
        </div>

        {/* Estado de reparto activo en esmeralda */}
        <Bike size={22} surface="emerald" animate="hover" />
        <Flame size={22} />

        {/* Tablas densas y spinners continuos usan outline (0 feGaussianBlur) */}
        <ArrowLeftRight size={16} variant="outline" />
        <Loader2 size={16} className="animate-spin" />
      </div>
    </SarchiIconProvider>
  );
}
```

> **Regla de rendimiento en producción:** Mantén un máximo de **`12–15` iconos `glass` simultáneos por pantalla** (barra lateral, insignias de cabecera, tarjetas de indicadores o estados principales). En tablas de comandas, listados con decenas de filas o animaciones de giro continuo (`Loader2`) usa `variant="outline"` o `variant="duotone"`, que no invocan `<feGaussianBlur>` en GPU y conservan `60fps` estables en móviles.

---

## Documentación Técnica Detallada

1. [**01 · Arquitectura Óptica Glass (`24×24`)**](./docs/01-ARQUITECTURA-OPTICA-GLASS.md): Receta de las 4 capas vectoriales, gradientes, máscaras duales `userSpaceOnUse`, bisel `evenodd` de `0.75 u`, física de resortes y presupuesto de GPU.
2. [**02 · Algoritmo del Compilador Geométrico `0-Tokens` (v2)**](./docs/02-ALGORITMO-COMPILADOR-0-TOKENS.md): Transformada de Distancia Euclidiana `O(N)`, descomposición morfológica v2 (`0` squircles), preservación de vértices agudos y paralaje gemelo autoencuadrado.
3. [**03 · Guía de Mantenimiento, Superficies `--iusoft-*` y Extensión**](./docs/03-GUIA-DE-MANTENIMIENTO-Y-EXTENSION.md): Cómo agregar iconos de Phosphor, configurar las 4 superficies ópticas, integrar `dist/sarchi-icons.tsx` y publicar en Vercel.
4. [**04 · Inventario de Cobertura POS (`197/197` iconos · `215` símbolos)**](./docs/04-INVENTARIO-COBERTURA-POS.md): Mapa completo 1 a 1 contra los símbolos de `lucide-react`.
