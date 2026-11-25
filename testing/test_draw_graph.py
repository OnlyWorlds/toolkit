"""The draw skill's graph.py draws exactly the graph the onlyworlds package reads (world_graph, the
lens profile's graph section in schema-dist), for the folder's owner.

A small world is planted in a temporary folder: a Character with a link to itself, a target
listed twice, a link to an element of another type than its field's (a Location in friends, a Pin
in objects), a link to an id that is not in the world, and links to a room element, a hidden one
and a proposed one; a Location in a Zone; a Map, a Pin and a Marker; two Lenses joined by
x_lens_leads_to, an x_spine_depends_on link and an x_ field no profile declares; a Charter with the
mark x_charter_of; a Character file with no type key. graph.py is run on it (--offline) and its
nodes and edges must be world_graph's: the same ids, and the same edges by source, target and
field in the reader's order. Then each rule is pinned by name: a Zone is a node, a self link is
an edge, a repeated target is two, a wrong-type link draws nothing, the two declared x_ links are
edges, the left-out counts are the reader's, a cut never adds an edge, and the page carries a self
edge in its data.

A second planted world holds a hidden element, a second file with its id, six files that are not
JSON and an element of a type outside the 22: the page and graph.json name none of those files
and carry neither the hidden id nor its name, the page counts the seven files not read, and the
terminal names each. A folder whose every file reads has no such line, and one file that does
not read adds that one line to the page and nothing else.

Small worlds then hold an element the World's hidden list names (the picture stays the reader's),
an id two files hold with one copy hidden (in both orders: neither is drawn), a --presentation file
given by its absolute path (the page names no folder), and an element of a type outside the 22
(counted, never named); the 22 types graph.py lists are the package's.

graph.py's left-out rules (hidden, proposed, room, reading aid) stay its own copies, since map.py
imports them and runs on the standard library alone: one table holds each equal to the package's
own function over thirteen values. A proposed mark of false, 0 or 0.0 is left out and one of only
spaces is not, alone and beside a plain copy in either order; an id that is not text is a file
not read; and one world plants every left-out kind, each by every road the graph reads (a link's
target, a copy of its id before and after it, the World's hidden list), and searches both files.

OW_DRAW_GRAPH points at another copy of graph.py (an older one, to show this test is red on it).

Runs under pytest, or alone:
    python testing/test_draw_graph.py

Python 3.12+ and the onlyworlds package (>=0.101.0).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from onlyworlds import world_graph

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GRAPH = Path(os.environ.get("OW_DRAW_GRAPH")
             or ROOT / "skills" / "onlyworlds-draw" / "scripts" / "graph.py")
WORLD = "0199c3a1-7b2e-7c3d-8e4f-000000000002"


def i(n):
    return f"00000000-0000-7000-8000-0000000002{n:02d}"


ADA, BRAM, SWAMPS, HARBOUR, PIN, CHART, LENS, LENS2, CHARTER, MO, HAL, PRU, MARKER = (
    i(n) for n in range(1, 14))
GHOST = i(99)  # an id no element holds

ROWS = {
    "character/ada": {"id": ADA, "name": "Ada", "type": "character",
                      "friends": [ADA, BRAM, BRAM, HARBOUR, GHOST],
                      "rivals": [BRAM, MO, HAL, PRU], "location": HARBOUR, "birthplace": GHOST,
                      "objects": [PIN]},
    # no type key: the folder names the type
    "character/bram": {"id": BRAM, "name": "Bram", "friends": [ADA],
                       "x_spine_depends_on": [HARBOUR], "x_other_links": [ADA],
                       "atlas_seen": [ADA]},
    "zone/the-swamps": {"id": SWAMPS, "name": "The swamps", "type": "zone"},
    "location/the-harbour": {"id": HARBOUR, "name": "The harbour", "type": "location",
                             "zone": SWAMPS},
    "pin/ada-on-the-chart": {"id": PIN, "name": "Ada on the chart", "type": "pin", "map": CHART,
                             "element_type": "character", "element_id": ADA, "x": 1, "y": 2},
    "map/the-chart": {"id": CHART, "name": "The chart", "type": "map"},
    "marker/a-swamp-corner": {"id": MARKER, "name": "A swamp corner", "type": "marker",
                              "map": CHART, "zone": SWAMPS, "x": 3, "y": 4},
    "construct/first-lens": {"id": LENS, "name": "First lens", "type": "construct",
                             "supertype": "Lens", "x_lens_leads_to": [LENS2]},
    "construct/second-lens": {"id": LENS2, "name": "Second lens", "type": "construct",
                              "supertype": "Lens", "x_lens_leads_to": [LENS, GHOST]},
    "law/house-rules": {"id": CHARTER, "name": "House rules", "type": "law",
                        "supertype": "Charter", "x_charter_of": WORLD},
    "character/mo": {"id": MO, "name": "Mo", "type": "character", "supertype": "Member",
                     "x_room_of": WORLD},
    "character/hal": {"id": HAL, "name": "Hal", "type": "character", "hidden": True},
    "character/pru": {"id": PRU, "name": "Pru", "type": "character",
                      "x_review_proposed": "2026-11-02", "friends": [ADA]},
}


def plant(folder):
    (folder / "world.json").write_text(json.dumps({"id": WORLD, "name": "Planted graph"}),
                                       encoding="utf-8")
    for rel, body in ROWS.items():
        p = folder / "elements" / f"{rel}--{body['id'][-8:]}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body, indent=2), encoding="utf-8")


def reader_graph(**flags):
    """What the package reads for the owner, each element's type as its folder names it."""
    elements = [dict(body, type=rel.split("/")[0]) for rel, body in ROWS.items()]
    return world_graph({"elements": elements}, {"rung": "owner"}, **flags)


def draw(*args):
    """graph.py's graph.json, its printed summary and its page, run on the planted world."""
    with tempfile.TemporaryDirectory() as tmp:
        world = Path(tmp) / "world"
        world.mkdir()
        plant(world)
        out = Path(tmp) / "draw"
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(GRAPH), str(world), "--offline", "--out", str(out),
                            *args], capture_output=True, text=True, encoding="utf-8", env=env)
        assert r.returncode == 0, f"graph.py exit {r.returncode}: {r.stderr or r.stdout}"
        graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))
        page = (out / "graph.html").read_text(encoding="utf-8")
    return graph, r.stdout, page


def triples(graph):
    """graph.py's edges as (source id, target id, field), in its order."""
    ids = [n["id"] for n in graph["nodes"]]
    return [(ids[a], ids[b], f) for a, b, f in graph["edges"]]


def reader_triples(read):
    return [(e["source"], e["target"], e["field"]) for e in read["edges"]]


def test_nodes_and_edges_are_the_readers():
    for args, flags in (((), {}), (("--room", "--hidden", "--proposed"),
                                   {"rooms": True, "hidden": True, "proposed": True})):
        graph, _, _ = draw(*args)
        read = reader_graph(**flags)
        drawn = sorted(n["id"] for n in graph["nodes"])
        assert drawn == [n["id"] for n in read["nodes"]], (args, drawn)
        assert triples(graph) == reader_triples(read), (args, triples(graph), reader_triples(read))
        print(f"{' '.join(args) or 'no flags'}: {len(drawn)} nodes, {len(graph['edges'])} edges, "
              "the reader's")


def test_a_zone_is_a_node():
    graph, _, _ = draw()
    assert SWAMPS in {n["id"] for n in graph["nodes"]}, "the Zone is not a node"
    assert (HARBOUR, SWAMPS, "zone") in triples(graph), "the Location's link to its Zone is not drawn"


def test_a_self_link_is_an_edge():
    graph, _, _ = draw()
    assert (ADA, ADA, "friends") in triples(graph), "Ada's link to Ada is not an edge"


def test_a_repeated_target_is_one_edge():
    # serial 128: a multi-link names each element once; a list naming one twice is one edge, in its first place
    graph, _, _ = draw()
    assert triples(graph).count((ADA, BRAM, "friends")) == 1, triples(graph)


def test_a_wrong_type_link_draws_nothing():
    graph, _, _ = draw()
    t = triples(graph)
    assert (ADA, HARBOUR, "friends") not in t, "a Location in friends is drawn"
    assert (ADA, HARBOUR, "location") in t, "the right-typed link to the same Location is gone"
    assert not [e for e in t if PIN in e[:2] or GHOST in e[:2]], t


def test_the_declared_x_links_are_edges():
    graph, _, _ = draw()
    t = triples(graph)
    assert (LENS, LENS2, "x_lens_leads_to") in t and (LENS2, LENS, "x_lens_leads_to") in t, t
    assert (BRAM, HARBOUR, "x_spine_depends_on") in t, t
    assert not [e for e in t if e[2] in ("x_other_links", "atlas_seen")], t


def test_the_left_out_counts_are_the_readers():
    _, text, _ = draw()
    cut = reader_graph()["cut"]
    assert cut == {"room": 1, "hidden": 1, "proposed": 1, "map_space": 3, "reading_aid": 1}, cut
    assert (f"Left out: {cut['map_space']} map space (map, pin, marker), {cut['room']} room, "
            f"{cut['proposed']} proposed, {cut['hidden']} hidden.") in text, text
    assert text.count("The three reading aids are not drawn (1 element).") == 1, text
    assert "placement" not in text and "zone" not in text.split("Left out:")[1].split(".")[0], text


def test_a_cut_never_adds_an_edge():
    whole = triples(draw()[0])
    for args in (("--type", "character"), ("--focus", "The harbour", "--depth", "1")):
        graph, _, _ = draw(*args)
        t = triples(graph)
        kept = {n["id"] for n in graph["nodes"]}
        assert t == [e for e in whole if e[0] in kept and e[1] in kept], (args, t)
    graph, _, _ = draw("--type", "character")
    assert {n["type"] for n in graph["nodes"]} == {"character"}, graph["nodes"]


def test_the_page_carries_a_self_edge():
    graph, _, page = draw()
    m = re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S)
    data = json.loads(m.group(1))
    selfs = [e for e in data["graph"]["edges"] if e[0] == e[1]]
    assert selfs and data["graph"]["edges"] == graph["edges"], data["graph"]["edges"]


# Files not read: a page is handed on, and a file that did not read can belong to an element the
# page leaves out, so the page counts them and names none; the terminal names each, with its reason.
HUSH = "019a7700-0000-7000-8000-00000000d1d1"
HUSH_NAME = "Hushed reckoning"
MARK = "unreadmark-q7x"
TWIN = "zz-twin-of-hidden"
OUTSIDE = "outside-the-types"
UNREAD = [f"construct/{TWIN}.json"] + [f"event/{MARK}-{n}.json" for n in range(1, 7)]


def plant_unread(root, unread=True):
    """A hidden Construct, a drawn Event and Character, a Map, and an element of a type outside the
    22; with `unread`, a second file holding the hidden element's id (after it in the folder's
    order, so it is the file not read) and six files that are not JSON, named with MARK."""
    rows = {"construct/hidden-one.json": {"id": HUSH, "type": "construct", "name": HUSH_NAME,
                                           "hidden": True, "start_date": 2},
            "event/the-thaw.json": {"id": i(51), "type": "event", "name": "The thaw", "start_date": 3},
            "character/ada.json": {"id": i(52), "type": "character", "name": "Ada", "location": i(51)},
            "map/chart.json": {"id": i(53), "type": "map", "name": "Chart", "width": 100, "height": 100},
            f"widget/{OUTSIDE}.json": {"id": i(54), "type": "widget", "name": "Odd gadget"}}
    if unread:
        rows[f"construct/{TWIN}.json"] = {"id": HUSH, "type": "construct", "name": "Twin"}
    for rel, body in rows.items():
        p = root / "elements" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body), encoding="utf-8")
    if unread:
        for n in range(1, 7):
            (root / "elements" / "event" / f"{MARK}-{n}.json").write_text("{ not json", encoding="utf-8")
    (root / "world.json").write_text(json.dumps({"id": WORLD, "name": "Unread"}), encoding="utf-8")


def draw_unread(unread=True):
    """(stdout, the page's bytes, graph.json's bytes) for plant_unread's folder."""
    with tempfile.TemporaryDirectory() as tmp:
        world, out = Path(tmp) / "world", Path(tmp) / "draw"
        plant_unread(world, unread)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(GRAPH), str(world), "--offline", "--out", str(out)],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        assert r.returncode == 0, f"graph.py exit {r.returncode}: {r.stderr or r.stdout}"
        return r.stdout, (out / "graph.html").read_bytes(), (out / "graph.json").read_bytes()


def test_the_page_counts_the_files_not_read_and_names_none():
    text, page, data = draw_unread()
    for name, b in (("graph.html", page), ("graph.json", data)):
        low = b.decode("utf-8").casefold()
        found = [w for w in (TWIN, MARK, OUTSIDE, "hidden-one", HUSH, HUSH_NAME) if w.casefold() in low]
        assert not found, (name, found)
    assert b"7 files not read." in page, page.decode("utf-8")[-1500:]
    missing = [rel for rel in UNREAD if rel not in text]
    assert not missing and "7 files not read" in text, (missing, text)
    print(f"the page holds the count and no name; the terminal names all {len(UNREAD)}")


def test_a_folder_that_reads_whole_draws_the_same_page():
    """No line about files not read when every file reads; a file that does not read changes the
    page by that one line and nothing else (the time of the read taken out)."""
    stamp = re.compile(rb"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")
    _, clean, clean_data = draw_unread(unread=False)
    assert b"not read" not in clean, clean
    with tempfile.TemporaryDirectory() as tmp:
        world, out = Path(tmp) / "world", Path(tmp) / "draw"
        plant_unread(world, unread=False)
        (world / "elements" / "event" / "broken.json").write_text("{", encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(GRAPH), str(world), "--offline", "--out", str(out)],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        assert r.returncode == 0, r.stderr
        one, one_data = (out / "graph.html").read_bytes(), (out / "graph.json").read_bytes()
    assert one_data == clean_data
    a, b = stamp.sub(b"T", clean), stamp.sub(b"T", one)
    assert b == a.replace(b'<div id="ms">', b"<div>1 file not read. " + UNREAD_WORDS + b'</div><div id="ms">'), b


# The page's fixed sentence after the count, the same in the three scripts.
UNREAD_WORDS = b"The list, with why each did not read, is in the terminal of whoever drew this page."


# What a page leaves out besides the files not read: an element the World's hidden list names, an
# id two files hold when either copy is left out, an element of a type outside the 22, and the
# folder of the file given to --presentation.
LISTED, COPIED, GADGET, ADA2 = i(61), i(62), i(63), i(64)
TYPES_22 = ("ability", "character", "collective", "construct", "creature", "event", "family",
            "institution", "language", "law", "location", "map", "marker", "narrative", "object",
            "phenomenon", "pin", "relation", "species", "title", "trait", "zone")


def draw_rows(rows, world_keys=None, *args):
    """(exit, stdout and stderr, the page's text, graph.json's text) for a folder of `rows`
    ({path under elements/: body}), world.json carrying `world_keys`."""
    with tempfile.TemporaryDirectory() as tmp:
        world, out = Path(tmp) / "world", Path(tmp) / "draw"
        for rel, body in rows.items():
            p = world / "elements" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(body), encoding="utf-8")
        (world / "world.json").write_text(json.dumps({"id": WORLD, "name": "Amended", **(world_keys or {})}),
                                          encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(GRAPH), str(world), "--offline", "--out", str(out), *args],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        page = (out / "graph.html").read_text(encoding="utf-8") if (out / "graph.html").exists() else ""
        data = (out / "graph.json").read_text(encoding="utf-8") if (out / "graph.json").exists() else ""
    return r.returncode, r.stdout + r.stderr, page, data


def held(texts, *words):
    """The words any of the texts holds, in any letter case."""
    return sorted({w for t in texts for w in words if w.casefold() in t.casefold()})


def ada_to(*ids):
    return {"character/ada.json": {"id": ADA2, "type": "character", "name": "Ada", "friends": list(ids)}}


def test_the_worlds_hidden_list_leaves_out_what_it_names():
    rows = {"event/listed.json": {"id": LISTED, "type": "event", "name": "Listed quietly",
                                  "description": "Murmurword only here."}, **ada_to(LISTED)}
    code, text, page, data = draw_rows(rows, {"hidden": [LISTED]})
    assert code == 0, text
    assert not held([page, data], LISTED, "Listed quietly", "Murmurword"), held([page, data], LISTED, "Listed quietly")
    assert "Left out: 1 hidden." in text, text
    # The graph already honours the list through the package's reader: its picture is the reader's.
    body = {"elements": [dict(b, type=rel.split("/")[0]) for rel, b in rows.items()], "hidden": [LISTED]}
    assert [n["id"] for n in json.loads(data)["nodes"]] == [n["id"] for n in world_graph(body, {"rung": "owner"})["nodes"]]
    code, text, page, data = draw_rows(rows, {"hidden": [LISTED]}, "--hidden")
    assert code == 0 and held([page], "Listed quietly", "Murmurword") == ["Listed quietly", "Murmurword"], text
    assert LISTED in data, data


def test_an_id_two_files_hold_is_drawn_from_neither_when_one_is_left_out():
    for plain in ("aa-plain-copy", "zz-plain-copy"):
        rows = {f"character/{plain}.json": {"id": COPIED, "type": "character", "name": "Plain copy",
                                            "description": "Plainword here."},
                "character/hidden-copy.json": {"id": COPIED, "type": "character", "name": "Hushed copy",
                                               "hidden": True, "description": "Hushword here."},
                **ada_to(COPIED)}
        code, text, page, data = draw_rows(rows)
        assert code == 0, text
        found = held([page, data], COPIED, "Plain copy", "Hushed copy", "Plainword", "Hushword")
        assert not found, (plain, found)
        assert "Left out: 1 hidden." in text and "1 file not read." in page, (plain, text)
        a, b = sorted([f"character/{plain}.json", "character/hidden-copy.json"])
        # The terminal names both files, blames neither, and says which copy the run took.
        assert f"{a} and {b} both hold the id {COPIED}; this run took character/hidden-copy.json" in text, (plain, text)
        # With --hidden no copy is left out: the first by path is drawn, as before.
        code, text, page, data = draw_rows(rows, None, "--hidden")
        first = "Plain copy" if plain.startswith("aa") else "Hushed copy"
        assert held([data], "Plain copy", "Hushed copy") == [first], (plain, data)
        assert f"{a} and {b} both hold the id {COPIED}; this run took {a}" in text, (plain, text)
    rows = {"character/aa-first.json": {"id": COPIED, "type": "character", "name": "First copy"},
            "character/zz-second.json": {"id": COPIED, "type": "character", "name": "Second copy"}}
    code, text, page, data = draw_rows(rows)
    assert held([page, data], "First copy", "Second copy") == ["First copy"], data
    assert (f"character/aa-first.json and character/zz-second.json both hold the id {COPIED}; "
            "this run took character/aa-first.json") in text, text


def presentation_files(folder):
    """A file that is not JSON and one of the right shape, in `folder`."""
    folder.mkdir()
    (folder / "colours-bad.json").write_text("not json", encoding="utf-8")
    shape = {"types": {t: {"family": "blue"} for t in TYPES_22},
             "colors": {"order": ["blue", "green", "pink", "amber"],
                        "families": {f: {"light": "#123456", "dark": "#654321"}
                                     for f in ("blue", "green", "pink", "amber")}}}
    (folder / "colours-good.json").write_text(json.dumps(shape), encoding="utf-8")
    return folder / "colours-bad.json", folder / "colours-good.json"


def test_the_page_names_no_folder_of_the_presentation_file():
    with tempfile.TemporaryDirectory() as tmp:
        bad, good = presentation_files(Path(tmp) / "presfolder-q9z")
        # A file that did not read, or a folder given by mistake, is named on the page not at all.
        for f, words in ((bad, "neutral greys (the presentation file did not read)"),
                         (bad.parent, "neutral greys (the presentation file did not read)"),
                         (good, "presentation.json from colours-good.json")):
            code, text, page, _ = draw_rows(ada_to(), None, "--presentation", str(f))
            assert code == 0, text
            assert not held([page], "presfolder-q9z", "Expecting value", "colours-bad"), (f.name, page[-2000:])
            assert words in page, (f.name, page[-2000:])
            assert str(f) in text, text
            if f == bad:
                assert "Expecting value" in text, text


def test_a_type_outside_the_22_is_left_out_and_counted():
    rows = {"widget/odd-gadget-file.json": {"id": GADGET, "type": "widget", "name": "Odd gadget",
                                            "start_date": 4, "description": "Gadgetword here."},
            **ada_to(GADGET)}
    code, text, page, data = draw_rows(rows)
    assert code == 0, text
    assert not held([page, data], GADGET, "Odd gadget", "Gadgetword", "odd-gadget-file", "widget"), page
    # The terminal counts it and names it not: it is read, so it is no file not read.
    assert "Left out: 1 outside the 22 types." in text and "odd-gadget-file" not in text, text


def test_the_scripts_22_types_are_the_packages():
    import onlyworlds
    assert sorted(TYPES_22) == sorted(onlyworlds.ELEMENT_TYPES), onlyworlds.ELEMENT_TYPES
    src = GRAPH.read_text(encoding="utf-8")
    start = src.index("OFFLINE_FAMILY = {")
    listed = re.findall(r'"([a-z]+)": "(?:blue|green|pink|amber)"', src[start:src.index("}", start)])
    assert sorted(listed) == sorted(TYPES_22), listed


# The scripts' own copies of the package's left-out rules. graph.py's rules are imported by map.py,
# which runs on the standard library alone, so they stay copies; this table holds each equal to the
# package's own function.
ABSENT = object()
VALUES = [ABSENT, None, False, True, 0, 0.0, 1, "", "   ", "yes", [], {}, [0]]


def graph_module():
    spec = importlib.util.spec_from_file_location("graph_under_test", GRAPH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_left_out_rules_are_the_packages():
    from onlyworlds import hands_on_as_proposed, is_charter_element, is_hidden, is_room_element
    g = graph_module()
    differ = []
    for v in VALUES:
        def body(key, **keys):
            b = {"id": "x", "_type": keys["type"], **keys}
            if v is not ABSENT:
                b[key] = v
            return b
        h = body("hidden", type="character")
        p = body("x_review_proposed", type="character")
        r = body("x_room_of", type="character", supertype="Member")
        a = body("x_charter_of", type="law", supertype="Charter")
        for rule, mine, theirs in (("hidden", g.is_hidden(h), is_hidden(h)),
                                   ("proposed", g.own_reason(p) == "proposed", hands_on_as_proposed(p)),
                                   ("room", g.is_room(r), is_room_element(r)),
                                   ("reading aid", g.is_reading_aid(a), is_charter_element(a))):
            if mine != theirs:
                differ.append((rule, "absent" if v is ABSENT else v, mine, theirs))
    assert not differ, differ
    print(f"{len(VALUES)} values x 4 rules: the script's answers are the package's")


def test_a_proposed_mark_is_read_as_the_package_reads_it():
    """false, 0 and 0.0 are a doubt, counted with the proposed; a text of only spaces is no mark."""
    for v, out in ((False, True), (0, True), (0.0, True), ("   ", False)):
        rows = {"character/marked.json": {"id": LISTED, "type": "character", "name": "Marked Fenwick",
                                          "x_review_proposed": v, "description": "Fenword here."}, **ada_to(LISTED)}
        code, text, page, data = draw_rows(rows)
        assert code == 0, text
        assert bool(held([page, data], LISTED, "Marked Fenwick", "Fenword")) is not out, (v, text)
        assert ("Left out: 1 proposed." in text) is out, (v, text)
        # A plain copy of a proposed element, in both orders: neither copy is drawn.
        for plain in ("aa-plain", "zz-plain"):
            rows[f"character/{plain}.json"] = {"id": LISTED, "type": "character", "name": "Plain Aster"}
            code, text, page, data = draw_rows(rows)
            assert bool(held([page, data], LISTED, "Plain Aster", "Marked Fenwick")) is not out, (v, plain, text)
            del rows[f"character/{plain}.json"]


def test_an_id_that_is_not_text_is_a_file_not_read():
    rows = {"character/numbered.json": {"id": 987654321, "type": "character", "name": "Numbered Nook",
                                        "description": "Numword here."}, **ada_to()}
    code, text, page, data = draw_rows(rows, {"hidden": [987654321]})
    assert code == 0, text
    assert not held([page, data], "987654321", "Numbered Nook", "Numword"), page[-1500:]
    assert "outside the 22" not in text and "1 file not read." in page, text
    assert "character/numbered.json: its id is not text" in text, text


# Every left-out kind, each by every road the graph reads an element by: a link's target, a copy of
# its id in two other files (one sorting before it, one after), the World's hidden list.
LEAKS = {"hidtrue": {"hidden": True}, "hidyes": {"hidden": "yes"}, "hidone": {"hidden": 1},
         "hidobj": {"hidden": {"a": 1}}, "listed": {}, "propmark": {"x_review_proposed": {"by": "someone"}},
         "propfalse": {"x_review_proposed": False}, "propzero": {"x_review_proposed": 0},
         "propzerof": {"x_review_proposed": 0.0}}
FORCED = {"room": ("character", {"supertype": "Member", "x_room_of": WORLD}),
          "aid": ("law", {"supertype": "Charter", "x_charter_of": WORLD}),
          "outside": ("widget", {})}


def plant_every_kind():
    """(rows, world keys, every id, name, word and file stem a page may not hold)."""
    rows, secrets, listed = {}, set(), []
    kinds = [(k, "character", mark) for k, mark in LEAKS.items()] + [(k, t, m) for k, (t, m) in FORCED.items()]
    for n, (k, t, mark) in enumerate(kinds, start=70):
        eid = i(n)
        rows[f"{t}/m-{k}.json"] = {"id": eid, "type": t, "name": f"Leak{k}Q", "description": f"Desc{k}Q", **mark}
        secrets |= {eid, f"Leak{k}Q", f"Desc{k}Q", f"m-{k}"}
        if k == "listed":
            listed.append(eid)
        if k != "outside":  # a copy that is only outside the 22 keeps no id out (amendment 1)
            for side in ("a", "z"):
                rows[f"{t}/{side}-plain-{k}.json"] = {"id": eid, "type": t, "name": f"Plain{side}{k}Q"}
                secrets |= {f"Plain{side}{k}Q", f"{side}-plain-{k}"}
    rows["character/m-numid.json"] = {"id": 987654321, "type": "character", "name": "Leaknumid"}
    secrets |= {"987654321", "Leaknumid", "m-numid"}
    rows.update(ada_to(*sorted(s for s in secrets if s.startswith("00000000-"))))
    return rows, {"hidden": listed}, secrets


def test_no_left_out_kind_reaches_a_written_file_by_any_road():
    rows, world_keys, secrets = plant_every_kind()
    code, text, page, data = draw_rows(rows, world_keys)
    assert code == 0, text
    found = held([page, data], *secrets)
    assert not found, found
    assert [n["name"] for n in json.loads(data)["nodes"]] == ["Ada"], data
    print(f"{len(secrets)} ids, names, words and file stems: none in graph.html or graph.json")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except Exception as e:  # noqa: BLE001 (one red test never stops the run)
            failed += 1
            print(f"FAIL {t.__name__}: {e.__class__.__name__}: {str(e)[:300]}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
