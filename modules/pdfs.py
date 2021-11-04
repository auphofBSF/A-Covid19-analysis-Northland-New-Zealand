import logging

log = logging.getLogger(__name__)
if not logging.getLogger().hasHandlers():
    # assume logging not active so use print114
    log.error = log.info = log.warn = print

import os, platform

if platform.system() == "Windows":
    install_path_ghostscript = r"C:\Program Files\gs\gs9.55.0\bin"
    os.environ["path"] = ";".join([os.environ["path"], install_path_ghostscript])
    import ctypes
    from ctypes.util import find_library

    if not find_library(
        "".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll"))
    ):
        log.error(f"Unable to find Ghostscript at :{install_path_ghostscript} ")
        global camelot
        camelot = None
    else:
        log.info(f"Detected Ghostscript installed at: {install_path_ghostscript}")
        import camelot
