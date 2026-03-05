"""Utility for resolving resource paths in both dev and PyInstaller modes."""
import os
import sys


def resource_path(*parts: str) -> str:
    """Resolve a path relative to src/ in dev mode, or _MEIPASS in PyInstaller exe.

    Accepts multiple path components (like os.path.join) so that the join
    is always done with the correct OS separator at call time.

    Uses the main script's __file__ as source of truth (always correct at
    runtime) rather than this module's __file__, which may contain a stale
    Windows path if the .pyc was compiled on a different OS.
    """
    if getattr(sys, '_MEIPASS', None):
        base = sys._MEIPASS
    else:
        # main.py lives in src/ — its __file__ is always resolved correctly
        # at runtime regardless of where the .pyc was compiled.
        main = sys.modules.get('__main__')
        main_file = getattr(main, '__file__', None)
        if main_file:
            base = os.path.dirname(os.path.abspath(main_file))
        else:
            # Fallback: derive from this module's own path
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)
