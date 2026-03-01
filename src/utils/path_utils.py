"""Utility for resolving resource paths in both dev and PyInstaller modes."""
import os
import sys


def resource_path(name: str) -> str:
    """Resolve a path relative to src/ in dev mode, or _MEIPASS in PyInstaller exe."""
    if getattr(sys, '_MEIPASS', None):
        base = sys._MEIPASS
    else:
        # __file__ is src/utils/path_utils.py → dirname x2 → src/
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)
