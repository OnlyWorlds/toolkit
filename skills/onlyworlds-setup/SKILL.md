---
name: onlyworlds-setup
description: "Set up a world for a company, a team, an AI's own home, a council or board, or a software project, from a starter pack: house rules, a world skill for the AIs, a seed, the invites. Use when the user says 'set up a world for work', 'a shared knowledge base for our agents', 'invite my AI', 'a home for my AI'."
---

# OnlyWorlds Setup

Set up a world for work, not fiction: a company's shared knowledge base for its AI agents, an AI's own home, a council's record, a workshop's room, a software project's context. A short interview chooses a **starter pack**; the pack decides the shape; the user's answers fill it. Nothing is invented: a seed row nobody answered is left out and named.

Every pack lands the same four things: a **charter** (one Law with supertype `Charter`: the house rules every agent reads first), a **world skill** (one Object with supertype `Skill`: how an agent reaches the world, copied to where a harness reads it), a **seed** (the first elements, with the pack's supertypes doing the job a company's own types would), and the **invites** to make (a person link for each human, a seat for each AI).

Shared rules: `knowledge/principles.md`. The folder: `knowledge/world-folder.md`.

## Quick Reference

| Pack | For | Its own shape |
|------|-----|---------------|
| `company` | a company or team: its people, the organisations it deals with, its products | a line with an organisation is a Relation: its kind the supertype, its status the subtype |
| `ai-home` | one AI's own world: its memory, its people, its projects | memories are knowledge entries the AI holds; projects are Constructs |
| `governance` | a council or board | rules as Laws, seats as Titles, tenures as dated Relations, decisions as Events, minutes as Narratives |
| `software-project` | a repository's context | components as Constructs, decisions as Laws with parents, a world kept in the repository |

A workshop pack exists as a draft, on request.

**The interview: eight questions at most, one message, each with its default.** Ask only what the user has not already said; never ask what the pack decides.

| # | Question | Default | Fills |
|---|----------|---------|-------|
| 1 | What is the world for? | the pack the user's words point to | the pack |
| 2 | Its name, and the organisation's or AI's name | the organisation's name | `{{world_name}}`, `{{org}}`, the slug |
| 3 | Who is in it: each person, one neutral line on what they do, and their role (contributor by default) | only you | the Person Characters, each with its `seat` |
| 4 | Which AIs get a seat, and whose each is | one, yours, contributor | an Agent Character per AI, its `seat` naming its human (`ai_of`); the invites; the charter's "Who is here" |
| 5 | Who keeps the world: accepts proposals, tidies, adds supertypes | you | the Keeper Title, `{{keeper}}` |
| 6 | The pack's own seed question (each `PACK.md` names it) | the pack's default | the seed rows |
| 7 | A folder only, or also online on onlyworlds.com? | the folder now, online when ready | the placement: the plan's `online` (step 6) |
| 8 | Where the AI's copy of the world skill lands: the project folder the AI runs in, or your home folder for every session? And a one-line `AGENTS.md` there? | the folder the AI runs in; yes | step 4's copies |

## What gets created

```
<project>/                             # the folder the AI runs in (or the user's home, for every session)
├── .agents/skills/ow-<slug>/SKILL.md  # the harness copies of the world skill
├── .claude/skills/ow-<slug>/SKILL.md
├── AGENTS.md                          # one line, on the user's yes; appended if the file exists (the user's file)
└── <world-folder>/                    # the world itself; it may also BE the project folder
    ├── .gitattributes                 # every pack: LF, binaries marked
    ├── world.json                     # id, name, description, "charter": <the Law's id>, time in days; online, api.world_id
    └── elements/
        ├── law/charter.json           # the charter: Law, supertype Charter; carries x_checks_rules
        ├── object/<slug>-skill.json   # the world skill: Object, supertype Skill, its description the SKILL.md text
        └── <type>/<name>--<id8>.json  # the seed
```

**Where the copies go.** Every harness reads `.agents/skills/` and `.claude/skills/` from the folder it runs in up to the repository root, never from a sub-folder: so the copies go to the root the AI works in, and into the world folder only when the world folder is that root. `.agents/` and `.claude/` are dot-folders: a world-folder reader ignores them and an `.owworld` writer leaves them out, so a snapshot of the world never carries the copies. **The copies are the path that reaches every harness; the `AGENTS.md` line is a courtesy.** Two harness facts: Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists (where one does, the line goes there too); Gemini CLI reads `GEMINI.md` unless configured otherwise.

Every world folder gets the same `.gitattributes` (`* text=auto eol=lf`, binaries marked), so a world put in git on any machine keeps the writer rules' LF. A repository (`"repo": true`, the software-project pack's default) also gets a `.gitignore` that ignores every dot-folder except `.agents/` and `.claude/`, and its `world.json` never carries an `api` block: the key lives in each person's environment, never in the repository.

**The placement speaks.** The world skill and the charter are written for the placement the plan names. A folder world's skill names its folder and reads files; it holds no API route and no id as an address (the folder's minted id is not the online world's). An online world's skill names the server world id, and the charter's roster is `GET /members`. The texts mark their lines `<!-- if folder -->` and `<!-- if online -->`; the writer keeps one set.

## Steps

1. **Interview.** One message with the questions still open, defaults shown. A user who says "just do it" gets every default, and still sees the plan (step 3).
2. **Read the pack**: `packs/<pack>/PACK.md` first (who is in such a world, which types and supertypes and why, the size budget), then `charter.md`, `skill.md`, `seed.md`. Fill the placeholders from the answers. Seed only the rows the answers fill; list the rest as "left out".
3. **Show the plan, then write** (principles §2: propose, review, apply). The plan's first line names the owner and where that name came from: a name taken from the machine (the git user, `$USER`) is said there, never used silently. Show the charter text whole, the seed as a table, the skill's name and where its copies land. Write nothing until the user says yes, even when they asked for the defaults up front: the plan names people and a keeper, and only the user can confirm those. When question 7 says online, steps 6.1 and 6.2 come first: the user makes the empty world, and its id goes into the plan before it is shown, so step 4 writes the online texts the first time.
4. **Write the folder** with `scripts/write_world.py` (the plan's shape is in its header): it mints the ids, fills every placeholder before any shape test (`day:{{today}}` lands as a day number), refuses a `{{` left after filling with the file and line named, writes every file by the writer rules, marks each seat on its Character (`x_seat`) and lists the seats in the charter's "Who is here", checks the size budget, writes `x_checks_rules` on the charter (the checks slot, below), and writes the harness copies to the root the plan names (`"copies"`: a path, `"world"`, or `"none"`), with the `AGENTS.md` line beside them (appended to an existing `AGENTS.md`, and to a `CLAUDE.md` there; printed for the user when the root is their home). That line is one sentence, the writer's own, and the world skill quotes it as its courtesy line. It never writes into a world folder that already holds files, and never overwrites a copy.
5. **Check**: schema-dist's folder lint (`walk/lint_folder.py <folder>`, Python 3 with PyYAML, run from a fresh clone of schema-dist in a scratch directory (how: `knowledge/world-folder.md`, the check paragraph), never one found on the disk); its last line is the count it read. Then read the charter file back whole. The seed elements were approved in step 3, so they are written settled (no proposed mark).
6. **Online** (an account, and the user wants it):
   1. The user makes an empty world on onlyworlds.com first.
   2. Its id (no secret) goes into the plan as `online.world_id` before step 4, so the skill names the server's id and `world.json` carries it as `api.world_id` (not in a repository). A folder world that goes online later is written again from its plan, with `online`, into a fresh folder, and that one is uploaded: its skill and roster line are the online ones, and nothing online points at the old ids yet.
   3. Start's Connect an account connects a `.env` (the user types the key; never in chat).
   4. `write_world.py --bulk <file>` writes the upload's body.
   5. Develop's Bulk Upload sends the elements.
   6. `PATCH /api/v2/world` sets the time settings from `world.json` (`time_current` goes as `time_range_current`; the `charter` key stays in the folder, the server has no place for it).
   7. The same PATCH sets `owner_character` to the owner's Person.
   8. Read back `GET /api/v2/law?supertype=Charter`.
7. **Invites, made by the user on the world's page** (the screen's own words):
   - A person: the owner opens **Access**, then the card **Let someone in** (**A person**), and **By a link you send**: the role (**guest** is selected by default, **contributor** and **co-builder** are the others: pick the role the plan gave them), the expiry under **More options**, then **Make a link**. The link shows once; **Copy** copies it. The reader opens it, presses **Sign in to accept** or **New here? Create an account**, then **Join as** their role. The same card also invites by email address (**By email address**, then **Invite**): no email is sent, and the invite waits on their worlds page when they sign in with that address.
   - An AI: the owner opens **Access**, then **Let someone in**, **An AI agent**. Its first button, **Make an agent link**, makes a link the AI opens itself, making its own key with nothing for a `.env`; for `.env` lines, **More options** holds **A seat here**: a name, a role, its Character (**its own new Character**, selected by default, or **no Character**), then **Make a seat**. A member uses **Your AI in this world** on their own page of the world, **Make a seat**, with a role at most their own; the Character choice offers **its own new Character** (selected by default), **my Character** (their own, when they play one), or **no Character**. The `.env` lines show once; they go into the AI's own `.env`, never into a chat. Online, the seat makes the AI's Character (supertype `Agent`), so the writer leaves an AI's row out of an online world (the charter still names it); in a folder world, the seed holds it, marked `x_seat`.
8. **Report**: what was made (counts by type), what was left out and why, the charter's and skill's sizes against the budget (counted by a tool, `len()` or `wc -m` on the filled text, never estimated: two blank trials guessed low by several hundred), and the first visit an AI makes (the world skill's step-in).

## The checks slot

The charter file carries `x_checks_rules`, the checks profile's one field (`profiles/checks.md` in the schema distribution): the house rules a machine can check, written beside the sentences a person reads. Every pack writes it empty, `[]`, so a keeper finds it; the company pack ships one rule. A rule has three keys. `rule` is the charter's own sentence, which a report prints. `where` scopes the elements: `type` (one of the 22, lowercase, a string or a list), and optionally `supertype` and `subtype`. `require` names a `field` and exactly one predicate: `present: true`, `matches: "<regex>"`, `links_min: n` or `one_of: [...]`.

```json
{
  "rule": "every Character carries a reputation",
  "where": {"type": "character"},
  "require": {"field": "reputation", "present": true}
}
```

The profile's page has the rest (how each predicate counts, what a reader reports as not checked). The Python package `onlyworlds` (`pip install onlyworlds`, Python 3.12+) reads the slot and reports each rule: its sentence, how many elements it scoped, how many fall short. The command is `python -m onlyworlds.doctor <world folder>`, or `python -m onlyworlds.doctor --api` for an online world (key and PIN from `OW_API_KEY` and `OW_API_PIN`); it never writes. Add a rule only when the user gives one; a plan's `charter.x_checks_rules` replaces a pack's default.

## Checks

| Check | Pass |
|-------|------|
| Charter size | under 4,000 characters filled (every pack; `write_world.py` refuses over) |
| World skill size | under 9,000 characters filled (a comfort for the harness that loads the skill, not a limit of anything: a filled text must never refuse on a company's own names), front matter `name` and `description` only, name `ow-<world-slug>` (lowercase, hyphens, 64 at most) |
| Placeholders | none left: a `{{` after filling refuses the write, naming the file and line |
| Placement | a folder world's skill and charter hold no API route; an online world's skill names the server world id, never the minted one |
| Who is here | every seat named, each AI with its role word and its human; the keeper named |
| Lint | the folder lint's count line, no problems |
| Checks slot | the charter file carries `x_checks_rules`: a list, `[]` unless the pack ships a rule |
| Open work | in messages and work items, never in the charter's prose |
| Credentials | never in chat, never in `world.json` of a folder meant for a shared repository |

## Never

- Write a seed fact the user did not give. "Unsure" with the reason beats a guess.
- Write into an existing world's elements: this skill makes new worlds. Growing one is import, read's link lens or develop.
- Build a patch from a package copy. A patch file this skill writes for a world that already exists (a new charter text, a new world skill, for its keeper to land) starts from a fresh GET of that element and states the `updated_at` of the element it was built on, so the keeper sees drift before landing it.
- Put a person's private reads into the world: one neutral line on what each person does, written as they would accept it.

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- The plan's first line: the owner, and where that name came from (Step 3).
- The charter whole, the seed as a table, the skill's name and where its copies land, and nothing written before the user's yes (Step 3).
- The seed rows nobody answered, left out and named (Step 2).
- The report: counts by type, what was left out and why, the charter's and skill's sizes against the budget, counted and never estimated, the AI's first visit (Step 8).
- No key, PIN or seat line in chat (Step 6, 3; Step 7).
- The lint's count line and the charter read back whole (Step 5); what else was checked and how (principles §5); a script that could not run is said so (principles §2).
