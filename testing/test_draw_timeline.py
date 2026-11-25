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
- test_the_hint_gives_the_id_in_double_quotes: the terminal's hint for a hidden world's
  calendar gives --calendar "<id>", for a name with quotes and a dollar sign and for a plain one;
  and where a drawn calendar's id is the hidden one's name, the hint followed as written speaks
  the World's calendar;
- test_the_page_counts_the_files_not_read_and_names_none: a hidden calendar, a second file
  holding its id, six files that are not JSON and an element of a type outside the 22: the page's
  bytes hold none of their file names, not the hidden one's id or words, and say "7 files not
  read."; the terminal names all seven;
- test_a_folder_that_reads_whole_draws_the_same_page: no line about files not read when every
  file reads, and one file that does not read adds that one line to the page and nothing else;
- test_the_worlds_hidden_list_leaves_out_what_it_names, test_an_id_two_files_hold_is_drawn_from_
  neither_when_one_is_left_out, test_the_page_names_no_folder_of_the_presentation_file and
  test_a_type_outside_the_22_is_left_out_and_counted: a dated Event the World's hidden list names,
  an Event id two files hold (one hidden, in both orders), a --presentation file by its absolute
  path, and a dated element of a type outside the 22: none reaches the page's bytes, each is counted;
- test_a_proposed_mark_is_read_as_the_package_reads_it: an Event marked proposed by false, 0 or
  0.0 is left out, by "   " not, alone and beside a plain copy in either order; the World's
  calendar carrying such a mark labels no page;
- test_an_id_that_is_not_text_is_a_file_not_read: an Event whose id is a number is not drawn, not
  counted outside the 22, and the terminal says its id is not text;
- test_no_left_out_kind_reaches_a_written_file_by_any_road: every left-out kind, each by every
  road the timeline reads (its dates, an era, the calendar the World names, a copy of its id
  before and after it, the World's hidden list), one run per calendar: none in the page.

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


def hint(out):
    """The --calendar argument the terminal's hint gives, as a shell would read it."""
    lines = [ln for ln in out.splitlines() if "plain numbers" in ln and "--calendar" in ln]
    assert len(lines) == 1, out
    m = re.search(r'--calendar "([^"]*)"', lines[0])
    assert m, lines[0]
    return m.group(1)


def test_the_hint_gives_the_id_in_double_quotes():
    for name in ('King\'s "Old" $Reckoning', SECRET_NAME):
        code, spoken, out, _ = draw(world(), [{**secret(), "name": name}])
        assert code == 0 and spoken == "", (code, spoken, out)
        assert hint(out) == SECRET, out
    # A drawn calendar whose id is the hidden calendar's name: the hint, followed as written,
    # speaks the World's calendar, never the drawn one.
    hidden = {**secret(), "name": "cal-vis"}
    drawn = calendar("cal-vis", "Visible reckoning")
    code, spoken, out, _ = draw(world(x_calendar=SECRET), [hidden, drawn])
    assert code == 0 and spoken == "", (code, spoken, out)
    code, spoken, out, page = draw(world(x_calendar=SECRET), [hidden, drawn], "--calendar", hint(out))
    assert code == 0, out
    assert spoken == "the calendar chosen for this page" and "Stillmonth" in page, (spoken, out)


# Files not read: a page is handed on, and a file that did not read can belong to an element the
# page leaves out, so the page counts them and names none; the terminal names each, with its reason.
MARK = "unreadmark-q7x"
TWIN = "zz-twin-of-hidden"
OUTSIDE = "outside-the-types"
UNREAD = [f"construct/{TWIN}.json"] + [f"event/{MARK}-{n}.json" for n in range(1, 7)]
# The page's fixed sentence after the count, the same in the three scripts.
UNREAD_WORDS = b"The list, with why each did not read, is in the terminal of whoever drew this page."


def plant_unread(root, unread=True):
    """The hidden secret calendar (dated, so it would be placed if drawn), a dated Event, and an
    undated element of a type outside the 22; with `unread`, a second file holding the hidden
    calendar's id (after it in the folder's order, so it is the file not read) and six files that
    are not JSON, named with MARK."""
    rows = {"construct/hidden-one.json": {**secret(), "start_date": 2},
            "event/the-thaw.json": {"id": EVENT, "type": "event", "name": "The thaw", "start_date": 12},
            f"widget/{OUTSIDE}.json": {"id": "019a3b10-0000-7000-8000-0000000d0a0e", "type": "widget",
                                       "name": "Odd gadget"}}
    if unread:
        rows[f"construct/{TWIN}.json"] = {"id": SECRET, "type": "construct", "name": "Twin"}
    for rel, body in rows.items():
        p = root / "elements" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body), encoding="utf-8")
    if unread:
        for n in range(1, 7):
            (root / "elements" / "event" / f"{MARK}-{n}.json").write_text("{ not json", encoding="utf-8")
    (root / "world.json").write_text(json.dumps(world()), encoding="utf-8")


def draw_unread(plant):
    """(stdout, the page's bytes) for the folder `plant` makes."""
    need_package()
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        plant(root)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, str(TIMELINE), str(root), "--out", str(out), "--offline"],
                           check=False, capture_output=True, text=True, encoding="utf-8", env=env)
        assert r.returncode == 0, r.stdout + r.stderr
        return r.stdout, (out / "timeline.html").read_bytes()


def test_the_page_counts_the_files_not_read_and_names_none():
    text, page = draw_unread(plant_unread)
    found = traces(page.decode("utf-8"), TWIN, MARK, OUTSIDE, "hidden-one", SECRET, SECRET_NAME, *SECRET_WORDS)
    assert not found, found
    assert b"7 files not read." in page, page.decode("utf-8")[-1500:]
    missing = [rel for rel in UNREAD if rel not in text]
    assert not missing and "7 files not read" in text, (missing, text)
    print(f"the page holds the count and no name; the terminal names all {len(UNREAD)}")


def test_a_folder_that_reads_whole_draws_the_same_page():
    """No line about files not read when every file reads; a file that does not read changes the
    page by that one line and nothing else (the time of the read taken out)."""
    def one_broken(root):
        plant_unread(root, unread=False)
        (root / "elements" / "event" / "broken.json").write_text("{", encoding="utf-8")
    stamp = re.compile(rb"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")
    _, clean = draw_unread(lambda root: plant_unread(root, unread=False))
    _, one = draw_unread(one_broken)
    assert b"not read" not in clean, clean
    a, b = stamp.sub(b"T", clean), stamp.sub(b"T", one)
    assert b == a.replace(b'<div id="ms">', b"<div>1 file not read. " + UNREAD_WORDS + b'</div><div id="ms">'), b


# What a page leaves out besides the files not read: an element the World's hidden list names, an
# id two files hold when either copy is left out, an element of a type outside the 22, and the
# folder of the file given to --presentation.
LISTED = "019a3b10-0000-7000-8000-0000000de001"
COPIED = "019a3b10-0000-7000-8000-0000000de002"
GADGET = "019a3b10-0000-7000-8000-0000000de003"
TYPES_22 = ("ability", "character", "collective", "construct", "creature", "event", "family",
            "institution", "language", "law", "location", "map", "marker", "narrative", "object",
            "phenomenon", "pin", "relation", "species", "title", "trait", "zone")
THAW = {"event/the-thaw.json": {"id": EVENT, "type": "event", "name": "The thaw", "start_date": 12}}


def draw_rows(rows, world_keys=None, *args):
    """(exit, stdout and stderr, the page's text) for a folder of `rows` ({path under elements/:
    body}), world.json carrying `world_keys`."""
    need_package()
    with tempfile.TemporaryDirectory() as d:
        root, out = Path(d) / "world", Path(d) / "out"
        for rel, body in rows.items():
            p = root / "elements" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(body), encoding="utf-8")
        (root / "world.json").write_text(json.dumps(world(**(world_keys or {}))), encoding="utf-8")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, str(TIMELINE), str(root), "--out", str(out), "--offline", *args],
                           check=False, capture_output=True, text=True, encoding="utf-8", env=env)
        page = (out / "timeline.html").read_text(encoding="utf-8") if (out / "timeline.html").exists() else ""
    return r.returncode, r.stdout + r.stderr, page


def test_the_worlds_hidden_list_leaves_out_what_it_names():
    rows = {**THAW, "event/listed.json": {"id": LISTED, "type": "event", "name": "Listed quietly", "start_date": 5,
                                          "description": "Murmurword only here."}}
    code, text, page = draw_rows(rows, {"hidden": [LISTED]})
    assert code == 0, text
    assert not traces(page, LISTED, "Listed quietly", "Murmurword"), traces(page, LISTED, "Listed quietly", "Murmurword")
    assert "Left out: 1 hidden." in text, text
    code, text, page = draw_rows(rows, {"hidden": [LISTED]}, "--hidden")
    assert code == 0 and traces(page, "Listed quietly", "Murmurword") == ["Listed quietly", "Murmurword"], text


def test_an_id_two_files_hold_is_drawn_from_neither_when_one_is_left_out():
    for plain in ("aa-plain-copy", "zz-plain-copy"):
        rows = {**THAW,
                f"event/{plain}.json": {"id": COPIED, "type": "event", "name": "Plain copy", "start_date": 4,
                                        "description": "Plainword here."},
                "event/hidden-copy.json": {"id": COPIED, "type": "event", "name": "Hushed copy", "start_date": 6,
                                           "hidden": True, "description": "Hushword here."}}
        code, text, page = draw_rows(rows)
        assert code == 0, text
        found = traces(page, COPIED, "Plain copy", "Hushed copy", "Plainword", "Hushword")
        assert not found, (plain, found)
        assert "Left out: 1 hidden." in text and "1 file not read." in page, (plain, text)
        a, b = sorted([f"event/{plain}.json", "event/hidden-copy.json"])
        # The terminal names both files, blames neither, and says which copy the run took.
        assert f"{a} and {b} both hold the id {COPIED}; this run took event/hidden-copy.json" in text, (plain, text)
        # With --hidden no copy is left out: the first by path is drawn, as before.
        code, text, page = draw_rows(rows, None, "--hidden")
        first = "Plain copy" if plain.startswith("aa") else "Hushed copy"
        assert traces(page, "Plain copy", "Hushed copy") == [first], (plain, text)
    rows = {**THAW, "event/aa-first.json": {"id": COPIED, "type": "event", "name": "First copy", "start_date": 4},
            "event/zz-second.json": {"id": COPIED, "type": "event", "name": "Second copy", "start_date": 4}}
    code, text, page = draw_rows(rows)
    assert traces(page, "First copy", "Second copy") == ["First copy"], text
    assert (f"event/aa-first.json and event/zz-second.json both hold the id {COPIED}; "
            "this run took event/aa-first.json") in text, text


def test_the_page_names_no_folder_of_the_presentation_file():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "presfolder-q9z"
        folder.mkdir()
        bad, good = folder / "colours-bad.json", folder / "colours-good.json"
        bad.write_text("not json", encoding="utf-8")
        families = ("blue", "green", "pink", "amber")
        good.write_text(json.dumps({"types": {t: {"family": "blue"} for t in TYPES_22},
                                    "colors": {"order": list(families),
                                               "families": {f: {"light": "#123456", "dark": "#654321"}
                                                            for f in families}}}), encoding="utf-8")
        # A file that did not read, or a folder given by mistake, is named on the page not at all.
        for f, words in ((bad, "neutral greys (the presentation file did not read)"),
                         (folder, "neutral greys (the presentation file did not read)"),
                         (good, "presentation.json from colours-good.json")):
            code, text, page = draw_rows(THAW, None, "--presentation", str(f))
            assert code == 0, text
            assert not traces(page, "presfolder-q9z", "Expecting value", "colours-bad"), (f.name, page[-2000:])
            assert words in page, (f.name, page[-2000:])
            assert str(f) in text, text
            if f == bad:
                assert "Expecting value" in text, text


def test_a_type_outside_the_22_is_left_out_and_counted():
    rows = {**THAW, "widget/odd-gadget-file.json": {"id": GADGET, "type": "widget", "name": "Odd gadget",
                                                    "start_date": 4, "description": "Gadgetword here."}}
    code, text, page = draw_rows(rows)
    assert code == 0, text
    assert not traces(page, GADGET, "Odd gadget", "Gadgetword", "odd-gadget-file", "widget"), page[-2000:]
    # The terminal counts it and names it not: it is read, so it is no file not read.
    assert "Left out: 1 outside the 22 types." in text and "odd-gadget-file" not in text, text


def test_a_proposed_mark_is_read_as_the_package_reads_it():
    """false, 0 and 0.0 are a doubt, counted with the proposed; a text of only spaces is no mark. The
    World's calendar carrying such a mark labels no page."""
    for v, out in ((False, True), (0, True), (0.0, True), ("   ", False)):
        rows = {**THAW, "event/marked.json": {"id": LISTED, "type": "event", "name": "Marked Fenwick",
                                              "start_date": 5, "x_review_proposed": v, "description": "Fenword here."}}
        code, text, page = draw_rows(rows)
        assert code == 0, text
        assert bool(traces(page, "Marked Fenwick", "Fenword")) is not out, (v, text)
        assert ("Left out: 1 proposed." in text) is out, (v, text)
        # A plain copy of a proposed element, in both orders: neither copy is drawn.
        for plain in ("aa-plain", "zz-plain"):
            rows[f"event/{plain}.json"] = {"id": LISTED, "type": "event", "name": "Plain Aster", "start_date": 6}
            code, text, page = draw_rows(rows)
            assert bool(traces(page, "Plain Aster", "Marked Fenwick")) is not out, (v, plain, text)
            del rows[f"event/{plain}.json"]
        velvet = {**secret(), "hidden": False, "x_review_proposed": v}
        code, spoken, text, page = draw(world(x_calendar=SECRET), [velvet])
        assert code == 0, text
        assert bool(no_secret(page)) is not out, (v, spoken, no_secret(page))


def test_an_id_that_is_not_text_is_a_file_not_read():
    for nid in (987654321, 5.5, True):  # a whole number, a decimal, true
        rows = {**THAW, "event/numbered.json": {"id": nid, "type": "event", "name": "Numbered Feast",
                                                "start_date": 5, "description": "Numword here."}}
        code, text, page = draw_rows(rows, {"hidden": [nid]})
        assert code == 0, text
        assert not traces(page, "Numbered Feast", "Numword"), (nid, page[-1500:])
        assert "outside the 22" not in text and "1 file not read." in page, (nid, text)
        assert "event/numbered.json: its id is not text" in text, (nid, text)


# Every left-out kind, each by every road the timeline reads an element by: its dates, an era, a
# calendar the World names, a copy of its id in two other files (one sorting before it, one after),
# the World's hidden list.
LEAKS = {"hidtrue": {"hidden": True}, "hidyes": {"hidden": "yes"}, "hidone": {"hidden": 1},
         "hidobj": {"hidden": {"a": 1}}, "listed": {}, "propmark": {"x_review_proposed": {"by": "someone"}},
         "propfalse": {"x_review_proposed": False}, "propzero": {"x_review_proposed": 0},
         "propzerof": {"x_review_proposed": 0.0}}
FORCED = {"room": (("event", "Sitting"), ("construct", "Spec"), {"x_room_of": world()["id"]}),
          "aid": (("law", "Charter"), ("construct", "Guide"), {"x_charter_of": world()["id"]}),
          "outside": (("widget", None), ("widget", None), {})}


def plant_every_kind():
    """(rows, the calendars' ids, the World's hidden list, every id, name and word a page may not hold)."""
    rows, secrets, cals, listed, n = dict(THAW), set(), [], [], [0]

    def nid():
        n[0] += 1
        return f"019a3b10-0000-7000-8000-0000001{n[0]:05d}"

    kinds = [(k, ("event", None), ("construct", None), mark) for k, mark in LEAKS.items()]
    kinds += [(k, a, c, mark) for k, (a, c, mark) in FORCED.items()]
    for k, (ta, sa), (tc, sc), mark in kinds:
        one, cal = nid(), nid()
        cal_words = [f"Mon{k}A", f"Mon{k}B", f"Era{k}Q"]
        rows[f"{ta}/m-{k}.json"] = {"id": one, "type": ta, "name": f"Leak{k}Q", "start_date": 3,
                                    "description": f"Desc{k}Q", **({"supertype": sa} if sa else {}), **mark}
        rows[f"{tc}/c-{k}.json"] = {"id": cal, "type": tc, "name": f"Cal{k}Q", "start_date": 1, "end_date": 2,
                                    "description": f"Desc{k}CalQ", **({"supertype": sc} if sc else {}), **mark,
                                    "atlas_calendar": {"version": 1, "grain": "day",
                                                       "bundles": {"months": {"names": cal_words[:2], "lengths": [10, 10]}},
                                                       "eras": [{"name": cal_words[2], "start": 0}]}}
        secrets |= {one, cal, f"Leak{k}Q", f"Desc{k}Q", f"Cal{k}Q", f"Desc{k}CalQ", f"m-{k}", f"c-{k}", *cal_words}
        cals.append(cal)
        listed += [one, cal] if k == "listed" else []
        if k != "outside":  # a copy that is only outside the 22 keeps no id out (amendment 1)
            for side in ("a", "z"):
                rows[f"{ta}/{side}-plain-{k}.json"] = {"id": one, "type": ta, "name": f"Plain{side}{k}Q", "start_date": 4}
                secrets |= {f"Plain{side}{k}Q", f"{side}-plain-{k}"}
    # An id that is not text, in three kinds: a whole number, a decimal, true; the World lists each.
    for stem, nid in (("m-numid", 987654321), ("m-floatid", 5.5), ("m-trueid", True)):
        rows[f"event/{stem}.json"] = {"id": nid, "type": "event", "name": f"Leak{stem[2:]}Q", "start_date": 3}
        secrets |= {f"Leak{stem[2:]}Q", stem}
        listed.append(nid)
    secrets.add("987654321")
    return rows, cals, listed, secrets


def test_no_left_out_kind_reaches_a_written_file_by_any_road():
    rows, cals, listed, secrets = plant_every_kind()
    found = {}
    for cal in [None, *cals]:  # the World naming no calendar, then each left-out calendar in turn
        code, text, page = draw_rows(rows, {"hidden": listed, **({"x_calendar": cal} if cal else {})})
        assert code == 0, text
        hits = traces(page, *secrets)
        if hits:
            found[cal] = hits
    assert not found, found
    print(f"{len(cals) + 1} runs, {len(secrets)} ids, names and words: none in timeline.html")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
