#!/usr/bin/env python3
"""
CLI Reproducible de Construcción v2.2 con Refracción Cromática Contextual (`compiler/build_suite.py`).

Genera de forma determinista (0 tokens):
1. `icons/{glass,outline,solid,duotone}/*.svg` (1,040 archivos SVG con refracción cromática contextual de 2 canales)
2. `dist/catalog.json` (260 iconos con `palette` y `paletteLabel` clasificados por `contextual_palettes.py`)
3. `dist/iusoft-icons-react.tsx` (`<IuSoftIcon />` con `tone="contextual" | "mono"` y adaptación automática Light + Dark OLED)
4. `dist/sarchi-icons.tsx` (adaptador drop-in para los 281 componentes Sarchi POS con color contextual por defecto)
5. `index.html` (aplicación web autocontenida con conmutador `Color Contextual | Monocromo` + `Claro | OLED`)
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
import contextual_palettes as cp
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
    """Genera `dist/iusoft-icons-react.tsx` con soporte nativo para las 8 paletas contextuales (claro + OLED)."""
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
        icon_entries[slug] = {
            **item["svg"],
            "palette": item["palette"],
        }
        alias_map[slug] = slug
        alias_map[item["name"]] = slug
        alias_map[item["name"].lower()] = slug
        for al in item.get("sarchiAliases", []):
            alias_map[al] = slug
            alias_map[al.lower()] = slug

    entries_json = json.dumps(icon_entries, ensure_ascii=False, separators=(",", ":"))
    aliases_json = json.dumps(alias_map, ensure_ascii=False, separators=(",", ":"))
    palettes_json = json.dumps(cp.CONTEXTUAL_PALETTES, ensure_ascii=False, separators=(",", ":"))

    return f""""use client";

import * as React from "react";

export type IuSoftIconVariant = "glass" | "outline" | "solid" | "duotone";
export type IuSoftIconSurface = "auto" | "light" | "dark" | "emerald" | "emerald-light";
export type IuSoftIconTone = "contextual" | "mono";
export type IuSoftPaletteId =
  | "gastronomia"
  | "horno-calor"
  | "mensajeria"
  | "tesoreria"
  | "ruta-logistica"
  | "clientes-equipo"
  | "alerta-peligro"
  | "sistema-grafito";

export type IuSoftIconName =
{union_block};

export interface IuSoftIconProps extends Omit<React.SVGProps<SVGSVGElement>, "name"> {{
  name: IuSoftIconName;
  variant?: IuSoftIconVariant;
  surface?: IuSoftIconSurface;
  tone?: IuSoftIconTone;
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
  palette: IuSoftPaletteId;
}}

interface DualChannelStops {{
  obsBack: [string, string];
  glass: [string, string, string, string];
  obsFront: [string, string];
  bevel: [string, string, string];
}}

export const CONTEXTUAL_PALETTES: Record<
  IuSoftPaletteId,
  {{ label: string; light: DualChannelStops; dark: DualChannelStops }}
> = {palettes_json};

export const IUSOFT_SURFACE_TOKENS: Record<Exclude<IuSoftIconSurface, "auto">, Record<string, string>> = {{
  light: {{
    "--iusoft-obs-back-top": "#5B5B5E",
    "--iusoft-obs-back-bottom": "#161617",
    "--iusoft-obs-front-top": "#5B5B5E",
    "--iusoft-obs-front-bottom": "#161617",
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
    "--iusoft-obs-back-top": "#FAFAFA",
    "--iusoft-obs-back-bottom": "#A1A1AA",
    "--iusoft-obs-front-top": "#FAFAFA",
    "--iusoft-obs-front-bottom": "#A1A1AA",
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
    "--iusoft-obs-back-top": "#4ADE80",
    "--iusoft-obs-back-bottom": "#10B981",
    "--iusoft-obs-front-top": "#ECFDF5",
    "--iusoft-obs-front-bottom": "#6EE7B7",
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
    "--iusoft-obs-back-top": "#0D7A5C",
    "--iusoft-obs-back-bottom": "#052E16",
    "--iusoft-obs-front-top": "#0D7A5C",
    "--iusoft-obs-front-bottom": "#052E16",
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
 * Cascada automática de superficie (`light` <-> `dark` OLED) respetando la paleta contextual de cada icono (`--ic-l-*` / `--ic-d-*`).
 */
export const IUSOFT_SURFACE_CSS = `
svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: var(--ic-l-ob0, #5B5B5E);
  --iusoft-obs-back-bottom: var(--ic-l-ob1, #161617);
  --iusoft-obs-front-top: var(--ic-l-of0, #5B5B5E);
  --iusoft-obs-front-bottom: var(--ic-l-of1, #161617);
  --iusoft-glass-top: var(--ic-l-g0, #D4D4D8);
  --iusoft-glass-top-op: var(--ic-l-gop0, 0.68);
  --iusoft-glass-bottom: var(--ic-l-g1, #A1A1AA);
  --iusoft-glass-bottom-op: var(--ic-l-gop1, 0.64);
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: var(--ic-l-bop0, 0.96);
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: var(--ic-l-bop1, 0.28);
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: var(--ic-l-bop2, 0.06);
}}
:is(.dark, [data-theme="dark"], [data-iusoft-surface="dark"], [data-driver-portal], .driver-pwa, .bg-primary, [class*="bg-[#18181B]"], [class*="bg-[#09090B]"], [class*="bg-zinc-900"], [class*="bg-zinc-950"]) svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: var(--ic-d-ob0, #FAFAFA);
  --iusoft-obs-back-bottom: var(--ic-d-ob1, #A1A1AA);
  --iusoft-obs-front-top: var(--ic-d-of0, #FAFAFA);
  --iusoft-obs-front-bottom: var(--ic-d-of1, #A1A1AA);
  --iusoft-glass-top: var(--ic-d-g0, #71717A);
  --iusoft-glass-top-op: var(--ic-d-gop0, 0.56);
  --iusoft-glass-bottom: var(--ic-d-g1, #3F3F46);
  --iusoft-glass-bottom-op: var(--ic-d-gop1, 0.52);
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: var(--ic-d-bop0, 0.94);
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: var(--ic-d-bop1, 0.34);
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: var(--ic-d-bop2, 0.10);
}}
:is(.dark .bg-primary, [data-theme="dark"] .bg-primary, [data-driver-portal] [class*="bg-[var(--driver-primary)]"], [data-driver-portal] [class*="bg-[#FAFAFA]"], [data-driver-portal] .bg-white, [data-iusoft-surface="light"]) svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: var(--ic-l-ob0, #5B5B5E);
  --iusoft-obs-back-bottom: var(--ic-l-ob1, #161617);
  --iusoft-obs-front-top: var(--ic-l-of0, #5B5B5E);
  --iusoft-obs-front-bottom: var(--ic-l-of1, #161617);
  --iusoft-glass-top: var(--ic-l-g0, #D4D4D8);
  --iusoft-glass-top-op: var(--ic-l-gop0, 0.68);
  --iusoft-glass-bottom: var(--ic-l-g1, #A1A1AA);
  --iusoft-glass-bottom-op: var(--ic-l-gop1, 0.64);
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: var(--ic-l-bop0, 0.96);
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: var(--ic-l-bop1, 0.28);
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: var(--ic-l-bop2, 0.06);
}}
[data-iusoft-surface="emerald"] svg[data-iusoft-glass],
[class*="bg-[#052E16]"] svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: #4ADE80;
  --iusoft-obs-back-bottom: #10B981;
  --iusoft-obs-front-top: #ECFDF5;
  --iusoft-obs-front-bottom: #6EE7B7;
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
[data-iusoft-surface="emerald-light"] svg[data-iusoft-glass],
[class*="bg-[#E7F8EE]"] svg[data-iusoft-glass],
[class*="bg-[#22C55E]"] svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: #0D7A5C;
  --iusoft-obs-back-bottom: #052E16;
  --iusoft-obs-front-top: #0D7A5C;
  --iusoft-obs-front-bottom: #052E16;
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
[class*="bg-[#0D7A5C]"] svg[data-iusoft-glass],
[class*="bg-[#16A34A]"] svg[data-iusoft-glass] {{
  --iusoft-obs-back-top: #FFFFFF;
  --iusoft-obs-back-bottom: #D1FAE5;
  --iusoft-obs-front-top: #FFFFFF;
  --iusoft-obs-front-bottom: #D1FAE5;
  --iusoft-glass-top: #6EE7B7;
  --iusoft-glass-top-op: 0.46;
  --iusoft-glass-bottom: #047857;
  --iusoft-glass-bottom-op: 0.48;
  --iusoft-bevel-top: #FFFFFF;
  --iusoft-bevel-top-op: 0.94;
  --iusoft-bevel-mid: #FFFFFF;
  --iusoft-bevel-mid-op: 0.28;
  --iusoft-bevel-bottom: #FFFFFF;
  --iusoft-bevel-bottom-op: 0.08;
}}
`;

let surfaceCssInjected = false;
function ensureSurfaceStyles() {{
  if (surfaceCssInjected || typeof document === "undefined") return;
  surfaceCssInjected = true;
  const existing = document.getElementById("iusoft-surface-css");
  if (existing) {{
    existing.textContent = IUSOFT_SURFACE_CSS;
    return;
  }}
  const styleEl = document.createElement("style");
  styleEl.id = "iusoft-surface-css";
  styleEl.textContent = IUSOFT_SURFACE_CSS;
  document.head.appendChild(styleEl);
}}

function buildDualModeVarMap(l: DualChannelStops, d: DualChannelStops): Record<string, string> {{
  return {{
    "--ic-l-ob0": l.obsBack[0],
    "--ic-l-ob1": l.obsBack[1],
    "--ic-l-g0": l.glass[0],
    "--ic-l-gop0": l.glass[1],
    "--ic-l-g1": l.glass[2],
    "--ic-l-gop1": l.glass[3],
    "--ic-l-of0": l.obsFront[0],
    "--ic-l-of1": l.obsFront[1],
    "--ic-l-bop0": l.bevel[0],
    "--ic-l-bop1": l.bevel[1],
    "--ic-l-bop2": l.bevel[2],
    "--ic-d-ob0": d.obsBack[0],
    "--ic-d-ob1": d.obsBack[1],
    "--ic-d-g0": d.glass[0],
    "--ic-d-gop0": d.glass[1],
    "--ic-d-g1": d.glass[2],
    "--ic-d-gop1": d.glass[3],
    "--ic-d-of0": d.obsFront[0],
    "--ic-d-of1": d.obsFront[1],
    "--ic-d-bop0": d.bevel[0],
    "--ic-d-bop1": d.bevel[1],
    "--ic-d-bop2": d.bevel[2],
  }};
}}

const MONO_STOPS_LIGHT: DualChannelStops = {{
  obsBack: ["#5B5B5E", "#161617"],
  glass: ["#D4D4D8", "0.68", "#A1A1AA", "0.64"],
  obsFront: ["#5B5B5E", "#161617"],
  bevel: ["0.96", "0.28", "0"],
}};

const MONO_STOPS_DARK: DualChannelStops = {{
  obsBack: ["#FAFAFA", "#A1A1AA"],
  glass: ["#71717A", "0.56", "#3F3F46", "0.52"],
  obsFront: ["#FAFAFA", "#A1A1AA"],
  bevel: ["0.94", "0.32", "0.08"],
}};

function buildDirectStopsStyle(s: DualChannelStops): Record<string, string> {{
  return {{
    "--iusoft-obs-back-top": s.obsBack[0],
    "--iusoft-obs-back-bottom": s.obsBack[1],
    "--iusoft-obs-front-top": s.obsFront[0],
    "--iusoft-obs-front-bottom": s.obsFront[1],
    "--iusoft-glass-top": s.glass[0],
    "--iusoft-glass-top-op": s.glass[1],
    "--iusoft-glass-bottom": s.glass[2],
    "--iusoft-glass-bottom-op": s.glass[3],
    "--iusoft-bevel-top": "#FFFFFF",
    "--iusoft-bevel-top-op": s.bevel[0],
    "--iusoft-bevel-mid": "#FFFFFF",
    "--iusoft-bevel-mid-op": s.bevel[1],
    "--iusoft-bevel-bottom": "#FFFFFF",
    "--iusoft-bevel-bottom-op": s.bevel[2],
  }};
}}

const ICON_DATA: Record<string, IconVariants> = {entries_json};
const ICON_ALIASES: Record<string, string> = {aliases_json};

export const IUSOFT_ICON_SLUGS = Object.keys(ICON_DATA);

export const IuSoftIcon = React.forwardRef<SVGSVGElement, IuSoftIconProps>(function IuSoftIcon(
  {{
    name,
    variant = "glass",
    surface = "auto",
    tone = "contextual",
    size = 24,
    strokeWidth: _ignoredStrokeWidth,
    animate = "hover",
    className,
    style,
    onMouseEnter,
    ...svgProps
  }},
  forwardedRef
) {{
  const rawId = React.useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const pfx = `iusoft-${{rawId}}`;
  const svgRef = React.useRef<SVGSVGElement | null>(null);
  const rafRef = React.useRef<number | null>(null);

  const setMergedRef = React.useCallback(
    (node: SVGSVGElement | null) => {{
      svgRef.current = node;
      if (typeof forwardedRef === "function") forwardedRef(node);
      else if (forwardedRef) (forwardedRef as React.MutableRefObject<SVGSVGElement | null>).current = node;
    }},
    [forwardedRef]
  );

  const useSafeInsertion = typeof React.useInsertionEffect === "function" ? React.useInsertionEffect : React.useEffect;
  useSafeInsertion(() => {{
    ensureSurfaceStyles();
  }}, []);

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
  const mergedClassName = ["lucide", `lucide-${{slug}}`, className].filter(Boolean).join(" ");

  if (variant === "glass") {{
    const g = entry.glass;
    const bevelD = g.inner !== undefined ? (g.inner ? `${{g.glass}} ${{g.inner}}` : g.glass) : (g.bevel || g.glass);
    const palSpec = CONTEXTUAL_PALETTES[entry.palette] || CONTEXTUAL_PALETTES["sistema-grafito"];
    const lStops = tone === "mono" ? MONO_STOPS_LIGHT : palSpec.light;
    const dStops = tone === "mono" ? MONO_STOPS_DARK : palSpec.dark;

    let tokenVars: Record<string, string>;
    if (surface === "auto") {{
      tokenVars = buildDualModeVarMap(lStops, dStops);
    }} else if (surface === "light") {{
      tokenVars = {{ ...buildDualModeVarMap(lStops, dStops), ...buildDirectStopsStyle(lStops) }};
    }} else if (surface === "dark") {{
      tokenVars = {{ ...buildDualModeVarMap(lStops, dStops), ...buildDirectStopsStyle(dStops) }};
    }} else {{
      tokenVars = {{ ...buildDualModeVarMap(lStops, dStops), ...IUSOFT_SURFACE_TOKENS[surface] }};
    }}

    const mergedStyle: React.CSSProperties = {{
      flexShrink: 0,
      ...tokenVars,
      ...style,
    }} as React.CSSProperties;

    return (
      <svg
        ref={{setMergedRef}}
        xmlns="http://www.w3.org/2000/svg"
        width={{size}}
        height={{size}}
        viewBox="0 0 24 24"
        fill="none"
        data-iusoft-glass={{"true"}}
        data-iusoft-palette={{entry.palette}}
        className={{mergedClassName}}
        style={{mergedStyle}}
        onMouseEnter={{handleMouseEnter}}
        {{...svgProps}}
      >
        <defs>
          <linearGradient id={{`${{pfx}}-obs-back`}} x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor={{lStops.obsBack[0]}} style={{{{ stopColor: `var(--iusoft-obs-back-top, ${{lStops.obsBack[0]}})` }}}} />
            <stop offset="100%" stopColor={{lStops.obsBack[1]}} style={{{{ stopColor: `var(--iusoft-obs-back-bottom, ${{lStops.obsBack[1]}})` }}}} />
          </linearGradient>
          <linearGradient id={{`${{pfx}}-obs-front`}} x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor={{lStops.obsFront[0]}} style={{{{ stopColor: `var(--iusoft-obs-front-top, ${{lStops.obsFront[0]}})` }}}} />
            <stop offset="100%" stopColor={{lStops.obsFront[1]}} style={{{{ stopColor: `var(--iusoft-obs-front-bottom, ${{lStops.obsFront[1]}})` }}}} />
          </linearGradient>
          <linearGradient id={{`${{pfx}}-glass`}} x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">
            <stop
              offset="0%"
              stopColor={{lStops.glass[0]}}
              stopOpacity={{lStops.glass[1]}}
              style={{{{
                stopColor: `var(--iusoft-glass-top, ${{lStops.glass[0]}})`,
                stopOpacity: `var(--iusoft-glass-top-op, ${{lStops.glass[1]}})`,
              }}}}
            />
            <stop
              offset="100%"
              stopColor={{lStops.glass[2]}}
              stopOpacity={{lStops.glass[3]}}
              style={{{{
                stopColor: `var(--iusoft-glass-bottom, ${{lStops.glass[2]}})`,
                stopOpacity: `var(--iusoft-glass-bottom-op, ${{lStops.glass[3]}})`,
              }}}}
            />
          </linearGradient>
          <linearGradient id={{`${{pfx}}-bevel`}} x1="12" y1={{g.y1}} x2="12" y2={{g.y2}} gradientUnits="userSpaceOnUse">
            <stop
              offset="0%"
              stopColor="#FFFFFF"
              stopOpacity={{lStops.bevel[0]}}
              style={{{{ stopColor: "var(--iusoft-bevel-top, #FFFFFF)", stopOpacity: `var(--iusoft-bevel-top-op, ${{lStops.bevel[0]}})` }}}}
            />
            <stop
              offset="58%"
              stopColor="#FFFFFF"
              stopOpacity={{lStops.bevel[1]}}
              style={{{{ stopColor: "var(--iusoft-bevel-mid, #FFFFFF)", stopOpacity: `var(--iusoft-bevel-mid-op, ${{lStops.bevel[1]}})` }}}}
            />
            <stop
              offset="100%"
              stopColor="#FFFFFF"
              stopOpacity={{lStops.bevel[2]}}
              style={{{{ stopColor: "var(--iusoft-bevel-bottom, #FFFFFF)", stopOpacity: `var(--iusoft-bevel-bottom-op, ${{lStops.bevel[2]}})` }}}}
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
              <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs-back)`}} />
            ))}}
          </g>
        </g>
        <g mask={{`url(#${{pfx}}-in)`}}>
          <g filter={{`url(#${{pfx}}-blur)`}}>
            <g className="iusoft-back-xf">
              {{g.back.map((d, i) => (
                <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs-back)`}} />
              ))}}
            </g>
          </g>
        </g>
        <g className="iusoft-glass-xf">
          <path d={{g.glass}} fill={{`url(#${{pfx}}-glass)`}} />
          <path d={{bevelD}} fill={{`url(#${{pfx}}-bevel)`}} fillRule="evenodd" />
          {{g.front.map((d, i) => (
            <path key={{i}} d={{d}} fill={{`url(#${{pfx}}-obs-front)`}} />
          ))}}
        </g>
      </svg>
    );
  }}

  const rawInner = entry[variant];
  return (
    <svg
      ref={{setMergedRef}}
      xmlns="http://www.w3.org/2000/svg"
      width={{size}}
      height={{size}}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={{mergedClassName}}
      style={{{{ flexShrink: 0, ...style }}}}
      onMouseEnter={{handleMouseEnter}}
      {{...svgProps}}
    >
      <g className="iusoft-whole-xf" dangerouslySetInnerHTML={{{{ __html: rawInner }}}} />
    </svg>
  );
}});
"""


def generate_sarchi_adapter_tsx(catalog: list[dict]) -> str:
    """Genera `dist/sarchi-icons.tsx`: adaptador drop-in compatible con `lucide-react` con color contextual activo."""
    micro_outline_slugs = {
        "loader-2",
        "check",
        "check-check",
        "x",
        "plus",
        "minus",
        "chevron-right",
        "chevron-left",
        "chevron-down",
        "chevron-up",
        "chevrons-up-down",
        "more-horizontal",
        "more-vertical",
        "grip-vertical",
        "arrow-up-down",
    }
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
                is_micro = item["slug"] in micro_outline_slugs or "loader" in item["slug"]
                default_var = '"outline"' if is_micro else "undefined"
                exported_identifiers.append(
                    f'export const {sym}: SarchiLucideIcon = createSarchiIcon("{item["slug"]}", "{sym}", {default_var});'
                )

    exports_block = "\n".join(exported_identifiers)
    return f""""use client";

import * as React from "react";
import {{
  IuSoftIcon,
  CONTEXTUAL_PALETTES,
  IUSOFT_SURFACE_CSS,
  IUSOFT_SURFACE_TOKENS,
  type IuSoftIconName,
  type IuSoftIconSurface,
  type IuSoftIconTone,
  type IuSoftIconVariant,
  type IuSoftPaletteId,
}} from "./iusoft-icons-react";

export {{ IuSoftIcon, CONTEXTUAL_PALETTES, IUSOFT_SURFACE_CSS, IUSOFT_SURFACE_TOKENS }};
export type {{ IuSoftIconName, IuSoftIconSurface, IuSoftIconTone, IuSoftIconVariant, IuSoftPaletteId }};

export interface LucideProps extends Omit<React.SVGProps<SVGSVGElement>, "name"> {{
  size?: string | number;
  strokeWidth?: string | number;
  absoluteStrokeWidth?: boolean;
  variant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  tone?: IuSoftIconTone;
  animate?: "hover" | "none";
}}

export type SarchiLucideIcon = React.ForwardRefExoticComponent<
  LucideProps & React.RefAttributes<SVGSVGElement>
>;
export type LucideIcon = SarchiLucideIcon;

interface SarchiIconContextValue {{
  defaultVariant: IuSoftIconVariant | "auto";
  surface: IuSoftIconSurface;
  tone: IuSoftIconTone;
}}

const SarchiIconContext = React.createContext<SarchiIconContextValue>({{
  defaultVariant: "auto",
  surface: "auto",
  tone: "contextual",
}});

export interface SarchiIconProviderProps {{
  defaultVariant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  tone?: IuSoftIconTone;
  children: React.ReactNode;
}}

export function SarchiIconProvider({{
  defaultVariant = "auto",
  surface = "auto",
  tone = "contextual",
  children,
}}: SarchiIconProviderProps) {{
  const value = React.useMemo(
    () => ({{ defaultVariant, surface, tone }}),
    [defaultVariant, surface, tone]
  );
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

  // Regla GPU y nitidez Sarchi: iconos compactos (size <= 15 o clases size/w/h 0.5..3.5 / px) usan outline 0-blur
  if (typeof size === "number" && size <= 15) return "outline";
  if (/\\b(?:size|w|h)-(?:0\\.5|1(?:\\.5)?|2(?:\\.5)?|3(?:\\.5)?|px)\\b/.test(cls)) return "outline";
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
      tone,
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
    const resolvedTone = tone || ctx.tone;
    return (
      <IuSoftIcon
        ref={{_ref}}
        name={{slug}}
        variant={{resolvedVariant}}
        surface={{resolvedSurface}}
        tone={{resolvedTone}}
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

// === 281 Símbolos Drop-In Compatibles con `lucide-react` para Sarchi Pizza POS ===
{exports_block}
"""


def write_icon_svg_files(slug: str, svg_data: dict, palette_id: str = "sistema-grafito"):
    for variant in ("glass", "outline", "solid", "duotone"):
        vdir = ICONS_DIR / variant
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / f"{slug}.svg").write_text(
            glass_compiler.render_standalone_svg(slug, variant, svg_data, palette_id=palette_id),
            encoding="utf-8",
        )


def build_catalog_entry(meta: dict, svg_data: dict) -> dict:
    palette_id = cp.classify_icon_palette(meta)
    palette_spec = cp.CONTEXTUAL_PALETTES[palette_id]
    return {
        "id": meta["id"],
        "slug": meta["slug"],
        "name": meta["name"],
        "label": meta["label"],
        "origin": meta["origin"],
        "source": meta["sourceGroup"],
        "sourceLabel": meta["sourceLabel"],
        "category": meta["category"],
        "palette": palette_id,
        "paletteLabel": palette_spec["label"],
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
    compact_palettes = json.dumps(cp.CONTEXTUAL_PALETTES, ensure_ascii=False, separators=(",", ":"))
    rendered = template.replace("__IUSOFT_CATALOG_JSON__", compact_catalog, 1)
    rendered = rendered.replace("__IUSOFT_PALETTES_JSON__", compact_palettes)
    INDEX_HTML_PATH.write_text(rendered, encoding="utf-8")


def recolor_from_existing_catalog():
    """Actualiza en <2s los 1,040 SVGs, catalog.json, SDK React e index.html usando la geometría ya compilada."""
    t0 = time.time()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    existing = {x["slug"]: x["svg"] for x in json.loads(CATALOG_PATH.read_text(encoding="utf-8"))}
    catalog = []
    counts = {}
    for m in manifest:
        svg_data = existing[m["slug"]]
        entry = build_catalog_entry(m, svg_data)
        write_icon_svg_files(m["slug"], svg_data, palette_id=entry["palette"])
        catalog.append(entry)
        counts[entry["palette"]] = counts.get(entry["palette"], 0) + 1
    regenerate_outputs(catalog)
    print(
        f"[OK] 260 iconos × 4 estilos = 1,040 SVGs recoloreados por contexto en {time.time() - t0:.2f}s · Distribución: {counts}"
    )


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
    parser = argparse.ArgumentParser(description="Compilador reproducible v2.2 de IU-SOFT Icons")
    parser.add_argument("--only", type=str, default=None, help="Compila únicamente el icono indicado en <1s")
    parser.add_argument("--recolor-only", action="store_true", help="Reasigna paletas contextuales y regenera SVGs/SDK/Web en <2s")
    parser.add_argument("--workers", type=int, default=8, help="Número de procesos paralelos para compilación completa")
    parser.add_argument("--worker-shard", nargs=2, type=int, metavar=("IDX", "TOTAL"), help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker_shard is not None:
        run_worker(args.worker_shard[0], args.worker_shard[1])
        return

    if args.recolor_only:
        recolor_from_existing_catalog()
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
            entry = build_catalog_entry(m, svg_data)
            write_icon_svg_files(m["slug"], svg_data, palette_id=entry["palette"])
            compiled_updates[m["slug"]] = entry

        if CATALOG_PATH.exists():
            existing = {x["slug"]: x for x in json.loads(CATALOG_PATH.read_text(encoding="utf-8"))}
            existing.update(compiled_updates)
            ordered = [existing[m["slug"]] for m in manifest if m["slug"] in existing]
            regenerate_outputs(ordered)
        print(
            f"[OK] Recompilado incremental ({', '.join(compiled_updates.keys())}) en {time.time() - t0:.2f}s"
        )
        return

    print("[Build] Generando 6 iconos artesanales desde compiler/domain_dsl.py...")
    domain_icons = domain_dsl.build_domain_icons()

    phos_slugs = sorted({m["phosphorSlug"] for m in manifest if m["origin"] == "phosphor-0-token"})
    print(f"[Build] Compilando {len(phos_slugs)} iconos v2.2 desde node_modules/@phosphor-icons/core en {args.workers} procesos...")
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
        entry = build_catalog_entry(m, svg_data)
        write_icon_svg_files(m["slug"], svg_data, palette_id=entry["palette"])
        catalog.append(entry)

    regenerate_outputs(catalog)
    print(
        f"[SUCCESS] {len(catalog)} iconos × 4 estilos = {len(catalog) * 4} SVGs escritos en icons/, "
        f"dist/ e index.html en {time.time() - t0:.1f}s"
    )


if __name__ == "__main__":
    main()
