"""The read skill's count and the draw skill's graph split a folder the same way: a Zone is
content (an element, a node), and map space is Map, Pin and Marker, the lens profile's graph
section's rule, which graph.py reads through the onlyworlds package and count.py applies to its
own id map. A folder with one of each, and a Character linking the Zone and the Pin, is counted
by both; the Zone must be in both counts and the Pin in neither."""

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNT = ROOT / "skills" / "onlyworlds-read" / "scripts" / "count.py"
GRAPH = ROOT / "skills" / "onlyworlds-draw" / "scripts" / "graph.py"


def _write(folder, type_slug, body):
    d = folder / "elements" / type_slug
    d.mkdir(parents=True, exist_ok=True)
    body = {"id": str(uuid.uuid4()), "type": type_slug, **body}
    (d / f"{body['id']}.json").write_text(json.dumps(body), encoding="utf-8")
    return body["id"]


def _run(script, folder, *args):
    r = subprocess.run([sys.executable, str(script), str(folder), *args], capture_output=True,
                       text=True, encoding="utf-8", cwd=str(folder.parent))
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_a_zone_is_an_element_for_both_and_a_pin_is_map_space_for_both(tmp_path):
    folder = tmp_path / "split"
    folder.mkdir()
    (folder / "world.json").write_text(json.dumps({"name": "Split"}), encoding="utf-8")
    zone = _write(folder, "zone", {"name": "The March"})
    pin = _write(folder, "pin", {"name": "A stone", "x": 1, "y": 2})
    place = _write(folder, "location", {"name": "The Keep", "zone": zone})
    _write(folder, "character", {"name": "Ada", "location": place, "birthplace": place})
    _write(folder, "map", {"name": "Chart", "width": 10, "height": 10})
    count = json.loads(_run(COUNT, folder, "--json"))
    assert count["total"] == 5 and count["placement"] == 2 and count["elements"] == 3
    assert count["left_out"]["placement"] == 2
    out = tmp_path / "draw"
    text = _run(GRAPH, folder, "--offline", "--out", str(out))
    graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))
    types = sorted(n["type"] for n in graph["nodes"])
    assert types == ["character", "location", "zone"]
    assert "3 elements and 3 links drawn, of 5 in the folder. Left out: 2 map space (map, pin, marker)." in text
    assert zone in {n["id"] for n in graph["nodes"]} and pin not in {n["id"] for n in graph["nodes"]}
    # Both say the same split in their words.
    assert f"of which 2 placement (map, pin, marker)" in _run(COUNT, folder)
