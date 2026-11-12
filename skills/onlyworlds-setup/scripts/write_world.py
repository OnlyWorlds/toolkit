"""Write a new world folder from a starter pack and a filled plan (the onlyworlds-setup skill).

    python write_world.py PLAN.json OUT_FOLDER [--bulk BULK.json]

The model fills the plan from the interview; this script does the counting: it mints the ids,
fills every placeholder, writes each file by the folder format's writer rules, checks the sizes,
and writes the harness copies of the world skill. It refuses, and writes nothing, when OUT_FOLDER
already holds files, a `{{` is left after filling (it names the file and the line), a link names
no element, the charter is over its budget, a plan value it puts on a line of a text holds a line
break or a control character (it names the key), or a path would land outside the folders it is
given (it names the path). The packs aim for skills under SKILL_MAX characters; a skill of SKILL_MAX
or more is written whole, with a note giving its size and the aim and saying that nothing needs
changing: its length follows the plan's own names. A skill's front matter description is written as
a YAML double-quoted scalar, so a reader reads exactly the filled text whatever the names hold. A
skill whose description is over DESCRIPTION_MAX
characters is written too, with a note giving its length and the specification's number. It deletes
nothing it did not make: when it stops on an error, or an interrupt, after its first act, it takes the
run back, last act first (a file it made removed, a line it appended cut off, a file it wrote over
given its bytes back, a folder it made removed while empty), and says each path it could not put back.
An interrupt during that take-back stops it: the path it was on is said as unknown, each path not yet
reached as left.

The plan (JSON):

    {
      "pack": "company",                       # a folder name under ../packs/
      "today": "2026-10-22",                   # the setup day (ISO date)
      "world": {"name": "...", "slug": "...", "description": "..."},
      "values": {"org": "...", "keeper": "...", ...},   # every {{name}} the pack's texts use
      "charter": {"links": {"author": "org", "adjudicators": ["keeper-title"]},
                  "x_checks_rules": []},         # optional: the checks slot (below)
      "skill": {"utility": "one line: what the skill is for"},
      "prefix": "fern",                        # a pack with design.md and work.md: the world's own short
                                               # lower-case word for its three skills (asked; never guessed)
      "elements": [
        {"key": "org", "type": "institution",
         "fields": {"name": "...", "supertype": "Company", "description": "..."},
         "links": {"parent_institution": "other-key", "characters": ["a", "b"]}},
        {"key": "ada", "type": "character", "seat": {"role": "owner"}, "fields": {...}},
        {"key": "ai-1", "type": "character", "seat": {"role": "contributor", "ai_of": "ada"},
         "fields": {"name": "...", "supertype": "Agent", ...}}
      ],
      "online": {"world_id": "<the id onlyworlds.com gave the empty world>"},   # or absent: a folder
      "copies": "C:/work/acme",                # the root the agent runs in (a project, or the home folder),
                                               # "world" when the world folder IS that root, or "none"
      "agents_md": true,                       # the one-line AGENTS.md beside the copies (appended to an
                                               # existing one, and to a CLAUDE.md there; printed for a home)
      "repo": false                            # true: a .gitignore for a shared repository
    }

The placement is the plan's: without "online" the world is a folder, and the texts keep only
their folder lines; with it, their online lines, which name the server world id (written to
world.json's `api.world_id`, except in a repository, whose world.json never carries an `api`
block). A pack text marks a placement's lines between `<!-- if folder -->` (or `<!-- if online -->`)
and `<!-- end -->`, each on its own line.

The Charter always carries `x_checks_rules` (the checks profile, schema-dist `profiles/checks.md`): the
plan's `charter.x_checks_rules` when it gives a list, else the pack's `checks.json` when the pack has
one, else the empty slot `[]`, so a keeper finds it. It is written beside the other body keys and goes
to the wire in the bulk body like any `x_` key; the writer never reads or judges a rule.

The reading aids carry the mark `x_charter_of` (the charter profile, schema-dist `profiles/charter.md`):
the Charter, and every element whose type and supertype, trimmed and case-folded as the room profile
defines, are `law`/`Charter`, `construct`/`Guide` or `construct`/`Domain`. Its value is the id of the
world the element is in: the folder's minted id for a folder world, the server's (`online.world_id`)
for an online one, whose elements live in the server world. Without the mark a reader treats the three
as lore. The key is the writer's: a plan that sets any `x_charter_` field itself is refused, and so is
a plan row whose pair is `law`/`Charter`, since the pack's charter is the world's one Charter.

A seat (question 4) is a Character row's "seat": its role (owner, co_builder, contributor, guest)
and, for an AI, "ai_of" (the key of its human). The file carries it as `x_seat`; the charter's
"Who is here" lists every seat. Online, an AI's Character comes from its seat (keel's "its own new
Character"), so its row is not written and nothing may link it.

A pack that holds `design.md` and `work.md` beside `skill.md` (a team world: company,
software-project) lands three skills, each written as `skill.md` is: an Object with supertype Skill
whose description is the filled text, under the same size note and front-matter test, and its two
harness copies. Their names take the plan's "prefix": `<prefix>-start` (the world skill),
`<prefix>-design`, `<prefix>-work`. Such a plan without a prefix is refused: the pack never invents
one. Any other pack keeps one skill, `ow-<slug>`.

Placeholders: `{{name}}` from "values", plus the ones this script knows: world_name, world_slug,
charter_id, skill_id, skill_name (ow-<slug>, or <prefix>-start), prefix, design_skill_id,
design_skill_name, work_skill_id, work_skill_name (the last five in a three-skill pack only),
today (ISO), today_day (the day number),
server_world_id (online only), world_folder (the world folder as the copies' root sees it),
who_is_here, roster, proposer_id, agents_line, world_id (the id of the world the elements are in, the
value `x_charter_of` takes: a mark's value, such as a sitting's `x_room_of`), and `{{id:<key>}}` for
any element's id (a seeded room element's `x_room_of` names its sitting by it). They are
filled in the charter, the skill and every string field of every element, before any shape test:
a date field written as "day:YYYY-MM-DD" (or "day:{{today}}") becomes its day number, since a work
world counts time in days, day 0 = 1970-01-01. The folder's own minted id is no placeholder of its
own: an online world does not share it, so `world_id` is the server's there, and no text names it
as an address.

Python 3, stdlib only.
"""
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

CHARTER_MAX = 4000
SKILL_MAX = 10000
DESCRIPTION_MAX = 1024  # the Agent Skills specification's description length (agentskills.io)
SLUG_MAX = 61  # a plan's own slug: the made slug's alphabet; `ow-<slug>` within a skill name's 64
# The 22 element types, each its folder under elements/ (knowledge/schema-reference.md; a test pins it).
TYPES = ("ability", "character", "collective", "construct", "creature", "event", "family", "institution",
         "language", "law", "location", "map", "marker", "narrative", "object", "phenomenon", "pin",
         "relation", "species", "title", "trait", "zone")
# A line break is \n, \r\n or \r, nothing else: refused only where the writer puts a value on one line.
# Every other character below U+0020 (the tab among them), U+007F, the C1 range and the two Unicode line
# separators are control characters: refused in every value the writer puts into a text.
LINE_BREAKS = ("\r\n", "\r", "\n")
SEPARATORS = (chr(0x2028), chr(0x2029))
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
FORMAT_VERSION = "0.3.22"
EPOCH = datetime.date(1970, 1, 1)
PACKS = Path(__file__).resolve().parent.parent / "packs"
PH = re.compile(r"\{\{([a-z_]+(?::[A-Za-z0-9_-]+)?)\}\}")
DAY = re.compile(r"^day:(\d{4}-\d{2}-\d{2})$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PREFIX = re.compile(r"^[a-z][a-z0-9]{0,15}$")
# A team world's two skills beside the world skill: the template, the Object's name and utility.
EXTRA_SKILLS = (("design", "design skill", "How an agent talks a design through with a person here."),
                ("work", "work skill", "How an agent does a session of work here and hands in its report."))
IF = re.compile(r"^<!-- if (folder|online) -->$")
END = "<!-- end -->"
NAMED = 8
ROLES = {"owner": "owner", "co_builder": "co-builder", "contributor": "contributor", "guest": "guest"}
RANK = {"owner": 3, "co_builder": 2, "contributor": 1, "guest": 0}
# The charter profile's three reading-aid pairs, folded; trimmed by Unicode's White_Space set, as the
# room profile defines (a byte order mark is not whitespace and stays).
READING_AIDS = {("law", "charter"), ("construct", "guide"), ("construct", "domain")}
WHITE_SPACE = ("\t\n\x0b\x0c\r \x85\xa0         "
               "       　")


def is_reading_aid(type_, supertype):
    if not isinstance(type_, str) or not isinstance(supertype, str):
        return False
    return (type_.strip(WHITE_SPACE).casefold(), supertype.strip(WHITE_SPACE).casefold()) in READING_AIDS

# The one AGENTS.md sentence: the writer writes it beside the copies and fills it into the world
# skill's courtesy line ({{agents_line}}), so the two cannot drift.
AGENTS_LINE = ("This folder works in the {world_name} world (OnlyWorlds): read its charter first "
               "({charter_route}), then load the {skill_name} skill.")
# The roster line of every pack's charter ({{roster}}), by placement.
ROSTER = {"folder": "The roster: the Characters marked x_seat (elements/character/).",
          "online": "The roster: GET /members."}
# Who a proposal's x_review_proposed "by" names ({{proposer_id}}), by placement.
PROPOSER = {"folder": "your Character's id", "online": "your membership id"}
# Every pack's world folder gets the same .gitattributes (the writer rules: LF, also on Windows).
GITATTRIBUTES = ("* text=auto eol=lf\n*.png binary\n*.jpg binary\n*.jpeg binary\n*.gif binary\n"
                 "*.webp binary\n*.pdf binary\n*.zip binary\n*.owworld binary\n")
GITIGNORE = ".*/\n!.agents/\n!.claude/\n.env\n.env.*\n"


def uuid7():
    b = bytearray(int(time.time() * 1000).to_bytes(6, "big") + os.urandom(10))
    b[6] = (b[6] & 0x0F) | 0x70
    b[8] = (b[8] & 0x3F) | 0x80
    h = b.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def day_number(iso):
    return (datetime.date.fromisoformat(iso) - EPOCH).days


def slug(text, cap=40):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower().encode("ascii", "ignore").decode()).strip("-")
    return s[:cap].strip("-")


def control_in(value):
    """The first control character anywhere in a text once its line breaks (\\n, \\r\\n, \\r) are set
    aside, or None; every character is read, not only the first odd one."""
    rest = value
    for brk in LINE_BREAKS:
        rest = rest.replace(brk, "")
    return next((c for c in rest if ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F or c in SEPARATORS), None)


def has_line_break(value):
    return any(brk in value for brk in LINE_BREAKS)


def surrogate_in(node, at="plan"):
    """Where a plan holds a lone surrogate (no UTF-8 file can store one), as a key path, or None."""
    lone = lambda s: any(0xD800 <= ord(c) <= 0xDFFF for c in s)  # noqa: E731
    if isinstance(node, str):
        return at if lone(node) else None
    items = node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else ()
    for k, v in items:
        here = f"{at}[{k}]" if isinstance(k, int) else (f"{at}.{k}" if at != "plan" else str(k))
        if isinstance(k, str) and lone(k):
            return f"{at}, the key {k!a}"
        where = surrogate_in(v, here)
        if where is not None:
            return where
    return None


def one_line_places(pack, placement):
    """Each placeholder the pack's written texts put in a place that is one line (a front matter line
    other than the description, which double_quoted() carries; a heading; a table row), with its first
    such place: {name: "a heading (packs/<pack>/<file> line n)"}. Read from the templates, so a new
    template needs no list. It reads a heading as a line starting with `#` and a table row as a line
    starting with `|`: an indented heading, a setext heading (a line under `===` or `---`) and a table
    row without a leading pipe are not seen. No template holds one; a template that adds one adds its
    shape here first."""
    found = {}
    for name in ("charter.md", "skill.md", "design.md", "work.md"):
        if not (pack / name).exists():
            continue
        fence = 0
        for src, ln in template(pack / name, placement, []):
            fence += ln == "---"
            if fence == 1 and ln != "---" and not ln.startswith("description: "):
                kind = "a front matter line"
            elif ln.startswith("#"):
                kind = "a heading"
            elif ln.lstrip().startswith("|"):
                kind = "a table row"
            else:
                continue
            for m in PH.finditer(ln):
                found.setdefault(m.group(1), f"{kind} (packs/{pack.name}/{name} line {src})")
    return found


def double_quoted(text):
    """`text` as a YAML double-quoted scalar, which a YAML reader reads back as exactly `text`: a
    backslash and a double quote escaped, and every character YAML does not print as itself (a
    control character, a line break, a byte order mark, a non-character) as its \\x or \\u escape.
    And a third dash in a row as \\x2d, so the line never holds `---`: skills-ref and Claude Code end
    the front matter at a `---` anywhere, even inside a quoted scalar, and drop it whole.
    PyYAML 6.0 and skills-ref 0.1.0's parser read `---` back from it (2026-11-12).
    Claude Code's `plugin validate --strict` passes the file but does not show the description it read."""
    out, dashes = [], 0
    for c in text:
        o = ord(c)
        dashes = dashes + 1 if c == "-" else 0
        if dashes == 3:
            out.append("\\x2d")
            dashes = 0
        elif c in '\\"':
            out.append("\\" + c)
        elif o < 0x20 or 0x7F <= o <= 0x9F or c in "\u2028\u2029\ufeff\ufffe\uffff" or 0xD800 <= o <= 0xDFFF:
            out.append(f"\\x{o:02x}" if o <= 0xFF else f"\\u{o:04x}")
        else:
            out.append(c)
    return '"' + "".join(out) + '"'


def outside(path, root):
    """True when `path` does not lie under `root`, both read as written: made absolute and their `..`
    folded, case-folded where the system folds, links never followed (a project whose .claude is a link
    is the user's to make). A path on another drive, or a drive-relative one such as D:x, is outside."""
    p, r = (os.path.normcase(os.path.abspath(x)) for x in (path, root))
    try:
        return os.path.commonpath([p, r]) != r
    except ValueError:  # another drive
        return True


def template(path, placement, problems):
    """A pack text for one placement: (source line number, line) pairs, without the leading
    template-note comment lines, the other placement's lines, or the markers."""
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    rows, n, block = [], 0, None
    while n < len(lines) and lines[n].startswith("<!--") and lines[n].rstrip().endswith("-->") \
            and not IF.match(lines[n].strip()):
        n += 1
    for i in range(n, len(lines)):
        ln, src = lines[i], i + 1
        m = IF.match(ln.strip())
        if m:
            if block:
                problems.append(f"{path.parent.name}/{path.name} line {src}: an `if` inside an `if`")
            block = m.group(1)
        elif ln.strip() == END:
            if not block:
                problems.append(f"{path.parent.name}/{path.name} line {src}: an `end` with no `if`")
            block = None
        elif block in (None, placement):
            rows.append((src, ln))
    if block:
        problems.append(f"{path.parent.name}/{path.name}: an `if {block}` never ends")
    while rows and not rows[0][1].strip():
        rows.pop(0)
    while rows and not rows[-1][1].strip():
        rows.pop()
    return rows


def checks_of(charter_plan, pack, problems):
    """The Charter's x_checks_rules: the plan's list, else the pack's checks.json, else the empty slot."""
    if "x_checks_rules" in charter_plan:
        rules, src = charter_plan["x_checks_rules"], "plan charter"
    elif (pack / "checks.json").exists():
        rules, src = json.loads((pack / "checks.json").read_text(encoding="utf-8")), f"packs/{pack.name}/checks.json"
    else:
        return []
    if not isinstance(rules, list) or not all(isinstance(r, dict) for r in rules):
        problems.append(f"{src}: x_checks_rules is a list of rule objects")
        return []
    return rules


def file_id(st):
    """A file's identity on its volume, or None where the system gives none (st_ino 0)."""
    return (st.st_dev, st.st_ino) if st.st_ino else None


class Journal:
    """The run's acts, each recorded before it is attempted: a folder made, a file made new, a file
    appended to (its length before), a file written over (its bytes before). undo() takes them back,
    last act first, and only what this run did: a folder only while empty (rmdir), a file only while it
    is the same file and holds nothing but a start of what this run wrote there (bytes the run did not
    write are never cut or removed; such a file is reported, and left as it is).

    The journal is the only record of what the undo did. Each act done gets its answer in one
    assignment, act["answer"]: None when taken back, else the state it is left in. So its two lists are
    read off the acts, never kept beside them: unanswered() (the acts done that have no answer yet)
    and not_put_back() (the acts answered with a state); every sentence about what is left reads them."""

    def __init__(self):
        self.acts = []  # dicts: kind, path, before, data, id, done, and answer once undone
        self.at = None  # the path of the act being attempted
        self.last = None  # the path of the last act done
        self.refused = False  # the folder pass refused, and said so

    # An act counts as done from just before it is attempted: an interrupt can land after the system
    # made the folder or opened the file and before the next line runs. Only an OSError from the
    # attempt itself says it changed nothing, and takes it off.

    def mkdir(self, folder):
        self.at = folder
        act = {"kind": "folder", "path": folder, "done": True}
        self.acts.append(act)
        try:
            folder.mkdir()
        except OSError:
            act["done"] = False
            raise
        self.at, self.last = None, folder

    def write(self, path, data, append):
        self.at = path
        if append:
            act = {"kind": "appended", "before": os.path.getsize(path)}
        elif path.exists():
            with open(path, "rb") as fh:
                act = {"kind": "overwritten", "before": fh.read()}
        else:
            act = {"kind": "new"}  # opened "xb": a file another process made meanwhile is refused, never taken
        act.update(path=path, data=data, done=True)
        self.acts.append(act)
        try:
            fh = open(path, "ab" if append else "wb" if act["kind"] == "overwritten" else "xb")
        except OSError:
            act["done"] = False
            raise
        with fh:
            act["id"] = file_id(os.fstat(fh.fileno()))
            fh.write(data)
        self.at, self.last = None, path

    def unanswered(self):
        """The acts done that the undo has not answered for, last first."""
        return [a for a in reversed(self.acts) if a["done"] and "answer" not in a]

    def not_put_back(self):
        """The acts the undo answered for with a state: what it could not put back, last first."""
        return [a for a in reversed(self.acts) if a.get("answer")]

    def undo(self):
        """Every act done taken back, last first, each answered in one assignment. An error inside one
        act's undo is that act's answer, and the undo goes on to the act before. An interrupt stops the
        undo where it lands: the act in hand and the ones before it stay unanswered, and it is raised."""
        for act in self.unanswered():
            try:
                state = self.undo_one(act)
            except OSError as err:
                state = f"could not be read back to be undone ({said(err)}); left as it is"
            except Exception as err:
                state = f"its undo was stopped by {said(err)}, and not finished; left as it stands"
            act["answer"] = state

    @staticmethod
    def undo_one(act):
        p, kind = act["path"], act["kind"]
        if kind == "folder":
            try:
                p.rmdir()
            except FileNotFoundError:
                return None
            except OSError as err:
                return f"the folder this run made could not be removed ({said(err)}); what stands at this path is left as it is"
            return None
        try:
            st = os.stat(p)
        except FileNotFoundError:
            return None if kind == "new" else "gone: no file stands at this path now"
        if act.get("id") and file_id(st) and file_id(st) != act["id"]:
            return "another file stands at this path now; left as it is"
        with open(p, "rb") as fh:
            now = fh.read()
        ours = now[act["before"]:] if kind == "appended" else now
        if (kind == "appended" and len(now) == act["before"]) or (kind == "overwritten" and now == act["before"]):
            return None  # the act never reached the file (an interrupt before the open)
        if kind == "appended" and (len(now) < act["before"] or not act["data"].startswith(ours)):
            return "no longer ends with only what this run appended to it; left as it is"
        if not act["data"].startswith(ours):
            return "no longer holds only what this run wrote there; left as it is"
        try:
            if kind == "new":
                os.remove(p)
            elif kind == "overwritten":
                with open(p, "wb") as fh:
                    fh.write(act["before"])
            else:
                with open(p, "r+b") as fh:
                    fh.truncate(act["before"])
        except OSError as err:
            why = f"({said(err)})"
            return {"new": f"made by this run, and still there {why}",
                    "overwritten": f"written over by this run, and its bytes before could not be written back "
                                   f"{why}; it holds what this run wrote, or only part of its bytes before",
                    "appended": f"still ends with the {len(ours)} byte(s) this run appended {why}"}[kind]
        return None


def said(err):
    """An error in its own words: its type, and its system message when it has one."""
    if isinstance(err, OSError) and err.strerror:
        return f"{type(err).__name__}: {err.strerror}"
    return f"{type(err).__name__}: {err}" if str(err) else type(err).__name__


def say(text):
    """Text to the output in one write, flushed: inside the journal's span, its failure undoes the run.
    A run with no output at all (none was given it) has nowhere to put the text, and that is no error."""
    if sys.stdout is None:
        return
    sys.stdout.write(text)
    sys.stdout.flush()


def say_refusal(text):
    """A refusal: to the output; when there is none, or it fails, to the error output; when that is
    gone too, the exit code still says it."""
    try:
        if sys.stdout is not None:
            say(text)
            return
    except (OSError, ValueError):
        pass
    try:
        if sys.stderr is not None:
            sys.stderr.write(text)
            sys.stderr.flush()
    except (OSError, ValueError):
        pass


def refusal(journal, whole, head):
    """The one place that says what a refused run left, read from the journal's two lists alone: `whole`
    (its own lines) when both are empty; else `head`, then the act in hand when an interrupt stopped the
    undo (UNKNOWN: it may or may not have been taken back), each act answered as not put back and each
    act the undo never reached (NOT PUT BACK), and the count."""
    # The undo goes last act first, so the first act it never answered for is the one in hand when an
    # interrupt stopped it: its step may have finished, or not. The acts before it were never reached.
    in_hand, *unreached = journal.unanswered() or [None]
    left = [(a["path"], a["answer"]) for a in journal.not_put_back()]
    left += [(a["path"], "the undo was interrupted before it reached this act; left as it is") for a in unreached]
    if not left and in_hand is None:
        return whole
    lines = [f"NOT PUT BACK {p}: {state}\n" for p, state in left]
    if in_hand is None:
        return (f"{head}{len(left)} path(s) below\n" + "".join(lines)
                + f"left behind: the {len(left)} path(s) above; 1 problem(s)\n")
    lines.insert(0, f"UNKNOWN {in_hand['path']}: the undo was interrupted while on this act; it may or may not have "
                    f"been taken back, so look at it\n")
    return (f"{head}{len(left)} path(s) marked NOT PUT BACK below, and perhaps the 1 marked UNKNOWN\n"
            + "".join(lines) + f"left behind: the {len(left)} path(s) marked NOT PUT BACK, and perhaps the 1 "
            f"marked UNKNOWN; 1 problem(s)\n")


def undone(journal, err):
    """The refusal after an error mid-run: the journal undone, then the path that failed, the error's
    own words, and what is left behind, read from the journal. An interrupt in the undo is raised
    after the refusal is said."""
    where = journal.at or getattr(err, "filename", None)
    words = (f"{type(err).__name__}: {err.strerror}" if isinstance(err, OSError) and err.strerror
             else "interrupted (KeyboardInterrupt)" if isinstance(err, KeyboardInterrupt)
             else f"{type(err).__name__}: {err}")
    head = (f"{where}: {words}" if where else f"after {journal.last}: {words}" if journal.last
            else f"before its first act: {words}")
    try:
        journal.undo()
    finally:  # an interrupt in the undo too: the refusal is said from the journal, then it goes on
        say_refusal(refusal(journal,
                            f"REFUSED {head}; the writer stopped there and took back everything it had written\n"
                            f"nothing left behind; 1 problem(s)\n",
                            f"REFUSED {head}; the writer stopped there and took back what it had written, but for "))
    return 1


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def shown(path, root):
    """A path as an agent at `root` sees it: relative under it, absolute otherwise; posix."""
    try:
        rel = Path(os.path.relpath(path, root))
    except ValueError:  # another drive
        return Path(path).resolve().as_posix()
    if rel.parts and rel.parts[0] == "..":
        return Path(path).resolve().as_posix()
    return rel.as_posix()


def main(argv):
    """The writer, with one catch before its first act: an error there (a plan in a shape it does not
    read, such as a list where a name goes, or a fault of the writer's own) stops it with the error's
    own words, and the key when a key is missing, and nothing is written. From its first act on, the
    run's journal catches every error, and the interrupt, and takes the run back (write_world)."""
    state = {"writing": False}
    try:
        return write_world(argv, state)
    except (KeyError, TypeError, AttributeError, ValueError, IndexError, OSError) as err:
        if state["writing"]:
            raise
        what = (f"KeyError: no key {err.args[0]!r} where one is read" if isinstance(err, KeyError)
                else f"{type(err).__name__}: {err}")
        to = sys.stdout or sys.stderr  # with no output at all, a refusal goes to the error output
        print(f"REFUSED the writer stopped before writing anything ({what})", file=to)
        print("nothing written; 1 problem(s)", file=to)
        return 1


def write_world(argv, state):
    bulk_arg = argv[argv.index("--bulk") + 1] if "--bulk" in argv and argv.index("--bulk") + 1 < len(argv) else None
    bulk = Path(bulk_arg) if bulk_arg else None
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and not (bulk_arg and i == argv.index("--bulk") + 1)]
    if len(args) != 2:
        sys.exit(__doc__.split("\n\n")[1])
    if hasattr(sys.stdout, "reconfigure"):  # a name the console cannot show prints escaped, never a crash
        sys.stdout.reconfigure(errors="backslashreplace")
    plan = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    out = Path(args[1])
    problems = []
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} already holds files: this script only writes new folders")
    pack = PACKS / plan["pack"]
    if not (pack / "PACK.md").exists():
        sys.exit(f"no pack {plan['pack']!r} under {PACKS}")

    # Every plan value is checked before anything is made, so the writer writes it all or refuses
    # before writing. A value the writer puts into a text is a string. A tab or another control
    # character is refused in it everywhere; a line break only where the value lands in a place that is
    # one line (read from the templates, and the writer's own uses: names, paths, the AGENTS.md line).
    # A value whose every place is a paragraph or a list item keeps its line breaks, as do the free
    # texts that land only in JSON (world.description, skill.utility, an element's fields).
    online = plan.get("online")
    placement = "online" if online else "folder"
    lone = surrogate_in(plan)
    if lone is not None:
        problems.append(f"{lone}: holds a lone surrogate (a half of a character), which no UTF-8 file can "
                        f"store; remove it")
    w = plan.get("world") if isinstance(plan.get("world"), dict) else {}
    one_line_at = one_line_places(pack, placement) if lone is None else {}
    texts = [("world.name", w.get("name"), "the world skill's name and the AGENTS.md line", True),
             ("world.slug", w.get("slug"), "a file name", False), ("prefix", plan.get("prefix"), "the skills' names", False),
             ("copies", plan.get("copies"), "a folder path", False),
             ("today", plan.get("today"), "a date", True)]
    for k, v in plan.get("values", {}).items():
        texts.append((f"values.{k}", v, one_line_at.get(k), True))
    humans = {(e.get("seat") or {}).get("ai_of") for e in plan["elements"]}
    for e in plan["elements"]:  # the seats and their humans reach the charter's "Who is here"
        seat = e.get("seat") or {}
        if seat or e["key"] in humans:
            texts.append((f"plan element {e['key']!r}, name", e.get("fields", {}).get("name", e["key"]),
                          "the Character's name", True))
        if seat.get("ai_of") is not None:
            texts.append((f"plan element {e['key']!r}, supertype", e.get("fields", {}).get("supertype", "Agent"),
                          "the Character's supertype", True))
    for label, v, place, needed in ([] if lone is not None else texts):
        if v is None and not needed:
            continue
        if not isinstance(v, str):
            problems.append(f"{label} {v!r}: the writer puts it into a text, so it is a string (in quotes)")
            continue
        shown_ = v if len(v) <= 60 else v[:60] + "..."
        c = control_in(v)
        if c == "\t":
            problems.append(f"{label} {shown_!r}: holds a tab; write a space instead")
        elif c is not None:
            problems.append(f"{label} {shown_!r}: holds a control character (U+{ord(c):04X}); remove it")
        if has_line_break(v) and place:
            problems.append(f"{label} {shown_!r}: holds a line break (\\n, \\r\\n or \\r), and it lands in "
                            f"{place}, which is one line; write it on one line")
        if "{{" in v:
            problems.append(f"{label} {shown_!r}: holds `{{{{`, which the writer reads as the start of a "
                            f"placeholder; write the value without it")
    if lone is None and isinstance(plan.get("today"), str) and not problems:
        try:  # the shape first (fromisoformat also takes 20261112 and 2026-W46-4), then the date
            if not DATE.fullmatch(plan["today"]):
                raise ValueError
            day_number(plan["today"])
        except ValueError:
            problems.append(f"today {plan['today']!r}: the setup day, a date written YYYY-MM-DD")
    for e in plan["elements"]:  # an element's type is its folder: one of the 22
        if e.get("type") not in TYPES:
            problems.append(f"plan element {e.get('key')!r}, type {e.get('type')!r}: one of the 22 element "
                            f"types, lowercase ({', '.join(TYPES)})")
    if problems:
        for p in problems:
            print("REFUSED", p, file=sys.stdout or sys.stderr)
        print(f"nothing written; {len(problems)} problem(s)", file=sys.stdout or sys.stderr)
        return 1

    server_id = (online or {}).get("world_id", "")
    if online and not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", server_id):
        problems.append(f"online.world_id {server_id!r}: the id onlyworlds.com gave the empty world, a UUID")
    # A plan's own slug keeps the made slug's rule (lowercase letters and digits, one hyphen between),
    # up to SLUG_MAX: it names files and, in a one-skill pack, the skill.
    if w.get("slug") and not (isinstance(w["slug"], str) and SKILL_NAME.fullmatch(w["slug"])
                              and len(w["slug"]) <= SLUG_MAX):
        problems.append(f"world.slug {w['slug']!r}: lowercase letters and digits, one hyphen between, "
                        f"{SLUG_MAX} at most, as a slug made from the name")
    world_slug = w.get("slug") or slug(w["name"])
    # A team world's pack lands three skills under the world's own prefix; any other pack, one.
    extras = [x for x in EXTRA_SKILLS if (pack / f"{x[0]}.md").exists()]
    prefix = plan.get("prefix")
    if extras and not (isinstance(prefix, str) and PREFIX.match(prefix)):
        problems.append(f"prefix {prefix!r}: the {plan['pack']} pack's skills take the world's own prefix "
                        f"(question 2), one short lower-case word (a letter first, 16 at most); the pack "
                        f"never invents one")
        prefix = "prefix"
    skill_name = f"{prefix}-start" if extras else "ow-" + world_slug
    if not SKILL_NAME.match(skill_name) or len(skill_name) > 64:
        problems.append(f"skill name {skill_name!r}: lowercase letters, digits and hyphens, 64 at most"
                        + ("; the world's name keeps no letter a slug keeps, so give `world.slug` in the plan "
                           "(lowercase letters and digits, one hyphen between)" if not extras and not world_slug else ""))
    today = plan["today"]
    rows = plan["elements"]
    ids = {e["key"]: uuid7() for e in rows}
    names = {e["key"]: e.get("fields", {}).get("name", e["key"]) for e in rows}
    world_id, charter_id, skill_id = uuid7(), uuid7(), uuid7()
    extra_ids = {x[0]: uuid7() for x in extras}
    # The reading aids' mark names the world the element is in: online, the server's world, never the
    # folder's minted id (which is no address there).
    charter_of = server_id if online else world_id

    # The seats (question 4): every Character row with a "seat"; online, an AI's row is its seat's.
    people, ais, seat_of, from_seat = {r: [] for r in ROLES}, [], {}, set()
    for e in rows:
        seat = e.get("seat")
        if not seat:
            continue
        where = f"plan element {e['key']!r}, seat"
        if e["type"] != "character":
            problems.append(f"{where}: only a Character has a seat")
        if seat.get("role") not in ROLES:
            problems.append(f"{where}: role {seat.get('role')!r}, one of {', '.join(ROLES)}")
        ai_of = seat.get("ai_of")
        if ai_of is not None and ai_of not in ids:
            problems.append(f"{where}: ai_of {ai_of!r} names no element")
        mark = {"role": seat.get("role")}
        if ai_of in ids:
            mark["ai_of"] = ids[ai_of]
            if online:
                from_seat.add(e["key"])
        seat_of[e["key"]] = mark
        word = ROLES.get(seat.get("role"), seat.get("role"))
        if ai_of is not None:
            kind = e.get("fields", {}).get("supertype", "Agent")
            ais.append(f"{names[e['key']]} ({kind}, {word}, {names.get(ai_of, ai_of)}'s AI)")
        elif seat.get("role") in people:
            people[seat["role"]].append(names[e["key"]])
    # An AI's seat is never above its human's: the platform gives a seat at most its sponsor's role
    # (POST /account/worlds/{world_id}/seats, role: "At most your own role"; the owner may give any).
    seat_role = {e["key"]: (e.get("seat") or {}).get("role") for e in rows}
    for e in rows:
        ai_of = (e.get("seat") or {}).get("ai_of")
        mine, theirs = seat_role[e["key"]], seat_role.get(ai_of)
        if ai_of in ids and mine in RANK and theirs in RANK and RANK[mine] > RANK[theirs]:
            problems.append(f"plan element {e['key']!r}, seat: {names[e['key']]}'s role {mine} is above its "
                            f"human {names[ai_of]}'s ({theirs}); an AI's seat is at most its human's role")
    # People grouped by role, every AI by name with its role word and its human; past NAMED seats in
    # all (people and AIs), a role's names and the AIs become counts (the roster holds them), so a big
    # team keeps the charter a page. The owner is always named.
    named = sum(len(n) for n in people.values()) + len(ais) <= NAMED

    def count(k, word):
        return f"{k} {word}" + ("s" if k != 1 else "")
    seats = [(f"{', '.join(n)} ({ROLES[r]})" if named or r == "owner" else count(len(n), ROLES[r]))
             for r, n in people.items() if n]
    seats += ais if named else ([count(len(ais), "AI")] if ais else [])
    who_is_here = ("Seated at setup: " + "; ".join(seats) + ".") if seats else "No one was seated at setup."

    # Where the copies go, and the paths an agent there reads.
    copies = plan.get("copies", "none")
    copy_root = None if copies == "none" else (out if copies == "world" else Path(copies))
    seen_from = copy_root if copy_root is not None else out
    world_folder = shown(out, seen_from)
    world_folder = "./" if world_folder == "." else world_folder.rstrip("/") + "/"
    rel_charter = shown(out / "elements" / "law" / "charter.json", seen_from)
    charter_route = rel_charter + (", or GET /law?supertype=Charter online" if online else "")
    agents_line = AGENTS_LINE.format(world_name=w["name"], charter_route=charter_route, skill_name=skill_name)

    values = dict(plan.get("values", {}))
    values.update(world_name=w["name"], world_slug=world_slug, charter_id=charter_id, skill_id=skill_id,
                  skill_name=skill_name, today=today, today_day=str(day_number(today)),
                  world_folder=world_folder, who_is_here=who_is_here, roster=ROSTER[placement],
                  proposer_id=PROPOSER[placement], agents_line=agents_line, world_id=charter_of)
    if online:
        values["server_world_id"] = server_id
    if extras:
        values["prefix"] = prefix
        for kind, _, _ in extras:
            values[f"{kind}_skill_id"] = extra_ids[kind]
            values[f"{kind}_skill_name"] = f"{prefix}-{kind}"

    def fill(text, where, first_line=1):
        """Every placeholder filled; a line that still holds `{{` after filling is a problem."""
        def sub(m):
            name = m.group(1)
            if name.startswith("id:"):
                return ids.get(name[3:], m.group(0))
            return str(values[name]) if name in values else m.group(0)
        done = PH.sub(sub, text)
        for n, ln in enumerate(done.split("\n"), first_line):
            if "{{" in ln:
                left = ln[ln.index("{{"):][:40]
                problems.append(f"{where}, line {n}: {left!r} is not filled")
        return done

    def fill_template(name):
        rows_ = template(pack / name, placement, problems)
        return "\n".join(fill(ln, f"packs/{plan['pack']}/{name}", src) for src, ln in rows_) + "\n"

    def fields_of(raw, where):
        body = {}
        for k, v in raw.items():
            if k.startswith("x_charter_"):  # the reading-aid mark is the writer's, by the pair
                problems.append(f"{where}, {k}: the writer sets x_charter_of on a reading aid itself; "
                                f"a plan never names an x_charter_ key")
                continue
            if isinstance(v, str):
                v = fill(v, f"{where}, {k}")  # fill first: "day:{{today}}" is a date once filled
                m = DAY.match(v)
                body[k] = day_number(m.group(1)) if m else v
            else:
                body[k] = v
        return body

    def links_of(raw, where):
        body = {}
        for field, target in (raw or {}).items():
            keys = target if isinstance(target, list) else [target]
            missing = [k for k in keys if k not in ids]
            if missing:
                problems.append(f"{where}.{field}: no element with key {missing}")
                continue
            seated = [k for k in keys if k in from_seat]
            if seated:
                problems.append(f"{where}.{field}: online, {', '.join(names[k] for k in seated)} gets a "
                                f"Character from its seat, after setup; link it on its first visit")
                continue
            body[field] = [ids[k] for k in keys] if isinstance(target, list) else ids[target]
        return body

    charter_text = fill_template("charter.md")
    if len(charter_text) >= CHARTER_MAX:
        problems.append(f"charter: {len(charter_text)} characters, the budget is under {CHARTER_MAX}")

    over = []  # a skill at or over SKILL_MAX, a description over DESCRIPTION_MAX: written, and a note says so

    def skill_of(template_name, label):
        """A filled skill text, checked: front matter name and description only; its sizes noted. The
        description line is written by double_quoted() from the filled description, so a YAML reader
        reads exactly the filled text, whatever the names hold."""
        where, lines, fence, description = f"packs/{plan['pack']}/{template_name}", [], 0, None
        for src, ln in template(pack / template_name, placement, problems):
            fence += ln == "---"
            if fence == 1 and ln.startswith("description: "):
                description = fill(ln[len("description: "):], where, src)
                lines.append("description: " + double_quoted(description))
            else:
                lines.append(fill(ln, where, src))
        text = "\n".join(lines) + "\n"
        if len(text) >= SKILL_MAX:
            over.append(f"note: the {label} is {len(text)} characters, and the packs aim for under "
                        f"{SKILL_MAX}; it is written whole, and nothing needs changing")
        if description is not None and len(description) > DESCRIPTION_MAX:
            over.append(f"note: the {label}'s description is {len(description)} characters, and the Agent "
                        f"Skills specification gives {DESCRIPTION_MAX}")
        fm_ = re.match(r"---\n(.*?)\n---\n", text, re.S)
        keys = [ln.split(":", 1)[0] for ln in fm_.group(1).split("\n") if ln and not ln.startswith(" ")] if fm_ else []
        if keys != ["name", "description"]:
            problems.append(f"{label} front matter: keys {keys}, want exactly name and description")
        return text, fm_

    skill_text, fm = skill_of("skill.md", "world skill")
    extra_texts = {kind: skill_of(f"{kind}.md", f"{kind} skill") for kind, _, _ in extras}

    files = {}  # relative path -> text
    world_json = {"id": world_id, "name": w["name"], "description": fill(w.get("description", ""), "plan world, description"),
                  "format_version": FORMAT_VERSION, "charter": charter_id,
                  "time_basic_unit": "Day", "time_format_names": ["Day", "Week", "Year"],
                  "time_format_equivalents": [1, 7, 365], "time_range_min": 0,
                  "time_range_max": day_number("2099-12-31"), "time_current": day_number(today)}
    if online and not plan.get("repo"):
        world_json["api"] = {"world_id": server_id}  # the key stays in .env (start's Connect an account), never here
    files["world.json"] = dump(world_json)

    charter = {"id": charter_id, "name": "Charter", "supertype": "Charter", "description": charter_text,
               "date": day_number(today)}
    charter.update(links_of(plan.get("charter", {}).get("links"), "charter"))
    charter["x_checks_rules"] = checks_of(plan.get("charter", {}), pack, problems)
    charter["x_charter_of"] = charter_of
    files["elements/law/charter.json"] = dump(charter)
    skill = {"id": skill_id, "name": f"{w['name']} world skill", "supertype": "Skill", "description": skill_text,
             "utility": fill(plan.get("skill", {}).get("utility", "How an agent reaches this world. Copy the "
                             "description, whole, to where your harness reads skills, as SKILL.md."), "plan skill, utility")}
    # A name the slug drops whole (no letters it keeps) names the skill files by the world skill's id,
    # as an element's file takes its id; in a one-skill pack the name `ow-` is refused above.
    file_slug = world_slug or skill_id
    origin = {}  # a written file's path -> (the plan key, its value) that named it
    origin[f"elements/object/{file_slug}-skill.json"] = ("world.slug", file_slug)
    origin.update({f"elements/object/{file_slug}-{kind}-skill.json": ("world.slug", file_slug) for kind, _, _ in extras})
    files[f"elements/object/{file_slug}-skill.json"] = dump(skill)
    for kind, label, utility in extras:
        files[f"elements/object/{file_slug}-{kind}-skill.json"] = dump(
            {"id": extra_ids[kind], "name": f"{w['name']} {label}", "supertype": "Skill",
             "description": extra_texts[kind][0],
             "utility": utility + " Copy the description, whole, to where your harness reads skills, as SKILL.md."})

    counts = {"law": 1, "object": 1 + len(extras)}
    taken = set(files)
    for e in rows:
        if e["key"] in from_seat:
            continue
        where = f"plan element {e['key']!r}"
        body = {"id": ids[e["key"]]}
        body.update(fields_of(e["fields"], where))
        body.update(links_of(e.get("links"), where))
        if e["key"] in seat_of:
            body["x_seat"] = seat_of[e["key"]]
        t = e["type"]
        if is_reading_aid(t, body.get("supertype")):
            if t.strip(WHITE_SPACE).casefold() == "law":  # newest-wins would make it supersede the pack's
                problems.append(f"{where}: the pack writes the Charter; a plan row cannot be a second one")
                continue
            body["x_charter_of"] = charter_of
        name = slug(body.get("name", "")) or ids[e["key"]]
        rel = f"elements/{t}/{name}--{ids[e['key']][-8:]}.json" if name != ids[e["key"]] else f"elements/{t}/{name}.json"
        if rel in taken:
            rel = f"elements/{t}/{ids[e['key']]}.json"
        taken.add(rel)
        files[rel] = dump(body)
        origin[rel] = (f"plan element {e['key']!r}, type", t)
        counts[t] = counts.get(t, 0) + 1

    def copy_of(text, fm_, object_id):
        """The harness copy: the text with one line after the front matter naming where it came from."""
        if not fm_:
            return text
        head = fm_.group(0)
        return (head + f"<!-- copied from the world: Object {object_id}; updated_at none yet "
                f"(made by the set-up skill on {today}) -->\n" + text[len(head):])

    skills = [(skill_name, copy_of(skill_text, fm, skill_id))]
    for kind, _, _ in extras:
        skills.append((f"{prefix}-{kind}", copy_of(*extra_texts[kind], extra_ids[kind])))
    # Harnesses read .agents/skills/ and .claude/skills/ from the directory they run in up to the
    # repository root, never from a sub-folder: the copies go to that root, and into the world folder
    # only when the world folder is that root ("world").
    copy_paths = []  # (path, text)
    if copy_root is not None:
        for name_, text_ in skills:
            for harness in (".agents", ".claude"):
                p = copy_root / harness / "skills" / name_ / "SKILL.md"
                if p.exists():
                    problems.append(f"{p} exists: a copy is the user's; not overwritten")
                copy_paths.append((p, text_))
    line, line_files, line_print = None, [], None
    if plan.get("agents_md") and copy_root is not None:
        line = agents_line
        if copy_root.resolve() == Path.home().resolve():
            line_print = line  # no harness reads a home AGENTS.md as a project's: the user places the line
        else:
            line_files.append(copy_root / "AGENTS.md")
            if (copy_root / "CLAUDE.md").exists():  # Claude Code reads AGENTS.md only when no CLAUDE.md exists
                line_files.append(copy_root / "CLAUDE.md")
    files[".gitattributes"] = GITATTRIBUTES  # every pack, every placement: one place
    # The copies' root is a repository of its own when it is not the world folder: its root files
    # (AGENTS.md, the skill copies) want the same line-ending rule, or git on an autocrlf machine
    # rewrites them (ruled 2026-10-22). The repository's own .gitattributes stands when it has one.
    root_attrs = None
    if copy_root is not None and copy_root.resolve() not in (out.resolve(), Path.home().resolve()):
        if not (copy_root / ".gitattributes").exists():
            root_attrs = copy_root / ".gitattributes"
    if plan.get("repo"):
        files[".gitignore"] = GITIGNORE

    # Nothing is written outside the folders the run is given, whatever value reaches a path: the world
    # folder's files under OUT_FOLDER; the copies, the AGENTS.md line and the root's .gitattributes under
    # the copies' root the plan names. The paths are read as written, never through a link: a project
    # whose .claude is a link to another folder is the user's own. (The --bulk file is the caller's.)
    targets = [(out / rel, out, origin.get(rel, ("OUT_FOLDER", str(out)))) for rel in files]
    targets += [(p, copy_root, ("copies", copies)) for p in [p for p, _ in copy_paths] + line_files
                + ([root_attrs] if root_attrs is not None else [])]
    for p, root, (key, value) in targets:
        if outside(p, root):
            problems.append(f"{key} {value!r} would write {os.path.abspath(p)}, outside {os.path.abspath(root)}; "
                            f"the writer writes nothing outside the folders it is given")

    if not problems:  # the net: nothing this run would write still holds a `{{`
        outputs = dict(files)
        outputs.update({str(p): t for p, t in copy_paths})
        if line:
            outputs["the AGENTS.md line"] = line + "\n"
        for rel, text in outputs.items():
            for n, ln in enumerate(text.split("\n"), 1):
                if "{{" in ln:
                    problems.append(f"{rel}, line {n}: {ln[ln.index('{{'):][:40]!r} is not filled")

    # Every file's bytes are made, and encoded, before the first one is written.
    writes, line_done = [], []  # (path, bytes, append)
    if not problems:
        writes = [(out / rel, text, False) for rel, text in files.items()]
        writes += [(p, t, False) for p, t in copy_paths]
        if root_attrs is not None:
            writes.append((root_attrs, GITATTRIBUTES, False))
        for p in line_files:  # the user's own file: never overwritten, the line appended once
            if not p.exists():
                writes.append((p, line + "\n", False))
                line_done.append(f"{p}: written")
                continue
            try:
                with open(p, encoding="utf-8", newline="") as fh:
                    old = fh.read()
            except UnicodeDecodeError:
                problems.append(f"copies {copies!r}: {p} is not UTF-8 text, so the AGENTS.md line cannot be "
                                f"appended to it; save it as UTF-8, or set agents_md to false")
                continue
            if line in old:
                line_done.append(f"{p}: holds the line already")
                continue
            nl = "\r\n" if "\r\n" in old else "\n"
            writes.append((p, ("" if not old or old.endswith("\n") else nl) + line + nl, True))
            line_done.append(f"{p}: the line appended")
        if bulk:
            items = [{"type": rel.split("/")[1], "element": json.loads(text)}
                     for rel, text in files.items() if rel.startswith("elements/")]
            writes.append((bulk, json.dumps({"items": items}, ensure_ascii=True, indent=1) + "\n", False))
        encoded = []
        for p, text, append in writes:
            try:
                encoded.append((p, text.encode("utf-8"), append))
            except UnicodeEncodeError as err:
                problems.append(f"{p}: {err.reason} at character {err.start}; nothing is written")
        writes = encoded

    if problems:
        for p in problems:
            print("REFUSED", p, file=sys.stdout or sys.stderr)
        print(f"nothing written; {len(problems)} problem(s)", file=sys.stdout or sys.stderr)
        return 1

    # From the first folder the run makes to its last line of output, every act is the journal's: on any
    # error, or an interrupt, the journal is undone, last act first, and the run refuses (an interrupt
    # is let through after the undo).
    journal = Journal()
    state["writing"] = True
    try:
        # Every folder the run writes into is made before the first file, each an act of the journal.
        # When one cannot be made (a name the system refuses, a file where a folder goes), the journal
        # is undone and the run refuses, leaving nothing behind.
        owner = {}  # each folder to make -> the plan key and value that put it there
        for p, _, _ in writes:
            key = (("--bulk", str(bulk)) if bulk is not None and p == bulk else
                   ("OUT_FOLDER", str(out)) if not outside(p, out) else ("copies", copies))
            owner.setdefault(Path(os.path.abspath(p.parent)), key)
        failed = None
        for folder in sorted(owner, key=lambda f: len(f.parts)):
            for step in [*reversed(folder.parents), folder]:
                if step.is_dir():
                    continue
                why = "a file is there" if step.exists() else None
                if why is None:
                    try:
                        journal.mkdir(step)
                        continue
                    except OSError as err:
                        why = err.strerror or str(err)
                key, value = owner[folder]
                failed = f"{key} {value!r}: the folder {step} cannot be made ({why})"
                break
            if failed:
                break
        if failed:  # the words say "nothing is written" only when the journal's two lists are empty
            journal.refused = True
            try:
                journal.undo()
            finally:  # an interrupt in the undo too: said from the journal, then it goes on
                say_refusal(refusal(journal, f"REFUSED {failed}; nothing is written\nnothing written; 1 problem(s)\n",
                                    f"REFUSED {failed}; the writer took back the folders it had made, but for "))
            return 1

        # The summary is composed whole before the first file, and printed in one write after the last,
        # as the run's last act: a caller never reads a line about files a later failure took back.
        summary = []
        if bulk and len(items) > 1000:
            summary.append(f"bulk: {len(items)} items, over 1000 a request: split it before sending")
        n = sum(1 for r in files if r.startswith("elements/"))
        summary.append(f"wrote {out} ({placement}): world.json and {n} elements "
                       f"({', '.join(f'{t} {c}' for t, c in sorted(counts.items()))})")

        def sized(n):  # two facts and no comparison, true at any size: the skill's length and the aim
            return f"{n} characters, the packs aim for under {SKILL_MAX}"
        summary.append(f"charter {len(charter_text)} of under {CHARTER_MAX} characters; "
                       f"world skill {sized(len(skill_text))}; skill name {skill_name}")
        for kind, _, _ in extras:
            summary.append(f"{kind} skill {sized(len(extra_texts[kind][0]))}; skill name {prefix}-{kind}")
        summary += over
        if not ais:
            summary.append("note: no AI is seated (question 4's default is one, the user's): its AI will find no Character")
        for k in sorted(from_seat):
            summary.append(f"seat: {names[k]}'s Character comes from its seat (Make a seat, its own new Character)")
        if online and plan.get("repo"):
            summary.append("online in a repository: world.json carries no api block; the server id is in the world skill")
        for p, _ in copy_paths:
            summary.append(f"copy: {p}")
        for d in line_done:
            summary.append(f"agents line: {d}")
        if line_print:
            summary.append(f"agents line, for the user to place (the copies went to a home folder): {line_print}")
        if bulk:
            summary.append(f"bulk body: {bulk} ({n} items)")

        for p, data, append in writes:
            journal.write(p, data, append)
        say("".join(line + "\n" for line in summary))
        return 0
    except BaseException as err:  # an interrupt too: undone, then let through
        if journal.refused:  # the folder pass refused and said so already; only its interrupt is left
            raise
        code = undone(journal, err)
        if not isinstance(err, Exception):
            raise
        return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
