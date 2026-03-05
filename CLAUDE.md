# Instructions for Claude — RembgExporter

This file contains instructions to follow every time you work on this project.

## Stack and Environment
- **Python 3.11+** + **PySide6** (dark QSS theme, 3-column layout, LGPL)
- **rembg** for AI background removal, **ImageMagick** for ICO generation
  - Windows: portable bundle in `src/third-party/imagemagick/magick.exe`
  - Linux: `sudo apt install imagemagick` | macOS: `brew install imagemagick`
- **Windows** distribution via PyInstaller; **Linux/macOS** run from source
- Virtual environment in `/venv` (created by `scripts/setup.bat`)

## Project Structure
```
scripts/              # Developer toolchain (setup, build)
  setup.bat           # Creates venv, installs deps, generates start.bat in root
  build.bat           # PyInstaller build — always cd to root automatically
  version_info.txt    # Windows exe metadata
src/
  main.py             # Entry point — adds src/ to sys.path, launches App
  ui/
    app.py            # GUI — PySide6, 3-column layout
  core/
    core.py           # Processing pipeline — ImageMagick, rembg, PIL
  utils/
    path_utils.py     # resource_path() — resolves assets in dev and PyInstaller
  assets/
    RembgExporter.ico
  third-party/        # Portable executables bundled with the project
    imagemagick/
requirements.txt
tests/
```

## Code Rules
- **Type hints** on all public functions
- `snake_case` for variables/functions, `PascalCase` for classes
- No `print()` in production — use `log_fn` callback for user-visible messages
- All code, comments and UI default in **English**; Italian available via IT/EN switcher

## Key Patterns (do NOT change without asking)
- `resource_path(name)` in `src/utils/path_utils.py` — resolves paths relative to `src/` in dev, `_MEIPASS` in exe
- `_get_imagemagick_path()` in `src/core/core.py` — finds magick.exe in src/third-party or system PATH
- `_t(key)` + `STRINGS` dict — i18n system, always add both EN and IT keys together
- `_tt(widget, key)` — registers tooltips for automatic language updates
- `log_fn` callback pattern — never use print() inside core.py functions

## About Button Pattern (reusable for future apps)

A small circular `?` button placed inline with a section header opens an About dialog with app info and a clickable GitHub link.

### 1. Top-level constants in `app.py`
```python
_GITHUB_URL  = "https://github.com/<user>/<repo>"
_APP_AUTHOR  = "<username>"
_APP_LICENSE = "MIT"
_APP_VERSION = _read_version()
```

### 2. `_read_version()` — reads version from `scripts/version_info.txt`
```python
def _read_version() -> str:
    import re
    try:
        vf = _resource_path('..', 'scripts', 'version_info.txt')
        with open(vf, encoding='utf-8') as f:
            m = re.search(r"ProductVersion.*?'([0-9]+\.[0-9]+\.[0-9]+)'", f.read())
            if m:
                return m.group(1)
    except Exception:
        pass
    return "1.0.0"  # fallback — update to current version at build time
```
> In PyInstaller exe mode `version_info.txt` is not in `_MEIPASS`, so the fallback is used. Keep it in sync with the real version when building.

### 3. QSS rule (add inside `DARK_STYLE`)
```css
QPushButton#btn_about {
    background-color: transparent;
    color: #666666;
    border: 1px solid #555555;
    border-radius: 9px;
    font-size: 11px;
    font-weight: bold;
    padding: 0px;
    min-width: 18px; max-width: 18px;
    min-height: 18px; max-height: 18px;
}
QPushButton#btn_about:hover { color: #aaaaaa; border-color: #888888; }
```

### 4. Header row in `_build_ui()`
Replace a plain `QLabel` header with a `QHBoxLayout` row containing the label and the button:
```python
preview_hdr_row = QWidget()
preview_hdr_row.setStyleSheet("background: transparent;")
preview_hdr_layout = QHBoxLayout(preview_hdr_row)
preview_hdr_layout.setContentsMargins(0, 0, 0, 0)
preview_hdr_layout.setSpacing(4)
self.lbl_preview_header = QLabel()
self.lbl_preview_header.setObjectName("lbl_section")
preview_hdr_layout.addWidget(self.lbl_preview_header, stretch=1)
self.btn_about = QPushButton("?")
self.btn_about.setObjectName("btn_about")
self.btn_about.setFixedSize(18, 18)
self.btn_about.setCursor(Qt.CursorShape.PointingHandCursor)
self.btn_about.clicked.connect(self._show_about)
self._tt(self.btn_about, "about_tooltip")
preview_hdr_layout.addWidget(self.btn_about)
parent_layout.addWidget(preview_hdr_row)
```

### 5. `_show_about()` method
```python
def _show_about(self) -> None:
    dlg = QDialog(self)
    dlg.setWindowTitle(_t("about_title"))
    dlg.setFixedWidth(300)
    layout = QVBoxLayout(dlg)
    layout.setSpacing(12)
    lbl = QLabel(
        f"<b>AppName</b> v{_APP_VERSION}<br><br>"
        f"{_t('about_desc')}<br><br>"
        f"<b>{_t('about_author')}</b> {_APP_AUTHOR}<br>"
        f"<b>{_t('about_license')}</b> {_APP_LICENSE}<br><br>"
        f"<a href='{_GITHUB_URL}' style='color:#4a9eff;'>{_GITHUB_URL}</a>"
    )
    lbl.setWordWrap(True)
    lbl.setOpenExternalLinks(True)
    lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    layout.addWidget(lbl)
    btn_close = QPushButton(_t("about_close"))
    btn_close.clicked.connect(dlg.accept)
    layout.addWidget(btn_close)
    dlg.exec()
```

### 6. i18n keys to add in `STRINGS` (both EN and IT)
```python
"about_tooltip": "About / GitHub",          # IT: "Informazioni / GitHub"
"about_title":   "About AppName",            # IT: "Informazioni su AppName"
"about_desc":    "Short description here.",  # IT: "Descrizione breve."
"about_author":  "Author:",                  # IT: "Autore:"
"about_license": "License:",                 # IT: "Licenza:"
"about_close":   "Close",                    # IT: "Chiudi"
```

### 7. Required import
Add `QDialog` to the `from PySide6.QtWidgets import (...)` block.

## scripts/ Rules
> **All `.bat` in `scripts/` must start with `cd /d "%~dp0.."` as first operation.**
> Without this, relative paths (`venv\`, `requirements.txt`, `src\`) resolve inside
> `scripts\` instead of the project root.

## Important Rules
- Do not modify `requirements.txt` without explaining what is being added and why
- Do not rename existing files without asking first
- Do not create files outside the defined structure

## Versioning
- Version source of truth: `scripts/version_info.txt` (fields `FileVersion` and `ProductVersion`)
- To release a new version: update both fields in `version_info.txt`, then commit with `bump:`
- Build output is automatically named `dist\RembgExporter_V<version>.exe` (e.g. `RembgExporter_V1.0.0.exe`)
- `setup.bat` uses `--upgrade-deps` so pip/setuptools in the venv are always up to date

## Commit Conventions
- `feat:` new feature
- `fix:` bug fix
- `refactor:` refactoring without functional change
- `style:` colors, layout, UI without logic change
- `docs:` documentation only
- `test:` add/modify tests
- `bump:` version update

## What NOT to Do
- Do not hardcode absolute paths — use `resource_path()` from `src/utils/path_utils.py` or `os.path.join()`
- Do not commit `venv/`, `dist/`, `build/`, `start.bat`
- Do not use global variables
- Do not leave commented-out code without explanation
