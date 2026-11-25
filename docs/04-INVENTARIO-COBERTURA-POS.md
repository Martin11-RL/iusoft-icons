# 04 · Inventario Completo de Cobertura POS (`197/197` + `46` Adicionales)

Referencia 1 a 1 entre los **197 iconos canónicos de `lucide-react`** utilizados en módulos operativos de Punto de Venta (caja, cocina, reparto, catálogo, inventario y configuración) y sus equivalencias en **IU-SOFT Icons**, más los **46 iconos complementarios** incluidos en el paquete (`243` iconos × `4` estilos = `972` SVGs).

---

## 1. Resumen por Fuente de Construcción

| Origen técnico | En cobertura POS | Complementarios | Total iconos | Total SVGs (`4` estilos) |
| :--- | ---: | ---: | ---: | ---: |
| `domain-dsl` (`compiler/domain_dsl.py`) | `4` | `2` | `6` | `24` |
| `phosphor-0-token` (`Esenciales Base` MIT) | `36` | `44` | `80` | `320` |
| `phosphor-0-token` (`Operación POS` MIT) | `157` | `0` | `157` | `628` |
| **Total general** | **`197` (`100%`)** | **`46`** | **`243`** | **`972`** |

---

## 2. Tabla 1 a 1 de los `197` Iconos Canónicos POS

| # | Símbolo `lucide-react` | Alias soportados | Slug en `icons/*/` | Nombre en español | Categoría | Fuente base | Usos |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | ---: |
| 1 | `Loader2` | `Loader2Icon` | `loader-2.svg` | Cargando proceso | Interfaz y Alertas | `phosphor:spinner-gap` | 114 |
| 2 | `Plus` | — | `plus.svg` | Agregar ítem | Interfaz y Alertas | `phosphor:plus` | 61 |
| 3 | `MapPin` | — | `map-pin.svg` | Domicilio de entrega | Pedidos y Reparto | `phosphor:map-pin` | 58 |
| 4 | `CheckCircle2` | `CheckCircle`, `CircleCheck`, `CircleCheckIcon` | `check-circle-2.svg` | Completado | Interfaz y Alertas | `phosphor:check-circle` | 56 |
| 5 | `RefreshCw` | — | `refresh-cw.svg` | Actualizar datos | Interfaz y Alertas | `phosphor:arrows-clockwise` | 52 |
| 6 | `Trash2` | — | `trash-2.svg` | Eliminar registro | Interfaz y Alertas | `phosphor:trash` | 44 |
| 7 | `Clock` | `Clock2` | `clock.svg` | Reloj y horario | Pedidos y Reparto | `phosphor:clock` | 43 |
| 8 | `Check` | `CheckIcon` | `check.svg` | Confirmar | Interfaz y Alertas | `phosphor:check` | 38 |
| 9 | `X` | `XIcon` | `x.svg` | Cerrar modal | Interfaz y Alertas | `phosphor:x` | 38 |
| 10 | `AlertTriangle` | `TriangleAlert`, `TriangleAlertIcon` | `alert-triangle.svg` | Advertencia | Interfaz y Alertas | `phosphor:warning` | 36 |
| 11 | `Truck` | — | `truck.svg` | Proveedor y reparto | Pedidos y Reparto | `phosphor:truck` | 34 |
| 12 | `AlertCircle` | — | `alert-circle.svg` | Alerta circular | Interfaz y Alertas | `phosphor:warning-circle` | 33 |
| 13 | `Package` | — | `package.svg` | Insumo o paquete | Pedidos y Reparto | `phosphor:package` | 28 |
| 14 | `Banknote` | — | `banknote.svg` | Efectivo y billetes | Caja y Comercio | `phosphor:money` | 27 |
| 15 | `Search` | `SearchIcon` | `search.svg` | Buscar | Navegación | `phosphor:magnifying-glass` | 24 |
| 16 | `QrCode` | — | `qr-code.svg` | Código QR | Interfaz y Alertas | `phosphor:qr-code` | 23 |
| 17 | `FileText` | — | `file-text.svg` | Documento y reporte | Interfaz y Alertas | `phosphor:file-text` | 22 |
| 18 | `Lock` | — | `lock.svg` | Candado y bloqueo | Usuarios y Ajustes | `phosphor:lock` | 22 |
| 19 | `Phone` | — | `phone.svg` | Teléfono | Interfaz y Alertas | `phosphor:phone` | 22 |
| 20 | `Smartphone` | — | `smartphone.svg` | App móvil PWA | Usuarios y Ajustes | `phosphor:device-mobile` | 22 |
| 21 | `ExternalLink` | — | `external-link.svg` | Abrir en pestaña | Navegación | `phosphor:arrow-square-out` | 21 |
| 22 | `Download` | — | `download.svg` | Descargar | Interfaz y Alertas | `phosphor:download-simple` | 19 |
| 23 | `ChevronRight` | `ChevronRightIcon` | `chevron-right.svg` | Siguiente | Navegación | `phosphor:caret-right` | 18 |
| 24 | `CreditCard` | — | `credit-card.svg` | Pago con tarjeta | Caja y Comercio | `phosphor:credit-card` | 18 |
| 25 | `History` | — | `history.svg` | Historial de movimientos | Interfaz y Alertas | `phosphor:clock-counter-clockwise` | 18 |
| 26 | `User` | — | `user.svg` | Cliente o empleado | Usuarios y Ajustes | `phosphor:user` | 17 |
| 27 | `Users` | — | `users.svg` | Equipo y nómina | Usuarios y Ajustes | `phosphor:users` | 17 |
| 28 | `KeyRound` | — | `key-round.svg` | PIN de acceso | Usuarios y Ajustes | `phosphor:key-return` | 16 |
| 29 | `Pencil` | — | `pencil.svg` | Modificar campo | Interfaz y Alertas | `phosphor:pencil` | 16 |
| 30 | `Copy` | — | `copy.svg` | Copiar | Interfaz y Alertas | `phosphor:copy` | 15 |
| 31 | `DollarSign` | — | `dollar-sign.svg` | Importe en pesos | Caja y Comercio | `phosphor:currency-dollar` | 15 |
| 32 | `Eye` | — | `eye.svg` | Ver detalle | Interfaz y Alertas | `phosphor:eye` | 14 |
| 33 | `Printer` | — | `printer.svg` | Ticket impresora | Giro Pizzería | `dsl:ticket-impresora` | 14 |
| 34 | `Sparkles` | — | `sparkles.svg` | Sugerencia inteligente | Interfaz y Alertas | `phosphor:sparkle` | 14 |
| 35 | `Wallet` | — | `wallet.svg` | Fondo de caja | Caja y Comercio | `phosphor:wallet` | 14 |
| 36 | `MessageCircle` | — | `message-circle.svg` | Chat WhatsApp | Interfaz y Alertas | `phosphor:chat-circle-dots` | 13 |
| 37 | `ChevronDown` | `ChevronDownIcon` | `chevron-down.svg` | Desplegar abajo | Navegación | `phosphor:caret-down` | 12 |
| 38 | `Info` | `InfoIcon` | `info.svg` | Información | Interfaz y Alertas | `phosphor:info` | 12 |
| 39 | `Save` | — | `save.svg` | Guardar cambios | Interfaz y Alertas | `phosphor:floppy-disk` | 12 |
| 40 | `ShieldCheck` | — | `shield-check.svg` | Acceso verificado | Usuarios y Ajustes | `phosphor:shield-check` | 12 |
| 41 | `Store` | — | `store.svg` | Mostrador y tienda | Caja y Comercio | `phosphor:storefront` | 12 |
| 42 | `TrendingUp` | — | `trending-up.svg` | Crecimiento y meta | Caja y Comercio | `phosphor:trend-up` | 12 |
| 43 | `ArrowLeft` | — | `arrow-left.svg` | Regresar | Navegación | `phosphor:arrow-left` | 11 |
| 44 | `Bike` | — | `bike.svg` | Moto de reparto | Giro Pizzería | `dsl:moto-reparto` | 11 |
| 45 | `Key` | — | `key.svg` | Llave de acceso | Usuarios y Ajustes | `phosphor:key` | 11 |
| 46 | `LayoutGrid` | — | `layout-grid.svg` | Catálogo en mosaico | Navegación | `phosphor:grid-four` | 11 |
| 47 | `Navigation` | — | `navigation.svg` | Navegar en ruta | Pedidos y Reparto | `phosphor:navigation-arrow` | 11 |
| 48 | `Calendar` | `CalendarIcon` | `calendar.svg` | Calendario | Interfaz y Alertas | `phosphor:calendar-blank` | 10 |
| 49 | `MapPinOff` | — | `map-pin-off.svg` | Sin cobertura GPS | Pedidos y Reparto | `phosphor:map-pin-simple-area` | 10 |
| 50 | `Receipt` | — | `receipt.svg` | Recibo de venta | Caja y Comercio | `phosphor:receipt` | 10 |
| 51 | `ShoppingBag` | — | `shopping-bag.svg` | Para llevar | Caja y Comercio | `phosphor:shopping-bag` | 10 |
| 52 | `Tag` | — | `tag.svg` | Etiqueta y promoción | Caja y Comercio | `phosphor:tag` | 10 |
| 53 | `Zap` | — | `zap.svg` | Acción rápida | Interfaz y Alertas | `phosphor:lightning` | 10 |
| 54 | `Calculator` | — | `calculator.svg` | Calculadora | Caja y Comercio | `phosphor:calculator` | 9 |
| 55 | `CalendarDays` | — | `calendar-days.svg` | Días del periodo | Interfaz y Alertas | `phosphor:calendar-dots` | 9 |
| 56 | `Edit` | `Edit2`, `Edit3`, `SquarePen` | `edit.svg` | Editar registro | Interfaz y Alertas | `phosphor:note-pencil` | 9 |
| 57 | `Power` | — | `power.svg` | Encender turno | Usuarios y Ajustes | `phosphor:power` | 9 |
| 58 | `RotateCcw` | — | `rotate-ccw.svg` | Deshacer o devolver | Interfaz y Alertas | `phosphor:arrow-counter-clockwise` | 9 |
| 59 | `ShoppingCart` | — | `shopping-cart.svg` | Carrito POS | Caja y Comercio | `phosphor:shopping-cart` | 9 |
| 60 | `ArrowRight` | — | `arrow-right.svg` | Continuar | Navegación | `phosphor:arrow-right` | 8 |
| 61 | `Bluetooth` | — | `bluetooth.svg` | Impresora Bluetooth | Usuarios y Ajustes | `phosphor:bluetooth` | 8 |
| 62 | `ChefHat` | — | `chef-hat.svg` | Cocina y preparación | Pedidos y Reparto | `phosphor:chef-hat` | 8 |
| 63 | `ChevronLeft` | `ChevronLeftIcon` | `chevron-left.svg` | Anterior | Navegación | `phosphor:caret-left` | 8 |
| 64 | `ClipboardList` | — | `clipboard-list.svg` | Comanda y lista | Navegación | `phosphor:clipboard` | 8 |
| 65 | `EyeOff` | — | `eye-off.svg` | Ocultar dato | Interfaz y Alertas | `phosphor:eye-slash` | 8 |
| 66 | `PowerOff` | — | `power-off.svg` | Desconectar | Usuarios y Ajustes | `phosphor:plugs` | 8 |
| 67 | `UtensilsCrossed` | — | `utensils-crossed.svg` | Restaurante y menú | Pedidos y Reparto | `phosphor:fork-knife` | 8 |
| 68 | `XCircle` | — | `xcircle.svg` | Limpiar o rechazar | Interfaz y Alertas | `phosphor:x-circle` | 8 |
| 69 | `BarChart3` | — | `bar-chart-3.svg` | Gráfica de ventas | Caja y Comercio | `phosphor:chart-bar` | 7 |
| 70 | `Briefcase` | — | `briefcase.svg` | Portafolio | Usuarios y Ajustes | `phosphor:briefcase` | 7 |
| 71 | `Bug` | — | `bug.svg` | Reporte de fallo | Interfaz y Alertas | `phosphor:bug` | 7 |
| 72 | `CalendarClock` | — | `calendar-clock.svg` | Cita programada | Pedidos y Reparto | `phosphor:calendar-check` | 7 |
| 73 | `Layers` | — | `layers.svg` | Capas y recetas | Interfaz y Alertas | `phosphor:stack` | 7 |
| 74 | `LogOut` | — | `log-out.svg` | Cerrar sesión | Usuarios y Ajustes | `phosphor:sign-out` | 7 |
| 75 | `MessageSquare` | — | `message-square.svg` | Nota de comanda | Interfaz y Alertas | `phosphor:chat-centered-text` | 7 |
| 76 | `Minus` | — | `minus.svg` | Restar cantidad | Interfaz y Alertas | `phosphor:minus` | 7 |
| 77 | `Pizza` | — | `pizza.svg` | Rebanada de pizza | Giro Pizzería | `dsl:pizza-slice` | 7 |
| 78 | `SlidersHorizontal` | — | `sliders-horizontal.svg` | Filtros de vista | Navegación | `phosphor:sliders-horizontal` | 7 |
| 79 | `Star` | — | `star.svg` | Destacado | Interfaz y Alertas | `phosphor:star` | 7 |
| 80 | `Sun` | — | `sun.svg` | Modo claro | Usuarios y Ajustes | `phosphor:sun` | 7 |
| 81 | `TrendingDown` | — | `trending-down.svg` | Baja o egreso | Caja y Comercio | `phosphor:trend-down` | 7 |
| 82 | `Chrome` | — | `chrome.svg` | Extensión Chrome | Interfaz y Alertas | `phosphor:google-chrome-logo` | 6 |
| 83 | `Flame` | — | `flame.svg` | Horno y fuego | Giro Pizzería | `dsl:horno-fuego` | 6 |
| 84 | `Globe` | — | `globe.svg` | Dominio web | Interfaz y Alertas | `phosphor:globe-hemisphere-west` | 6 |
| 85 | `Image` | `ImageIcon` | `image.svg` | Foto de producto | Interfaz y Alertas | `phosphor:image` | 6 |
| 86 | `Monitor` | — | `monitor.svg` | Pantalla TV / POS | Usuarios y Ajustes | `phosphor:monitor` | 6 |
| 87 | `Settings` | — | `settings.svg` | Configuración | Usuarios y Ajustes | `phosphor:gear` | 6 |
| 88 | `Upload` | — | `upload.svg` | Subir archivo | Interfaz y Alertas | `phosphor:upload-simple` | 6 |
| 89 | `WifiOff` | — | `wifi-off.svg` | Sin Wi-Fi | Usuarios y Ajustes | `phosphor:wifi-slash` | 6 |
| 90 | `Ban` | — | `ban.svg` | Cancelar o bloquear | Interfaz y Alertas | `phosphor:prohibit` | 5 |
| 91 | `FolderOpen` | — | `folder-open.svg` | Carpeta | Interfaz y Alertas | `phosphor:folder-open` | 5 |
| 92 | `Moon` | — | `moon.svg` | Modo oscuro | Usuarios y Ajustes | `phosphor:moon` | 5 |
| 93 | `Palette` | — | `palette.svg` | Apariencia y tema | Usuarios y Ajustes | `phosphor:palette` | 5 |
| 94 | `Timer` | — | `timer.svg` | Cronómetro SLA | Pedidos y Reparto | `phosphor:timer` | 5 |
| 95 | `ArrowRightLeft` | — | `arrow-right-left.svg` | Intercambiar | Navegación | `phosphor:arrows-left-right` | 4 |
| 96 | `ArrowUpDown` | — | `arrow-up-down.svg` | Ordenar columna | Navegación | `phosphor:arrows-down-up` | 4 |
| 97 | `ChevronUp` | — | `chevron-up.svg` | Contraer arriba | Navegación | `phosphor:caret-up` | 4 |
| 98 | `Filter` | — | `filter.svg` | Filtrar vista | Navegación | `phosphor:funnel` | 4 |
| 99 | `Home` | — | `home.svg` | Inicio | Navegación | `phosphor:house` | 4 |
| 100 | `Map` | — | `map.svg` | Mapa de zona | Pedidos y Reparto | `phosphor:map-trifold` | 4 |
| 101 | `PackageOpen` | — | `package-open.svg` | Insumo abierto | Pedidos y Reparto | `phosphor:archive` | 4 |
| 102 | `Send` | — | `send.svg` | Enviar mensaje | Interfaz y Alertas | `phosphor:paper-plane-tilt` | 4 |
| 103 | `Settings2` | — | `settings-2.svg` | Parámetros avanzados | Usuarios y Ajustes | `phosphor:sliders` | 4 |
| 104 | `SplitSquareHorizontal` | — | `split-square-horizontal.svg` | Mitad y mitad | Pedidos y Reparto | `phosphor:columns` | 4 |
| 105 | `StickyNote` | — | `sticky-note.svg` | Nota adhesiva | Interfaz y Alertas | `phosphor:note` | 4 |
| 106 | `UserCheck` | — | `user-check.svg` | Asistencia confirmada | Usuarios y Ajustes | `phosphor:user-check` | 4 |
| 107 | `UserPlus` | — | `user-plus.svg` | Nuevo cliente | Usuarios y Ajustes | `phosphor:user-plus` | 4 |
| 108 | `Wifi` | — | `wifi.svg` | Red Wi-Fi activa | Usuarios y Ajustes | `phosphor:wifi-high` | 4 |
| 109 | `AlertOctagon` | — | `alert-octagon.svg` | Alerta crítica | Caja y Comercio | `phosphor:warning-octagon` | 3 |
| 110 | `ArrowUp` | — | `arrow-up.svg` | Flecha arriba | Navegación | `phosphor:arrow-up` | 3 |
| 111 | `Bot` | — | `bot.svg` | Asistente IA | Interfaz y Alertas | `phosphor:robot` | 3 |
| 112 | `CheckCheck` | — | `check-check.svg` | Leído doble | Interfaz y Alertas | `phosphor:checks` | 3 |
| 113 | `Hourglass` | — | `hourglass.svg` | En espera | Pedidos y Reparto | `phosphor:hourglass` | 3 |
| 114 | `Landmark` | — | `landmark.svg` | Transferencia bancaria | Caja y Comercio | `phosphor:bank` | 3 |
| 115 | `Mail` | — | `mail.svg` | Correo electrónico | Interfaz y Alertas | `phosphor:envelope-simple` | 3 |
| 116 | `Maximize2` | — | `maximize-2.svg` | Pantalla completa | Navegación | `phosphor:arrows-out-simple` | 3 |
| 117 | `MoreHorizontal` | `MoreHorizontalIcon` | `more-horizontal.svg` | Más acciones | Interfaz y Alertas | `phosphor:dots-three` | 3 |
| 118 | `Rocket` | — | `rocket.svg` | Despliegue rápido | Interfaz y Alertas | `phosphor:rocket-launch` | 3 |
| 119 | `ShieldX` | — | `shield-x.svg` | Sin autorización | Usuarios y Ajustes | `phosphor:shield-slash` | 3 |
| 120 | `Trash` | — | `trash.svg` | Papelera simple | Interfaz y Alertas | `phosphor:trash-simple` | 3 |
| 121 | `ArrowDown` | — | `arrow-down.svg` | Flecha abajo | Navegación | `phosphor:arrow-down` | 2 |
| 122 | `ArrowUpCircle` | — | `arrow-up-circle.svg` | Subir nivel | Navegación | `phosphor:arrow-circle-up` | 2 |
| 123 | `ArrowUpRight` | — | `arrow-up-right.svg` | Abrir externo | Navegación | `phosphor:arrow-up-right` | 2 |
| 124 | `Boxes` | — | `boxes.svg` | Lotes e inventario | Pedidos y Reparto | `phosphor:shipping-container` | 2 |
| 125 | `CalendarOff` | — | `calendar-off.svg` | Día cerrado | Interfaz y Alertas | `phosphor:calendar-x` | 2 |
| 126 | `Camera` | — | `camera.svg` | Cámara | Interfaz y Alertas | `phosphor:camera` | 2 |
| 127 | `Cloud` | — | `cloud.svg` | Sincronizado nube | Interfaz y Alertas | `phosphor:cloud` | 2 |
| 128 | `Crosshair` | — | `crosshair.svg` | Centrar GPS | Pedidos y Reparto | `phosphor:crosshair` | 2 |
| 129 | `GripVertical` | — | `grip-vertical.svg` | Arrastrar orden | Interfaz y Alertas | `phosphor:dots-six-vertical` | 2 |
| 130 | `HelpCircle` | — | `help-circle.svg` | Ayuda contextual | Interfaz y Alertas | `phosphor:question` | 2 |
| 131 | `Link2` | — | `link-2.svg` | Enlace público | Interfaz y Alertas | `phosphor:link-simple` | 2 |
| 132 | `List` | — | `list.svg` | Vista de lista | Navegación | `phosphor:list-bullets` | 2 |
| 133 | `LocateFixed` | — | `locate-fixed.svg` | GPS activo | Pedidos y Reparto | `phosphor:gps-fix` | 2 |
| 134 | `MapPinned` | — | `map-pinned.svg` | Zona confirmada | Pedidos y Reparto | `phosphor:map-pin-line` | 2 |
| 135 | `Megaphone` | — | `megaphone.svg` | Aviso y campaña | Interfaz y Alertas | `phosphor:megaphone` | 2 |
| 136 | `Menu` | — | `menu.svg` | Menú principal | Navegación | `phosphor:list` | 2 |
| 137 | `Music` | — | `music.svg` | Sonido de alerta | Interfaz y Alertas | `phosphor:music-notes` | 2 |
| 138 | `PackageCheck` | — | `package-check.svg` | Recepción de compra | Pedidos y Reparto | `phosphor:box-arrow-down` | 2 |
| 139 | `RotateCw` | — | `rotate-cw.svg` | Reintentar envío | Interfaz y Alertas | `phosphor:arrow-clockwise` | 2 |
| 140 | `Shield` | — | `shield.svg` | Rol y permiso | Usuarios y Ajustes | `phosphor:shield` | 2 |
| 141 | `Table2` | — | `table-2.svg` | Vista tabular | Navegación | `phosphor:table` | 2 |
| 142 | `Type` | — | `type.svg` | Tipografía de ticket | Usuarios y Ajustes | `phosphor:text-t` | 2 |
| 143 | `Unlock` | — | `unlock.svg` | Caja abierta | Usuarios y Ajustes | `phosphor:lock-open` | 2 |
| 144 | `UserCircle` | — | `user-circle.svg` | Perfil de cuenta | Usuarios y Ajustes | `phosphor:user-circle` | 2 |
| 145 | `ArrowDownRight` | — | `arrow-down-right.svg` | Salida diagonal | Navegación | `phosphor:arrow-down-right` | 1 |
| 146 | `Blend` | — | `blend.svg` | Combinar mitades | Interfaz y Alertas | `phosphor:intersect` | 1 |
| 147 | `Bold` | — | `bold.svg` | Texto en negrita | Usuarios y Ajustes | `phosphor:text-b` | 1 |
| 148 | `Building` | — | `building.svg` | Sucursal | Usuarios y Ajustes | `phosphor:building-office` | 1 |
| 149 | `Building2` | — | `building-2.svg` | Multi-sucursal | Interfaz y Alertas | `phosphor:buildings` | 1 |
| 150 | `ChevronsUpDown` | — | `chevrons-up-down.svg` | Selector desplegable | Navegación | `phosphor:caret-up-down` | 1 |
| 151 | `Circle` | — | `circle.svg` | Indicador radio | Interfaz y Alertas | `phosphor:circle` | 1 |
| 152 | `ClipboardCheck` | — | `clipboard-check.svg` | Auditoría validada | Interfaz y Alertas | `phosphor:clipboard-text` | 1 |
| 153 | `CloudOff` | — | `cloud-off.svg` | Modo sin conexión | Interfaz y Alertas | `phosphor:cloud-slash` | 1 |
| 154 | `Coffee` | — | `coffee.svg` | Bebidas calientes | Pedidos y Reparto | `phosphor:coffee` | 1 |
| 155 | `Coins` | — | `coins.svg` | Monedas y morralla | Caja y Comercio | `phosphor:coins` | 1 |
| 156 | `FileImage` | — | `file-image.svg` | Archivo de imagen | Interfaz y Alertas | `phosphor:file-image` | 1 |
| 157 | `Gift` | — | `gift.svg` | Promoción y regalo | Caja y Comercio | `phosphor:gift` | 1 |
| 158 | `Grid2X2` | — | `grid-2-x-2.svg` | Cuadrícula compacta | Navegación | `phosphor:squares-four` | 1 |
| 159 | `Hash` | — | `hash.svg` | Folio numérico | Interfaz y Alertas | `phosphor:hash` | 1 |
| 160 | `Inbox` | — | `inbox.svg` | Bandeja de entrada | Interfaz y Alertas | `phosphor:tray` | 1 |
| 161 | `LayoutDashboard` | — | `layout-dashboard.svg` | Tablero operativo | Navegación | `phosphor:gauge` | 1 |
| 162 | `Minimize2` | — | `minimize-2.svg` | Reducir vista | Navegación | `phosphor:arrows-in-simple` | 1 |
| 163 | `MoreVertical` | — | `more-vertical.svg` | Opciones de fila | Interfaz y Alertas | `phosphor:dots-three-vertical` | 1 |
| 164 | `MousePointerClick` | — | `mouse-pointer-click.svg` | Selección rápida | Interfaz y Alertas | `phosphor:cursor-click` | 1 |
| 165 | `NotebookText` | — | `notebook-text.svg` | Recetario BOM | Interfaz y Alertas | `phosphor:notebook` | 1 |
| 166 | `OctagonX` | `OctagonXIcon` | `octagon-x.svg` | Error bloqueante | Caja y Comercio | `phosphor:x-square` | 1 |
| 167 | `PackageMinus` | — | `package-minus.svg` | Merma o salida | Pedidos y Reparto | `phosphor:cube-focus` | 1 |
| 168 | `PackagePlus` | — | `package-plus.svg` | Alta de insumo | Pedidos y Reparto | `phosphor:box-arrow-up` | 1 |
| 169 | `Paintbrush` | — | `paintbrush.svg` | Personalizar estilo | Usuarios y Ajustes | `phosphor:paint-brush` | 1 |
| 170 | `PanelLeft` | — | `panel-left.svg` | Barra lateral | Navegación | `phosphor:sidebar-simple` | 1 |
| 171 | `Percent` | — | `percent.svg` | Descuento porcentual | Caja y Comercio | `phosphor:percent` | 1 |
| 172 | `PieChart` | — | `pie-chart.svg` | Distribución de ventas | Caja y Comercio | `phosphor:chart-pie-slice` | 1 |
| 173 | `Pin` | — | `pin.svg` | Fijar marcador | Interfaz y Alertas | `phosphor:push-pin` | 1 |
| 174 | `Plug` | — | `plug.svg` | Conectar periférico | Usuarios y Ajustes | `phosphor:plug` | 1 |
| 175 | `PlusCircle` | — | `plus-circle.svg` | Nuevo registro | Interfaz y Alertas | `phosphor:plus-circle` | 1 |
| 176 | `Puzzle` | — | `puzzle.svg` | Extensión | Interfaz y Alertas | `phosphor:puzzle-piece` | 1 |
| 177 | `Radio` | — | `radio.svg` | Transmisión en vivo | Interfaz y Alertas | `phosphor:broadcast` | 1 |
| 178 | `Route` | — | `route.svg` | Trazo de ruta | Pedidos y Reparto | `phosphor:path` | 1 |
| 179 | `Scale` | — | `scale.svg` | Báscula y gramaje | Caja y Comercio | `phosphor:scales` | 1 |
| 180 | `Share2` | — | `share-2.svg` | Compartir enlace | Interfaz y Alertas | `phosphor:share-network` | 1 |
| 181 | `ShieldAlert` | — | `shield-alert.svg` | Alerta de seguridad | Usuarios y Ajustes | `phosphor:shield-warning` | 1 |
| 182 | `Shuffle` | — | `shuffle.svg` | Orden aleatorio | Interfaz y Alertas | `phosphor:shuffle` | 1 |
| 183 | `Signal` | — | `signal.svg` | Señal excelente | Usuarios y Ajustes | `phosphor:cell-signal-full` | 1 |
| 184 | `SignalZero` | — | `signal-zero.svg` | Sin señal móvil | Usuarios y Ajustes | `phosphor:cell-signal-none` | 1 |
| 185 | `Space` | — | `space.svg` | Espaciado de ticket | Usuarios y Ajustes | `phosphor:brackets-square` | 1 |
| 186 | `Sunset` | — | `sunset.svg` | Corte vespertino | Usuarios y Ajustes | `phosphor:sun-horizon` | 1 |
| 187 | `Target` | — | `target.svg` | Meta de ventas | Interfaz y Alertas | `phosphor:target` | 1 |
| 188 | `TestTube` | — | `test-tube.svg` | Prueba diagnóstica | Interfaz y Alertas | `phosphor:flask` | 1 |
| 189 | `ToggleLeft` | — | `toggle-left.svg` | Interruptor | Interfaz y Alertas | `phosphor:toggle-left` | 1 |
| 190 | `ToggleRight` | — | `toggle-right.svg` | Opción activa | Interfaz y Alertas | `phosphor:toggle-right` | 1 |
| 191 | `Tv` | — | `tv.svg` | Pantalla TV cocina | Usuarios y Ajustes | `phosphor:television` | 1 |
| 192 | `Unplug` | — | `unplug.svg` | Reconectar servicio | Usuarios y Ajustes | `phosphor:plugs-connected` | 1 |
| 193 | `Usb` | — | `usb.svg` | Puerto USB ESC/POS | Usuarios y Ajustes | `phosphor:usb` | 1 |
| 194 | `UserX` | — | `user-x.svg` | Baja de usuario | Usuarios y Ajustes | `phosphor:user-minus` | 1 |
| 195 | `Utensils` | — | `utensils.svg` | Cubiertos y comedor | Pedidos y Reparto | `phosphor:bowl-food` | 1 |
| 196 | `ZoomIn` | — | `zoom-in.svg` | Acercar vista | Navegación | `phosphor:magnifying-glass-plus` | 1 |
| 197 | `CupSoda` | — | `cup-soda.svg` | Refrescos y bebidas | Pedidos y Reparto | `phosphor:pint-glass` | 0 |

---

## 3. Los `46` Iconos Complementarios Incluidos (`2` Giro + `44` Esenciales Base)

| # | Slug en `icons/*/` | Nombre (`IuSoftIconName`) | Nombre en español | Categoría | Fuente base |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `airplane.svg` | `Airplane` | Avión | Interfaz y Alertas | `phosphor:airplane-tilt` |
| 2 | `anchor.svg` | `Anchor` | Ancla | Interfaz y Alertas | `phosphor:anchor` |
| 3 | `balloon.svg` | `Balloon` | Globo festivo | Interfaz y Alertas | `phosphor:balloon` |
| 4 | `beach.svg` | `Beach` | Sombrilla de playa | Interfaz y Alertas | `phosphor:island` |
| 5 | `bed.svg` | `Bed` | Hospedaje | Interfaz y Alertas | `phosphor:bed` |
| 6 | `bell.svg` | `Bell` | Campana de aviso | Interfaz y Alertas | `phosphor:bell` |
| 7 | `bone.svg` | `Bone` | Mascota | Interfaz y Alertas | `phosphor:bone` |
| 8 | `book.svg` | `Book` | Manual operativo | Interfaz y Alertas | `phosphor:book-open` |
| 9 | `bookmark.svg` | `Bookmark` | Marcador guardado | Interfaz y Alertas | `phosphor:bookmark-simple` |
| 10 | `broom.svg` | `Broom` | Limpieza de turno | Interfaz y Alertas | `phosphor:broom` |
| 11 | `campfire.svg` | `Campfire` | Fogata a la leña | Pedidos y Reparto | `phosphor:campfire` |
| 12 | `confetti.svg` | `Confetti` | Celebración | Interfaz y Alertas | `phosphor:confetti` |
| 13 | `cube.svg` | `Cube` | Cubo 3D | Interfaz y Alertas | `phosphor:cube` |
| 14 | `diamond.svg` | `Diamond` | Calidad premium | Caja y Comercio | `phosphor:sketch-logo` |
| 15 | `door.svg` | `Door` | Puerta de acceso | Navegación | `phosphor:door-open` |
| 16 | `drop.svg` | `Drop` | Gota e insumo líquido | Interfaz y Alertas | `phosphor:drop` |
| 17 | `dumbbell.svg` | `Dumbbell` | Esfuerzo | Interfaz y Alertas | `phosphor:barbell` |
| 18 | `earth.svg` | `Earth` | Planeta | Interfaz y Alertas | `phosphor:globe` |
| 19 | `emoji.svg` | `Emoji` | Cliente satisfecho | Interfaz y Alertas | `phosphor:smiley` |
| 20 | `emoji-laugh.svg` | `EmojiLaugh` | Reseña excelente | Interfaz y Alertas | `phosphor:smiley-wink` |
| 21 | `eraser.svg` | `Eraser` | Borrador | Interfaz y Alertas | `phosphor:eraser` |
| 22 | `fan.svg` | `Fan` | Ventilación cocina | Interfaz y Alertas | `phosphor:fan` |
| 23 | `feather.svg` | `Feather` | Ligero | Interfaz y Alertas | `phosphor:feather` |
| 24 | `flashlight.svg` | `Flashlight` | Linterna nocturna | Pedidos y Reparto | `phosphor:flashlight` |
| 25 | `gas.svg` | `Gas` | Gasolina de moto | Pedidos y Reparto | `phosphor:gas-pump` |
| 26 | `ghost.svg` | `Ghost` | Fantasma | Interfaz y Alertas | `phosphor:ghost` |
| 27 | `glasses.svg` | `Glasses` | Revisión y auditoría | Interfaz y Alertas | `phosphor:eyeglasses` |
| 28 | `handshake.svg` | `Handshake` | Acuerdo con proveedor | Interfaz y Alertas | `phosphor:handshake` |
| 29 | `headphones.svg` | `Headphones` | Audio | Usuarios y Ajustes | `phosphor:headphones` |
| 30 | `headset.svg` | `Headset` | Telefonista y soporte | Usuarios y Ajustes | `phosphor:headset` |
| 31 | `heart.svg` | `Heart` | Favorito del cliente | Interfaz y Alertas | `phosphor:heart` |
| 32 | `ice-cream.svg` | `IceCream` | Postres y helados | Pedidos y Reparto | `phosphor:ice-cream` |
| 33 | `laptop.svg` | `Laptop` | Consola portátil | Usuarios y Ajustes | `phosphor:laptop` |
| 34 | `lasso.svg` | `Lasso` | Selección libre | Interfaz y Alertas | `phosphor:lasso` |
| 35 | `leaf.svg` | `Leaf` | Ingrediente fresco | Pedidos y Reparto | `phosphor:leaf` |
| 36 | `lightbulb.svg` | `Lightbulb` | Idea y sugerencia | Interfaz y Alertas | `phosphor:lightbulb` |
| 37 | `magnet.svg` | `Magnet` | Retención de clientes | Interfaz y Alertas | `phosphor:magnet` |
| 38 | `parachute.svg` | `Parachute` | Entrega segura | Interfaz y Alertas | `phosphor:parachute` |
| 39 | `pizza-cutter.svg` | `pizza-cutter` | Cortador de pizza | Giro Pizzería | `dsl:pizza-cutter` |
| 40 | `pizza-whole.svg` | `pizza-whole` | Pizza entera | Giro Pizzería | `dsl:pizza-whole` |
| 41 | `sailboat.svg` | `Sailboat` | Velero | Interfaz y Alertas | `phosphor:sailboat` |
| 42 | `saved.svg` | `Saved` | Casilla verificada | Interfaz y Alertas | `phosphor:check-square` |
| 43 | `scooter.svg` | `Scooter` | Patín de reparto | Pedidos y Reparto | `phosphor:scooter` |
| 44 | `trophy.svg` | `Trophy` | Meta cumplida | Caja y Comercio | `phosphor:trophy` |
| 45 | `umbrella.svg` | `Umbrella` | Lluvia en ruta | Pedidos y Reparto | `phosphor:umbrella` |
| 46 | `windmill.svg` | `Windmill` | Molino artesanal | Interfaz y Alertas | `phosphor:windmill` |
