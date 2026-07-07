import tkinter as tk
import subprocess
import math
import os
import sys
import json
import locale as _locale
import threading
import ctypes
import ctypes.wintypes as wintypes

# ── dependencias opcionales ──────────────────────────────────
try:
    import pystray
    from pystray import MenuItem as TrayItem
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

try:
    from win10toast import ToastNotifier
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

BG     = "#0d0d0f"
ACCENT = "#c084fc"
ACCENT2= "#818cf8"
RED    = "#f87171"
GREEN  = "#4ade80"
TEXT   = "#f1f5f9"
MUTED  = "#64748b"
CARD   = "#13131a"
BORDER = "#2a2a3e"
TROUGH = "#1e1e32"

TIMES_ES = [
    ("Ahora",     0),
    ("1 min",    60),
    ("5 min",   300),
    ("15 min",  900),
    ("30 min", 1800),
    ("1 hora", 3600),
]

TIMES_EN = [
    ("Now",       0),
    ("1 min",    60),
    ("5 min",   300),
    ("15 min",  900),
    ("30 min", 1800),
    ("1 hour", 3600),
]

APP_NAME    = "ElAlehYT-Apagado"
CONFIG_DIR  = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# ── umbrales del detector de descargas ───────────────────────
DL_ACTIVE_KBPS     = 300   # por encima de esto se considera "descargando"
DL_IDLE_KBPS       = 40    # por debajo de esto se considera "sin actividad"
DL_CONFIRM_SECONDS = 20    # segundos de inactividad seguidos para confirmar el final

# ── textos de la interfaz (ES / EN) ──────────────────────────
LANG = {
    "es": {
        "window_title":       "Apagado del Sistema",
        "app_title":          "Apagado del Sistema",
        "subtitle":           "Elige cuándo quieres apagar tu PC",
        "time_wait":          "TIEMPO DE ESPERA",
        "schedule_btn":       "  Programar apagado",
        "time_custom":        "TIEMPO PERSONALIZADO",
        "custom_desc":        "Escribe horas / minutos / segundos:",
        "hours":              "horas",
        "minutes":            "minutos",
        "seconds":            "segundos",
        "preview_zero":       "Ingresa un tiempo mayor a 0",
        "preview_prefix":     "⏱  Apagado en: ",
        "preview_invalid":    "Solo se permiten números",
        "use_custom_btn":     "  Usar tiempo personalizado y apagar",
        "err_invalid_time":   "⚠  Ingresa un tiempo válido (mayor a 0)",
        "cancel_hint":        "Pulsa el botón central, cancela abajo o pulsa Esc",
        "cancel_btn":         "✕   Cancelar apagado",
        "cancel_center":      "cancelar",
        "cancelled_msg":      "✓  Apagado cancelado",
        "notify_sched_title": "⏻ Apagado programado",
        "notify_sched_body":  "Tu PC se apagará en {t}.",
        "notify_immi_title":  "⏻ Apagado inminente",
        "notify_immi_body":   "Tu PC se apagará en 1 minuto.",
        "notify_canc_title":  "✓ Apagado cancelado",
        "notify_canc_body":   "Se canceló el apagado programado.",
        "notify_game_title":  "🎮 Juego detectado",
        "notify_game_body":   "Hay una app a pantalla completa. El apagado sigue en curso.",
        "game_warning":       "🎮  Se detectó un juego a pantalla completa",
        "postpone_btn":       "+  Posponer 10 minutos",
        "notify_post_title":  "⏻ Apagado pospuesto",
        "notify_post_body":   "Se añadieron {m} minutos.",
        "tray_show":          "Mostrar ventana",
        "tray_cancel":        "Cancelar apagado",
        "tray_exit":          "Salir",
        "tray_tooltip":       "Apagado del Sistema",
        "close_notify_title": "Apagado del Sistema",
        "close_notify_body":  "La app sigue activa en la bandeja del sistema.",
        "download_section":   "DESCARGAS",
        "download_btn":       "📥  Apagar cuando termine una descarga",
        "download_hint":      "Sirve para Steam, Epic Games, Battle.net y similares. Mide la\nvelocidad de red: cuando una descarga activa se detiene, se apaga el PC.",
        "download_no_psutil": "Necesita la librería 'psutil' instalada (pip install psutil)",
        "download_status_waiting": "Esperando que empiece una descarga…",
        "download_status_active":  "⬇  Descargando · {speed}",
        "download_status_confirm":"Sin actividad · confirmando en {s}s…",
        "download_cancel_btn":    "✕   Cancelar",
        "notify_dl_title":    "⏻ Descarga completada",
        "notify_dl_body":     "Se detectó que la descarga terminó. Apagando el PC…",
    },
    "en": {
        "window_title":       "System Shutdown",
        "app_title":          "System Shutdown",
        "subtitle":           "Choose when to shut down your PC",
        "time_wait":          "WAIT TIME",
        "schedule_btn":       "  Schedule shutdown",
        "time_custom":        "CUSTOM TIME",
        "custom_desc":        "Enter hours / minutes / seconds:",
        "hours":              "hours",
        "minutes":            "minutes",
        "seconds":            "seconds",
        "preview_zero":       "Enter a time greater than 0",
        "preview_prefix":     "⏱  Shutting down in: ",
        "preview_invalid":    "Only numbers are allowed",
        "use_custom_btn":     "  Use custom time and shut down",
        "err_invalid_time":   "⚠  Enter a valid time (greater than 0)",
        "cancel_hint":        "Click the center button, cancel below, or press Esc",
        "cancel_btn":         "✕   Cancel shutdown",
        "cancel_center":      "cancel",
        "cancelled_msg":      "✓  Shutdown cancelled",
        "notify_sched_title": "⏻ Shutdown scheduled",
        "notify_sched_body":  "Your PC will shut down in {t}.",
        "notify_immi_title":  "⏻ Shutdown imminent",
        "notify_immi_body":   "Your PC will shut down in 1 minute.",
        "notify_canc_title":  "✓ Shutdown cancelled",
        "notify_canc_body":   "The scheduled shutdown was cancelled.",
        "notify_game_title":  "🎮 Game detected",
        "notify_game_body":   "A fullscreen app is active. The shutdown is still running.",
        "game_warning":       "🎮  A fullscreen game was detected",
        "postpone_btn":       "+  Postpone 10 minutes",
        "notify_post_title":  "⏻ Shutdown postponed",
        "notify_post_body":   "{m} minutes were added.",
        "tray_show":          "Show window",
        "tray_cancel":        "Cancel shutdown",
        "tray_exit":          "Exit",
        "tray_tooltip":       "System Shutdown",
        "close_notify_title": "System Shutdown",
        "close_notify_body":  "The app is still running in the system tray.",
        "download_section":   "DOWNLOADS",
        "download_btn":       "📥  Shut down when a download finishes",
        "download_hint":      "Works with Steam, Epic Games, Battle.net and similar. It measures\nnetwork speed: once an active download stops, the PC shuts down.",
        "download_no_psutil": "Requires the 'psutil' library (pip install psutil)",
        "download_status_waiting": "Waiting for a download to start…",
        "download_status_active":  "⬇  Downloading · {speed}",
        "download_status_confirm":"No activity · confirming in {s}s…",
        "download_cancel_btn":    "✕   Cancel",
        "notify_dl_title":    "⏻ Download complete",
        "notify_dl_body":     "Detected that the download finished. Shutting down the PC…",
    },
}


def _detect_system_lang():
    """Detecta el idioma de Windows; si no puede, mira el locale del SO; si no, español."""
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        code = _locale.windows_locale.get(lang_id, "")
        if code.startswith("es"):
            return "es"
        if code:
            return "en"
    except Exception:
        pass
    try:
        code = _locale.getdefaultlocale()[0] or ""
        if code.startswith("es"):
            return "es"
        if code:
            return "en"
    except Exception:
        pass
    return "es"


def sep(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=12)


class App:
    def __init__(self, root):
        self.root = root

        # ── idioma: config guardada > idioma de Windows > es ──
        self.lang = self._initial_lang()

        root.title(self.L("window_title"))
        root.geometry("480x860")
        root.resizable(False, False)
        root.configure(bg=BG)

        self.selected  = tk.IntVar(value=300)
        self.remaining = 0
        self.total     = 0
        self.running   = False
        self._tick_id  = None
        self._ring_id  = None
        self._angle    = 0

        self.custom_h  = tk.StringVar(value="0")
        self.custom_m  = tk.StringVar(value="0")
        self.custom_s  = tk.StringVar(value="0")

        # ── estado de las nuevas features ────────────────────
        self.tray_icon       = None
        self._my_hwnd        = None
        self._game_warned    = False
        self._warn_frame     = None
        self._game_check_id  = None
        self.lbl_hint        = None
        self.cbtn            = None

        # ── estado del monitor de descargas ──────────────────
        self.dl_running    = False
        self._dl_check_id  = None
        self._dl_prev_bytes = None
        self._dl_state     = "waiting"   # waiting -> active -> confirming
        self._dl_confirm   = 0
        self.dl_status_lbl = None
        self.dl_speed_lbl  = None

        self._build()
        self._idle_spin()

        # cargar tiempo personalizado guardado
        self._load_config()

        # bandeja del sistema
        self._my_hwnd = self._get_hwnd()
        self._build_tray()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # atajo de teclado: Esc cancela el apagado o el monitor en curso
        self.root.bind("<Escape>", lambda e: self._cancel_any())

    # ── helpers de idioma ─────────────────────────────────────
    def L(self, key, **kwargs):
        text = LANG[self.lang].get(key, key)
        return text.format(**kwargs) if kwargs else text

    @property
    def TIMES(self):
        return TIMES_ES if self.lang == "es" else TIMES_EN

    def _initial_lang(self):
        data = self._read_config()
        saved = data.get("lang")
        if saved in ("es", "en"):
            return saved
        return _detect_system_lang()

    def _set_lang(self, lang):
        if lang == self.lang:
            return
        self.lang = lang
        data = self._read_config()
        data["lang"] = lang
        self._write_config(data)
        self._apply_lang()

    def _apply_lang(self):
        self.root.title(self.L("window_title"))
        self.lang_es_lbl.configure(fg=ACCENT if self.lang == "es" else MUTED)
        self.lang_en_lbl.configure(fg=ACCENT if self.lang == "en" else MUTED)
        self.title_lbl.configure(text=self.L("app_title"))
        self.subtitle_lbl.configure(text=self.L("subtitle"))
        self.section_time_lbl.configure(text=self.L("time_wait"))
        self.btn_preset.configure(text=self.L("schedule_btn"))
        self.section_custom_lbl.configure(text=self.L("time_custom"))
        self.custom_desc_lbl.configure(text=self.L("custom_desc"))
        for lbl_widget, key in zip(self.entry_labels, ("hours", "minutes", "seconds")):
            lbl_widget.configure(text=self.L(key))
        self.use_btn.configure(text=self.L("use_custom_btn"))
        self.section_dl_lbl.configure(text=self.L("download_section"))
        self.dl_btn.configure(text=self.L("download_btn") if PSUTIL_AVAILABLE
                               else self.L("download_no_psutil"))
        self.dl_hint_lbl.configure(text=self.L("download_hint"))
        self._build_grid()
        self._update_preview()
        if self.running:
            if self.lbl_hint is not None:
                self.lbl_hint.configure(text=self.L("cancel_hint"))
            if self.cbtn is not None:
                self.cbtn.configure(text=self.L("cancel_btn"))

    # ── construcción de la UI ─────────────────────────────────
    def _build(self):
        self.wrap = tk.Frame(self.root, bg=BG)
        self.wrap.pack(fill="both", expand=True, padx=28, pady=14)

        lang_row = tk.Frame(self.wrap, bg=BG)
        lang_row.pack(fill="x")
        self.lang_es_lbl = tk.Label(lang_row, text="ES", font=("Segoe UI", 9, "bold"),
                                     bg=BG, fg=ACCENT if self.lang == "es" else MUTED,
                                     cursor="hand2")
        self.lang_es_lbl.pack(side="right", padx=(6, 0))
        tk.Label(lang_row, text="|", font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(side="right")
        self.lang_en_lbl = tk.Label(lang_row, text="EN", font=("Segoe UI", 9, "bold"),
                                     bg=BG, fg=ACCENT if self.lang == "en" else MUTED,
                                     cursor="hand2")
        self.lang_en_lbl.pack(side="right")
        self.lang_es_lbl.bind("<Button-1>", lambda e: self._set_lang("es"))
        self.lang_en_lbl.bind("<Button-1>", lambda e: self._set_lang("en"))

        self.icon_cv = tk.Canvas(self.wrap, width=72, height=72,
                                  bg=BG, highlightthickness=0)
        self.icon_cv.pack()

        self.title_lbl = tk.Label(self.wrap, text=self.L("app_title"),
                                   font=("Segoe UI", 19, "bold"), bg=BG, fg=TEXT)
        self.title_lbl.pack(pady=(6, 2))
        self.subtitle_lbl = tk.Label(self.wrap, text=self.L("subtitle"),
                                      font=("Segoe UI", 10), bg=BG, fg=MUTED)
        self.subtitle_lbl.pack()

        sep(self.wrap)

        self.selectors = tk.Frame(self.wrap, bg=BG)
        self.selectors.pack(fill="x")

        self.section_time_lbl = tk.Label(self.selectors, text=self.L("time_wait"),
                                          font=("Segoe UI", 8, "bold"), bg=BG, fg=MUTED)
        self.section_time_lbl.pack(anchor="w")
        self.grid_f = tk.Frame(self.selectors, bg=BG)
        self.grid_f.pack(fill="x", pady=(8, 0))
        self._build_grid()

        self.btn_preset = tk.Button(
            self.selectors, text=self.L("schedule_btn"),
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT, fg="#0d0d0f", relief="flat", bd=0,
            activebackground=ACCENT2, activeforeground="#0d0d0f",
            cursor="hand2", pady=13,
            command=lambda: self._start(self.selected.get())
        )
        self.btn_preset.pack(fill="x", pady=(12, 0))
        self.btn_preset.bind("<Enter>", lambda e: self.btn_preset.configure(bg=ACCENT2))
        self.btn_preset.bind("<Leave>", lambda e: self.btn_preset.configure(bg=ACCENT))

        tk.Frame(self.selectors, bg=BORDER, height=1).pack(fill="x", pady=12)

        self.section_custom_lbl = tk.Label(self.selectors, text=self.L("time_custom"),
                                            font=("Segoe UI", 8, "bold"), bg=BG, fg=MUTED)
        self.section_custom_lbl.pack(anchor="w")

        self.custom_desc_lbl = tk.Label(self.selectors, text=self.L("custom_desc"),
                                         font=("Segoe UI", 9), bg=BG, fg=MUTED)
        self.custom_desc_lbl.pack(anchor="w", pady=(8, 4))

        fields_row = tk.Frame(self.selectors, bg=BG)
        fields_row.pack(fill="x", pady=(0, 4))

        self.entry_labels = []
        for var, key in [
            (self.custom_h, "hours"),
            (self.custom_m, "minutes"),
            (self.custom_s, "seconds"),
        ]:
            col = tk.Frame(fields_row, bg=BG)
            col.pack(side="left", expand=True, fill="x", padx=4)

            entry_frame = tk.Frame(col, bg=BORDER)
            entry_frame.pack(fill="x")
            inner = tk.Frame(entry_frame, bg=CARD)
            inner.pack(padx=1, pady=1)

            entry = tk.Entry(
                inner, textvariable=var,
                font=("Segoe UI", 22, "bold"),
                bg=CARD, fg=ACCENT,
                insertbackground=ACCENT,
                relief="flat", bd=0,
                justify="center", width=4
            )
            entry.pack(fill="x", ipady=10)

            entry.bind("<FocusIn>", lambda e, w=entry: w.after(0, w.select_range, 0, "end"))

            lbl = tk.Label(col, text=self.L(key),
                           font=("Segoe UI", 9), bg=BG, fg=MUTED)
            lbl.pack(pady=(3, 0))
            self.entry_labels.append(lbl)

        self.preview_lbl = tk.Label(
            self.selectors, text="",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        )
        self.preview_lbl.pack(pady=(6, 0))

        for var in (self.custom_h, self.custom_m, self.custom_s):
            var.trace_add("write", self._update_preview)
        self._update_preview()

        self.use_btn = tk.Button(
            self.selectors,
            text=self.L("use_custom_btn"),
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg="#0d0d0f", relief="flat", bd=0,
            activebackground=ACCENT2, activeforeground="#0d0d0f",
            cursor="hand2", pady=11,
            command=self._use_custom
        )
        self.use_btn.pack(fill="x", pady=(10, 0))
        self.use_btn.bind("<Enter>", lambda e: self.use_btn.configure(bg=ACCENT2))
        self.use_btn.bind("<Leave>", lambda e: self.use_btn.configure(bg=ACCENT))

        tk.Frame(self.selectors, bg=BORDER, height=1).pack(fill="x", pady=12)

        # ── sección: apagar cuando termine una descarga ──────
        self.section_dl_lbl = tk.Label(self.selectors, text=self.L("download_section"),
                                        font=("Segoe UI", 8, "bold"), bg=BG, fg=MUTED)
        self.section_dl_lbl.pack(anchor="w")

        dl_btn_text = self.L("download_btn") if PSUTIL_AVAILABLE else self.L("download_no_psutil")
        self.dl_btn = tk.Button(
            self.selectors, text=dl_btn_text,
            font=("Segoe UI", 11, "bold"),
            bg=CARD if PSUTIL_AVAILABLE else BORDER,
            fg=ACCENT2 if PSUTIL_AVAILABLE else MUTED,
            relief="flat", bd=0,
            activebackground=BORDER, activeforeground=ACCENT2,
            cursor="hand2" if PSUTIL_AVAILABLE else "arrow",
            pady=11,
            state="normal" if PSUTIL_AVAILABLE else "disabled",
            command=self._start_download_monitor
        )
        self.dl_btn.pack(fill="x", pady=(8, 0))
        if PSUTIL_AVAILABLE:
            self.dl_btn.bind("<Enter>", lambda e: self.dl_btn.configure(bg=BORDER))
            self.dl_btn.bind("<Leave>", lambda e: self.dl_btn.configure(bg=CARD))

        self.dl_hint_lbl = tk.Label(self.selectors, text=self.L("download_hint"),
                                     font=("Segoe UI", 8), bg=BG, fg=MUTED,
                                     justify="left")
        self.dl_hint_lbl.pack(anchor="w", pady=(6, 0))

        tk.Frame(self.selectors, bg=BORDER, height=1).pack(fill="x", pady=12)

        self.zone = tk.Frame(self.wrap, bg=BG)
        self.zone.pack(fill="x")

    # ── preview ────────────────────────────────────────────────
    def _update_preview(self, *_):
        try:
            h = int(self.custom_h.get() or 0)
            m = int(self.custom_m.get() or 0)
            s = int(self.custom_s.get() or 0)
            total = h * 3600 + m * 60 + s
            if total <= 0:
                self.preview_lbl.configure(text=self.L("preview_zero"), fg=MUTED)
            else:
                parts = []
                if h: parts.append(f"{h}h")
                if m: parts.append(f"{m}min")
                if s: parts.append(f"{s}seg" if self.lang == "es" else f"{s}s")
                self.preview_lbl.configure(
                    text=f"{self.L('preview_prefix')}{' '.join(parts)}",
                    fg=ACCENT
                )
        except ValueError:
            self.preview_lbl.configure(text=self.L("preview_invalid"), fg=RED)

    # ── grid ──────────────────────────────────────────────────
    def _build_grid(self):
        for w in self.grid_f.winfo_children():
            w.destroy()
        sel = self.selected.get()
        for i, (lbl, secs) in enumerate(self.TIMES):
            r, c = divmod(i, 3)
            is_sel = secs == sel
            bg_c = ACCENT if is_sel else CARD
            fg_c = "#0d0d0f" if is_sel else TEXT
            outer = tk.Frame(self.grid_f, bg=ACCENT if is_sel else BORDER)
            inner = tk.Frame(outer, bg=bg_c)
            inner.pack(padx=1, pady=1)
            lw = tk.Label(inner, text=lbl, font=("Segoe UI", 11, "bold"),
                          bg=bg_c, fg=fg_c, pady=13, padx=10)
            lw.pack()
            for w2 in (outer, inner, lw):
                w2.bind("<Button-1>", lambda e, s=secs: self._pick(s))
                w2.configure(cursor="hand2")
            outer.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            self.grid_f.columnconfigure(c, weight=1)

    def _pick(self, secs):
        self.selected.set(secs)
        self._build_grid()

    # ── tiempo personalizado ──────────────────────────────────
    def _use_custom(self):
        try:
            h = int(self.custom_h.get() or 0)
            m = int(self.custom_m.get() or 0)
            s = int(self.custom_s.get() or 0)
            secs = h * 3600 + m * 60 + s
            if secs <= 0:
                raise ValueError
            self._save_config(h, m, s)
            self._start(secs)
        except ValueError:
            err = tk.Label(self.selectors,
                           text=self.L("err_invalid_time"),
                           font=("Segoe UI", 9), bg=BG, fg=RED)
            err.pack()
            self.root.after(2500,
                            lambda: err.destroy() if err.winfo_exists() else None)

    # ── config persistente (último tiempo personalizado + idioma) ─
    def _read_config(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_config(self, data):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def _load_config(self):
        data = self._read_config()
        self.custom_h.set(str(data.get("h", 0)))
        self.custom_m.set(str(data.get("m", 0)))
        self.custom_s.set(str(data.get("s", 0)))

    def _save_config(self, h, m, s):
        data = self._read_config()
        data.update({"h": h, "m": m, "s": s})
        self._write_config(data)

    # ── mostrar/ocultar selectores ────────────────────────────
    def _hide_selectors(self):
        self.selectors.pack_forget()

    def _show_selectors(self):
        self.selectors.pack(fill="x", before=self.zone)

    # ── zona countdown ─────────────────────────────────────────
    def _clear_zone(self):
        self.running = False
        if self._tick_id:
            self.root.after_cancel(self._tick_id)
            self._tick_id = None
        if self._ring_id:
            self.root.after_cancel(self._ring_id)
            self._ring_id = None
        if self._game_check_id:
            self.root.after_cancel(self._game_check_id)
            self._game_check_id = None
        self._warn_frame = None
        self.lbl_hint = None
        self.cbtn = None
        for w in self.zone.winfo_children():
            w.destroy()

    def _show_countdown(self):
        self._clear_zone()
        self._hide_selectors()
        self.running = True
        self._game_warned = False

        self.ring_cv = tk.Canvas(self.zone, width=200, height=200,
                                  bg=BG, highlightthickness=0)
        self.ring_cv.pack()
        self.ring_cv.bind(
            "<Button-1>",
            lambda e: self._cancel() if self._click_on_center(e.x, e.y) else None
        )

        self.lbl_time = tk.Label(self.zone, text="00:00:00",
                                  font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT)
        self.lbl_time.pack(pady=(4, 2))

        self.lbl_hint = tk.Label(self.zone, text=self.L("cancel_hint"),
                                  font=("Segoe UI", 9), bg=BG, fg=MUTED)
        self.lbl_hint.pack()

        self.cbtn = tk.Button(
            self.zone, text=self.L("cancel_btn"),
            font=("Segoe UI", 12, "bold"),
            bg=RED, fg="#0d0d0f", relief="flat", bd=0,
            activebackground="#ef4444", activeforeground="#0d0d0f",
            cursor="hand2", pady=13,
            command=self._cancel
        )
        self.cbtn.pack(fill="x", pady=(12, 0))
        self.cbtn.bind("<Enter>", lambda e: self.cbtn.configure(bg="#ef4444"))
        self.cbtn.bind("<Leave>", lambda e: self.cbtn.configure(bg=RED))

        self._animate_ring()
        self._tick()
        self._game_check_loop()

    def _click_on_center(self, x, y):
        return math.hypot(x - 100, y - 100) < 30

    # ── lógica de apagado ─────────────────────────────────────
    def _fmt(self, secs):
        h, rem = divmod(secs, 3600)
        m, s = divmod(rem, 60)
        parts = []
        if h: parts.append(f"{h}h")
        if m: parts.append(f"{m}min")
        if s and not h: parts.append(f"{s}s")
        return " ".join(parts) if parts else "0s"

    def _start(self, secs):
        if secs == 0:
            subprocess.run("shutdown /s /t 0", shell=True)
            return
        self.remaining = secs
        self.total     = secs
        subprocess.run(
            f'shutdown /s /t {secs} /c "Apagado programado"',
            shell=True, capture_output=True
        )
        self._notify(self.L("notify_sched_title"), self.L("notify_sched_body", t=self._fmt(secs)))
        self._show_countdown()

    def _tick(self):
        if not self.running:
            return
        h, rem = divmod(self.remaining, 3600)
        m, s   = divmod(rem, 60)
        self.lbl_time.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
        if self.remaining == 60:
            self._notify(self.L("notify_immi_title"), self.L("notify_immi_body"))
        if self.remaining <= 0:
            return
        self.remaining -= 1
        self._tick_id = self.root.after(1000, self._tick)

    def _cancel_any(self):
        if self.running:
            self._cancel()
        elif self.dl_running:
            self._cancel_download()

    def _cancel(self):
        subprocess.run("shutdown /a", shell=True, capture_output=True)
        self._clear_zone()
        self._show_selectors()
        self._notify(self.L("notify_canc_title"), self.L("notify_canc_body"))
        msg = tk.Label(self.zone, text=self.L("cancelled_msg"),
                       font=("Segoe UI", 10), bg=BG, fg=GREEN)
        msg.pack(pady=8)
        self.root.after(
            3000,
            lambda: msg.destroy() if msg.winfo_exists() else None
        )

    # ── detección de juego/app en pantalla completa ───────────
    def _get_hwnd(self):
        try:
            return self.root.winfo_id()
        except Exception:
            return None

    def _is_fullscreen_app(self):
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if not hwnd or hwnd == self._my_hwnd:
                return False
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            screen_w = user32.GetSystemMetrics(0)
            screen_h = user32.GetSystemMetrics(1)
            return w >= screen_w and h >= screen_h
        except Exception:
            return False

    def _game_check_loop(self):
        if not self.running:
            return
        if self._is_fullscreen_app() and not self._game_warned:
            self._game_warned = True
            self._notify(self.L("notify_game_title"), self.L("notify_game_body"))
            self._show_game_warning()
        self._game_check_id = self.root.after(5000, self._game_check_loop)

    def _show_game_warning(self):
        if self._warn_frame is not None:
            return
        self._warn_frame = tk.Frame(self.zone, bg=BG)
        self._warn_frame.pack(fill="x", pady=(10, 0))
        tk.Label(self._warn_frame, text=self.L("game_warning"),
                 font=("Segoe UI", 9, "bold"), bg=BG, fg=ACCENT2).pack()
        pbtn = tk.Button(
            self._warn_frame, text=self.L("postpone_btn"),
            font=("Segoe UI", 10, "bold"),
            bg=CARD, fg=ACCENT2, relief="flat", bd=0,
            activebackground=BORDER, activeforeground=ACCENT2,
            cursor="hand2", pady=9,
            command=self._postpone
        )
        pbtn.pack(fill="x", pady=(6, 0))
        pbtn.bind("<Enter>", lambda e: pbtn.configure(bg=BORDER))
        pbtn.bind("<Leave>", lambda e: pbtn.configure(bg=CARD))

    def _postpone(self, extra=600):
        subprocess.run("shutdown /a", shell=True, capture_output=True)
        self.remaining += extra
        self.total += extra
        subprocess.run(
            f'shutdown /s /t {self.remaining} /c "Apagado programado"',
            shell=True, capture_output=True
        )
        self._notify(self.L("notify_post_title"), self.L("notify_post_body", m=extra // 60))
        if self._warn_frame:
            self._warn_frame.destroy()
            self._warn_frame = None
        self._game_warned = False

    # ── monitor de descargas (Steam / Epic / Battle.net / etc.) ──
    def _start_download_monitor(self):
        if not PSUTIL_AVAILABLE or self.dl_running or self.running:
            return
        self._clear_zone()
        self._hide_selectors()
        self.dl_running = True
        self._dl_state = "waiting"
        self._dl_confirm = 0
        self._dl_prev_bytes = psutil.net_io_counters().bytes_recv

        tk.Label(self.zone, text="📥", font=("Segoe UI", 40), bg=BG, fg=ACCENT).pack(pady=(4, 6))

        self.dl_status_lbl = tk.Label(self.zone, text=self.L("download_status_waiting"),
                                       font=("Segoe UI", 12, "bold"), bg=BG, fg=TEXT,
                                       wraplength=380, justify="center")
        self.dl_status_lbl.pack(pady=(0, 4))

        self.dl_speed_lbl = tk.Label(self.zone, text="0.0 KB/s",
                                      font=("Segoe UI", 22, "bold"), bg=BG, fg=ACCENT)
        self.dl_speed_lbl.pack(pady=(0, 10))

        dcbtn = tk.Button(
            self.zone, text=self.L("download_cancel_btn"),
            font=("Segoe UI", 12, "bold"),
            bg=RED, fg="#0d0d0f", relief="flat", bd=0,
            activebackground="#ef4444", activeforeground="#0d0d0f",
            cursor="hand2", pady=13,
            command=self._cancel_download
        )
        dcbtn.pack(fill="x", pady=(4, 0))
        dcbtn.bind("<Enter>", lambda e: dcbtn.configure(bg="#ef4444"))
        dcbtn.bind("<Leave>", lambda e: dcbtn.configure(bg=RED))

        self._download_tick()

    def _download_tick(self):
        if not self.dl_running:
            return
        try:
            now_bytes = psutil.net_io_counters().bytes_recv
        except Exception:
            now_bytes = self._dl_prev_bytes

        kbps = max(0.0, (now_bytes - self._dl_prev_bytes) / 1024.0)
        self._dl_prev_bytes = now_bytes

        speed_txt = f"{kbps:,.1f} KB/s" if kbps < 1024 else f"{kbps/1024:,.2f} MB/s"
        self.dl_speed_lbl.configure(text=speed_txt)

        if self._dl_state == "waiting":
            self.dl_status_lbl.configure(text=self.L("download_status_waiting"), fg=TEXT)
            if kbps > DL_ACTIVE_KBPS:
                self._dl_state = "active"

        elif self._dl_state == "active":
            self.dl_status_lbl.configure(
                text=self.L("download_status_active", speed=speed_txt), fg=ACCENT
            )
            if kbps < DL_IDLE_KBPS:
                self._dl_state = "confirming"
                self._dl_confirm = 0

        elif self._dl_state == "confirming":
            if kbps > DL_ACTIVE_KBPS:
                self._dl_state = "active"
                self._dl_confirm = 0
            else:
                self._dl_confirm += 1
                remaining_s = max(0, DL_CONFIRM_SECONDS - self._dl_confirm)
                self.dl_status_lbl.configure(
                    text=self.L("download_status_confirm", s=remaining_s), fg=GREEN
                )
                if self._dl_confirm >= DL_CONFIRM_SECONDS:
                    self._finish_download_monitor()
                    return

        self._dl_check_id = self.root.after(1000, self._download_tick)

    def _finish_download_monitor(self):
        self.dl_running = False
        if self._dl_check_id:
            self.root.after_cancel(self._dl_check_id)
            self._dl_check_id = None
        self._notify(self.L("notify_dl_title"), self.L("notify_dl_body"))
        subprocess.run("shutdown /s /t 10", shell=True, capture_output=True)
        self._start(10)

    def _cancel_download(self):
        self.dl_running = False
        if self._dl_check_id:
            self.root.after_cancel(self._dl_check_id)
            self._dl_check_id = None
        for w in self.zone.winfo_children():
            w.destroy()
        self._show_selectors()

    # ── notificaciones toast de Windows ───────────────────────
    def _notify(self, title, msg, duration=5):
        if not TOAST_AVAILABLE:
            return
        def _run():
            try:
                ToastNotifier().show_toast(title, msg, duration=duration, threaded=True)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    # ── bandeja del sistema ────────────────────────────────────
    def _tray_image(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse((6, 6, 58, 58), outline=ACCENT, width=5)
        d.line((32, 12, 32, 30), fill=ACCENT, width=5)
        return img

    def _build_tray(self):
        if not TRAY_AVAILABLE:
            return
        menu = pystray.Menu(
            TrayItem(lambda i: self.L("tray_show"), self._restore_from_tray, default=True),
            TrayItem(lambda i: self.L("tray_cancel"), self._tray_cancel,
                     enabled=lambda i: self.running or self.dl_running),
            TrayItem(lambda i: self.L("tray_exit"), self._quit_app)
        )
        self.tray_icon = pystray.Icon("apagado", self._tray_image(),
                                       self.L("tray_tooltip"), menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _restore_from_tray(self, icon=None, tray_item=None):
        self.root.after(0, self.root.deiconify)

    def _tray_cancel(self, icon=None, tray_item=None):
        self.root.after(0, self._cancel_any)

    def _quit_app(self, icon=None, tray_item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def _on_close(self):
        if TRAY_AVAILABLE:
            self.root.withdraw()
            self._notify(self.L("close_notify_title"), self.L("close_notify_body"))
        else:
            if self.tray_icon:
                self.tray_icon.stop()
            self.root.destroy()

    # ── animaciones ───────────────────────────────────────────
    def _animate_ring(self):
        if not self.running:
            return
        c = self.ring_cv
        cx, cy, r = 100, 100, 72
        prog = 1 - (self.remaining / self.total) if self.total else 0
        c.delete("all")

        c.create_arc(cx-r, cy-r, cx+r, cy+r,
                     start=0, extent=359.9,
                     outline=TROUGH, width=12, style="arc")

        if prog > 0:
            ext = -359.9 * prog
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=90, extent=ext,
                         outline=ACCENT, width=12, style="arc")
            ang = math.radians(90 + ext)
            dx  = cx + r * math.cos(ang)
            dy  = cy - r * math.sin(ang)
            c.create_oval(dx-8, dy-8, dx+8, dy+8, fill=ACCENT, outline="")

        c.create_oval(cx-26, cy-26, cx+26, cy+26,
                      fill="#1e1e2e", outline=ACCENT, width=2)
        c.create_text(cx, cy, text="⏻", font=("Segoe UI", 22), fill=ACCENT)
        c.create_text(cx, cy+48, text=self.L("cancel_center"), font=("Segoe UI", 8), fill=MUTED)

        self._ring_id = self.root.after(120, self._animate_ring)

    def _idle_spin(self):
        c = self.icon_cv
        cx, cy, r = 36, 36, 26
        a = self._angle
        c.delete("all")
        for i, col in enumerate(["#2a1040", "#5a2080", "#c084fc"]):
            off = i * 2
            c.create_arc(cx-r+off, cy-r+off, cx+r-off, cy+r-off,
                         start=a % 360, extent=260,
                         outline=col, width=2, style="arc")
        c.create_arc(cx-r, cy-r, cx+r, cy+r,
                     start=50, extent=260,
                     outline=ACCENT, width=3, style="arc")
        c.create_line(cx, cy-r+5, cx, cy-8,
                      fill=ACCENT, width=3, capstyle="round")
        self._angle = (a + 2) % 360
        self.root.after(30, self._idle_spin)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
