"""The draw skill's timeline.py: which calendar speaks (schema-dist profiles/calendar.md, "Which
calendar speaks", serial 147), and what the page says of it.

Each test plants a small world folder in a temporary directory, runs timeline.py on it
(--offline), and reads the page's words for its calendar (the page data's `calendar`: "the
calendar <name>", "the calendar chosen for this page", or "" for plain numbers), the written
page's bytes, and the printed summary. Which calendar is the world's is read over every element;
a calendar labels the page only when its element is drawn, or when --calendar asks for it; the
page says which calendar its dates are read through, or that they are plain numbers, and nothing
else of calendars. The terminal is the person's own.

- test_the_persons_pick_speaks_over_the_worlds: the World names one calendar, --calendar the
  other: the person's pick speaks, and the terminal names the World's own;
- test_the_world_names_its_calendar: the World's x_calendar names the second of two calendars
  (by name order): that one speaks;
- test_several_calendars_and_none_named_none_speaks: two calendars, nothing named: none speaks;
  the terminal names both and both ways to pick (--calendar, the element's id exactly as written
  in x_calendar), and the page holds none of it;
- test_the_world_names_no_calendar_of_this_world: the World names an id no element has: none
  speaks, and the terminal names the key and its value; with --calendar the person's pick still
  speaks; the page holds the value in neither run;
- test_the_published_world_names_cases: the twelve world-names cases of the profile's fixture
  (`profiles/calendar.fixture.json`), each planted as a folder: the calendar that speaks is the
  case's `speaks` (OW_CALENDAR_FIXTURE points at another copy; else schema-dist's beside the
  toolkit's main checkout, which must not sit behind its fetched origin/main);
- test_a_package_without_speaking_calendar_stops: an onlyworlds package with no
  speaking_calendar stops the script with exit 2 and a line naming the version that has it;
- test_the_world_names_a_calendar_on_a_hidden_element: it is the world's, but the page shows
  plain numbers and carries none of its words, its name or its id; the terminal names it and
  both ways to have it (--calendar, --hidden);
- test_a_second_calendar_on_a_hidden_element_and_none_named: none speaks (several, none named);
  the page carries no trace of the hidden one and no list of calendars;
- test_one_calendar_on_a_hidden_element_and_none_named: the world's only calendar, hidden, no
  x_calendar: plain numbers on the page, the terminal names it and both ways;
- test_the_world_names_a_hidden_calendar_by_its_name: x_calendar holds a hidden element's name
  (no id, so no calendar is named): none speaks, and the page does not hold the name;
- test_left_out_calendars_leave_no_trace_on_the_page: a hidden, a room and a proposed calendar,
  alone or beside a drawn one; named by nothing, by its id, by its id in upper case, and by its
  name: the page's bytes hold none of its name, its id in any letter case, or any word of the
  calendar, and the page speaks no calendar;
- test_calendar_picks_a_left_out_calendar: --calendar names a hidden calendar: the page is
  labelled by it, says "the calendar chosen for this page", and holds neither name nor id;
- test_a_name_picks_the_drawn_calendar_first: a hidden and a drawn calendar of one name, the
  hidden one's id sorting first: --calendar NAME speaks the drawn one, and the page holds none of
  the hidden one's words or its id; --calendar with the hidden one's id still picks it;
- test_the_hint_gives_an_id_for_a_name_no_shell_reads_whole: a hidden calendar whose name holds
  quotes and a dollar sign: the terminal's hint gives --calendar with its id, never a Python
  repr; a plain name is given in double quotes.

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
SECRET = "019a3b10-0000-7000-8000-0000000d5ec1"
SECRET_NAME = "Secret reckoning"
# Every word of the secret calendar: none may reach a page that does not speak it.
SECRET_WORDS = ["Hushmonth", "Stillmonth", "Murmurday", "Lullday", "Quiet Reign", "QRX", "Whisperstep"]
SECRET_CAL = {"version": 1, "grain": "day", "step_name": "Whisperstep",
              "bundles": {"months": {"names": ["Hushmonth", "Stillmonth"], "lengths": [10, 10]},
                          "week": {"length": 2, "names": ["Murmurday", "Lullday"]}},
              "eras": [{"name": "Quiet Reign", "abbrev": "QRX", "start": 0}]}
# How an element is left out of a default run (graph.py's left_out_reason).
LEFT_OUT = {"hidden": {"hidden": True},
            "room": {"supertype": "Spec", "x_room_of": "019a3b10-0000-7000-8000-0000000d0a00"},
            "proposed": {"x_review_proposed": {"by": "019a3b10-0000-7000-8000-0000000d0a09"}}}


def calendar(cid, name):
    return {"id": cid, "type": "construct", "supertype": "calendar", "name": name, "atlas_calendar": CAL}


def secret(how="hidden"):
    return {"id": SECRET, "type": "construct", "supertype": "calendar", "name": SECRET_NAME,
            "atlas_calendar": SECRET_CAL, **LEFT_OUT[how]}


def called(name):
    return f"the calendar {name}"


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
    """(exit code, the page's words for its calendar or None when no page, stdout + stderr, the
    page's text)."""
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


def traces(page, *words):
    """The words a page holds, in any letter case (the page's data is ASCII-escaped JSON, and
    these words are ASCII)."""
    low = page.casefold()
    return [w for w in words if w.casefold() in low]


def no_secret(page):
    return traces(page, SECRET_NAME, SECRET, *SECRET_WORDS)


def world(**keys):
    return {"id": "019a3b10-0000-7000-8000-0000000d0a00", "name": "Two seasons", **keys}


TWO = [calendar(ALPHA, "Alpha reckoning"), calendar(ZETA, "Zeta reckoning")]


def test_the_persons_pick_speaks_over_the_worlds():
    code, spoken, out, page = draw(world(x_calendar=ZETA), TWO, "--calendar", "Alpha reckoning")
    assert code == 0, out
    assert spoken == called("Alpha reckoning"), (spoken, out)
    lines = [ln for ln in out.splitlines() if "as --calendar asks" in ln]
    assert len(lines) == 1 and "Zeta reckoning" in lines[0], out
    assert traces(page, "as --calendar asks") == [], "the override note is the terminal's"


def test_the_world_names_its_calendar():
    code, spoken, out, _ = draw(world(x_calendar=ZETA), TWO)
    assert code == 0, out
    assert spoken == called("Zeta reckoning"), (spoken, out)


def test_several_calendars_and_none_named_none_speaks():
    code, spoken, out, page = draw(world(), TWO)
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert "Dates are the world's plain integers (no calendar reads)." in out, out
    lines = [ln for ln in out.splitlines() if "none speaks" in ln]
    assert len(lines) == 1, out
    for word in ("Alpha reckoning", "Zeta reckoning", "--calendar NAME", "x_calendar", "exactly as written"):
        assert word in lines[0], (word, lines[0])
    assert "for every tool" not in lines[0], lines[0]
    assert traces(page, "calendars read", "none speaks", "x_calendar") == [], "the list is the terminal's"


def test_the_world_names_no_calendar_of_this_world():
    dangling = "019a3b10-0000-7000-8000-0000000d0a09"
    code, spoken, out, page = draw(world(x_calendar=dangling), TWO[:1])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    lines = [ln for ln in out.splitlines() if "names no calendar of this world" in ln]
    assert len(lines) == 1, out
    assert f'x_calendar is "{dangling}"' in lines[0] and "the dates stay numbers" in lines[0], lines[0]
    assert traces(page, dangling, "x_calendar") == [], "the World's value is the terminal's"
    code, spoken, out, page = draw(world(x_calendar=dangling), TWO[:1], "--calendar", "Alpha reckoning")
    assert code == 0, out
    assert spoken == called("Alpha reckoning"), (spoken, out)
    lines = [ln for ln in out.splitlines() if "names no calendar of this world" in ln]
    assert len(lines) == 1 and f'"{dangling}"' in lines[0], out
    assert traces(page, dangling, "x_calendar") == [], "the World's value is the terminal's"


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
        want = called(names[c["speaks"]]) if c["speaks"] is not None else ""
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


def ways_named(out):
    """The terminal's line on a world's calendar the page does not speak: it names the calendar
    and both ways to have it."""
    lines = [ln for ln in out.splitlines() if "plain numbers" in ln and SECRET_NAME in ln]
    assert len(lines) == 1, out
    assert "--calendar" in lines[0] and "--hidden" in lines[0], lines[0]


def test_the_world_names_a_calendar_on_a_hidden_element():
    code, spoken, out, page = draw(world(x_calendar=SECRET), [TWO[0], secret()])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert no_secret(page) == [], no_secret(page)
    ways_named(out)


def test_a_second_calendar_on_a_hidden_element_and_none_named():
    code, spoken, out, page = draw(world(), [TWO[0], secret()])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert no_secret(page) == [], no_secret(page)
    assert traces(page, "calendars read", "leaves out") == [], "the list is the terminal's"
    lines = [ln for ln in out.splitlines() if "none speaks" in ln]
    assert len(lines) == 1 and "Alpha reckoning" in lines[0] and SECRET_NAME in lines[0], out


def test_one_calendar_on_a_hidden_element_and_none_named():
    code, spoken, out, page = draw(world(), [secret()])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert "Dates are the world&#x27;s plain integers" in page or "Dates are the world's plain integers" in page
    assert no_secret(page) == [], no_secret(page)
    ways_named(out)


def test_the_world_names_a_hidden_calendar_by_its_name():
    code, spoken, out, page = draw(world(x_calendar=SECRET_NAME), [TWO[0], secret()])
    assert code == 0, out
    assert spoken == "", (spoken, out)
    assert no_secret(page) == [], no_secret(page)
    assert f'x_calendar is "{SECRET_NAME}"' in out, out


def test_left_out_calendars_leave_no_trace_on_the_page():
    found = []
    for how in LEFT_OUT:
        for others in ([], [TWO[0]]):
            for named in ({}, {"x_calendar": SECRET}, {"x_calendar": SECRET.upper()}, {"x_calendar": SECRET_NAME}):
                code, spoken, out, page = draw(world(**named), [*others, secret(how)])
                assert code == 0, out
                if spoken or no_secret(page):
                    found.append(f"{how}, {len(others)} other, {named}: page speaks {spoken!r}, "
                                 f"holds {no_secret(page)}")
    assert not found, "\n".join(found)


def test_calendar_picks_a_left_out_calendar():
    code, spoken, out, page = draw(world(), [TWO[0], secret()], "--calendar", SECRET_NAME)
    assert code == 0, out
    assert spoken == "the calendar chosen for this page", (spoken, out)
    assert "Stillmonth" in page, "the page is not labelled by the chosen calendar"
    assert traces(page, SECRET_NAME, SECRET) == [], traces(page, SECRET_NAME, SECRET)
    assert "Dates read through the calendar chosen for this page" in page, page[-800:]


def test_a_name_picks_the_drawn_calendar_first():
    hidden_first = {**secret(), "id": "019a3b10-0000-7000-8000-0000000d0001", "name": "Sun Reckoning"}
    drawn_last = {**calendar("019a3b10-0000-7000-8000-0000000dffff", "Sun Reckoning")}
    code, spoken, out, page = draw(world(), [hidden_first, drawn_last], "--calendar", "sun reckoning")
    assert code == 0, out
    assert spoken == called("Sun Reckoning"), (spoken, out)
    assert "Thaw" in page, "the page is not labelled by the drawn calendar"
    held = traces(page, hidden_first["id"], *SECRET_WORDS)
    assert held == [], held
    code, spoken, out, page = draw(world(), [hidden_first, drawn_last], "--calendar", hidden_first["id"])
    assert code == 0, out
    assert spoken == "the calendar chosen for this page" and "Stillmonth" in page, (spoken, out)


def test_the_hint_gives_an_id_for_a_name_no_shell_reads_whole():
    odd = {**secret(), "name": 'King\'s "Old" $Reckoning'}
    code, spoken, out, _ = draw(world(), [odd])
    assert code == 0 and spoken == "", (code, spoken, out)
    lines = [ln for ln in out.splitlines() if "plain numbers" in ln and "--calendar" in ln]
    assert len(lines) == 1, out
    assert f"--calendar {SECRET}," in lines[0] and "\\'" not in lines[0], lines[0]
    code, spoken, out, _ = draw(world(), [secret()])
    lines = [ln for ln in out.splitlines() if "plain numbers" in ln and "--calendar" in ln]
    assert len(lines) == 1 and f'--calendar "{SECRET_NAME}"' in lines[0], out


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
