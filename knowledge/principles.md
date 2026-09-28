# Toolkit Principles

The rules every skill in this toolkit follows. Each skill points here instead of repeating them. They hold whether the world is an OnlyWorlds world, a folder of files, or the user's own database.

## Contents
1. Where the world lives
2. How changes happen
3. Identity
4. Fields
5. Checking your work
6. Credentials

---

## 1. Where the world lives

- **Folder first, account optional.** A world can live entirely as files on disk (see `world-folder.md`). An OnlyWorlds account adds hosting, sync, and the API. Never require it for work a folder can do.
- **The world is the record.** Chats, session briefs, summaries, and reports are views of it, rebuilt when needed. A summary that replaces its source loses detail unevenly and compounds the loss each pass.
- **Records beside the graph.** High-volume happenings (every line of dialogue, every dice roll, every simulation step) do not belong as elements: keep them in a log beside the world, joined by element id. An Event is for what crosses a line someone cares about; a Narrative can chronicle a stretch of time.
- **Branch, don't copy.** A copied world gets new ids, and every comparison between the copies degrades to matching by name. Keep one world and version it (see `world-folder.md`, keeping history in git).

## 2. How changes happen

- **Code counts, the model judges.** Anything countable (who is where, which threads are open, which elements a text mentions, link degree) is computed by a query or a script. The model renders, proposes, and judges; it never re-decides what the count settled.
- **Propose, review, apply.** A model proposes changes as a readable list; a human rules on it; a single writer applies only what was approved. Extraction and writing are never the same step.
- **One writer at a time.** Two processes editing the same world overwrite each other silently. Before editing a folder in place, ask the user to close the Atlas tab (switching worlds is not enough); Atlas reads a folder only when it opens. In a folder linked to an account, an edited file must also carry a fresh `local_updated_at`, or Atlas never sends the edit (`world-folder.md`, writer rules).
- **Merge, don't overwrite.** An update touches only the fields it names and keeps everything else, including fields it does not understand.
- **Retire, never delete.** The dead, the departed, and the finished are marked and dated, not removed, so the past stays answerable.
- **Say what you didn't do.** What was not extracted, a rule that could not apply, a passage that was skipped, a gap in the context: each is a written line, never silence.

## 3. Identity

A name match is a **candidate**, never a conclusion.
- Confirm a match by type plus at least one anchor: what it is, where it is, who holds or leads it.
- Flag near-names and sound-alikes ("Perran" and "Piran"), relabels ("the ferryman" and the ferryman's name), and titles used as names ("the Captain"). Check within the current batch too, not only against the existing world.
- Before creating something new, look for an existing element that already does the same job.
- Two different things may share a name. Merging them, splitting one into two, or renaming are identity calls: list them for review, never make them silently.

## 4. Fields

- **Know each field's kind.** Some fields are *replaced* (current state: location, status, mood). Some are *appended* (a history that grows a dated line). Some are *never touched* (identity and canon: name, species, birthplace, birth date). Most wrong updates are a right fact in the wrong kind of field. Standing rules and secrets live in never-touched fields, or the next update erases them.
- **Field presence over labels.** Tools recognise data by which fields are present, not by `supertype` or `subtype` text, which are for humans. The exception is a value a convention reserves: Atlas marks knowledge entries with Narrative subtype `knowledge` (see `atlas-conventions.md`). Honour reserved values; do not invent new ones.
- **Custom data goes in extension fields.** Unprefixed fields must be schema fields. Anything else goes in `x_<name>`: stored verbatim, returned by the API, kept by Atlas sync and export. A tool prefixes its own fields with its name (`x_mytool_...`) and writes only its own namespace; `atlas_*` and `shadow_*` belong to those tools. Fields a machine writes are never hand-edited.
- **Numbers are data.** Numeric schema fields are integers in the world's own units (state the unit somewhere the reader will find it). A tool, or a simulation, can only read what is a field; prose is for people.
- **Keep the source voice apart from the summary.** A Narrative's `story` holds verbatim text (the only type with that field); `description` holds the editorial overview everywhere. Provenance (where a fact came from) goes in a side record or a citation, not inside descriptions.

## 5. Checking your work

- **Verify against the source of truth.** After a write, read back what actually landed and compare it with what you intended. A check whose two sides come from the same place (comparing a folder with an export you just copied into it) passes by construction and proves nothing.
- **Structure is not correctness.** A green check proves links resolve and fields exist; it cannot see a wrong fact or a missed one. Sample-read the output against the source.
- **A zero is a claim about the instrument.** An empty result, zero flags, or "nothing changed" deserves a second look at the check before it is trusted.
- **Test clean.** Test a recipe or skill in a fresh session with no project memory; a session that knows the project fills gaps the world does not.

## 6. Credentials

- Load keys and PINs from `.env` (ignored by git before it is written: check `git ls-files .env`). Send them from variables; never print, quote, or commit them.
- A PIN never goes into a build. Deployed or public tools use a read key (`ow_r_...`) or ask the user at runtime.
