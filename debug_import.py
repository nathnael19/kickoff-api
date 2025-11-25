import sys
import traceback
import os

with open("error.log", "w") as f:
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"Path: {sys.path}\n")
    try:
        from app.main import app
        f.write("Import successful\n")
    except Exception:
        traceback.print_exc(file=f)
