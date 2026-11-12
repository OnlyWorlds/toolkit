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
    filled past the writer's comfortable size are written, exit 0, with one note naming each; a
    charter over its budget is still refused (18c).

Output goes to a fresh folder under <repo>/.scratch/tests/ (OW_SETUP_TEST_OUT to override);
nothing is deleted. The lint is schema-dist's walk/lint_folder.py, from the schema-dist checkout
beside this repository's main checkout, found through git from a worktree too (OW_LINT to point
at another).
Python 3, stdlib only.
"""
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
# The room a filled world skill keeps under the writer's comfortable size (its SKILL_MAX, read from
# the writer), so a company's own names rarely push a skill past it (the writer writes one over, and
# says so: test 18).
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
        keeps ROOM characters under the writer's budget."""
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
        """The writer's FORMAT_VERSION is the folder spec's current (0.3.21): no older-format finding."""
        src = read(WRITER)
        self.assertIn('FORMAT_VERSION = "0.3.21"', src)
        for placement in PLACEMENTS:
            self.assertEqual(RUNS["company", placement].world_json["format_version"], "0.3.21", placement)

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
        plan_path.write_text(json.dumps(plan, indent=1), encoding="utf-8")
        r = subprocess.run([sys.executable, str(WRITER), str(plan_path), str(world)],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr, world, root

    def assert_over_written(self, code, out, label, path, name, root, budget):
        """A skill at or over SKILL_MAX: exit 0, its file and both copies written, one note naming it."""
        self.assertEqual(code, 0, out)
        size = len(json.loads(read(path))["description"])
        self.assertGreaterEqual(size, budget, f"the case must fill the {label} past {budget}")
        note = (f"note: the {label} is {size} characters, over its comfortable size (under {budget}), "
                f"and was written anyway; shorter names or answers in the plan make it shorter")
        self.assertEqual([ln for ln in out.splitlines() if ln.startswith(f"note: the {label} ")], [note], out)
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
        long answer on where else its knowledge lives fill the work skill past SKILL_MAX."""
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


if __name__ == "__main__":
    print(f"output: {OUT}")
    unittest.main()
