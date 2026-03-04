"""Entry point for RembgExporter."""
import ctypes
import os
import sys

# Add src/ to Python path so that 'from ui.app import App' etc. work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Windows AppUserModelID before creating the window (required for taskbar icon)
if sys.platform == "win32":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('RembgExporter.App')
    except Exception:
        pass


def main() -> None:
    """Launch the RembgExporter GUI."""
    from ui.app import run
    run()


if __name__ == "__main__":
    main()
