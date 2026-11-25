"""The two folder loaders (load_world in the read skill's consistency.py and in the draw skill's
graph.py) take the files knowledge/world-folder.md's "Reading a folder" names: a file directly in
a folder under elements/ (or in map, pin, zone or marker under a legacy spatial/), whose name ends
in .json in exactly that case and does not begin with a dot. The fixed names are compared as
written; the order is the path below the world folder by code point, so the file kept of a
repeated id is the same on every system. A name passed over for its case gets a line in skipped;
a dot-file or a dot-folder is passed over in silence. Each case builds its own folder in a
temporary directory and is asserted for both loaders."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LOADERS = {
    "consistency": ROOT / "skills" / "onlyworlds-read" / "scripts" / "consistency.py",
    "graph": ROOT / "skills" / "onlyworlds-draw" / "scripts" / "graph.py",
}


def _module(name):
    path = LOADERS[name]
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(f"loader_files_{name}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(path.parent))
    return mod


MODULES = {name: _module(name) for name in LOADERS}


def _put(world, rel, ident, name=None):
    p = world / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"id": ident, "name": name or ident}), encoding="utf-8")


def _world(tmp_path, files):
    world = tmp_path / "w"
    world.mkdir()
    (world / "world.json").write_text(json.dumps({"id": "w", "name": "W"}), encoding="utf-8")
    for rel, ident in files:
        _put(world, rel, ident)
    return world


def _read(loader, world):
    _, elements, skipped = MODULES[loader].load_world(world)
    return elements, skipped


@pytest.fixture(params=sorted(LOADERS))
def loader(request):
    return request.param


def test_a_dot_file_is_passed_over_in_silence(tmp_path, loader):
    world = _world(tmp_path, [("elements/character/ada.json", "ada"),
                              ("elements/character/.cole.json", "cole"),
                              ("elements/character/.Dunn.JSON", "dunn")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["ada"]
    assert skipped == []


def test_a_dot_folder_is_passed_over_in_silence(tmp_path, loader):
    world = _world(tmp_path, [("elements/character/ada.json", "ada"),
                              ("elements/character/.trash/dunn.json", "dunn"),
                              ("elements/.obsidian/note.json", "note"),
                              ("elements/.Trash/Old.JSON", "old"),
                              ("spatial/.cache/pin.json", "cached")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["ada"]
    assert skipped == []


def test_a_file_one_level_too_deep_is_not_read(tmp_path, loader):
    world = _world(tmp_path, [("elements/character/ada.json", "ada"),
                              ("elements/character/old/bram.json", "bram"),
                              ("elements/stray.json", "stray")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["ada"]
    assert skipped == []


def test_an_upper_case_extension_is_not_read_and_said(tmp_path, loader):
    world = _world(tmp_path, [("elements/location/sluice.json", "sluice"),
                              ("elements/location/Fenwick.JSON", "fenwick"),
                              ("elements/location/marsh.Json", "marsh")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["sluice"]
    assert skipped == [
        "elements/location/Fenwick.JSON: not read (the name must end in .json, in lower case)",
        "elements/location/marsh.Json: not read (the name must end in .json, in lower case)",
    ]


def test_an_upper_case_type_folder_is_not_read_and_said(tmp_path, loader):
    world = _world(tmp_path, [("elements/location/sluice.json", "sluice"),
                              ("elements/Character/ada.json", "ada")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["sluice"]
    assert skipped == ["elements/Character/: not read (a type folder's name is in lower case)"]


def test_an_upper_case_elements_folder_is_not_read_and_said(tmp_path, loader):
    world = _world(tmp_path, [("Elements/character/ada.json", "ada")])
    elements, skipped = _read(loader, world)
    assert elements == {}
    assert skipped == ["Elements/: not read (the folder must be named elements/, in lower case)"]


def test_a_lower_case_folder_that_is_no_type_is_still_read(tmp_path, loader):
    world = _world(tmp_path, [("elements/misc/thing.json", "thing")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["thing"]
    assert skipped == []


def test_spatial_reads_its_four_folders_and_no_fifth(tmp_path, loader):
    world = _world(tmp_path, [("spatial/map/m.json", "m"), ("spatial/pin/p.json", "p"),
                              ("spatial/zone/z.json", "z"), ("spatial/marker/k.json", "k"),
                              ("spatial/misc/x.json", "x"),
                              ("elements/character/ada.json", "ada")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["ada", "k", "m", "p", "z"]
    assert skipped == []


def test_a_repeated_id_keeps_the_first_file_by_code_point(tmp_path, loader):
    # Code point puts "B.json" before "a.json"; a case-blind sort puts "a.json" first.
    world = _world(tmp_path, [("elements/character/a.json", "same"),
                              ("elements/character/B.json", "same")])
    elements, skipped = _read(loader, world)
    assert sorted(elements) == ["same"]
    assert elements["same"]["_file"] == "character/B.json"
    assert skipped == ["character/a.json: id same also in character/B.json"]


def test_elements_before_spatial(tmp_path, loader):
    world = _world(tmp_path, [("spatial/pin/p.json", "same"), ("elements/pin/p.json", "same")])
    elements, skipped = _read(loader, world)
    assert elements["same"]["_file"] == "pin/p.json"
    assert skipped == ["spatial/pin/p.json: id same also in pin/p.json"]


def test_the_two_loaders_read_one_folder_the_same(tmp_path):
    world = _world(tmp_path, [("elements/character/a.json", "same"),
                              ("elements/character/B.json", "same"),
                              ("elements/character/.c.json", "c"),
                              ("elements/location/Fen.JSON", "fen"),
                              ("elements/location/sluice.json", "sluice"),
                              ("spatial/misc/x.json", "x"),
                              ("spatial/zone/z.json", "z")])
    a, b = (_read(name, world) for name in sorted(LOADERS))
    assert a == b
