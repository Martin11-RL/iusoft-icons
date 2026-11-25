#!/usr/bin/env python3
"""
Primitivas Geométricas Analíticas y DSL de Iconografía de Giro (`compiler/domain_dsl.py`).

Construye caminos vectoriales exactos en espacio `viewBox="0 0 24 24"` con continuidad
tangencial `G¹` / `C¹` y desplazamiento normal interior exacto (`ins = 0.75 u`) para el
bisel especular `evenodd` del estilo Glass, sin depender de trazos `stroke` en capas de cristal.
"""

import math

DEG = math.pi / 180.0


def fmt_num(v: float) -> str:
    """Formatea coordenadas SVG con hasta 2 decimales sin ceros sobrantes."""
    if abs(v) < 1e-6:
        return "0"
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def circle_path(cx: float, cy: float, r: float) -> str:
    """Círculo analítico cerrado mediante dos arcos SVG de 180 grados."""
    f = fmt_num
    return (
        f"M {f(cx)} {f(cy - r)} "
        f"A {f(r)} {f(r)} 0 1 1 {f(cx)} {f(cy + r)} "
        f"A {f(r)} {f(r)} 0 1 1 {f(cx)} {f(cy - r)} Z"
    )


def capsule_path(x1: float, y1: float, x2: float, y2: float, r: float) -> str:
    """Cápsula (estadio) analítica entre los centros `(x1, y1)` y `(x2, y2)` con radio `r`."""
    f = fmt_num
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    ex, ey = dx / ln, dy / ln
    nx, ny = -ey, ex
    return (
        f"M {f(x1 - r * nx)} {f(y1 - r * ny)} "
        f"L {f(x2 - r * nx)} {f(y2 - r * ny)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x2 + r * nx)} {f(y2 + r * ny)} "
        f"L {f(x1 + r * nx)} {f(y1 + r * ny)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x1 - r * nx)} {f(y1 - r * ny)} Z"
    )


def rounded_rect_path(x: float, y: float, w: float, h: float, r: float) -> str:
    """Rectángulo con esquinas boleadas de radio `r`."""
    f = fmt_num
    r = min(r, w / 2.0, h / 2.0)
    return (
        f"M {f(x + r)} {f(y)} L {f(x + w - r)} {f(y)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x + w)} {f(y + r)} "
        f"L {f(x + w)} {f(y + h - r)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x + w - r)} {f(y + h)} "
        f"L {f(x + r)} {f(y + h)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x)} {f(y + h - r)} "
        f"L {f(x)} {f(y + r)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(x + r)} {f(y)} Z"
    )


def rounded_polygon_path(pts: list[tuple[float, float]], radii: list[float], ins: float = 0.0) -> str:
    """
    Polígono cerrado con chaflanes circulares exactos por vértice y offset paralelo interior `ins`.
    En vértices convexos el radio efectivo se reduce (`r - ins`) y en cóncavos se expande (`r + ins`),
    preservando un grosor constante `ins` en todo el perímetro para el bisel `evenodd`.
    """
    f = fmt_num
    n = len(pts)
    fillets = []
    for i in range(n):
        pp, pc, pn = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        rb = radii[i]
        vix, viy = pc[0] - pp[0], pc[1] - pp[1]
        li = math.hypot(vix, viy)
        uix, uiy = vix / li, viy / li
        vox, voy = pn[0] - pc[0], pn[1] - pc[1]
        lo = math.hypot(vox, voy)
        uox, uoy = vox / lo, voy / lo
        nix, niy = -uiy, uix
        nox, noy = -uoy, uox
        cr = uix * uoy - uiy * uox
        ha = math.acos(max(-1.0, min(1.0, (-uix) * uox + (-uiy) * uoy))) / 2.0
        dt = rb / math.tan(ha)
        bx, by = pc[0] - dt * uix, pc[1] - dt * uiy
        if cr > 0:
            cx, cy = bx + rb * nix, by + rb * niy
            re = rb - ins
            fillets.append((cx - re * nix, cy - re * niy, cx - re * nox, cy - re * noy, re, 1))
        else:
            cx, cy = bx - rb * nix, by - rb * niy
            re = rb + ins
            fillets.append((cx + re * nix, cy + re * niy, cx + re * nox, cy + re * noy, re, 0))
    out = [f"M {f(fillets[0][0])} {f(fillets[0][1])}"]
    for i, (t1x, t1y, t2x, t2y, re, sw) in enumerate(fillets):
        if i > 0:
            out.append(f"L {f(t1x)} {f(t1y)}")
        out.append(f"A {f(re)} {f(re)} 0 0 {sw} {f(t2x)} {f(t2y)}")
    out.append("Z")
    return " ".join(out)


def wedge_path(
    ax: float,
    ay: float,
    radius: float,
    center_deg: float,
    half_deg: float,
    r_tip: float,
    r_corner: float,
    ins: float = 0.0,
) -> str:
    """Cuña circular (rebanada) con punta y esquinas tangentes boleadas y offset paralelo `ins`."""
    f = fmt_num
    tc, al = center_deg * DEG, half_deg * DEG
    t1, t2 = tc - al, tc + al
    e1x, e1y = math.cos(t1), math.sin(t1)
    e2x, e2y = math.cos(t2), math.sin(t2)
    ecx, ecy = math.cos(tc), math.sin(tc)
    n1x, n1y = -e1y, e1x
    n2x, n2y = e2y, -e2x
    dt = r_tip / math.sin(al)
    ptx, pty = ax + dt * ecx, ay + dt * ecy
    rt = r_tip - ins
    tr = math.sqrt((radius - r_corner) ** 2 - r_corner ** 2)
    rc, ra = r_corner - ins, radius - ins
    p1x, p1y = ax + tr * e1x + r_corner * n1x, ay + tr * e1y + r_corner * n1y
    u1x, u1y = (p1x - ax) / (radius - r_corner), (p1y - ay) / (radius - r_corner)
    p2x, p2y = ax + tr * e2x + r_corner * n2x, ay + tr * e2y + r_corner * n2x
    u2x, u2y = (p2x - ax) / (radius - r_corner), (p2y - ay) / (radius - r_corner)
    return (
        f"M {f(ptx - rt * n2x)} {f(pty - rt * n2y)} "
        f"A {f(rt)} {f(rt)} 0 0 1 {f(ptx - rt * n1x)} {f(pty - rt * n1y)} "
        f"L {f(p1x - rc * n1x)} {f(p1y - rc * n1y)} "
        f"A {f(rc)} {f(rc)} 0 0 1 {f(ax + ra * u1x)} {f(ay + ra * u1y)} "
        f"A {f(ra)} {f(ra)} 0 0 1 {f(ax + ra * u2x)} {f(ay + ra * u2y)} "
        f"A {f(rc)} {f(rc)} 0 0 1 {f(p2x - rc * n2x)} {f(p2y - rc * n2y)} Z"
    )


def inset_wedge_path(
    ax: float,
    ay: float,
    radius: float,
    center_deg: float,
    half_deg: float,
    r_tip: float,
    r_corner: float,
    inset_u: float = 0.75,
) -> str:
    """Atajo semántico de `wedge_path` con offset paralelo interior exacto de `0.75 u`."""
    return wedge_path(ax, ay, radius, center_deg, half_deg, r_tip, r_corner, ins=inset_u)


def crust_arc_path(
    ax: float,
    ay: float,
    r_mid: float,
    half_thick: float,
    center_deg: float,
    half_deg: float,
    r_cap: float,
) -> str:
    """Arco anular con extremos boleados tangentes (orilla horneada de pizza)."""
    f = fmt_num
    rin, rout = r_mid - half_thick, r_mid + half_thick
    tc, al = center_deg * DEG, half_deg * DEG
    t1, t2 = tc - al, tc + al
    e1x, e1y = math.cos(t1), math.sin(t1)
    e2x, e2y = math.cos(t2), math.sin(t2)
    n1x, n1y = -e1y, e1x
    n2x, n2y = e2y, -e2x
    to = math.sqrt((rout - r_cap) ** 2 - r_cap ** 2)
    ti = math.sqrt((rin + r_cap) ** 2 - r_cap ** 2)
    po1x, po1y = ax + to * e1x + r_cap * n1x, ay + to * e1y + r_cap * n1y
    uo1x, uo1y = (po1x - ax) / (rout - r_cap), (po1y - ay) / (rout - r_cap)
    po2x, po2y = ax + to * e2x + r_cap * n2x, ay + to * e2y + r_cap * n2y
    uo2x, uo2y = (po2x - ax) / (rout - r_cap), (po2y - ay) / (rout - r_cap)
    pi2x, pi2y = ax + ti * e2x + r_cap * n2x, ay + ti * e2y + r_cap * n2y
    ui2x, ui2y = (pi2x - ax) / (rin + r_cap), (pi2y - ay) / (rin + r_cap)
    pi1x, pi1y = ax + ti * e1x + r_cap * n1x, ay + ti * e1y + r_cap * n1y
    ui1x, ui1y = (pi1x - ax) / (rin + r_cap), (pi1y - ay) / (rin + r_cap)
    return (
        f"M {f(ax + ti * e1x)} {f(ay + ti * e1y)} "
        f"L {f(ax + to * e1x)} {f(ay + to * e1y)} "
        f"A {f(r_cap)} {f(r_cap)} 0 0 1 {f(ax + rout * uo1x)} {f(ay + rout * uo1y)} "
        f"A {f(rout)} {f(rout)} 0 0 1 {f(ax + rout * uo2x)} {f(ay + rout * uo2y)} "
        f"A {f(r_cap)} {f(r_cap)} 0 0 1 {f(ax + to * e2x)} {f(ay + to * e2y)} "
        f"L {f(ax + ti * e2x)} {f(ay + ti * e2y)} "
        f"A {f(r_cap)} {f(r_cap)} 0 0 1 {f(ax + rin * ui2x)} {f(ay + rin * ui2y)} "
        f"A {f(rin)} {f(rin)} 0 0 0 {f(ax + rin * ui1x)} {f(ay + rin * ui1y)} "
        f"A {f(r_cap)} {f(r_cap)} 0 0 1 {f(ax + ti * e1x)} {f(ay + ti * e1y)} Z"
    )


def pacman_pie_path(
    cx: float,
    cy: float,
    radius: float,
    gap_center_deg: float,
    gap_half_deg: float,
    r_corner: float,
    r_notch: float,
) -> str:
    """Disco circular de 3/4 con muesca angular interior y esquinas exteriores boleadas."""
    f = fmt_num
    tg, b = gap_center_deg * DEG, gap_half_deg * DEG
    ts, te = tg + b, tg - b
    esx, esy = math.cos(ts), math.sin(ts)
    eex, eey = math.cos(te), math.sin(te)
    ugx, ugy = math.cos(tg), math.sin(tg)
    nsx, nsy = -esy, esx
    nex, ney = eey, -eex
    dn = r_notch / math.sin(b)
    pnx, pny = cx + dn * ugx, cy + dn * ugy
    tr = math.sqrt((radius - r_corner) ** 2 - r_corner ** 2)
    psx, psy = cx + tr * esx + r_corner * nsx, cy + tr * esy + r_corner * nsy
    usx, usy = (psx - cx) / (radius - r_corner), (psy - cy) / (radius - r_corner)
    pex, pey = cx + tr * eex + r_corner * nex, cy + tr * eey + r_corner * ney
    uex, uey = (pex - cx) / (radius - r_corner), (pey - cy) / (radius - r_corner)
    return (
        f"M {f(pnx + r_notch * nsx)} {f(pny + r_notch * nsy)} "
        f"L {f(cx + tr * esx)} {f(cy + tr * esy)} "
        f"A {f(r_corner)} {f(r_corner)} 0 0 1 {f(cx + radius * usx)} {f(cy + radius * usy)} "
        f"A {f(radius)} {f(radius)} 0 1 1 {f(cx + radius * uex)} {f(cy + radius * uey)} "
        f"A {f(r_corner)} {f(r_corner)} 0 0 1 {f(cx + tr * eex)} {f(cy + tr * eey)} "
        f"L {f(pnx + r_notch * nex)} {f(pny + r_notch * ney)} "
        f"A {f(r_notch)} {f(r_notch)} 0 0 0 {f(pnx + r_notch * nsx)} {f(pny + r_notch * nsy)} Z"
    )


def handlebar_stem_path(
    p_grip: tuple[float, float],
    p_elbow: tuple[float, float],
    p_base: tuple[float, float],
    r: float,
) -> str:
    """Poste y manubrio doblado en 'L' con codo tangente exterior e interior."""
    f = fmt_num
    v1x, v1y = p_elbow[0] - p_grip[0], p_elbow[1] - p_grip[1]
    l1 = math.hypot(v1x, v1y)
    u1x, u1y = v1x / l1, v1y / l1
    n1x, n1y = u1y, -u1x
    v2x, v2y = p_base[0] - p_elbow[0], p_base[1] - p_elbow[1]
    l2 = math.hypot(v2x, v2y)
    u2x, u2y = v2x / l2, v2y / l2
    n2x, n2y = u2y, -u2x
    ang = math.acos(max(-1.0, min(1.0, (-u1x) * u2x + (-u1y) * u2y)))
    din = r / math.tan(ang / 2.0)
    cix, ciy = p_elbow[0] - r * n1x - din * u1x, p_elbow[1] - r * n1y - din * u1y
    rf = 0.45
    df = rf / math.tan(ang / 2.0)
    return (
        f"M {f(p_grip[0] + r * n1x)} {f(p_grip[1] + r * n1y)} "
        f"L {f(p_elbow[0] + r * n1x)} {f(p_elbow[1] + r * n1y)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(p_elbow[0] + r * n2x)} {f(p_elbow[1] + r * n2y)} "
        f"L {f(p_base[0] + r * n2x)} {f(p_base[1] + r * n2y)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(p_base[0] - r * n2x)} {f(p_base[1] - r * n2y)} "
        f"L {f(cix + df * u2x)} {f(ciy + df * u2y)} "
        f"A {f(rf)} {f(rf)} 0 0 0 {f(cix - df * u1x)} {f(ciy - df * u1y)} "
        f"L {f(p_grip[0] - r * n1x)} {f(p_grip[1] - r * n1y)} "
        f"A {f(r)} {f(r)} 0 0 1 {f(p_grip[0] + r * n1x)} {f(p_grip[1] + r * n1y)} Z"
    )


def ticket_serrated_path(
    x_left: float,
    x_right: float,
    y_top: float,
    y_peaks: float,
    r_top: float,
    r_peak: float,
    r_valley: float,
    ins: float = 0.0,
) -> str:
    """Hoja de comanda térmica con borde inferior dentado suave (ondas tangentes `G¹`) y offset `ins`."""
    f = fmt_num
    c1x, c5x = x_left + r_peak, x_right - r_peak
    sx = (c5x - c1x) / 4.0
    dy = math.sqrt((r_peak + r_valley) ** 2 - sx ** 2)
    p1 = (c1x, y_peaks)
    v2 = (c1x + sx, y_peaks + dy)
    p3 = (c1x + 2.0 * sx, y_peaks)
    v4 = (c1x + 3.0 * sx, y_peaks + dy)
    p5 = (c5x, y_peaks)
    rt, rp, rv = r_top - ins, r_peak - ins, r_valley + ins
    xl, xr, yt = x_left + ins, x_right - ins, y_top + ins

    def tangent_pt(pk, vl):
        w = rp / (rp + rv)
        return (pk[0] + w * (vl[0] - pk[0]), pk[1] + w * (vl[1] - pk[1]))

    t54 = tangent_pt(p5, v4)
    t34 = tangent_pt(p3, v4)
    t32 = tangent_pt(p3, v2)
    t12 = tangent_pt(p1, v2)
    return (
        f"M {f(x_left + r_top)} {f(yt)} L {f(x_right - r_top)} {f(yt)} "
        f"A {f(rt)} {f(rt)} 0 0 1 {f(xr)} {f(y_top + r_top)} "
        f"L {f(xr)} {f(y_peaks)} "
        f"A {f(rp)} {f(rp)} 0 0 1 {f(t54[0])} {f(t54[1])} "
        f"A {f(rv)} {f(rv)} 0 0 0 {f(t34[0])} {f(t34[1])} "
        f"A {f(rp)} {f(rp)} 0 0 1 {f(t32[0])} {f(t32[1])} "
        f"A {f(rv)} {f(rv)} 0 0 0 {f(t12[0])} {f(t12[1])} "
        f"A {f(rp)} {f(rp)} 0 0 1 {f(xl)} {f(y_peaks)} "
        f"L {f(xl)} {f(y_top + r_top)} "
        f"A {f(rt)} {f(rt)} 0 0 1 {f(x_left + r_top)} {f(yt)} Z"
    )


def oven_dome_path(
    cx: float,
    y_spring: float,
    radius: float,
    y_bottom: float,
    r_bottom: float,
    ins: float = 0.0,
) -> str:
    """Cúpula semicircular de horno artesanal con faldón recto y base boleada."""
    f = fmt_num
    ra, rbi = radius - ins, r_bottom - ins
    xl, xr, ybi = cx - radius + ins, cx + radius - ins, y_bottom - ins
    return (
        f"M {f(xl)} {f(y_spring)} A {f(ra)} {f(ra)} 0 0 1 {f(xr)} {f(y_spring)} "
        f"L {f(xr)} {f(y_bottom - r_bottom)} "
        f"A {f(rbi)} {f(rbi)} 0 0 1 {f(cx + radius - r_bottom)} {f(ybi)} "
        f"L {f(cx - radius + r_bottom)} {f(ybi)} "
        f"A {f(rbi)} {f(rbi)} 0 0 1 {f(xl)} {f(y_bottom - r_bottom)} Z"
    )


def build_domain_icons() -> dict[str, dict]:
    """Genera los 6 iconos insignia del giro en sus 4 estilos (`glass`, `outline`, `solid`, `duotone`)."""
    # 1. Rebanada de pizza (`pizza-slice`)
    sl_go = wedge_path(1.1, 22.9, 18.0, -45, 26.5, 1.55, 1.45, 0.0)
    sl_gi = inset_wedge_path(1.1, 22.9, 18.0, -45, 26.5, 1.55, 1.45, 0.75)
    sl_cr = crust_arc_path(1.1, 22.9, 18.5, 2.1, -45, 28.0, 1.72)
    sl_bk = wedge_path(1.1, 22.9, 16.5, -54.0, 21.5, 1.85, 1.25, 0.0)
    sl_peps = [circle_path(7.35, 17.05, 1.24), circle_path(8.75, 11.82, 1.34), circle_path(12.78, 15.42, 1.28)]
    sl_out = (
        f'<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{sl_go}"/><path d="M 6.9 4.4 A 19.6 19.6 0 0 1 19.6 17.1"/>'
        f'<circle cx="7.35" cy="17.05" r="1.15"/><circle cx="8.75" cy="11.82" r="1.2"/><circle cx="12.78" cy="15.42" r="1.15"/></g>'
    )

    # 2. Pizza entera (`pizza-whole`)
    wh_pie = pacman_pie_path(10.2, 13.8, 8.1, -45, 36, 1.10, 0.68)
    wh_go = wedge_path(9.75, 14.25, 10.7, -45, 32.0, 0.98, 1.25, 0.0)
    wh_gi = inset_wedge_path(9.75, 14.25, 10.7, -45, 32.0, 0.98, 1.25, 0.75)
    wh_peps = [circle_path(13.35, 9.15, 1.06), circle_path(16.05, 10.35, 1.06)]
    wh_out = (
        f'<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{wh_pie}"/><path d="{wh_go}"/>'
        f'<circle cx="13.35" cy="9.15" r="0.9"/><circle cx="16.05" cy="10.35" r="0.9"/></g>'
    )

    # 3. Cortador de pizza (`pizza-cutter`)
    ct_hd = capsule_path(14.4, 9.6, 4.6, 19.4, 1.75)
    ct_hd_solid = capsule_path(9.6, 14.4, 4.0, 20.0, 1.55)
    ct_go = circle_path(14.4, 9.6, 6.5)
    ct_gi = circle_path(14.4, 9.6, 5.75)
    ct_rv = circle_path(14.4, 9.6, 1.45)
    ct_out = (
        '<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="14.4" cy="9.6" r="6.3"/><circle cx="14.4" cy="9.6" r="1.5"/><path d="M 9.8 14.2 L 4.4 19.6"/></g>'
    )

    # 4. Moto de reparto (`moto-reparto`)
    mt_pts = [(3.2, 17.2), (3.2, 11.4), (10.3, 11.4), (10.3, 14.8), (13.7, 14.8), (15.2, 9.8), (20.6, 13.5), (20.6, 17.2)]
    mt_rad = [1.4, 2.05, 1.35, 0.95, 1.05, 1.55, 2.55, 1.35]
    mt_go = rounded_polygon_path(mt_pts, mt_rad, 0.0)
    mt_gi = rounded_polygon_path(mt_pts, mt_rad, 0.75)
    mt_bk = [
        circle_path(6.3, 17.5, 2.65),
        circle_path(17.7, 17.5, 2.65),
        handlebar_stem_path((13.0, 7.2), (15.2, 7.2), (17.3, 16.3), 0.98),
        capsule_path(15.5, 8.5, 16.95, 8.5, 0.85),
        rounded_rect_path(3.1, 6.8, 6.3, 5.6, 1.55),
    ]
    mt_tr = capsule_path(5.1, 13.5, 8.2, 13.5, 0.65)
    mt_out = (
        f'<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="3.2" y="6.8" width="6.1" height="4.6" rx="1.4"/><path d="{mt_go}"/>'
        f'<circle cx="6.3" cy="17.5" r="2.4"/><circle cx="17.7" cy="17.5" r="2.4"/>'
        f'<path d="M 13.2 7.2 H 15.3 L 16.4 11.2"/></g>'
    )

    # 5. Ticket impresora (`ticket-impresora`)
    pr_bd = rounded_rect_path(2.8, 10.2, 18.4, 10.3, 2.8)
    pr_go = ticket_serrated_path(6.0, 18.0, 2.6, 14.55, 1.85, 1.32, 1.18, 0.0)
    pr_gi = ticket_serrated_path(6.0, 18.0, 2.6, 14.55, 1.85, 1.32, 1.18, 0.75)
    pr_ln = [capsule_path(8.9, 6.0, 15.1, 6.0, 0.70), capsule_path(8.9, 8.65, 13.4, 8.65, 0.70)]
    pr_out = (
        f'<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{pr_go}"/>'
        f'<path d="M 6.0 10.5 H 5.2 A 2.4 2.4 0 0 0 2.8 12.9 V 18.0 A 2.4 2.4 0 0 0 5.2 20.4 H 18.8 A 2.4 2.4 0 0 0 21.2 18.0 V 12.9 A 2.4 2.4 0 0 0 18.8 10.5 H 18.0"/>'
        f'<path d="M 9.2 6.0 H 14.8"/><path d="M 9.2 8.7 H 13.2"/></g>'
    )

    # 6. Horno y fuego (`horno-fuego`)
    ov_hb = rounded_rect_path(2.5, 17.0, 19.0, 3.7, 1.85)
    ov_ch = rounded_rect_path(15.4, 2.6, 3.4, 6.0, 1.45)
    ov_go = oven_dome_path(12.0, 12.7, 8.5, 18.4, 1.65, 0.0)
    ov_gi = oven_dome_path(12.0, 12.7, 8.5, 18.4, 1.65, 0.75)
    ov_fl = (
        "M 12.05 16.65 C 10.02 16.65 8.95 15.28 8.95 13.60 C 8.95 12.42 9.44 11.45 10.08 10.78 "
        "C 10.32 10.52 10.72 10.68 10.69 11.05 C 10.66 11.46 10.80 11.86 11.12 11.90 "
        "C 11.42 11.94 11.58 11.52 11.70 11.00 C 11.90 10.02 12.24 8.98 12.70 8.38 "
        "C 12.95 8.06 13.42 8.20 13.48 8.62 C 13.75 10.42 15.05 11.68 15.05 13.62 "
        "C 15.05 15.32 13.92 16.65 12.05 16.65 Z"
    )
    ov_out = (
        f'<g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{ov_go}"/><path d="M 2.8 20.4 H 21.2"/>'
        f'<path d="M 15.6 5.6 V 3.6 A 1.2 1.2 0 0 1 18.0 3.6 V 7.2"/><path d="{ov_fl}"/></g>'
    )

    return {
        "pizza-slice": {
            "glass": {"back": [sl_cr, sl_bk], "glass": sl_go, "inner": sl_gi, "front": sl_peps, "y1": 3.4, "y2": 21.6},
            "outline": sl_out,
            "solid": f'<path d="{sl_cr}" fill="currentColor"/><path fill-rule="evenodd" d="{sl_go} {" ".join(sl_peps)}" fill="currentColor"/>',
            "duotone": f'<path d="{sl_go}" fill="currentColor" fill-opacity="0.2"/>{sl_out}',
        },
        "pizza-whole": {
            "glass": {"back": [wh_pie], "glass": wh_go, "inner": wh_gi, "front": wh_peps, "y1": 3.5, "y2": 14.8},
            "outline": wh_out,
            "solid": f'<path d="{wh_pie}" fill="currentColor"/><path fill-rule="evenodd" d="{wh_go} {" ".join(wh_peps)}" fill="currentColor"/>',
            "duotone": f'<path d="{wh_go}" fill="currentColor" fill-opacity="0.2"/>{wh_out}',
        },
        "pizza-cutter": {
            "glass": {"back": [ct_hd], "glass": ct_go, "inner": ct_gi, "front": [ct_rv], "y1": 3.1, "y2": 16.1},
            "outline": ct_out,
            "solid": f'<path d="{ct_hd_solid}" fill="currentColor"/><path fill-rule="evenodd" d="{ct_go} {ct_rv}" fill="currentColor"/>',
            "duotone": f'<path d="{ct_go}" fill="currentColor" fill-opacity="0.2"/>{ct_out}',
        },
        "moto-reparto": {
            "glass": {"back": mt_bk, "glass": mt_go, "inner": mt_gi, "front": [mt_tr], "y1": 9.8, "y2": 17.2},
            "outline": mt_out,
            "solid": (
                f'<path d="{rounded_rect_path(3.1, 6.8, 6.2, 4.2, 1.4)}" fill="currentColor"/>'
                f'<path d="{circle_path(6.3, 18.0, 2.3)}" fill="currentColor"/>'
                f'<path d="{circle_path(17.7, 18.0, 2.3)}" fill="currentColor"/>'
                f'<path d="{handlebar_stem_path((13.0, 7.2), (15.2, 7.2), (16.4, 11.5), 0.9)}" fill="currentColor"/>'
                f'<path fill-rule="evenodd" d="{mt_go} {mt_tr}" fill="currentColor"/>'
            ),
            "duotone": f'<path d="{mt_go}" fill="currentColor" fill-opacity="0.2"/>{mt_out}',
        },
        "ticket-impresora": {
            "glass": {"back": [pr_bd], "glass": pr_go, "inner": pr_gi, "front": pr_ln, "y1": 2.6, "y2": 15.8},
            "outline": pr_out,
            "solid": (
                f'<path fill-rule="evenodd" d="{pr_bd} {ticket_serrated_path(5.2, 18.8, 2.0, 15.1, 2.1, 1.65, 1.45, 0.0)}" fill="currentColor"/>'
                f'<path fill-rule="evenodd" d="{pr_go} {" ".join(pr_ln)}" fill="currentColor"/>'
            ),
            "duotone": f'<path d="{pr_go}" fill="currentColor" fill-opacity="0.2"/>{pr_out}',
        },
        "horno-fuego": {
            "glass": {"back": [ov_hb, ov_ch], "glass": ov_go, "inner": ov_gi, "front": [ov_fl], "y1": 4.2, "y2": 18.4},
            "outline": ov_out,
            "solid": (
                f'<path d="{rounded_rect_path(2.5, 19.0, 19.0, 2.0, 1.0)}" fill="currentColor"/>'
                f'<path d="{rounded_rect_path(15.4, 2.6, 3.2, 4.0, 1.2)}" fill="currentColor"/>'
                f'<path fill-rule="evenodd" d="{ov_go} {ov_fl}" fill="currentColor"/>'
            ),
            "duotone": f'<path d="{ov_go}" fill="currentColor" fill-opacity="0.2"/>{ov_out}',
        },
    }
