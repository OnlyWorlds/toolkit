"""The five folder readers leave out an element file nested more than 200 levels deep, and say so.

The rule is the folder spec's "How deep an element file may nest": an element file in which an
object or array sits more than 200 levels deep (objects and arrays both counted, the file's top
object at 1) is not read; the reader leaves it out for the reason `too_deep` and names it where it
names the files it left out, and the world around it is read as it stands. The count is made in
the file's text before any parse (each reader carries schema-dist's own `_too_deep`), so every
value of a repeated key counts, a bracket inside a string is no level, and the verdict never rests
on Python's recursion limit. A world.json that deep is a world.json the reader cannot read: no
world, exit 2.

The readers: the read skill's count.py and consistency.py (one loader, consistency's), the draw
skill's graph.py, map.py and timeline.py (one loader, graph's copy of it). Each is run as a person
runs it, on a folder unpacked from the standard's own cases: the nine OW-25 archives of schema-dist
`fixtures/owworld/` (CASES below, each archive checked against its row in verdicts.json, and the
rows checked to be exactly these nine). Each archive holds the base world (Ana, Brother Tomas, The
Abbey) and, but for the world.json case, one more Character file, `elements/character/deep--
0000ab0e.json`:

- pass-OW-25-depth-200-read: nested to 200 by arrays and objects in turn, read.
- pass-OW-25-depth-201-left-out: the same one level deeper, left out.
- pass-OW-25-dup-key-deep-first-left-out, pass-OW-25-dup-key-deep-last-left-out: the 201 value and
  a plain 1 under one key, in both orders: left out (a parse keeps one of the two).
- pass-OW-25-brackets-in-string-read: 200 brackets inside a string, nothing nested: read.
- pass-OW-25-escaped-backslash-then-deep-left-out: a string ending in an escaped backslash, then
  the 201 value: left out.
- pass-OW-25-empty-array-at-201-left-out, pass-OW-25-empty-object-at-201-left-out: an empty array
  or object at 201: left out.
- fail-OW-25-world-json-too-deep: world.json nested to 201: refused, exit 2, world.json named.

A case that leaves the file out: exit 0, the file named with `too_deep` in the reader's own list of
what it did not read (count: "Not counted" and the JSON's notes; consistency: "not checked" and
not_checked; the draw scripts: the terminal's list of files not read), and the base's three
elements read, not four. A case that reads it: four, and no too_deep line.

- test_<reader>_follows_the_nine_cases, one per reader.
- test_a_link_to_a_file_left_out_is_a_link_to_no_element: Ana's friends names The Deep; at 201
  consistency reports a link to no element in the folder, count counts no link and graph draws no
  edge; at 200 none of that.
- test_a_raised_recursion_limit_changes_no_verdict: the five readers on 200 and 201 under
  sys.setrecursionlimit(100000): the same verdicts, so neither comes from the limit.
- test_a_file_100000_deep_is_left_out: a file this test makes, 100,000 levels, by the archives'
  shape (checked level for level against the 200 and 201 archives first): each reader leaves it
  out and runs on (a parse of it overflows).

OW_DEPTH_FIXTURES names another fixtures/owworld folder; else schema-dist's beside the toolkit's
main checkout (from a worktree too), which must not sit behind its fetched origin/main.
OW_TK_SKILLS names another skills/ folder (an older one, to show this test is red on it).

Runs under pytest, or alone:
    python testing/test_too_deep.py

Python 3.12+ and the onlyworlds package (>=0.101.0), for graph.py and timeline.py.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILLS = Path(os.environ.get("OW_TK_SKILLS") or ROOT / "skills")
SCRIPTS = {
    "count": SKILLS / "onlyworlds-read" / "scripts" / "count.py",
    "consistency": SKILLS / "onlyworlds-read" / "scripts" / "consistency.py",
    "graph": SKILLS / "onlyworlds-draw" / "scripts" / "graph.py",
    "map": SKILLS / "onlyworlds-draw" / "scripts" / "map.py",
    "timeline": SKILLS / "onlyworlds-draw" / "scripts" / "timeline.py",
}
DEEP = "elements/character/deep--0000ab0e.json"
DEEP_ID = "0695db83-0000-7000-8000-00000000ab0e"
ANA = "elements/character/ana--0000ab01.json"
TOP = "abbey"  # the archives' top folder
# file -> what the reader leaves out ("too_deep": the deep file; "world": refuses the world; None: reads all)
CASES = {
    "pass-OW-25-depth-200-read.owworld": None,
    "pass-OW-25-depth-201-left-out.owworld": "too_deep",
    "pass-OW-25-dup-key-deep-first-left-out.owworld": "too_deep",
    "pass-OW-25-dup-key-deep-last-left-out.owworld": "too_deep",
    "pass-OW-25-brackets-in-string-read.owworld": None,
    "pass-OW-25-escaped-backslash-then-deep-left-out.owworld": "too_deep",
    "pass-OW-25-empty-array-at-201-left-out.owworld": "too_deep",
    "pass-OW-25-empty-object-at-201-left-out.owworld": "too_deep",
    "fail-OW-25-world-json-too-deep.owworld": "world",
}
RAISE_LIMIT = ("import runpy, sys; sys.setrecursionlimit(100000); script = sys.argv[1]; "
               "sys.argv = sys.argv[1:]; runpy.run_path(script, run_name='__main__')")


def fixtures_dir():
    """The OW-25 archives' folder: OW_DEPTH_FIXTURES, else schema-dist's beside the toolkit's main
    checkout. Loud when there is none, and when that checkout sits behind its fetched origin/main."""
    if os.environ.get("OW_DEPTH_FIXTURES"):
        path = Path(os.environ["OW_DEPTH_FIXTURES"])
        assert (path / "verdicts.json").exists(), f"OW_DEPTH_FIXTURES names no fixtures folder: {path}"
        return path
    roots = [ROOT]
    common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            check=False, capture_output=True, text=True).stdout.strip()
    if common:
        roots.insert(0, Path(common).parent)
    path = next((p for p in (r.parent / "schema-dist" / "fixtures" / "owworld" for r in roots)
                 if (p / "verdicts.json").exists()), None)
    assert path is not None, (f"no schema-dist checkout beside {ROOT.parent}: clone it there, "
                              "or set OW_DEPTH_FIXTURES to its fixtures/owworld folder")
    repo = path.parent.parent
    behind = subprocess.run(["git", "-C", str(repo), "rev-list", "--count", "HEAD..origin/main"],
                            check=False, capture_output=True, text=True).stdout.strip()
    assert behind in ("", "0"), f"schema-dist is {behind} commits behind its fetched origin/main: git -C {repo} pull"
    return path


def checked_cases():
    """{file: its archive's path}: the verdicts' OW-25 rows are exactly CASES, with the left-out
    file and the refusal CASES says, and each archive is its row's bytes."""
    where = fixtures_dir()
    rows = {r["file"]: r for r in json.loads((where / "verdicts.json").read_text(encoding="utf-8"))["fixtures"]
            if r.get("test") == "OW-25"}
    assert sorted(rows) == sorted(CASES), sorted(set(rows) ^ set(CASES))
    for name, kind in CASES.items():
        row = rows[name]
        if kind == "world":
            assert (row["reader"], row.get("reason")) == ("refuse", "not_a_world"), row
        else:
            assert row["reader"] == "accept" and row["left_out"] == {"too_deep": [DEEP] if kind else []}, row
        data = (where / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"], f"{name} is not its row's bytes"
    return {name: where / name for name in CASES}


def unpack(archive, into):
    with zipfile.ZipFile(archive) as z:
        z.extractall(into)
    return Path(into) / TOP


def run(reader, world, out, limit=False):
    """(exit code, stdout, stderr, the elements the reader read, the links it read or None)."""
    script = SCRIPTS[reader]
    args = {"count": ["--json"], "consistency": ["--json"]}.get(reader, ["--offline", "--out", str(out)])
    head = [sys.executable, "-c", RAISE_LIMIT] if limit else [sys.executable]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(head + [str(script), str(world), *args], capture_output=True, text=True,
                       encoding="utf-8", env=env)
    read = links = None
    if r.returncode == 0:
        if reader == "count":
            data = json.loads(r.stdout)
            read, links = data["total"], data["links"]
        elif reader == "consistency":
            data = json.loads(r.stdout)
            read, links = data["elements"], data
        elif reader == "graph":
            data = json.loads((Path(out) / "graph.json").read_text(encoding="utf-8"))
            read, links = len(data["nodes"]), len(data["edges"])
        elif reader == "timeline":
            m = re.search(r"Not placed: (\d+) with no date", r.stdout)
            read = int(m.group(1)) if m else None
    return r.returncode, r.stdout, r.stderr, read, links


def said_left_out(reader, stdout, file=DEEP):
    """Whether the reader names `file` with too_deep in its own list of what it did not read."""
    line = f"{file}: not read, too_deep"
    if reader == "count":
        return any(n.startswith(line) for n in json.loads(stdout)["notes"])
    if reader == "consistency":
        return any(n.startswith(line) for n in json.loads(stdout)["not_checked"])
    return f"  - {line}" in stdout


def verdict(reader, world, out, kind, limit=False):
    """What is wrong with the reader's run on a case of this kind, or None."""
    code, stdout, stderr, read, _ = run(reader, world, out, limit)
    if kind == "world":
        if code != 2 or "world.json" not in stderr or "too_deep" not in stderr:
            return f"exit {code}, want 2 naming world.json and too_deep: {(stderr or stdout)[-300:]}"
        return None
    if code != 0:
        return f"exit {code}: {(stderr or stdout)[-300:]}"
    said = said_left_out(reader, stdout)
    if kind == "too_deep" and not said:
        return "the deep file is not named with too_deep"
    if kind is None and "too_deep" in stdout:
        return "a too_deep line on a file that is read"
    want = 3 if kind else 4
    if reader != "map" and read != want:
        return f"read {read} elements, want {want}"
    return None


def follows_the_nine_cases(reader):
    failed = []
    for name, archive in checked_cases().items():
        with tempfile.TemporaryDirectory() as tmp:
            world = unpack(archive, Path(tmp) / "w")
            why = verdict(reader, world, Path(tmp) / "draw", CASES[name])
        if why:
            failed.append(f"{name}: {why}")
    assert not failed, f"{reader}.py on the OW-25 cases:\n" + "\n".join(failed)
    print(f"{reader}.py follows all {len(CASES)} OW-25 cases")


def test_count_follows_the_nine_cases():
    follows_the_nine_cases("count")


def test_consistency_follows_the_nine_cases():
    follows_the_nine_cases("consistency")


def test_graph_follows_the_nine_cases():
    follows_the_nine_cases("graph")


def test_map_follows_the_nine_cases():
    follows_the_nine_cases("map")


def test_timeline_follows_the_nine_cases():
    follows_the_nine_cases("timeline")


def test_a_link_to_a_file_left_out_is_a_link_to_no_element():
    cases = checked_cases()
    failed = []
    for name, left in (("pass-OW-25-depth-200-read.owworld", False), ("pass-OW-25-depth-201-left-out.owworld", True)):
        with tempfile.TemporaryDirectory() as tmp:
            world = unpack(cases[name], Path(tmp) / "w")
            ana = world / ANA
            body = json.loads(ana.read_text(encoding="utf-8"))
            body["friends"] = [DEEP_ID]
            ana.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8", newline="\n")
            _, _, _, _, report = run("consistency", world, None)
            dangling = [f for f in report["findings"]["links"]
                        if f["field"] == "friends" and f["value"] == DEEP_ID and f["other"] is None]
            _, _, _, _, counted = run("count", world, None)
            _, _, _, _, edges = run("graph", world, Path(tmp) / "draw")
        got = (len(dangling), counted, edges)
        want = (1, 0, 0) if left else (0, 1, 1)
        if got != want:
            failed.append(f"{name}: (findings of a link to no element, links counted, edges drawn) {got}, want {want}")
    assert not failed, "\n".join(failed)
    print("a link to the file left out is a link to no element in consistency, count and graph")


def test_a_raised_recursion_limit_changes_no_verdict():
    cases = checked_cases()
    failed = []
    for name in ("pass-OW-25-depth-200-read.owworld", "pass-OW-25-depth-201-left-out.owworld"):
        for reader in SCRIPTS:
            with tempfile.TemporaryDirectory() as tmp:
                world = unpack(cases[name], Path(tmp) / "w")
                why = verdict(reader, world, Path(tmp) / "draw", CASES[name], limit=True)
            if why:
                failed.append(f"{reader}.py, {name}, recursion limit 100000: {why}")
    assert not failed, "\n".join(failed)
    print(f"the {len(SCRIPTS)} readers give the same verdicts at a recursion limit of 100000")


def nested_text(depth):
    """An element file whose x_depth nests an array and an object in turn so that its deepest one
    sits at `depth`, the element's own object at 1: the archives' shape, as text."""
    opens = "".join("[" if level % 2 == 0 else '{"a": ' for level in range(2, depth + 1))
    closes = "".join("]" if level % 2 == 0 else "}" for level in range(depth, 1, -1))
    return f'{{"id": "{DEEP_ID}", "name": "The Abyss", "x_depth": {opens}1{closes}}}\n'


def test_a_file_100000_deep_is_left_out():
    cases = checked_cases()
    for name, depth in (("pass-OW-25-depth-200-read.owworld", 200), ("pass-OW-25-depth-201-left-out.owworld", 201)):
        with zipfile.ZipFile(cases[name]) as z:  # the made shape is the archives' own, level for level
            served = json.loads(z.read(f"{TOP}/{DEEP}").decode("utf-8"))["x_depth"]
        assert json.loads(nested_text(depth))["x_depth"] == served, f"nested_text({depth}) is not {name}'s shape"
    failed = []
    for reader in SCRIPTS:
        with tempfile.TemporaryDirectory() as tmp:
            world = unpack(cases["pass-OW-25-depth-200-read.owworld"], Path(tmp) / "w")
            (world / DEEP).write_text(nested_text(100_000), encoding="utf-8", newline="\n")
            why = verdict(reader, world, Path(tmp) / "draw", "too_deep")
        if why:
            failed.append(f"{reader}.py: {why}")
    assert not failed, "\n".join(failed)
    print(f"the {len(SCRIPTS)} readers leave a file 100,000 deep out and run on")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
    print(f"{len(tests)} tests passed")
