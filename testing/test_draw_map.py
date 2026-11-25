"""The draw skill's map.py: what it places, what it says it places, and how it reads a Zone.

Each test plants a small world folder in a temporary directory and runs map.py on it (--offline,
and --no-image unless the test says otherwise), then reads the printed summary and the page's
data:

- test_shape_read_as_written: three zones on one Map (`shape: line`, only `atlas_shape: line`,
  none); the first is a line and the other two polygons, as the map-space profile reads `shape`.
- test_older_line_mark_is_named: the summary names the second zone, and only it, as carrying a
  line mark in an older key and no shape.
- test_an_id_field_that_is_no_string_names_nothing: an id field holding a list or an object names
  nothing, as a missing one does; the page is written and nothing raises.
- test_a_map_of_size_zero_counts_its_points_apart: a stated 0 x 0 and a measured 0 x 0 beside a
  sized map; only the sized map's pin is placed, the other two are counted as not placed.
- test_a_map_with_one_slot_of_size_zero_has_no_canvas: a stated width with a stated height of 0,
  a stated width with a measured height of 0, a negative width, and a zone on a 0 x 0 map: none
  has a canvas, and their pins and zones are counted as not placed, never as placed; a canvas
  with a stated width and a measured height says only its height was measured, one with a
  stated height only its width, and one with neither stated its size.
- test_a_map_with_no_size_and_an_image: a 0 x 0 map with an image_url, and a map with only an
  image_url, wait on their image when images load (in neither total, one line saying the page
  places the pin if the image loads) and are not placed with --no-image (counted, the reason
  given as the images not being loaded).
- test_the_page_script_reads_the_state: the page's script, pinned as text (no test runs it), a
  tripwire for the plain slip: it shows the note and the size words it is handed, and the pins
  catch a text of its own added or changed whole (a note, words about how a size was found other
  than "(from its image)", a change of `place` where it should not), never words built from pieces.
- test_the_page_counts_the_files_not_read_and_names_none: a hidden Location with a pin on it, a
  second file holding its id, six files that are not JSON and an element of a type outside the
  22: the page's bytes hold none of their file names, not the hidden one's id or name, and say
  "7 files not read."; the terminal names all seven.
- test_a_folder_that_reads_whole_draws_the_same_page: no line about files not read when every
  file reads, and one file that does not read adds that one line to the page and nothing else.

The page's data carries each map's `place` (canvas, image, unloaded, none), its size words
(`size`) and the page's notes for a map with no canvas, so its script writes no note of its own
and no words about how a size was found but "(from its image)"; its count line is its own and
reads `place`. The tests read the data beside the summary.

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


def _draw(root, out, images=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(MAP), str(root), "--out", str(out), "--offline",
                           *([] if images else ["--no-image"])],
                          capture_output=True, text=True, encoding="utf-8", env=env)


def _page_data(out):
    page = (out / "map.html").read_text(encoding="utf-8")
    return json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S).group(1))


def _pin(n, m, x, y, loc):
    return ("pin", {"id": f"019a9000-0000-7000-8000-0000000f1{n:03d}", "name": f"p{n}", "map": m,
                    "element_type": "location", "element_id": loc, "x": x, "y": y})


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
    from, the page does not place its points, and the summary counts them as not placed, never as
    placed. A Map with a real size beside it keeps its count."""
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
        sizes = {m["name"]: (m["w"], m["h"], m["place"]) for m in data["maps"]}
        assert sizes == {"Flat Chart": (0, 0, "none"), "Bare Chart": (0, 0, "none"),
                         "Real Chart": (100, 80, "canvas")}, sizes
        assert "3 maps, 1 pins and 0 zones placed." in r.stdout, r.stdout
        assert "Not placed: 2 pins on maps with no size." in r.stdout, r.stdout
        assert ("- 2 pins sit on maps with no size (Bare Chart, Flat Chart) and are not placed: the maps "
                "have no image to take a size from.") in r.stdout, r.stdout
        assert "- Flat Chart: 1 pins, 0 zones (no size: width 0, height 0), not placed" in r.stdout, r.stdout
        assert ("- Bare Chart: 1 pins, 0 zones (no size: width 0 measured, height 0 measured), not placed"
                in r.stdout), r.stdout
        assert "no stated size" not in r.stdout, r.stdout
        # The page's note for these maps is handed to it in the data and gives the summary's reason.
        assert data["notes"]["none"] == ("It has no image to take a size from: its pins and zones are not "
                                         "placed."), data["notes"]


def test_a_map_with_one_slot_of_size_zero_has_no_canvas():
    """A canvas needs both slots greater than 0: a width with a height of 0 (stated, or measured
    from points on the axis) is no canvas, nor is a negative width. Their pins, and a zone on a
    0 x 0 map, are counted as not placed, by kind ("on maps" when a kind sits on more than one);
    nothing of them is in the placed totals. A canvas with one slot stated and the other measured
    says which one was measured, and one with neither stated says its size was, on its line and in
    the size words the page is handed."""
    loc = "019a9000-0000-7000-8000-0000000e0001"
    half, strip, neg, flat, real, zone = (f"019a9000-0000-7000-8000-0000000e00{n}" for n in (31, 32, 33, 34, 35, 36))
    tall, wide, nonums = (f"019a9000-0000-7000-8000-0000000e00{n}" for n in (37, 38, 39))
    rows = [("location", {"id": loc, "name": "Harbour"}),
            ("map", {"id": tall, "name": "Tall", "width": 100}), _pin(6, tall, 10, 10, loc),
            ("map", {"id": wide, "name": "Wide", "height": 80}), _pin(7, wide, 40, 10, loc),
            ("map", {"id": nonums, "name": "NoNums"}), _pin(8, nonums, 10, 12, loc),
            ("map", {"id": half, "name": "Half", "width": 100, "height": 0}),
            ("map", {"id": strip, "name": "Strip", "width": 100}),
            ("map", {"id": neg, "name": "Neg", "width": -50, "height": 80}),
            ("map", {"id": flat, "name": "Flat", "width": 0, "height": 0}),
            ("map", {"id": real, "name": "Real", "width": 100, "height": 80}),
            _pin(1, half, 10, 10, loc), _pin(2, strip, 10, 0, loc), _pin(3, strip, 40, 0, loc),
            _pin(4, neg, 10, 10, loc), _pin(5, real, 5, 6, loc),
            ("zone", {"id": zone, "name": "Marsh"})]
    rows += [("marker", {"id": f"019a9000-0000-7000-8000-0000000f2{k:03d}", "name": f"k{k}", "map": flat,
                         "zone": zone, "x": x, "y": y, "order": k}) for k, (x, y) in enumerate(((1, 1), (5, 1), (5, 5)))]
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        _plant(root, rows)
        r = _draw(root, out)
        assert r.returncode == 0, r.stderr
        data = _page_data(out)
    places = {m["name"]: (m["w"], m["h"], m["place"], m["measured"]) for m in data["maps"]}
    assert places == {"Half": (100, 0, "none", ""), "Strip": (100, 0, "none", "height"),
                      "Neg": (-50, 80, "none", ""), "Flat": (0, 0, "none", ""),
                      "Real": (100, 80, "canvas", ""), "Tall": (100, 10, "canvas", "height"),
                      "Wide": (40, 80, "canvas", "width"), "NoNums": (10, 12, "canvas", "size")}, places
    sizes = {m["name"]: m["size"] for m in data["maps"] if m["place"] == "canvas"}
    assert sizes == {"Real": "", "Tall": "height measured from its points",
                     "Wide": "width measured from its points", "NoNums": "size measured from its points"}, sizes
    assert "8 maps, 4 pins and 0 zones placed." in r.stdout, r.stdout
    assert "Not placed: 4 pins on maps with no size, 1 zone on a map with no size." in r.stdout, r.stdout
    assert "- Tall: 1 pins, 0 zones (height measured from its points)\n" in r.stdout, r.stdout
    assert "- Wide: 1 pins, 0 zones (width measured from its points)\n" in r.stdout, r.stdout
    assert "- NoNums: 1 pins, 0 zones (size measured from its points)\n" in r.stdout, r.stdout
    assert ("- 4 pins and 1 zone sit on maps with no size (Flat, Half, Neg, Strip) and are not placed: "
            "the maps have no image to take a size from.") in r.stdout, r.stdout
    for line in ("- Half: 1 pins, 0 zones (no size: width 100, height 0), not placed",
                 "- Strip: 2 pins, 0 zones (no size: width 100, height 0 measured), not placed",
                 "- Neg: 1 pins, 0 zones (no size: width -50, height 80), not placed",
                 "- Flat: 0 pins, 1 zones (no size: width 0, height 0), not placed",
                 "- Real: 1 pins, 0 zones\n"):
        assert line in r.stdout, (line, r.stdout)


def test_a_map_with_no_size_and_an_image():
    """A 0 x 0 map with an image_url: when the page loads images, it takes the size from the image
    if it loads, so the summary counts the pin in neither total and says so with "if"; with
    --no-image the pin is not placed, and the reason is that the images are not loaded, never that
    the map has no image. A map with only an image_url (no size, no point) waits on its image the
    same way. The page's notes for these maps are handed to it in the data and give the same reason
    as the summary."""
    loc = "019a9000-0000-7000-8000-0000000e0001"
    flat, only = "019a9000-0000-7000-8000-0000000e0041", "019a9000-0000-7000-8000-0000000e0042"
    rows = [("location", {"id": loc, "name": "Harbour"}),
            ("map", {"id": flat, "name": "Flat", "width": 0, "height": 0,
                     "image_url": "https://example.invalid/chart.png"}),
            ("map", {"id": only, "name": "Only Image", "image_url": "https://example.invalid/only.png"}),
            _pin(1, flat, 3, 4, loc)]
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "world"
        _plant(root, rows)
        on = _draw(root, Path(d) / "on", images=True)
        off = _draw(root, Path(d) / "off")
        assert on.returncode == 0 and off.returncode == 0, (on.stderr, off.stderr)
        data_on, data_off = _page_data(Path(d) / "on"), _page_data(Path(d) / "off")
    place_on = {m["name"]: m["place"] for m in data_on["maps"]}
    place_off = {m["name"]: m["place"] for m in data_off["maps"]}
    assert place_on == {"Flat": "image", "Only Image": "image"}, place_on
    assert place_off == {"Flat": "unloaded", "Only Image": "unloaded"}, place_off
    for r in (on, off):
        assert "- Only Image: 0 pins, 0 zones (no stated size)\n" in r.stdout, r.stdout
    notes = data_on["notes"]
    assert data_off["notes"] == notes and set(notes) == {"image", "unloaded", "none", "failed"}, notes
    assert notes["image"] == ("Its image is loading: its pins and zones are placed if it loads and gives "
                              "a size."), notes
    assert notes["unloaded"] == ("The map images are not loaded (--no-image), so its image cannot give a "
                                 "size: its pins and zones are not placed."), notes
    assert notes["failed"] == "Its image did not load or gave no size: its pins and zones are not placed.", notes
    assert "2 maps, 0 pins and 0 zones placed." in on.stdout and "Not placed: nothing." in on.stdout, on.stdout
    assert ("- 1 pin sits on a map with no size (Flat): the page places it if the map's image loads and "
            "gives a size.") in on.stdout, on.stdout
    assert ("- Flat: 1 pins, 0 zones (no size: width 0, height 0), placed if its image loads and gives a size"
            in on.stdout), on.stdout
    assert "2 maps, 0 pins and 0 zones placed." in off.stdout, off.stdout
    assert "Not placed: 1 pin on a map with no size." in off.stdout, off.stdout
    assert ("- 1 pin sits on a map with no size (Flat) and is not placed: the map images are not loaded "
            "(--no-image), so its image cannot give a size.") in off.stdout, off.stdout
    assert "- Flat: 1 pins, 0 zones (no size: width 0, height 0), not placed" in off.stdout, off.stdout
    for r in (on, off):
        assert "no image to take" not in r.stdout and " when " not in r.stdout, r.stdout


def test_the_page_script_reads_the_state():
    """No test here runs the page's script, so its text is pinned, as a tripwire for the plain slip:
    it shows the note and the size words it is handed (no note of its own, and no words about how a
    size was found but "(from its image)", which only the browser can know); its count line ("N pins,
    M zones placed") is its own and reads `place`; it sets `place` to canvas once (an image that
    loads with a size) and to failed in two places (an image with no size, an image that does not
    load); its panel says placed only on a canvas. A text pin catches a text added or changed whole,
    never words built from pieces."""
    src = MAP.read_text(encoding="utf-8")
    start = src.index('MAP_JS = VIEW_JS + r"""') + len('MAP_JS = VIEW_JS + r"""')
    js = src[start:src.index('"""', start)]
    assert js.count("panel(m,D.notes[m.place])") == 1, js
    assert js.count("m.sized?' (from its image)':m.size?' ('+m.size+')':''") == 1, js
    # A tripwire for the plain slip, no more: the script holds no double quote and no backtick, so
    # every text in it is single-quoted and the check reads them all, and of those that name a size
    # or how it was found only "(from its image)" may stand. It catches a text added whole; it cannot
    # see words built from pieces or copied from a value the script already holds.
    assert '"' not in js and "`" not in js, [ln for ln in js.splitlines() if '"' in ln or "`" in ln]
    texts = re.findall(r"'([^'\n]*)'", js)
    found = [t for t in texts if re.search(r"measur|from its|stated|(?<!-)\bsize\b", t)]
    assert found == [" (from its image)"], found
    assert js.count("m.place='canvas'") == 1 and js.count("m.place='failed'") == 2, js
    assert js.count("const on=m.place==='canvas'") == 1 and js.count("(on?'placed'") == 1, js
    assert js.count(":'not placed'+(m.unplaced?") == 1, js
    for words in ("image to take", "--no-image", "is loading", "did not load"):
        assert words not in js, words


# Files not read: a page is handed on, and a file that did not read can belong to an element the
# page leaves out, so the page counts them and names none; the terminal names each, with its reason.
HUSH = "019a9000-0000-7000-8000-00000000d1d1"
HUSH_NAME = "Hushed harbour"
MARK = "unreadmark-q7x"
TWIN = "zz-twin-of-hidden"
OUTSIDE = "outside-the-types"
UNREAD = [f"location/{TWIN}.json"] + [f"pin/{MARK}-{n}.json" for n in range(1, 7)]
# The page's fixed sentence after the count, the same in the three scripts.
UNREAD_WORDS = b"The list, with why each did not read, is in the terminal of whoever drew this page."


def _plant_unread(root, unread=True):
    """A Map with a drawn Location's pin, a hidden Location and its pin, and an element of a type
    outside the 22; with `unread`, a second file holding the hidden Location's id (after it in the
    folder's order, so it is the file not read) and six files that are not JSON, named with MARK."""
    rows = {"map/chart.json": {"id": MAP_ID, "type": "map", "name": "Chart", "width": 100, "height": 100},
            "location/hidden-one.json": {"id": HUSH, "type": "location", "name": HUSH_NAME, "hidden": True},
            "location/the-quay.json": {"id": "019a9000-0000-7000-8000-00000000d0d1", "type": "location",
                                       "name": "The quay"},
            "pin/a.json": _pin(1, MAP_ID, 5, 5, HUSH)[1],
            "pin/b.json": _pin(2, MAP_ID, 9, 9, "019a9000-0000-7000-8000-00000000d0d1")[1],
            f"widget/{OUTSIDE}.json": {"id": "019a9000-0000-7000-8000-00000000d0d2", "type": "widget",
                                       "name": "Odd gadget"}}
    if unread:
        rows[f"location/{TWIN}.json"] = {"id": HUSH, "type": "location", "name": "Twin"}
    for rel, body in rows.items():
        p = root / "elements" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"type": rel.split("/")[0], **body}), encoding="utf-8")
    if unread:
        for n in range(1, 7):
            (root / "elements" / "pin" / f"{MARK}-{n}.json").write_text("{ not json", encoding="utf-8")
    (root / "world.json").write_text(json.dumps({"id": "w", "name": "Coast"}), encoding="utf-8")


def _draw_unread(plant):
    """(stdout, the page's bytes) for the folder `plant` makes."""
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        plant(root)
        r = _draw(root, out)
        assert r.returncode == 0, r.stderr
        return r.stdout, (out / "map.html").read_bytes()


def test_the_page_counts_the_files_not_read_and_names_none():
    text, page = _draw_unread(_plant_unread)
    low = page.decode("utf-8").casefold()
    found = [w for w in (TWIN, MARK, OUTSIDE, "hidden-one", HUSH, HUSH_NAME) if w.casefold() in low]
    assert not found, found
    assert b"7 files not read." in page, page.decode("utf-8")[-1500:]
    missing = [rel for rel in UNREAD if rel not in text]
    assert not missing and "7 files not read" in text, (missing, text)
    print(f"the page holds the count and no name; the terminal names all {len(UNREAD)}")


def test_a_folder_that_reads_whole_draws_the_same_page():
    """No line about files not read when every file reads; a file that does not read changes the
    page by that one line and nothing else (the time of the read taken out)."""
    def one_broken(root):
        _plant_unread(root, unread=False)
        (root / "elements" / "pin" / "broken.json").write_text("{", encoding="utf-8")
    stamp = re.compile(rb"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")
    _, clean = _draw_unread(lambda root: _plant_unread(root, unread=False))
    _, one = _draw_unread(one_broken)
    assert b"not read" not in clean, clean
    a, b = stamp.sub(b"T", clean), stamp.sub(b"T", one)
    assert b == a.replace(b'<div id="ms">', b"<div>1 file not read. " + UNREAD_WORDS + b'</div><div id="ms">'), b


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
