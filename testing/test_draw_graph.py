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

OW_DRAW_GRAPH points at another copy of graph.py (an older one, to show this test is red on it).

Runs under pytest, or alone:
    python testing/test_draw_graph.py

Python 3.12+ and the onlyworlds package (>=0.101.0).
"""
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


def test_a_repeated_target_is_two_edges():
    graph, _, _ = draw()
    assert triples(graph).count((ADA, BRAM, "friends")) == 2, triples(graph)


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
