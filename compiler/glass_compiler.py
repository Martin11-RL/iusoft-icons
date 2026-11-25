#!/usr/bin/env python3
"""
Compilador Geométrico Determinista 0-Tokens (`compiler/glass_compiler.py`).

Transforma cualquier icono vectorial estándar de `@phosphor-icons/core` (`MIT`, `viewBox="0 0 256 256"`,
trazo equivalente `16 u`, medio trazo `8 u === 0.75 u` en `24×24`) en sus 4 estilos `viewBox="0 0 24 24"`:
- `glass` (4 capas ópticas sin `stroke`: obsidiana exterior, refracción `feGaussianBlur`, cristal y bisel `evenodd` 0.75 u)
- `outline` (trazo regular escalado exacto a `1.5 u`)
- `solid` (relleno sólido `fill`)
- `duotone` (doble tono `fill-opacity="0.2"` + contorno principal)

Etapas matemáticas del motor Glass:
1. Parseo completo de comandos `<path d="...">` (`M,L,H,V,C,S,Q,T,A,Z`) y rasterización supermuestreada `4x` (`1536×1536` -> `384×384`).
2. Transformada de Distancia Euclidiana Exacta 2D (`EDT` lineal `O(N)` de Felzenszwalb-Huttenlocher) con proyección al punto frontera más cercano.
3. Clasificación topológica automática (cero `if` por nombre de icono):
   - Patrón A (`perimeter_coverage >= 0.89`): Vasijas bordeadas con absorción del trazo perimetral `G_glass = dilate(P_seed, +8 u)`, preservación de cavidades multicontorno y extrusión normal de `18 u` bajo el cristal para refracción real.
   - Patrón B (`perimeter_coverage < 0.89`): Placas de fondo abiertas donde `P_primary` se conserva 100% íntegro y nítido en `front`.
   - Patrón C (`< 900 px` de obsidiana expuesta o sin `P_seed`): Alternancia 50/50 en siluetas multi-pieza o placa *squircle* `rx=5` con glifo centrado al `72%`.
4. Extracción sub-píxel por Marching Squares + suavizado sin encogimiento de Taubin (`λ=0.33, μ=-0.34`) + simplificación Ramer-Douglas-Peucker + ajuste de curvas de Bézier cúbicas `C¹`.
"""

import math
import pathlib
import re
import xml.etree.ElementTree as ET
from array import array
from collections import deque
from PIL import Image, ImageChops, ImageDraw

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PHOSPHOR_ASSETS = REPO_ROOT / "node_modules" / "@phosphor-icons" / "core" / "assets"

GRID = 384
SCALE_GRID = GRID / 256.0          # 1.5 px por unidad de 256
SS_SCALE = 4                       # 1536x1536 supermuestreo antialiasing 4x4
TO_24 = 24.0 / GRID                # 0.0625 u por px de rejilla
PHOS_TO_24 = 24.0 / 256.0          # 0.09375 (escala directa 256 -> 24)
HALF_STROKE_PX = 8.0 * SCALE_GRID  # 12.0 px == 8 u en 256 == 0.75 u exactos en 24x24
INF = 1e12

TOKEN_RE = re.compile(r"[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")

SQUIRCLE_OUTER = (
    "M 7.75 2.75 L 16.25 2.75 A 5 5 0 0 1 21.25 7.75 L 21.25 16.25 "
    "A 5 5 0 0 1 16.25 21.25 L 7.75 21.25 A 5 5 0 0 1 2.75 16.25 "
    "L 2.75 7.75 A 5 5 0 0 1 7.75 2.75 Z"
)
SQUIRCLE_INNER = (
    "M 7.75 3.5 L 16.25 3.5 A 4.25 4.25 0 0 1 20.5 7.75 L 20.5 16.25 "
    "A 4.25 4.25 0 0 1 16.25 20.5 L 7.75 20.5 A 4.25 4.25 0 0 1 3.5 16.25 "
    "L 3.5 7.75 A 4.25 4.25 0 0 1 7.75 3.5 Z"
)


def f3(v: float) -> str:
    if abs(v) < 1e-6:
        return "0"
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def scale_svg_path_d(d_str: str, scale: float = PHOS_TO_24, tx: float = 0.0, ty: float = 0.0) -> str:
    """Escala y traslada analíticamente cualquier `<path d='...'>` SVG sin pérdida de curvas."""
    tokens = TOKEN_RE.findall(d_str)
    out = []
    i = 0
    n = len(tokens)
    cmd = ""
    first_move = True

    def is_cmd(t: str) -> bool:
        return len(t) == 1 and t.isalpha()

    def nf() -> float:
        nonlocal i
        v = float(tokens[i])
        i += 1
        return v

    def nflag() -> str:
        nonlocal i
        tok = tokens[i]
        if tok in ("0", "1"):
            i += 1
            return tok
        val = tok[0]
        rest = tok[1:]
        if rest:
            tokens[i] = rest
        else:
            i += 1
        return val

    while i < n:
        if is_cmd(tokens[i]):
            cmd = tokens[i]
            out.append("M" if (cmd == "m" and first_move) else cmd)
            i += 1
            if cmd in ("Z", "z"):
                cmd = ""
                continue
        if cmd == "M":
            first_move = False
            out.extend([f3(nf() * scale + tx), f3(nf() * scale + ty)])
            cmd = "L"
        elif cmd == "m":
            if first_move:
                first_move = False
                out.extend([f3(nf() * scale + tx), f3(nf() * scale + ty)])
            else:
                out.extend([f3(nf() * scale), f3(nf() * scale)])
            cmd = "l"
        elif cmd in ("L", "T"):
            out.extend([f3(nf() * scale + tx), f3(nf() * scale + ty)])
        elif cmd in ("l", "t"):
            out.extend([f3(nf() * scale), f3(nf() * scale)])
        elif cmd == "H":
            out.append(f3(nf() * scale + tx))
        elif cmd == "h":
            out.append(f3(nf() * scale))
        elif cmd == "V":
            out.append(f3(nf() * scale + ty))
        elif cmd == "v":
            out.append(f3(nf() * scale))
        elif cmd == "C":
            for _ in range(3):
                out.extend([f3(nf() * scale + tx), f3(nf() * scale + ty)])
        elif cmd == "c":
            for _ in range(6):
                out.append(f3(nf() * scale))
        elif cmd in ("S", "Q"):
            for _ in range(2):
                out.extend([f3(nf() * scale + tx), f3(nf() * scale + ty)])
        elif cmd in ("s", "q"):
            for _ in range(4):
                out.append(f3(nf() * scale))
        elif cmd == "A":
            rx = nf() * scale
            ry = nf() * scale
            rot = nf()
            la = nflag()
            sw = nflag()
            x = nf() * scale + tx
            y = nf() * scale + ty
            out.extend([f3(rx), f3(ry), f3(rot), la, sw, f3(x), f3(y)])
        elif cmd == "a":
            rx = nf() * scale
            ry = nf() * scale
            rot = nf()
            la = nflag()
            sw = nflag()
            x = nf() * scale
            y = nf() * scale
            out.extend([f3(rx), f3(ry), f3(rot), la, sw, f3(x), f3(y)])
        else:
            break
    return " ".join(out)


def arc_to_points(x1, y1, rx, ry, phi_deg, large_arc, sweep, x2, y2, steps_per_rad=18):
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [(x2, y2)]
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg % 360.0)
    cp, sp = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p = cp * dx2 + sp * dy2
    y1p = -sp * dx2 + cp * dy2
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1.0:
        sq = math.sqrt(lam)
        rx *= sq
        ry *= sq
    num = max(0.0, rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p)
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    rad = math.sqrt(num / den) if den > 1e-12 else 0.0
    if large_arc == sweep:
        rad = -rad
    cxp = rad * (rx * y1p / ry)
    cyp = rad * (-ry * x1p / rx)
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2.0
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2.0

    def vec_angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        ln = math.hypot(ux, uy) * math.hypot(vx, vy)
        ang = math.acos(max(-1.0, min(1.0, dot / ln))) if ln > 1e-12 else 0.0
        return -ang if (ux * vy - uy * vx) < 0 else ang

    ux, uy = (x1p - cxp) / rx, (y1p - cyp) / ry
    vx, vy = (-x1p - cxp) / rx, (-y1p - cyp) / ry
    theta1 = vec_angle(1.0, 0.0, ux, uy)
    dtheta = vec_angle(ux, uy, vx, vy)
    if sweep == 0 and dtheta > 0:
        dtheta -= 2.0 * math.pi
    elif sweep == 1 and dtheta < 0:
        dtheta += 2.0 * math.pi

    n_steps = max(4, int(math.ceil(abs(dtheta) * steps_per_rad)))
    pts = []
    for k in range(1, n_steps + 1):
        th = theta1 + dtheta * (k / n_steps)
        ct, st = math.cos(th), math.sin(th)
        pts.append((cp * rx * ct - sp * ry * st + cx, sp * rx * ct + cp * ry * st + cy))
    return pts


def parse_svg_subpaths(d_str: str):
    tokens = TOKEN_RE.findall(d_str)
    subpaths, curr = [], []
    i, n = 0, len(tokens)
    cx = cy = sx = sy = 0.0
    cmd = None
    prev_ctrl = None

    def is_cmd(t):
        return len(t) == 1 and t.isalpha()

    def nf():
        nonlocal i
        v = float(tokens[i])
        i += 1
        return v

    def nflag():
        nonlocal i
        tok = tokens[i]
        if tok in ("0", "1"):
            i += 1
            return int(tok)
        val = int(tok[0])
        rest = tok[1:]
        if rest:
            tokens[i] = rest
        else:
            i += 1
        return val

    while i < n:
        if is_cmd(tokens[i]):
            cmd = tokens[i]
            i += 1
        if cmd in ("Z", "z"):
            if len(curr) >= 3:
                subpaths.append(curr)
            curr = []
            cx, cy = sx, sy
            prev_ctrl = None
            cmd = None
            continue
        if cmd in ("M", "m"):
            x, y = nf(), nf()
            if len(curr) >= 3:
                subpaths.append(curr)
            cx, cy = (x, y) if cmd == "M" else (cx + x, cy + y)
            sx, sy = cx, cy
            curr = [(cx, cy)]
            prev_ctrl = None
            cmd = "L" if cmd == "M" else "l"
        elif cmd in ("L", "l"):
            x, y = nf(), nf()
            cx, cy = (x, y) if cmd == "L" else (cx + x, cy + y)
            curr.append((cx, cy))
            prev_ctrl = None
        elif cmd in ("H", "h"):
            x = nf()
            cx = x if cmd == "H" else cx + x
            curr.append((cx, cy))
            prev_ctrl = None
        elif cmd in ("V", "v"):
            y = nf()
            cy = y if cmd == "V" else cy + y
            curr.append((cx, cy))
            prev_ctrl = None
        elif cmd in ("C", "c"):
            x1, y1, x2, y2, x3, y3 = nf(), nf(), nf(), nf(), nf(), nf()
            if cmd == "c":
                x1 += cx
                y1 += cy
                x2 += cx
                y2 += cy
                x3 += cx
                y3 += cy
            for k in range(1, 17):
                t = k / 16.0
                mt = 1.0 - t
                curr.append((
                    mt ** 3 * cx + 3 * mt ** 2 * t * x1 + 3 * mt * t ** 2 * x2 + t ** 3 * x3,
                    mt ** 3 * cy + 3 * mt ** 2 * t * y1 + 3 * mt * t ** 2 * y2 + t ** 3 * y3,
                ))
            prev_ctrl = (x2, y2)
            cx, cy = x3, y3
        elif cmd in ("S", "s"):
            x1 = 2 * cx - prev_ctrl[0] if prev_ctrl else cx
            y1 = 2 * cy - prev_ctrl[1] if prev_ctrl else cy
            x2, y2, x3, y3 = nf(), nf(), nf(), nf()
            if cmd == "s":
                x2 += cx
                y2 += cy
                x3 += cx
                y3 += cy
            for k in range(1, 17):
                t = k / 16.0
                mt = 1.0 - t
                curr.append((
                    mt ** 3 * cx + 3 * mt ** 2 * t * x1 + 3 * mt * t ** 2 * x2 + t ** 3 * x3,
                    mt ** 3 * cy + 3 * mt ** 2 * t * y1 + 3 * mt * t ** 2 * y2 + t ** 3 * y3,
                ))
            prev_ctrl = (x2, y2)
            cx, cy = x3, y3
        elif cmd in ("Q", "q"):
            x1, y1, x2, y2 = nf(), nf(), nf(), nf()
            if cmd == "q":
                x1 += cx
                y1 += cy
                x2 += cx
                y2 += cy
            for k in range(1, 15):
                t = k / 14.0
                mt = 1.0 - t
                curr.append((mt * mt * cx + 2 * mt * t * x1 + t * t * x2, mt * mt * cy + 2 * mt * t * y1 + t * t * y2))
            prev_ctrl = (x1, y1)
            cx, cy = x2, y2
        elif cmd in ("A", "a"):
            rx, ry, rot = nf(), nf(), nf()
            la, sw = nflag(), nflag()
            x2, y2 = nf(), nf()
            if cmd == "a":
                x2 += cx
                y2 += cy
            curr.extend(arc_to_points(cx, cy, rx, ry, rot, la, sw, x2, y2))
            cx, cy = x2, y2
            prev_ctrl = None
        else:
            break
    if len(curr) >= 3:
        subpaths.append(curr)
    return subpaths


def rasterize_subpaths_aa(subpaths):
    hi = GRID * SS_SCALE
    sc = SCALE_GRID * SS_SCALE
    acc = Image.new("1", (hi, hi), 0)
    for sp in subpaths:
        layer = Image.new("1", (hi, hi), 0)
        ImageDraw.Draw(layer).polygon([(p[0] * sc, p[1] * sc) for p in sp], fill=1)
        acc = ImageChops.logical_xor(acc, layer)
    return acc.convert("L").resize((GRID, GRID), resample=Image.Resampling.BOX)


def edt_1d(f_arr, n):
    v = [0] * n
    z = [0.0] * (n + 1)
    z[0], z[1] = -INF, INF
    k = 0
    has_seed = f_arr[0] < INF
    for q in range(1, n):
        fq = f_arr[q]
        if fq >= INF:
            continue
        has_seed = True
        while True:
            vk = v[k]
            fvk = f_arr[vk]
            if fvk >= INF:
                k = 0
                v[0] = q
                z[0] = -INF
                z[1] = INF
                break
            s = ((fq + q * q) - (fvk + vk * vk)) / (2.0 * (q - vk))
            if s <= z[k]:
                k -= 1
                if k < 0:
                    k = 0
                    v[0] = q
                    z[0] = -INF
                    z[1] = INF
                    break
            else:
                k += 1
                v[k] = q
                z[k] = s
                z[k + 1] = INF
                break
    if not has_seed:
        return [INF] * n
    out = [INF] * n
    k = 0
    for q in range(n):
        while z[k + 1] < q:
            k += 1
        vk = v[k]
        d = q - vk
        out[q] = d * d + f_arr[vk]
    return out


def edt_1d_proj(f_arr, idx_arr, n):
    v = [0] * n
    z = [0.0] * (n + 1)
    z[0], z[1] = -INF, INF
    k = 0
    has_seed = f_arr[0] < INF
    for q in range(1, n):
        fq = f_arr[q]
        if fq >= INF:
            continue
        has_seed = True
        while True:
            vk = v[k]
            fvk = f_arr[vk]
            if fvk >= INF:
                k = 0
                v[0] = q
                z[0] = -INF
                z[1] = INF
                break
            s = ((fq + q * q) - (fvk + vk * vk)) / (2.0 * (q - vk))
            if s <= z[k]:
                k -= 1
                if k < 0:
                    k = 0
                    v[0] = q
                    z[0] = -INF
                    z[1] = INF
                    break
            else:
                k += 1
                v[k] = q
                z[k] = s
                z[k + 1] = INF
                break
    if not has_seed:
        return [INF] * n, [0] * n
    out_d = [INF] * n
    out_i = [0] * n
    k = 0
    for q in range(n):
        while z[k + 1] < q:
            k += 1
        vk = v[k]
        d = q - vk
        out_d[q] = d * d + f_arr[vk]
        out_i[q] = idx_arr[vk]
    return out_d, out_i


def compute_edt_only(mask_bool, w=GRID, h=GRID):
    n_tot = w * h
    f_grid = [0.0 if mask_bool[i] else INF for i in range(n_tot)]
    tmp = [INF] * n_tot
    for y in range(h):
        ro = y * w
        row = f_grid[ro : ro + w]
        if min(row) < INF:
            tmp[ro : ro + w] = edt_1d(row, w)
    res = array("d", [1e6] * n_tot)
    col = [0.0] * h
    for x in range(w):
        for y in range(h):
            col[y] = tmp[y * w + x]
        if min(col) < INF:
            d2 = edt_1d(col, h)
            for y in range(h):
                if d2[y] < INF:
                    res[y * w + x] = math.sqrt(d2[y])
    return res


def compute_sdf_full(cov_bytes, need_proj=False, w=GRID, h=GRID):
    n_tot = w * h
    f_out = [INF] * n_tot
    f_in = [INF] * n_tot
    for idx in range(n_tot):
        c = cov_bytes[idx]
        if c == 255:
            f_out[idx] = 0.0
        elif c == 0:
            f_in[idx] = 0.0
        else:
            a = c / 255.0
            do = max(0.0, 0.5 - a)
            di = max(0.0, a - 0.5)
            f_out[idx] = do * do
            f_in[idx] = di * di

    tmp_out = [INF] * n_tot
    for y in range(h):
        ro = y * w
        row = f_out[ro : ro + w]
        if min(row) < INF:
            tmp_out[ro : ro + w] = edt_1d(row, w)
    d_out = array("d", [1e6] * n_tot)
    col = [0.0] * h
    for x in range(w):
        for y in range(h):
            col[y] = tmp_out[y * w + x]
        if min(col) < INF:
            d2 = edt_1d(col, h)
            for y in range(h):
                if d2[y] < INF:
                    d_out[y * w + x] = math.sqrt(d2[y])

    d_in = array("d", [1e6] * n_tot)
    proj_in = array("I", range(n_tot)) if need_proj else None

    if need_proj:
        tmp_in = [INF] * n_tot
        tmp_idx = list(range(n_tot))
        for y in range(h):
            ro = y * w
            row = f_in[ro : ro + w]
            if min(row) < INF:
                ir = list(range(ro, ro + w))
                od, oi = edt_1d_proj(row, ir, w)
                tmp_in[ro : ro + w] = od
                tmp_idx[ro : ro + w] = oi
        ci = [0] * h
        for x in range(w):
            for y in range(h):
                col[y] = tmp_in[y * w + x]
                ci[y] = tmp_idx[y * w + x]
            if min(col) < INF:
                od, oi = edt_1d_proj(col, ci, h)
                for y in range(h):
                    if od[y] < INF:
                        d_in[y * w + x] = math.sqrt(od[y])
                        proj_in[y * w + x] = oi[y]
    else:
        tmp_in = [INF] * n_tot
        for y in range(h):
            ro = y * w
            row = f_in[ro : ro + w]
            if min(row) < INF:
                tmp_in[ro : ro + w] = edt_1d(row, w)
        for x in range(w):
            for y in range(h):
                col[y] = tmp_in[y * w + x]
            if min(col) < INF:
                d2 = edt_1d(col, h)
                for y in range(h):
                    if d2[y] < INF:
                        d_in[y * w + x] = math.sqrt(d2[y])

    sdf = array("d", [0.0] * n_tot)
    for idx in range(n_tot):
        c = cov_bytes[idx]
        if c >= 128:
            sdf[idx] = -d_in[idx] if c == 255 else (0.5 - c / 255.0)
        else:
            sdf[idx] = d_out[idx] if c == 0 else (0.5 - c / 255.0)
    return sdf, d_out, d_in, proj_in


def connected_components(mask_bool, w=GRID, h=GRID):
    vis = bytearray(w * h)
    comps = []
    for s in range(w * h):
        if mask_bool[s] and not vis[s]:
            q = deque([s])
            vis[s] = 1
            pxs = []
            while q:
                u = q.popleft()
                pxs.append(u)
                ux, uy = u % w, u // w
                if ux > 0 and mask_bool[u - 1] and not vis[u - 1]:
                    vis[u - 1] = 1
                    q.append(u - 1)
                if ux < w - 1 and mask_bool[u + 1] and not vis[u + 1]:
                    vis[u + 1] = 1
                    q.append(u + 1)
                if uy > 0 and mask_bool[u - w] and not vis[u - w]:
                    vis[u - w] = 1
                    q.append(u - w)
                if uy < h - 1 and mask_bool[u + w] and not vis[u + w]:
                    vis[u + w] = 1
                    q.append(u + w)
            comps.append(pxs)
    return comps


def fill_small_exterior_holes(prim_mask, glass_mask, max_area_ratio=0.012, w=GRID, h=GRID):
    """Rellena ojales exteriores diminutos sin enterrar jamás cavidades con islas internas."""
    prim_comp_id = [-1] * (w * h)
    for cid, pcomp in enumerate(connected_components(prim_mask, w, h)):
        for p in pcomp:
            prim_comp_id[p] = cid

    inv = bytearray(0 if prim_mask[i] else 1 for i in range(w * h))
    out = bytearray(prim_mask)
    max_px = int(w * h * max_area_ratio)
    for comp in connected_components(inv, w, h):
        if len(comp) > max_px:
            continue
        bad = False
        adj_cids = set()
        for p in comp:
            px, py = p % w, p // w
            if px == 0 or px == w - 1 or py == 0 or py == h - 1 or glass_mask[p]:
                bad = True
                break
            for nb in (p - 1, p + 1, p - w, p + w):
                cid = prim_comp_id[nb]
                if cid >= 0:
                    adj_cids.add(cid)
                    if len(adj_cids) > 1:
                        bad = True
                        break
            if bad:
                break
        if not bad:
            for p in comp:
                out[p] = 1
    return out


def marching_squares_loops(field, iso, w=GRID, h=GRID):
    segments, adj = {}, {}

    def qkey(pt):
        return (round(pt[0] * 1024), round(pt[1] * 1024))

    def interp(x0, y0, v0, x1, y1, v1):
        dv = v1 - v0
        t = 0.5 if abs(dv) < 1e-12 else max(0.0, min(1.0, (iso - v0) / dv))
        return (x0 + t * (x1 - x0) + 0.5, y0 + t * (y1 - y0) + 0.5)

    for y in range(h - 1):
        r0, r1 = y * w, (y + 1) * w
        for x in range(w - 1):
            v00, v10 = field[r0 + x], field[r0 + x + 1]
            v11, v01 = field[r1 + x + 1], field[r1 + x]
            case = (
                (1 if v00 <= iso else 0)
                | (2 if v10 <= iso else 0)
                | (4 if v11 <= iso else 0)
                | (8 if v01 <= iso else 0)
            )
            if case == 0 or case == 15:
                continue
            top = interp(x, y, v00, x + 1, y, v10)
            right = interp(x + 1, y, v10, x + 1, y + 1, v11)
            bot = interp(x, y + 1, v01, x + 1, y + 1, v11)
            left = interp(x, y, v00, x, y + 1, v01)
            cs = []
            if case == 1:
                cs.append((left, top))
            elif case == 2:
                cs.append((top, right))
            elif case == 3:
                cs.append((left, right))
            elif case == 4:
                cs.append((right, bot))
            elif case == 5:
                vc = 0.25 * (v00 + v10 + v11 + v01)
                cs.extend([(left, bot), (right, top)] if vc <= iso else [(left, top), (right, bot)])
            elif case == 6:
                cs.append((top, bot))
            elif case == 7:
                cs.append((left, bot))
            elif case == 8:
                cs.append((bot, left))
            elif case == 9:
                cs.append((bot, top))
            elif case == 10:
                vc = 0.25 * (v00 + v10 + v11 + v01)
                cs.extend([(top, right), (bot, left)] if vc <= iso else [(top, left), (bot, right)])
            elif case == 11:
                cs.append((bot, right))
            elif case == 12:
                cs.append((right, left))
            elif case == 13:
                cs.append((right, top))
            elif case == 14:
                cs.append((top, left))
            for pa, pb in cs:
                ka, kb = qkey(pa), qkey(pb)
                if ka != kb:
                    segments[ka] = pa
                    segments[kb] = pb
                    adj.setdefault(ka, []).append(kb)

    vis, loops = set(), []
    for sk in list(adj.keys()):
        for nk in adj[sk]:
            if (sk, nk) in vis:
                continue
            lp = [segments[sk]]
            vis.add((sk, nk))
            ck = nk
            while ck != sk:
                lp.append(segments[ck])
                ch = next((c for c in adj.get(ck, []) if (ck, c) not in vis), None)
                if ch is None:
                    break
                vis.add((ck, ch))
                ck = ch
            if len(lp) >= 6:
                loops.append(lp)
    return loops


def taubin_smooth(loop, iters=4, lam=0.33, mu=-0.34):
    pts = list(loop)
    n = len(pts)
    for _ in range(iters):
        for wf in (lam, mu):
            pts = [
                (
                    pts[i][0] + wf * (0.5 * (pts[(i - 1) % n][0] + pts[(i + 1) % n][0]) - pts[i][0]),
                    pts[i][1] + wf * (0.5 * (pts[(i - 1) % n][1] + pts[(i + 1) % n][1]) - pts[i][1]),
                )
                for i in range(n)
            ]
    return pts


def rdp_open(pts, eps):
    if len(pts) <= 2:
        return pts
    x1, y1 = pts[0]
    x2, y2 = pts[-1]
    dx, dy = x2 - x1, y2 - y1
    den = math.hypot(dx, dy)
    md, idx = -1.0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = math.hypot(px - x1, py - y1) if den < 1e-12 else abs(dy * px - dx * py + x2 * y1 - y2 * x1) / den
        if d > md:
            md, idx = d, i
    if md > eps:
        return rdp_open(pts[: idx + 1], eps)[:-1] + rdp_open(pts[idx:], eps)
    return [pts[0], pts[-1]]


def simplify_closed_loop(loop, eps=0.28):
    n = len(loop)
    i0 = min(range(n), key=lambda k: (loop[k][1], loop[k][0]))
    i1 = max(range(n), key=lambda k: math.hypot(loop[k][0] - loop[i0][0], loop[k][1] - loop[i0][1]))
    if i0 > i1:
        i0, i1 = i1, i0
    s1 = rdp_open(loop[i0 : i1 + 1], eps)
    s2 = rdp_open(loop[i1:] + loop[: i0 + 1], eps)
    m = s1[:-1] + s2[:-1]
    return m if len(m) >= 3 else loop[:3]


def loop_to_svg_bezier(pts_grid):
    n = len(pts_grid)
    if n < 3:
        return ""
    pts = [(p[0] * TO_24, p[1] * TO_24) for p in pts_grid]
    straight_min = 7.5
    seg_dirs, seg_lens, seg_line = [], [], []
    for i in range(n):
        j = (i + 1) % n
        dx = pts_grid[j][0] - pts_grid[i][0]
        dy = pts_grid[j][1] - pts_grid[i][1]
        lg = math.hypot(dx, dy)
        seg_lens.append(lg * TO_24)
        seg_dirs.append((dx / lg, dy / lg) if lg > 1e-6 else (1.0, 0.0))
        seg_line.append(lg >= straight_min)

    tangents, sharp = [], []
    for i in range(n):
        ps = (i - 1 + n) % n
        u1x, u1y = seg_dirs[ps]
        u2x, u2y = seg_dirs[i]
        ang = math.acos(max(-1.0, min(1.0, u1x * u2x + u1y * u2y)))
        if ang > math.radians(65):
            tangents.append((0.0, 0.0))
            sharp.append(True)
        elif seg_line[ps] and not seg_line[i]:
            tangents.append((u1x, u1y))
            sharp.append(False)
        elif seg_line[i] and not seg_line[ps]:
            tangents.append((u2x, u2y))
            sharp.append(False)
        else:
            tx, ty = u1x + u2x, u1y + u2y
            tl = math.hypot(tx, ty)
            tangents.append((tx / tl, ty / tl) if tl > 1e-6 else (u2x, u2y))
            sharp.append(False)

    cmds = [f"M {f3(pts[0][0])} {f3(pts[0][1])}"]
    for i in range(n):
        j = (i + 1) % n
        p0, p1 = pts[i], pts[j]
        sl = seg_lens[i]
        if sl < 1e-5:
            continue
        if seg_line[i] or (sharp[i] and sharp[j]):
            cmds.append(f"L {f3(p1[0])} {f3(p1[1])}")
        else:
            t0, t1 = tangents[i], tangents[j]
            h0 = 0.0 if sharp[i] else sl / 3.0
            h1 = 0.0 if sharp[j] else sl / 3.0
            cmds.append(
                f"C {f3(p0[0] + h0 * t0[0])} {f3(p0[1] + h0 * t0[1])} "
                f"{f3(p1[0] - h1 * t1[0])} {f3(p1[1] - h1 * t1[1])} "
                f"{f3(p1[0])} {f3(p1[1])}"
            )
    cmds.append("Z")
    return " ".join(cmds)


def field_to_paths(sdf_field, iso=0.0, smooth_iters=4, rdp_eps=0.28):
    paths = []
    for lp in marching_squares_loops(sdf_field, iso):
        per = sum(
            math.hypot(lp[(k + 1) % len(lp)][0] - lp[k][0], lp[(k + 1) % len(lp)][1] - lp[k][1])
            for k in range(len(lp))
        )
        if per < 7.5:
            continue
        d = loop_to_svg_bezier(simplify_closed_loop(taubin_smooth(lp, iters=smooth_iters), eps=rdp_eps))
        if d:
            paths.append(d)
    return paths


def compile_phosphor_slug(phos_slug: str, assets_dir: pathlib.Path = DEFAULT_PHOSPHOR_ASSETS) -> dict:
    """Compila un icono de `@phosphor-icons/core` en sus 4 variantes `24x24` (`glass`, `outline`, `solid`, `duotone`)."""
    assets_dir = pathlib.Path(assets_dir)
    duo_fp = assets_dir / "duotone" / f"{phos_slug}-duotone.svg"
    reg_fp = assets_dir / "regular" / f"{phos_slug}.svg"
    fil_fp = assets_dir / "fill" / f"{phos_slug}-fill.svg"

    if not duo_fp.exists():
        raise FileNotFoundError(
            f"No se encontró {duo_fp}. Ejecuta `npm install` para instalar @phosphor-icons/core@2.1.1."
        )

    def extract_raw_paths(fp: pathlib.Path):
        root = ET.parse(fp).getroot()
        return [
            (el.attrib.get("d", ""), el.attrib.get("opacity", "1"))
            for el in root.iter()
            if el.tag.split("}")[-1] == "path"
        ]

    reg_raw_paths = extract_raw_paths(reg_fp)
    fil_raw_paths = extract_raw_paths(fil_fp)
    duo_raw_paths = extract_raw_paths(duo_fp)

    outline_inner = "".join(f'<path d="{scale_svg_path_d(d)}" fill="currentColor"/>' for d, _ in reg_raw_paths)
    solid_inner = "".join(f'<path d="{scale_svg_path_d(d)}" fill="currentColor"/>' for d, _ in fil_raw_paths)
    duotone_inner = "".join(
        f'<path d="{scale_svg_path_d(d)}" fill="currentColor"{f" fill-opacity=\"{op}\"" if op != "1" else ""}/>'
        for d, op in duo_raw_paths
    )

    seed_sps, prim_sps, prim_d_raw = [], [], []
    for d, op in duo_raw_paths:
        sps = parse_svg_subpaths(d)
        if op == "0.2":
            seed_sps.extend(sps)
        else:
            prim_sps.extend(sps)
            prim_d_raw.append(d)

    cov_prim = rasterize_subpaths_aa(prim_sps)
    b_prim = cov_prim.tobytes()
    prim_bool = bytearray(1 if b_prim[i] >= 128 else 0 for i in range(GRID * GRID))
    use_squircle_badge = False

    if seed_sps:
        cov_seed_orig = rasterize_subpaths_aa(seed_sps)
        b_seed_orig = cov_seed_orig.tobytes()
        sdf_seed_orig, _, _, _ = compute_sdf_full(b_seed_orig, need_proj=False)
        perim_ring = [i for i in range(GRID * GRID) if abs(sdf_seed_orig[i]) <= 3.0]
        perim_cov = sum(1 for i in perim_ring if prim_bool[i]) / max(1, len(perim_ring))

        if perim_cov < 0.89:
            # Patrón B: Placa de fondo sin borde cerrado -> G_glass suavizado + 100% de P_primary nítido en front
            glass_cov = bytearray(GRID * GRID)
            glass_bool = bytearray(GRID * GRID)
            pad_px = 3.5
            for idx in range(GRID * GRID):
                val = pad_px - sdf_seed_orig[idx]
                if val >= 0.5:
                    glass_cov[idx] = 255
                    glass_bool[idx] = 1
                elif val > -0.5:
                    c = max(0, min(255, int(round((val + 0.5) * 255.0))))
                    glass_cov[idx] = c
                    if c >= 128:
                        glass_bool[idx] = 1
            sdf_glass, _, _, _ = compute_sdf_full(glass_cov, need_proj=False)
            glass_outer_paths = field_to_paths(sdf_glass, iso=0.0)
            glass_inner_paths = field_to_paths(sdf_glass, iso=-HALF_STROKE_PX)
            front_paths = [scale_svg_path_d(d, PHOS_TO_24) for d in prim_d_raw]
            back_paths = []
        else:
            # Patrón A: Vasija bordeada
            b_seed_raw = bytearray(b_seed_orig)
            inv_seed = bytearray(1 if b_seed_raw[i] < 128 else 0 for i in range(GRID * GRID))
            max_hole_px = int(GRID * GRID * 0.22)
            for hcomp in connected_components(inv_seed):
                if len(hcomp) <= max_hole_px:
                    touches_edge = any(
                        (p % GRID == 0 or p % GRID == GRID - 1 or p // GRID == 0 or p // GRID == GRID - 1)
                        for p in hcomp
                    )
                    if not touches_edge:
                        for p in hcomp:
                            b_seed_raw[p] = 255
            b_seed = bytes(b_seed_raw)
            sdf_seed, _, _, _ = compute_sdf_full(b_seed, need_proj=False)

            glass_cov = bytearray(GRID * GRID)
            glass_bool = bytearray(GRID * GRID)
            for idx in range(GRID * GRID):
                val = HALF_STROKE_PX - sdf_seed[idx]
                if val >= 0.5:
                    glass_cov[idx] = 255
                    glass_bool[idx] = 1
                elif val > -0.5:
                    c = max(0, min(255, int(round((val + 0.5) * 255.0))))
                    glass_cov[idx] = c
                    if c >= 128:
                        glass_bool[idx] = 1

            sdf_glass, _, d_in_glass, proj_in_glass = compute_sdf_full(glass_cov, need_proj=True)
            glass_outer_paths = field_to_paths(sdf_glass, iso=0.0)
            glass_inner_paths = field_to_paths(sdf_glass, iso=-HALF_STROKE_PX)

            dfg_mask = bytearray(GRID * GRID)
            deep_thresh = 18.0 * SCALE_GRID
            min_in_thresh = 2.5 * SCALE_GRID
            for comp in connected_components(prim_bool):
                max_out = max(sdf_glass[p] for p in comp)
                if max_out > 1.5 * SCALE_GRID:
                    continue
                min_in = min(d_in_glass[p] for p in comp)
                deep_cnt = sum(1 for p in comp if d_in_glass[p] > deep_thresh)
                if min_in >= min_in_thresh or (len(comp) >= 16 and (deep_cnt / len(comp)) >= 0.32):
                    for p in comp:
                        dfg_mask[p] = 1

            if any(dfg_mask):
                d_dfg = compute_edt_only(dfg_mask)
                dfg_cov = bytearray(b_prim[i] if d_dfg[i] <= 1.5 else 0 for i in range(GRID * GRID))
                sdf_dfg, _, _, _ = compute_sdf_full(dfg_cov, need_proj=False)
                front_paths = field_to_paths(sdf_dfg, iso=0.0)
            else:
                front_paths = []

            tuck_px = 18.0 * SCALE_GRID
            prim_filled = fill_small_exterior_holes(prim_bool, glass_bool, max_area_ratio=0.012)
            ext_cand = bytearray(
                1 if (prim_filled[i] and sdf_glass[i] > 1.4 * SCALE_GRID) else 0 for i in range(GRID * GRID)
            )
            valid_core = bytearray(GRID * GRID)
            for comp in connected_components(ext_cand):
                if max(sdf_glass[p] for p in comp) >= 5.0 * SCALE_GRID and len(comp) >= 10:
                    for p in comp:
                        valid_core[p] = 1

            dback_cov = bytearray(GRID * GRID)
            if any(valid_core):
                d_core = compute_edt_only(valid_core)
                p_ext_bool = bytearray(
                    1 if (prim_filled[i] and not glass_bool[i] and d_core[i] <= 2.6 * SCALE_GRID) else 0
                    for i in range(GRID * GRID)
                )
                ext_comps = connected_components(p_ext_bool)
                bridge_mask = bytearray(GRID * GRID)
                if 2 <= len(ext_comps) <= 8:
                    comp_dists = []
                    for comp in ext_comps:
                        cm = bytearray(GRID * GRID)
                        for p in comp:
                            cm[p] = 1
                        comp_dists.append(compute_edt_only(cm))
                    kc = len(comp_dists)
                    for i in range(GRID * GRID):
                        if prim_filled[i] and glass_bool[i] and d_in_glass[i] <= tuck_px and not dfg_mask[i]:
                            d1 = d2 = INF
                            for m in range(kc):
                                dm = comp_dists[m][i]
                                if dm < d1:
                                    d2 = d1
                                    d1 = dm
                                elif dm < d2:
                                    d2 = dm
                            if d1 + d2 <= 38.0 * SCALE_GRID:
                                bridge_mask[i] = 1

                union_ext = bytearray(1 if (p_ext_bool[i] or bridge_mask[i]) else 0 for i in range(GRID * GRID))
                d_to_ext = compute_edt_only(union_ext)
                for i in range(GRID * GRID):
                    if union_ext[i]:
                        dback_cov[i] = b_prim[i] if b_prim[i] >= 128 else 255
                    elif glass_bool[i] and d_in_glass[i] <= tuck_px and not dfg_mask[i]:
                        b_pt = proj_in_glass[i]
                        if d_to_ext[b_pt] <= 2.6 * SCALE_GRID and d_to_ext[i] <= tuck_px + 1.5 * SCALE_GRID:
                            dback_cov[i] = 255
                sdf_dback, _, _, _ = compute_sdf_full(dback_cov, need_proj=False)
                back_paths = field_to_paths(sdf_dback, iso=0.0)
            else:
                back_paths = []

            exposed_obs_px = sum(
                1 for i in range(GRID * GRID) if (dback_cov[i] >= 128 and not glass_bool[i]) or dfg_mask[i]
            )
            if exposed_obs_px < 900:
                # Patrón C: Siluetas cerradas sin obsidiana expuesta suficiente
                g_comps = [c for c in connected_components(glass_bool) if len(c) >= 64]
                if len(g_comps) >= 2:
                    g_comps_sorted = sorted(
                        g_comps,
                        key=lambda c: (
                            round((sum(p // GRID for p in c) / len(c)) / 48.0),
                            sum(p % GRID for p in c) / len(c),
                        ),
                    )
                    obs_indices = {0, 3} if len(g_comps_sorted) == 4 else {k for k in range(len(g_comps_sorted)) if k % 2 == 0}
                    obs_set = set()
                    for k in obs_indices:
                        obs_set.update(g_comps_sorted[k])
                    dback_cov = bytearray(glass_cov[i] if i in obs_set else 0 for i in range(GRID * GRID))
                    glass_cov = bytearray(0 if i in obs_set else glass_cov[i] for i in range(GRID * GRID))
                    glass_bool = bytearray(1 if glass_cov[i] >= 128 else 0 for i in range(GRID * GRID))
                    sdf_glass, _, _, _ = compute_sdf_full(glass_cov, need_proj=False)
                    glass_outer_paths = field_to_paths(sdf_glass, iso=0.0)
                    glass_inner_paths = field_to_paths(sdf_glass, iso=-HALF_STROKE_PX)
                    sdf_dback, _, _, _ = compute_sdf_full(dback_cov, need_proj=False)
                    back_paths = field_to_paths(sdf_dback, iso=0.0)
                    front_paths = []
                else:
                    use_squircle_badge = True
    else:
        use_squircle_badge = True

    if use_squircle_badge:
        glass_outer_paths = [SQUIRCLE_OUTER]
        glass_inner_paths = [SQUIRCLE_INNER]
        back_paths = []
        sc_c = 0.72
        off_c = 12.0 * (1.0 - sc_c)
        front_paths = [scale_svg_path_d(d, PHOS_TO_24 * sc_c, off_c, off_c) for d, _ in reg_raw_paths]
        y1_24, y2_24 = 2.75, 21.25
    else:
        ys = [i // GRID for i in range(GRID * GRID) if glass_bool[i]]
        y1_24 = round(min(ys) * TO_24, 2) if ys else 2.5
        y2_24 = round(max(ys) * TO_24, 2) if ys else 21.5

    return {
        "glass": {
            "back": back_paths,
            "glass": " ".join(glass_outer_paths),
            "inner": " ".join(glass_inner_paths),
            "front": front_paths,
            "y1": y1_24,
            "y2": y2_24,
        },
        "outline": outline_inner,
        "solid": solid_inner,
        "duotone": duotone_inner,
    }


def render_standalone_svg(slug: str, variant: str, svg_data: dict) -> str:
    """Serializa un archivo `.svg` 24x24 100% autocontenido para Figma, navegador o `<img>`."""
    safe_id = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")
    pfx = f"iusoft-{safe_id}"

    if variant == "glass":
        g = svg_data["glass"]
        inner_str = g.get("inner", "")
        bevel_d = f"{g['glass']} {inner_str}".strip() if "inner" in g else g.get("bevel", g["glass"])
        back_m = "".join(f'<path d="{d}" fill="url(#{pfx}-obs)"/>' for d in g["back"])
        front_m = "".join(f'<path d="{d}" fill="url(#{pfx}-obs)"/>' for d in g["front"])
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n'
            f'  <defs>\n'
            f'    <linearGradient id="{pfx}-obs" x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0%" stop-color="#5b5b5e"/><stop offset="100%" stop-color="#161617"/></linearGradient>\n'
            f'    <linearGradient id="{pfx}-glass" x1="12" y1="2.5" x2="12" y2="21.5" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0%" stop-color="#e3e3e5" stop-opacity="0.64"/><stop offset="100%" stop-color="#bbbbc0" stop-opacity="0.62"/></linearGradient>\n'
            f'    <linearGradient id="{pfx}-bevel" x1="12" y1="{g["y1"]}" x2="12" y2="{g["y2"]}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0%" stop-color="#ffffff" stop-opacity="0.96"/><stop offset="58%" stop-color="#ffffff" stop-opacity="0.26"/><stop offset="100%" stop-color="#ffffff" stop-opacity="0"/></linearGradient>\n'
            f'    <filter id="{pfx}-blur" x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox">'
            f'<feGaussianBlur stdDeviation="1.6"/></filter>\n'
            f'    <mask id="{pfx}-out" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="-8" y="-8" width="40" height="40">'
            f'<rect x="-8" y="-8" width="40" height="40" fill="#ffffff"/><path d="{g["glass"]}" fill="#000000"/></mask>\n'
            f'    <mask id="{pfx}-in" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="-8" y="-8" width="40" height="40">'
            f'<rect x="-8" y="-8" width="40" height="40" fill="#000000"/><path d="{g["glass"]}" fill="#ffffff"/></mask>\n'
            f'  </defs>\n'
            f'  <g mask="url(#{pfx}-out)">{back_m}</g>\n'
            f'  <g mask="url(#{pfx}-in)"><g filter="url(#{pfx}-blur)">{back_m}</g></g>\n'
            f'  <g><path d="{g["glass"]}" fill="url(#{pfx}-glass)"/><path d="{bevel_d}" fill="url(#{pfx}-bevel)" fill-rule="evenodd"/>{front_m}</g>\n'
            f'</svg>\n'
        )

    inner = svg_data[variant]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">\n'
        f'  {inner}\n'
        f'</svg>\n'
    )
