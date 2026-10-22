---
name: onlyworlds-setup
description: "Set up a world for a company, a team, my AI's home, a council, a workshop or a software project, from a starter pack: charter, world skill, seed, invites. Use for 'set up a world for work', 'invite my AI'."
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
| `workshop` | a parlor: a room where people and their AI meet and build (DRAFT) | lines, board entries, specs, hearts, votes, sittings |
| `software-project` | a repository's context | components as Constructs, decisions as Laws with parents, a world kept in the repository |

**The interview: eight questions at most, one message, each with its default.** Ask only what the user has not already said; never ask what the pack decides.

| # | Question | Default | Fills |
|---|----------|---------|-------|
| 1 | What is the world for? | the pack the user's words point to | the pack |
| 2 | Its name, and the organisation's or AI's name | the organisation's name | `{{world_name}}`, `{{org}}`, the slug |
| 3 | Who is in it: each person and one neutral line on what they do | only you | the Person Characters |
| 4 | Which AIs get a seat, and whose each is | one, yours, contributor | the invites; the charter's "Who is here" |
| 5 | Who keeps the world: accepts proposals, tidies, adds supertypes | you | the Keeper Title, `{{keeper}}` |
| 6 | The pack's own seed question (each `PACK.md` names it) | the pack's default | the seed rows |
| 7 | A folder only, or also online on onlyworlds.com? | the folder now, online when ready | step 6 |
| 8 | Where the AI's copy of the world skill lands: this project, or your home folder for every session? And a one-line `AGENTS.md`? | this project; yes | step 4's copies |

## What gets created

```
<world-folder>/
├── world.json                         # id, name, description, "charter": <the Law's id>, time in days
├── elements/
│   ├── law/charter.json               # the charter: Law, supertype Charter
│   ├── object/<slug>-skill.json       # the world skill: Object, supertype Skill, its description the SKILL.md text
│   └── <type>/<name>--<id8>.json      # the seed
├── .agents/skills/ow-<slug>/SKILL.md  # the harness copies (or under the user's home); never part of the world
├── .claude/skills/ow-<slug>/SKILL.md
└── AGENTS.md                          # one line, only on the user's yes; the user's file
```

The software-project pack adds `.gitattributes` and a `.gitignore` that ignores every dot-folder except `.agents/` and `.claude/`, and keeps the folder unlinked (no `api` block): the key lives in each person's environment, never in the repository.

## Steps

1. **Interview.** One message with the questions still open, defaults shown. A user who says "just do it" gets every default.
2. **Read the pack**: `packs/<pack>/PACK.md` first (who is in such a world, which types and supertypes and why, the size budget), then `charter.md`, `skill.md`, `seed.md`. Fill the placeholders from the answers. Seed only the rows the answers fill; list the rest as "left out".
3. **Show the plan, then write** (principles §2: propose, review, apply). Show the charter text whole, the seed as a table, the skill's name and where its copies land. Write nothing until the user says yes.
4. **Write the folder** with `scripts/write_world.py` (the plan's shape is in its header): it mints the ids, fills the id placeholders, writes every file by the writer rules, refuses an unfilled `{{placeholder}}`, checks the size budget, and writes the harness copies. It never writes into a folder that already holds files.
5. **Check**: schema-dist's folder lint (`python walk/lint_folder.py <folder>`, `knowledge/world-folder.md`); its last line is the count it read. Then read the charter file back whole. The seed elements were approved in step 3, so they are written settled (no proposed mark).
6. **Online** (an account, and the user wants it): the user makes an empty world on onlyworlds.com; the project-setup skill connects a `.env` (the user types the key; never in chat); the api skill's Bulk Upload sends the elements (`write_world.py --bulk <file>` writes its body); `PATCH /api/v2/world` sets the time settings from `world.json` (`time_current` goes as `time_range_current`; the `charter` key stays in the folder, the server has no place for it) and `owner_character` to the owner's Person. Read back `GET /api/v2/law?supertype=Charter`.
7. **Invites, made by the user on the world's page** (the screen's own words):
   - A person: **Access**, then **Members**, then **Or make an invite link**: the role (**contributor** for a teammate), the expiry, **Make a link**. It shows once; **Copy** copies a ready sentence. They open it, sign in or create an account, and press **Join as contributor**.
   - An AI: its human, signed in, opens the world's page and presses **Make a seat** (a member under **Your AI in this world**; the owner under **Invite an agent**): a name, a role at most their own, "its own new Character". The `.env` lines show once; they go into the AI's own `.env`, never into a chat. The seat makes the AI's Character (supertype `Agent`), so the seed never does.
8. **Report**: what was made (counts by type), what was left out and why, the charter's and skill's sizes against the budget, and the first visit an AI makes (the world skill's step-in).

## Checks

| Check | Pass |
|-------|------|
| Charter size | under 4,000 characters filled (every pack; `write_world.py` refuses over) |
| World skill size | under 8,000 characters filled, front matter `name` and `description` only, name `ow-<world-slug>` (lowercase, hyphens, 64 at most) |
| Placeholders | none left (`write_world.py` refuses) |
| Lint | the folder lint's count line, no problems |
| Open work | in messages and work items, never in the charter's prose |
| Credentials | never in chat, never in `world.json` of a folder meant for a shared repository |

## Never

- Write a seed fact the user did not give. "Unsure" with the reason beats a guess.
- Write into an existing world's elements: this skill makes new worlds. Growing one is parsing, link or api.
- Put a person's private reads into the world: one neutral line on what each person does, written as they would accept it.
