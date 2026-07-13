#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.cli import main
raise SystemExit(main(["cad-macro", *__import__("sys").argv[1:]]))
