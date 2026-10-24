---
name: onlyworlds-read
description: "Read a whole world and report on it through one of three lenses: what it contains and where its weight sits (a creative brief), which connections are missing (orphans, characters with no relations, places nobody lives in), or where it contradicts itself (dates, places, names, broken links). Use when the user says 'survey my world', 'what do I actually have', 'my elements feel disconnected', 'find orphans', 'continuity check', 'does this timeline add up'. A world folder or an account world. Writes only what the user approves."
---

# Read

Read a whole world, from a folder or an account, through one lens: **survey** (what it is, where its weight sits), **link** (the connections it is missing) or **consistency** (where it disagrees with itself). Code counts the world; the model reads only what matters and writes nothing the user has not approved.

Shared rules (identity, code counts, propose-review-apply, merge-don't-overwrite, checking your work): `knowledge/principles.md`, here especially §2 and §5.

## Quick Reference

| The user wants | Lens | First move |
|---|---|---|
| what they have, a brief | `survey` | count, read the top of the web, write the brief |
| disconnected, orphans, missing links | `link` | count, gather evidence, propose links |
| contradictions, continuity, timeline, duplicates, broken links | `consistency` | `scripts/consistency.py`, then read what it flags |
| unsure | `survey`, then offer the other two | |

**Picking the lens.** The first word of the invocation's argument picks it: `survey` (or `brief`), `link` (or `links`, `orphans`), `consistency` (or `contradictions`, `continuity`). With no such word, the table picks from the user's words. One lens runs at a time; run a second only when the user asks for it. A picture of the web ("show my world", a graph) is the draw skill, not a lens here.

## Step 1: Pick the Source

- **World folder** (no account needed): the current directory if it holds `world.json`, else the folder the user names (for Atlas, the world's own subfolder, not the `onlyworlds-atlas/` wrapper). Read `world.json` and every `*.json` under `elements/*/`, keyed on the internal id, never the filename (`knowledge/world-folder.md`). For an Atlas world, also read `knowledge/atlas-conventions.md`.
- **API**: export the world to a folder first, then treat it as one: `knowledge/world-folder.md`, "Exporting an account world to a folder", gives the walk and the file shape, and the develop skill's list rules hold for the calls (`www.`, singular endpoints, exact headers, follow `next_cursor` until `has_more` is false). Load credentials from `.env`, as start's Connect an account writes it (principles §6): `set -a; . ./.env; set +a`, and fill an unset `OW_*` name from its older `ONLYWORLDS_*` twin (`OW_API_KEY=${OW_API_KEY:-$ONLYWORLDS_API_KEY}`, likewise the PIN). A read key (`ow_r_`) reads without a PIN; every write needs one. If there are none, ask the user to type them into `.env` themselves; never ask for them in chat, never print one.

The export is for reading: approved changes to an account world go back through the API, not into it. The rest is the same for both sources.

## Step 2: Count the World (survey and link)

Counting is code's job (principles §2), and the skill ships the counter:

```bash
python <this skill's folder>/scripts/count.py WORLD_FOLDER              # the report, Markdown
python <this skill's folder>/scripts/count.py WORLD_FOLDER --mentions   # plus ow:// mentions no link backs
python <this skill's folder>/scripts/count.py WORLD_FOLDER --json       # every list in full
```

Python 3, stdlib only; it reads the folder with the consistency script's loader, writes nothing, and reports:

- **Distribution**: element count per type.
- **Link degree**: per element, links out plus links in (backlinks). A link is any field whose value is an id, or a list of ids, found in the id map.
- **Orphans** (degree 0) and **near-orphans** (degree 1, with the one link).
- **Clusters**: connected groups in the link graph, with their sizes and their most linked members.
- **Bridges**: elements whose removal splits their cluster.
- **Text weight**: characters of `description` plus `story` per element; the most linked and the most written each get a table (`--top N`, default 40).

**The room is left out unless the user asks.** A room element (principles §4: one of the room profile's pairs and its mark `x_room_of`; its lines, boards, hearts, votes, sittings, specs and members) is the world's work about itself, not its lore. The script drops room elements from the id map before counting, so distribution, degree, orphans and clusters exclude them and their links, and its "Left out" line gives their count: carry it into your answer once. `--room` counts them. Placement (map, pin, marker and zone, the four the draw skill leaves out of its graph) is left out the same way; the report's first line gives the world's whole count and that split, and `--placement` counts them.

**The marks are named.** A proposed element (`x_review_proposed`, an AI seat's write waiting for a keeper: schema-dist's review profile) is not yet canon, so it is left out the same way and the "Left out" line says how many; `--proposed` counts them, each labelled "proposed, not yet reviewed", and a brief never states one as a fact. A known-of stub (`known_of: true`, an element the reader's sheet names but cannot see whole) is counted but its empty fields are unknown: it is never an orphan, a near-orphan or a text row. A hidden element (`hidden`, folder spec 4.8) is counted, since the folder's holder sees it; the "Marks" line gives the counts, and a brief that may be handed on says how many are hidden.

Save the report beside your output; the brief and the link lists cite its numbers and never recount them. The consistency lens runs its own script instead.

## The survey lens

A creative brief: a reading of what the world is about and where its weight sits.

### Read the World

This is the creative step. Read by the count:

| World Size | Brief Length | Approach |
|-----------|-------------|----------|
| Under 20 elements | Short (~60-80 lines) | Go deep on each element |
| 20-100 elements | Standard (~100-150 lines) | Read everything; cover shape and highlights |
| 100-300 elements | Full (~150-200 lines) | Read the top ~40 plus every bridge |
| 300+ elements | Focused (~150-200 lines) | Read the top ~40 plus bridges and a sample per cluster |

The top ~40 come from the count's two tables, by link degree and by text weight. The rest are known by their counts, and the brief says so.

From what you read, find:

- **The skeleton**: What types dominate? Character-heavy? Institution-heavy? The distribution tells a story.
- **The web**: Which clusters form, what the bridges join, what the orphans are.
- **The heat**: Long descriptions signal care. Dense link webs signal importance. Named Relations signal explicit bonds. Narrative `story` holds the prose; read it as the densest heat signal.
- **The gaps**: What's conspicuously absent? A world full of Characters but no Institutions tells a story about individuals against chaos.
- **The darkness**: Tensions, contradictions, Events that changed everything.

### Write the Brief

**Head the brief with two lines** (principles §2 "Say what you didn't do" and §5):

```markdown
True as of: {when the data was read} from {folder path or API world name}
Not read: {M} of {N} elements read in full; the rest known only by their counts. Skipped: {placement: map, pin, marker, zone}; the room left out: {R} elements; proposed, not yet reviewed, left out: {P} elements; hidden: {H} elements
```

`{H}` counts the elements marked `hidden: true`: counted, since the holder reads them; said, since a brief is handed on. `{P}` and `{H}` are the count's "Left out" and "Marks" lines, never recounted.

Then the count's **distribution table**, before any prose. Then the brief's sections (adapt to what the world gives you):

1. **The One Sentence**: What is this world, in one line? A feeling, not a genre label.
2. **What This World Actually Is**: Surface and underneath.
3. **The Physical World**: How it feels to be there. Locations, atmosphere, texture.
4. **The Characters**: Who they are in your gut, not stat blocks.
5. **The Emotional Core**: 2-4 things this world is *about*.
6. **What's Dark / Funny / Strange**: Whatever applies.
7. **The Web**: How things connect. Surprising links. What the bridges join.
8. **What's Missing**: Gaps as observation, not criticism.
9. **One Last Thing**: The single detail that says everything. The image or connection that lingers. End the brief here.

### Voice

**Match the world's register.** A grim frontier war shouldn't be cheery. A puppet world shouldn't be grim. The world sets the atmosphere; bring observation and wit to the reading, not a fixed tone.

The brief should feel like a friend who read your entire world overnight and is telling you about it: catching things you forgot, connecting things you didn't realize were connected, occasionally making you laugh at your own creation.

**Allowed:**
- Observations about what the data implies ("they share three Events but have no Relation; whatever's between them hasn't been named")
- Patterns the creator may not have intended ("every Location has a water source; you may not have planned a water theme, but you've got one")
- Reading emotional weight from description density and link patterns

**Not allowed:**
- Inventing facts not in the data
- Stating implications as fact ("they're in love" vs "they orbit each other")
- Filling gaps with assumptions
- Being dismissive about any world, regardless of size or quality

**The line**: Every claim traces back to element data. Interpretive readings are framed as readings ("this looks like...", "the web suggests...", "hard not to read this as...").

### Zone Filtering

Zones with no description or generic names (poly1, new zone, TRE) are likely map test data. Skip or note as artifacts; don't interpret them.

### Output

Write the brief to `survey-{world-name}.md` beside the world folder (principles §1; or where the user asked) and report the path. Then offer the next step: orphans and bridges feed the link lens; preparing a session from this world is the context skill; a picture of the web is the draw skill.

## The link lens

Find the connections a world is missing and add the approved ones. It adds links only. A known-of stub is never a link target (its reader cannot see it whole; `--mentions` leaves it out), and a proposed element is not linked to until a keeper settles it.

### Gather the Evidence

Start from the count's orphans, near-orphans, clusters and bridges; a room element is never a source, a target or evidence for a suggested link. **Evidence for new links**, in order of strength:

1. **Narrative `story`** (chapter, scene and session prose). An in-prose mention `[Name](ow://type/uuid)` is an exact reference; `count.py --mentions` lists every mention no link field backs, with the fields that could carry it. An element mentioned in a Narrative's story is evidence for that Narrative's involves-fields (`characters`, `locations`, ...), and elements that share scenes are candidates for Relations.
2. **`description` and other text fields** that name another element.
3. **Structure**: shared Events, shared locations, elements that bridge otherwise separate clusters.

In an Atlas world, a knowledge entry (Narrative with subtype `knowledge`) uses `collectives` for the groups who HOLD the knowledge, not its topics: never add a Collective there because the entry mentions it (`knowledge/atlas-conventions.md`).

### The Three Lists

**Orphans** (0 links in, 0 out) and **near-orphans** (1 link total):
```markdown
| Element | Type | Links Out | Links In | Issue |
|---------|------|-----------|----------|-------|
| The Stale Roll | Object | 0 | 0 | Orphan: completely disconnected |
| Deep Drip | Location | 0 | 1 | Near-orphan: only referenced by one Event |
```

**Implicit connections**: links the evidence supports:
```markdown
| Source | Target | Suggested Link | Evidence |
|--------|--------|---------------|----------|
| Admiral Fluffington | USS Fuzzball (Location) | Character.location | "lives aboard the USS Fuzzball" in description |
| Chapter 3 (Narrative) | Dampworth | Narrative.characters | `[Dampworth](ow://character/…)` in story |
| Battle of Button Bay | Feltropolis | Event.locations | "fought at Feltropolis harbor" in description |
```

**Missing Relations**: significant connections that need Relation elements:
```markdown
| Actor (Character) | Other parties | Type | Evidence |
|-------------------|---------------|------|----------|
| Fluffington | Commodore Snoot | rivalry | Opposing descriptions, shared Events |
| (none) | Moisture Merchants, Eternal Drip | dependence | Guild exists because of the Drip |
```

`actor` must be a Character. Standing between two Institutions goes in `Institution.allies` / `adversaries`; any other tie without a defining Character is a Relation with involves-fields and no actor.

### Present Recommendations

Group by priority:

1. **High value**: links that connect clusters (bridge elements between isolated groups)
2. **Medium value**: links that fill obvious gaps (Character missing species, Event missing location)
3. **Low value**: links that add richness but aren't critical

For each recommendation, show what to link (source and target), which field to use (or a new Relation), and why: the evidence (a quoted phrase, a story mention, or the structural count). No evidence, no suggestion. Write nothing until the user has approved (principles §2).

### Execute (With Approval)

Apply only the approved items.

**World folder**:
1. **Snapshot first**: commit the folder in git, or copy it (`knowledge/world-folder.md`, "Keeping history").
2. **Edit per the world-folder writer rules**: change only the approved link fields; keep every other field, including `atlas_*`/`shadow_*`/`x_*` values and nulls, value for value; keep keys in their original order. In a folder linked to an account, set a fresh `local_updated_at` on every edited file, or Atlas never sends the edit. A new Relation is a new file: mint a UUID, name the file per the folder rules, and omit `local_updated_at`/`server_updated_at`.
3. **Read back**: re-load each edited file and confirm every approved link landed and nothing else changed (principles §5).

**API** (develop's Add or Remove Links is the full reference):

- **Multi-link fields** (`objects`, `characters`, `friends`, …): the links endpoint adds and removes atomically on the server, skips ids already linked, tolerates removing ids that aren't there, and returns `400 invalid_link` if an added target doesn't exist. MCP-connected users: the `edit_links` tool does the same.
```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/{type}/{uuid}/links/{field}" \
  -H "API-Key: $OW_API_KEY" -H "API-Pin: $OW_API_PIN" -H "X-OW-Agent: 1" \
  -H "Content-Type: application/json" \
  -d '{"add": ["target-uuid-1", "target-uuid-2"], "remove": []}'
```
- **Single-link fields** (`location`, `parent_location`, `birthplace`): PATCH `/api/v2/{type}/{uuid}` with the bare field name and a UUID value (`{"location": "target-uuid"}`; no `_id` suffix on v2). PATCH *replaces* the field: read the element first. Never PATCH a multi-link array to add to it.
- **New Relations**: POST `/api/v2/relation`, minting your own UUID so you can set the links in the same call. A Relation has a single `actor` (the defining Character) plus multi-link involves-fields (`characters`, `institutions`, `objects`, …) for the other parties:
```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/relation" \
  -H "API-Key: $OW_API_KEY" -H "API-Pin: $OW_API_PIN" -H "X-OW-Agent: 1" \
  -H "Content-Type: application/json" \
  -d '{"id": "{your-uuidv7}", "name": "Fluffington-Snoot Rivalry", "description": "...", "intensity": 85, "actor": "actor-uuid", "characters": ["other-party-uuid"]}'
```
  If a linked UUID doesn't exist you get a `400 invalid_link` naming the field; fix and resend.

For non-ASCII names or descriptions, write the body to a file with ASCII-escaped JSON and send `-d @body.json` (Windows curl can corrupt raw UTF-8 silently). After each write, GET the element and confirm the change landed.

Report results: N links added, N Relations created, N orphans resolved. For a folder in git, commit with the approved list as the message.

### Link Field Reference

Which type has which link field: the type's own section of `knowledge/schema-reference.md` (`single-link → T`, `multi-link → T`) and its Link Direction Summary; v2 uses bare field names holding UUIDs. Single links: Character.location, Character.birthplace, Location.parent_location. Multi links: Character.species, Character.objects, Character.institutions, Event.characters, Event.locations. Relation: `actor` (single Character) plus the involves multi-links, with `intensity` and `description`.

## The consistency lens

Find where a world disagrees with itself, and propose fixes the user rules on. A script finds the structural contradictions; the model reads only the elements the script flags.

### Run the Script

```bash
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER            # all four classes
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER --dates    # one class; flags combine
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER --json     # the same report as JSON
```

Python 3, stdlib only; it writes nothing. It reads the link and date fields from this skill's `knowledge/schema-reference.md`. The report opens with the counts ("Checked 158 elements, 412 links; 3 contradictions, 7 possible"), then one section per class, one line per finding: the element, the field, the two values that disagree, the other element's name and id, and the file. A finding that involves a proposed element is not yet canon: it opens "Not yet canon", is counted apart from the contradictions, and goes to its keeper as a question. The user's words pick the flags: a timeline is `--dates`, nesting `--places`, duplicates `--names`, broken links `--links`.

| Class | Contradiction | Possible |
|-------|---------------|----------|
| dates | a date field outside the world's `time_range_min`..`time_range_max`; an `end_date` before its `start_date` (or `revoke_date` before `grant_date`); a birth after the death date | an Event or Relation that starts before the birth of a Character it links |
| places | a `parent_location` cycle; a `location` or `parent_location` naming a missing element or one that is not a Location | |
| names | two elements of one type with the same name (case and spaces folded) | one edit apart, or one name inside another |
| links | an id that names nothing, or an element of the wrong type; a Relation with the same element at both ends | |

- **Deaths** follow the model skill's convention, its one home ("Marking a Dead Character"): a `[Deceased] ` prefix on a Character's `physicality` or a Creature's `status` marks the death. The death date is a year right after the prefix; else the year on `background`'s death line, where the convention writes it; else a lone integer in the rest of the field.
- **Mutual bonds**: the schema names no link field as mutual (`Character.friends` is each character's own view), so a one-way bond is not a finding. If the user says their world treats a field as mutual, pass `--mutual Character.friends`.
- **Places** owns `location` and `parent_location`; `--links` alone skips them.
- **The room**: the script checks every element, the room's too. A finding on a room element is the room's, not the lore's: report it apart.
- **The "not checked" section** says what the run skipped (a missing time range, unreadable files, map, pin and marker in the names check). Carry it into your answer.
- **Exit 0** on every report: it is a report, not a gate. Exit 2 means the folder could not be read.

### Read the Flagged Elements

Read only the elements a finding names, and the other element on the same line. Never read the whole world for this.

**The text class is yours, not the script's**: a description or story that speaks of a dead element as living, or of a living one as dead. The report's "text" section lists every element marked dead and the elements that link to it. Read those: the dead element's own text, and each linking element's `description` (and `story` for a Narrative). Look for the dead acting after their death date, a living character mourned, a destroyed place still visited. Anything you find is a "possible" finding, quoted, with the file.

### Ask Before Calling It Wrong

A contradiction may be canon:

- an unreliable narrator, a legend, a propaganda history;
- a secret or a false belief: in an Atlas world, a knowledge entry (a Narrative with subtype `knowledge`) records what its holders believe, true or not (`knowledge/atlas-conventions.md`);
- two different things that share a name (principles §3: a name match is a candidate, never a conclusion).

Ask the user which findings are intended before proposing fixes for them. "Possible" findings are questions, not verdicts: put them as questions.

### Propose Fixes

One readable list; nothing is written until the user approves (principles §2):

```markdown
| # | Finding | Proposed fix | File, field |
|---|---------|--------------|-------------|
| 1 | Pip's birth_date 260 is after time_range_max 250 | birth_date 206 (a typo?), or widen the world's range | character/pip--….json, birth_date |
| 2 | Two Characters named "Mira" | Keep both; rename one "Mira of the Fen" | character/mira--….json, name |
| 3 | possible: the Siege starts before Ash is born | Ask: is this Ash's father? | event/siege--….json, characters |
```

Offer two fixes when the right one depends on intent (the date was wrong, or the range was). A fix to a never-touched field (name, birth date, birthplace: principles §4) is an identity call: say so.

### Apply What Was Approved

- **World folder**: snapshot first (git, or a copy: world-folder.md, "Keeping history"); edit only the approved fields, per the world-folder writer rules (keep every other field and key order; in a folder linked to an account, a fresh `local_updated_at`).
- **API**: read before write, PATCH only the approved fields; multi-link changes go through the links endpoint (the link lens's Execute shows both calls).
- Read each edited element back, then run the script again: an approved fix should take its finding with it, and nothing new should appear.

Report: N findings, N fixed, N kept as canon, N left open, and the "not checked" lines.

### What This Does Not See

The script checks structure, not truth (principles §5): a wrong fact stated consistently passes, and zero findings is a claim about the check. Numbers in prose ("born in the year of the flood") are not dates to it; only the integer date fields are.

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- The lens taken, from the argument's first word or the user's words (Picking the lens).
- The script's count line and its "Left out" line, cited once, never recounted (Step 2; Run the Script).
- For the consistency lens, the "not checked" section (Run the Script).
- A question before any fix: which findings are intended, every "possible" finding put as a question (Ask Before Calling It Wrong).
- Nothing written until the user approves; then the tally of what was fixed, kept, left open or linked (Propose Fixes; Apply What Was Approved; Execute).
- For a survey, the brief's two head lines, true as of and not read, and the brief's path (Write the Brief; Output).
- What was checked and how (principles §5); a script that could not run is said so (principles §2).
