"""The set-up skill's writer, on every pack, in three placements (OW Industry #493, round 2).

    python testing/setup-493/test_write_world.py [-v]

Each pack's plan (plans/<pack>.json, the rows of that pack's seed.md) is written three ways:
a plain folder (the world in <project>/world, the copies at <project>), a repository (the world
folder IS the repository, copies "world", "repo": true) and online (as the plain folder, with
"online": {"world_id": <a server id>}). Then the checks, one test per finding of the first
harness trial (h67 #9988):

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
   charter-order sentence with its reason, once each (OW Industry #552);
8. the company pack writes the Guide "Start here" and a Welcome message to a person.

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
# in every pack (OW Industry #552). A change to it is a change at its source first.
DAILY_SWEEP = (
    "**What a visit gives your human.** A visit always ends in a few lines to your human, never in a "
    "silent \"ok\": what is new for them (messages, with who wrote and what it asks), which of the lines "
    "they keep are over two weeks old or past their `Next: ... by` date, and what is asked of them. "
    "Nothing new and nothing stale is said in those words. A scheduled or daily read gives the same "
    "digest, then offers to go deeper: query the elements the new messages touch, read enough to see "
    "the whole picture, and talk it through with your human before writing anything.")
ORDER = ("This order is in the skill itself because harnesses differ on whether an `AGENTS.md` line "
         "or a skill is read first.")
API_ROUTE = re.compile(r"onlyworlds\.com/(api|mcp)|\b(GET|POST|PATCH|PUT|DELETE) /")
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
            copy = read(run.copy_root / ".claude" / "skills" / ("ow-" + run.plan["world"]["slug"]) / "SKILL.md")
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
            else:  # the copies' root is its own repository: the same rule at its root (h67 #10318)
                q = run.world.parent / ".gitattributes"
                self.assertTrue(q.exists(), "no root .gitattributes beside the world folder")
                self.assertEqual(read(q), GITATTRIBUTES)
        self.each(check)

    def test_7_daily_sweep_and_charter_order_every_pack(self):
        def check(run):
            text = run.skill()
            self.assertEqual(text.count(ORDER), 1, "the charter-order sentence, once")
            sweep = DAILY_SWEEP
            if run.pack == "ai-home":  # the pack names the AI's human by the owner's name
                sweep = sweep.replace("your human", run.plan["values"]["owner"])
            self.assertEqual(text.count(sweep), 1, "the daily sweep, word for word, once")
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
                welcomes = [b for b in bodies if b.get("supertype") == "Message" and b.get("name") == "Welcome"
                            and len(b.get("characters") or []) == 1]
                self.assertTrue(welcomes and all(w["characters"][0] in people for w in welcomes),
                                "a Welcome message to a person")
                self.assertIn("Construct, supertype Guide, named Start here", run.charter())


if __name__ == "__main__":
    print(f"output: {OUT}")
    unittest.main()
