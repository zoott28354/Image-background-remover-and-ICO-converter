@echo off
:: ── RembgExporter build script ─────────────────────────────────────────────
:: Author : zoott28354
:: GitHub : https://github.com/zoott28354/rembgexporter
:: ─────────────────────────────────────────────────────────────────────────
cd /d "%~dp0.."

echo ==========================================
echo  RembgExporter - Build .exe
echo ==========================================

echo.
if not exist venv\Scripts\python.exe (
    echo Virtual environment not found. Run scripts\setup.bat first.
    pause
    exit /b 1
)

:: Extract ProductVersion from version_info.txt  →  e.g. 1.0.0
for /f "tokens=4 delims='" %%v in ('findstr "ProductVersion" scripts\version_info.txt') do set APP_VERSION=%%v
set EXE_NAME=RembgExporter_V%APP_VERSION%
echo Building version: %APP_VERSION%
echo.

venv\Scripts\python.exe -m PyInstaller --onefile --windowed ^
  --icon=src\assets\RembgExporter.ico ^
  --name=%EXE_NAME% ^
  --version-file=scripts\version_info.txt ^
  --collect-all PySide6 ^
  --collect-all rembg ^
  --collect-all svglib ^
  --collect-all reportlab ^
  --copy-metadata rembg ^
  --copy-metadata pymatting ^
  --copy-metadata onnxruntime ^
  --copy-metadata Pillow ^
  --copy-metadata numpy ^
  --hidden-import=click ^
  --hidden-import=PySide6.QtSvg ^
  --hidden-import=PySide6.QtXml ^
  --hidden-import=PIL.ImageQt ^
  --paths src ^
  --add-data "src\assets;assets" ^
  --add-data "src\third-party\imagemagick;imagemagick" ^
  src\main.py

echo.
if exist "dist\%EXE_NAME%.exe" (
    echo ==========================================
    echo  Build complete: dist\%EXE_NAME%.exe
    echo ==========================================
) else (
    echo ERROR: build failed. Check output above.
)
pause
