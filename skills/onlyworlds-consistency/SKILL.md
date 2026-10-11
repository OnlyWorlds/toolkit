---
name: onlyworlds-consistency
description: "Find where a world contradicts itself: dates, places, names, links. Use when the user says 'check my world for contradictions', 'my world contradicts itself', 'continuity check', 'does this timeline add up'."
---

# OnlyWorlds Consistency

Find where a world disagrees with itself, and propose fixes the user rules on. A script finds the structural contradictions; the model reads only the elements the script flags.

Shared rules (code counts, propose-review-apply, merge-don't-overwrite, checking your work): `knowledge/principles.md`.

## Quick Reference

| User Says | Action |
|-----------|--------|
| "Check my world for contradictions" / "continuity check" | All four classes, then the text read |
| "Does this timeline add up?" | `--dates` |
| "Are my places nested right?" | `--places` |
| "Do I have duplicates?" | `--names` |
| "Are my links broken?" | `--links` |

## Instructions

### Step 1: Pick the Source

- **World folder** (no account needed): the current directory if it holds `world.json`, else the folder the user names (for Atlas, the world's own subfolder, not the `onlyworlds-atlas/` wrapper). The format: `knowledge/world-folder.md`.
- **API**: export the world to a folder first, then treat it as one. The api skill loads the credentials and sets the list rules (`www.`, singular endpoints, follow `next_cursor` until `has_more` is false); `knowledge/world-folder.md`, "Exporting an account world to a folder", gives the walk and the file shape. The analysis is the same on both sources.

### Step 2: Run the Script

```bash
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER            # all four classes
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER --dates    # one class; flags combine
python <this skill's folder>/scripts/consistency.py WORLD_FOLDER --json     # the same report as JSON
```

Python 3, standard library only; it reads the folder and writes nothing. It reads the link and date fields from this skill's `knowledge/schema-reference.md`. The report opens with the counts ("Checked 158 elements, 412 links; 3 contradictions, 7 possible"), then one section per class, one line per finding: the element, the field, the two values that disagree, the other element's name and id, and the file.

| Class | Contradiction | Possible |
|-------|---------------|----------|
| dates | a date field outside the world's `time_range_min`..`time_range_max`; an `end_date` before its `start_date` (or `revoke_date` before `grant_date`); a birth after the death date | an Event or Relation that starts before the birth of a Character it links |
| places | a `parent_location` cycle; a `location` or `parent_location` naming a missing element or one that is not a Location | |
| names | two elements of one type with the same name (case and spaces folded) | one edit apart, or one name inside another |
| links | an id that names nothing, or an element of the wrong type; a Relation with the same element at both ends | |

- **Deaths** follow the schema skill's convention, its one home ("Marking a Dead Character"): a `[Deceased] ` prefix on a Character's `physicality` or a Creature's `status` marks the death. The death date is a year right after the prefix; else the year on `background`'s death line, where the convention writes it; else a lone integer in the rest of the field.
- **Mutual bonds**: the schema names no link field as mutual (`Character.friends` is each character's own view), so a one-way bond is not a finding. If the user says their world treats a field as mutual, pass `--mutual Character.friends`.
- **Places** owns `location` and `parent_location`; `--links` alone skips them.
- **The "not checked" section** says what the run skipped (a missing time range, unreadable files, map, pin and marker in the names check). Carry it into your answer.
- **Exit 0** on every report: it is a report, not a gate. Exit 2 means the folder could not be read.

### Step 3: Read the Flagged Elements

Read only the elements a finding names, and the other element on the same line. Never read the whole world for this.

**The text class is yours, not the script's**: a description or story that speaks of a dead element as living, or of a living one as dead. The report's "text" section lists every element marked dead and the elements that link to it. Read those: the dead element's own text, and each linking element's `description` (and `story` for a Narrative). Look for the dead acting after their death date, a living character mourned, a destroyed place still visited. Anything you find is a "possible" finding, quoted, with the file.

### Step 4: Ask Before Calling It Wrong

A contradiction may be canon:

- an unreliable narrator, a legend, a propaganda history;
- a secret or a false belief: in an Atlas world, a knowledge entry (a Narrative with subtype `knowledge`) records what its holders believe, true or not (`knowledge/atlas-conventions.md`);
- two different things that share a name (`knowledge/principles.md` §3: a name match is a candidate, never a conclusion).

Ask the user which findings are intended before proposing fixes for them. "Possible" findings are questions, not verdicts: put them as questions.

### Step 5: Propose Fixes

One readable list; nothing is written until the user approves (principles §2):

```markdown
| # | Finding | Proposed fix | File, field |
|---|---------|--------------|-------------|
| 1 | Pip's birth_date 260 is after time_range_max 250 | birth_date 206 (a typo?), or widen the world's range | character/pip--….json, birth_date |
| 2 | Two Characters named "Mira" | Keep both; rename one "Mira of the Fen" | character/mira--….json, name |
| 3 | possible: the Siege starts before Ash is born | Ask: is this Ash's father? | event/siege--….json, characters |
```

Offer two fixes when the right one depends on intent (the date was wrong, or the range was). A fix to a never-touched field (name, birth date, birthplace: principles §4) is an identity call: say so.

### Step 6: Apply What Was Approved

- **World folder**: snapshot first (git, or a copy: world-folder.md, "Keeping history"); edit only the approved fields, per the world-folder writer rules (keep every other field and key order; in a folder linked to an account, a fresh `local_updated_at`).
- **API**: read before write, PATCH only the approved fields; multi-link changes go through the links endpoint (the link skill, Step 5, shows both calls).
- Read each edited element back, then run the script again: an approved fix should take its finding with it, and nothing new should appear.

Report: N findings, N fixed, N kept as canon, N left open, and the "not checked" lines.

## What This Does Not See

The script checks structure, not truth (principles §5): a wrong fact stated consistently passes, and zero findings is a claim about the check. Numbers in prose ("born in the year of the flood") are not dates to it; only the integer date fields are.
