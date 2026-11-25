# 03 · Guía de Mantenimiento, Superficies `--iusoft-*` y Extensión

Esta guía explica paso a paso cómo mantener la librería, configurar las **4 paletas ópticas adaptativas (`--iusoft-*`)**, integrar el adaptador directo **`dist/sarchi-icons.tsx`** (`215/215` símbolos), sumar nuevos iconos desde `@phosphor-icons/core` (`1,512` iconos `MIT`) y desplegar en Vercel.

---

## 1. Las 4 Paletas Ópticas Adaptativas (`--iusoft-*`)

En Glass v1 los gradientes estaban fijos para fondo blanco (`#5b5b5e -> #161617`), por lo que al montar un icono sobre una cabecera oscura (`#18181B`) o una vista nocturna OLED (`#09090B`) el contraste caía a `1.04:1`.

En **Glass v2**, los `243` archivos `icons/glass/*.svg`, `<IuSoftIcon />` y `<SarchiIconProvider />` consumen variables CSS `--iusoft-*` con respaldo automático a modo claro:

| Superficie (`data-iusoft-surface`) | Escenario de uso real | Masa trasera / frontal (`obs`) | Lente esmerilada (`glass`) | Bisel especular (`bevel`) |
| :--- | :--- | :--- | :--- | :--- |
| **`light`** *(por defecto)* | Fondos `#FFFFFF` y `#FAFAFA` (consola POS, barra lateral, tarjetas KPI, menú `/pedir`) | Obsidiana `#52525B -> #18181B` | Cristal frío `#E4E4E7 (0.68) -> #A1A1AA (0.64)` | Blanco `#FFFFFF` (`0.94 / 0.44 / 0.80`) |
| **`dark`** *(o ancestro `.dark`)* | Cabeceras `#18181B` y portal nocturno OLED `#09090B` (`/driver`) | Plata-cromo `#FAFAFA -> #A1A1AA` (`contraste > 7:1`) | Humo `#71717A (0.56) -> #3F3F46 (0.52)` | Luz cenital `#FFFFFF` (`0.94 / 0.32 / 0.08`) |
| **`emerald`** | Indicadores GPS activos, cobro en ruta y barras oscuras de confirmación | Menta viva `#4ADE80 -> #10B981` | Esmeralda `#10B981 (0.42) -> #065F46 (0.56)` | Destello `#ECFDF5 -> #6EE7B7` |
| **`emerald-light`** | Insignias verificadas sobre fondo claro (`#E7F8EE` / `#FFFFFF` en `/pedir`) | Bosque `#0D7A5C -> #052E16` | Jade translúcido `#6EE7B7 (0.58) -> #10B981 (0.48)` | Blanco puro `#FFFFFF` (`0.96 / 0.28 / 0`) |

Puedes inspeccionar las 4 superficies en vivo abriendo [`../examples/04-sarchi-surfaces-preview.html`](../examples/04-sarchi-surfaces-preview.html).

---

## 2. Integración Drop-In en Sarchi POS (`dist/sarchi-icons.tsx`)

`dist/sarchi-icons.tsx` exporta los **`215/215` símbolos** utilizados en el código de Sarchi POS (incluyendo alias exactos como `ArrowLeftRight`, `ArrowRightLeft`, `CheckCircle2`, `Trash2`, `Loader2`, `Pizza`, `Bike`, `Printer`, `Flame`):

1. **Copia `dist/sarchi-icons.tsx` e `dist/iusoft-icons-react.tsx`** dentro de `src/components/ui/` en tu proyecto Next.js / React.
2. **Monta `<SarchiIconProvider defaultVariant="glass">` en el layout raíz:** inyecta una sola vez la hoja CSS `IUSOFT_SURFACE_CSS` para que `.dark` y `[data-iusoft-surface="..."]` funcionen por cascada CSS sin re-renderizar componentes.
3. **Respeta las 3 reglas operativas de presupuesto gráfico:**
   - **Máximo `12–15` iconos `glass` simultáneos por vista** (navegación lateral, insignia de cabecera, tarjetas KPI, modales).
   - **Tablas densas y filas repetidas con `variant="outline"`:** evita crear docenas de filtros `feGaussianBlur` en listados largos de comandas.
   - **Spinners continuos sin desenfoque:** `Loader2` está preconfigurado por defecto en `variant="outline"` para que `animate-spin` corra en GPU sin recalcular máscaras en cada fotograma.

---

## 3. Agregar un Icono Nuevo desde Phosphor en `< 1 minuto` (`0 tokens`)

`@phosphor-icons/core@2.1.1` incluye `1,512` iconos en `node_modules/@phosphor-icons/core/assets/{duotone,regular,fill}/`. Para sumar cualquiera de ellos:

### Paso 1: Localizar el `phosphorSlug`
```bash
ls node_modules/@phosphor-icons/core/assets/duotone/ | grep barcode
# -> barcode-duotone.svg  (el phosphorSlug es "barcode")
```

### Paso 2: Declararlo en `compiler/manifest.json`
```json
  {
    "id": "phos-barcode",
    "slug": "barcode",
    "name": "Barcode",
    "label": "Código de barras",
    "origin": "phosphor-0-token",
    "sourceGroup": "compiler",
    "sourceLabel": "Compilado 0-Tokens",
    "category": "Caja y Comercio",
    "dslKey": null,
    "phosphorSlug": "barcode",
    "inPos": false,
    "posUses": 0,
    "lucideAliases": ["Barcode", "ScanBarcode"],
    "posModules": [],
    "keywords": "barcode codigo de barras escaner lector producto sku caja"
  }
```

### Paso 3: Compilar de forma incremental y verificar
```bash
python3 compiler/build_suite.py --only barcode
npm run verify
```

Este flujo actualiza automáticamente `icons/{glass,outline,solid,duotone}/barcode.svg`, `dist/catalog.json`, `dist/iusoft-icons-react.tsx`, `dist/sarchi-icons.tsx` e `index.html`.

---

## 4. Diseñar un Icono Insignia de Giro en `compiler/domain_dsl.py`

Cuando lances un producto para otro sector y quieras entre `4` y `8` iconos protagonistas hechos a medida:

1. **Abre `compiler/domain_dsl.py`** y compone las piezas con las primitivas analíticas (`circle_path`, `capsule_path`, `rounded_rect_path`, `rounded_polygon_path`, `wedge_path`, `oven_dome_path`).
2. **Asegura las 3 reglas ópticas:**
   - Una pieza `back` que cruce parcialmente por detrás del panel `glass` para producir refracción real bajo `feGaussianBlur`.
   - Contorno interior del bisel (`inner`) generado con `ins=0.75` sobre la misma primitiva exterior.
   - Variantes hermanas `outline` (`stroke-width="1.5"`), `solid` y `duotone` (`fill-opacity="0.2"`).
3. Registra la clave en `build_domain_icons()`, añádela en `compiler/manifest.json` con `"origin": "domain-dsl"` y ejecuta `python3 compiler/build_suite.py --only <slug>`.

---

## 5. Modificar la Galería Web (`index.html`) y Desplegar en Vercel

1. **Edita siempre `compiler/template.html`** (nunca `index.html` directamente) manteniendo cero dependencias de CDN externas.
2. Regenera las salidas rápidas sin recompilar los 243 iconos ejecutando:
   ```bash
   python3 -c 'import json, pathlib, sys; sys.path.insert(0, "compiler"); import build_suite; build_suite.regenerate_outputs(json.loads(pathlib.Path("dist/catalog.json").read_text(encoding="utf-8")))'
   ```
3. Ejecuta siempre `npm run verify` antes de confirmar cambios en Git o desplegar en Vercel (`vercel deploy --prod`).
