"""Rebuild index2.html from the captured public HACOM homev6 page."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    module = runpy.run_path(str(Path(__file__).resolve().parent / "tools/homev6/build.py"))
    module["build"]()
