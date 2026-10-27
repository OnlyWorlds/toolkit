"""The two readers that leave the room out of a lore view agree with the room profile.

The draw skill's graph.py and the read skill's count.py each hold the room profile's pairs
(schema-dist `profiles/room.md`): a skill installs alone, so the two cannot share one module.
This test keeps the two copies one table:

1. the two tables are equal, and hold the profile's nine pairs (relation + Take among them);
2. a planted Take (a Relation with supertype Take and the mark x_room_of) is left out of the
   graph and out of the count, and a Take without the mark stays in both as lore;
3. when the schema-dist checkout sits beside this repository's main checkout, every case of
   the profile's conformance fixture (`profiles/room.fixture.json`) reads the same through
   both readers, and the fixture's pairs equal the tables (OW_ROOM_FIXTURE points at another
   copy; without one the check says it was skipped).

Runs under pytest, or alone:
    python testing/test_room_pairs.py

Python 3, stdlib only.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "skills" / "onlyworlds-draw" / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "onlyworlds-read" / "scripts"))
import graph  # noqa: E402
import count as counter  # noqa: E402

NINE = {("narrative", "message"), ("narrative", "board"), ("relation", "work item"),
        ("construct", "spec"), ("relation", "heart"), ("relation", "take"),
        ("relation", "vote"), ("event", "sitting"), ("character", "member")}
WORLD = "0199c3a1-7b2e-7c3d-8e4f-000000000001"


def default_fixture():
    """schema-dist's room fixture beside the toolkit's MAIN checkout, from a worktree too."""
    roots = [ROOT]
    try:
        common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute",
                                 "--git-common-dir"], capture_output=True, text=True).stdout.strip()
        if common:
            roots.insert(0, Path(common).parent)
    except OSError:
        pass
    found = [r.parent / "schema-dist" / "profiles" / "room.fixture.json" for r in roots]
    return next((p for p in found if p.exists()), None)


def plant(folder):
    """A small world: two people, a work item, a Take on it with the mark, a Take without it."""
    rows = {
        "character/ada--00000001.json": {"id": "00000000-0000-7000-8000-000000000001",
                                         "name": "Ada", "type": "character"},
        "character/bram--00000002.json": {"id": "00000000-0000-7000-8000-000000000002",
                                          "name": "Bram", "type": "character"},
        "relation/the-bridge--00000003.json": {
            "id": "00000000-0000-7000-8000-000000000003", "name": "The bridge",
            "type": "relation", "supertype": "Work item", "x_room_of": WORLD,
            "actor": "00000000-0000-7000-8000-000000000002"},
        "relation/ada-takes-the-bridge--00000004.json": {
            "id": "00000000-0000-7000-8000-000000000004", "name": "Ada takes the bridge",
            "type": "relation", "supertype": "Take", "x_room_of": WORLD,
            "x_room_item": "00000000-0000-7000-8000-000000000003",
            "actor": "00000000-0000-7000-8000-000000000001"},
        "relation/the-old-take--00000005.json": {
            "id": "00000000-0000-7000-8000-000000000005", "name": "The old take",
            "type": "relation", "supertype": "Take",
            "actor": "00000000-0000-7000-8000-000000000002"},
    }
    (folder / "world.json").write_text(json.dumps({"id": WORLD, "name": "Planted"}), encoding="utf-8")
    for rel, body in rows.items():
        p = folder / "elements" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body, indent=2), encoding="utf-8")


def test_the_two_tables_are_one():
    assert graph.ROOM_PAIRS == counter.ROOM_PAIRS, graph.ROOM_PAIRS ^ counter.ROOM_PAIRS
    assert graph.ROOM_PAIRS == NINE, NINE - graph.ROOM_PAIRS
    print(f"pairs: graph.py {len(graph.ROOM_PAIRS)}, count.py {len(counter.ROOM_PAIRS)}")


def test_a_planted_take_is_room_not_lore():
    with tempfile.TemporaryDirectory() as tmp:
        world = Path(tmp) / "world"
        world.mkdir()
        plant(world)
        out = Path(tmp) / "draw"
        with contextlib.redirect_stdout(io.StringIO()):
            assert graph.main([str(world), "--offline", "--out", str(out)]) == 0
        drawn = sorted(n["name"] for n in json.loads((out / "graph.json").read_text(encoding="utf-8"))["nodes"])
        r = counter.count(world)
        counted = sorted(x["name"] for x in r["most_linked"])
    print(f"graph: drew {len(drawn)} of 5 ({', '.join(drawn)}); "
          f"count: counted {r['elements']} of {r['total']}, the room {r['left_out']['room']} left out")
    assert drawn == ["Ada", "Bram", "The old take"], drawn
    assert r["left_out"]["room"] == 2 and r["elements"] == 3, (r["left_out"], r["elements"])
    assert counted == ["Ada", "Bram", "The old take"], counted


def test_the_profile_fixture_reads_the_same():
    path = Path(os.environ["OW_ROOM_FIXTURE"]) if os.environ.get("OW_ROOM_FIXTURE") else default_fixture()
    if not path or not path.exists():
        print("room fixture: not found beside this checkout; skipped (OW_ROOM_FIXTURE points at one)")
        return
    fx = json.loads(path.read_text(encoding="utf-8"))
    pairs = {(p["type"].casefold(), p["supertype"].casefold()) for p in fx["pairs"]}
    assert pairs == graph.ROOM_PAIRS, pairs ^ graph.ROOM_PAIRS
    wrong = []
    for case in fx["cases"]:
        e = dict(case["element"], _type=str(case["element"].get("type") or "").lower())
        for name, reader in (("graph.py", graph.is_room), ("count.py", counter.is_room)):
            if reader(e) is not case["in_room"]:
                wrong.append(f"{name} {case['name']}: {reader(e)}, the fixture says {case['in_room']}")
    print(f"room fixture: {len(fx['cases'])} cases through both readers, {len(wrong)} disagree ({path})")
    assert not wrong, wrong


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
