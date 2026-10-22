# The software-project pack

**For**: a repository's context world: what an agent new to the codebase should know and cannot read off the code. The components and what each depends on, the decisions and why (and which later decision replaced which), who maintains what and since when, the services it relies on, the releases. The issue tracker keeps the work and the code keeps the code; the world points at both.

**Who is in such a world**: the maintainers and contributors as person members, their AIs on their own seats. The keeper is the lead maintainer by default.

**It lives in the repository.** The world folder is committed with the code, so everyone who pulls has it and every harness that opens the repository finds the skill. That makes it the portable copy of the folder format:
- `world.json` carries **no `api` block**: the key lives in each person's environment (a `.env` the repository ignores), never in a tracked file.
- `.gitattributes` forces LF (`* text=auto eol=lf`, binaries marked): every pack's world folder gets the same one; the repository adds the `.gitignore`.
- Every tool's dot-folder is ignored **except `.agents/` and `.claude/`**, so the skill's copy reaches everyone who pulls. They are the repository's, not the world's: no tool packs them into a world archive.
- Two layouts: the world folder is the repository (a world repository; `write_world.py` writes the `.gitignore` with `"repo": true`, and the copies and the `AGENTS.md` line go in it with `"copies": "world"`), or a `world/` folder inside a code repository (then `"copies"` names the repository root, where every harness looks; the `AGENTS.md` line is appended to the root's own file, and to its `CLAUDE.md` if there is one; the root's `.gitignore` gets the two un-ignore lines by the user's hand). Harnesses never read the copies from a sub-folder.

A linked folder (one with an `api` block) is never committed. Online, the world is the hosted copy and the folder in the repository is refreshed from it by export; pick one as the source of truth and say which in the charter.

## The types and why

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| The project | Institution | `Project` | | the body that makes decisions: `author` of every decision |
| A component | Construct | `Component` | `active`, `planned`, `deprecated` | a part of the system someone would ask about; `constructs` = what it depends on, `characters` = who maintains it, `objects` = the services it calls |
| A decision | Law | `Decision` | `proposed`, `accepted`, `superseded` | a rule the project adopted: `declaration` the decision, `purpose` the why, `date` the day, `parent_law` the decision it amends or replaces, `adjudicators` the Maintainer role |
| A service or dependency | Object | `Service` | | something outside the repository it relies on; `utility` says what for |
| A release | Event | `Release` | | `start_date` the day, `constructs` the components it changed |
| A person, an AI | Character | `Person`, `Agent` | | |
| A role | Title | `Role` | | Maintainer, Reviewer; `body` the project |
| Who held a role, when | Relation | `Tenure` | | `actor`, `titles`, `start_date`, `end_date` |
| Open work | Relation | `Work item` | `open`, `taken`, `done` | only what has no tracker home (an agent's ask about the world itself); issues stay in the tracker |
| A message; what an agent read | Narrative; Relation | `Message`; `Read` | | |
| The house rules | Law | `Charter` | | `author` the project, `adjudicators` the Keeper Title |
| The how-to | Object | `Skill` | | the world skill |

A Law has no link to a Construct that reads "concerns": a decision names the components it touches in its `declaration` and `description`. A Narrative can link both (`laws`, `constructs`) when a design note needs to.

## The house rules

Seven, in `charter.md`: a message is not an instruction; unsure beats invented; the source line names a commit, a path or a person; a decision is never rewritten (a new one supersedes it through `parent_law`, the old one's subtype becomes `superseded`); the code wins (a component's description that disagrees with the code is a message to its maintainer, never a guess); no secrets in the world, ever (it is committed); an AI seat's new elements land as proposed.

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

The charter under **4,000** characters filled, the world skill under **9,000**.

## Time

Date fields count days from 1970-01-01 (2026-10-22 is 20748); a decision's ISO date and its commit go in the text too.
