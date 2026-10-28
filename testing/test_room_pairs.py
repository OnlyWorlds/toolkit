"""The two readers that leave the room and the reading aids out of a lore view agree with the
room and charter profiles.

The draw skill's graph.py and the read skill's count.py each hold the room profile's pairs
(schema-dist `profiles/room.md`) and the charter profile's three (`profiles/charter.md`): a skill
installs alone, so the two cannot share one module. This test keeps the two copies one table:

1. the two tables are equal, and hold the profile's nine pairs (relation + Take among them);
2. a planted Take (a Relation with supertype Take and the mark x_room_of) is left out of the
   graph and out of the count, and a Take without the mark stays in both as lore;
3. when the schema-dist checkout sits beside this repository's main checkout, every case of
   the profile's conformance fixture (`profiles/room.fixture.json`) reads the same through
   both readers, and the fixture's pairs equal the tables (OW_ROOM_FIXTURE points at another
   copy; without one the check says it was skipped);
4. the two CHARTER_PAIRS tables are equal and hold the charter profile's three pairs;
5. a planted Charter, Guide and Domain, each with the mark x_charter_of, are left out of the
   graph and the count, run as scripts, and said once in each; a Law with supertype Charter
   without the mark, and a Guide whose mark is only whitespace, stay in both as lore; a mark on
   a Character is named as malformed;
6. both scripts read a mark by presence (the profiles' rule): null, an empty string and a string
   of whitespace are absent; a string with something left, a number and an object are present;
7. the charter profile's fixture (`profiles/charter.fixture.json`, OW_CHARTER_FIXTURE points at
   another copy) gives the same pairs, and its element cases read the same through both readers.

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


def default_fixture(name="room.fixture.json"):
    """schema-dist's fixture beside the toolkit's MAIN checkout, from a worktree too."""
    roots = [ROOT]
    try:
        common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute",
                                 "--git-common-dir"], capture_output=True, text=True).stdout.strip()
        if common:
            roots.insert(0, Path(common).parent)
    except OSError:
        pass
    found = [r.parent / "schema-dist" / "profiles" / name for r in roots]
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


THREE = {("law", "charter"), ("construct", "guide"), ("construct", "domain")}
SCRIPTS = {"graph.py": ROOT / "skills" / "onlyworlds-draw" / "scripts" / "graph.py",
           "count.py": ROOT / "skills" / "onlyworlds-read" / "scripts" / "count.py"}


def plant_aids(folder):
    """Two people; a marked Charter, Guide and Domain (the Domain's supertype padded and lower
    case, its mark a number); a Charter Law without the mark; a Guide whose mark is whitespace;
    a Character carrying x_charter_of."""
    def i(n):
        return f"00000000-0000-7000-8000-0000000001{n:02d}"
    rows = {
        "character/ada--01.json": {"id": i(1), "name": "Ada", "type": "character"},
        "character/bram--02.json": {"id": i(2), "name": "Bram", "type": "character",
                                    "friends": [i(1)]},
        "law/house-rules--03.json": {"id": i(3), "name": "House rules", "type": "law",
                                     "supertype": "Charter", "x_charter_of": WORLD},
        "construct/start-here--04.json": {"id": i(4), "name": "Start here", "type": "construct",
                                          "supertype": "Guide", "x_charter_of": WORLD,
                                          "constructs": [i(5)]},
        "construct/the-harbour--05.json": {"id": i(5), "name": "The harbour", "type": "construct",
                                           "supertype": " domain ", "x_charter_of": 7,
                                           "characters": [i(1), i(2)]},
        "law/the-old-charter--06.json": {"id": i(6), "name": "The old charter", "type": "law",
                                         "supertype": "Charter", "author": i(2)},
        "construct/spaced-guide--07.json": {"id": i(7), "name": "Spaced guide", "type": "construct",
                                            "supertype": "Guide", "x_charter_of": "  \u00a0"},
        "character/stray-mark--08.json": {"id": i(8), "name": "Stray mark", "type": "character",
                                          "x_charter_of": WORLD},
    }
    (folder / "world.json").write_text(json.dumps({"id": WORLD, "name": "Planted aids"}), encoding="utf-8")
    for rel, body in rows.items():
        p = folder / "elements" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body, indent=2), encoding="utf-8")


def run(script, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, str(SCRIPTS[script]), *args], capture_output=True,
                       text=True, encoding="utf-8", env=env)
    assert r.returncode == 0, f"{script} exit {r.returncode}: {r.stderr or r.stdout}"
    return r.stdout


def test_the_two_charter_tables_are_one():
    assert graph.CHARTER_PAIRS == counter.CHARTER_PAIRS, graph.CHARTER_PAIRS ^ counter.CHARTER_PAIRS
    assert graph.CHARTER_PAIRS == THREE, THREE ^ graph.CHARTER_PAIRS
    print(f"charter pairs: graph.py {len(graph.CHARTER_PAIRS)}, count.py {len(counter.CHARTER_PAIRS)}")


def test_planted_aids_are_left_out_and_said_once():
    lore = ["Ada", "Bram", "Spaced guide", "Stray mark", "The old charter"]
    with tempfile.TemporaryDirectory() as tmp:
        world = Path(tmp) / "world"
        world.mkdir()
        plant_aids(world)
        out = Path(tmp) / "draw"
        drawn_text = run("graph.py", str(world), "--offline", "--out", str(out))
        drawn = sorted(n["name"] for n in json.loads((out / "graph.json").read_text(encoding="utf-8"))["nodes"])
        r = json.loads(run("count.py", str(world), "--json"))
        md = run("count.py", str(world))
    counted = sorted(x["name"] for x in r["most_linked"])
    print(f"graph: drew {len(drawn)} of 8 ({', '.join(drawn)}); count: counted {r['elements']} of "
          f"{r['total']}, reading aids {r['left_out'].get('reading aids')} left out")
    assert drawn == lore, drawn
    assert drawn_text.count("The three reading aids are not drawn (3 elements).") == 1, drawn_text
    assert counted == lore and r["elements"] == 5, (counted, r["elements"])
    assert r["left_out"]["reading aids"] == 3, r["left_out"]
    assert r["reading_aids"] == "the three reading aids are not counted or listed", r["reading_aids"]
    assert md.count("The three reading aids are not counted or listed (3 elements).") == 1, md
    stray = [n for n in r["notes"] if "x_charter_of" in n]
    assert len(stray) == 1 and "stray-mark" in stray[0], r["notes"]
    bram = next(x for x in r["most_linked"] if x["name"] == "Bram")
    assert bram["degree"] == 2, bram  # friends Ada, and the old charter's author; never the Domain


def test_both_readers_read_a_mark_by_presence():
    cases = [(None, False), ("", False), ("  \u00a0", False), ("\t\u3000", False),
             ("x", True), (0, True), ({}, True), ("  x  ", True)]
    wrong = []
    for name, mod in (("graph.py", graph), ("count.py", counter)):
        for value, want in cases:
            room = {"type": "narrative", "_type": "narrative", "supertype": "Message"}
            aid = {"type": "construct", "_type": "construct", "supertype": "Domain"}
            if value is not None:
                room["x_room_of"] = aid["x_charter_of"] = value
            got = (mod.mark_present(value), mod.is_room(room), mod.is_reading_aid(aid))
            if got != (want, want, want):
                wrong.append(f"{name} {value!r}: {got}, the profiles say {want}")
    print(f"presence: {len(cases)} values through both readers' mark_present, is_room and "
          f"is_reading_aid, {len(wrong)} disagree")
    assert not wrong, wrong


def test_the_charter_fixture_reads_the_same():
    env = os.environ.get("OW_CHARTER_FIXTURE")
    path = Path(env) if env else default_fixture("charter.fixture.json")
    if not path or not path.exists():
        print("charter fixture: not found beside this checkout; skipped (OW_CHARTER_FIXTURE points at one)")
        return
    fx = json.loads(path.read_text(encoding="utf-8"))
    pairs = {(p["type"].casefold(), p["supertype"].casefold()) for p in fx["pairs"]}
    assert pairs == graph.CHARTER_PAIRS, pairs ^ graph.CHARTER_PAIRS
    assert fx["mark"]["field"] == "x_charter_of", fx["mark"]
    cases = [c for c in fx["cases"] if c.get("kind") == "element"]
    wrong = []
    for case in cases:
        e = dict(case["element"], _type=str(case["element"].get("type") or "").lower())
        for name, reader in (("graph.py", graph.is_reading_aid), ("count.py", counter.is_reading_aid)):
            if reader(e) is not case["is_charter_element"]:
                wrong.append(f"{name} {case['name']}: {reader(e)}, the fixture says {case['is_charter_element']}")
    print(f"charter fixture: {len(cases)} element cases through both readers, {len(wrong)} disagree ({path})")
    assert cases and not wrong, wrong


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except Exception as e:  # noqa: BLE001 (a reader without the function fails, never stops the run)
            failed += 1
            print(f"FAIL {t.__name__}: {e.__class__.__name__}: {e}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
