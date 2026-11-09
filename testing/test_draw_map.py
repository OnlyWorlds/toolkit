"""The draw skill's map.py reads a Zone's shape as the map-space profile does, and says so when a
zone carries a line mark only in an older key.

A three-zone folder is planted in a temporary directory, all on one Map: one zone with
`shape: line`, one with no shape and only `atlas_shape: line`, one plain. map.py is run on it
(--offline --no-image) and the page's data must hold the first as a line and the other two as
polygons (the profile reads `shape` as written), while the printed summary names the second, and
only the second, as a zone with a line mark in an older key and no shape.

OW_DRAW_MAP points at another copy of map.py (an older one, to show this test is red on it).

Runs under pytest, or alone:
    python testing/test_draw_map.py

Python 3, stdlib only.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAP = Path(os.environ.get("OW_DRAW_MAP")
           or ROOT / "skills" / "onlyworlds-draw" / "scripts" / "map.py")

MAP_ID = "019a9000-0000-7000-8000-00000000aa01"
ZONES = [("019a9000-0000-7000-8000-0000000b0001", "Coast Road", {"shape": "line"}),
         ("019a9000-0000-7000-8000-0000000b0002", "Old River", {"atlas_shape": "line"}),
         ("019a9000-0000-7000-8000-0000000b0003", "Marsh", {})]


def _run():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "world"
        rows = [("map", {"id": MAP_ID, "name": "Coast", "width": 100, "height": 100})]
        for n, (zid, name, extra) in enumerate(ZONES):
            rows.append(("zone", {"id": zid, "name": name, **extra}))
            for k in range(3):
                rows.append(("marker", {"id": f"019a9000-0000-7000-8000-0000000c{n}{k:03d}", "name": "corner",
                                        "map": MAP_ID, "zone": zid, "x": 10 * (n + 1) + k, "y": 5 * k,
                                        "order": k}))
        for t, e in rows:
            p = root / "elements" / t / f"{e['id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"type": t, **e}), encoding="utf-8")
        (root / "world.json").write_text(json.dumps({"id": "w", "name": "Coast"}), encoding="utf-8")
        out = Path(d) / "out"
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, str(MAP), str(root), "--out", str(out), "--offline", "--no-image"],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        assert r.returncode == 0, r.stderr
        page = (out / "map.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S).group(1))
    return {z["name"]: z["shape"] for m in data["maps"] for z in m["zones"]}, r.stdout


def test_shape_read_as_written():
    shapes, _ = _run()
    assert shapes == {"Coast Road": "line", "Old River": "polygon", "Marsh": "polygon"}, shapes


def test_older_line_mark_is_named():
    _, summary = _run()
    lines = [ln for ln in summary.splitlines() if "older key" in ln]
    assert len(lines) == 1, summary
    print(lines[0])
    assert lines[0].startswith("- 1 zone carries a line mark") and "Old River" in lines[0], lines[0]
    assert "Coast Road" not in lines[0] and "Marsh" not in lines[0], lines[0]


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {t.__name__}: {e.__class__.__name__}: {e}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
