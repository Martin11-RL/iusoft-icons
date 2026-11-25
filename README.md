# IU-SOFT Icons

Librería vectorial de **243 iconos × 4 estilos (`972` SVGs)** en `viewBox="0 0 24 24"`, diseñada para sistemas de punto de venta, comercio digital y aplicaciones web/móviles de alto contraste. Combina geometría analítica propia para iconos de dominio con un **compilador geométrico determinista (`0 tokens`, sin IA generativa)** sobre `@phosphor-icons/core` (`MIT`).

- **Galería interactiva en vivo:** [https://iusoft-icons.vercel.app](https://iusoft-icons.vercel.app)
- **Licencia:** `MIT` (`IU-SOFT` + atribución `@phosphor-icons/core`)

---

## Resumen de Arquitectura

| Bloque | Cantidad | Origen | Variantes incluidas |
| :--- | ---: | :--- | :--- |
| **Giro Pizzería y POS** | `6` iconos (`24` SVGs) | Primitivas analíticas (`compiler/domain_dsl.py`) | `glass`, `outline`, `solid`, `duotone` |
| **Esenciales Base** | `80` iconos (`320` SVGs) | Compilador `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Operación POS Extendida** | `157` iconos (`628` SVGs) | Compilador `0-tokens` sobre `@phosphor-icons/core` (`MIT`) | `glass`, `outline`, `solid`, `duotone` |
| **Total librería** | **`243` iconos (`972` SVGs)** | **100% reproducible desde código (`npm run build`)** | **`197/197` equivalencias `lucide-react` cubiertas** |

---

## Estructura del Repositorio

```text
iusoft-icons/
├── index.html                        # Aplicación web interactiva autocontenida (0 peticiones externas)
├── vercel.json                       # Configuración de despliegue estático en Vercel
├── package.json                      # Scripts npm (build, verify, serve) + @phosphor-icons/core@2.1.1
├── requirements.txt                  # Dependencia Python del compilador (Pillow>=10.0.0)
├── icons/
│   ├── glass/*.svg                   # 243 SVGs independientes con refracción feGaussianBlur y bisel 0.75u
│   ├── outline/*.svg                 # 243 SVGs lineales (peso óptico 1.5u)
│   ├── solid/*.svg                   # 243 SVGs sólidos
│   └── duotone/*.svg                 # 243 SVGs en doble tono (opacidad secundaria 0.20)
├── dist/
│   ├── catalog.json                  # Catálogo estructurado completo de los 243 iconos
│   └── iusoft-icons-react.tsx        # Componente React/TypeScript <IuSoftIcon /> con física de resortes
├── compiler/
│   ├── manifest.json                 # Declaración de los 243 iconos (punto único para agregar nuevos)
│   ├── domain_dsl.py                 # Primitivas analíticas G¹/C¹ con offset interior exacto de 0.75u
│   ├── glass_compiler.py             # Motor EDT + Patrones Topológicos A/B/C + Marching Squares + Bézier
│   ├── template.html                 # Plantilla HTML limpia de la galería web
│   ├── build_suite.py                # CLI de compilación completa o incremental (--only <slug>)
│   └── verify_suite.py               # Auditor determinista de los 972 SVGs e higiene del repositorio
├── examples/
│   ├── 01-pizza-glass-lab.html       # Laboratorio óptico de 3 iconos base (Rebanada, Entera, Cortador)
│   ├── 02-domain-suite-lab.html      # Laboratorio de giro (Moto reparto, Ticket impresora, Horno y fuego)
│   └── 03-compiler-before-after.html # Comparativa en vivo: SVG Duotone crudo vs. salida compilada Glass
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
# Galería principal:  http://localhost:4321/
# Laboratorio 01:     http://localhost:4321/examples/01-pizza-glass-lab.html
# Laboratorio 02:     http://localhost:4321/examples/02-domain-suite-lab.html
# Laboratorio 03:     http://localhost:4321/examples/03-compiler-before-after.html
```

### 3. Agregar o recompilar un icono en menos de 1 segundo (`0 tokens`)

Edita `compiler/manifest.json` agregando cualquier icono de `@phosphor-icons/core` y ejecuta:

```bash
python3 compiler/build_suite.py --only credit-card
```

Para regenerar los `972` archivos `.svg`, `dist/catalog.json`, `dist/iusoft-icons-react.tsx` e `index.html` desde cero en paralelo:

```bash
npm run build
```

---

## Uso en Proyectos Web y React

### A. Archivo SVG directo (`<img>`, Figma o HTML estático)

Todos los archivos dentro de `icons/{glass,outline,solid,duotone}/` incluyen definiciones `<defs>` autocontenidas con IDs únicos por slug:

```html
<img src="/icons/glass/pizza.svg" width="32" height="32" alt="Pizza" />
<img src="/icons/glass/printer.svg" width="32" height="32" alt="Impresora térmica" />
<img src="/icons/outline/credit-card.svg" width="24" height="24" alt="Pago con tarjeta" />
```

### B. Componente React / Next.js (`dist/iusoft-icons-react.tsx`)

El componente `<IuSoftIcon />` usa `React.useId()` para evitar colisiones de máscaras SVG cuando se montan varios iconos en la misma vista, integra física de resortes amortiguados a `60fps` en hover y respeta `prefers-reduced-motion: reduce`:

```tsx
import { IuSoftIcon } from "./dist/iusoft-icons-react";

export function BarraAccionesCaja() {
  return (
    <div className="flex items-center gap-3">
      {/* Puntos protagonistas (navegación, KPIs, cabeceras): variante Glass */}
      <IuSoftIcon name="Pizza" variant="glass" size={28} animate="hover" />
      <IuSoftIcon name="Printer" variant="glass" size={28} animate="hover" />
      <IuSoftIcon name="Bike" variant="glass" size={28} animate="hover" />

      {/* Listas densas o tablas operativas: variante Outline o Duotone (sin feGaussianBlur) */}
      <IuSoftIcon name="CreditCard" variant="outline" size={20} className="text-zinc-900" />
    </div>
  );
}
```

> **Regla de rendimiento en producción:** Mantén un máximo de **`12–15` iconos `glass` simultáneos por pantalla** (barra lateral, tarjetas de resumen, estados vacíos o modales de confirmación). En tablas, comandas o catálogos con `50+` filas repetidas usa siempre `variant="outline"` o `variant="duotone"`, que no invocan `<feGaussianBlur>` en GPU y mantienen `60fps` estables en móviles de gama media.

---

## Documentación Técnica Detallada

1. [**01 · Arquitectura Óptica Glass (`24×24`)**](./docs/01-ARQUITECTURA-OPTICA-GLASS.md): Receta exacta de las 4 capas vectoriales, gradientes, máscaras duales `userSpaceOnUse`, bisel `evenodd` de `0.75 u`, física de resortes y presupuesto de GPU.
2. [**02 · Algoritmo del Compilador Geométrico `0-Tokens`**](./docs/02-ALGORITMO-COMPILADOR-0-TOKENS.md): Transformada de Distancia Euclidiana de Felzenszwalb-Huttenlocher, los 3 Patrones Topológicos (`A`, `B` y `C`), suavizado Taubin `λ/μ`, curvas de Bézier `C¹` y límites geométricos reales.
3. [**03 · Guía de Mantenimiento y Extensión**](./docs/03-GUIA-DE-MANTENIMIENTO-Y-EXTENSION.md): Cómo incorporar cualquiera de los `1,512` iconos de Phosphor o programar iconos propios de industria en `domain_dsl.py`.
4. [**04 · Inventario de Cobertura POS (`197/197`)**](./docs/04-INVENTARIO-COBERTURA-POS.md): Mapa completo 1 a 1 contra los símbolos de `lucide-react`.
