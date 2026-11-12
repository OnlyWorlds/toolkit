"""The set-up skill's writer, on every pack, in three placements (round 2).

    python testing/setup-493/test_write_world.py [-v]

Each pack's plan (plans/<pack>.json, the rows of that pack's seed.md) is written three ways:
a plain folder (the world in <project>/world, the copies at <project>), a repository (the world
folder IS the repository, copies "world", "repo": true) and online (as the plain folder, with
"online": {"world_id": <a server id>}). Then the checks, one test per finding of the first
harness trial (2026-10-22):

1. every placeholder is filled before a shape test (a `day:{{today}}` date lands as its day
   number), the folder lint reads zero problems, and a `{{` left after filling refuses the
   write with the file and line named;
2. the world skill speaks for its placement: a folder world's names the folder and no API route
   or id-as-address; an online world's names the server world id, never the minted one;
3. the charter's "Who is here" names everyone seated at setup, the AI with its role word, and
   the keeper; a folder world holds the AI's Character (supertype Agent);
4. the charter's roster line: the folder's own Characters in a folder world, GET /members online;
5. the AGENTS.md line and the world skill's courtesy line are one sentence;
6. every pack writes the same .gitattributes, in every placement;
7. every pack's world skill holds the daily sweep, word for word, and the
   charter-order sentence with its reason, once each; only the company pack,
   whose lines keep a Next line, keeps the sweep's clause about stale lines;
8. the company pack writes the Guide "Start here", a Welcome message to a person, and the
   charter's Next-line sentence;
9. every pack's charter file carries the checks slot `x_checks_rules`: empty only in a pack
   with no rule; the company pack ships three rules (the Next line and the two room marks), the
   software-project pack two (the room marks), the workshop pack one (a work item's room mark),
   each taken from schema-dist's published fixture (9f, skipped with its reason when the
   fixture is not found) and each sentence in its charter; it reaches
   the bulk body, a plan's list replaces the pack's, and the Python package's doctor (0.24.0 or
   newer, when installed) applies it;
10. the company pack answers the five points a cold visit to a live company world guessed
    (`cold-visit-checklist.md`);
11. the company pack names who writes the board (the owner and the co-builders) and steers
    everyone to keep a Note about themselves, in the charter and the world skill, and a Note
    lands settled beside the messages;
12. the reading aids carry the charter profile's mark `x_charter_of` (schema-dist
    `profiles/charter.md`): the Charter in every pack and the company pack's Guide, each the id of
    the world it is in (world.json's for a folder, the server's online), in the files and the bulk
    body; no other element carries the key; a Domain matches by its pair trimmed and folded, a
    near-word does not; a plan that names an `x_charter_` key, or a plan row with the pair
    law/Charter, is refused;
13. the two team packs (company, software-project) land three skills under the plan's prefix,
    `<prefix>-start`, `-design` and `-work`, each an Object with its two copies, each under the
    budget and speaking for its placement; the work skill carries the report profile's keys; a
    team pack's plan without a prefix is refused;
14. a real team fits: each team pack written at 2, 5, 8, 12 and 20 seats (and 8 with six AIs, the
    last size the charter names every seat) keeps CHARTER_ROOM characters under the charter budget;
    and no pack's charter is longer than 5.9.5 (ac34e55) filled it, for the test's own plans (14c)
    and for one owner with a 31-character name and seven AIs of theirs (14b);
15. no route in a filled online skill carries a query value with a raw space;
16. the writer refuses an AI seat whose role is above its human's;
18. a skill's size never refuses a plan: a world skill (18a) and a team pack's work skill (18b)
    filled to SKILL_MAX characters or more (the packs aim for under it) are written, exit 0, with one
    note naming each; at exactly SKILL_MAX - 1, SKILL_MAX and SKILL_MAX + 1 the size line and the note
    are true (18d); a charter over its budget is still refused (18c), at exactly CHARTER_MAX too, and
    one of CHARTER_MAX - 1 is written (18e);
19. a plan's own text never breaks a written skill or leaves the folder: in every pack and every skill
    template, names holding a colon and a space, a trailing colon, a space and a hash, a run of dashes,
    a double quote or a backslash give a front matter whose description, read by PyYAML (and by
    skills-ref's parser where it is installed), is the filled text (19a); a tab or a control
    character in any plan value written into a text is refused, the key named, nothing written, a
    line break only where its place is one line, while a value whose places are all paragraphs and
    the free texts that land only in JSON keep theirs (19b); a world slug or an element type that
    climbs out of the world folder is refused, nothing written anywhere, and the writer's own check
    refuses a copy path that climbs out of its root (19c); a description of 1,024 characters is
    written with no note, one of 1,025 with a note giving its length and the specification's 1,024
    (19d); a world named in a script the slug drops whole, with no slug, names a team pack's skill
    files by the world skill's id, and a one-skill pack still refuses the name `ow-` (19e); a
    project whose .claude is a link is written through (19f); an element's type is one of the 22
    (19g); a plan the writer refuses leaves the folder empty, also for a lone surrogate, a value
    that is no string, a setup day not written YYYY-MM-DD and a plan in a shape the writer does not
    read (19h); every folder is made before the first file, and a copies root that cannot be made
    leaves nothing behind (19i);
20. a run that stops after its first act takes itself back: for one plan of each pack, every act
    made to fail in turn (before it, half way through its bytes, by an interrupt) and a failure after
    the last file leave the output folder's parent and the copies' parent byte for byte as before,
    an appended AGENTS.md and CLAUDE.md and a written-over bulk file among them (20a); a read-only
    AGENTS.md or CLAUDE.md (20b) and a --bulk path that is a folder (20c) refuse, nothing left; the
    bulk file written over gets its bytes back (20d); an undo that cannot remove a file says so,
    each path named (20e); an error of the writer's own before its first act blames nobody (20f); an
    interrupt at any step of the undo still ends the run, and every path left is named (20g); an error
    of any kind in the undo is named and the undo goes on (20h); the summary is one write, the run's
    last act (20i); a file this run changed twice is described by what it holds (20j); a folder pass
    whose undo leaves a folder never says that nothing is written (20k).

Output goes to a fresh folder under <repo>/.scratch/tests/ (OW_SETUP_TEST_OUT to override);
nothing is deleted. The lint is schema-dist's walk/lint_folder.py, from the schema-dist checkout
beside this repository's main checkout, found through git from a worktree too (OW_LINT to point
at another).
Python 3, stdlib only.
"""
import io
import json
import os
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WRITER = REPO / "skills" / "onlyworlds-setup" / "scripts" / "write_world.py"
PLANS = Path(__file__).resolve().parent / "plans"
PACKS = ["company", "ai-home", "governance", "workshop", "software-project"]
PLACEMENTS = ["folder", "repo", "online"]
def default_lint():
    """schema-dist's lint beside the toolkit's MAIN checkout: from a worktree too, since git's
    common dir is the main checkout's .git (a worktree's own parent need not hold schema-dist)."""
    roots = [REPO]
    try:
        common = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--path-format=absolute",
                                 "--git-common-dir"], capture_output=True, text=True).stdout.strip()
        if common:
            roots.insert(0, Path(common).parent)
    except OSError:
        pass
    found = [r.parent / "schema-dist" / "walk" / "lint_folder.py" for r in roots]
    return next((p for p in found if p.exists()), found[0])


LINT = Path(os.environ.get("OW_LINT") or default_lint())
SERVER_ID = "019a0b0c-0d0e-7f00-8a00-5e2be2000001"  # stands for the id onlyworlds.com gave the empty world
GITATTRIBUTES = ("* text=auto eol=lf\n*.png binary\n*.jpg binary\n*.jpeg binary\n*.gif binary\n"
                 "*.webp binary\n*.pdf binary\n*.zip binary\n*.owworld binary\n")
# The daily sweep: one text, copied word for word from a live work world's own skill, the same
# in every pack. A change to it is a change at its source first.
DAILY_SWEEP = (
    "**What a visit gives your human.** A visit always ends in a few lines to your human, never in a "
    "silent \"ok\": what is new for them (messages, with who wrote and what it asks), which of the lines "
    "they keep are over two weeks old or past their `Next: ... by` date, and what is asked of them. "
    "Nothing new and nothing stale is said in those words. A scheduled or daily read gives the same "
    "digest, then offers to go deeper: query the elements the new messages touch, read enough to see "
    "the whole picture, and talk it through with your human before writing anything.")
LINES_CLAUSE = "which of the lines they keep are over two weeks old or past their `Next: ... by` date, "
ORDER = ("This order is in the skill itself because harnesses differ on whether an `AGENTS.md` line "
         "or a skill is read first.")
API_ROUTE = re.compile(r"onlyworlds\.com/(api|mcp)|\b(GET|POST|PATCH|PUT|DELETE) /")
FIXTURE = Path(os.environ.get("OW_CHECKS_FIXTURE") or LINT.parent.parent / "profiles" / "checks.fixture.json")
# The room a filled world skill keeps under the size the packs aim for (the writer's SKILL_MAX, read
# from the writer), so a company's own names rarely bring a skill to it (the writer writes one of
# SKILL_MAX or more whole, and says so: test 18).
ROOM = 500
# The room a team pack's filled charter keeps under the writer's budget at every team size (test 14).
CHARTER_ROOM = 300


def visit_steps(text):
    """The numbered lines of the visit list that holds "2. The Charter, whole.": from its "1. " line
    to the first blank line after the Charter step, lines that are not numbered left out."""
    lines = text.split("\n")
    at = lines.index("2. The Charter, whole.")
    start = max(i for i in range(at) if lines[i].startswith("1. "))
    end = next((i for i in range(at, len(lines)) if not lines[i].strip()), len(lines))
    return [ln for ln in lines[start:end] if re.match(r"\d+\. ", ln)]
OUT = Path(os.environ.get("OW_SETUP_TEST_OUT") or
           REPO / ".scratch" / "tests" / time.strftime("%Y%m%d-%H%M%S"))


def size_line(label, size, budget, name):
    """The writer's size line for one skill: its length and the packs' aim, no comparison."""
    return f"{label} {size} characters, the packs aim for under {budget}; skill name {name}"


def size_note(label, size, budget):
    """The note the writer prints for a skill of SKILL_MAX characters or more."""
    return (f"note: the {label} is {size} characters, and the packs aim for under {budget}; it is "
            f"written whole, and nothing needs changing")


def ai_keys(plan):
    return {e["key"] for e in plan["elements"] if (e.get("seat") or {}).get("ai_of")}


def variant(plan, placement, root):
    """The plan for one placement, and the world folder it writes."""
    p = json.loads(json.dumps(plan))
    if placement == "repo":
        world, p["copies"], p["repo"] = root, "world", True
        return p, world
    world, p["copies"], p["repo"] = root / "world", str(root), False
    if placement == "online":
        p["online"] = {"world_id": SERVER_ID}
        ais = ai_keys(p)
        kept = []
        for e in p["elements"]:  # online, an AI's Character comes from its seat: nothing links it yet
            if e["key"] not in ais and (e.get("links") or {}).get("actor") in ais:
                continue
            links = {}
            for f, t in (e.get("links") or {}).items():
                if isinstance(t, list):
                    links[f] = [k for k in t if k not in ais]
                elif t not in ais:
                    links[f] = t
            if e.get("links") is not None:
                e["links"] = links
            kept.append(e)
        p["elements"] = kept
    return p, world


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


class Run:
    """One writer run: its plan, its folders, what it printed."""

    def __init__(self, pack, placement):
        self.pack, self.placement = pack, placement
        self.plan_src = json.loads(read(PLANS / f"{pack}.json"))
        root = OUT / f"{pack}-{placement}"
        self.plan, self.world = variant(self.plan_src, placement, root)
        self.copy_root = self.world if placement == "repo" else root
        plan_path = OUT / "plans" / f"{pack}-{placement}.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(self.plan, indent=1), encoding="utf-8")
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(self.world),
                            "--bulk", str(OUT / "plans" / f"{pack}-{placement}-bulk.json")],
                           capture_output=True, text=True, encoding="utf-8")
        self.code, self.out = r.returncode, r.stdout + r.stderr

    @property
    def world_json(self):
        return json.loads(read(self.world / "world.json"))

    def elements(self):
        for p in sorted((self.world / "elements").glob("*/*.json")):
            yield p, json.loads(read(p))

    def charter(self):
        return json.loads(read(self.world / "elements" / "law" / "charter.json"))["description"]

    def skill(self):
        slug = self.plan["world"]["slug"]
        return json.loads(read(self.world / "elements" / "object" / f"{slug}-skill.json"))["description"]

    @property
    def skill_name(self):
        """The world skill's name: <prefix>-start in a three-skill pack, else ow-<slug>."""
        return f"{self.plan['prefix']}-start" if self.plan.get("prefix") else "ow-" + self.plan["world"]["slug"]

    def extra_skills(self):
        """A three-skill pack's design and work skills: {kind: (Object body, its name)}."""
        slug, out = self.plan["world"]["slug"], {}
        for kind in ("design", "work"):
            p = self.world / "elements" / "object" / f"{slug}-{kind}-skill.json"
            if p.exists():
                out[kind] = (json.loads(read(p)), f"{self.plan['prefix']}-{kind}")
        return out

    def written(self):
        """Every file the run wrote: the world folder, the copies, the AGENTS.md line."""
        files = [p for p in self.world.rglob("*") if p.is_file()]
        for h in (".agents", ".claude"):
            files += list((self.copy_root / h).rglob("SKILL.md"))
        if (self.copy_root / "AGENTS.md").exists():
            files.append(self.copy_root / "AGENTS.md")
        return sorted(set(files))


RUNS = {}


def setUpModule():
    OUT.mkdir(parents=True, exist_ok=True)
    for pack in PACKS:
        for placement in PLACEMENTS:
            RUNS[pack, placement] = Run(pack, placement)


class SetupWriter(unittest.TestCase):

    def each(self, check):
        for (pack, placement), run in RUNS.items():
            with self.subTest(pack=pack, placement=placement):
                self.assertEqual(run.code, 0, run.out)
                check(run)

    def test_1a_dates_filled_and_lint_clean(self):
        self.assertTrue(LINT.exists(), f"no lint at {LINT}: set OW_LINT")
        def check(run):
            for p, body in run.elements():
                for k, v in body.items():
                    self.assertFalse(isinstance(v, str) and v.startswith("day:"), f"{p.name}.{k} = {v!r}")
            lint = subprocess.run([sys.executable, str(LINT), str(run.world)], capture_output=True,
                                  text=True, encoding="utf-8")
            last = lint.stdout.strip().splitlines()[-1] if lint.stdout.strip() else ""
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
            self.assertRegex(last, r": 0 problems$")
        self.each(check)

    def test_1b_no_brace_written_anywhere(self):
        def check(run):
            for p in run.written():
                self.assertNotIn("{{", read(p), str(p))
        self.each(check)

    def test_1c_leftover_brace_refused_with_file_and_line(self):
        plan = json.loads(read(PLANS / "company.json"))
        org = next(e for e in plan["elements"] if e["key"] == "org")
        org["fields"]["description"] = "Source: the test · as of {{today}}\nSecond line.\nMade by {{ Org }}."
        plan_path = OUT / "plans" / "leftover.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "leftover"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"REFUSED .*org.*description.*line 3")
        self.assertFalse(out.exists() and any(out.iterdir()), "a refused plan wrote files")

    def test_2_skill_speaks_for_its_placement(self):
        def check(run):
            text, minted = run.skill(), run.world_json["id"]
            self.assertNotIn(minted, text, "the minted folder id is no address")
            if run.placement == "online":
                self.assertIn(SERVER_ID, text)
                self.assertIn("https://www.onlyworlds.com/api/v2", text)
                if not run.plan.get("repo"):
                    self.assertEqual(run.world_json.get("api", {}).get("world_id"), SERVER_ID)
            else:
                self.assertIsNone(API_ROUTE.search(text), f"an API route in a folder world's skill: "
                                  f"{API_ROUTE.search(text) and text[API_ROUTE.search(text).start() - 60:][:120]!r}")
                self.assertIn("world.json", text)
                self.assertNotIn("api", run.world_json)
        self.each(check)

    def test_2b_lenses_at_the_door_and_room_for_names(self):
        """Every pack's world skill sends the visitor to its lenses right after the Charter, in its
        placement's own words (online: the ids from GET /me, each lens read through the draught with
        as_of, since a reading with none is fenced on the world's own clock; a folder: the Character's
        x_lens_uses and which links are anchors), the visit list reads 1 to 6, and the filled text
        keeps ROOM characters under the writer's budget, so the writer prints no size note."""
        budget = int(re.search(r"^SKILL_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        wrong = "1. a\n2. The Charter, whole.\n3. b\n3. c\n5. d\n\nafter"
        self.assertEqual([s.split(". ")[0] for s in visit_steps(wrong)], ["1", "2", "3", "3", "5"],
                         "the list reader must see a wrong numbering as it is")

        def check(run):
            text = run.skill()
            steps = visit_steps(text)
            self.assertEqual([s.split(". ")[0] for s in steps], ["1", "2", "3", "4", "5", "6"], steps)
            self.assertTrue(steps[2].startswith("3. Your lenses, the readings set for you"), steps[2])
            if run.placement == "online":
                self.assertIn("`GET /me` lists their ids in `lenses`", steps[2])
                self.assertIn("/context?lens=<id>&as_of=<today's day number>&compact=true", steps[2])
                self.assertNotIn("x_lens_uses", text)
            else:
                self.assertIn("`x_lens_uses`", steps[2])
                self.assertIn("never `founder`, `custodian` or `titles`", steps[2])
            self.assertLess(len(text), budget - ROOM, f"{len(text)} characters filled, budget {budget}")
            self.assertIsNone(re.search(r"^note: the (world|design|work) skill ", run.out, re.M), run.out)
        self.each(check)

    def test_3_who_is_here_names_the_seats(self):
        def check(run):
            charter = run.charter()
            m = re.search(r"Who is here\n(.*?)\n\n", charter, re.S)
            self.assertTrue(m, "no Who is here section")
            who = m.group(1)
            names = {e["key"]: e["fields"]["name"] for e in run.plan_src["elements"]}
            for e in run.plan_src["elements"]:
                seat = e.get("seat")
                if not seat:
                    continue
                self.assertIn(e["fields"]["name"], who)
                if seat.get("ai_of"):
                    role = seat["role"].replace("_", "-")
                    self.assertRegex(who, re.escape(e["fields"]["name"]) + r" \(Agent, " + re.escape(role)
                                     + r", " + re.escape(names[seat["ai_of"]]) + r"'s AI\)")
            keeper = run.plan["values"].get("keeper") or run.plan["values"].get("ai")
            self.assertIn(keeper, who)
            self.assertRegex(who, re.escape(keeper) + r"[^.]*keeps the")
            agents = [b for _, b in run.elements() if b.get("supertype") == "Agent"]
            if run.placement == "online":
                self.assertEqual(agents, [], "online, the seat makes the AI's Character")
            else:
                self.assertTrue(agents, "no Agent Character in a folder world")
                self.assertTrue(all(b.get("x_seat", {}).get("ai_of") for b in agents))
        self.each(check)

    def test_4_roster_route(self):
        def check(run):
            charter = run.charter()
            if run.placement == "online":
                self.assertIn("GET /members", charter)
            else:
                self.assertIsNone(API_ROUTE.search(charter), "an API route in a folder world's charter")
                self.assertIn("x_seat", charter)
        self.each(check)

    def test_5_agents_line_is_the_skill_line(self):
        def check(run):
            line = read(run.copy_root / "AGENTS.md").strip()
            self.assertTrue(line)
            copy = read(run.copy_root / ".claude" / "skills" / run.skill_name / "SKILL.md")
            self.assertIn(line, copy)
            self.assertIn(line, run.skill())
        self.each(check)

    def test_6_gitattributes_every_pack(self):
        def check(run):
            p = run.world / ".gitattributes"
            self.assertTrue(p.exists(), "no .gitattributes")
            self.assertEqual(read(p), GITATTRIBUTES)
            if run.placement == "repo":
                self.assertTrue((run.world / ".gitignore").exists())
            else:  # the copies' root is its own repository: the same rule at its root (ruled 2026-10-22)
                q = run.world.parent / ".gitattributes"
                self.assertTrue(q.exists(), "no root .gitattributes beside the world folder")
                self.assertEqual(read(q), GITATTRIBUTES)
        self.each(check)

    def test_7_daily_sweep_and_charter_order_every_pack(self):
        def check(run):
            text = run.skill()
            self.assertEqual(text.count(ORDER), 1, "the charter-order sentence, once")
            sweep = DAILY_SWEEP
            if run.pack != "company":  # only the company pack keeps lines with a Next line: the clause is cut
                self.assertIn(LINES_CLAUSE, sweep)
                sweep = sweep.replace(LINES_CLAUSE, "")
            if run.pack == "ai-home":  # the pack names the AI's human by the owner's name
                sweep = sweep.replace("your human", run.plan["values"]["owner"])
            self.assertEqual(text.count(sweep), 1, "the daily sweep, word for word, once")
            self.assertEqual(text.count("`Next: <step> · <who> · by YYYY-MM-DD`"), 1 if run.pack == "company" else 0)
        self.each(check)

    def test_8_company_start_here(self):
        for placement in PLACEMENTS:
            run = RUNS["company", placement]
            with self.subTest(placement=placement):
                self.assertEqual(run.code, 0, run.out)
                bodies = [b for _, b in run.elements()]
                guides = [b for b in bodies if b.get("supertype") == "Guide"]
                self.assertEqual([g["name"] for g in guides], ["Start here"])
                people = {b["id"] for b in bodies if b.get("supertype") == "Person"}
                welcomes = [b for b in bodies if b.get("supertype") == "Message"
                            and b.get("name", "").startswith("Welcome") and len(b.get("characters") or []) == 1]
                self.assertTrue(welcomes and all(w["characters"][0] in people for w in welcomes),
                                "a Welcome message to a person")
                self.assertIn("Start here, for people: Construct, supertype Guide", run.charter())
                self.assertIn('carries its Next, "Next: <step> · <who> · by YYYY-MM-DD"', run.charter())

    def test_9_checks_slot_every_pack(self):
        """Every charter file carries x_checks_rules, empty only in a pack with no rule; a pack's
        rules each a sentence in its charter (test 9f compares them with the published fixture)."""
        shipped = {"company": 3, "software-project": 2, "workshop": 1}
        def check(run):
            body = json.loads(read(run.world / "elements" / "law" / "charter.json"))
            self.assertIn("x_checks_rules", body, "no checks slot on the charter")
            rules = body["x_checks_rules"]
            self.assertIsInstance(rules, list)
            n = shipped.get(run.pack, 0)
            self.assertEqual(len(rules), n, f"the {run.pack} pack ships {n} rules")
            if not n:
                return  # the empty slot
            self.assertIn("x_checks_rules", run.charter())
            for rule in rules:
                self.assertEqual(set(rule), {"rule", "where", "require"})
                self.assertIn(rule["rule"].lower(), run.charter().lower(), "the rule's sentence is in the charter's own words")
        self.each(check)

    def test_9f_pack_rules_are_the_published_fixtures(self):
        """Every rule a pack ships is one of the published checks fixture's rules, byte for byte as
        JSON, never paraphrased. Skipped, with the path it looked at, when the fixture is not there
        (OW_CHECKS_FIXTURE names it; by default it sits beside OW_LINT's schema-dist)."""
        if not FIXTURE.exists():
            self.skipTest(f"the published checks fixture is not at {FIXTURE}: set OW_CHECKS_FIXTURE "
                          "(or OW_LINT) to the schema distribution's copy")
        fixture = json.loads(read(FIXTURE))

        def check(run):
            for rule in json.loads(read(run.world / "elements" / "law" / "charter.json"))["x_checks_rules"]:
                self.assertIn(rule, fixture["rules"])
        self.each(check)

    def test_9b_checks_slot_reaches_the_bulk_body(self):
        for placement in PLACEMENTS:
            bulk = json.loads(read(OUT / "plans" / f"company-{placement}-bulk.json"))
            charters = [i["element"] for i in bulk["items"] if i["type"] == "law"]
            self.assertEqual(len(charters), 1)
            self.assertEqual(len(charters[0]["x_checks_rules"]), 3, placement)

    def test_9e_format_version_is_the_spec_current(self):
        """The writer's FORMAT_VERSION is the folder spec's current (0.3.22): no older-format finding."""
        src = read(WRITER)
        self.assertIn('FORMAT_VERSION = "0.3.22"', src)
        for placement in PLACEMENTS:
            self.assertEqual(RUNS["company", placement].world_json["format_version"], "0.3.22", placement)

    def test_9c_plan_replaces_the_pack_rule(self):
        plan = json.loads(read(PLANS / "company.json"))
        plan["charter"]["x_checks_rules"] = []
        plan["copies"] = "none"
        plan_path = OUT / "plans" / "no-rule.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "no-rule"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(json.loads(read(out / "elements" / "law" / "charter.json"))["x_checks_rules"], [])
        plan["charter"]["x_checks_rules"] = "not a list"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(OUT / "bad-rule")],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("x_checks_rules", r.stdout)

    def test_9d_the_doctor_reads_the_slot(self):
        """The Python package's doctor (onlyworlds 0.24.0 or newer) applies the company rules; skipped without it."""
        try:
            import onlyworlds.checks  # noqa: F401  (0.24.0 added it)
        except ImportError:
            self.skipTest("onlyworlds 0.24.0 or newer is not installed")
        run = RUNS["company", "folder"]
        r = subprocess.run([sys.executable, "-m", "onlyworlds.doctor", str(run.world)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertIn("3 of 3 house rules applied", r.stdout, r.stdout + r.stderr)
        self.assertIn('rule 0, "a live line carries its Next"', r.stdout)

    def test_10_cold_visit_checklist(self):
        """The five points a cold visit guessed, answered by the company pack's own text.
        The questions and where the pack answers them: cold-visit-checklist.md."""
        for placement in ("online", "folder"):
            run = RUNS["company", placement]
            skill, charter = run.skill(), run.charter()
            with self.subTest(placement=placement):
                # (a) the Read list grows through the links route, never a PATCH of the list
                self.assertIn("(add, never replace)", charter)
                self.assertIn("never a PATCH of the list" if placement == "online" else "keeping what is there", skill)
                if placement == "online":
                    self.assertIn("links route", skill)
                    self.assertIn("POST /<type>/<id>/links/<field>", skill)
                # (b) a Read sets actor and characters
                self.assertIn("actor and characters = your Character", charter)
                self.assertIn("`actor` and `characters` your Character", skill)
                if placement == "online":
                    self.assertIn("relation?supertype=Read&characters=<your id>", skill)
                # (c) no x_seat on an online Agent; whose AI it is comes from /me
                if placement == "online":
                    self.assertIn("an online Agent has no `x_seat`", skill)
                    self.assertIn("front_door.sponsor_character", skill)
                else:
                    self.assertIn("`x_seat` says whose AI you are", skill)
                # (d) a human with no Person
                self.assertIn("No Person for your human", skill)
                self.assertIn("ask the keeper by message for a `Person`", skill)
                # (e) the filing table holds Guide, Concept, Regulation, Milestone, Charter (and Skill)
                for sup in ("Charter", "Skill", "Guide", "Concept", "Regulation", "Milestone"):
                    self.assertIn(f"`{sup}`", skill, sup)
                for sup in ("Concept", "Regulation", "Milestone"):
                    self.assertIn(sup, charter, sup)

    def test_11_board_and_note(self):
        """The board's writers and the Note's steer, in the company pack's own words."""
        for placement in PLACEMENTS:
            run = RUNS["company", placement]
            skill, charter = run.skill(), run.charter()
            with self.subTest(placement=placement):
                self.assertIn("The board: the owner's and the co-builders' messages to everyone", charter)
                self.assertIn("keeps a Note about themselves, not their work", charter)
                self.assertIn("Narrative, supertype Note", charter)
                self.assertIn("never on a schedule", charter)
                self.assertIn("Its own to write: its messages, Note, Read relation", charter)
                self.assertIn("your newest Note about yourself, not your work", skill)
                self.assertIn("`Note`", skill)
                self.assertIn("its message, Note, Read relation", skill)

    def test_12a_company_charter_and_guide_carry_the_mark(self):
        """Written from the company pack: the charter and the guide files carry x_charter_of, the
        world's id; no other element carries the key."""
        for placement in PLACEMENTS:
            run = RUNS["company", placement]
            with self.subTest(placement=placement):
                self.assertEqual(run.code, 0, run.out)
                want = SERVER_ID if placement == "online" else run.world_json["id"]
                if placement != "online":
                    self.assertNotEqual(want, SERVER_ID)
                charter = json.loads(read(run.world / "elements" / "law" / "charter.json"))
                self.assertEqual(charter.get("x_charter_of"), want, "the Charter's mark")
                guides = [b for _, b in run.elements() if b.get("supertype") == "Guide"]
                self.assertEqual(len(guides), 1)
                self.assertEqual(guides[0].get("x_charter_of"), want, "the Guide's mark")
                marked = [b["id"] for _, b in run.elements() if "x_charter_of" in b]
                total = sum(1 for _ in run.elements())
                self.assertEqual(sorted(marked), sorted([charter["id"], guides[0]["id"]]),
                                 "only the Charter and the Guide carry the mark")
                print(f"\n  company/{placement}: {total} elements read, {len(marked)} carry x_charter_of "
                      f"(the Charter, the Guide), each = {'the server id' if placement == 'online' else 'world.json id'}")

    def test_12b_every_pack_marks_its_aids_only(self):
        def check(run):
            want = SERVER_ID if run.placement == "online" else run.world_json["id"]
            aids, others = 0, 0
            for p, body in run.elements():
                aid = p.parts[-2] == "law" and body.get("supertype") == "Charter" or \
                    p.parts[-2] == "construct" and body.get("supertype") in ("Guide", "Domain")
                if aid:
                    aids += 1
                    self.assertEqual(body.get("x_charter_of"), want, p.name)
                else:
                    others += 1
                    self.assertNotIn("x_charter_of", body, p.name)
            self.assertGreaterEqual(aids, 1, "no Charter")
        self.each(check)

    def test_12c_the_mark_reaches_the_bulk_body(self):
        for placement in PLACEMENTS:
            bulk = json.loads(read(OUT / "plans" / f"company-{placement}-bulk.json"))
            marked = [i for i in bulk["items"] if "x_charter_of" in i["element"]]
            self.assertEqual(sorted(i["type"] for i in marked), ["construct", "law"], placement)
            if placement == "online":
                self.assertTrue(all(i["element"]["x_charter_of"] == SERVER_ID for i in marked))
            print(f"\n  company/{placement} bulk: {len(bulk['items'])} items, {len(marked)} carry x_charter_of")

    def test_12d_domain_pair_folded_near_word_not(self):
        plan = json.loads(read(PLANS / "company.json"))
        plan["copies"] = "none"
        plan["elements"] += [
            {"key": "dom", "type": "construct", "fields": {"name": "People", "supertype": "  domain\t",
                                                           "description": "Who is here."}},
            {"key": "near", "type": "construct", "fields": {"name": "Domains", "supertype": "Domains",
                                                            "description": "Not an aid."}},
            {"key": "lore", "type": "law", "fields": {"name": "Founding rules", "supertype": "Charters",
                                                      "description": "Not an aid."}},
        ]
        plan_path = OUT / "plans" / "domain.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "domain"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout)
        wid = json.loads(read(out / "world.json"))["id"]
        bodies = {b["name"]: b for b in (json.loads(read(p)) for p in (out / "elements").glob("*/*.json"))}
        self.assertEqual(bodies["People"].get("x_charter_of"), wid)
        self.assertNotIn("x_charter_of", bodies["Domains"])
        self.assertNotIn("x_charter_of", bodies["Founding rules"])
        print(f"\n  domain plan: {len(bodies)} elements, "
              f"{sum('x_charter_of' in b for b in bodies.values())} carry x_charter_of (Charter, Guide, Domain)")

    def test_12e_a_plan_never_names_the_mark(self):
        plan = json.loads(read(PLANS / "company.json"))
        plan["copies"] = "none"
        org = next(e for e in plan["elements"] if e["key"] == "org")
        org["fields"]["x_charter_of"] = "019a0b0c-0d0e-7f00-8a00-5e2be2000002"
        plan_path = OUT / "plans" / "plan-mark.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "plan-mark"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"REFUSED .*org.*x_charter_of")
        self.assertFalse(out.exists() and any(out.iterdir()), "a refused plan wrote files")

    def test_12f_a_plan_row_is_never_a_second_charter(self):
        plan = json.loads(read(PLANS / "company.json"))
        plan["copies"] = "none"
        plan["elements"].append({"key": "rules-two", "type": "law",
                                 "fields": {"name": "Rules", "supertype": " charter ", "description": "A second one."}})
        plan_path = OUT / "plans" / "second-charter.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "second-charter"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)], capture_output=True,
                           text=True, encoding="utf-8")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"REFUSED plan element 'rules-two': the pack writes the Charter; "
                                   r"a plan row cannot be a second one")
        self.assertFalse(out.exists() and any(out.iterdir()), "a refused plan wrote files")

    def test_13_team_packs_land_three_skills(self):
        """The company and software-project packs land three skills under the plan's prefix
        (<prefix>-start, -design, -work): each an Object with supertype Skill, under the budget with
        ROOM to spare, front matter name and description only, each with its two harness copies
        carrying the copied-from line; each speaks for its placement as the world skill does; the
        world skill names the other two; the work skill carries the report profile's keys. Every
        other pack keeps one skill, ow-<slug>."""
        budget = int(re.search(r"^SKILL_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))

        def check(run):
            extra = run.extra_skills()
            if run.pack not in ("company", "software-project"):
                self.assertEqual(extra, {})
                return
            self.assertEqual(sorted(extra), ["design", "work"])
            for kind, (body, name) in extra.items():
                text = body["description"]
                self.assertEqual(body["supertype"], "Skill")
                self.assertLess(len(text), budget - ROOM, f"{kind}: {len(text)} characters filled")
                self.assertTrue(text.startswith(f"---\nname: {name}\ndescription: "), text[:80])
                self.assertIn(f"`{name}`", run.skill())
                # the door hands out the skills the Charter names by address (GET /me, charter_skill)
                self.assertIn(f"ow://object/{body['id']}", run.charter())
                self.assertNotIn(run.world_json["id"], text, "the minted folder id is no address")
                if run.placement == "online":
                    if kind == "work":  # the report's mark names the server's world
                        self.assertIn(SERVER_ID, text)
                else:
                    self.assertIsNone(API_ROUTE.search(text), f"an API route in a folder world's {kind} skill")
                for h in (".agents", ".claude"):
                    copy = read(run.copy_root / h / "skills" / name / "SKILL.md")
                    self.assertIn(f"<!-- copied from the world: Object {body['id']}; updated_at none yet", copy)
                if kind == "work":
                    for key in ("x_report_answers", "x_room_of", '"handed in"', "consequences",
                                "what did this session make untrue?"):
                        self.assertIn(key, text, key)
        self.each(check)

    def test_14_team_sizes_leave_room_in_the_charter(self):
        """A real team fits: each team pack's test plan grown (or shrunk) to 2, 5, 8, 12 and 20 seats,
        people and AIs mixed with names of ordinary length, and 8 seats with six of them AIs (8 is the
        last size the charter names every seat: past NAMED seats the writer counts them), is written
        without a refusal in a folder and online, and the filled charter keeps CHARTER_ROOM characters
        under the writer's budget."""
        budget = int(re.search(r"^CHARTER_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        people = ["Morgan Ellis", "Samira Okafor", "Jonas Whitfield", "Priya Ramaswamy", "Lucas Moreau",
                  "Hannah Lindqvist", "Tobias Achterberg", "Ines Carvalho", "Daniel Osei", "Freya Thornton"]
        ais = ["Juniper", "Halden", "Marlow", "Sorrow-Lark", "Tamsin", "Quill", "Brennick", "Ostara",
               "Pell", "Wickham"]

        def sized(base, n, ai_heavy=False):
            plan = json.loads(json.dumps(base))
            seated = [e for e in plan["elements"] if e.get("seat")]
            person = next(e["key"] for e in seated if e["seat"]["role"] == "contributor" and not e["seat"].get("ai_of"))
            if n < len(seated):  # drop the plain person, and every link to it
                plan["elements"] = [e for e in plan["elements"] if e["key"] != person]
                for e in plan["elements"]:
                    for f, t in list((e.get("links") or {}).items()):
                        if isinstance(t, list):
                            e["links"][f] = [k for k in t if k != person]
                        elif t == person:
                            del e["links"][f]
                seated = [e for e in seated if e["key"] != person]
            human, p, a = "owner", iter(people), iter(ais)
            for i in range(n - len(seated)):
                if (i % 4 != 0) if ai_heavy else (i % 2 == 0):
                    name = next(a)
                    plan["elements"].append({"key": f"x-ai-{i}", "type": "character",
                                             "seat": {"role": "contributor", "ai_of": human},
                                             "fields": {"name": name, "supertype": "Agent"}})
                else:
                    human = f"x-p-{i}"
                    plan["elements"].append({"key": human, "type": "character", "seat": {"role": "contributor"},
                                             "fields": {"name": next(p), "supertype": "Person"}})
            return plan

        cases = [(n, False) for n in (2, 5, 8, 12, 20)] + [(8, True)]
        for pack in ("company", "software-project"):
            base = json.loads(read(PLANS / f"{pack}.json"))
            for n, heavy in cases:
                for placement in ("folder", "online"):
                    with self.subTest(pack=pack, seats=n, ai_heavy=heavy, placement=placement):
                        root = OUT / f"size-{pack}-{n}{'-ai' if heavy else ''}-{placement}"
                        plan, world = variant(sized(base, n, heavy), placement, root)
                        self.assertEqual(sum(1 for e in plan["elements"] if e.get("seat")), n)
                        plan_path = OUT / "plans" / f"{root.name}.json"
                        plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
                        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(world)],
                                           capture_output=True, text=True, encoding="utf-8")
                        self.assertEqual(r.returncode, 0, r.stdout)
                        size = len(json.loads(read(world / "elements" / "law" / "charter.json"))["description"])
                        print(f"\n  charter {pack} {n} seats{' (6 AIs)' if heavy else ''} {placement}: {size}")
                        self.assertLessEqual(size, budget - CHARTER_ROOM, f"{size} characters filled")

    # Each pack's charter as toolkit 5.9.5 (commit ac34e55) filled the test's own plans, folder and
    # online. A charter's free text has no longest case, so the guard is the length a plan had
    # before: no pack's charter grows, and no plan that 5.9.5 wrote is refused for a charter's words.
    CHARTER_AT_595 = {"company": (3478, 3440), "ai-home": (3343, 3304), "governance": (3760, 3721),
                      "workshop": (3248, 3233), "software-project": (3312, 3274)}

    def test_14c_no_charter_longer_than_595(self):
        """Every pack's filled charter, for the test's own plan, is no longer than 5.9.5 filled it."""
        def check(run):
            folder, online = self.CHARTER_AT_595[run.pack]
            most = online if run.placement == "online" else folder
            self.assertLessEqual(len(run.charter()), most, f"{run.pack} {run.placement}: longer than 5.9.5's {most}")
        self.each(check)

    def test_14b_an_owner_with_seven_ais(self):
        """One case among many, the one each AI's entry makes long (it repeats its human's name): one
        owner with a 31-character name and seven AIs of theirs, no other seat, in the three packs that
        ship rules, folder and online; each charter no longer than 5.9.5 (ac34e55) filled the same
        plan."""
        ceiling = {"company": (3926, 3888), "software-project": (3755, 3717), "workshop": (3690, 3675)}
        owner_name = "Anastasia Wilhelmina Ravensbury"
        ais = ["Juniper", "Halden", "Marlow", "Sorrow-Lark", "Tamsin", "Quill", "Brennick"]

        def owner_with_seven(base):
            plan = json.loads(json.dumps(base))
            owner = next(e for e in plan["elements"] if (e.get("seat") or {}).get("role") == "owner")
            gone = {e["key"] for e in plan["elements"] if e.get("seat") and e is not owner}
            plan["elements"] = [e for e in plan["elements"] if e["key"] not in gone]
            for e in plan["elements"]:
                for f, t in list((e.get("links") or {}).items()):
                    if isinstance(t, list):
                        e["links"][f] = [k for k in t if k not in gone]
                    elif t in gone:
                        del e["links"][f]
            owner["fields"]["name"] = owner_name
            for i, name in enumerate(ais):
                plan["elements"].append({"key": f"x-ai-{i}", "type": "character",
                                         "seat": {"role": "contributor", "ai_of": owner["key"]},
                                         "fields": {"name": name, "supertype": "Agent"}})
            for k in ("keeper", "owner"):
                if plan["values"].get(k):
                    plan["values"][k] = owner_name
            return plan

        self.assertEqual(len(owner_name), 31)
        for pack, (most_folder, most_online) in ceiling.items():
            base = json.loads(read(PLANS / f"{pack}.json"))
            for placement in ("folder", "online"):
                most = most_online if placement == "online" else most_folder
                with self.subTest(pack=pack, placement=placement):
                    root = OUT / f"owner7-{pack}-{placement}"
                    plan, world = variant(owner_with_seven(base), placement, root)
                    plan_path = OUT / "plans" / f"{root.name}.json"
                    plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
                    r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(world)],
                                       capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(r.returncode, 0, r.stdout)
                    size = len(json.loads(read(world / "elements" / "law" / "charter.json"))["description"])
                    print(f"\n  charter {pack} owner and 7 AIs {placement}: {size}")
                    self.assertLessEqual(size, most, f"{size} characters filled")

    def test_15_query_values_are_encoded(self):
        """No route in a filled online skill (all three in a team pack) carries a query value with a raw
        space (curl refuses `supertype=Work item` before sending): every code span with a `?`, its
        <placeholders> set aside, holds no space after the `?`."""
        def check(run):
            if run.placement != "online":
                return
            texts = [run.skill()] + [b["description"] for b, _ in run.extra_skills().values()]
            for text in texts:
                for span in re.findall(r"`([^`\n]*\?[^`\n]*)`", text):
                    query = re.sub(r"<[^>]*>", "", span.split("?", 1)[1])
                    self.assertNotIn(" ", query, span)
        self.each(check)

    def test_16_an_ai_seat_is_never_above_its_human(self):
        """The writer refuses a plan whose AI seat holds a role above its human's, naming both (the
        platform gives a seat at most its sponsor's role); the test plans pass (the other tests)."""
        plan = json.loads(read(PLANS / "company.json"))
        for e in plan["elements"]:
            if e["key"] == "tomas":
                e["seat"]["role"] = "contributor"
        plan["elements"].append({"key": "ai-tomas", "type": "character",
                                 "seat": {"role": "co_builder", "ai_of": "tomas"},
                                 "fields": {"name": "Pell", "supertype": "Agent"}})
        plan_path = OUT / "plans" / "company-ai-above.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "company-ai-above"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertRegex(r.stdout, r"Pell's role co_builder is above its human Tomas[^']*'s \(contributor\)")
        self.assertFalse(out.exists() and any(out.iterdir()), "a refused plan wrote files")

    def test_17_workshop_room_elements_carry_the_mark(self):
        """The workshop's seeded room elements carry x_room_of (the room profile): the sitting the
        world's id (the server's online), the board entry and the line the sitting's own id, in every
        placement; nothing else the writer wrote carries the key (the Charter, the skill, the people)."""
        room_pairs = {("narrative", "message"), ("narrative", "board"), ("event", "sitting")}
        for placement in PLACEMENTS:
            run = RUNS["workshop", placement]
            with self.subTest(placement=placement):
                self.assertEqual(run.code, 0, run.out)
                world = SERVER_ID if placement == "online" else run.world_json["id"]
                bodies = [(p.parts[-2], b) for p, b in run.elements()]
                sittings = [b for t, b in bodies if (t, (b.get("supertype") or "").casefold()) == ("event", "sitting")]
                self.assertEqual(len(sittings), 1)
                self.assertEqual(sittings[0].get("x_room_of"), world, "the sitting's mark is the world's id")
                marked = 0
                for t, b in bodies:
                    pair = (t, (b.get("supertype") or "").casefold())
                    if pair in room_pairs and pair != ("event", "sitting"):
                        self.assertEqual(b.get("x_room_of"), sittings[0]["id"], b.get("name"))
                        marked += 1
                    elif pair not in room_pairs:
                        self.assertNotIn("x_room_of", b, b.get("name"))
                self.assertEqual(marked, 2, "the board's welcome and the welcome line")

    def test_13b_a_team_pack_without_a_prefix_is_refused(self):
        plan = json.loads(read(PLANS / "company.json"))
        del plan["prefix"]
        plan_path = OUT / "plans" / "company-no-prefix.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out = OUT / "company-no-prefix"
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(out)],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("the pack never invents one", r.stdout)
        self.assertFalse(out.exists() and any(out.iterdir()), "a refused plan wrote files")

    def write_plan(self, plan, placement, name):
        """One writer run on a plan in a placement: (exit code, output, world folder, copies root)."""
        root = OUT / name
        plan, world = variant(plan, placement, root)
        plan_path = OUT / "plans" / f"{name}.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(world)],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr, world, root

    def assert_over_written(self, code, out, label, path, name, root, budget):
        """A skill at or over SKILL_MAX: exit 0, its file and both copies written, its size line giving
        its size and the aim, one note naming it that asks for nothing."""
        self.assertEqual(code, 0, out)
        size = len(json.loads(read(path))["description"])
        self.assertGreaterEqual(size, budget, f"the case must fill the {label} to {budget} or more")
        self.assertEqual([ln for ln in out.splitlines() if ln.startswith(f"note: the {label} ")],
                         [size_note(label, size, budget)], out)
        self.assertIn(size_line(label, size, budget, name), out)
        for h in (".agents", ".claude"):
            self.assertTrue((root / h / "skills" / name / "SKILL.md").exists(), f"{h} copy of {name}")

    def test_18a_a_world_skill_over_the_size_is_written(self):
        """A skill's size never refuses a plan: a workshop online named with 88 characters (5.9.5
        wrote it at 9,955; the world skill is now past SKILL_MAX) is written, exit 0, with one note."""
        budget = int(re.search(r"^SKILL_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        plan = json.loads(read(PLANS / "workshop.json"))
        name = "Kiln Street Toolmakers Collective and Friends of the Brickworks Monthly Open Build Night"
        self.assertEqual(len(name), 88)
        plan["world"]["name"] = plan["values"]["workshop"] = name
        plan["world"]["slug"] = "kiln-street-toolmakers-collective-and-friends-of-the-brickworks"[:61]
        code, out, world, root = self.write_plan(plan, "online", "over-workshop-online")
        self.assert_over_written(code, out, "world skill",
                                 world / "elements" / "object" / f"{plan['world']['slug']}-skill.json",
                                 "ow-" + plan["world"]["slug"], root, budget)

    def test_18b_a_work_skill_over_the_size_is_written(self):
        """The same for a team pack's extra skill: a company online whose long organisation name and
        long answer on where else its knowledge lives fill the work skill past SKILL_MAX (and the world
        skill with it: a note for each)."""
        budget = int(re.search(r"^SKILL_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        plan = json.loads(read(PLANS / "company.json"))
        plan["values"]["org"] = ("The Worshipful Company of Northern Cartographers, Surveyors, Instrument "
                                 "Makers and Allied Draughtsmen of the Lower Tyne Valley and the Port of Blyth")
        plan["values"]["elsewhere"] = (
            "the members' handbook in the shared drive (Governance, then Handbook, then the current year), "
            "the apprentices' logbooks kept by each workshop master, the survey archive on the plan chest "
            "server with its own index, the minutes of the court of assistants in the clerk's binder, the "
            "instrument register in the stores spreadsheet, and the chat channels of each of the five "
            "workshops, where most day-to-day decisions are first talked through and later written up by "
            "the clerk for the members' monthly letter")
        code, out, world, root = self.write_plan(plan, "online", "over-company-online")
        self.assert_over_written(code, out, "work skill",
                                 world / "elements" / "object" / f"{plan['world']['slug']}-work-skill.json",
                                 f"{plan['prefix']}-work", root, budget)
        self.assert_over_written(code, out, "world skill",
                                 world / "elements" / "object" / f"{plan['world']['slug']}-skill.json",
                                 f"{plan['prefix']}-start", root, budget)

    def test_18d_the_size_lines_at_the_boundary(self):
        """The real writer with the workshop's online world skill filled to exactly SKILL_MAX - 1,
        SKILL_MAX and SKILL_MAX + 1 (the `workshop` value padded): the size line gives the size and the
        aim at each, the note prints at SKILL_MAX and above and not below, and no printed line about
        the skill holds a comparing word that could be false at that size."""
        budget = int(re.search(r"^SKILL_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        base = json.loads(read(PLANS / "workshop.json"))
        pad = "and Friends of the Old Brickworks Open Build Night " * 30
        slug = base["world"]["slug"]

        def size_with(n, tag):
            plan = json.loads(json.dumps(base))
            plan["values"]["workshop"] += " " + pad[:n] if n else ""
            code, out, world, root = self.write_plan(plan, "online", f"edge-{tag}")
            self.assertEqual(code, 0, out)
            return len(json.loads(read(world / "elements" / "object" / f"{slug}-skill.json"))["description"]), out

        s0, _ = size_with(0, "base")
        s1, _ = size_with(10, "probe")
        self.assertEqual(s1 - s0, 11, "the `workshop` value fills the world skill once")
        for target in (budget - 1, budget, budget + 1):
            with self.subTest(size=target):
                size, out = size_with(target - s0 - 1, str(target))
                self.assertEqual(size, target)
                self.assertIn(size_line("world skill", size, budget, "ow-" + slug), out)
                notes = [ln for ln in out.splitlines() if ln.startswith("note: the world skill ")]
                self.assertEqual(notes, [size_note("world skill", size, budget)] if size >= budget else [], out)
                for part in (p for ln in out.splitlines() for p in ln.split(";") if "world skill" in p):
                    self.assertIsNone(re.search(r"\b(past|over|above|below|exceeds?)\b|of under", part), part)

    def test_18e_the_charter_at_the_boundary(self):
        """The real writer with the workshop's charter filled to exactly CHARTER_MAX - 1, CHARTER_MAX
        and CHARTER_MAX + 1 (the `about` value padded, which the charter holds once): written at
        CHARTER_MAX - 1, refused at CHARTER_MAX and above, as SKILL.md's Checks row says."""
        budget = int(re.search(r"^CHARTER_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        base = json.loads(read(PLANS / "workshop.json"))
        pad = "an evening of small tools built in the open by people and their AI " * 20

        def run_with(n, tag):
            plan = json.loads(json.dumps(base))
            plan["values"]["about"] += " " + pad[:n] if n else ""
            code, out, world, root = self.write_plan(plan, "folder", f"charter-edge-{tag}")
            charter = world / "elements" / "law" / "charter.json"
            if code == 0:
                return code, len(json.loads(read(charter))["description"]), out, world
            m = re.search(rf"^REFUSED charter: (\d+) characters, the budget is under {budget}$", out, re.M)
            return code, int(m.group(1)) if m else None, out, world

        _, s0, _, _ = run_with(0, "base")
        _, s1, _, _ = run_with(10, "probe")
        self.assertEqual(s1 - s0, 11, "the `about` value fills the charter once")
        for target in (budget - 1, budget, budget + 1):
            with self.subTest(size=target):
                code, size, out, world = run_with(target - s0 - 1, str(target))
                self.assertEqual(size, target, out)
                if target < budget:
                    self.assertEqual(code, 0, out)
                    self.assertIn(f"charter {target} of under {budget} characters;", out)
                else:
                    self.assertEqual(code, 1, out)
                    self.assertFalse(world.exists() and any(world.iterdir()), "a refused plan wrote files")
        self.assertIn(f"`write_world.py` refuses {budget:,} or more",
                      read(REPO / "skills" / "onlyworlds-setup" / "SKILL.md"))

    def test_18c_a_charter_over_its_budget_is_still_refused(self):
        """The charter's budget stands: a workshop whose `about` fills the charter past CHARTER_MAX is
        refused, naming the charter and its size, and nothing is written."""
        budget = int(re.search(r"^CHARTER_MAX = (\d+)\s*$", read(WRITER), re.M).group(1))
        plan = json.loads(read(PLANS / "workshop.json"))
        plan["values"]["about"] = " ".join(["a monthly evening where people and their AI bring specs for "
                                            "small tools, choose one together and build it in the open"] * 8)
        code, out, world, root = self.write_plan(plan, "folder", "charter-over")
        self.assertEqual(code, 1, out)
        size = int(re.search(rf"^REFUSED charter: (\d+) characters, the budget is under {budget}$", out,
                             re.M).group(1))
        self.assertGreaterEqual(size, budget)
        self.assertFalse(world.exists() and any(world.iterdir()), "a refused plan wrote files")
        self.assertFalse((root / ".claude").exists(), "a refused plan wrote copies")

    # 19: a plan's own text never breaks a written skill or leaves the folder.
    SHAPES = {"colon-space": "Fernhollow: Ferry", "trailing-colon": "Fernhollow Ferry:",
              "space-hash": "Atelier #9", "dashes": "Beta---Lab", "double-quote": 'The "Beta" Lab',
              "backslash": "Beta\\Lab"}

    @staticmethod
    def description_template(pack, kind):
        """A skill template's own description line, unfilled: the text after `description: `."""
        text = read(REPO / "skills" / "onlyworlds-setup" / "packs" / pack / f"{kind}.md").replace("\r\n", "\n")
        return next(ln for ln in text.split("\n") if ln.startswith("description: "))[len("description: "):]

    @staticmethod
    def front_matter(text):
        """The front matter between the opening `---` line and the next line that is `---`."""
        assert text.startswith("---\n"), text[:40]
        return text[4:text.index("\n---\n", 4)]

    def test_19a_names_never_break_the_front_matter(self):
        """Every pack, every skill template: names holding each shape a plain YAML scalar breaks on (or a
        quoted one must escape) give a front matter whose description is the filled text, in the
        Object and both copies, read by PyYAML and, where it is installed, by skills-ref's parser; and
        no `---` inside the front matter, where skills-ref and Claude Code would end it. The test
        prints which parsers ran (the gate's venv has no skills-ref). The double-quote and
        backslash shapes read whole on 5.9.6 too: they pin the escape, not a fix."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")
        try:
            from skills_ref.parser import parse_frontmatter
        except ImportError:
            parse_frontmatter = None
        print(f"\n  19a read by: PyYAML {yaml.__version__}"
              + ("; skills-ref's parser" if parse_frontmatter else "; skills-ref's parser not installed here, not run"))
        ph = re.compile(r"\{\{([a-z_]+)\}\}")
        for pack in PACKS:
            base = json.loads(read(PLANS / f"{pack}.json"))
            kinds = ["skill"] + [k for k in ("design", "work") if (REPO / "skills" / "onlyworlds-setup" / "packs"
                                                                   / pack / f"{k}.md").exists()]
            templates = {k: self.description_template(pack, k) for k in kinds}
            named = {m for t in templates.values() for m in ph.findall(t)}
            for shape, name in self.SHAPES.items():
                with self.subTest(pack=pack, shape=shape):
                    plan = json.loads(json.dumps(base))
                    values = dict(plan["values"])
                    for key in named & set(values):
                        plan["values"][key] = values[key] = name
                    if "world_name" in named:
                        plan["world"]["name"] = name
                    values.update(world_name=plan["world"]["name"], work_skill_name=f"{plan.get('prefix')}-work")
                    code, out, world, root = self.write_plan(plan, "folder", f"shape-{pack}-{shape}")
                    self.assertEqual(code, 0, out)
                    slug = plan["world"]["slug"]
                    for kind in kinds:
                        want = ph.sub(lambda m: values[m.group(1)], templates[kind])
                        self.assertIn(name, want)
                        skill_name = (f"{plan['prefix']}-{'start' if kind == 'skill' else kind}" if len(kinds) > 1
                                      else "ow-" + slug)
                        obj = world / "elements" / "object" / (f"{slug}-skill.json" if kind == "skill"
                                                               else f"{slug}-{kind}-skill.json")
                        texts = {"Object": json.loads(read(obj))["description"]}
                        for h in (".agents", ".claude"):
                            texts[h] = read(root / h / "skills" / skill_name / "SKILL.md")
                        self.assertEqual(texts[".agents"], texts[".claude"])
                        for where, text in texts.items():
                            fm = self.front_matter(text)
                            # skills-ref and Claude Code end the front matter at a `---` anywhere
                            self.assertNotIn("---", fm, f"{kind} {where}")
                            meta = yaml.safe_load(fm)
                            self.assertEqual(meta, {"name": skill_name, "description": want}, f"{kind} {where}")
                            if parse_frontmatter:
                                self.assertEqual(parse_frontmatter(text)[0]["description"], want, f"{kind} {where}")

    # The values keys a pack's written texts put in a place that is one line (a heading, a table row),
    # read off the templates by hand, so the writer's own reading of them is pinned.
    ONE_LINE_VALUES = {("ai-home", "ai"), ("company", "org_kinds"), ("company", "line_kinds"),
                       ("governance", "body"), ("software-project", "project")}

    def test_19b_a_line_break_only_where_the_place_is_one_line(self):
        """A tab or another control character in any plan value written into a text is refused, named as
        what it is; a line break is refused where the value lands in a place that is one line (a heading,
        a table row, a name, a path, a date, the AGENTS.md line) and kept where every place is a paragraph
        or a list item, as 5.9.6 wrote it (a multi-line `about` or `privacy_rule`); a `{{` in a value is
        refused as the value's; a refused plan writes nothing; the free JSON texts keep their breaks."""
        def setter(path):
            def put(plan, value):
                node = plan
                for k in path[:-1]:
                    node = node[k]
                node[path[-1]] = (node[path[-1]] or "") + value if path[-1] in node else value
            return put

        def seated(field, ai):
            def put(plan, value):
                e = next(e for e in plan["elements"] if e.get("seat") and bool(e["seat"].get("ai_of")) == ai)
                e["fields"][field] = e["fields"].get(field, "Agent") + value
            return put
        cases = []  # (pack, label, how to set it, one line)
        for pack in PACKS:
            for key in json.loads(read(PLANS / f"{pack}.json"))["values"]:
                cases.append((pack, f"values.{key}", setter(["values", key]), (pack, key) in self.ONE_LINE_VALUES))
        cases += [("company", "world.name", setter(["world", "name"]), True),
                  ("workshop", "world.name", setter(["world", "name"]), True),
                  ("company", "world.slug", setter(["world", "slug"]), True),
                  ("governance", "world.slug", setter(["world", "slug"]), True),
                  ("company", "prefix", setter(["prefix"]), True),
                  ("company", "today", setter(["today"]), True),
                  ("company", "plan element 'owner', name", seated("name", False), True),
                  ("software-project", "plan element 'ai-burr', supertype", seated("supertype", True), True)]
        others = ["\t", "\x00", "\x0b", "\x0c", "\x1b", "\x1c", "\x1f", "\x7f", "\x85", "\x9b",
                  chr(0x2028), chr(0x2029)]
        breaks = ["\n", "\r\n", "\r"]
        wants = {"tab": "holds a tab; write a space instead",
                 "control": "holds a control character \\(U\\+{:04X}\\); remove it",
                 "break": "holds a line break \\(\\\\n, \\\\r\\\\n or \\\\r\\), and it lands in [^\\n]*, "
                          "which is one line; write it on one line"}
        for i, (pack, label, put, one) in enumerate(cases):
            for kind, ch in ((("tab" if others[i % 12] == "\t" else "control"), others[i % 12]),
                             ("break", breaks[i % 3])):
                with self.subTest(pack=pack, key=label, char=repr(ch)):
                    plan = json.loads(read(PLANS / f"{pack}.json"))
                    put(plan, ch + "Lab")
                    code, out, world, root = self.write_plan(plan, "folder", f"ctrl-{i}-{kind}")
                    if kind == "break" and not one:
                        self.assertEqual(code, 0, out)
                        continue
                    self.assertEqual(code, 1, out)
                    self.assertRegex(out, rf"REFUSED {re.escape(label)} [^\n]*: " + wants[kind].format(ord(ch[0])))
                    self.assertFalse(world.exists() and any(world.iterdir()), "a refused plan wrote files")
                    self.assertFalse(root.exists() and any(p for p in root.iterdir() if p != world), "copies written")
        with self.subTest(pack="company", key="copies", char="U+000A"):
            root = OUT / "ctrl-copies"
            plan, world = variant(json.loads(read(PLANS / "company.json")), "folder", root)
            plan["copies"] = str(root / "pro\nject")
            plan_path = OUT / "plans" / "ctrl-copies.json"
            plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
            r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(world)],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertRegex(r.stdout, r"REFUSED copies [^\n]*: holds a line break \(\\n, \\r\\n or \\r\), and it "
                                       r"lands in a folder path")
            self.assertEqual(self.listing(root), [], "a refused plan wrote files")
        for ch in others:  # wherever it stands: at the start, after a line break, at the end
            for where, text in (("start", ch + "GitHub Issues"), ("after a line break", "GitHub Issues\nsee " + ch + " done"),
                                ("end", "GitHub Issues" + ch)):
                with self.subTest(key="values.tracker", char=repr(ch), where=where):
                    plan = json.loads(read(PLANS / "software-project.json"))
                    plan["values"]["tracker"] = text
                    code, out, world, root = self.write_plan(plan, "folder", f"ctrl-at-{ord(ch):04x}-{where[:5]}")
                    self.assertEqual(code, 1, out)
                    self.assertRegex(out, r"REFUSED values\.tracker [^\n]*: holds a (tab|control character)")
                    self.assertFalse(root.exists() and any(root.iterdir()), "a refused plan wrote files")
        with self.subTest(case="the reader's tracker"):
            plan = json.loads(read(PLANS / "software-project.json"))
            plan["values"]["tracker"] = "GitHub Issues\nsee \x00\x1b[2J\t done"
            code, out, world, root = self.write_plan(plan, "folder", "ctrl-reader-tracker")
            self.assertEqual(code, 1, out)
            self.assertIn("holds a control character (U+0000); remove it", out)
        with self.subTest(case="a `{{` in a value is the value's"):
            plan = json.loads(read(PLANS / "governance.json"))
            plan["values"]["body"] = "The {{Board}}"
            code, out, world, root = self.write_plan(plan, "folder", "ctrl-brace")
            self.assertEqual(code, 1, out)
            self.assertIn("REFUSED values.body 'The {{Board}}': holds `{{`, which the writer reads as the start "
                          "of a placeholder; write the value without it", out)
            self.assertNotIn("packs/governance", out, "the pack's own line is not to blame")
        for pack, key, text in (("workshop", "about", "a workshop where people and their AI\nbring specs,\n"
                                 "choose one, and build it in the open"),
                                ("ai-home", "privacy_rule", "What the owner says in confidence stays here.\n"
                                 "Nobody else's private details enter.")):
            with self.subTest(case=f"a multi-line {key} is written"):
                plan = json.loads(read(PLANS / f"{pack}.json"))
                plan["values"][key] = text
                code, out, world, root = self.write_plan(plan, "folder", f"multiline-{key}")
                self.assertEqual(code, 0, out)
                self.assertIn(text, json.loads(read(world / "elements" / "law" / "charter.json"))["description"])
        with self.subTest(case="free texts keep their line breaks"):
            plan = json.loads(read(PLANS / "company.json"))
            plan["world"]["description"] = "One line.\nAnother line."
            plan["skill"] = {"utility": "How an agent reaches this world.\nCopy it whole."}
            plan["elements"][0]["fields"]["description"] = "First.\n\nSecond."
            code, out, world, root = self.write_plan(plan, "folder", "ctrl-free")
            self.assertEqual(code, 0, out)
            self.assertEqual(json.loads(read(world / "world.json"))["description"], "One line.\nAnother line.")

    def listing(self, folder):
        return sorted(str(p.relative_to(folder)) for p in folder.rglob("*")) if folder.exists() else []

    def test_19c_nothing_is_written_outside_the_folders(self):
        """A plan's world.slug that climbs (`../../escaped`, the two team packs, where no skill name
        gates it) or an element type that climbs out of the world folder is refused, the key
        named, and nothing is written anywhere under the case's own folder; the writer's own
        containment check, read on the path as written, refuses a copy path that climbs out of
        its copies root, and one on another drive."""
        cases = [("company", "slug-2", "../../escaped", r"world\.slug '\.\./\.\./escaped'"),
                 ("software-project", "slug-2", "../../escaped", r"world\.slug '\.\./\.\./escaped'"),
                 ("company", "slug-4", "../../../../escaped", r"world\.slug '\.\./\.\./\.\./\.\./escaped'"),
                 ("governance", "type", "../../../escaped",
                  r"plan element 'x-climb', type '\.\./\.\./\.\./escaped': one of the 22")]
        for pack, tag, bad, message in cases:
            with self.subTest(pack=pack, case=tag):
                plan = json.loads(read(PLANS / f"{pack}.json"))
                if tag == "type":
                    plan["elements"].append({"key": "x-climb", "type": bad, "fields": {"name": "Climber"}})
                else:
                    plan["world"]["slug"] = bad
                case = OUT / f"climb-{pack}-{tag}"
                case.mkdir(parents=True, exist_ok=True)
                before = self.listing(case)
                code, out, world, root = self.write_plan(plan, "folder", f"climb-{pack}-{tag}/a/b/c")
                self.assertEqual(code, 1, out)
                self.assertRegex(out, "REFUSED .*" + message)
                self.assertEqual(self.listing(case), before, "a refused plan wrote files")
        import importlib.util
        spec = importlib.util.spec_from_file_location("write_world_19c", WRITER)
        ww = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ww)
        root = OUT / "climb-copies"
        self.assertTrue(ww.outside(root / ".claude" / "skills" / ".." / ".." / ".." / "x" / "SKILL.md", root))
        self.assertFalse(ww.outside(root / ".claude" / "skills" / "ow-x" / "SKILL.md", root))
        if os.name == "nt":
            other = "D:" if str(root.resolve())[:1].upper() != "D" else "E:"
            self.assertTrue(ww.outside(other + "escape", root))

    def test_19d_a_description_past_the_specification(self):
        """The workshop world skill's description filled to exactly 1,024 characters is written with no
        note; at 1,025 it is written, exit 0, with one note giving its length and the 1,024 the Agent
        Skills specification gives, and no comparing word."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")
        base = json.loads(read(PLANS / "workshop.json"))
        pad = "and Friends of the Old Brickworks Open Build Night " * 20

        def described(n, tag):
            plan = json.loads(json.dumps(base))
            plan["values"]["workshop"] += " " + pad[:n] if n else ""
            code, out, world, root = self.write_plan(plan, "folder", f"desc-{tag}")
            self.assertEqual(code, 0, out)
            text = read(root / ".claude" / "skills" / ("ow-" + plan["world"]["slug"]) / "SKILL.md")
            return len(yaml.safe_load(self.front_matter(text))["description"]), out

        s0, _ = described(0, "base")
        s1, _ = described(10, "probe")
        self.assertEqual(s1 - s0, 11, "the `workshop` value fills the description once")
        for target in (1024, 1025):
            with self.subTest(size=target):
                size, out = described(target - s0 - 1, str(target))
                self.assertEqual(size, target)
                notes = [ln for ln in out.splitlines() if "description" in ln and ln.startswith("note: ")]
                want = ([f"note: the world skill's description is {size} characters, and the Agent Skills "
                         f"specification gives 1024"] if size > 1024 else [])
                self.assertEqual(notes, want, out)

    def test_19e_a_name_with_no_letters_a_slug_keeps(self):
        """A world named in a script the slug drops whole, with no slug in the plan: in a team pack the
        skill Objects' files take the world skill's own id where the slug would stand (no file name
        starts with a hyphen); in a one-skill pack the skill's name would be `ow-`, which the name
        rule refuses, as before, and nothing is written."""
        for pack in ("company", "software-project"):
            with self.subTest(pack=pack):
                plan = json.loads(read(PLANS / f"{pack}.json"))
                plan["world"]["name"] = "東京"
                del plan["world"]["slug"]
                code, out, world, root = self.write_plan(plan, "folder", f"noslug-{pack}")
                self.assertEqual(code, 0, out)
                folder = world / "elements" / "object"
                objects = sorted(p.name for p in folder.glob("*.json"))
                self.assertFalse([n for n in objects if n.startswith("-")], objects)
                by_name = {}
                for n in objects:
                    body = json.loads(read(folder / n))
                    by_name[body["name"]] = (n, body["id"])
                name, sid = by_name["東京 world skill"]
                self.assertEqual(name, f"{sid}-skill.json")
                for kind in ("design", "work"):
                    self.assertEqual(by_name[f"東京 {kind} skill"][0], f"{sid}-{kind}-skill.json")
        with self.subTest(pack="governance"):
            plan = json.loads(read(PLANS / "governance.json"))
            plan["world"]["name"] = "Москва"
            del plan["world"]["slug"]
            code, out, world, root = self.write_plan(plan, "folder", "noslug-governance")
            self.assertEqual(code, 1, out)
            self.assertIn("REFUSED skill name 'ow-': lowercase letters, digits and hyphens, 64 at most; "
                          "the world's name keeps no letter a slug keeps, so give `world.slug` in the plan", out)
            self.assertFalse(world.exists() and any(world.iterdir()), "a refused plan wrote files")
    def writer_module(self, tag):
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"write_world_{tag}", WRITER)
        ww = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ww)
        return ww

    def test_19f_a_linked_folder_is_written_through(self):
        """A project whose .claude, .agents and world folder are links to other folders (junctions on
        Windows, symlinks elsewhere) is the user's own: the writer reads paths as written, never through
        a link, and writes through them, as 5.9.6 did: exit 0, each file in the linked folder."""
        base = OUT / "linked"
        root, shared = base / "proj", base / "shared-claude"
        root.mkdir(parents=True, exist_ok=True)
        shared.mkdir(parents=True, exist_ok=True)
        shared_agents, shared_world = base / "shared-agents", base / "shared-world"
        shared_agents.mkdir(parents=True, exist_ok=True)
        shared_world.mkdir(parents=True, exist_ok=True)
        for target, link in ((shared, root / ".claude"), (shared_agents, root / ".agents"), (shared_world, root / "world")):
            if os.name == "nt":
                import _winapi
                _winapi.CreateJunction(str(target), str(link))
            else:
                os.symlink(target, link, target_is_directory=True)
            self.assertTrue(link.exists())
        plan = json.loads(read(PLANS / "governance.json"))
        code, out, world, _ = self.write_plan(plan, "folder", "linked/proj")
        self.assertEqual(code, 0, out)
        name = "ow-" + plan["world"]["slug"]
        self.assertTrue((shared / "skills" / name / "SKILL.md").exists(), out)
        self.assertTrue((shared_agents / "skills" / name / "SKILL.md").exists(), out)
        self.assertTrue((shared_world / "world.json").exists(), out)

    def test_19g_an_element_type_is_one_of_the_22(self):
        """The writer's TYPES are the 22 sections of knowledge/schema-reference.md, in order; a plan
        element whose type is not one of them is refused, its key and type named, nothing written."""
        page = read(REPO / "knowledge" / "schema-reference.md").replace("\r\n", "\n")
        on_page = [ln[3:].lower() for ln in page.split("\n") if re.fullmatch(r"## [A-Z]+", ln)]
        self.assertEqual(len(on_page), 22)
        self.assertEqual(list(self.writer_module("19g").TYPES), on_page)
        for i, bad in enumerate(["..", "", "../law", "a:b", "C:escape-type", "character ", "CHARACTER", "nul",
                                 'a"b', "a\nb", "a*b", None, 5]):
            with self.subTest(type=repr(bad)):
                plan = json.loads(read(PLANS / "governance.json"))
                plan["elements"].append({"key": "x-t", "type": bad, "fields": {"name": "Typed"}})
                case = OUT / f"type-{i}"
                code, out, world, root = self.write_plan(plan, "folder", f"type-{i}")
                self.assertEqual(code, 1, out)
                self.assertIn(f"REFUSED plan element 'x-t', type {bad!r}: one of the 22 element types", out)
                self.assertEqual(self.listing(case), [], "a refused plan wrote files")

    def test_19h_refused_before_anything_is_written(self):
        """The writer writes it all or refuses before writing: a lone surrogate in a name, a value that
        is null, a list or an object, a null world name with no slug, or a setup day not written
        YYYY-MM-DD is refused, the key named; a plan in a shape the writer does not read (a number
        where text or a pack goes, no elements) is refused, not a traceback; the case's folder stays empty."""
        def company(put):
            plan = json.loads(read(PLANS / "company.json"))
            put(plan)
            return plan
        cases = [
            ("surrogate", lambda p: p["world"].__setitem__("name", "Fern" + chr(0xD800)),
             "REFUSED world.name: holds a lone surrogate"),
            ("null", lambda p: p["values"].__setitem__("org", None),
             "REFUSED values.org None: the writer puts it into a text, so it is a string"),
            ("list", lambda p: p["values"].__setitem__("org", ["a", "b"]),
             "REFUSED values.org ['a', 'b']: the writer puts it into a text, so it is a string"),
            ("object", lambda p: p["values"].__setitem__("org", {"a": 1}),
             "REFUSED values.org {'a': 1}: the writer puts it into a text, so it is a string"),
            ("null-name", lambda p: (p["world"].__setitem__("name", None), p["world"].pop("slug")),
             "REFUSED world.name None: the writer puts it into a text, so it is a string"),
            ("today", lambda p: p.__setitem__("today", "2026-13-45"),
             "REFUSED today '2026-13-45': the setup day, a date written YYYY-MM-DD"),
            ("today-basic", lambda p: p.__setitem__("today", "20261112"),
             "REFUSED today '20261112': the setup day, a date written YYYY-MM-DD"),
            ("today-week", lambda p: p.__setitem__("today", "2026-W46-4"),
             "REFUSED today '2026-W46-4': the setup day, a date written YYYY-MM-DD"),
            ("description", lambda p: p["world"].__setitem__("description", 5),
             "REFUSED the writer stopped before writing anything ("),
            ("utility", lambda p: p.__setitem__("skill", {"utility": ["a"]}),
             "REFUSED the writer stopped before writing anything ("),
            ("world-id", lambda p: p.__setitem__("online", {"world_id": 5}),
             "REFUSED the writer stopped before writing anything ("),
            ("pack", lambda p: p.__setitem__("pack", 5),
             "REFUSED the writer stopped before writing anything ("),
            ("no-elements", lambda p: p.pop("elements"),
             "REFUSED the writer stopped before writing anything (KeyError: no key 'elements' where one is read)"),
        ]
        for tag, put, message in cases:
            with self.subTest(case=tag):
                code, out, world, root = self.write_plan(company(put), "folder", f"before-{tag}")
                self.assertEqual(code, 1, out)
                self.assertIn(message, out)
                self.assertNotIn("Traceback", out)
                self.assertEqual(self.listing(root), [], "a refused plan wrote files")


    def test_19i_every_folder_is_made_before_the_first_file(self):
        """A copies root whose name the system refuses (Windows: a `|`), that names an existing file, or
        whose .claude/skills is a file is refused, the key and the folder named; the folders the run
        made are gone again and nothing is written: the listings of the output folder's parent and of
        the copies' parent are the same before and after."""
        base = OUT / "copies-shapes"
        base.mkdir(parents=True, exist_ok=True)
        (base / "a-file.txt").write_text("x", encoding="utf-8")
        (base / "skills-file" / ".claude").mkdir(parents=True, exist_ok=True)
        (base / "skills-file" / ".claude" / "skills").write_text("x", encoding="utf-8")
        cases = [("a-file", base / "a-file.txt"), ("skills-is-file", base / "skills-file")]
        if os.name == "nt":
            cases.append(("refused-name", base / "pr|oj"))
        for tag, copies in cases:
            with self.subTest(case=tag):
                case = OUT / f"copies-{tag}"
                case.mkdir(parents=True, exist_ok=True)
                plan = json.loads(read(PLANS / "governance.json"))
                plan["copies"], plan["repo"], plan["agents_md"] = str(copies), False, True
                plan_path = OUT / "plans" / f"copies-{tag}.json"
                plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
                before = (self.listing(case), self.listing(base))
                r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(case / "world")],
                                   capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
                self.assertRegex(r.stdout, r"REFUSED copies [^\n]*: the folder [^\n]* cannot be made")
                self.assertNotIn("Traceback", r.stdout + r.stderr)
                self.assertEqual((self.listing(case), self.listing(base)), before, "the run left something")


def contents(*folders):
    """Each folder's listing with every file's bytes: {(folder, relative path): bytes, or None for a folder}."""
    out = {}
    for folder in folders:
        for p in sorted(folder.rglob("*")) if folder.exists() else []:
            out[str(folder), str(p.relative_to(folder))] = p.read_bytes() if p.is_file() else None
    return out


class ClosedOut(io.StringIO):
    """An output whose reader goes away after `accept` writes, as `| head -1` does: each later write is
    refused (a broken pipe). What the reader read is the text it holds."""

    def __init__(self, accept=0):
        super().__init__()
        self.accept = accept

    def write(self, text):
        if self.accept <= 0:
            raise BrokenPipeError(32, "Broken pipe (made to fail)")
        self.accept -= 1
        return super().write(text)


class UndoFault:
    """The j-th step of an undo made to fail: a step is a folder removed (Path.rmdir), a file removed
    (os.remove) or a file opened (`open`, any mode) while Journal.undo runs. `when` is "before" (raised
    in place of the step) or "after" (the step done, then raised); `raise_` makes what is raised. The
    run's first failure is `first`: ("bulk", make) at the bulk file's open, or ("mkdir", n, make) at
    the n-th folder made, `make` making what is raised. j = 0 counts the steps and fails none."""

    def __init__(self, ww, j, when, raise_, first):
        self.ww, self.j, self.when, self.raise_, self.first = ww, j, when, raise_, first
        self.n, self.in_undo, self.made = 0, False, 0
        self.real = (open, Path.rmdir, os.remove, Path.mkdir, ww.Journal.undo)

    def step(self, do, *a, **kw):
        if not self.in_undo:
            return do(*a, **kw)
        self.n += 1
        if self.n != self.j:
            return do(*a, **kw)
        if self.when == "after":
            got = do(*a, **kw)
            if hasattr(got, "close"):
                got.close()
        raise self.raise_()

    def __enter__(self):
        fault = self
        real_open, real_rmdir, real_remove, real_mkdir, real_undo = self.real

        def open_(file, mode="r", *a, **kw):
            if not fault.in_undo and fault.first[0] == "bulk" and Path(file).name == "bulk.json" and mode != "rb":
                raise fault.first[1]()
            return fault.step(real_open, file, mode, *a, **kw)

        def mkdir(path, *a, **kw):
            if not fault.in_undo and fault.first[0] == "mkdir":
                fault.made += 1
                if fault.made == fault.first[1]:
                    raise fault.first[2]()
            return real_mkdir(path, *a, **kw)

        def undo(journal):
            fault.in_undo = True
            try:
                return real_undo(journal)
            finally:
                fault.in_undo = False
        self.ww.open, Path.mkdir, self.ww.Journal.undo = open_, mkdir, undo
        Path.rmdir = lambda path: fault.step(real_rmdir, path)
        os.remove = lambda path, *a, **kw: fault.step(real_remove, path, *a, **kw)
        return self

    def __exit__(self, *exc):
        _, Path.rmdir, os.remove, Path.mkdir, self.ww.Journal.undo = self.real
        del self.ww.open
        return False


class Fault:
    """The k-th act of a run made to fail: an act is a folder made (Path.mkdir) or a file opened to
    write (`open` with w, a, x or +). `how` is "open" (an OSError before the act), "half" (the file
    opened and half its bytes written, then an OSError; a folder: as "open") or "interrupt" (the act
    done, half the bytes written, then KeyboardInterrupt). k = 0 counts the acts and fails none."""

    def __init__(self, ww, k, how):
        self.ww, self.k, self.how, self.n = ww, k, how, 0
        self.real_open, self.real_mkdir = open, Path.mkdir

    def hit(self):
        self.n += 1
        return self.n == self.k

    def __enter__(self):
        fault = self

        def mkdir(path, *a, **kw):
            if fault.hit():
                if fault.how == "interrupt":
                    fault.real_mkdir(path, *a, **kw)
                    raise KeyboardInterrupt
                raise PermissionError(13, "Permission denied (made to fail)", str(path))
            return fault.real_mkdir(path, *a, **kw)

        def open_(file, mode="r", *a, **kw):
            if not any(c in mode for c in "wax+") or not fault.hit():
                return fault.real_open(file, mode, *a, **kw)
            if fault.how == "open":
                raise PermissionError(13, "Permission denied (made to fail)", str(file))
            fh = fault.real_open(file, mode, *a, **kw)
            real_write = fh.write

            def write(data):
                real_write(data[:len(data) // 2])
                fh.flush()
                raise KeyboardInterrupt if fault.how == "interrupt" else OSError(28, "No space left on device (made to fail)")
            fh.write = write
            return fh

        Path.mkdir, self.ww.open = mkdir, open_
        return self

    def __exit__(self, *exc):
        Path.mkdir = self.real_mkdir
        del self.ww.open
        return False


class TakenBack(unittest.TestCase):
    """A run that stops on an error, or an interrupt, after its first act leaves every folder it was
    given as it was, byte for byte: the folders and files it made removed, a line it appended cut
    off, a file it wrote over given its bytes back; an undo that cannot put a path back says so."""

    def writer(self, tag):
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"write_world_{tag}", WRITER)
        ww = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ww)
        return ww

    def project(self, pack, name, placement="folder"):
        """A project holding the user's AGENTS.md and CLAUDE.md, and an older bulk file the run writes
        over; the world written into a new folder in it, the copies at its root (folder and online). In
        the repository placement the project IS the world folder, new and empty, so the user's files are
        none and the bulk file waits beside it. (argv, the output folder's parent, the copies' parent)."""
        case = OUT / name
        proj = case / "proj"
        case.mkdir(parents=True, exist_ok=True)
        bulk = (case if placement == "repo" else proj) / "bulk.json"
        if placement != "repo":
            proj.mkdir(exist_ok=True)
            (proj / "AGENTS.md").write_bytes(b"# House rules\n\nKeep it short.")  # no line end: one is added
            (proj / "CLAUDE.md").write_bytes(b"# Claude\r\n\r\nRead AGENTS.md.\r\n")
        bulk.write_bytes(b'{"items": []}\n')
        plan, world = variant(json.loads(read(PLANS / f"{pack}.json")), placement, proj)
        plan["agents_md"] = True
        plan_path = case / "plan.json"
        plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
        return [str(plan_path), str(world), "--bulk", str(bulk)], proj, case

    def run_in(self, ww, argv, out=None):
        import contextlib
        buf = out if out is not None else io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ww.main(argv)
        return code, buf.getvalue()

    def test_20a_any_act_that_fails_is_taken_back(self):
        """For one plan of each pack, in a project with an AGENTS.md and a CLAUDE.md the run appends to
        and a bulk file it writes over: for every k from the first act to the last, the k-th act fails
        (before it, half way through its bytes, or by an interrupt), and once after the last file (the
        summary's one write fails); after each, the two listings with every file's bytes are as before,
        and the exit is 1, or the interrupt comes through. The folder placement for every pack; the
        repository and online placements for the company plan: their acts are of the same kinds (a
        folder made, a file made new, appended to or written over) in other places and numbers, and
        each is run here, not argued."""
        ww = self.writer("20a")
        runs, counts = 0, []
        sweeps = [(pack, "folder") for pack in PACKS] + [("company", "repo"), ("company", "online")]
        for pack, placement in sweeps:
            count_argv, _, _ = self.project(pack, f"undo-{pack}-{placement}-count", placement)
            with Fault(ww, 0, "open") as count:  # the same plan in a project of its own: the acts counted
                code, out = self.run_in(ww, count_argv)
            self.assertEqual(code, 0, out)
            self.assertEqual(out.count("the line appended"), 0 if placement == "repo" else 2, out)
            acts = count.n
            counts.append(f"{pack} {placement} {acts}")
            argv, proj, case = self.project(pack, f"undo-{pack}-{placement}", placement)
            before = contents(proj, case)
            for k in range(1, acts + 1):
                for how in ("open", "half", "interrupt"):
                    with self.subTest(pack=pack, placement=placement, k=k, how=how):
                        with Fault(ww, k, how):
                            if how == "interrupt":
                                with self.assertRaises(KeyboardInterrupt):
                                    self.run_in(ww, argv)
                            else:
                                code, out = self.run_in(ww, argv)
                                self.assertEqual(code, 1, out)
                        self.assertEqual(contents(proj, case), before, f"act {k} of {acts} ({how}) left something")
                        runs += 1
            with self.subTest(pack=pack, placement=placement, k="after the last file"):
                code, _ = self.run_in(ww, argv, ClosedOut(0))
                self.assertEqual(code, 1)
                self.assertEqual(contents(proj, case), before, "a failure after the last file left something")
                runs += 1
        print(f"\n20a: acts per run: {', '.join(counts)}; every k run three ways and once after the last "
              f"file: {runs} failing runs")
        self.assertGreater(runs, 100)

    def run_writer(self, argv):
        r = subprocess.run([sys.executable, str(WRITER), *argv], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def test_20b_a_read_only_agents_or_claude_md(self):
        """The user's AGENTS.md read-only; or their CLAUDE.md read-only beside a writable AGENTS.md, which
        the run appends to first: the run refuses, naming the file, and both listings are as before."""
        import stat
        for tag, locked in (("agents", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(case=tag):
                argv, proj, case = self.project("governance", f"undo-ro-{tag}")
                os.chmod(proj / locked, stat.S_IREAD)
                try:
                    before = contents(proj, case)
                    code, out = self.run_writer(argv)
                    self.assertEqual(code, 1, out)
                    self.assertIn(f"REFUSED {proj / locked}: PermissionError", out)
                    self.assertIn("nothing left behind; 1 problem(s)", out)
                    self.assertNotIn("Traceback", out)
                    self.assertEqual(contents(proj, case), before, "the run left something")
                finally:
                    os.chmod(proj / locked, stat.S_IREAD | stat.S_IWRITE)

    def test_20c_a_bulk_path_that_is_a_folder(self):
        """--bulk names a folder: the run refuses, naming it, and both listings are as before."""
        argv, proj, case = self.project("governance", "undo-bulk-folder")
        (proj / "bulk-folder").mkdir(exist_ok=True)
        argv[-1] = str(proj / "bulk-folder")
        before = contents(proj, case)
        code, out = self.run_writer(argv)
        self.assertEqual(code, 1, out)
        self.assertIn(f"REFUSED {proj / 'bulk-folder'}: ", out)
        self.assertNotIn("Traceback", out)
        self.assertEqual(contents(proj, case), before, "the run left something")

    def test_20d_a_file_written_over_gets_its_bytes_back(self):
        """The one file the writer writes over when it is there, the --bulk file: a failure after it
        was written (the summary's one write fails) gives it its bytes before."""
        ww = self.writer("20d")
        argv, proj, case = self.project("company", "undo-over")
        old = (proj / "bulk.json").read_bytes()
        before = contents(proj, case)
        code, _ = self.run_in(ww, argv, ClosedOut(0))
        self.assertEqual(code, 1)
        self.assertEqual((proj / "bulk.json").read_bytes(), old)
        self.assertEqual(contents(proj, case), before, "the run left something")

    def test_20e_an_undo_that_cannot_put_a_path_back_says_so(self):
        """A file the run made is held open by another (Windows; elsewhere its folder is made read-only)
        when a later act fails: the undo cannot remove it, and the message names it and its folders,
        never "nothing left behind"; exit 1."""
        import stat
        ww = self.writer("20e")
        argv, proj, case = self.project("governance", "undo-held")
        held = {}
        real_open = open

        def hold():  # the first copy, written and closed, is held by another
            if os.name == "nt":
                held["fh"] = real_open(held["path"], "rb")
            else:
                os.chmod(held["path"].parent, stat.S_IREAD | stat.S_IEXEC)
                held["fh"] = None

        def open_(file, mode="r", *a, **kw):
            if any(c in mode for c in "wax"):
                p = Path(file)
                if "path" in held and "fh" not in held:  # the next file after the first copy
                    hold()
                if p.name == "bulk.json":
                    raise PermissionError(13, "Permission denied (made to fail)", str(file))
                if p.name == "SKILL.md" and "path" not in held:
                    held["path"] = p
            return real_open(file, mode, *a, **kw)
        ww.open = open_
        try:
            code, out = self.run_in(ww, argv)
        finally:
            del ww.open
            if held.get("fh"):
                held["fh"].close()
            elif "path" in held and os.name != "nt":
                os.chmod(held["path"].parent, stat.S_IRWXU)
        self.assertEqual(code, 1, out)
        self.assertIn(f"NOT PUT BACK {held['path']}: ", out)
        self.assertIn(f"NOT PUT BACK {held['path'].parent}: the folder this run made could not be removed", out)
        self.assertRegex(out, r"left behind: the \d+ path\(s\) above; 1 problem\(s\)")
        self.assertNotIn("nothing left behind", out)

    def test_20f_an_error_of_the_writers_own_blames_nobody(self):
        """An error of the writer's own before its first act (a helper raises TypeError): the refusal
        says the writer stopped before writing anything, with the error's words, and names no culprit."""
        ww = self.writer("20f")
        argv, proj, case = self.project("governance", "undo-own")
        before = contents(proj, case)

        def broken(text):
            raise TypeError("a fault inside the writer")
        ww.double_quoted = broken
        code, out = self.run_in(ww, argv)
        self.assertEqual(code, 1, out)
        self.assertIn("REFUSED the writer stopped before writing anything (TypeError: a fault inside the writer)", out)
        self.assertNotIn("the plan", out)
        self.assertEqual(contents(proj, case), before, "the run left something")

    def assert_told(self, before, after, out):
        """The listing is as before, or every path that differs is named in a NOT PUT BACK line and the
        words never say that nothing is left."""
        changed = sorted({str(Path(folder) / rel) for (folder, rel) in set(before) | set(after)
                          if before.get((folder, rel), "absent") != after.get((folder, rel), "absent")})
        named = set(re.findall(r"^NOT PUT BACK (.+?): ", out, re.M))
        self.assertEqual([p for p in changed if p not in named], [], out)
        if changed:
            self.assertNotIn("nothing left behind", out)
            self.assertNotIn("nothing is written", out)
            self.assertNotIn("nothing written", out)
        return len(changed)

    def test_20g_an_interrupt_in_the_undo(self):
        """An interrupt at every step of the undo (in place of the step, or just after it), after a run
        that failed at its last file by an interrupt, or at its fifth folder by a refusal: the interrupt
        still ends the run, and the listing is as before or every changed path is named, with no word
        that nothing is left."""
        ww = self.writer("20g")
        firsts = {"interrupt at the bulk file": ("bulk", KeyboardInterrupt),
                  "the fifth folder refused": ("mkdir", 5, lambda: PermissionError(13, "Permission denied (made to fail)"))}
        runs, named, counts = 0, 0, []
        for tag, first in firsts.items():
            argv, proj, case = self.project("governance", f"undo-kbi-{tag.split()[1]}-count")
            with UndoFault(ww, 0, "before", KeyboardInterrupt, first) as count:
                try:
                    self.run_in(ww, argv)
                except KeyboardInterrupt:
                    pass
            steps = count.n
            self.assertGreaterEqual(steps, 4, tag)
            counts.append(f"{tag}: {steps} steps")
            for j in range(1, steps + 1):
                for when in ("before", "after"):
                    with self.subTest(first=tag, j=j, when=when):
                        argv, proj, case = self.project("governance", f"undo-kbi-{tag.split()[1]}-{j}-{when}")
                        before = contents(proj, case)
                        buf = io.StringIO()
                        with UndoFault(ww, j, when, KeyboardInterrupt, first):
                            with self.assertRaises(KeyboardInterrupt):
                                self.run_in(ww, argv, buf)
                        named += bool(self.assert_told(before, contents(proj, case), buf.getvalue()))
                        runs += 1
        print(f"\n20g: {'; '.join(counts)}; each step two ways: {runs} runs with an interrupt in the undo; "
              f"{named} left a path, each named")

    def test_20h_any_error_in_the_undo_is_named(self):
        """An error that is not an OSError (here a RuntimeError at the first file the undo removes) is
        that act's answer: the run goes on, takes back the rest, names the path, exits 1."""
        ww = self.writer("20h")
        argv, proj, case = self.project("governance", "undo-runtime")
        before = contents(proj, case)

        def boom():
            return RuntimeError("made to fail")
        real_remove = os.remove
        removes = []

        def remove(path, *a, **kw):
            removes.append(path)
            if len(removes) == 1:
                raise boom()
            return real_remove(path, *a, **kw)
        with UndoFault(ww, 0, "before", KeyboardInterrupt, ("bulk", lambda: PermissionError(13, "Permission denied (made to fail)"))):
            os.remove = remove
            code, out = self.run_in(ww, argv)
        self.assertEqual(code, 1, out)
        self.assertIn(f"NOT PUT BACK {removes[0]}: its undo was stopped by RuntimeError: made to fail, and not "
                      f"finished; left as it stands", out)
        self.assertEqual(self.assert_told(before, contents(proj, case), out), len(Path(removes[0]).parts)
                         - len(proj.parts))  # the file and each folder above it up to the project

    def test_20i_the_summary_is_one_write(self):
        """The summary is printed in one write, as the run's last act. A reader that goes away after the
        first write has read the whole summary of a run that exits 0; an output closed from the start
        takes the run back, exit 1, the reader having read nothing."""
        ww = self.writer("20i")
        with self.subTest(case="the reader goes after one write"):
            argv, proj, case = self.project("company", "undo-head")
            out = ClosedOut(1)
            try:
                code, read_ = self.run_in(ww, argv, out)
            except OSError as err:
                code, read_ = repr(err), out.getvalue()
            self.assertEqual(code, 0, read_)
            self.assertIn("wrote ", read_)
            self.assertIn("bulk body: ", read_)
        with self.subTest(case="closed from the start"):
            argv, proj, case = self.project("company", "undo-closed")
            before = contents(proj, case)
            out = ClosedOut(0)
            try:
                code, read_ = self.run_in(ww, argv, out)
            except OSError as err:
                code, read_ = repr(err), out.getvalue()
            self.assertEqual((code, read_), (1, ""))
            self.assertEqual(contents(proj, case), before, "the run left something")

    def test_20j_a_file_changed_by_this_run_twice(self):
        """CLAUDE.md is a hard link to AGENTS.md, so the run appends to one file twice; the bulk file
        fails, and the undo's first cut (the second append's) is refused. The first append's state
        says what is there, never who changed it."""
        ww = self.writer("20j")
        argv, proj, case = self.project("governance", "undo-hardlink")
        (proj / "CLAUDE.md").unlink()
        os.link(proj / "AGENTS.md", proj / "CLAUDE.md")
        cuts = []
        real_open = open

        def open_(file, mode="r", *a, **kw):
            if mode == "r+b":
                cuts.append(file)
                if len(cuts) == 1:
                    raise PermissionError(13, "Permission denied (made to fail)", str(file))
            return real_open(file, mode, *a, **kw)
        with UndoFault(ww, 0, "before", KeyboardInterrupt, ("bulk", lambda: PermissionError(13, "Permission denied (made to fail)"))) as f:
            inner = ww.open
            ww.open = lambda file, mode="r", *a, **kw: (open_ if f.in_undo else inner)(file, mode, *a, **kw)
            code, out = self.run_in(ww, argv)
        self.assertEqual(code, 1, out)
        self.assertNotIn("other than the writer", out)
        self.assertRegex(out, r"NOT PUT BACK [^\n]*CLAUDE\.md: still ends with the \d+ byte\(s\) this run appended")
        self.assertIn(f"NOT PUT BACK {proj / 'AGENTS.md'}: no longer ends with only what this run appended to it; "
                      f"left as it is", out)

    def test_20k_a_folder_refused_and_one_left_by_the_undo(self):
        """The third folder is refused and the undo cannot remove one folder it made: the refusal names
        the folder that could not be made, and does not say that nothing is written; the folder left is
        named below it."""
        ww = self.writer("20k")
        argv, proj, case = self.project("governance", "undo-mkdir-left")
        before = contents(proj, case)
        perm = lambda: PermissionError(13, "Permission denied (made to fail)")  # noqa: E731
        with UndoFault(ww, 1, "before", perm, ("mkdir", 3, perm)):
            code, out = self.run_in(ww, argv)
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"REFUSED [^\n]*: the folder [^\n]* cannot be made \(Permission denied \(made to fail\)\)\n")
        self.assertIn("the folder this run made could not be removed", out)
        self.assertGreater(self.assert_told(before, contents(proj, case), out), 0)


if __name__ == "__main__":
    print(f"output: {OUT}")
    unittest.main()
