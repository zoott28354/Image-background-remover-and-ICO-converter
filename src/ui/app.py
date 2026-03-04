import os
import threading

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QCheckBox, QRadioButton, QButtonGroup,
    QSlider, QComboBox, QLineEdit, QTextEdit, QFrame, QFileDialog,
    QProgressBar, QScrollArea, QSizePolicy,
)
from PySide6.QtCore import Qt, Signal, QObject, QTimer, QThread
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QIcon

from utils.path_utils import resource_path as _resource_path

# ── i18n ──────────────────────────────────────────────────────────────────────
_lang = "en"

STRINGS = {
    "en": {
        "images_label":          "Images",
        "add_btn":               "+ Add",
        "clear_btn":             "Clear all",
        "add_tooltip":           "Select images to process\n(PNG, JPG, SVG)",
        "clear_tooltip":         "Remove all files from the list",
        "mode_label":            "Mode",
        "mode_format":           "Format Conversion",
        "mode_ico":              "Convert ICO",
        "mode_favicon":          "Favicon Generator",
        "mode_appstore":         "App Store Icons",
        "mode_format_tooltip":   "Batch convert between formats\n(PNG, JPG, WebP, GIF)",
        "mode_ico_tooltip":      "Multi-resolution Windows icons\nwith AI background removal",
        "mode_favicon_tooltip":  "Complete web favicon\n(ICO + PNG + manifest.json)",
        "mode_appstore_tooltip": "Icons for Google Play,\nApple Store, Microsoft Store",
        "format_label":          "Format:",
        "quality_label":         "Quality:",
        "quality_tooltip":       "1 = fast/large\n100 = slow/small",
        "format_tooltip":        "Output format for conversion",
        "store_label":           "Store:",
        "store_tooltip":         "Choose store for icon sizes",
        "ops_label":             "Operations",
        "remove_bg":             "1. Remove background",
        "remove_bg_tooltip":     "Use AI (rembg) to remove background",
        "model_label":           "Model:",
        "model_tooltip":         "Choose AI model for background removal",
        "crop_square":           "2. Crop to square",
        "crop_square_tooltip":   "Center image on transparent square background",
        "convert_ico":           "3. Convert to ICO  (otherwise save PNG)",
        "convert_ico_tooltip":   "Convert to multi-frame ICO\n(If no, save PNG only)",
        "output_dest_label":     "Output destination",
        "dest_same":             "Same folder as source file",
        "dest_custom":           "Custom folder:",
        "choose_btn":            "Choose...",
        "choose_tooltip":        "Select output folder",
        "process_btn":           "PROCESS",
        "process_tooltip":       "Start processing selected files",
        "log_label":             "Log",
        "preview_label":         "Preview",
        "preview_orig":          "Original",
        "preview_result":        "Result",
        "preview_select":        "← Select a file",
        "output_fixed_favicon":  "3.  Fixed output: ICO + PNG + manifest.json",
        "output_fixed_appstore": "3.  Fixed output: PNG at store dimensions",
        "transparency_yes":      "transparency ✓",
        "transparency_no":       "no transparency",
        "distorted_info":        "⚠ distorted → 512×512",
        "bg_removed_preview":    "— bg removal not in preview",
        "no_files_log":          "[!] No files in list.",
        "invalid_dir_log":       "[ERROR] Invalid output folder.",
        "done_log":              "─── Done ───",
        "open_images_title":     "Select images",
        "choose_dir_title":      "Choose output folder",
        "images_types_label":    "Images",
        # Model descriptions
        "desc_birefnet-general":      "Most precise, sharp edges — recommended",
        "desc_birefnet-general-lite": "Fast, slightly lower quality than general",
        "desc_isnet-general-use":     "Robust alternative for complex objects",
        "desc_u2net":                 "Fast, ideal for large non-critical batches",
        "desc_u2net_human_seg":       "Optimized for human subjects",
        "desc_isnet-anime":           "For illustrations, cartoons and anime",
    },
    "it": {
        "images_label":          "Immagini",
        "add_btn":               "+ Aggiungi",
        "clear_btn":             "Pulisci tutto",
        "add_tooltip":           "Seleziona immagini da elaborare\n(PNG, JPG, SVG)",
        "clear_tooltip":         "Rimuovi tutti i file dalla lista",
        "mode_label":            "Modalità",
        "mode_format":           "Format Conversion",
        "mode_ico":              "Converti ICO",
        "mode_favicon":          "Favicon Generator",
        "mode_appstore":         "App Store Icons",
        "mode_format_tooltip":   "Converte batch tra formati\n(PNG, JPG, WebP, GIF)",
        "mode_ico_tooltip":      "Icone Windows multi-risoluzione\ncon rimozione sfondo AI",
        "mode_favicon_tooltip":  "Favicon web complete\n(ICO + PNG + manifest.json)",
        "mode_appstore_tooltip": "Icone per Google Play,\nApple Store, Microsoft Store",
        "format_label":          "Formato:",
        "quality_label":         "Qualità:",
        "quality_tooltip":       "1 = veloce/pesante\n100 = lento/leggero",
        "format_tooltip":        "Formato di output per la conversione",
        "store_label":           "Store:",
        "store_tooltip":         "Scegli lo store per le dimensioni icone",
        "ops_label":             "Operazioni",
        "remove_bg":             "1. Rimuovi sfondo",
        "remove_bg_tooltip":     "Usa AI (rembg) per rimuovere lo sfondo",
        "model_label":           "Modello:",
        "model_tooltip":         "Scegli il modello AI per rimozione sfondo",
        "crop_square":           "2. Ritaglia a quadrato",
        "crop_square_tooltip":   "Centra l'immagine su sfondo trasparente quadrato",
        "convert_ico":           "3. Converti in ICO  (altrimenti salva PNG)",
        "convert_ico_tooltip":   "Converti in ICO multi-frame\n(Se no, salva solo PNG)",
        "output_dest_label":     "Destinazione output",
        "dest_same":             "Stessa cartella del file",
        "dest_custom":           "Cartella personalizzata:",
        "choose_btn":            "Scegli...",
        "choose_tooltip":        "Seleziona la cartella di output",
        "process_btn":           "PROCESSA",
        "process_tooltip":       "Avvia l'elaborazione dei file selezionati",
        "log_label":             "Log",
        "preview_label":         "Preview",
        "preview_orig":          "Originale",
        "preview_result":        "Risultato",
        "preview_select":        "← Seleziona un file",
        "output_fixed_favicon":  "3.  Output fisso: ICO + PNG + manifest.json",
        "output_fixed_appstore": "3.  Output fisso: PNG nelle dimensioni store",
        "transparency_yes":      "trasparenza ✓",
        "transparency_no":       "no trasparenza",
        "distorted_info":        "⚠ distorta → 512×512",
        "bg_removed_preview":    "— sfondo rimosso non in preview",
        "no_files_log":          "[!] Nessun file in lista.",
        "invalid_dir_log":       "[ERRORE] Cartella di output non valida.",
        "done_log":              "─── Completato ───",
        "open_images_title":     "Seleziona immagini",
        "choose_dir_title":      "Scegli cartella di output",
        "images_types_label":    "Immagini",
        # Descrizioni modelli
        "desc_birefnet-general":      "Più preciso, bordi netti — consigliato",
        "desc_birefnet-general-lite": "Veloce, qualità leggermente inferiore al generale",
        "desc_isnet-general-use":     "Alternativa robusta per oggetti complessi",
        "desc_u2net":                 "Veloce, ideale per batch grandi non critici",
        "desc_u2net_human_seg":       "Ottimizzato per soggetti umani",
        "desc_isnet-anime":           "Per illustrazioni, cartoon e anime",
    },
}


def _t(key: str) -> str:
    """Returns the translation for key in the current language."""
    return STRINGS.get(_lang, STRINGS["en"]).get(key, key)


# ── Dark theme stylesheet ──────────────────────────────────────────────────────
DARK_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: Arial;
    font-size: 13px;
}
QMainWindow {
    background-color: #1e1e1e;
}
QFrame#sidebar {
    background-color: transparent;
}
QFrame#panel {
    background-color: transparent;
}
QPushButton {
    background-color: #1f538d;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
}
QPushButton:hover {
    background-color: #2563a8;
}
QPushButton:disabled {
    background-color: #3a3a3a;
    color: #666666;
}
QPushButton#btn_secondary {
    background-color: #3a3a3a;
    color: #cccccc;
}
QPushButton#btn_secondary:hover {
    background-color: #484848;
}
QPushButton#btn_process {
    background-color: #1f538d;
    font-size: 15px;
    font-weight: bold;
    padding: 10px;
    border-radius: 8px;
}
QPushButton#btn_process:hover {
    background-color: #2563a8;
}
QPushButton#btn_process:disabled {
    background-color: #3a3a3a;
    color: #555555;
}
QPushButton#btn_lang {
    background-color: transparent;
    color: #888888;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    min-width: 28px;
    max-width: 28px;
    max-height: 22px;
}
QPushButton#btn_lang:hover {
    background-color: #444444;
}
QPushButton#btn_lang_active {
    background-color: #555555;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    min-width: 28px;
    max-width: 28px;
    max-height: 22px;
}
QPushButton#btn_remove_file {
    background-color: transparent;
    color: #888888;
    font-size: 11px;
    padding: 0px 4px;
    border-radius: 3px;
    max-width: 22px;
    max-height: 20px;
    min-width: 22px;
    min-height: 20px;
}
QPushButton#btn_remove_file:hover {
    background-color: #553333;
    color: #ff8888;
}
QRadioButton, QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #555555;
    background-color: #2a2a2a;
}
QCheckBox::indicator {
    border-radius: 4px;
}
QRadioButton::indicator:checked {
    background-color: #1f538d;
    border-color: #1f538d;
}
QCheckBox::indicator:checked {
    background-color: #1f538d;
    border-color: #1f538d;
    image: url(none);
}
QRadioButton:disabled, QCheckBox:disabled {
    color: #555555;
}
QComboBox {
    background-color: #333333;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e0e0e0;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #333333;
    border: 1px solid #555555;
    selection-background-color: #1f538d;
    color: #e0e0e0;
}
QLineEdit {
    background-color: #333333;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e0e0e0;
}
QLineEdit:disabled {
    background-color: #2a2a2a;
    color: #555555;
}
QSlider::groove:horizontal {
    height: 4px;
    background: #444444;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #1f538d;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::sub-page:horizontal {
    background: #1f538d;
    border-radius: 2px;
}
QTextEdit {
    background-color: #151515;
    border: 1px solid #333333;
    border-radius: 6px;
    font-family: Consolas;
    font-size: 10px;
    color: #cccccc;
}
QProgressBar {
    background-color: #333333;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #1f538d;
    border-radius: 4px;
}
QScrollBar:vertical {
    background: #2a2a2a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #555555;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollArea {
    border: none;
    background-color: #151515;
    border-radius: 6px;
}
QLabel#lbl_section {
    font-size: 13px;
    font-weight: bold;
    color: #e0e0e0;
}
QLabel#lbl_muted {
    font-size: 11px;
    color: #666666;
}
QLabel#lbl_desc {
    font-size: 11px;
    color: #666666;
}
QWidget#file_row_selected {
    background-color: #2c4a70;
    border-radius: 4px;
}
QWidget#file_row {
    background-color: transparent;
    border-radius: 4px;
}
QWidget#file_row:hover {
    background-color: #333333;
}
"""


# ── Worker thread ──────────────────────────────────────────────────────────────

class _WorkerSignals(QObject):
    log      = Signal(str)
    progress = Signal(float)
    done     = Signal()


class _Worker(QThread):
    """Background processing thread."""

    def __init__(self, files: list[str], modalita: str, output_dir,
                 formato: str = None, qualita: int = 85, store: str = None,
                 rimuovi_bg: bool = True, quadrato: bool = True,
                 ico: bool = True, modello: str = ""):
        super().__init__()
        self.files      = files
        self.modalita   = modalita
        self.output_dir = output_dir
        self.formato    = formato
        self.qualita    = qualita
        self.store      = store
        self.rimuovi_bg = rimuovi_bg
        self.quadrato   = quadrato
        self.ico        = ico
        self.modello    = modello
        self.signals    = _WorkerSignals()

    def run(self) -> None:
        from core.core import (
            elabora_file, converti_formato_batch,
            genera_favicon_batch, genera_app_store_icons_batch,
        )

        log_fn = self.signals.log.emit
        totale = len(self.files)

        if self.modalita == "ico":
            for i, path in enumerate(self.files, 1):
                elabora_file(
                    input_path=path,
                    output_dir=self.output_dir,
                    rimuovi_bg=self.rimuovi_bg,
                    quadrato=self.quadrato,
                    converti_ico=self.ico,
                    modello=self.modello,
                    log_fn=log_fn,
                )
                self.signals.progress.emit(i / totale)

        elif self.modalita == "format":
            converti_formato_batch(
                self.files, self.formato, self.qualita,
                self.output_dir, log_fn,
                rimuovi_bg=self.rimuovi_bg,
                modello=self.modello,
                quadrato=self.quadrato,
            )
            self.signals.progress.emit(1.0)

        elif self.modalita == "favicon":
            genera_favicon_batch(self.files, self.output_dir, log_fn)
            self.signals.progress.emit(1.0)

        elif self.modalita == "appstore":
            genera_app_store_icons_batch(self.files, self.store, self.output_dir, log_fn)
            self.signals.progress.emit(1.0)

        self.signals.done.emit()


# ── Preview canvas ─────────────────────────────────────────────────────────────

class PreviewCanvas(QLabel):
    """QLabel that renders a PIL RGBA image with checkerboard background, fitted to size."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pil_image = None
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #151515; border-radius: 6px;")

    def set_image(self, pil_image) -> None:
        self._pil_image = pil_image
        self._refresh()

    def clear_image(self) -> None:
        self._pil_image = None
        self.clear()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._refresh()

    def _refresh(self) -> None:
        if self._pil_image is None:
            return
        from PIL import Image
        cw = max(self.width() - 12, 1)
        ch = max(self.height() - 12, 1)
        thumb = self._pil_image.copy()
        thumb.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        tw, th = thumb.size
        bg = self._make_checkerboard((tw, th))
        if thumb.mode == 'RGBA':
            bg.paste(thumb, mask=thumb.split()[3])
        else:
            bg.paste(thumb)
        self.setPixmap(self._pil_to_pixmap(bg))

    @staticmethod
    def _make_checkerboard(size, tile: int = 8):
        from PIL import Image, ImageDraw
        w, h = size
        bg = Image.new('RGB', (w, h), (200, 200, 200))
        draw = ImageDraw.Draw(bg)
        for y in range(0, h, tile):
            for x in range(0, w, tile):
                if ((x // tile) + (y // tile)) % 2:
                    draw.rectangle([x, y, x + tile - 1, y + tile - 1], fill=(160, 160, 160))
        return bg

    @staticmethod
    def _pil_to_pixmap(pil_img) -> QPixmap:
        from PIL import Image
        from PIL.ImageQt import ImageQt
        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')
        qt_image = ImageQt(pil_img)
        return QPixmap.fromImage(qt_image)


# ── Main window ────────────────────────────────────────────────────────────────

from core.core import SUPPORTED_EXT, MODELLI_REMBG, MODELLO_DEFAULT


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RembgExporter")
        ico_path = _resource_path(os.path.join('assets', 'RembgExporter.ico'))
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        self.resize(1250, 700)
        self.setMinimumSize(1100, 650)

        self._file_list: list[str] = []
        self._selected_file: str | None = None
        self._img_orig_pil = None
        self._img_result_pil = None
        self._lang_btns: dict[str, QPushButton] = {}
        self._tooltips: list[tuple] = []   # (widget, key)
        self._worker_thread: _Worker | None = None

        self._build_ui()
        self._set_texts()
        self._on_modalita_change()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(12, 6, 12, 12)
        root.setSpacing(10)

        # ── left sidebar ───────────────────────────────────────────────────────
        left = self._make_panel()
        left.setFixedWidth(195)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(8, 10, 8, 10)
        left_layout.setSpacing(6)

        # Header: Images label + IT/EN buttons
        hdr = QHBoxLayout()
        self.lbl_images = QLabel()
        self.lbl_images.setObjectName("lbl_section")
        hdr.addWidget(self.lbl_images)
        hdr.addStretch()
        for lang in ["IT", "EN"]:
            btn = QPushButton(lang)
            btn.setObjectName("btn_lang")
            btn.clicked.connect(lambda checked=False, l=lang.lower(): self._switch_lang(l))
            hdr.addWidget(btn)
            self._lang_btns[lang.lower()] = btn
        left_layout.addLayout(hdr)

        # Add / Clear buttons
        btn_row = QHBoxLayout()
        self.btn_aggiungi = QPushButton()
        self._tt(self.btn_aggiungi, "add_tooltip")
        self.btn_aggiungi.clicked.connect(self._aggiungi)
        btn_row.addWidget(self.btn_aggiungi)

        self.btn_pulisci = QPushButton()
        self.btn_pulisci.setObjectName("btn_secondary")
        self._tt(self.btn_pulisci, "clear_tooltip")
        self.btn_pulisci.clicked.connect(self._pulisci)
        btn_row.addWidget(self.btn_pulisci)
        left_layout.addLayout(btn_row)

        # File list scroll area
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._files_container = QWidget()
        self._files_container.setStyleSheet("background-color: #151515;")
        self._files_layout = QVBoxLayout(self._files_container)
        self._files_layout.setContentsMargins(4, 4, 4, 4)
        self._files_layout.setSpacing(2)
        self._files_layout.addStretch()
        self._scroll_area.setWidget(self._files_container)
        left_layout.addWidget(self._scroll_area)

        root.addWidget(left)

        # ── center panel ───────────────────────────────────────────────────────
        center = QVBoxLayout()
        center.setSpacing(8)

        # Mode section
        frm_mode = self._make_panel()
        mode_layout = QVBoxLayout(frm_mode)
        mode_layout.setContentsMargins(12, 10, 12, 10)
        mode_layout.setSpacing(6)

        self.lbl_modalita = QLabel()
        self.lbl_modalita.setObjectName("lbl_section")
        mode_layout.addWidget(self.lbl_modalita)

        mode_row = QHBoxLayout()
        self._mode_group = QButtonGroup(self)
        self.rad_format  = QRadioButton()
        self.rad_ico     = QRadioButton()
        self.rad_favicon = QRadioButton()
        self.rad_appstore = QRadioButton()
        self.rad_format.setChecked(True)

        for i, (rad, key) in enumerate([
            (self.rad_format,   "mode_format_tooltip"),
            (self.rad_ico,      "mode_ico_tooltip"),
            (self.rad_favicon,  "mode_favicon_tooltip"),
            (self.rad_appstore, "mode_appstore_tooltip"),
        ]):
            self._mode_group.addButton(rad, i)
            self._tt(rad, key)
            mode_row.addWidget(rad)
        mode_row.addStretch()
        mode_layout.addLayout(mode_row)
        self._mode_group.idClicked.connect(lambda _: self._on_modalita_change())

        # Format options (shown only in Format mode)
        self.frm_format_opts = QWidget()
        fmt_row = QHBoxLayout(self.frm_format_opts)
        fmt_row.setContentsMargins(0, 0, 0, 0)
        fmt_row.setSpacing(6)

        self.lbl_formato_label = QLabel()
        fmt_row.addWidget(self.lbl_formato_label)

        self.om_formato = QComboBox()
        self.om_formato.addItems(["PNG", "JPG", "WebP", "GIF"])
        self.om_formato.setFixedWidth(100)
        self._tt(self.om_formato, "format_tooltip")
        self.om_formato.currentTextChanged.connect(
            lambda _: (self._aggiorna_lbl_output(), self._aggiorna_preview()))
        fmt_row.addWidget(self.om_formato)

        self.lbl_qualita_label = QLabel()
        fmt_row.addWidget(self.lbl_qualita_label)

        self.slider_qualita = QSlider(Qt.Orientation.Horizontal)
        self.slider_qualita.setRange(1, 100)
        self.slider_qualita.setValue(85)
        self.slider_qualita.setFixedWidth(150)
        self._tt(self.slider_qualita, "quality_tooltip")
        fmt_row.addWidget(self.slider_qualita)

        self.lbl_qualita = QLabel("85")
        self.lbl_qualita.setFixedWidth(30)
        self.slider_qualita.valueChanged.connect(
            lambda v: self.lbl_qualita.setText(str(v)))
        fmt_row.addWidget(self.lbl_qualita)
        fmt_row.addStretch()
        mode_layout.addWidget(self.frm_format_opts)

        # App store options (shown only in App Store mode)
        self.frm_appstore_opts = QWidget()
        store_row = QHBoxLayout(self.frm_appstore_opts)
        store_row.setContentsMargins(0, 0, 0, 0)
        store_row.setSpacing(6)

        self.lbl_store_label = QLabel()
        store_row.addWidget(self.lbl_store_label)

        self.om_store = QComboBox()
        self.om_store.addItems(["Google Play", "Apple App Store", "Microsoft Store"])
        self.om_store.setFixedWidth(180)
        self._tt(self.om_store, "store_tooltip")
        self.om_store.currentTextChanged.connect(lambda _: self._aggiorna_preview())
        store_row.addWidget(self.om_store)
        store_row.addStretch()
        mode_layout.addWidget(self.frm_appstore_opts)

        center.addWidget(frm_mode)

        # Operations section
        frm_op = self._make_panel()
        op_layout = QVBoxLayout(frm_op)
        op_layout.setContentsMargins(12, 10, 12, 10)
        op_layout.setSpacing(6)

        self.lbl_ops = QLabel()
        self.lbl_ops.setObjectName("lbl_section")
        op_layout.addWidget(self.lbl_ops)

        # Remove bg row
        bg_row = QHBoxLayout()
        self.chk_bg = QCheckBox()
        self.chk_bg.setChecked(True)
        self._tt(self.chk_bg, "remove_bg_tooltip")
        self.chk_bg.stateChanged.connect(
            lambda _: (self._toggle_modello(), self._aggiorna_preview()))
        bg_row.addWidget(self.chk_bg)

        self.lbl_modello_label = QLabel()
        bg_row.addWidget(self.lbl_modello_label)

        self.om_modello = QComboBox()
        self.om_modello.addItems(MODELLI_REMBG)
        self.om_modello.setCurrentText(MODELLO_DEFAULT)
        self.om_modello.setFixedWidth(220)
        self._tt(self.om_modello, "model_tooltip")
        self.om_modello.currentTextChanged.connect(self._aggiorna_desc_modello)
        bg_row.addWidget(self.om_modello)

        self.lbl_desc = QLabel()
        self.lbl_desc.setObjectName("lbl_desc")
        bg_row.addWidget(self.lbl_desc)
        bg_row.addStretch()
        op_layout.addLayout(bg_row)

        # Crop to square
        self.chk_sq = QCheckBox()
        self.chk_sq.setChecked(True)
        self._tt(self.chk_sq, "crop_square_tooltip")
        self.chk_sq.stateChanged.connect(lambda _: self._aggiorna_preview())
        op_layout.addWidget(self.chk_sq)

        # Convert ICO checkbox (ICO mode only)
        self.chk_ico = QCheckBox()
        self.chk_ico.setChecked(True)
        self._tt(self.chk_ico, "convert_ico_tooltip")
        op_layout.addWidget(self.chk_ico)

        # Output info label (non-ICO modes)
        self.lbl_output_info = QLabel()
        self.lbl_output_info.setObjectName("lbl_desc")
        op_layout.addWidget(self.lbl_output_info)

        center.addWidget(frm_op)

        # Output destination section
        frm_out = self._make_panel()
        out_layout = QVBoxLayout(frm_out)
        out_layout.setContentsMargins(12, 10, 12, 10)
        out_layout.setSpacing(6)

        self.lbl_output_dest = QLabel()
        self.lbl_output_dest.setObjectName("lbl_section")
        out_layout.addWidget(self.lbl_output_dest)

        self._dest_group = QButtonGroup(self)
        self.rad_dest_same = QRadioButton()
        self.rad_dest_same.setChecked(True)
        self._dest_group.addButton(self.rad_dest_same, 0)
        out_layout.addWidget(self.rad_dest_same)

        dest_row = QHBoxLayout()
        self.rad_dest_custom = QRadioButton()
        self._dest_group.addButton(self.rad_dest_custom, 1)
        dest_row.addWidget(self.rad_dest_custom)

        self.entry_dest = QLineEdit()
        self.entry_dest.setEnabled(False)
        dest_row.addWidget(self.entry_dest)

        self.btn_scegli = QPushButton()
        self.btn_scegli.setEnabled(False)
        self._tt(self.btn_scegli, "choose_tooltip")
        self.btn_scegli.clicked.connect(self._scegli_dest)
        dest_row.addWidget(self.btn_scegli)
        out_layout.addLayout(dest_row)
        self._dest_group.idClicked.connect(self._toggle_dest)

        center.addWidget(frm_out)

        # Process button + progress bar
        self.btn_processa = QPushButton()
        self.btn_processa.setObjectName("btn_process")
        self._tt(self.btn_processa, "process_tooltip")
        self.btn_processa.clicked.connect(self._processa)
        center.addWidget(self.btn_processa)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setValue(0)
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        center.addWidget(self.progress)

        # Log section
        frm_log = self._make_panel()
        log_layout = QVBoxLayout(frm_log)
        log_layout.setContentsMargins(12, 10, 12, 10)
        log_layout.setSpacing(4)

        self.lbl_log = QLabel()
        self.lbl_log.setObjectName("lbl_section")
        log_layout.addWidget(self.lbl_log)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(120)
        log_layout.addWidget(self.log_text)

        center.addWidget(frm_log, stretch=1)
        root.addLayout(center, stretch=1)

        # ── right preview sidebar ──────────────────────────────────────────────
        right = self._make_panel()
        right.setFixedWidth(235)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(8, 10, 8, 10)
        right_layout.setSpacing(4)

        self.lbl_preview_header = QLabel()
        self.lbl_preview_header.setObjectName("lbl_section")
        right_layout.addWidget(self.lbl_preview_header)

        self.lbl_preview_orig_label = QLabel()
        self.lbl_preview_orig_label.setObjectName("lbl_muted")
        right_layout.addWidget(self.lbl_preview_orig_label)

        self._canvas_orig = PreviewCanvas()
        right_layout.addWidget(self._canvas_orig, stretch=1)

        self.lbl_preview_result_label = QLabel()
        self.lbl_preview_result_label.setObjectName("lbl_muted")
        right_layout.addWidget(self.lbl_preview_result_label)

        self._canvas_result = PreviewCanvas()
        right_layout.addWidget(self._canvas_result, stretch=1)

        self.lbl_preview_info = QLabel()
        self.lbl_preview_info.setObjectName("lbl_muted")
        self.lbl_preview_info.setWordWrap(True)
        right_layout.addWidget(self.lbl_preview_info)

        root.addWidget(right)

    @staticmethod
    def _make_panel() -> QFrame:
        """Create a styled dark panel frame."""
        frame = QFrame()
        frame.setObjectName("panel")
        return frame

    # ── i18n ──────────────────────────────────────────────────────────────────

    def _tt(self, widget, key: str) -> None:
        """Set tooltip and register for language updates."""
        widget.setToolTip(_t(key))
        self._tooltips.append((widget, key))

    def _switch_lang(self, lang: str) -> None:
        global _lang
        _lang = lang
        self._set_texts()

    def _set_texts(self) -> None:
        """Update all UI widget text to the current language."""
        self.lbl_images.setText(_t("images_label"))
        self.btn_aggiungi.setText(_t("add_btn"))
        self.btn_pulisci.setText(_t("clear_btn"))
        self.lbl_modalita.setText(_t("mode_label"))
        self.rad_format.setText(_t("mode_format"))
        self.rad_ico.setText(_t("mode_ico"))
        self.rad_favicon.setText(_t("mode_favicon"))
        self.rad_appstore.setText(_t("mode_appstore"))
        self.lbl_formato_label.setText(_t("format_label"))
        self.lbl_qualita_label.setText(_t("quality_label"))
        self.lbl_store_label.setText(_t("store_label"))
        self.lbl_ops.setText(_t("ops_label"))
        self.chk_bg.setText(_t("remove_bg"))
        self.lbl_modello_label.setText(_t("model_label"))
        self.chk_sq.setText(_t("crop_square"))
        self.chk_ico.setText(_t("convert_ico"))
        self.lbl_output_dest.setText(_t("output_dest_label"))
        self.rad_dest_same.setText(_t("dest_same"))
        self.rad_dest_custom.setText(_t("dest_custom"))
        self.btn_scegli.setText(_t("choose_btn"))
        self.btn_processa.setText(_t("process_btn"))
        self.lbl_log.setText(_t("log_label"))
        self.lbl_preview_header.setText(_t("preview_label"))
        self.lbl_preview_orig_label.setText(_t("preview_orig"))
        self.lbl_preview_result_label.setText(_t("preview_result"))
        self.lbl_desc.setText(_t(f"desc_{self.om_modello.currentText()}"))
        # Tooltips
        for widget, key in self._tooltips:
            widget.setToolTip(_t(key))
        # Language button highlight
        for lang, btn in self._lang_btns.items():
            btn.setObjectName("btn_lang_active" if lang == _lang else "btn_lang")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        # Refresh dynamic labels
        self._aggiorna_lbl_output()
        self._aggiorna_preview()

    # ── file list management ───────────────────────────────────────────────────

    def _render_file_list(self) -> None:
        """Rebuild the file list widget."""
        # Clear existing items (keep the trailing stretch)
        while self._files_layout.count() > 1:
            item = self._files_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for path in self._file_list:
            is_sel = (path == self._selected_file)
            row = QWidget()
            row.setObjectName("file_row_selected" if is_sel else "file_row")
            row.setFixedHeight(28)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(6, 2, 4, 2)
            row_layout.setSpacing(4)

            lbl = QLabel(os.path.basename(path))
            lbl.setStyleSheet("background: transparent; font-size: 12px;")
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row_layout.addWidget(lbl)

            btn_rm = QPushButton("✕")
            btn_rm.setObjectName("btn_remove_file")
            btn_rm.clicked.connect(lambda checked=False, p=path: self._rimuovi_file(p))
            row_layout.addWidget(btn_rm)

            # Click on row/label to select
            row.mousePressEvent = lambda e, p=path: self._on_file_select(p)
            lbl.mousePressEvent = lambda e, p=path: self._on_file_select(p)

            self._files_layout.insertWidget(self._files_layout.count() - 1, row)

    def _aggiungi(self) -> None:
        exts = " ".join(f"*{e}" for e in SUPPORTED_EXT)
        files, _ = QFileDialog.getOpenFileNames(
            self, _t("open_images_title"), "",
            f"{_t('images_types_label')} ({exts});;All files (*.*)"
        )
        for f in files:
            if f not in self._file_list:
                self._file_list.append(f)
        if files and self._selected_file is None and self._file_list:
            self._selected_file = self._file_list[0]
            self._aggiorna_preview()
        self._render_file_list()

    def _rimuovi_file(self, path: str) -> None:
        self._file_list.remove(path)
        if self._selected_file == path:
            self._selected_file = self._file_list[0] if self._file_list else None
            self._aggiorna_preview()
        self._render_file_list()

    def _pulisci(self) -> None:
        self._file_list.clear()
        self._selected_file = None
        self._aggiorna_preview()
        self._render_file_list()

    def _on_file_select(self, path: str) -> None:
        self._selected_file = path
        self._render_file_list()
        self._aggiorna_preview()

    # ── preview ───────────────────────────────────────────────────────────────

    def _aggiorna_preview(self) -> None:
        """Update the preview for the selected file with current settings."""
        from PIL import Image, ImageDraw

        self._canvas_orig.clear_image()
        self._canvas_result.clear_image()
        self._img_orig_pil = None
        self._img_result_pil = None

        if not self._selected_file:
            self.lbl_preview_orig_label.setText(_t("preview_orig"))
            self.lbl_preview_info.setText(_t("preview_select"))
            return

        path = self._selected_file
        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == '.svg':
                sz = 200
                img_orig = Image.new('RGBA', (sz, sz), (70, 70, 70, 255))
                draw = ImageDraw.Draw(img_orig)
                draw.text((sz // 2 - 14, sz // 2 - 8), "SVG", fill=(180, 180, 180, 255))
                w_orig, h_orig = sz, sz
                self.lbl_preview_orig_label.setText(_t("preview_orig"))
            else:
                img_orig = Image.open(path).convert('RGBA')
                w_orig, h_orig = img_orig.size
                self.lbl_preview_orig_label.setText(
                    f'{_t("preview_orig")} ({w_orig}×{h_orig})')

            modalita = self._get_modalita()
            non_quadrata = (w_orig != h_orig)
            forza_quadrato = (modalita in ("ico", "favicon", "appstore"))
            ha_sq = (modalita != "format")

            if ha_sq and self.chk_sq.isChecked() and non_quadrata:
                size = max(w_orig, h_orig)
                img_result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                img_result.paste(img_orig, ((size - w_orig) // 2, (size - h_orig) // 2))
                risultato_tag = "padding"
            elif ha_sq and not self.chk_sq.isChecked() and non_quadrata and forza_quadrato:
                img_result = img_orig.resize((512, 512), Image.Resampling.LANCZOS)
                risultato_tag = "distorta"
            else:
                img_result = img_orig.copy()
                risultato_tag = "ok"

            self._img_orig_pil = img_orig
            self._img_result_pil = img_result
            self._canvas_orig.set_image(img_orig)
            self._canvas_result.set_image(img_result)

            if modalita == "ico":
                info = f"{w_orig}×{h_orig}\n→ ICO  16–256px"
            elif modalita == "favicon":
                info = f"{w_orig}×{h_orig}\n→ ICO + PNG\n   32 / 192 / 512px"
            elif modalita == "appstore":
                store = self.om_store.currentText().replace(" App Store", "").replace(" Store", "")
                info = f"{w_orig}×{h_orig}\n→ {store} icons"
            else:
                fmt = self.om_formato.currentText().upper()
                info = f"{w_orig}×{h_orig}\n→ {fmt}"

            if risultato_tag == "padding":
                sq = max(w_orig, h_orig)
                info += f"\npadding → {sq}×{sq}"
            elif risultato_tag == "distorta":
                info += "\n" + _t("distorted_info")

            if self.chk_bg.isChecked():
                info += "\n" + _t("bg_removed_preview")

            self.lbl_preview_info.setText(info)

        except Exception as e:
            self.lbl_preview_orig_label.setText(_t("preview_orig"))
            self.lbl_preview_info.setText(f"Preview N/A\n{str(e)[:35]}")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _get_modalita(self) -> str:
        """Return current mode key string."""
        idx = self._mode_group.checkedId()
        return ["format", "ico", "favicon", "appstore"][idx]

    def _toggle_modello(self) -> None:
        enabled = self.chk_bg.isChecked()
        self.om_modello.setEnabled(enabled)
        color = "#666666" if enabled else "#444444"
        self.lbl_desc.setStyleSheet(f"color: {color}; font-size: 11px;")

    def _aggiorna_desc_modello(self, modello: str) -> None:
        self.lbl_desc.setText(_t(f"desc_{modello}"))

    def _toggle_dest(self, btn_id: int) -> None:
        custom = (btn_id == 1)
        self.entry_dest.setEnabled(custom)
        self.btn_scegli.setEnabled(custom)

    def _scegli_dest(self) -> None:
        d = QFileDialog.getExistingDirectory(self, _t("choose_dir_title"))
        if d:
            self.entry_dest.setText(d)

    def _log(self, msg: str) -> None:
        self.log_text.append(msg)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum())

    def _aggiorna_lbl_output(self) -> None:
        """Update output info label text based on current mode."""
        modalita = self._get_modalita()
        if modalita == "favicon":
            testo = _t("output_fixed_favicon")
        elif modalita == "appstore":
            testo = _t("output_fixed_appstore")
        elif modalita == "format":
            fmt = self.om_formato.currentText().upper()
            trasparenza = fmt in ("PNG", "WEBP", "GIF")
            nota = _t("transparency_yes") if trasparenza else _t("transparency_no")
            testo = f"3.  Output: {fmt}  ({nota})"
        else:
            testo = ""
        self.lbl_output_info.setText(testo)

    def _on_modalita_change(self) -> None:
        """Show/hide options depending on the selected mode."""
        modalita = self._get_modalita()

        self.frm_format_opts.setVisible(modalita == "format")
        self.frm_appstore_opts.setVisible(modalita == "appstore")
        self.chk_sq.setVisible(modalita != "format")
        self.chk_ico.setVisible(modalita == "ico")
        self.lbl_output_info.setVisible(modalita != "ico")

        if modalita != "ico":
            self._aggiorna_lbl_output()

        self._aggiorna_preview()

    def _set_ui_busy(self, busy: bool) -> None:
        self.btn_processa.setEnabled(not busy)

    # ── processing ────────────────────────────────────────────────────────────

    def _processa(self) -> None:
        if not self._file_list:
            self._log(_t("no_files_log"))
            return

        output_dir = None
        if self.rad_dest_custom.isChecked():
            output_dir = self.entry_dest.text().strip() or None
            if not output_dir or not os.path.isdir(output_dir):
                self._log(_t("invalid_dir_log"))
                return

        modalita = self._get_modalita()
        store_map = {
            "Google Play": "google",
            "Apple App Store": "apple",
            "Microsoft Store": "microsoft",
        }

        self._set_ui_busy(True)
        self.progress.setValue(0)

        self._worker_thread = _Worker(
            files=list(self._file_list),
            modalita=modalita,
            output_dir=output_dir,
            formato=self.om_formato.currentText().lower(),
            qualita=self.slider_qualita.value(),
            store=store_map.get(self.om_store.currentText(), "google"),
            rimuovi_bg=self.chk_bg.isChecked(),
            quadrato=self.chk_sq.isChecked(),
            ico=self.chk_ico.isChecked(),
            modello=self.om_modello.currentText(),
        )
        self._worker_thread.signals.log.connect(self._log)
        self._worker_thread.signals.progress.connect(
            lambda v: self.progress.setValue(int(v * 1000)))
        self._worker_thread.signals.done.connect(self._done)
        self._worker_thread.start()

    def _done(self) -> None:
        self._log(_t("done_log"))
        self._set_ui_busy(False)


# ── Application entry point ────────────────────────────────────────────────────

def run() -> None:
    """Create QApplication and launch App (called from main.py)."""
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(DARK_STYLE)
    window = App()
    window.show()
    app.exec()
