---
name: onlyworlds-update
description: "Write a finished session, or a finished chapter or scene, back into the world so canon holds. Use when the user says 'update my world from these session notes', 'I finished chapter 14, update my files', 'a character died in play', 'turn last night's recap into canon', 'keep the AI from rewriting my lore'. Lists what the session touched, proposes a change list, writes only what the user approves. For a first import of existing material, use import."
---

# OnlyWorlds Update

Updating the world from a finished session is the resolve: list what the session touched, give each item a verdict, propose a change list, and write only the rows the user approves. Help the user design THEIR way of doing it: what gets found, what becomes canon, who approves, how it is written, and how it is checked. Teach the principles, co-design the procedure, build the smallest working version. Do not install a one-size pipeline. The context skill covers the other half: loading the world into a session. For a one-off import of existing documents (a novel, old notes, a backlog of past sessions), use the import skill; the update is the loop that follows every new session. A single edit the user dictates ("make the Consul tired") is not a session: make it directly, merged, with no change list.

Shared rules (propose-review-apply, one writer, identity, field kinds, retire never delete, verify against the source) live in `knowledge/principles.md`; this skill applies them to writing a session back.

## Quick Reference

| Principle | The failure it prevents |
|---|---|
| Nothing is canon until the update; the world does not move mid-session | the AI quietly rewriting canon while it writes or plays |
| Two closes: a quick handover every session, and the update | losing the thread, or never getting the world updated |
| List everything the session touched first, then give each a verdict | the facts nobody extracted, which every later check passes silently |
| Propose, review, apply (principles §2) | confidently wrong entries that everything downstream trusts |
| One writer of the world (principles §2) | two processes overwriting each other |
| Know each field's kind (principles §4) | a character's birthplace rewritten; a history log overwritten |
| Identity by what, where, who holds it (principles §3) | two people merged into one; the wrong sword updated |
| Evidence only; what a character says is their belief, not a world fact | a lie told in a scene becoming world truth |
| Contradictions surface as flags with both versions | the newer version silently winning |
| Retire, never delete (principles §2) | the past no longer answerable |
| A write that comes back as a proposal is reported, never resent | the same change queued twice for the world's keeper |
| Check after every update | drift that nobody notices for a month |

## Instructions

### Step 1: Diagnose (ask only what isn't already visible)

- **What does a session leave behind?** A transcript · written chapters · GM notes or a recap · a game log.
- **Where does the world live?** Documents · a notes vault · a world folder · an OnlyWorlds account world.
- **What can the AI touch?** Chat only · a local agent with files · code and APIs.
- **How much review does the user want?** Every change · only the flagged ones · a sample.
- **What has gone wrong?** Their words. "It keeps rewriting my canon" and "I never update my notes" are different designs.

**A session in hand** ("we played last night, here are my notes, update the world"): resolve that session first and design the procedure from it afterwards. Read the world (and its world rules file, if it has one), then run Step 4's listing, verdicts, passes and flags against the notes, and write the change list in Step 4's row format to a file beside the notes (`session-3-changes.md`), never inside the world's `elements/`. Then stop: nothing in the world changes until the user has ruled on the rows, and then only the approved rows are written, as Step 4's "Who writes" says (the writer rules, then the read-back). What they had to rule on the spot is the first draft of their procedure file.

### Step 2: Pick the shape for their tier

| Tier | Their update procedure becomes |
|---|---|
| **Chat only** | an end-of-session prompt that outputs a change list in a fixed format; they review and apply it by hand or in their editor |
| **Local agent** | their own skill that lists what the session touched, writes a proposed change list to a file, waits for rulings, then applies the approved rows |
| **Code / API** | a listing script → proposal (structured output) → review → a mechanical writer → checks |

In every tier the change list is the artifact: readable, reviewable, kept.

### Step 3: Learn how the world keeps its fields

Field kinds (replaced, appended with a dated line, never touched) are defined in principles §4. The job here is to find THIS world's: look at how it was updated before (a previous session's edits, version history, or a few elements of each type) and write down, per type, which fields are which and where standing rules and secrets live. Which fields a type has at all, and what each link field points at, is the type's section of `knowledge/schema-reference.md`. If the world has a world rules file from an import (import's Step 2), this belongs in it, beside the taxonomy the update should keep using. An update proposes nothing in a never-touched field without a flag.

### Step 4: Design the procedure together

Write each answer into a file in their project (e.g. `update-procedure.md`). The file is the deliverable. Propose a default for each item from what you can see and ask the user only for the rulings; a user with a session's notes in hand resolves that session first (Step 1) and fills the procedure from it.

1. **The handover** (cheap, every session): where everyone is, what is unresolved, what is tentative, secrets not yet revealed. The next session can continue from it before any update runs. Keep each one.
2. **The listing** (code, where possible): every named thing the session mentions, matched against the world (names, aliases, titles); names that match nothing; unnamed figures who recur ("the ferryman"); threads whose subject came up. Nothing enters the proposal that the listing didn't surface, and nothing the listing surfaced is left without a verdict.
3. **The verdicts.** Each listed item gets one: *changed* (a row follows), *touched* (present, nothing changed), or *no change* with a short reason (no change is a decision, not a default). Each unmatched name gets one: a new entry, an alias of an existing one, or noise. New entries follow the rule: recurs, named, or matters, and are extracted by the import skill's rules (its Key Rules and Step 3: type, decomposition, fields before elements, the world's own taxonomy). A one-off becomes a line on its place or event, or nothing.
4. **The passes**, in this order:
   - new entries first (so later rows can link to them)
   - where everyone ended up (every present character's final place against their location field)
   - what happened (events: who, where, when in the world). A tool that writes play back puts every participant on each Event it mints and stamps `start_date` in the world's own time unit; finer ordering stays in the tool. The reason: an Event without its participants or a date leaves no reader able to say who was there or what happened before what.
   - what changed (in each field's own kind: replace, append a dated line, or flag)
   - threads: advanced only when their next step actually happened, not when they were mentioned
   - who learned what: a first telling, a witnessed secret, a discovery becomes knowledge held by that character or group (a group needs a knower-group first, e.g. a party Collective with the player characters as members). An entry inferred rather than witnessed (she was at the battle, so she knows who won) links its `events` to the Events it was inferred from, so a reader can trace it back to them
   - what finished (the dead, the departed, the resolved): retired by the field's own marker, so context stops picking them by default: a Character's death as model's "Marking a Dead Character" says (the one home of that convention), an `end_date` on a Relation or Event, a Title's `revoke_date`
5. **The row format**: one line per change, from a small fixed set of operations (create · update · append · link · retire · event · knowledge · flag), with target, old and new value, and evidence (a quote or a pointer into the session). Keep a short list of what was deliberately NOT proposed, and why.
6. **Identity before names.** Before an existing element's name goes into a row, confirm it is the same thing (principles §3). A different referent is a collision note, never an edit.
7. **Flags**: ambiguity, near-names, contradictions with canon, a link whose target is the wrong type for its field, anything that might be a mistake. Rule them by reading the session, never the proposer's summary. A proposal with zero flags deserves suspicion. Contradiction is sometimes the world: rumours, lies, and disputed histories are content, recorded as what someone believes.
8. **Canon status.** Decide the levels the user wants (e.g. draft / established / locked). Promotion to canon is an explicit decision in review.
9. **Who writes.** Before the first write, a snapshot: commit the world folder, or export the account world to a folder (`knowledge/world-folder.md`); with it, and the old value every row keeps, any write can be undone. Then one process applies only the approved rows, the ones the user passed in principles §2's "Propose, review, apply", merging (principles §2), by the writer rules ("To write", below), and reads back what landed (the checks). A session kept as a Narrative of its own goes, as `knowledge/atlas-conventions.md` says under "Prose: the writing room", "usually at the scene tier under the campaign's chapter"; in a world with no narratives yet, "the person says where a new one goes".
10. **The checks**: every listed item has a verdict; every *no change* has its reason, and a few are spot-checked against the session; every link points at something real, of the type its field takes (`single-link → T` in the schema reference: a Character's `location` takes a Location, never an Object); every place is a real place; nothing identity-level changed without a ruling. After applying, read back what landed and compare it with the approved rows, not with a copy just made (principles §5). Passages the user chose to skip are reported as a coverage gap, with their count. Add a check every time a mistake slips through; never remove one.

### Step 5: Build the smallest working version

- **Chat only**: the end-of-session prompt and the row template; resolve one real session together.
- **Local agent / code**: their skill or script. The listing and the checks are code; the verdicts are the model's; the rulings are the human's; the writer only applies what was approved.

### Step 6: Run it once and read it

Resolve one real session. Walk the rows with the user. A ruling they had to invent on the spot belongs in the procedure file. Test in a fresh session with no project memory or instructions; one that knows the project fills gaps the session does not.

### Step 7: Name the next rung

- **history in git**: commit the world folder after each update, with the change list as the message; `main` is canon and a branch is a timeline (a what-if, an alternate ending). A folder linked to an account holds its API key in `world.json`'s `api` block and is never committed: version an unlinked copy (`knowledge/world-folder.md`, keeping history)
- **recall testing**: resolve a session whose correct result is known, and compare; read's consistency report cannot see a dropped fact
- **resolve in story order** when several sessions are pending
- **derived views** (timelines, relationship registers) computed from the kept change lists instead of maintained by hand

## Critical Rules

- ❌ Letting the session AI edit the world mid-session ✅ write or play freely, resolve afterwards
- ❌ Starting from "what seems important" ✅ start from the full listing; every item gets a verdict
- ❌ Replacing a record with a freshly extracted version ✅ merge; update only the fields the row names
- ❌ Overwriting canon when the session disagrees ✅ a flag with both versions, and a recorded ruling
- ❌ Writing before the user has ruled ✅ the change list first, then only the approved rows
- ❌ Resending a write that came back as a proposal ✅ report it as waiting for the world's keeper
- ❌ Hand-maintaining summaries that could be computed ✅ derive them, or they drift within a week

## Example (Hyperion)

After the session where the Consul receives the fatline message:

```
LISTING: The Consul (touched) · Meina Gladstone (touched) · The Shrike Pilgrimage (changed) ·
         The Time Tombs (touched) · "the Home Rule Council" (no match: new entry or noise?)
ROWS:
  link      The Shrike Pilgrimage.characters  + The Consul      evidence: "You have been chosen..."
  knowledge "The Time Tombs show signs of opening"  held by: The Consul   evidence: Gladstone's message
  flag      Has the Consul accepted? The session ends before he answers. Leave the pilgrimage row as "chosen"?
NOT PROPOSED: the storm, the carrion-breed pack (background, no recurrence)
```

The list goes in a file beside the session's notes, never inside `elements/`, and nothing in the world changes until the user has ruled on its rows; no passage was skipped.

## Where OnlyWorlds Helps (optional)

| Update need | OnlyWorlds field |
|---|---|
| the session itself, verbatim | `Narrative.story`, with `events`, `characters`, `parent_narrative` (campaign → chapter → scene) |
| what happened | `Event` (`characters`, `locations`, `start_date`, `triggers`, `consequences`) |
| someone moved | `Character.location` (a Location) |
| a relationship changed | `Relation` (`intensity`, `start_date`, `end_date`, `events`) |
| who learned what | a knowledge entry: `Narrative` with subtype `knowledge`, held by `narrator`, `collectives`, or both; a rumour and the truth are separate entries held by different people. See `knowledge/atlas-conventions.md` |
| a death | Creature `status`; Character: model's "Marking a Dead Character" |
| canon status, custom state | `x_*` extension fields |
| verbatim vs editorial | a Narrative's `story` (the only type with that field) vs any element's `description` |

Every-line happenings (each exchange, each roll) go in a log beside the world, not in elements (principles §1). That log points at element ids, never copies of element text; a tool that follows the change feed (develop's Sync Changes) applies its delete rows, so an element gone from the world goes from the tool.

**To write**: edit files in a world folder (`knowledge/world-folder.md`, writer rules; in a folder linked to an account, every edited file gets a fresh `local_updated_at`), or use the API as the develop skill gives it: an existing element by PATCH of only the fields its row names, read first; multi-link changes through develop's Add or Remove Links; new elements through develop's Bulk Upload.

**A write that comes back as a proposal.** A world whose owner takes an AI seat's writes as proposals (`agent_writes_proposed` on `GET /api/v2/world`) answers a seat's PATCH or link write with `202` and a body of exactly `{"proposal": {...}}`: the element did not change, and the world's keeper accepts or declines it. A new element lands marked `x_review_proposed`, waiting the same way. Read the queue with `GET /api/v2/world/proposals` (open rows by default; `?element=<id>` for one element), report each row to the user as proposed, not applied, and never resend it. The read-back of Step 4's checks then compares the approved rows with the queue, not with the elements.

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- The change list in Step 4's row format, and where it was written: beside the notes, never inside `elements/` (Step 1).
- Every listed item's verdict, and every *no change* with its reason (Step 4, 3).
- Every flag, near-names among them, listed for the user's ruling, never decided in a row (Step 4, 6 and 7).
- What was deliberately not proposed, and why (Step 4, 5).
- Nothing written before the user has ruled, then only the approved rows (Step 1; Step 4, 9); a write that comes back as a proposal is reported as proposed, not applied (A write that comes back as a proposal).
- Passages the user chose to skip, as a coverage gap with their count (Step 4, 10).
- What was checked and how (principles §5).

## References

- `knowledge/world-memory.md`: the full loop, the dials, failure modes by name, and how other tools and tabletop practice do it
- `knowledge/schema-reference.md`: every field per type, and what each link field points at
- `knowledge/atlas-conventions.md`: knowledge entries, the calendar, and Atlas's other habits in a world folder
- The API's routes and their full answers: the live OpenAPI document, `https://www.onlyworlds.com/api/v2/openapi.json`
