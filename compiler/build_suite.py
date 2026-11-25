#!/usr/bin/env python3
"""
CLI Reproducible de Construcción v2 (`compiler/build_suite.py`).

Genera de forma determinista:
1. `icons/{glass,outline,solid,duotone}/*.svg` (972 archivos SVG autocontenidos con `--iusoft-*`)
2. `dist/catalog.json` (catálogo completo de 243 iconos)
3. `dist/iusoft-icons-react.tsx` (`<IuSoftIcon />` con soporte `surface="auto|light|dark|emerald|emerald-light"`)
4. `dist/sarchi-icons.tsx` (adaptador drop-in 100% compatible con `lucide-react` para los 215+ símbolos de Sarchi POS,
   con presupuesto GPU inteligente y soporte automático para SARCHI-UI v3, `/driver` OLED y `/pedir`)
5. `index.html` (aplicación web autocontenida de librería)
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time

COMPILER_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = COMPILER_DIR.parent

sys.path.insert(0, str(COMPILER_DIR))
import domain_dsl
import glass_compiler

MANIFEST_PATH = COMPILER_DIR / "manifest.json"
TEMPLATE_PATH = COMPILER_DIR / "template.html"
ICONS_DIR = REPO_ROOT / "icons"
DIST_DIR = REPO_ROOT / "dist"
CATALOG_PATH = DIST_DIR / "catalog.json"
REACT_TSX_PATH = DIST_DIR / "iusoft-icons-react.tsx"
SARCHI_TSX_PATH = DIST_DIR / "sarchi-icons.tsx"
INDEX_HTML_PATH = REPO_ROOT / "index.html"

JS_IDENT_RE = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def generate_react_component_tsx(catalog: list[dict]) -> str:
    """Genera el componente React/TypeScript autocontenido con soporte multi-superficie (`light`/`dark`/`emerald`)."""
    union_tokens = []
    seen = set()
    for item in catalog:
        for key in [item["name"], item["slug"]] + item.get("sarchiAliases", []):
            if key and key not in seen:
                seen.add(key)
                union_tokens.append(f'  | "{key}"')
    union_block = "\n".join(union_tokens)

    icon_entries = {}
    alias_map = {}
    for item in catalog:
        slug = item["slug"]
        icon_entries[slug] = item["svg"]
        alias_map[slug] = slug
        alias_map[item["name"]] = slug
        alias_map[item["name"].lower()] = slug
        for al in item.get("sarchiAliases", []):
            alias_map[al] = slug
            alias_map[al.lower()] = slug

    entries_json = json.dumps(icon_entries, ensure_ascii=False, separators=(",", ":"))
    aliases_json = json.dumps(alias_map, ensure_ascii=False, separators=(",", ":"))

    return f"""import * as React from "react";

export type IuSoftIconVariant = "glass" | "outline" | "solid" | "duotone";
export type IuSoftIconSurface = "auto" | "light" | "dark" | "emerald" | "emerald-light";

export type IuSoftIconName =
{union_block};

export interface IuSoftIconProps extends Omit<React.SVGProps<SVGSVGElement>, "name"> {{
  name: IuSoftIconName;
  variant?: IuSoftIconVariant;
  surface?: IuSoftIconSurface;
  size?: number | string;
  strokeWidth?: number | string;
  animate?: "hover" | "none";
}}

interface GlassGeometry {{
  back: string[];
  glass: string;
  inner?: string;
  bevel?: string;
  front: string[];
  y1: number;
  y2: number;
}}

interface IconVariants {{
  glass: GlassGeometry;
  outline: string;
  solid: string;
  duotone: string;
}}

export const IUSOFT_SURFACE_TOKENS: Record<Exclude<IuSoftIconSurface, "auto">, Record<string, string>> = {{
  light: {{
    "--iusoft-obs-top": "#5B5B5E",
    "--iusoft-obs-bottom": "#161617",
    "--iusoft-glass-top": "#D4D4D8",
    "--iusoft-glass-top-op": "0.68",
    "--iusoft-glass-bottom": "#A1A1AA",
    "--iusoft-glass-bottom-op": "0.64",
    "--iusoft-bevel-top": "#FFFFFF",
    "--iusoft-bevel-top-op": "0.96",
    "--iusoft-bevel-mid": "#FFFFFF",
    "--iusoft-bevel-mid-op": "0.28",
    "--iusoft-bevel-bottom": "#FFFFFF",
    "--iusoft-bevel-bottom-op": "0",
  }},
  dark: {{
    "--iusoft-obs-top": "#FAFAFA",
    "--iusoft-obs-bottom": "#A1A1AA",
    "--iusoft-glass-top": "#71717A",
    "--iusoft-glass-top-op": "0.56",
    "--iusoft-glass-bottom": "#3F3F46",
    "--iusoft-glass-bottom-op": "0.52",
    "--iusoft-bevel-top": "#FFFFFF",
    "--iusoft-bevel-top-op": "0.94",
    "--iusoft-bevel-mid": "#FFFFFF",
    "--iusoft-bevel-mid-op": "0.32",
    "--iusoft-bevel-bottom": "#FFFFFF",
    "--iusoft-bevel-bottom-op": "0.08",
  }},
  emerald: {{
    "--iusoft-obs-top": "#4ADE80",
    "--iusoft-obs-bottom": "#10B981",
    "--iusoft-glass-top": "#10B981",
    "--iusoft-glass-top-op": "0.42",
    "--iusoft-glass-bottom": "#065F46",
    "--iusoft-glass-bottom-op": "0.56",
    "--iusoft-bevel-top": "#ECFDF5",
    "--iusoft-bevel-top-op": "0.94",
    "--iusoft-bevel-mid": "#A7F3D0",
    "--iusoft-bevel-mid-op": "0.30",
    "--iusoft-bevel-bottom": "#6EE7B7",
    "--iusoft-bevel-bottom-op": "0.10",
  }},
  "emerald-light": {{
    "--iusoft-obs-top": "#0D7A5C",
    "--iusoft-obs-bottom": "#052E16",
    "--iusoft-glass-top": "#6EE7B7",
    "--iusoft-glass-top-op": "0.58",
    "--iusoft-glass-bottom": "#10B981",
    "--iusoft-glass-bottom-op": "0.48",
    "--iusoft-bevel-top": "#FFFFFF",
    "--iusoft-bevel-top-op": "0.96",
    "--iusoft-bevel-mid": "#FFFFFF",
    "--iusoft-bevel-mid-op": "0.28",
    "--iusoft-bevel-bottom": "#FFFFFF",
    "--iusoft-bevel-bottom-op": "0",
  }},
}};

/**
 * Hoja CSS opcional para activar cascada automática en contenedores oscuros (`.dark`, `/driver`, `[data-iusoft-surface]`).
 */
export const IUSOFT_SURFACE_CSS = `
.dark, [data-iusoft-surface="dark"], .driver-pwa {{
  --iusoft-obs-top: #FAFAFA;
  --iusoft-obs-bottom: #A1A1AA;
  --iusoft-glass-top: #71717A;
  --iusoft-glass-top-op: 0.56;
  --iusoft-glass-bottom: #3F3F46;
  --iusoft-glass-bottom-op: 0.52;
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: 0.94;
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: 0.32;
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: 0.08;
}}
[data-iusoft-surface="emerald"] {{
  --iusoft-obs-top: #4ADE80;
  --iusoft-obs-bottom: #10B981;
  --iusoft-glass-top: #10B981;
  --iusoft-glass-top-op: 0.42;
  --iusoft-glass-bottom: #065F46;
  --iusoft-glass-bottom-op: 0.56;
  --iusoft-bevel-top: #ECFDF5;
  --iusoft-bevel-top-op: 0.94;
  --iusoft-bevel-mid: #A7F3D0;
  --iusoft-bevel-mid-op: 0.30;
  --iusoft-bevel-bottom: #6EE7B7;
  --iusoft-bevel-bottom-op: 0.10;
}}
[data-iusoft-surface="emerald-light"] {{
  --iusoft-obs-top: #0D7A5C;
  --iusoft-obs-bottom: #052E16;
  --iusoft-glass-top: #6EE7B7;
  --iusoft-glass-top-op: 0.58;
  --iusoft-glass-bottom: #10B981;
  --iusoft-glass-bottom-op: 0.48;
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: 0.96;
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: 0.28;
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: 0;
}}
`;

const ICON_DATA: Record<string, IconVariants> = {entries_json};
const ICON_ALIASES: Record<string, string> = {aliases_json};

export const IUSOFT_ICON_SLUGS = Object.keys(ICON_DATA);

export function IuSoftIcon({{
  name,
  variant = "glass",
  surface = "auto",
  size = 24,
  strokeWidth: _ignoredStrokeWidth,
  animate = "hover",
  style,
  onMouseEnter,
  ...svgProps
}}: IuSoftIconProps) {{
  const rawId = React.useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const pfx = `iusoft-${{rawId}}`;
  const svgRef = React.useRef<SVGSVGElement | null>(null);
  const rafRef = React.useRef<number | null>(null);

  React.useEffect(() => {{
    return () => {{
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    }};
  }}, []);

  const triggerSpring = React.useCallback(() => {{
    if (animate === "none" || typeof window === "undefined") return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const svg = svgRef.current;
    if (!svg) return;
    if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);

    const glassNodes = svg.querySelectorAll(".iusoft-glass-xf");
    const backNodes = svg.querySelectorAll(".iusoft-back-xf");
    const wholeNode = svg.querySelector(".iusoft-whole-xf");

    let pos = 1.0;
    let vel = 3.8;
    const k = 290;
    const c = 14.5;
    let last = performance.now();

    const frame = (now: number) => {{
      const dt = Math.min((now - last) / 1000, 0.032);
      last = now;
      vel += (-k * pos - c * vel) * dt;
      pos += vel * dt;

      if (Math.abs(pos) < 0.003 && Math.abs(vel) < 0.015) {{
        glassNodes.forEach((n) => n.removeAttribute("transform"));
        backNodes.forEach((n) => n.removeAttribute("transform"));
        if (wholeNode) wholeNode.removeAttribute("transform");
        rafRef.current = null;
        return;
      }}

      if (glassNodes.length > 0) {{
        const dy = (-1.15 * pos).toFixed(3);
        const rot = (-3.2 * pos).toFixed(3);
        const bdy = (0.35 * pos).toFixed(3);
        glassNodes.forEach((n) => n.setAttribute("transform", `translate(0 ${{dy}}) rotate(${{rot}} 12 12)`));
        backNodes.forEach((n) => n.setAttribute("transform", `translate(0 ${{bdy}})`));
      }} else if (wholeNode) {{
        const sc = (1 + 0.08 * pos).toFixed(3);
        const rot = (-3.5 * pos).toFixed(3);
        wholeNode.setAttribute("transform", `translate(12 12) rotate(${{rot}}) scale(${{sc}}) translate(-12 -12)`);
      }}
      rafRef.current = requestAnimationFrame(frame);
    }};

    rafRef.current = requestAnimationFrame(frame);
  }}, [animate]);

  const handleMouseEnter = (e: React.MouseEvent<SVGSVGElement>) => {{
    triggerSpring();
    if (onMouseEnter) onMouseEnter(e);
  }};

  const slug = ICON_ALIASES[name] || ICON_ALIASES[String(name).toLowerCase()];
  const entry = slug ? ICON_DATA[slug] : undefined;
  if (!entry) return null;

  if (variant === "glass") {{
    const g = entry.glass;
    const bevelD = g.inner !== undefined ? (g.inner ? `${{g.glass}} ${{g.inner}}` : g.glass) : (g.bevel || g.glass);
    const mergedStyle: React.CSSProperties | undefined =
      surface === "auto"
        ? style
        : ({{ ...IUSOFT_SURFACE_TOKENS[surface], ...style }} as React.CSSProperties);

    return (
      <svg
        ref={{svgRef}}
        xmlns="http://www.w3.org/2000/svg"
        width={{size}}
        height={{size}}
        viewBox="0 0 24 24"
        fill="none"
        style={{mergedStyle}}
        onMouseEnter={{handleMouseEnter}}
        {{...svgProps}}
      >
        <defs>
          <linearGradient id={{`${{pfx}}-obs`}} x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#5B5B5E" style={{{{ stopColor: "var(--iusoft-obs-top, #5B5B5E)" }}}} />
            <stop offset="100%" stopColor="#161617" style={{{{ stopColor: "var(--iusoft-obs-bottom, #161617)" }}}} />
          </linearGradient>
          <linearGradient id={{`${{pfx}}-glass`}} x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">
            <stop
              offset="0%"
              stopColor="#D4D4D8"
              stopOpacity="0.68"
              style={{{{ stopColor: "var(--iusoft-glass-top, #D4D4D8)", stopOpacity: "var(--iusoft-glass-top-op, 0.68)" }}}}
            />
            <stop
              offset="100%"
              stopColor="#A1A1AA"
              stopOpacity="0.64"
              style={{{{ stopColor: "var(--iusoft-glass-bottom, #A1A1AA)", stopOpacity: "var(--iusoft-glass-bottom-op, 0.64)" }}}}
            />
          </linearGradient>
          <linearGradient id={{`${{pfx}}-bevel`}} x1="12" y1={{g.y1}} x2="12" y2={{g.y2}} gradientUnits="userSpaceOnUse">
            <stop
              offset="0%"
              stopColor="#FFFFFF"
              stopOpacity="0.96"
              style={{{{ stopColor: "var(--iusoft-bevel-top, #FFFFFF)", stopOpacity: "var(--iusoft-bevel-top-op, 0.96)" }}}}
            />
            <stop
              offset="58%"
              stopColor="#FFFFFF"
              stopOpacity="0.28"
              style={{{{ stopColor: "var(--iusoft-bevel-mid, #FFFFFF)", stopOpacity: "var(--iusoft-bevel-mid-op, 0.28)" }}}}
            />
            <stop
              offset="100%"
              stopColor="#FFFFFF"
              stopOpacity="0"
              style={{{{ stopColor: "var(--iusoft-bevel-bottom, #FFFFFF)", stopOpacity: "var(--iusoft-bevel-bottom-op, 0)" }}}}
            />
          </linearGradient>
          <filter id={{`${{pfx}}-blur`}} x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox">
            <feGaussianBlur stdDeviation="1.6" />
          </filter>
          <mask id={{`${{pfx}}-out`}} maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="-8" y="-8" width="40" height="40">
            <rect x="-8" y="-8" width="40" height="40" fill="#ffffff" />
            <g className="iusoft-glass-xf">
              <path d={{g.glass}} fill="#000000" />
            </g>
          </mask>
          <mask id={{`${{pfx}}-in`}} maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="-8" y="-8" width="40" height="40">
            <rect x="-8" y="-8" width="40" height="40" fill="#000000" />
            <g className="iusoft-glass-xf">
              <path d={{g.glass}} fill="#ffffff" />
            </g>
          </mask>
        </defs>
        <g mask={{`url(#${{pfx}}-out)`}}>
          <g className="iusoft-back-xf">
            {{g.back.map((d, i) => (
              <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs)`}} />
            ))}}
          </g>
        </g>
        <g mask={{`url(#${{pfx}}-in)`}}>
          <g filter={{`url(#${{pfx}}-blur)`}}>
            <g className="iusoft-back-xf">
              {{g.back.map((d, i) => (
                <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs)`}} />
              ))}}
            </g>
          </g>
        </g>
        <g className="iusoft-glass-xf">
          <path d={{g.glass}} fill={{`url(#${{pfx}}-glass)`}} />
          <path d={{bevelD}} fill={{`url(#${{pfx}}-bevel)`}} fillRule="evenodd" />
          {{g.front.map((d, i) => (
            <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs)`}} />
          ))}}
        </g>
      </svg>
    );
  }}

  const rawInner = entry[variant];
  return (
    <svg
      ref={{svgRef}}
      xmlns="http://www.w3.org/2000/svg"
      width={{size}}
      height={{size}}
      viewBox="0 0 24 24"
      fill="currentColor"
      style={{style}}
      onMouseEnter={{handleMouseEnter}}
      {{...svgProps}}
    >
      <g className="iusoft-whole-xf" dangerouslySetInnerHTML={{{{ __html: rawInner }}}} />
    </svg>
  );
}}
"""


def generate_sarchi_adapter_tsx(catalog: list[dict]) -> str:
    """Genera `dist/sarchi-icons.tsx`: adaptador drop-in compatible con `lucide-react` para Sarchi Pizza POS."""
    exported_identifiers = []
    seen = set()
    for item in catalog:
        candidates = []
        if JS_IDENT_RE.match(item["name"]) and item["name"][0].isupper():
            candidates.append(item["name"])
        for al in item.get("sarchiAliases", []):
            if JS_IDENT_RE.match(al) and al[0].isupper():
                candidates.append(al)
        for sym in candidates:
            if sym not in seen:
                seen.add(sym)
                is_spinner = "loader" in item["slug"]
                default_var = '"outline"' if is_spinner else "undefined"
                exported_identifiers.append(
                    f'export const {sym}: SarchiLucideIcon = createSarchiIcon("{item["slug"]}", "{sym}", {default_var});'
                )

    exports_block = "\n".join(exported_identifiers)
    return f"""import * as React from "react";
import {{
  IuSoftIcon,
  IUSOFT_SURFACE_CSS,
  IUSOFT_SURFACE_TOKENS,
  type IuSoftIconName,
  type IuSoftIconSurface,
  type IuSoftIconVariant,
}} from "./iusoft-icons-react";

export {{ IuSoftIcon, IUSOFT_SURFACE_CSS, IUSOFT_SURFACE_TOKENS }};
export type {{ IuSoftIconName, IuSoftIconSurface, IuSoftIconVariant }};

/**
 * Propiedades 100% compatibles con `lucide-react` (`LucideProps`) + extensiones Glass/Superficie de Sarchi POS.
 */
export interface LucideProps extends Omit<React.SVGProps<SVGSVGElement>, "name"> {{
  size?: string | number;
  strokeWidth?: string | number;
  absoluteStrokeWidth?: boolean;
  variant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  animate?: "hover" | "none";
}}

export type SarchiLucideIcon = React.ForwardRefExoticComponent<
  LucideProps & React.RefAttributes<SVGSVGElement>
>;
export type LucideIcon = SarchiLucideIcon;

interface SarchiIconContextValue {{
  defaultVariant: IuSoftIconVariant | "auto";
  surface: IuSoftIconSurface;
}}

const SarchiIconContext = React.createContext<SarchiIconContextValue>({{
  defaultVariant: "auto",
  surface: "auto",
}});

export interface SarchiIconProviderProps {{
  /**
   * - `"auto"` (recomendado): `glass` en tamaños >= 18px (Sidebar, Headers, KPIs, Empty States) y `outline` ligero en
   *   controles compactos (`<= 16px`), spinners (`animate-spin`) o dentro de botones sólidos.
   * - `"glass"` / `"outline"` / `"solid"` / `"duotone"`: fuerza variante global salvo override por prop.
   */
  defaultVariant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  children: React.ReactNode;
}}

export function SarchiIconProvider({{
  defaultVariant = "auto",
  surface = "auto",
  children,
}}: SarchiIconProviderProps) {{
  const value = React.useMemo(() => ({{ defaultVariant, surface }}), [defaultVariant, surface]);
  return (
    <SarchiIconContext.Provider value={{value}}>
      <style dangerouslySetInnerHTML={{{{ __html: IUSOFT_SURFACE_CSS }}}} />
      {{children}}
    </SarchiIconContext.Provider>
  );
}}

function resolveSmartVariant(
  explicitVariant: IuSoftIconVariant | "auto" | undefined,
  ctxVariant: IuSoftIconVariant | "auto",
  forcedDefault: IuSoftIconVariant | undefined,
  size: string | number | undefined,
  className: string | undefined
): IuSoftIconVariant {{
  if (explicitVariant && explicitVariant !== "auto") return explicitVariant;
  if (forcedDefault) return forcedDefault;
  const cls = className || "";
  if (cls.includes("animate-spin")) return "outline";
  const targetMode = explicitVariant || ctxVariant;
  if (targetMode !== "auto") return targetMode;

  // Regla GPU Sarchi: iconos compactos (size <= 15 o clases size-3 / size-3.5 / w-3 / h-3) usan outline 0-blur
  if (typeof size === "number" && size <= 15) return "outline";
  if (/\\b(size-3(?:\\.5)?|[wh]-3(?:\\.5)?)\\b/.test(cls)) return "outline";
  return "glass";
}}

function createSarchiIcon(
  slug: IuSoftIconName,
  displayName: string,
  forcedDefault?: IuSoftIconVariant
): SarchiLucideIcon {{
  const Comp = React.forwardRef<SVGSVGElement, LucideProps>(function SarchiBoundIcon(
    {{
      variant,
      surface,
      size = 24,
      className,
      strokeWidth: _sw,
      absoluteStrokeWidth: _asw,
      animate = "hover",
      ...rest
    }},
    _ref
  ) {{
    const ctx = React.useContext(SarchiIconContext);
    const resolvedVariant = resolveSmartVariant(variant, ctx.defaultVariant, forcedDefault, size, className);
    const resolvedSurface = surface || ctx.surface;
    return (
      <IuSoftIcon
        name={{slug}}
        variant={{resolvedVariant}}
        surface={{resolvedSurface}}
        size={{size}}
        className={{className}}
        animate={{clsHasSpin(className) ? "none" : animate}}
        {{...rest}}
      />
    );
  }});
  Comp.displayName = displayName;
  return Comp;
}}

function clsHasSpin(cls?: string): boolean {{
  return Boolean(cls && cls.includes("animate-spin"));
}}

// === 215+ Símbolos Drop-In Compatibles con `lucide-react` para Sarchi Pizza POS ===
{exports_block}
"""


def write_icon_svg_files(slug: str, svg_data: dict):
    for variant in ("glass", "outline", "solid", "duotone"):
        vdir = ICONS_DIR / variant
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / f"{slug}.svg").write_text(
            glass_compiler.render_standalone_svg(slug, variant, svg_data),
            encoding="utf-8",
        )


def build_catalog_entry(meta: dict, svg_data: dict) -> dict:
    return {
        "id": meta["id"],
        "slug": meta["slug"],
        "name": meta["name"],
        "label": meta["label"],
        "origin": meta["origin"],
        "source": meta["sourceGroup"],
        "sourceLabel": meta["sourceLabel"],
        "category": meta["category"],
        "phosphorSlug": meta.get("phosphorSlug"),
        "inSarchi": meta["inPos"],
        "sarchiUses": meta["posUses"],
        "sarchiAliases": meta.get("lucideAliases", []),
        "sarchiModules": meta.get("posModules", []),
        "keywords": meta["keywords"],
        "svg": svg_data,
    }


def regenerate_outputs(catalog: list[dict]):
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REACT_TSX_PATH.write_text(generate_react_component_tsx(catalog), encoding="utf-8")
    SARCHI_TSX_PATH.write_text(generate_sarchi_adapter_tsx(catalog), encoding="utf-8")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert "__IUSOFT_CATALOG_JSON__" in template, "Falta el marcador __IUSOFT_CATALOG_JSON__ en compiler/template.html"
    compact_catalog = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    INDEX_HTML_PATH.write_text(template.replace("__IUSOFT_CATALOG_JSON__", compact_catalog, 1), encoding="utf-8")


def run_worker(worker_idx: int, num_workers: int):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    phos_slugs = sorted({m["phosphorSlug"] for m in manifest if m["origin"] == "phosphor-0-token"})
    shard = [s for idx, s in enumerate(phos_slugs) if idx % num_workers == worker_idx]
    out = {}
    for s in shard:
        out[s] = glass_compiler.compile_phosphor_slug(s)
    tmp_fp = DIST_DIR / f"_shard_{worker_idx}.json"
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    tmp_fp.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compilador reproducible v2 de IU-SOFT Icons")
    parser.add_argument("--only", type=str, default=None, help="Compila únicamente el icono indicado (<slug>, nombre o phosphorSlug) en <1s")
    parser.add_argument("--workers", type=int, default=8, help="Número de procesos paralelos para compilación completa")
    parser.add_argument("--worker-shard", nargs=2, type=int, metavar=("IDX", "TOTAL"), help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker_shard is not None:
        run_worker(args.worker_shard[0], args.worker_shard[1])
        return

    t0 = time.time()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if args.only:
        target_q = args.only.strip().lower()
        matches = [
            m for m in manifest
            if target_q in (
                m["slug"].lower(),
                m["name"].lower(),
                (m.get("phosphorSlug") or "").lower(),
                (m.get("dslKey") or "").lower(),
            )
        ]
        if not matches:
            raise SystemExit(f"[ERROR] No existe ningún icono '{args.only}' en compiler/manifest.json")

        domain_icons = None
        compiled_updates = {}
        for m in matches:
            if m["origin"] == "domain-dsl":
                if domain_icons is None:
                    domain_icons = domain_dsl.build_domain_icons()
                svg_data = domain_icons[m["dslKey"]]
            else:
                svg_data = glass_compiler.compile_phosphor_slug(m["phosphorSlug"])
            write_icon_svg_files(m["slug"], svg_data)
            compiled_updates[m["slug"]] = build_catalog_entry(m, svg_data)

        if CATALOG_PATH.exists():
            existing = {x["slug"]: x for x in json.loads(CATALOG_PATH.read_text(encoding="utf-8"))}
            existing.update(compiled_updates)
            ordered = [existing[m["slug"]] for m in manifest if m["slug"] in existing]
            regenerate_outputs(ordered)
        print(
            f"[OK] Recompilado incremental ({', '.join(compiled_updates.keys())}) -> "
            f"4 SVGs + dist/catalog.json + dist/iusoft-icons-react.tsx + dist/sarchi-icons.tsx + index.html en {time.time() - t0:.2f}s"
        )
        return

    print("[Build] Generando 6 iconos artesanales desde compiler/domain_dsl.py...")
    domain_icons = domain_dsl.build_domain_icons()

    phos_slugs = sorted({m["phosphorSlug"] for m in manifest if m["origin"] == "phosphor-0-token"})
    print(f"[Build] Compilando {len(phos_slugs)} iconos v2 desde node_modules/@phosphor-icons/core en {args.workers} procesos...")
    procs = [
        subprocess.Popen([sys.executable, str(pathlib.Path(__file__).resolve()), "--worker-shard", str(k), str(args.workers)])
        for k in range(args.workers)
    ]
    for p in procs:
        rc = p.wait()
        if rc != 0:
            raise RuntimeError(f"Subproceso compilador terminó con código {rc}")

    compiled_phos = {}
    for k in range(args.workers):
        sfp = DIST_DIR / f"_shard_{k}.json"
        compiled_phos.update(json.loads(sfp.read_text(encoding="utf-8")))
        sfp.unlink()

    catalog = []
    for m in manifest:
        if m["origin"] == "domain-dsl":
            svg_data = domain_icons[m["dslKey"]]
        else:
            svg_data = compiled_phos[m["phosphorSlug"]]
        write_icon_svg_files(m["slug"], svg_data)
        catalog.append(build_catalog_entry(m, svg_data))

    regenerate_outputs(catalog)
    print(
        f"[SUCCESS] {len(catalog)} iconos × 4 estilos = {len(catalog) * 4} SVGs escritos en icons/, "
        f"dist/ (incluyendo sarchi-icons.tsx) e index.html en {time.time() - t0:.1f}s"
    )


if __name__ == "__main__":
    main()
