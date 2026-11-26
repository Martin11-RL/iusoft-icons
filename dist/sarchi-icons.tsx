"use client";

import * as React from "react";
import {
  IuSoftIcon,
  CONTEXTUAL_PALETTES,
  IUSOFT_SURFACE_CSS,
  IUSOFT_SURFACE_TOKENS,
  type IuSoftIconName,
  type IuSoftIconSurface,
  type IuSoftIconTone,
  type IuSoftIconVariant,
  type IuSoftPaletteId,
} from "./iusoft-icons-react";

export { IuSoftIcon, CONTEXTUAL_PALETTES, IUSOFT_SURFACE_CSS, IUSOFT_SURFACE_TOKENS };
export type { IuSoftIconName, IuSoftIconSurface, IuSoftIconTone, IuSoftIconVariant, IuSoftPaletteId };

export interface LucideProps extends Omit<React.SVGProps<SVGSVGElement>, "name"> {
  size?: string | number;
  strokeWidth?: string | number;
  absoluteStrokeWidth?: boolean;
  variant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  tone?: IuSoftIconTone;
  animate?: "hover" | "none";
}

export type SarchiLucideIcon = React.ForwardRefExoticComponent<
  LucideProps & React.RefAttributes<SVGSVGElement>
>;
export type LucideIcon = SarchiLucideIcon;

interface SarchiIconContextValue {
  defaultVariant: IuSoftIconVariant | "auto";
  surface: IuSoftIconSurface;
  tone: IuSoftIconTone;
}

const SarchiIconContext = React.createContext<SarchiIconContextValue>({
  defaultVariant: "auto",
  surface: "auto",
  tone: "contextual",
});

export interface SarchiIconProviderProps {
  defaultVariant?: IuSoftIconVariant | "auto";
  surface?: IuSoftIconSurface;
  tone?: IuSoftIconTone;
  children: React.ReactNode;
}

export function SarchiIconProvider({
  defaultVariant = "auto",
  surface = "auto",
  tone = "contextual",
  children,
}: SarchiIconProviderProps) {
  const value = React.useMemo(
    () => ({ defaultVariant, surface, tone }),
    [defaultVariant, surface, tone]
  );
  return (
    <SarchiIconContext.Provider value={value}>
      <style dangerouslySetInnerHTML={{ __html: IUSOFT_SURFACE_CSS }} />
      {children}
    </SarchiIconContext.Provider>
  );
}

function resolveSmartVariant(
  explicitVariant: IuSoftIconVariant | "auto" | undefined,
  ctxVariant: IuSoftIconVariant | "auto",
  forcedDefault: IuSoftIconVariant | undefined,
  size: string | number | undefined,
  className: string | undefined
): IuSoftIconVariant {
  if (explicitVariant && explicitVariant !== "auto") return explicitVariant;
  if (forcedDefault) return forcedDefault;
  const cls = className || "";
  if (cls.includes("animate-spin")) return "outline";
  const targetMode = explicitVariant || ctxVariant;
  if (targetMode !== "auto") return targetMode;

  // Regla GPU y nitidez Sarchi: iconos compactos (size <= 15 o clases size/w/h 0.5..3.5 / px) usan outline 0-blur
  if (typeof size === "number" && size <= 15) return "outline";
  if (/\b(?:size|w|h)-(?:0\.5|1(?:\.5)?|2(?:\.5)?|3(?:\.5)?|px)\b/.test(cls)) return "outline";
  return "glass";
}

function createSarchiIcon(
  slug: IuSoftIconName,
  displayName: string,
  forcedDefault?: IuSoftIconVariant
): SarchiLucideIcon {
  const Comp = React.forwardRef<SVGSVGElement, LucideProps>(function SarchiBoundIcon(
    {
      variant,
      surface,
      tone,
      size = 24,
      className,
      strokeWidth: _sw,
      absoluteStrokeWidth: _asw,
      animate = "hover",
      ...rest
    },
    _ref
  ) {
    const ctx = React.useContext(SarchiIconContext);
    const resolvedVariant = resolveSmartVariant(variant, ctx.defaultVariant, forcedDefault, size, className);
    const resolvedSurface = surface || ctx.surface;
    const resolvedTone = tone || ctx.tone;
    return (
      <IuSoftIcon
        ref={_ref}
        name={slug}
        variant={resolvedVariant}
        surface={resolvedSurface}
        tone={resolvedTone}
        size={size}
        className={className}
        animate={clsHasSpin(className) ? "none" : animate}
        {...rest}
      />
    );
  });
  Comp.displayName = displayName;
  return Comp;
}

function clsHasSpin(cls?: string): boolean {
  return Boolean(cls && cls.includes("animate-spin"));
}

// === 281 Símbolos Drop-In Compatibles con `lucide-react` para Sarchi Pizza POS ===
export const Printer: SarchiLucideIcon = createSarchiIcon("printer", "Printer", undefined);
export const Bike: SarchiLucideIcon = createSarchiIcon("bike", "Bike", undefined);
export const Pizza: SarchiLucideIcon = createSarchiIcon("pizza", "Pizza", undefined);
export const Flame: SarchiLucideIcon = createSarchiIcon("flame", "Flame", undefined);
export const Loader2: SarchiLucideIcon = createSarchiIcon("loader-2", "Loader2", "outline");
export const Loader2Icon: SarchiLucideIcon = createSarchiIcon("loader-2", "Loader2Icon", "outline");
export const Plus: SarchiLucideIcon = createSarchiIcon("plus", "Plus", "outline");
export const MapPin: SarchiLucideIcon = createSarchiIcon("map-pin", "MapPin", undefined);
export const CheckCircle2: SarchiLucideIcon = createSarchiIcon("check-circle-2", "CheckCircle2", undefined);
export const CheckCircle: SarchiLucideIcon = createSarchiIcon("check-circle-2", "CheckCircle", undefined);
export const CircleCheck: SarchiLucideIcon = createSarchiIcon("check-circle-2", "CircleCheck", undefined);
export const CircleCheckIcon: SarchiLucideIcon = createSarchiIcon("check-circle-2", "CircleCheckIcon", undefined);
export const RefreshCw: SarchiLucideIcon = createSarchiIcon("refresh-cw", "RefreshCw", undefined);
export const Trash2: SarchiLucideIcon = createSarchiIcon("trash-2", "Trash2", undefined);
export const Clock: SarchiLucideIcon = createSarchiIcon("clock", "Clock", undefined);
export const Clock2: SarchiLucideIcon = createSarchiIcon("clock", "Clock2", undefined);
export const Check: SarchiLucideIcon = createSarchiIcon("check", "Check", "outline");
export const CheckIcon: SarchiLucideIcon = createSarchiIcon("check", "CheckIcon", "outline");
export const X: SarchiLucideIcon = createSarchiIcon("x", "X", "outline");
export const XIcon: SarchiLucideIcon = createSarchiIcon("x", "XIcon", "outline");
export const AlertTriangle: SarchiLucideIcon = createSarchiIcon("alert-triangle", "AlertTriangle", undefined);
export const TriangleAlert: SarchiLucideIcon = createSarchiIcon("alert-triangle", "TriangleAlert", undefined);
export const TriangleAlertIcon: SarchiLucideIcon = createSarchiIcon("alert-triangle", "TriangleAlertIcon", undefined);
export const Truck: SarchiLucideIcon = createSarchiIcon("truck", "Truck", undefined);
export const AlertCircle: SarchiLucideIcon = createSarchiIcon("alert-circle", "AlertCircle", undefined);
export const Package: SarchiLucideIcon = createSarchiIcon("package", "Package", undefined);
export const Banknote: SarchiLucideIcon = createSarchiIcon("banknote", "Banknote", undefined);
export const Search: SarchiLucideIcon = createSarchiIcon("search", "Search", undefined);
export const SearchIcon: SarchiLucideIcon = createSarchiIcon("search", "SearchIcon", undefined);
export const QrCode: SarchiLucideIcon = createSarchiIcon("qr-code", "QrCode", undefined);
export const FileText: SarchiLucideIcon = createSarchiIcon("file-text", "FileText", undefined);
export const Lock: SarchiLucideIcon = createSarchiIcon("lock", "Lock", undefined);
export const Phone: SarchiLucideIcon = createSarchiIcon("phone", "Phone", undefined);
export const Smartphone: SarchiLucideIcon = createSarchiIcon("smartphone", "Smartphone", undefined);
export const ExternalLink: SarchiLucideIcon = createSarchiIcon("external-link", "ExternalLink", undefined);
export const Download: SarchiLucideIcon = createSarchiIcon("download", "Download", undefined);
export const ChevronRight: SarchiLucideIcon = createSarchiIcon("chevron-right", "ChevronRight", "outline");
export const ChevronRightIcon: SarchiLucideIcon = createSarchiIcon("chevron-right", "ChevronRightIcon", "outline");
export const CreditCard: SarchiLucideIcon = createSarchiIcon("credit-card", "CreditCard", undefined);
export const History: SarchiLucideIcon = createSarchiIcon("history", "History", undefined);
export const User: SarchiLucideIcon = createSarchiIcon("user", "User", undefined);
export const Users: SarchiLucideIcon = createSarchiIcon("users", "Users", undefined);
export const KeyRound: SarchiLucideIcon = createSarchiIcon("key-round", "KeyRound", undefined);
export const Pencil: SarchiLucideIcon = createSarchiIcon("pencil", "Pencil", undefined);
export const Copy: SarchiLucideIcon = createSarchiIcon("copy", "Copy", undefined);
export const DollarSign: SarchiLucideIcon = createSarchiIcon("dollar-sign", "DollarSign", undefined);
export const Eye: SarchiLucideIcon = createSarchiIcon("eye", "Eye", undefined);
export const Sparkles: SarchiLucideIcon = createSarchiIcon("sparkles", "Sparkles", undefined);
export const Wallet: SarchiLucideIcon = createSarchiIcon("wallet", "Wallet", undefined);
export const MessageCircle: SarchiLucideIcon = createSarchiIcon("message-circle", "MessageCircle", undefined);
export const ChevronDown: SarchiLucideIcon = createSarchiIcon("chevron-down", "ChevronDown", "outline");
export const ChevronDownIcon: SarchiLucideIcon = createSarchiIcon("chevron-down", "ChevronDownIcon", "outline");
export const Info: SarchiLucideIcon = createSarchiIcon("info", "Info", undefined);
export const InfoIcon: SarchiLucideIcon = createSarchiIcon("info", "InfoIcon", undefined);
export const Save: SarchiLucideIcon = createSarchiIcon("save", "Save", undefined);
export const ShieldCheck: SarchiLucideIcon = createSarchiIcon("shield-check", "ShieldCheck", undefined);
export const Store: SarchiLucideIcon = createSarchiIcon("store", "Store", undefined);
export const TrendingUp: SarchiLucideIcon = createSarchiIcon("trending-up", "TrendingUp", undefined);
export const ArrowLeft: SarchiLucideIcon = createSarchiIcon("arrow-left", "ArrowLeft", undefined);
export const Key: SarchiLucideIcon = createSarchiIcon("key", "Key", undefined);
export const LayoutGrid: SarchiLucideIcon = createSarchiIcon("layout-grid", "LayoutGrid", undefined);
export const Navigation: SarchiLucideIcon = createSarchiIcon("navigation", "Navigation", undefined);
export const Calendar: SarchiLucideIcon = createSarchiIcon("calendar", "Calendar", undefined);
export const CalendarIcon: SarchiLucideIcon = createSarchiIcon("calendar", "CalendarIcon", undefined);
export const MapPinOff: SarchiLucideIcon = createSarchiIcon("map-pin-off", "MapPinOff", undefined);
export const Receipt: SarchiLucideIcon = createSarchiIcon("receipt", "Receipt", undefined);
export const ShoppingBag: SarchiLucideIcon = createSarchiIcon("shopping-bag", "ShoppingBag", undefined);
export const Tag: SarchiLucideIcon = createSarchiIcon("tag", "Tag", undefined);
export const Zap: SarchiLucideIcon = createSarchiIcon("zap", "Zap", undefined);
export const Calculator: SarchiLucideIcon = createSarchiIcon("calculator", "Calculator", undefined);
export const CalendarDays: SarchiLucideIcon = createSarchiIcon("calendar-days", "CalendarDays", undefined);
export const Edit: SarchiLucideIcon = createSarchiIcon("edit", "Edit", undefined);
export const Edit2: SarchiLucideIcon = createSarchiIcon("edit", "Edit2", undefined);
export const Edit3: SarchiLucideIcon = createSarchiIcon("edit", "Edit3", undefined);
export const SquarePen: SarchiLucideIcon = createSarchiIcon("edit", "SquarePen", undefined);
export const Power: SarchiLucideIcon = createSarchiIcon("power", "Power", undefined);
export const RotateCcw: SarchiLucideIcon = createSarchiIcon("rotate-ccw", "RotateCcw", undefined);
export const ShoppingCart: SarchiLucideIcon = createSarchiIcon("shopping-cart", "ShoppingCart", undefined);
export const ArrowRight: SarchiLucideIcon = createSarchiIcon("arrow-right", "ArrowRight", undefined);
export const Bluetooth: SarchiLucideIcon = createSarchiIcon("bluetooth", "Bluetooth", undefined);
export const ChefHat: SarchiLucideIcon = createSarchiIcon("chef-hat", "ChefHat", undefined);
export const ChevronLeft: SarchiLucideIcon = createSarchiIcon("chevron-left", "ChevronLeft", "outline");
export const ChevronLeftIcon: SarchiLucideIcon = createSarchiIcon("chevron-left", "ChevronLeftIcon", "outline");
export const ClipboardList: SarchiLucideIcon = createSarchiIcon("clipboard-list", "ClipboardList", undefined);
export const EyeOff: SarchiLucideIcon = createSarchiIcon("eye-off", "EyeOff", undefined);
export const PowerOff: SarchiLucideIcon = createSarchiIcon("power-off", "PowerOff", undefined);
export const UtensilsCrossed: SarchiLucideIcon = createSarchiIcon("utensils-crossed", "UtensilsCrossed", undefined);
export const XCircle: SarchiLucideIcon = createSarchiIcon("xcircle", "XCircle", undefined);
export const BarChart3: SarchiLucideIcon = createSarchiIcon("bar-chart-3", "BarChart3", undefined);
export const Briefcase: SarchiLucideIcon = createSarchiIcon("briefcase", "Briefcase", undefined);
export const Bug: SarchiLucideIcon = createSarchiIcon("bug", "Bug", undefined);
export const CalendarClock: SarchiLucideIcon = createSarchiIcon("calendar-clock", "CalendarClock", undefined);
export const Layers: SarchiLucideIcon = createSarchiIcon("layers", "Layers", undefined);
export const LogOut: SarchiLucideIcon = createSarchiIcon("log-out", "LogOut", undefined);
export const MessageSquare: SarchiLucideIcon = createSarchiIcon("message-square", "MessageSquare", undefined);
export const Minus: SarchiLucideIcon = createSarchiIcon("minus", "Minus", "outline");
export const SlidersHorizontal: SarchiLucideIcon = createSarchiIcon("sliders-horizontal", "SlidersHorizontal", undefined);
export const Star: SarchiLucideIcon = createSarchiIcon("star", "Star", undefined);
export const Sun: SarchiLucideIcon = createSarchiIcon("sun", "Sun", undefined);
export const TrendingDown: SarchiLucideIcon = createSarchiIcon("trending-down", "TrendingDown", undefined);
export const Chrome: SarchiLucideIcon = createSarchiIcon("chrome", "Chrome", undefined);
export const Globe: SarchiLucideIcon = createSarchiIcon("globe", "Globe", undefined);
export const Image: SarchiLucideIcon = createSarchiIcon("image", "Image", undefined);
export const ImageIcon: SarchiLucideIcon = createSarchiIcon("image", "ImageIcon", undefined);
export const Monitor: SarchiLucideIcon = createSarchiIcon("monitor", "Monitor", undefined);
export const Settings: SarchiLucideIcon = createSarchiIcon("settings", "Settings", undefined);
export const Upload: SarchiLucideIcon = createSarchiIcon("upload", "Upload", undefined);
export const WifiOff: SarchiLucideIcon = createSarchiIcon("wifi-off", "WifiOff", undefined);
export const Ban: SarchiLucideIcon = createSarchiIcon("ban", "Ban", undefined);
export const FolderOpen: SarchiLucideIcon = createSarchiIcon("folder-open", "FolderOpen", undefined);
export const Moon: SarchiLucideIcon = createSarchiIcon("moon", "Moon", undefined);
export const Palette: SarchiLucideIcon = createSarchiIcon("palette", "Palette", undefined);
export const Timer: SarchiLucideIcon = createSarchiIcon("timer", "Timer", undefined);
export const ArrowRightLeft: SarchiLucideIcon = createSarchiIcon("arrow-right-left", "ArrowRightLeft", undefined);
export const ArrowLeftRight: SarchiLucideIcon = createSarchiIcon("arrow-right-left", "ArrowLeftRight", undefined);
export const ArrowUpDown: SarchiLucideIcon = createSarchiIcon("arrow-up-down", "ArrowUpDown", "outline");
export const ChevronUp: SarchiLucideIcon = createSarchiIcon("chevron-up", "ChevronUp", "outline");
export const Filter: SarchiLucideIcon = createSarchiIcon("filter", "Filter", undefined);
export const Home: SarchiLucideIcon = createSarchiIcon("home", "Home", undefined);
export const Map: SarchiLucideIcon = createSarchiIcon("map", "Map", undefined);
export const PackageOpen: SarchiLucideIcon = createSarchiIcon("package-open", "PackageOpen", undefined);
export const Send: SarchiLucideIcon = createSarchiIcon("send", "Send", undefined);
export const Settings2: SarchiLucideIcon = createSarchiIcon("settings-2", "Settings2", undefined);
export const SplitSquareHorizontal: SarchiLucideIcon = createSarchiIcon("split-square-horizontal", "SplitSquareHorizontal", undefined);
export const StickyNote: SarchiLucideIcon = createSarchiIcon("sticky-note", "StickyNote", undefined);
export const UserCheck: SarchiLucideIcon = createSarchiIcon("user-check", "UserCheck", undefined);
export const UserPlus: SarchiLucideIcon = createSarchiIcon("user-plus", "UserPlus", undefined);
export const Wifi: SarchiLucideIcon = createSarchiIcon("wifi", "Wifi", undefined);
export const AlertOctagon: SarchiLucideIcon = createSarchiIcon("alert-octagon", "AlertOctagon", undefined);
export const ArrowUp: SarchiLucideIcon = createSarchiIcon("arrow-up", "ArrowUp", undefined);
export const Bot: SarchiLucideIcon = createSarchiIcon("bot", "Bot", undefined);
export const CheckCheck: SarchiLucideIcon = createSarchiIcon("check-check", "CheckCheck", "outline");
export const Hourglass: SarchiLucideIcon = createSarchiIcon("hourglass", "Hourglass", undefined);
export const Landmark: SarchiLucideIcon = createSarchiIcon("landmark", "Landmark", undefined);
export const Mail: SarchiLucideIcon = createSarchiIcon("mail", "Mail", undefined);
export const Maximize2: SarchiLucideIcon = createSarchiIcon("maximize-2", "Maximize2", undefined);
export const MoreHorizontal: SarchiLucideIcon = createSarchiIcon("more-horizontal", "MoreHorizontal", "outline");
export const MoreHorizontalIcon: SarchiLucideIcon = createSarchiIcon("more-horizontal", "MoreHorizontalIcon", "outline");
export const Rocket: SarchiLucideIcon = createSarchiIcon("rocket", "Rocket", undefined);
export const ShieldX: SarchiLucideIcon = createSarchiIcon("shield-x", "ShieldX", undefined);
export const Trash: SarchiLucideIcon = createSarchiIcon("trash", "Trash", undefined);
export const ArrowDown: SarchiLucideIcon = createSarchiIcon("arrow-down", "ArrowDown", undefined);
export const ArrowUpCircle: SarchiLucideIcon = createSarchiIcon("arrow-up-circle", "ArrowUpCircle", undefined);
export const ArrowUpRight: SarchiLucideIcon = createSarchiIcon("arrow-up-right", "ArrowUpRight", undefined);
export const Boxes: SarchiLucideIcon = createSarchiIcon("boxes", "Boxes", undefined);
export const CalendarOff: SarchiLucideIcon = createSarchiIcon("calendar-off", "CalendarOff", undefined);
export const Camera: SarchiLucideIcon = createSarchiIcon("camera", "Camera", undefined);
export const Cloud: SarchiLucideIcon = createSarchiIcon("cloud", "Cloud", undefined);
export const Crosshair: SarchiLucideIcon = createSarchiIcon("crosshair", "Crosshair", undefined);
export const GripVertical: SarchiLucideIcon = createSarchiIcon("grip-vertical", "GripVertical", "outline");
export const HelpCircle: SarchiLucideIcon = createSarchiIcon("help-circle", "HelpCircle", undefined);
export const Link2: SarchiLucideIcon = createSarchiIcon("link-2", "Link2", undefined);
export const List: SarchiLucideIcon = createSarchiIcon("list", "List", undefined);
export const LocateFixed: SarchiLucideIcon = createSarchiIcon("locate-fixed", "LocateFixed", undefined);
export const MapPinned: SarchiLucideIcon = createSarchiIcon("map-pinned", "MapPinned", undefined);
export const Megaphone: SarchiLucideIcon = createSarchiIcon("megaphone", "Megaphone", undefined);
export const Menu: SarchiLucideIcon = createSarchiIcon("menu", "Menu", undefined);
export const Music: SarchiLucideIcon = createSarchiIcon("music", "Music", undefined);
export const PackageCheck: SarchiLucideIcon = createSarchiIcon("package-check", "PackageCheck", undefined);
export const RotateCw: SarchiLucideIcon = createSarchiIcon("rotate-cw", "RotateCw", undefined);
export const Shield: SarchiLucideIcon = createSarchiIcon("shield", "Shield", undefined);
export const Table2: SarchiLucideIcon = createSarchiIcon("table-2", "Table2", undefined);
export const Type: SarchiLucideIcon = createSarchiIcon("type", "Type", undefined);
export const Unlock: SarchiLucideIcon = createSarchiIcon("unlock", "Unlock", undefined);
export const UserCircle: SarchiLucideIcon = createSarchiIcon("user-circle", "UserCircle", undefined);
export const ArrowDownRight: SarchiLucideIcon = createSarchiIcon("arrow-down-right", "ArrowDownRight", undefined);
export const Blend: SarchiLucideIcon = createSarchiIcon("blend", "Blend", undefined);
export const Bold: SarchiLucideIcon = createSarchiIcon("bold", "Bold", undefined);
export const Building: SarchiLucideIcon = createSarchiIcon("building", "Building", undefined);
export const Building2: SarchiLucideIcon = createSarchiIcon("building-2", "Building2", undefined);
export const ChevronsUpDown: SarchiLucideIcon = createSarchiIcon("chevrons-up-down", "ChevronsUpDown", "outline");
export const Circle: SarchiLucideIcon = createSarchiIcon("circle", "Circle", undefined);
export const ClipboardCheck: SarchiLucideIcon = createSarchiIcon("clipboard-check", "ClipboardCheck", undefined);
export const CloudOff: SarchiLucideIcon = createSarchiIcon("cloud-off", "CloudOff", undefined);
export const Coffee: SarchiLucideIcon = createSarchiIcon("coffee", "Coffee", undefined);
export const Coins: SarchiLucideIcon = createSarchiIcon("coins", "Coins", undefined);
export const FileImage: SarchiLucideIcon = createSarchiIcon("file-image", "FileImage", undefined);
export const Gift: SarchiLucideIcon = createSarchiIcon("gift", "Gift", undefined);
export const Grid2X2: SarchiLucideIcon = createSarchiIcon("grid-2-x-2", "Grid2X2", undefined);
export const Hash: SarchiLucideIcon = createSarchiIcon("hash", "Hash", undefined);
export const Inbox: SarchiLucideIcon = createSarchiIcon("inbox", "Inbox", undefined);
export const LayoutDashboard: SarchiLucideIcon = createSarchiIcon("layout-dashboard", "LayoutDashboard", undefined);
export const Minimize2: SarchiLucideIcon = createSarchiIcon("minimize-2", "Minimize2", undefined);
export const MoreVertical: SarchiLucideIcon = createSarchiIcon("more-vertical", "MoreVertical", "outline");
export const MousePointerClick: SarchiLucideIcon = createSarchiIcon("mouse-pointer-click", "MousePointerClick", undefined);
export const NotebookText: SarchiLucideIcon = createSarchiIcon("notebook-text", "NotebookText", undefined);
export const OctagonX: SarchiLucideIcon = createSarchiIcon("octagon-x", "OctagonX", undefined);
export const OctagonXIcon: SarchiLucideIcon = createSarchiIcon("octagon-x", "OctagonXIcon", undefined);
export const PackageMinus: SarchiLucideIcon = createSarchiIcon("package-minus", "PackageMinus", undefined);
export const PackagePlus: SarchiLucideIcon = createSarchiIcon("package-plus", "PackagePlus", undefined);
export const Paintbrush: SarchiLucideIcon = createSarchiIcon("paintbrush", "Paintbrush", undefined);
export const PanelLeft: SarchiLucideIcon = createSarchiIcon("panel-left", "PanelLeft", undefined);
export const Percent: SarchiLucideIcon = createSarchiIcon("percent", "Percent", undefined);
export const PieChart: SarchiLucideIcon = createSarchiIcon("pie-chart", "PieChart", undefined);
export const Pin: SarchiLucideIcon = createSarchiIcon("pin", "Pin", undefined);
export const Plug: SarchiLucideIcon = createSarchiIcon("plug", "Plug", undefined);
export const PlusCircle: SarchiLucideIcon = createSarchiIcon("plus-circle", "PlusCircle", undefined);
export const Puzzle: SarchiLucideIcon = createSarchiIcon("puzzle", "Puzzle", undefined);
export const Radio: SarchiLucideIcon = createSarchiIcon("radio", "Radio", undefined);
export const Route: SarchiLucideIcon = createSarchiIcon("route", "Route", undefined);
export const Scale: SarchiLucideIcon = createSarchiIcon("scale", "Scale", undefined);
export const Share2: SarchiLucideIcon = createSarchiIcon("share-2", "Share2", undefined);
export const ShieldAlert: SarchiLucideIcon = createSarchiIcon("shield-alert", "ShieldAlert", undefined);
export const Shuffle: SarchiLucideIcon = createSarchiIcon("shuffle", "Shuffle", undefined);
export const Signal: SarchiLucideIcon = createSarchiIcon("signal", "Signal", undefined);
export const SignalZero: SarchiLucideIcon = createSarchiIcon("signal-zero", "SignalZero", undefined);
export const Space: SarchiLucideIcon = createSarchiIcon("space", "Space", undefined);
export const Sunset: SarchiLucideIcon = createSarchiIcon("sunset", "Sunset", undefined);
export const Target: SarchiLucideIcon = createSarchiIcon("target", "Target", undefined);
export const TestTube: SarchiLucideIcon = createSarchiIcon("test-tube", "TestTube", undefined);
export const ToggleLeft: SarchiLucideIcon = createSarchiIcon("toggle-left", "ToggleLeft", undefined);
export const ToggleRight: SarchiLucideIcon = createSarchiIcon("toggle-right", "ToggleRight", undefined);
export const Tv: SarchiLucideIcon = createSarchiIcon("tv", "Tv", undefined);
export const Unplug: SarchiLucideIcon = createSarchiIcon("unplug", "Unplug", undefined);
export const Usb: SarchiLucideIcon = createSarchiIcon("usb", "Usb", undefined);
export const UserX: SarchiLucideIcon = createSarchiIcon("user-x", "UserX", undefined);
export const Utensils: SarchiLucideIcon = createSarchiIcon("utensils", "Utensils", undefined);
export const ZoomIn: SarchiLucideIcon = createSarchiIcon("zoom-in", "ZoomIn", undefined);
export const CupSoda: SarchiLucideIcon = createSarchiIcon("cup-soda", "CupSoda", undefined);
export const Airplane: SarchiLucideIcon = createSarchiIcon("airplane", "Airplane", undefined);
export const Anchor: SarchiLucideIcon = createSarchiIcon("anchor", "Anchor", undefined);
export const Balloon: SarchiLucideIcon = createSarchiIcon("balloon", "Balloon", undefined);
export const Beach: SarchiLucideIcon = createSarchiIcon("beach", "Beach", undefined);
export const Bed: SarchiLucideIcon = createSarchiIcon("bed", "Bed", undefined);
export const Bell: SarchiLucideIcon = createSarchiIcon("bell", "Bell", undefined);
export const Bone: SarchiLucideIcon = createSarchiIcon("bone", "Bone", undefined);
export const Drumstick: SarchiLucideIcon = createSarchiIcon("bone", "Drumstick", undefined);
export const Book: SarchiLucideIcon = createSarchiIcon("book", "Book", undefined);
export const Bookmark: SarchiLucideIcon = createSarchiIcon("bookmark", "Bookmark", undefined);
export const Broom: SarchiLucideIcon = createSarchiIcon("broom", "Broom", undefined);
export const Campfire: SarchiLucideIcon = createSarchiIcon("campfire", "Campfire", undefined);
export const Confetti: SarchiLucideIcon = createSarchiIcon("confetti", "Confetti", undefined);
export const Cube: SarchiLucideIcon = createSarchiIcon("cube", "Cube", undefined);
export const Diamond: SarchiLucideIcon = createSarchiIcon("diamond", "Diamond", undefined);
export const Door: SarchiLucideIcon = createSarchiIcon("door", "Door", undefined);
export const Drop: SarchiLucideIcon = createSarchiIcon("drop", "Drop", undefined);
export const Dumbbell: SarchiLucideIcon = createSarchiIcon("dumbbell", "Dumbbell", undefined);
export const Earth: SarchiLucideIcon = createSarchiIcon("earth", "Earth", undefined);
export const Emoji: SarchiLucideIcon = createSarchiIcon("emoji", "Emoji", undefined);
export const EmojiLaugh: SarchiLucideIcon = createSarchiIcon("emoji-laugh", "EmojiLaugh", undefined);
export const Eraser: SarchiLucideIcon = createSarchiIcon("eraser", "Eraser", undefined);
export const Fan: SarchiLucideIcon = createSarchiIcon("fan", "Fan", undefined);
export const Feather: SarchiLucideIcon = createSarchiIcon("feather", "Feather", undefined);
export const Flashlight: SarchiLucideIcon = createSarchiIcon("flashlight", "Flashlight", undefined);
export const Gas: SarchiLucideIcon = createSarchiIcon("gas", "Gas", undefined);
export const Ghost: SarchiLucideIcon = createSarchiIcon("ghost", "Ghost", undefined);
export const Glasses: SarchiLucideIcon = createSarchiIcon("glasses", "Glasses", undefined);
export const Handshake: SarchiLucideIcon = createSarchiIcon("handshake", "Handshake", undefined);
export const Headphones: SarchiLucideIcon = createSarchiIcon("headphones", "Headphones", undefined);
export const Headset: SarchiLucideIcon = createSarchiIcon("headset", "Headset", undefined);
export const Heart: SarchiLucideIcon = createSarchiIcon("heart", "Heart", undefined);
export const IceCream: SarchiLucideIcon = createSarchiIcon("ice-cream", "IceCream", undefined);
export const Laptop: SarchiLucideIcon = createSarchiIcon("laptop", "Laptop", undefined);
export const Lasso: SarchiLucideIcon = createSarchiIcon("lasso", "Lasso", undefined);
export const Leaf: SarchiLucideIcon = createSarchiIcon("leaf", "Leaf", undefined);
export const Lightbulb: SarchiLucideIcon = createSarchiIcon("lightbulb", "Lightbulb", undefined);
export const Magnet: SarchiLucideIcon = createSarchiIcon("magnet", "Magnet", undefined);
export const Parachute: SarchiLucideIcon = createSarchiIcon("parachute", "Parachute", undefined);
export const Sailboat: SarchiLucideIcon = createSarchiIcon("sailboat", "Sailboat", undefined);
export const Saved: SarchiLucideIcon = createSarchiIcon("saved", "Saved", undefined);
export const Scooter: SarchiLucideIcon = createSarchiIcon("scooter", "Scooter", undefined);
export const Trophy: SarchiLucideIcon = createSarchiIcon("trophy", "Trophy", undefined);
export const Umbrella: SarchiLucideIcon = createSarchiIcon("umbrella", "Umbrella", undefined);
export const Windmill: SarchiLucideIcon = createSarchiIcon("windmill", "Windmill", undefined);
export const Cookie: SarchiLucideIcon = createSarchiIcon("cookie", "Cookie", undefined);
export const Beer: SarchiLucideIcon = createSarchiIcon("beer", "Beer", undefined);
export const Wine: SarchiLucideIcon = createSarchiIcon("wine", "Wine", undefined);
export const Soup: SarchiLucideIcon = createSarchiIcon("soup", "Soup", undefined);
export const Sandwich: SarchiLucideIcon = createSarchiIcon("sandwich", "Sandwich", undefined);
export const Cake: SarchiLucideIcon = createSarchiIcon("cake", "Cake", undefined);
export const Salad: SarchiLucideIcon = createSarchiIcon("salad", "Salad", undefined);
export const Fish: SarchiLucideIcon = createSarchiIcon("fish", "Fish", undefined);
export const Beef: SarchiLucideIcon = createSarchiIcon("beef", "Beef", undefined);
export const Milk: SarchiLucideIcon = createSarchiIcon("milk", "Milk", undefined);
export const Apple: SarchiLucideIcon = createSarchiIcon("apple", "Apple", undefined);
export const Cherry: SarchiLucideIcon = createSarchiIcon("cherry", "Cherry", undefined);
export const Citrus: SarchiLucideIcon = createSarchiIcon("citrus", "Citrus", undefined);
export const Grape: SarchiLucideIcon = createSarchiIcon("grape", "Grape", undefined);
export const Candy: SarchiLucideIcon = createSarchiIcon("candy", "Candy", undefined);
export const Croissant: SarchiLucideIcon = createSarchiIcon("croissant", "Croissant", undefined);
export const Popcorn: SarchiLucideIcon = createSarchiIcon("popcorn", "Popcorn", undefined);
