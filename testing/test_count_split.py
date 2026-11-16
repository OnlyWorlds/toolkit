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


def test_an_element_whose_id_is_a_list_is_a_file_not_read(tmp_path):
    """An id that is a list (or an object) is no id: the file is not read and is named, as a file
    with none is, and the rest is counted."""
    folder = tmp_path / "ids"
    folder.mkdir()
    (folder / "world.json").write_text(json.dumps({"name": "Ids"}), encoding="utf-8")
    ada = _write(folder, "character", {"name": "Ada"})
    d = folder / "elements" / "character"
    (d / "bram.json").write_text(json.dumps({"id": [ada], "type": "character", "name": "Bram"}), encoding="utf-8")
    (d / "cleo.json").write_text(json.dumps({"id": {"id": ada}, "type": "character", "name": "Cleo"}), encoding="utf-8")
    count = json.loads(_run(COUNT, folder, "--json"))
    assert count["total"] == 1 and count["elements"] == 1, count
    assert sorted(n for n in count["notes"] if "no id" in n) == ["elements/character/bram.json: no id",
                                                               "elements/character/cleo.json: no id"], count["notes"]


CONSISTENCY = ROOT / "skills" / "onlyworlds-read" / "scripts" / "consistency.py"


def test_a_pin_whose_element_id_is_a_list_names_nothing(tmp_path):
    """The read skill's consistency report reads a Pin's element_id as the draw skill's map does: a
    list or an object there names no element, as a missing one does, and the report runs on."""
    folder = tmp_path / "pins"
    folder.mkdir()
    (folder / "world.json").write_text(json.dumps({"name": "Pins"}), encoding="utf-8")
    ada = _write(folder, "character", {"name": "Ada"})
    chart = _write(folder, "map", {"name": "Chart", "width": 10, "height": 10})
    _write(folder, "pin", {"name": "A list", "map": chart, "x": 1, "y": 1, "element_id": [ada]})
    _write(folder, "pin", {"name": "An object", "map": chart, "x": 2, "y": 2, "element_id": {"id": ada}})
    _write(folder, "pin", {"name": "Ada's pin", "map": chart, "x": 3, "y": 3, "element_id": ada,
                           "element_type": "character"})
    report = json.loads(_run(CONSISTENCY, folder, "--json"))
    assert not [f for f in report["findings"]["links"] if f.get("field") in ("element_id", "element_type")], report
    assert report["links"] == 4, report  # the three pins' map links and Ada's pin; the list and the object none
