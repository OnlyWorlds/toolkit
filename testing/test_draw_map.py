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


def _plant(root, rows):
    for n, (t, e) in enumerate(rows):
        p = root / "elements" / t / f"e{n:02d}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"type": t, **e}), encoding="utf-8")
    (root / "world.json").write_text(json.dumps({"id": "w", "name": "Coast"}), encoding="utf-8")


def _draw(root, out):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(MAP), str(root), "--out", str(out), "--offline", "--no-image"],
                          capture_output=True, text=True, encoding="utf-8", env=env)


def test_an_id_field_that_is_no_string_names_nothing():
    """A field that should hold an id and holds a list or an object names nothing, as a missing
    one does: a Map's location and parent_map, a Pin's map and element_id, a Marker's map and zone,
    a Location's parent_location; an element whose own id is a list is a file not read. The page
    is written; nothing raises."""
    loc, ch, zone = (f"019a9000-0000-7000-8000-0000000d000{n}" for n in (1, 2, 3))
    rows = [("location", {"id": loc, "name": "Harbour"}),
            ("character", {"id": ch, "name": "Ada"}),
            ("character", {"id": [ch], "name": "Bram"}),
            ("map", {"id": MAP_ID, "name": "Coast", "width": 100, "height": 80,
                     "location": [loc], "parent_map": {"id": MAP_ID}}),
            ("pin", {"id": "019a9000-0000-7000-8000-0000000d0011", "name": "p1", "map": [MAP_ID],
                     "element_type": "character", "element_id": ch, "x": 1, "y": 2}),
            ("pin", {"id": "019a9000-0000-7000-8000-0000000d0012", "name": "p2", "map": MAP_ID,
                     "element_type": "character", "element_id": [ch], "x": 3, "y": 4}),
            ("zone", {"id": zone, "name": "Marsh"}),
            ("marker", {"id": "019a9000-0000-7000-8000-0000000d0021", "name": "m1", "map": [MAP_ID],
                        "zone": zone, "x": 5, "y": 6, "order": 0}),
            ("marker", {"id": "019a9000-0000-7000-8000-0000000d0022", "name": "m2", "map": MAP_ID,
                        "zone": {"id": zone}, "x": 7, "y": 8, "order": 1})]
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        _plant(root, rows)
        r = _draw(root, out)
        assert r.returncode == 0, r.stderr
        page = (out / "map.html").read_text(encoding="utf-8")
        data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S).group(1))
        (m,) = data["maps"]
        assert (m["loc"], m["parent"], m["w"], m["h"]) == ("", None, 100, 80), m
        assert [p["label"] for p in m["pins"]] == ["p2"], m["pins"]
        assert m["zones"] == [], m["zones"]
        assert ("Not placed: 1 pins on no map in the folder, 1 markers on no map in the folder, "
                "1 markers with no zone in the folder.") in r.stdout, r.stdout
        assert "no id" in r.stdout, r.stdout
        # With no Map, the parent_location outline reads a list as no parent.
        root2 = Path(d) / "world2"
        _plant(root2, [("location", {"id": loc, "name": "Harbour", "parent_location": [loc]})])
        r = _draw(root2, Path(d) / "out2")
        assert r.returncode == 0, r.stderr
        assert "- Harbour" in r.stdout, r.stdout


def test_a_map_of_size_zero_counts_its_points_apart():
    """The summary's totals say what the page draws. A Map whose width or height is 0 (stated so,
    or measured from points that all sit on an axis) has no canvas: with no image to take a size
    from (here: --no-image), the page does not place its points, and the summary must not count
    them as placed. A Map with a real size beside it keeps its count."""
    loc = "019a9000-0000-7000-8000-0000000e0001"
    flat, bare, sized = (f"019a9000-0000-7000-8000-0000000e001{n}" for n in (1, 2, 3))
    rows = [("location", {"id": loc, "name": "Harbour"}),
            ("map", {"id": flat, "name": "Flat Chart", "width": 0, "height": 0}),
            ("map", {"id": bare, "name": "Bare Chart"}),
            ("map", {"id": sized, "name": "Real Chart", "width": 100, "height": 80}),
            ("pin", {"id": "019a9000-0000-7000-8000-0000000e0021", "name": "p1", "map": flat,
                     "element_type": "location", "element_id": loc, "x": 3, "y": 4}),
            ("pin", {"id": "019a9000-0000-7000-8000-0000000e0022", "name": "p2", "map": bare,
                     "element_type": "location", "element_id": loc, "x": 0, "y": 0}),
            ("pin", {"id": "019a9000-0000-7000-8000-0000000e0023", "name": "p3", "map": sized,
                     "element_type": "location", "element_id": loc, "x": 5, "y": 6})]
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        _plant(root, rows)
        r = _draw(root, out)
        assert r.returncode == 0, r.stderr
        page = (out / "map.html").read_text(encoding="utf-8")
        data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S).group(1))
        sizes = {m["name"]: (m["w"], m["h"]) for m in data["maps"]}
        assert sizes == {"Flat Chart": (0, 0), "Bare Chart": (0, 0), "Real Chart": (100, 80)}, sizes
        assert "3 maps, 1 pins and 0 zones placed." in r.stdout, r.stdout
        assert ("2 pins and 0 zones sit on a map with no size (Bare Chart, Flat Chart): the page does not "
                "place them, since there is no image to take a size from.") in r.stdout, r.stdout


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
