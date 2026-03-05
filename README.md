# RembgExporter

**RembgExporter** is a desktop app that removes backgrounds from images using AI and converts them into the format you need — Windows icons, web favicons, app store assets, or common image formats like PNG, WebP and JPG.

It works on **Windows, Linux and macOS**, it's free and open source.

---

## Processing Modes

### 🔧 1. Convert ICO — Full pipeline for Windows icons

Combines three operations in a pipeline:
1. **AI background removal** — powered by [rembg](https://github.com/danielgatis/rembg)
2. **Crop to square** — Centers the image on a transparent background
3. **Multi-resolution ICO conversion** — powered by [ImageMagick](https://imagemagick.org)

**Available AI models** (selectable from the GUI):

| Model | Characteristics |
|---|---|
| `birefnet-general` | **Most precise**, sharp edges — recommended |
| `birefnet-general-lite` | Fast, slightly lower quality |
| `isnet-general-use` | Robust alternative for complex objects |
| `u2net` | Fast, ideal for large batches |
| `u2net_human_seg` | Optimized for human subjects |
| `isnet-anime` | For illustrations, cartoons and anime |

> Models are downloaded automatically on first use to `~/.u2net/` and then reused from local cache. No internet connection required for subsequent uses.

**Generated output:**
```
filename_nobg.png        # PNG with transparent background (if background removal is active)
filename.ico             # Multi-resolution icon 16 · 24 · 32 · 48 · 64 · 128 · 256 px
```

---

### 🌐 2. Favicon Generator — Complete favicon for websites

Generates a complete favicon package for modern websites and PWAs.
Optionally supports AI background removal and crop to square.

**Generated files:**
```
favicon.ico              # Multi-frame icon (7 resolutions)
favicon.png              # 32×32 for modern browsers
favicon-192.png          # 192×192 for Android
favicon-512.png          # 512×512 for iOS
manifest.json            # PWA manifest with icon references
```

**Usage:** Copy files to the website root and add to `<head>`:
```html
<link rel="icon" href="/favicon.ico">
<link rel="manifest" href="/manifest.json">
```

> Supports PNG, JPG and SVG images. SVG is automatically rendered to 512×512.

---

### 📱 3. App Store Icons — Optimized icons for app stores

Generates icons with exact dimensions for the main app stores.
Optionally supports AI background removal and crop to square.

**Google Play Store:**
```
play_store_512.png       # 512×512 main icon
```

**Apple App Store:**
```
app_store_1024.png       # 1024×1024 main icon
iphone_180.png           # 180×180 iPhone
ipad_pro_167.png         # 167×167 iPad Pro
ipad_152.png             # 152×152 iPad standard
```

**Microsoft Store:**
```
tile_150.png             # 150×150 standard tile
tile_70.png              # 70×70 small tile
```

> Select the store from the dropdown menu. Images are automatically resized and optimized.

---

### 🎨 4. Format Conversion — Batch conversion between formats

Converts images between formats with quality control.
Optionally supports **AI background removal** and **crop to square** before conversion.

**Supported formats:**
- PNG (lossless)
- JPG (lossy, quality 1-100) — white background if background removal is active
- WebP (modern, quality 1-100)
- GIF

**Quality control:** Slider 1-100 (for JPG and WebP)

**Generated output:**
```
filename.png / .jpg / .webp / .gif    # In the selected format
```

> Supports batch processing: load multiple files at once.

---

## Available Operations

The operations in the **Operations** section adapt to the selected mode:

| Operation | ICO | Favicon | App Store | Format |
|---|---|---|---|---|
| 1. Remove background (AI) | ✅ | ✅ | ✅ | ✅ |
| 2. Crop to square | ✅ | ✅ | ✅ | — |
| 3. Output | ICO/PNG checkbox | fixed info | fixed info | dynamic info |

> In non-ICO modes, operation 3 shows an informational label about the fixed or selected output.

---

## Using the App

### Main interface

The interface is divided into three panels:

- **Left sidebar** — Image list: add, remove single files or clear all. Click a file to select it and update the preview
- **Center panel** — All options: mode, operations, destination, start and log
- **Right sidebar (Preview)** — Shows in real time the original image and the expected result based on current settings:
  - If the image is non-square and "Crop to square" is active: shows the applied transparent padding
  - If the image is non-square and "Crop to square" is inactive (in ICO/Favicon/AppStore mode): shows the distorted result with ⚠ warning
  - The preview automatically adapts to window resizing

**Workflow:**
1. **Add files** with the "+ Add" button (PNG, JPG, SVG, BMP, WebP, GIF)
2. **Choose the mode** in the "Mode" section
3. **Configure operations** (background removal, AI model, crop)
4. **Choose the output destination** (same folder or custom)
5. **Start** with the "PROCESS" button
6. **Monitor** progress in the progress bar and log

### Language

The app supports **English** and **Italian**. Use the **IT | EN** toggle in the top-left of the image sidebar to switch language.

### Tooltips

All buttons, checkboxes and menus show a **descriptive tooltip** on mouse hover (500ms delay).

---

## Project structure

```
rembgexporter/
├── requirements.txt
├── start.bat                       # Launch shortcut (generated by scripts\setup.bat)
│
├── scripts/
│   ├── setup.bat                   # Creates venv, installs deps, generates start.bat
│   ├── build.bat                   # Builds exe with PyInstaller
│   └── version_info.txt            # Windows metadata (author, version, copyright)
│
├── src/
│   ├── main.py                     # Entry point
│   ├── ui/
│   │   └── app.py                  # GUI interface (PySide6)
│   ├── core/
│   │   └── core.py                 # Image processing pipeline
│   ├── utils/
│   │   └── path_utils.py           # resource_path() for dev and PyInstaller
│   ├── assets/
│   │   └── RembgExporter.ico
│   └── third-party/
│       └── imagemagick/            # ImageMagick 7.1.2 portable
│           └── magick.exe
│
├── tests/
├── venv/                           # Virtual environment (created by setup.bat)
└── dist/                           # Portable exe (generated by build.bat)
```

---

## Installation

```bat
git clone https://github.com/zoott28354/rembgexporter.git
cd rembgexporter
scripts\setup.bat
```

`scripts\setup.bat` creates the virtual environment, installs all dependencies and generates `start.bat`.

**Requirements:** Python 3.10+ installed on the system.

> **Windows:** ImageMagick is already included (`src/third-party/imagemagick/magick.exe`) — no additional download required.
>
> **Linux:** Install ImageMagick via `sudo apt install imagemagick`.
>
> **macOS:** Install ImageMagick via `brew install imagemagick`.

---

## Launch

**Windows:**
```bat
start.bat
```
Starts the app using `pythonw.exe` — no CMD window. Generated automatically by `scripts\setup.bat`.

**Linux / macOS:**
```bash
python3 src/main.py
```

---

## Build portable exe

```bat
scripts\build.bat
```

Generates `dist\RembgExporter_V<version>.exe` via PyInstaller — single executable, no installation required.
The version is read automatically from `scripts\version_info.txt` (e.g. `RembgExporter_V1.0.0.exe`).

**Included in the distribution:**
- ✅ All Python dependencies (rembg, Pillow, PySide6, svglib, reportlab, etc.)
- ✅ **ImageMagick 7.1.2** (for perfect ICO creation)
- ✅ Windows metadata (author, copyright, GitHub URL visible in Properties → Details)

**Not included (downloaded on first use):**
- rembg AI models: downloaded to `~/.u2net/` on first use on each machine

---

## Data and storage

The app does not save any configuration file — all settings reset to default on each launch.

| What | Where | Notes |
|---|---|---|
| **AI models** (rembg) | `~/.u2net/` | Downloaded automatically on first use per model, then reused from cache. Safe to delete to free disk space (~100–200 MB per model). |
| **Output files** | Same folder as source **or** custom folder | Chosen in the "Output destination" section before processing. |
| **Virtual environment** | `venv/` in project root | Created by `scripts\setup.bat`. Can be deleted and recreated at any time. |
| **PyInstaller cache** | `build/` in project root | Temporary build folder, safe to delete after building. |

> **Model cache path by OS:**
> - Windows: `C:\Users\<name>\.u2net\`
> - Linux/macOS: `~/.u2net/`

---

## Main dependencies

### Python (pip)

| Package | Role |
|---|---|
| `rembg` | AI background removal |
| `Pillow` | Image manipulation |
| `onnxruntime` | AI model execution (CPU) |
| `PySide6` | Cross-platform GUI (LGPL) |
| `svglib` + `reportlab` | SVG to PNG rendering |
| `pyinstaller` | Portable exe build |

### External (included in distribution)

| Tool | Role | Version |
|---|---|---|
| **ImageMagick** | Multi-frame ICO creation, favicon, app store icons, format conversion | 7.1.2-Q16-HDRI |

---

## Technologies used

| Technology | Usage |
|---|---|
| **Python 3.10+** | Main language |
| **PySide6** | Cross-platform GUI with dark theme (LGPL) |
| **rembg** | AI background removal (deep neural networks) |
| **Pillow (PIL)** | Image manipulation and color profiles |
| **ImageMagick CLI** | Batch processing, multi-frame ICO creation, format conversion |
| **svglib + reportlab** | SVG → PNG rendering |
| **ONNX Runtime** | Accelerated AI model execution (CPU) |
| **PyInstaller** | Portable exe packaging |

---

## Usage examples

### Example 1: Create a Windows icon from a PNG logo

```
1. Add logo.png
2. Choose "Convert ICO"
3. Select AI model (birefnet-general recommended)
4. ✅ Enable background removal and crop to square
5. Click "PROCESS"
```
**Output:** `logo_nobg.png`, `logo.ico` (7 resolutions: 16→256px)

### Example 2: Create favicon for a website

```
1. Add logo_square.png (at least 512×512)
2. Choose "Favicon Generator"
3. Click "PROCESS"
```
**Output:** `favicon.ico`, `favicon.png`, `favicon-192.png`, `favicon-512.png`, `manifest.json`

### Example 3: Prepare icons for Apple App Store

```
1. Add app_icon.png (1024×1024 minimum)
2. Choose "App Store Icons"
3. Select "Apple App Store" from the menu
4. Click "PROCESS"
```
**Output:** `app_store_1024.png`, `iphone_180.png`, `ipad_pro_167.png`, `ipad_152.png`

### Example 4: Convert photo to WebP with background removed

```
1. Add photo.jpg
2. Choose "Format Conversion"
3. Select format "WebP", quality 80
4. ✅ Enable background removal
5. Click "PROCESS"
```
**Output:** `photo.webp` with transparent background
