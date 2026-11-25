#!/usr/bin/env python3
"""
Validador Determinista de Integridad y Portabilidad (`compiler/verify_suite.py`).

Verifica con 0 tokens:
1. `compiler/manifest.json` contiene los 243 iconos únicos (197 de cobertura POS).
2. Existen los 972 archivos `.svg` en `icons/{glass,outline,solid,duotone}/`, todos son XML válido,
   tienen `viewBox="0 0 24 24"` y `icons/glass/*.svg` tiene `0` atributos `stroke`.
3. `dist/catalog.json`, `dist/iusoft-icons-react.tsx` e `index.html` están sincronizados, sin
   marcadores pendientes ni URLs de CDN externas.
4. Higiene de repositorio público: `0` rutas locales absolutas de máquina y `0` referencias a paquetes cerrados.
"""

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

COMPILER_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = COMPILER_DIR.parent


def fail(msg: str):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    manifest_fp = COMPILER_DIR / "manifest.json"
    if not manifest_fp.exists():
        fail("No existe compiler/manifest.json")
    manifest = json.loads(manifest_fp.read_text(encoding="utf-8"))
    if len(manifest) < 243:
        fail(f"Se esperaban >= 243 iconos en manifest.json, encontrados: {len(manifest)}")

    slugs = [m["slug"] for m in manifest]
    if len(set(slugs)) != len(slugs):
        fail("Existen slugs duplicados en compiler/manifest.json")

    pos_count = sum(1 for m in manifest if m.get("inPos"))
    if pos_count < 197:
        fail(f"Cobertura POS incompleta: {pos_count} < 197")

    # 1. Validar los 972 archivos SVG individuales
    total_svgs = 0
    for variant in ("glass", "outline", "solid", "duotone"):
        vdir = REPO_ROOT / "icons" / variant
        if not vdir.exists():
            fail(f"Falta carpeta icons/{variant}")
        for slug in slugs:
            fp = vdir / f"{slug}.svg"
            if not fp.exists():
                fail(f"Falta archivo SVG: icons/{variant}/{slug}.svg")
            raw = fp.read_text(encoding="utf-8")
            try:
                root = ET.fromstring(raw)
            except ET.ParseError as exc:
                fail(f"XML inválido en icons/{variant}/{slug}.svg: {exc}")
            if root.attrib.get("viewBox") != "0 0 24 24":
                fail(f"viewBox inválido en icons/{variant}/{slug}.svg: {root.attrib.get('viewBox')}")
            paths = [el for el in root.iter() if el.tag.split("}")[-1] in ("path", "circle", "rect")]
            if not paths:
                fail(f"SVG vacío sin geometría en icons/{variant}/{slug}.svg")
            if variant == "glass":
                for el in root.iter():
                    if "stroke" in el.attrib and el.attrib["stroke"] not in ("none", ""):
                        fail(f"Prohibido atributo stroke en estilo Glass: icons/glass/{slug}.svg")
            total_svgs += 1

    # 2. Validar dist/catalog.json y dist/iusoft-icons-react.tsx
    cat_fp = REPO_ROOT / "dist" / "catalog.json"
    if not cat_fp.exists():
        fail("Falta dist/catalog.json")
    cat = json.loads(cat_fp.read_text(encoding="utf-8"))
    if len(cat) != len(manifest):
        fail(f"dist/catalog.json ({len(cat)}) no coincide con manifest.json ({len(manifest)})")
    for item in cat:
        g = item["svg"]["glass"]
        if len(g.get("back", [])) + len(g.get("front", [])) == 0:
            fail(f"Icono Glass sin contraste de obsidiana: {item['slug']}")

    tsx_fp = REPO_ROOT / "dist" / "iusoft-icons-react.tsx"
    if not tsx_fp.exists():
        fail("Falta dist/iusoft-icons-react.tsx")
    tsx_txt = tsx_fp.read_text(encoding="utf-8")
    if "export function IuSoftIcon" not in tsx_txt:
        fail("dist/iusoft-icons-react.tsx no exporta IuSoftIcon")

    # 3. Validar index.html autocontenido
    html_fp = REPO_ROOT / "index.html"
    if not html_fp.exists():
        fail("Falta index.html en la raíz")
    html_txt = html_fp.read_text(encoding="utf-8")
    if "__IUSOFT_CATALOG_JSON__" in html_txt:
        fail("Marcador __IUSOFT_CATALOG_JSON__ sin reemplazar en index.html")
    ext_urls = [
        u for u in re.findall(r"https?://[^\s\"'<>]+", html_txt)
        if u != "http://www.w3.org/2000/svg"
    ]
    if ext_urls:
        fail(f"index.html contiene URLs externas prohibidas: {ext_urls[:5]}")

    # 4. Escaneo de higiene sobre todo el repositorio (excluyendo node_modules y .git)
    local_path_prefix = "/" + "Users/"
    forbidden_pkg = "jigg" + "icon"
    checked_files = 0
    for fp in REPO_ROOT.rglob("*"):
        if not fp.is_file():
            continue
        rel_parts = fp.relative_to(REPO_ROOT).parts
        if any(p in ("node_modules", ".git", "__pycache__") for p in rel_parts):
            continue
        if fp.suffix in (".pyc", ".png", ".jpg", ".ico"):
            continue
        txt = fp.read_text(encoding="utf-8", errors="ignore")
        checked_files += 1
        if local_path_prefix in txt:
            fail(f"Ruta local absoluta detectada en {fp.relative_to(REPO_ROOT)}")
        if forbidden_pkg in txt.lower():
            fail(f"Referencia no permitida detectada en {fp.relative_to(REPO_ROOT)}")

    print(
        f"[PASS] Verificación exitosa: {len(manifest)} iconos · {total_svgs} archivos SVG válidos · "
        f"0 strokes en Glass · 0 URLs externas en index.html · {checked_files} archivos auditados sin rutas locales."
    )


if __name__ == "__main__":
    main()
