"""The draw skill's timeline.py: which calendar speaks (schema-dist profiles/calendar.md, "Which
calendar speaks", serial 147).

Each test plants a small world folder in a temporary directory, runs timeline.py on it
(--offline), and reads the calendar the page speaks (the page data's `calendar`, the speaking
element's name) and the printed summary:

- test_the_persons_pick_speaks_over_the_worlds: the World names one calendar, --calendar the
  other: the person's pick speaks, and the summary names the World's own;
- test_the_world_names_its_calendar: the World's x_calendar names the second of two calendars
  (by name order): that one speaks;
- test_several_calendars_and_none_named_none_speaks: two calendars, nothing named: none speaks,
  and the summary names both calendars and both ways to pick (--calendar, x_calendar);
- test_the_world_names_no_calendar_of_this_world: the World names an id no element has: none
  speaks, though the world holds one calendar, and one line names the key and its value; with
  --calendar the person's pick still speaks, and the line is still said;
- test_the_published_world_names_cases: the twelve world-names cases of the profile's fixture
  (`profiles/calendar.fixture.json`), each planted as a folder: the calendar that speaks is the
  case's `speaks`, the only calendar speaking when none is named among them (OW_CALENDAR_FIXTURE
  points at another copy; else schema-dist's beside the toolkit's main checkout, which must not
  sit behind its fetched origin/main);
- test_a_package_without_speaking_calendar_stops: an onlyworlds package with no
  speaking_calendar stops the script with exit 2 and a line naming the version that has it;
- test_a_calendar_on_a_left_out_element_the_world_names_speaks: the World names a calendar on
  a hidden element: it speaks (the pick is over every element read), the page calls it "the
  world's calendar" and carries neither its name nor its id, and the terminal names it;
- test_a_second_calendar_on_a_left_out_element_and_none_named: one calendar drawn, a second on
  a hidden element, nothing named: none speaks; the page carries neither the hidden one's name
  nor its id; the terminal's line names both.

Every test but the package one fails in plain words, never skips, when the interpreter running
it has an onlyworlds package without speaking_calendar.

OW_DRAW_TIMELINE points at another copy of timeline.py (an older one, to show this test is red
on it); graph.py and simple_fold.py must sit beside it.

Runs under pytest, or alone:
    python testing/test_draw_timeline.py

Python 3; the onlyworlds package (0.153.0 or newer) for the script it runs.
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
TIMELINE = Path(os.environ.get("OW_DRAW_TIMELINE")
                or ROOT / "skills" / "onlyworlds-draw" / "scripts" / "timeline.py")

CAL = {"version": 1, "grain": "day", "bundles": {"months": {"names": ["Frost", "Thaw"], "lengths": [10, 10]}}}
ALPHA = "019a3b10-0000-7000-8000-0000000d0a01"
ZETA = "019a3b10-0000-7000-8000-0000000d0a02"
EVENT = "019a3b10-0000-7000-8000-0000000d0a03"


def calendar(cid, name):
    return {"id": cid, "type": "construct", "supertype": "calendar", "name": name, "atlas_calendar": CAL}


def plant(root, world, elements):
    """A world folder: world.json (when world is not None), each element in its type's folder, and
    one dated Event so the page has a date to speak."""
    rows = list(elements) + [{"id": EVENT, "type": "event", "name": "The thaw", "start_date": 12}]
    for n, e in enumerate(rows):
        p = root / "elements" / str(e.get("type") or "construct").lower() / f"e{n:02d}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(e), encoding="utf-8")
    if world is not None:
        (root / "world.json").write_text(json.dumps(world), encoding="utf-8")


def need_package():
    """Fail in plain words, never skip, when this interpreter's onlyworlds cannot run the script."""
    try:
        from onlyworlds.calendar import speaking_calendar  # noqa: F401
    except ImportError as e:
        raise AssertionError(f"the onlyworlds package of {sys.executable} has no speaking_calendar ({e}): "
                             'the timeline needs pip install "onlyworlds>=0.153.0"') from None


def draw(world, elements, *args, env_extra=None):
    """(exit code, the page's calendar name or None when no page, stdout + stderr, the page's text)."""
    if env_extra is None:
        need_package()
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        plant(root, world, elements)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", **(env_extra or {}))
        r = subprocess.run([sys.executable, str(TIMELINE), str(root), "--out", str(out), "--offline", *args],
                           check=False, capture_output=True, text=True, encoding="utf-8", env=env)
        page = out / "timeline.html"
        if r.returncode or not page.exists():
            return r.returncode, None, r.stdout + r.stderr, ""
        text = page.read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', text, re.DOTALL).group(1))
    return r.returncode, data["tl"]["calendar"], r.stdout + r.stderr, text


def world(**keys):
    return {"id": "019a3b10-0000-7000-8000-0000000d0a00", "name": "Two seasons", **keys}


TWO = [calendar(ALPHA, "Alpha reckoning"), calendar(ZETA, "Zeta reckoning")]


def test_the_persons_pick_speaks_over_the_worlds():
    code, spoken, out, _ = draw(world(x_calendar=ZETA), TWO, "--calendar", "Alpha reckoning")
    assert code == 0, out
    assert spoken == "Alpha reckoning", (spoken, out)
    lines = [ln for ln in out.splitlines() if "as --calendar asks" in ln]
    assert len(lines) == 1 and "Zeta reckoning" in lines[0], out


def test_the_world_names_its_calendar():
    code, spoken, out, _ = draw(world(x_calendar=ZETA), TWO)
    assert code == 0, out
    assert spoken == "Zeta reckoning", (spoken, out)


def test_several_calendars_and_none_named_none_speaks():
    code, spoken, out, _ = draw(world(), TWO)
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert "Dates are the world's plain integers (no calendar reads)." in out, out
    lines = [ln for ln in out.splitlines() if "none speaks" in ln]
    assert len(lines) == 1, out
    for word in ("Alpha reckoning", "Zeta reckoning", "--calendar NAME", "x_calendar"):
        assert word in lines[0], (word, lines[0])


def test_the_world_names_no_calendar_of_this_world():
    dangling = "019a3b10-0000-7000-8000-0000000d0a09"
    code, spoken, out, _ = draw(world(x_calendar=dangling), TWO[:1])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    lines = [ln for ln in out.splitlines() if "names no calendar of this world" in ln]
    assert len(lines) == 1, out
    assert f'x_calendar is "{dangling}"' in lines[0] and "the dates stay numbers" in lines[0], lines[0]
    code, spoken, out, _ = draw(world(x_calendar=dangling), TWO[:1], "--calendar", "Alpha reckoning")
    assert code == 0, out
    assert spoken == "Alpha reckoning", (spoken, out)
    lines = [ln for ln in out.splitlines() if "names no calendar of this world" in ln]
    assert len(lines) == 1 and f'"{dangling}"' in lines[0], out


def fixture_path():
    """The calendar fixture: the file OW_CALENDAR_FIXTURE names, else schema-dist's beside the
    toolkit's main checkout (from a worktree too). Loud when there is none, and loud when that
    checkout sits behind its own fetched origin/main."""
    if os.environ.get("OW_CALENDAR_FIXTURE"):
        path = Path(os.environ["OW_CALENDAR_FIXTURE"])
        assert path.exists(), f"OW_CALENDAR_FIXTURE names a file that is not there: {path}"
        return path
    roots = [ROOT]
    common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            check=False, capture_output=True, text=True).stdout.strip()
    if common:
        roots.insert(0, Path(common).parent)
    path = next((p for p in (r.parent / "schema-dist" / "profiles" / "calendar.fixture.json" for r in roots)
                 if p.exists()), None)
    assert path is not None, (f"no schema-dist checkout beside {ROOT.parent}: clone it there, "
                              "or set OW_CALENDAR_FIXTURE to a calendar.fixture.json")
    repo = path.parent.parent
    behind = subprocess.run(["git", "-C", str(repo), "rev-list", "--count", "HEAD..origin/main"],
                            check=False, capture_output=True, text=True).stdout.strip()
    assert behind in ("", "0"), f"schema-dist is {behind} commits behind its fetched origin/main: git -C {repo} pull"
    return path


def test_the_published_world_names_cases():
    cases = [c for c in json.loads(fixture_path().read_text(encoding="utf-8"))["cases"]
             if c["name"].startswith("world-names-")]
    assert len(cases) == 12, [c["name"] for c in cases]
    wrong = []
    for c in cases:
        names = {e["id"]: e["name"] for e in c["elements"]}
        assert len(set(names.values())) == len(names), c["name"]
        code, spoken, _, _ = draw(c["world"], c["elements"])
        want = names[c["speaks"]] if c["speaks"] is not None else ""
        if code != 0 or spoken != want:
            wrong.append(f"{c['name']}: spoke {spoken!r}, the case says {want!r} (exit {code})")
    print(f"{len(cases) - len(wrong)} of {len(cases)} world-names cases agree")
    assert not wrong, "\n".join(wrong)


def test_a_package_without_speaking_calendar_stops():
    with tempfile.TemporaryDirectory() as d:
        pkg = Path(d) / "onlyworlds"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        (pkg / "calendar.py").write_text("def format_step(cfg, step):\n    return str(step)\n\n\n"
                                         "def read_calendar_value(raw):\n    return None\n", encoding="utf-8")
        code, _, out, _ = draw(world(), TWO[:1], env_extra={"PYTHONPATH": d})
    assert code == 2, (code, out)
    assert "onlyworlds>=0.153.0" in out, out


def no_trace_of(page, *words):
    """The words a page must not carry, in any letter case (the page's data is ASCII-escaped JSON,
    and these words are ASCII)."""
    low = page.casefold()
    return [w for w in words if w.casefold() in low]


def test_a_calendar_on_a_left_out_element_the_world_names_speaks():
    hidden_zeta = {**TWO[1], "hidden": True}
    code, spoken, out, page = draw(world(x_calendar=ZETA), [TWO[0], hidden_zeta])
    assert code == 0, out
    assert spoken == "the world's calendar", (spoken, out)
    assert "3 Thaw, 0" in page, "the event at step 12 is not labelled through the calendar"
    assert no_trace_of(page, "Zeta reckoning", ZETA) == [], no_trace_of(page, "Zeta reckoning", ZETA)
    assert "Dates read through the calendar Zeta reckoning" in out, out


def test_a_second_calendar_on_a_left_out_element_and_none_named():
    hidden_zeta = {**TWO[1], "hidden": True}
    code, spoken, out, page = draw(world(), [TWO[0], hidden_zeta])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert no_trace_of(page, "Zeta reckoning", ZETA) == [], no_trace_of(page, "Zeta reckoning", ZETA)
    lines = [ln for ln in out.splitlines() if "none speaks" in ln]
    assert len(lines) == 1 and "Alpha reckoning" in lines[0] and "Zeta reckoning" in lines[0], out


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
