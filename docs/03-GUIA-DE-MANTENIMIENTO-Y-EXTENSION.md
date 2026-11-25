# 03 · Guía de Mantenimiento y Extensión

Esta guía explica paso a paso cómo mantener la librería, agregar nuevos iconos desde `@phosphor-icons/core` (`1,512` iconos disponibles bajo licencia `MIT`), diseñar iconos propios de industria y publicar actualizaciones en Vercel.

---

## Caso A · Agregar un Icono Nuevo desde Phosphor en `< 1 minuto` (`0 tokens`)

`@phosphor-icons/core@2.1.1` incluye `1,512` iconos en `node_modules/@phosphor-icons/core/assets/{duotone,regular,fill}/`. Para sumar cualquiera de ellos a **IU-SOFT Icons**:

### Paso 1: Localizar el nombre (`phosphorSlug`) en Phosphor

```bash
ls node_modules/@phosphor-icons/core/assets/duotone/ | grep barcode
# -> barcode-duotone.svg  (el phosphorSlug es "barcode")
```

### Paso 2: Agregar la entrada en `compiler/manifest.json`

Abre `compiler/manifest.json` y añade un objeto JSON al final del arreglo:

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

> **Nota sobre `verify_suite.py`:** Si incrementas el total de iconos por encima de `243`, actualiza la constante esperada en `compiler/verify_suite.py` (o déjala como `len(manifest) >= 243`).

### Paso 3: Compilar solo ese icono en `< 1s`

```bash
python3 compiler/build_suite.py --only barcode
```

Este comando:
1. Genera `icons/glass/barcode.svg`, `icons/outline/barcode.svg`, `icons/solid/barcode.svg` e `icons/duotone/barcode.svg`.
2. Actualiza `dist/catalog.json` y el union type `IuSoftIconName` en `dist/iusoft-icons-react.tsx`.
3. Regenera `index.html` a partir de `compiler/template.html`.

### Paso 4: Validar con la puerta determinista

```bash
npm run verify
```

---

## Caso B · Diseñar un Icono Insignia de Giro en `compiler/domain_dsl.py`

Cuando lances un producto para otro sector (por ejemplo, **manufactura textil**, **logística**, **mensajería conversacional** o **punto de venta minorista**) y quieras entre `4` y `6` iconos protagonistas hechos a medida:

1. **Abre `compiler/domain_dsl.py`** y compone las piezas usando las primitivas analíticas existentes:
   - `circle_path(cx, cy, r)`
   - `capsule_path(x1, y1, x2, y2, r)`
   - `rounded_rect_path(x, y, w, h, r)`
   - `rounded_polygon_path(pts, radii, ins=0.0)` y `rounded_polygon_path(pts, radii, ins=0.75)` para el bisel interior `evenodd`.
   - `wedge_path(...)` / `inset_wedge_path(...)` / `oven_dome_path(...)`.
2. **Respeta las 3 reglas geométricas del DSL:**
   - Diseña siempre una pieza trasera (`back`) que **cruce parcialmente por detrás** del panel de cristal (`glass`) para que el desenfoque `feGaussianBlur` sea visible y aporte profundidad real.
   - Genera el contorno interior del bisel (`inner`) pasando `ins=0.75` a la misma primitiva del cristal exterior (`glass`).
   - Agrega también las salidas `outline` (`stroke-width="1.5"`), `solid` (`fill-rule="evenodd"` en recortes internos) y `duotone` (`fill-opacity="0.2"` + `outline`).
3. **Registra la clave en `build_domain_icons()`** de `compiler/domain_dsl.py` y agrega su ficha en `compiler/manifest.json` con `"origin": "domain-dsl"` y `"dslKey": "<tu-clave>"`.
4. Ejecuta `python3 compiler/build_suite.py --only <tu-clave>` e inspecciónalo a `24px`, `32px`, `40px`, `48px` y `96px` tanto en modo claro como en modo oscuro.

---

## Caso C · Modificar la Interfaz Web de la Galería (`index.html`)

Nunca edites `index.html` a mano directamente porque `npm run build` lo regenera desde `compiler/template.html`:

1. Edita **`compiler/template.html`** (conservando la línea `const CATALOG = __IUSOFT_CATALOG_JSON__;`).
2. Si agregas clases CSS nuevas en el HTML, decláralas dentro del bloque `<style>` de `compiler/template.html` para mantener **cero dependencias de CDN externas**.
3. Ejecuta `python3 compiler/build_suite.py --only pizza` (tarda `< 0.5s`) para regenerar `index.html` y luego corre `npm run verify`.

---

## Caso D · Despliegue a Producción en Vercel

El proyecto es `100%` estático en la raíz (`index.html` + `icons/` + `examples/` + `vercel.json`), por lo que Vercel no necesita ejecutar Python durante el despliegue si los artefactos generados ya fueron confirmados en Git:

1. Corre siempre antes de confirmar cambios:
   ```bash
   npm run verify
   ```
2. Confirma en Git (`compiler/`, `icons/`, `dist/`, `index.html`, `docs/`).
3. Al hacer `git push` a la rama principal de `Martin11-RL/iusoft-icons` (conectada a Vercel) o ejecutar `vercel deploy --prod`, la galería y las rutas estáticas (`/icons/glass/<slug>.svg`, `/examples/...`) quedan publicadas instantáneamente en el CDN global.
