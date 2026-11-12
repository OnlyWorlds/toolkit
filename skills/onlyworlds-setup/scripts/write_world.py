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
characters is written too, with a note giving its length and the specification's number. It never
deletes anything.

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
FORMAT_VERSION = "0.3.21"
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


def line_breaker(value):
    """The first line break or control character in a text (Unicode's Cc, and U+2028, U+2029), or None."""
    return next((c for c in value if ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F or c in "\u2028\u2029"), None)


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
    """True when `path`, resolved, does not lie under `root`, resolved."""
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return False
    except ValueError:
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


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


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
    bulk_arg = argv[argv.index("--bulk") + 1] if "--bulk" in argv and argv.index("--bulk") + 1 < len(argv) else None
    bulk = Path(bulk_arg) if bulk_arg else None
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and not (bulk_arg and i == argv.index("--bulk") + 1)]
    if len(args) != 2:
        sys.exit(__doc__.split("\n\n")[1])
    plan = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    out = Path(args[1])
    problems = []
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} already holds files: this script only writes new folders")
    pack = PACKS / plan["pack"]
    if not (pack / "PACK.md").exists():
        sys.exit(f"no pack {plan['pack']!r} under {PACKS}")

    # A plan value the writer puts on a line of a text (the charter, a skill, the AGENTS.md line, a
    # path) holds no line break and no control character: refused first, since the checks below would
    # trip on it. The free texts that land only in an element's JSON (world.description, skill.utility,
    # a field's description) keep their line breaks.
    w = plan["world"]
    one_line = [("world.name", w.get("name")), ("world.slug", w.get("slug")), ("prefix", plan.get("prefix")),
                ("copies", plan.get("copies")), ("today", plan.get("today"))]
    one_line += [(f"values.{k}", v) for k, v in plan.get("values", {}).items()]
    humans = {(e.get("seat") or {}).get("ai_of") for e in plan["elements"]}
    for e in plan["elements"]:  # the seats and their humans reach the charter's "Who is here"
        seat = e.get("seat") or {}
        if seat or e["key"] in humans:
            one_line.append((f"plan element {e['key']!r}, name", e.get("fields", {}).get("name")))
        if seat.get("ai_of") is not None:
            one_line.append((f"plan element {e['key']!r}, supertype", e.get("fields", {}).get("supertype")))
    for label, v in one_line:
        c = line_breaker(str(v)) if v is not None else None
        if c:
            v = str(v) if len(str(v)) <= 60 else str(v)[:60] + "..."
            problems.append(f"{label} {v!r}: holds a line break or a control character (U+{ord(c):04X}), "
                            f"and the writer puts this value on one line of a text")
    if problems:
        for p in problems:
            print("REFUSED", p)
        print(f"nothing written; {len(problems)} problem(s)")
        return 1

    online = plan.get("online")
    placement = "online" if online else "folder"
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
        problems.append(f"skill name {skill_name!r}: lowercase letters, digits and hyphens, 64 at most")
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
    # the copies' root the plan names. (The --bulk file is the caller's own path.)
    targets = [(out / rel, out) for rel in files] + [(p, copy_root) for p, _ in copy_paths]
    targets += [(p, copy_root) for p in line_files + ([root_attrs] if root_attrs is not None else [])]
    for p, root in targets:
        if outside(p, root):
            problems.append(f"{Path(p).resolve()}: outside {Path(root).resolve()}, the folder it is written in; "
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

    if problems:
        for p in problems:
            print("REFUSED", p)
        print(f"nothing written; {len(problems)} problem(s)")
        return 1

    for rel, text in files.items():
        write(out / rel, text)
    for p, t in copy_paths:
        write(p, t)
    if root_attrs is not None:
        write(root_attrs, GITATTRIBUTES)
    line_done = []
    for p in line_files:  # the user's own file: never overwritten, the line appended once
        if not p.exists():
            write(p, line + "\n")
            line_done.append(f"{p}: written")
            continue
        with open(p, encoding="utf-8", newline="") as fh:
            old = fh.read()
        if line in old:
            line_done.append(f"{p}: holds the line already")
            continue
        nl = "\r\n" if "\r\n" in old else "\n"
        with open(p, "a", encoding="utf-8", newline="") as fh:
            fh.write(("" if not old or old.endswith("\n") else nl) + line + nl)
        line_done.append(f"{p}: the line appended")
    if bulk:
        items = [{"type": rel.split("/")[1], "element": json.loads(text)}
                 for rel, text in files.items() if rel.startswith("elements/")]
        if len(items) > 1000:
            print(f"bulk: {len(items)} items, over 1000 a request: split it before sending")
        write(bulk, json.dumps({"items": items}, ensure_ascii=True, indent=1) + "\n")
    n = sum(1 for r in files if r.startswith("elements/"))
    print(f"wrote {out} ({placement}): world.json and {n} elements "
          f"({', '.join(f'{t} {c}' for t, c in sorted(counts.items()))})")
    def sized(n):  # two facts and no comparison, true at any size: the skill's length and the aim
        return f"{n} characters, the packs aim for under {SKILL_MAX}"
    print(f"charter {len(charter_text)} of under {CHARTER_MAX} characters; "
          f"world skill {sized(len(skill_text))}; skill name {skill_name}")
    for kind, _, _ in extras:
        print(f"{kind} skill {sized(len(extra_texts[kind][0]))}; skill name {prefix}-{kind}")
    for note in over:
        print(note)
    if not ais:
        print("note: no AI is seated (question 4's default is one, the user's): its AI will find no Character")
    for k in sorted(from_seat):
        print(f"seat: {names[k]}'s Character comes from its seat (Make a seat, its own new Character)")
    if online and plan.get("repo"):
        print("online in a repository: world.json carries no api block; the server id is in the world skill")
    for p, _ in copy_paths:
        print(f"copy: {p}")
    for d in line_done:
        print(f"agents line: {d}")
    if line_print:
        print(f"agents line, for the user to place (the copies went to a home folder): {line_print}")
    if bulk:
        print(f"bulk body: {bulk} ({n} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
