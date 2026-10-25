#!/usr/bin/env python3
"""Compatibility entry point for the article diagram builder."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("build_diagrams.py")), run_name="__main__")
