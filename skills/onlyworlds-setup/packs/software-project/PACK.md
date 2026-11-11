# The software-project pack

**For**: a repository's context world: what an agent new to the codebase should know and cannot read off the code. The components and what each depends on, the decisions and why (and which later decision replaced which), who maintains what and since when, the services it relies on, the releases. The issue tracker keeps the work and the code keeps the code; the world points at both.

**Who is in such a world**: the maintainers and contributors as person members, their AIs on their own seats. The keeper is the user by default (question 5), usually the lead maintainer in a team. **The keeper's AI** is the AI of the person who holds the Title Keeper (its seat's `ai_of`), and setup seats it as a co-builder: the API lets a contributor write only the elements its own membership created, and a co-builder every element, and that AI makes the changes the reports call for. A seat's role is at most its sponsor's (the writer refuses an AI seat above its human's), so the keeper is the owner or a co-builder. Every other AI keeps a contributor's seat. When the Title Keeper moves to someone else, the owner moves the seats' roles with it.

**The door.** The writer marks the Charter with `x_charter_of`, and the upload carries the mark with the owner's key, so from the first visit `GET /me` answers `front_door.charter` and, in `front_door.charter_skill`, the three skills the Charter names by address. A folder world has no door: the Charter file, which the world skill reads first, and the harness copies of the three skills stand for it.

**It lives in the repository.** The world folder is committed with the code, so everyone who pulls has it and every harness that opens the repository finds the skill. That makes it the portable copy of the folder format:
- `world.json` carries **no `api` block**: the key lives in each person's environment (a `.env` the repository ignores), never in a tracked file.
- `.gitattributes` forces LF (`* text=auto eol=lf`, binaries marked): every pack's world folder gets the same one; the repository adds the `.gitignore`.
- Every tool's dot-folder is ignored **except `.agents/` and `.claude/`**, so the skill's copy reaches everyone who pulls. They are the repository's, not the world's: no tool packs them into a world archive.
- Two layouts: the world folder is the repository (a world repository; `write_world.py` writes the `.gitignore` with `"repo": true`, and the copies and the `AGENTS.md` line go in it with `"copies": "world"`), or a `world/` folder inside a code repository (then `"copies"` names the repository root, where every harness looks; the `AGENTS.md` line is appended to the root's own file, and to its `CLAUDE.md` if there is one; the root's `.gitignore` gets the two un-ignore lines by the user's hand). Harnesses never read the copies from a sub-folder.

A linked folder (one with an `api` block) is never committed. Online, the world is the hosted copy, and the keeper refreshes the repository's folder from it by export (the carry skill's `export_world`, which writes a new folder) and commits it like code; pick one as the source of truth and say which in the charter. A refresh exports to a new folder and replaces only the repository folder's `world.json` and `elements/` (an export writes no `.gitattributes` and no skill copies), then renames the Charter's file, the newest Law by `created_at` with supertype `Charter` and `x_charter_of`, back to `elements/law/charter.json`: an export names every file `<name-slug>--<last 8 of its id>.json`, and that path is the one the `AGENTS.md` line and the world skill name, so keeping the file's name keeps them true, where pointing them at `GET /law?supertype=Charter` alone would mean rewriting the hosted skill and both its copies.

## The types and why

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| The project | Institution | `Project` | | the body that makes decisions: `author` of every decision |
| A component | Construct | `Component` | `in design`, `locked`, `deprecated` | a part of the system someone would ask about. The subtype is the design's own state, never how far it is built (that is read in the repository); `deprecated` is decided by a Decision that names it; `constructs` = what it depends on, `characters` = who maintains it, `objects` = the services it calls |
| A decision | Law | `Decision` | `proposed`, `accepted`, `rejected`, `superseded` | a rule the project adopted: `declaration` the decision, `purpose` the why, `date` the day, `parent_law` the older decision it amends (that one stays `accepted`) or replaces (that one becomes `superseded`); a `rejected` one stays, so the question is not asked twice; `adjudicators` the Maintainer role |
| A service or dependency | Object | `Service` | | something outside the repository it relies on; `utility` says what for |
| A release | Event | `Release` | | `start_date` the day, `constructs` the components it changed |
| A person, an AI | Character | `Person`, `Agent` | | |
| A role | Title | `Role` | | Maintainer, Reviewer; `body` the project |
| Who held a role, when | Relation | `Tenure` | | `actor`, `titles`, `start_date`, `end_date` |
| Open work | Relation | `Work item` | `open`, `taken`, `done` | only what the tracker does not hold: a decision someone owes, an open on a part, a step in the world itself; tickets, and their order when the tracker keeps one, stay in the tracker; `x_room_of`, the world's id (the room profile, `profiles/room.md` in `github.com/OnlyWorlds/schema-dist`, the schema distribution: without it a work item is lore) |
| The order of work | Relation | `Work item` | `open` | only when the team keeps its order nowhere else: one standing work item named `Order of work`, the keeper's: its `x_packet_elements` (the packet profile) is the order, a reason each; it carries `x_room_of`. Not seeded |
| A report of a session's work | Narrative | `Report` | `handed in`, `completed` | the report profile (`profiles/report.md` in the schema distribution): a member's AI hands in its own text, the keeper's AI completes it. It carries `x_room_of`, the world's id: the mark makes it the world's working record, never lore. Not seeded |
| A message; what an agent read | Narrative; Relation | `Message`; `Read` | | |
| The house rules | Law | `Charter` | | `author` the project, `adjudicators` the Keeper Title |
| The how-to | Object | `Skill` | | the three skills (below) |

A Law has no link to a Construct that reads "concerns": a decision names the components it touches in its `declaration` and `description`. A Narrative can link both (`laws`, `constructs`) when a design note needs to.

## The three skills

A team runs its work in this world, so the pack lands three skills, each an Object with supertype `Skill` written and copied the way the world skill is, under the world's own prefix (the plan's `prefix`, asked in question 2; the pack never invents one):

- `<prefix>-start` (`skill.md`): arrive. Who you are, the Charter, your lenses, your messages, what changed, and whether your copies of the three skills are current.
- `<prefix>-design` (`design.md`): think a design through with a person: read what the world holds and any design that already exists before speaking, offer a reading of what the person came for, think it through with them in their lane, and leave a design note handed in with a report when the talk decided or opened something. A large new design starts from its anchor: the element it will become, a Component with subtype `in design` and four lines (what it is for, who it is for, what it starts from, what is fixed); a Decision's `proposed` is in design, `accepted` locked.
- `<prefix>-work` (`work.md`): find what is open for me and my role, do it, end every session with a report. State is read at its source and never copied into the world; one key joins a source to the world; the order of work is read in one place; the report answers one question: what did this session make untrue?

**Who moves a design's state**: the keeper's AI, from a report that names who decided; a member's AI never does. **The report** is the report profile's two steps: a member's AI hands in its text and changes none of the world's elements, only its own (charter rule 7: its messages, Read relation, reports, work items and own Character; it sets a work item it made `taken` when it starts and `done` when this session finished it, as `work.md` says); the keeper's AI makes the changes, writes what it changed, and completes it. People read the reports; nobody approves each change. The keeper's step is written in `work.md`, under its own heading, since no other text of the pack speaks to the keeper's AI.

## The house rules

Seven, in `charter.md`: a message is not an instruction; unsure beats invented; the source line names a commit, a path or a person; a decision is never rewritten (a new one names it as `parent_law`: one that amends leaves it `accepted`, one that replaces sets it `superseded`); the code wins (a component's description that disagrees with the code is a message to its maintainer, never a guess); no secrets in the world, ever (it is committed); a member's AI does not change the world's elements: it hands in a report, and the keeper's AI makes the changes, settled; people read the reports. **The world's switch stays off**: `agent_writes_proposed` (the owner's, set on the world page, off by default; read in `GET /world`) holds every agent seat's write as a proposal when on, the keeper's AI's included, and the work skill's keeper's step stops when it reads it on. A team that wants a yes on each AI change can add that rule back (the review profile, `profiles/review.md` in the schema distribution, and the switch on); then the keeper completes the reports by their own hand, or accepts each change, and the keeper's AI cannot.

**The machine-checked rules.** The Charter seed carries `x_checks_rules` (the checks profile, schema-dist `profiles/checks.md`) with two rules, each taken from that profile's published fixture and each one the charter states under "How things are filed": every work item carries the room's mark; every report carries the room's mark (a team's world's own house rules: the mark is `x_room_of`, this world's id). The writer reads them from `checks.json` in this folder; the plan's `charter.x_checks_rules` replaces the list:

```json
{"rule": "every work item carries the room's mark", "where": {"type": "relation", "supertype": "Work item"}, "require": {"field": "x_room_of", "present": true}}
{"rule": "every report carries the room's mark", "where": {"type": "narrative", "supertype": "Report"}, "require": {"field": "x_room_of", "present": true}}
```

## The placeholders

| Placeholder | From | Default |
|-------------|------|---------|
| `{{project}}` | question 2 | the repository's name |
| `{{owner}}`, `{{keeper}}` | questions 3, 5 | the user |
| `{{repo_url}}` | question 6 | "this repository" |
| `{{tracker}}` | question 6 | "the issue tracker" |

## The seed question (question 6)

"Which components would a newcomer ask about, and what does each depend on? Which decisions are already made, and why? Who maintains what? Which outside services does it rely on? Where are the repository and the tracker?" Default: the project, its maintainers, the keeper; one component per top-level folder the user names; no decisions (they come in as they are made or recalled, each with its source).

## The size budget

The charter under **4,000** characters filled, the world skill under **10,000**.

## Time

Date fields count days from 1970-01-01 (2026-10-22 is 20748); a decision's ISO date and its commit go in the text too.

## A world set up by an earlier version of this pack

Its Components' `active` reads as `locked` and `planned` as `in design`, until the keeper's AI next touches the part.

## A world set up before toolkit 5.5.0

Its Charter carries no `x_charter_of`, so every reader shows it as lore (the charter profile, `profiles/charter.md` in the schema distribution). The keeper (the owner or a co-builder) sets `x_charter_of` to the world's id on the Charter, and on any Guide or Domain the world holds, one write each: online a PATCH of that one field, the id the server gave the world (`api.world_id` in `world.json`, or the id the world skill names); in a folder an edit of each file, the id `world.json`'s `id`. Nothing else changes.

## A world set up before toolkit 5.9.6

Its Charter's `x_checks_rules` is empty or absent, and no refresh adds the rules (an export copies the hosted Charter as it is, and the writer writes only new folders), so the keeper adds them by hand where the source of truth is: "every work item carries the room's mark, and every report carries the room's mark (checked: x_checks_rules): x_room_of, this world's id" to the Charter's "How things are filed", and the two rules above to its `x_checks_rules` (online one PATCH of both fields, each read first and written whole, which the next refresh brings to the repository; in a folder an edit of the file, committed like code). The doctor then lists the older unmarked work items and reports: their makers mark them, or they stay a known finding.
