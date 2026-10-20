---
name: onlyworlds-resolve
description: "Write each session back into the world so canon holds. Use when the user says 'update my world from these session notes', 'a character died in play', 'keep the AI from rewriting my lore'. For a first import use parsing."
---

# World Resolve

Help the user design THEIR way of resolving a finished session back into the world: what gets found, what becomes canon, who approves, how it is written, and how it is checked. Teach the principles, co-design the procedure, build the smallest working version. Do not install a one-size pipeline. The companion context skill covers the other half: loading the world into a session. For a one-off import of existing documents (a novel, old notes, a backlog of past sessions), use the parsing skill; resolve is the loop that follows every new session.

Shared rules (propose-review-apply, one writer, identity, field kinds, retire never delete, verify against the source) live in **knowledge/principles.md**; this skill applies them to writing a session back.

## Quick Reference

| Principle | The failure it prevents |
|---|---|
| Nothing is canon until resolved; the world does not move mid-session | the AI quietly rewriting canon while it writes or plays |
| Two closes: a quick handover every session, and the resolve | losing the thread, or never getting the world updated |
| List everything the session touched first, then give each a verdict | the facts nobody extracted, which every later check passes silently |
| Propose, review, apply (principles §2) | confidently wrong entries that everything downstream trusts |
| One writer of the world (principles §2) | two processes overwriting each other |
| Know each field's kind (principles §4) | a character's birthplace rewritten; a history log overwritten |
| Identity by what, where, who holds it (principles §3) | two people merged into one; the wrong sword updated |
| Evidence only; what a character says is their belief, not a world fact | a lie told in a scene becoming world truth |
| Contradictions surface as flags with both versions | the newer version silently winning |
| Retire, never delete (principles §2) | the past no longer answerable |
| Check after every resolve | drift that nobody notices for a month |

## Instructions

### Step 1: Diagnose (ask only what isn't already visible)

- **What does a session leave behind?** A transcript · written chapters · GM notes or a recap · a game log.
- **Where does the world live?** Documents · a notes vault · a database · an OnlyWorlds world.
- **What can the AI touch?** Chat only · a local agent with files · code and APIs.
- **How much review does the user want?** Every change · only the flagged ones · a sample.
- **What has gone wrong?** Their words. "It keeps rewriting my canon" and "I never update my notes" are different designs.

### Step 2: Pick the shape for their tier

| Tier | Their resolve procedure becomes |
|---|---|
| **Chat only** | an end-of-session prompt that outputs a change list in a fixed format; they review and apply it by hand or in their editor |
| **Local agent** | their own skill that lists what the session touched, writes a proposed change list to a file, waits for rulings, then applies the approved rows |
| **Code / API** | a listing script → proposal (structured output) → review → a mechanical writer → checks |

In every tier the change list is the artifact: readable, reviewable, kept.

### Step 3: Learn how the world keeps its fields

Field kinds (replaced, appended with a dated line, never touched) are defined in principles §4. The job here is to find THIS world's: look at how it was updated before (a previous session's edits, version history, or a few elements of each type) and write down, per type, which fields are which and where standing rules and secrets live. If the world has a world rules file from a parse (the parsing skill, Step 2), this belongs in it, beside the taxonomy the resolve should keep using. A resolve proposes nothing in a never-touched field without a flag.

### Step 4: Design the procedure together

Write each answer into a file in their project (e.g. `resolve-procedure.md`). The file is the deliverable. Propose a default for each item from what you can see and ask the user only for the rulings; a user with a session's notes in hand can resolve that session first and fill the procedure from it.

1. **The handover** (cheap, every session): where everyone is, what is unresolved, what is tentative, secrets not yet revealed. The next session can continue from it before any resolve runs. Keep each one.
2. **The listing** (code, where possible): every named thing the session mentions, matched against the world (names, aliases, titles); names that match nothing; unnamed figures who recur ("the ferryman"); threads whose subject came up. Nothing enters the proposal that the listing didn't surface, and nothing the listing surfaced is left without a verdict.
3. **The verdicts.** Each listed item gets one: *changed* (a row follows), *touched* (present, nothing changed), or *no change* with a short reason (no change is a decision, not a default). Each unmatched name gets one: a new entry, an alias of an existing one, or noise. New entries follow the rule: recurs, named, or matters, and are extracted with the parsing skill's rules (Key Rules and Step 3: type, decomposition, fields before elements, the world's own taxonomy). A one-off becomes a line on its place or event, or nothing.
4. **The passes**, in this order:
   - new entries first (so later rows can link to them)
   - where everyone ended up (every present character's final place against their location field)
   - what happened (events: who, where, when in the world). A tool that writes play back puts every participant on each Event it mints and stamps `start_date` in the world's own time unit; finer ordering stays in the tool. The reason: in a parsed Curse of Strahd, 78% of the "was there" links already mean "knows", and only 2% of the Events carry a date, so no reader can say what happened before what.
   - what changed (in each field's own kind: replace, append a dated line, or flag)
   - threads: advanced only when their next step actually happened, not when they were mentioned
   - who learned what: a first telling, a witnessed secret, a discovery becomes knowledge held by that character or group (a group needs a knower-group first, e.g. a party Collective with the player characters as members). An entry inferred rather than witnessed (she was at the battle, so she knows who won) links its `events` to the Events it was inferred from, so a reader can trace it back to them
   - what finished (the dead, the departed, the resolved): retired with a date so context stops picking them by default
5. **The row format**: one line per change, from a small fixed set of operations (create · update · append · link · retire · event · knowledge · flag), with target, old and new value, and evidence (a quote or a pointer into the session). Keep a short list of what was deliberately NOT proposed, and why.
6. **Identity before names.** Before an existing element's name goes into a row, confirm it is the same thing (principles §3). A different referent is a collision note, never an edit.
7. **Flags**: ambiguity, near-names, contradictions with canon, anything that might be a mistake. Rule them by reading the session, never the proposer's summary. A proposal with zero flags deserves suspicion. Contradiction is sometimes the world: rumours, lies, and disputed histories are content, recorded as what someone believes.
8. **Canon status.** Decide the levels the user wants (e.g. draft / established / locked). Promotion to canon is an explicit decision in review.
9. **Who writes.** One process applies the approved rows, merging (principles §2).
10. **The checks**: every listed item has a verdict; every *no change* has its reason, and a few are spot-checked against the session; every link points at something real; every place is a real place; nothing identity-level changed without a ruling. After applying, read back what landed and compare it with the approved rows, not with a copy just made (principles §5). Passages the user chose to skip are reported as a coverage gap, with their count. Add a check every time a mistake slips through; never remove one.

### Step 5: Build the smallest working version

- **Chat only**: the end-of-session prompt and the row template; resolve one real session together.
- **Local agent / code**: their skill or script. The listing and the checks are code; the verdicts are the model's; the rulings are the human's; the writer only applies what was approved.

### Step 6: Run it once and read it

Resolve one real session. Walk the rows with the user. A ruling they had to invent on the spot belongs in the procedure file. Test in a fresh session with no project memory or instructions; one that knows the project fills gaps the session does not.

### Step 7: Name the next rung

- **history in git**: commit the world folder after each resolve, with the change list as the message; `main` is canon and a branch is a timeline (a what-if, an alternate ending). A linked folder holds its API key in `world.json`'s `api` block, so read the credentials line before pushing anywhere (see **knowledge/world-folder.md**, keeping history)
- **recall testing**: resolve a session whose correct result is known, and compare; consistency checks cannot see a dropped fact
- **resolve in story order** when several sessions are pending
- **derived views** (timelines, relationship registers) computed from the kept change lists instead of maintained by hand

## Critical Rules

- ❌ Letting the session AI edit the world mid-session ✅ write or play freely, resolve afterwards
- ❌ Starting from "what seems important" ✅ start from the full listing; every item gets a verdict
- ❌ Replacing a record with a freshly extracted version ✅ merge; update only the fields the row names
- ❌ Overwriting canon when the session disagrees ✅ a flag with both versions, and a recorded ruling
- ❌ Hand-maintaining summaries that could be computed ✅ derive them, or they drift within a week

## Example (Hyperion)

After the session where the Consul receives the fatline message:

```
LISTING: The Consul (touched) · Meina Gladstone (touched) · The Shrike Pilgrimage (changed) ·
         The Time Tombs (mentioned) · "the Home Rule Council" (no match: new entry or noise?)
ROWS:
  link      The Shrike Pilgrimage.characters  + The Consul      evidence: "You have been chosen..."
  knowledge "The Time Tombs show signs of opening"  held by: The Consul   evidence: Gladstone's message
  flag      Has the Consul accepted? The session ends before he answers. Leave the pilgrimage row as "chosen"?
NOT PROPOSED: the storm, the carrion-breed pack (background, no recurrence)
```

## Where OnlyWorlds Helps (optional)

| Resolve need | OnlyWorlds field |
|---|---|
| the session itself, verbatim | `Narrative.story`, with `events`, `characters`, `parent_narrative` (campaign → session) |
| what happened | `Event` (`characters`, `locations`, `start_date`, `triggers`, `consequences`) |
| someone moved | `Character.location` |
| a relationship changed | `Relation` (`intensity`, `start_date`, `end_date`, `events`) |
| who learned what | a knowledge entry: `Narrative` with subtype `knowledge`, held by `narrator`, `collectives`, or both; a rumour and the truth are separate entries held by different people. See **knowledge/atlas-conventions.md** |
| a death | Creature `status`; Character: the `[Deceased]` prefix on `physicality` (the schema skill holds the convention) |
| canon status, custom state | `x_*` extension fields |
| verbatim vs editorial | a Narrative's `story` (the only type with that field) vs any element's `description` |

Every-line happenings (each exchange, each roll) go in a log beside the world, not in elements (principles §1). That log points at element ids, never copies of element text; a tool that follows the change feed (`/changes`) applies its delete rows, so an element gone from the world goes from the tool. To write: edit files in a world folder (see **knowledge/world-folder.md**, writer rules; in a folder linked to an account, every edited file gets a fresh `local_updated_at`), or use the API or MCP (the api skill; **knowledge/ai-builders.md**); multi-link changes go through the links route, and anything else is read before it is written.

## References

- **knowledge/world-memory.md**: the full loop, the dials, failure modes by name, and how other tools and tabletop practice do it
