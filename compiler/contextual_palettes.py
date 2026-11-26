#!/usr/bin/env python3
"""
Motor Determinista 0-Tokens de Refracción Cromática Contextual (`compiler/contextual_palettes.py`).

Asigna de forma 100% determinista (sin llamadas a IA) una de las 8 familias ópticas de vidrio
esmerilado de doble canal (`obs-back` para refracción `feGaussianBlur 1.6` + `obs-front` para detalle
nítido + `glass` con tinte sutil `7–14%` + `bevel` especular blanco `0.75 u`), calibradas tanto para
superficie clara (`#FFFFFF` / `#FAFAFA`) como para modo oscuro OLED (`#09090B` / `#18181B`).
"""

CONTEXTUAL_PALETTES: dict[str, dict] = {
    "gastronomia": {
        "label": "Gastronomía · Terracota y queso",
        "light": {
            "obsBack": ["#D97706", "#78350F"],
            "glass": ["#F7EFE2", "0.72", "#E2CEAE", "0.66"],
            "obsFront": ["#C2410C", "#7C2D12"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#FBBF24", "#D97706"],
            "glass": ["#786954", "0.56", "#443A2E", "0.52"],
            "obsFront": ["#FB923C", "#EA580C"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "horno-calor": {
        "label": "Horno y Energía · Ámbar-carmesí",
        "light": {
            "obsBack": ["#9A3412", "#292524"],
            "glass": ["#E5DCD7", "0.68", "#B8ACA6", "0.64"],
            "obsFront": ["#EA580C", "#B91C1C"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#FDBA74", "#D97706"],
            "glass": ["#6B5B53", "0.56", "#3F3530", "0.52"],
            "obsFront": ["#FDE047", "#EF4444"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "mensajeria": {
        "label": "Mensajería y Éxito · Verde jade",
        "light": {
            "obsBack": ["#0D7A5C", "#052E16"],
            "glass": ["#DCF2EA", "0.70", "#A8D8C8", "0.64"],
            "obsFront": ["#0D7A5C", "#052E16"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#34D399", "#059669"],
            "glass": ["#2A594B", "0.56", "#17362D", "0.52"],
            "obsFront": ["#ECFDF5", "#6EE7B7"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "tesoreria": {
        "label": "Caja y Comercio · Esmeralda tesorería",
        "light": {
            "obsBack": ["#16A34A", "#14532D"],
            "glass": ["#DCE8E0", "0.70", "#AFC5B7", "0.64"],
            "obsFront": ["#52525B", "#18181B"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#4ADE80", "#16A34A"],
            "glass": ["#4B5850", "0.56", "#2C3530", "0.52"],
            "obsFront": ["#FAFAFA", "#A1A1AA"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "ruta-logistica": {
        "label": "Reparto y Ruta · Azul cobalto",
        "light": {
            "obsBack": ["#3B82F6", "#1E3A8A"],
            "glass": ["#DCE6FA", "0.70", "#AEBEE6", "0.64"],
            "obsFront": ["#1D4ED8", "#1E3A8A"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#60A5FA", "#3B82F6"],
            "glass": ["#354B75", "0.56", "#202D47", "0.52"],
            "obsFront": ["#DBEAFE", "#60A5FA"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "clientes-equipo": {
        "label": "Clientes y Equipo · Índigo zafiro",
        "light": {
            "obsBack": ["#4F46E5", "#312E81"],
            "glass": ["#E0E4F5", "0.70", "#B5BEDE", "0.64"],
            "obsFront": ["#4338CA", "#1E1B4B"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#A5B4FC", "#818CF8"],
            "glass": ["#3A3F66", "0.56", "#232640", "0.52"],
            "obsFront": ["#EEF2FF", "#A5B4FC"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "alerta-peligro": {
        "label": "Alertas y Control · Rubí sobrio",
        "light": {
            "obsBack": ["#DC2626", "#881337"],
            "glass": ["#F2DEDE", "0.70", "#D9B4B6", "0.64"],
            "obsFront": ["#B91C1C", "#7F1D1D"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#F87171", "#EF4444"],
            "glass": ["#6B3D42", "0.56", "#3D2428", "0.52"],
            "obsFront": ["#FEF2F2", "#FCA5A5"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
    "sistema-grafito": {
        "label": "Sistema y Estructura · Cuarzo grafito",
        "light": {
            "obsBack": ["#475569", "#1E293B"],
            "glass": ["#E2E6EC", "0.70", "#B1B9C5", "0.64"],
            "obsFront": ["#334155", "#0F172A"],
            "bevel": ["0.96", "0.30", "0.06"],
        },
        "dark": {
            "obsBack": ["#E2E8F0", "#94A3B8"],
            "glass": ["#5B6575", "0.56", "#343B46", "0.52"],
            "obsFront": ["#F8FAFC", "#CBD5E1"],
            "bevel": ["0.94", "0.34", "0.10"],
        },
    },
}

SLUG_TO_PALETTE: dict[str, str] = {
    # 1. Gastronomía (Terracota y queso)
    **{
        s: "gastronomia"
        for s in (
            "pizza",
            "pizza-whole",
            "pizza-cutter",
            "chef-hat",
            "utensils",
            "utensils-crossed",
            "coffee",
            "cup-soda",
            "ice-cream",
            "bone",
            "cookie",
            "beer",
            "wine",
            "soup",
            "sandwich",
            "cake",
            "salad",
            "fish",
            "beef",
            "milk",
            "apple",
            "cherry",
            "citrus",
            "grape",
            "candy",
            "croissant",
            "popcorn",
        )
    },
    # 2. Horno y Energía (Ámbar-carmesí)
    **{
        s: "horno-calor"
        for s in (
            "flame",
            "campfire",
            "zap",
            "sparkles",
            "sun",
            "sunset",
            "lightbulb",
            "flashlight",
            "rocket",
            "star",
            "trophy",
            "confetti",
            "balloon",
            "heart",
            "gas",
        )
    },
    # 3. Mensajería y Éxito (Verde jade)
    **{
        s: "mensajeria"
        for s in (
            "message-circle",
            "message-square",
            "send",
            "mail",
            "phone",
            "megaphone",
            "check-circle-2",
            "check",
            "check-check",
            "clipboard-check",
            "package-check",
            "user-check",
            "shield-check",
            "handshake",
            "leaf",
            "radio",
            "share-2",
        )
    },
    # 4. Caja y Comercio (Esmeralda tesorería)
    **{
        s: "tesoreria"
        for s in (
            "wallet",
            "banknote",
            "coins",
            "dollar-sign",
            "credit-card",
            "receipt",
            "trending-up",
            "percent",
            "calculator",
            "tag",
            "shopping-bag",
            "shopping-cart",
            "landmark",
            "scale",
            "diamond",
            "gift",
        )
    },
    # 5. Reparto y Ruta (Azul cobalto)
    **{
        s: "ruta-logistica"
        for s in (
            "bike",
            "scooter",
            "truck",
            "map",
            "map-pin",
            "map-pinned",
            "navigation",
            "locate-fixed",
            "crosshair",
            "route",
            "globe",
            "earth",
            "package",
            "package-open",
            "package-plus",
            "boxes",
            "wifi",
            "bluetooth",
            "signal",
            "cloud",
            "airplane",
            "sailboat",
            "anchor",
            "parachute",
            "drop",
            "umbrella",
            "beach",
        )
    },
    # 6. Clientes y Equipo (Índigo zafiro)
    **{
        s: "clientes-equipo"
        for s in (
            "user",
            "users",
            "user-plus",
            "user-circle",
            "store",
            "building",
            "building-2",
            "briefcase",
            "key",
            "key-round",
            "lock",
            "unlock",
            "shield",
            "bot",
            "palette",
            "paintbrush",
            "camera",
            "music",
            "headphones",
            "headset",
            "glasses",
            "emoji",
            "emoji-laugh",
            "home",
            "door",
            "bed",
        )
    },
    # 7. Alertas y Control (Rubí sobrio)
    **{
        s: "alerta-peligro"
        for s in (
            "alert-triangle",
            "alert-circle",
            "alert-octagon",
            "octagon-x",
            "xcircle",
            "x",
            "trash",
            "trash-2",
            "ban",
            "shield-x",
            "shield-alert",
            "trending-down",
            "wifi-off",
            "cloud-off",
            "power-off",
            "unplug",
            "calendar-off",
            "map-pin-off",
            "package-minus",
            "user-x",
            "signal-zero",
            "bug",
            "log-out",
            "eraser",
        )
    },
}

KEYWORD_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("alerta-peligro", ("alerta", "error", "peligro", "eliminar", "borrar", "merma", "bloque", "rechaz", "fallo", "sin ", "baja")),
    ("gastronomia", ("pizza", "comida", "bebida", "restaurante", "ingrediente", "postre", "pan", "queso", "carne", "fruta", "sopa", "cerveza", "vino", "cafe")),
    ("horno-calor", ("horno", "fuego", "flama", "calor", "energia", "rayo", "destacad", "trofeo", "cohete", "sol")),
    ("mensajeria", ("whatsapp", "chat", "mensaje", "correo", "enviar", "completad", "confirm", "verificad")),
    ("tesoreria", ("caja", "efectivo", "billete", "moneda", "pago", "tarjeta", "precio", "venta", "descuento", "promo", "recibo", "banco", "carrito")),
    ("ruta-logistica", ("reparto", "moto", "camion", "mapa", "gps", "ruta", "domicilio", "paquete", "insumo", "lote", "wifi", "bluetooth", "nube")),
    ("clientes-equipo", ("cliente", "usuario", "empleado", "equipo", "sucursal", "tienda", "llave", "candado", "permiso", "tema", "apariencia")),
]


def classify_icon_palette(meta: dict) -> str:
    """Clasifica determinísticamente cualquier icono actual o futuro en una de las 8 paletas ópticas."""
    explicit = meta.get("palette")
    if explicit in CONTEXTUAL_PALETTES:
        return explicit

    slug = meta.get("slug", "").lower()
    if slug in SLUG_TO_PALETTE:
        return SLUG_TO_PALETTE[slug]

    haystack = f"{slug} {meta.get('label', '')} {meta.get('keywords', '')}".lower()
    for pal_id, words in KEYWORD_RULES:
        if any(w in haystack for w in words):
            return pal_id

    cat = meta.get("category", "")
    if cat == "Giro Pizzería":
        return "gastronomia"
    if cat == "Caja y Comercio":
        return "tesoreria"
    if cat == "Pedidos y Reparto":
        return "ruta-logistica"
    if cat == "Usuarios y Ajustes":
        return "clientes-equipo"
    return "sistema-grafito"
