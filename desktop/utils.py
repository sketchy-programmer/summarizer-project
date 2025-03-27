import os
import sys

def resource_path(relative_path):
    """Get absolute path for bundled images when running as an executable."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
