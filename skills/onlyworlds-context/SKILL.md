---
name: onlyworlds-context
description: Design how a world gets loaded into an AI session - fresh, scoped, sourced context instead of one giant chat that forgets. Use when the user says their AI forgets details, loses canon, drifts, or compresses old chats; asks how to load their world, lore bible, notes or PDFs into a writing, tabletop, or roleplay session; wants a character played from what that character knows; or is designing session prep, context assembly, or retrieval for a long-running world. Works with or without OnlyWorlds.
---

# World Context

Help the user design THEIR way of building a fresh, scoped context for each session from their world. Teach the principles, co-design the recipe, build the smallest working version. Do not install a one-size pipeline. The companion resolve skill covers the other half: writing what happened back into the world.

Shared rules (code counts, the world is the record, checking your work) live in **knowledge/principles.md**; this skill applies them to loading a session.

## Quick Reference

| Principle                                                                                                      | The failure it prevents                                                             |
|----------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| The world is the memory; each session starts fresh and is preloaded                                            | the long chat that compresses, summarises, and forgets                              |
| Code counts, the AI writes (principles §2)                                                                     | statuses, dates, and who-is-present quietly changed by the model                    |
| Learn the world's shape before assembling                                                                      | a recipe that assumes story threads in a world that keeps its state in dated events |
| Rebuild the context from the world every time; never append to it                                              | a scroll nobody can audit; one wrong fact carried forward until it is canon         |
| Choose by focus: where, when, who (or one character and their circle)                                          | "similar" lore instead of the people in the room                                    |
| Two layers: loaded, and one lookup away                                                                        | the block that answers everything and gets skimmed                                  |
| Whose view: author, one character, a group of players                                                          | a character acting on knowledge she cannot have; spoilers                           |
| State what it is true as of, and list the gaps                                                                 | a stale or partial packet that reads as complete                                    |
| Every line names its source                                                                                    | facts nobody can check or trace                                                     |
| Write the recipe down                                                                                          | a setup that works once and cannot be repeated or debugged                          |

## Instructions

### Step 1: Diagnose (ask only what isn't already visible)

- **Where does the world live?** Chat history · documents or PDFs · a notes vault · a database · an OnlyWorlds world (folder or API).
- **What is a session?** A writing session · tabletop prep or play · a game or simulation tick.
- **What can the AI touch?** Chat only (they paste) · a local agent with files (Claude Code, Codex) · code and APIs. Mixed is common: a local agent builds the brief, and the user pastes it into a fresh chat in the app they play in.
- **How big?** Tens, hundreds, or thousands of things.
- **What goes wrong today?** Their words, verbatim. That sentence is the design target.

Speak their vocabulary back (canon, bible, drift, prep, recap). Say "schema" only if they do.

### Step 2: Pick the shape for their tier

| Tier            | Their context recipe becomes                                                             |
|-----------------|------------------------------------------------------------------------------------------|
| **Chat only**   | a written recipe plus a prompt that fills it from their world files into a session brief |
| **Local agent** | their own script or skill that writes a fresh context file before each session           |
| **Code / API**  | a query layer that compiles the packet, with the recipe as config                        |

If the world still lives in documents (PDFs, chat exports, long notes), sessions should not read them whole; they assemble from structured entries. Start small: write the recipe, then turn only the documents the next session needs into entries, and build the first brief from those. Parse the rest over time, one document at a time, recording what each one contributed. A chat-only user may keep the entries as plain markdown (one file per character, place, or thread); a world folder or OnlyWorlds JSON comes from the parsing skill.

### Step 3: Learn the world's shape

Before choosing what goes in, read how THIS world keeps its state:
- **Where does "what's going on" live?** Story threads with a status · dated events · relationships · nothing yet. Pick the one the world actually uses; a world can have no story threads at all.
- **Which fields mean "current"?** A current location, a status, a present-day marker. Which fields are background that never changes?
- **Does a status field hold a small set of values?** Check before trusting it as a status; some worlds keep sentences there.
- **What is secret, and from whom?**
- **What does the folder NOT hold?** A session log not yet written back, a notes file, a tracker. Name these stores; they come in through the recipe, or the packet says it lacks them.

### Step 4: Design the recipe together

Write each answer into a file in their project (e.g. `context-recipe.md`). The file is the deliverable.

1. **The focus.** A scene (place, time, who is present) or one character (their circle, their threads, their places). Where does each live in the data? Presence guessed by the model is how ghosts walk into scenes.
2. **The counting half.** Everything that can be counted is computed by a plain query or script: who is present, which threads are open, what is due, what happened recently here and to these people, who is close to the focus and who is opposed. The model receives these as given and may reword them, never re-classify them.
   - Rank the circle by current threads plus declared bonds; all-time appearances only break ties, or last year's cast crowds in.
   - Walk links both ways: a minor character's circle mostly comes from who links *to* them. Also count names mentioned in live threads.
3. **The loaded layer.** The now, the focus, the people and places around it (following links one or two steps, depth written down), open threads, recent events, three real quoted lines per lead voice. Plans and next steps are their own kind: never listed under recent, never written as done. Leave near-neighbours out unless the scene needs them: the rival family and last year's treaty confuse more than they help.
4. **The reachable layer.** Everything else, one lookup away. Put a one-line index of what exists but is not loaded into the packet, so the model can ask for it by name.
5. **The view.** An author or GM sees everything. A single character sees only what she knows. A group of players sees what the group has learned. What a viewer does not know is absent from their packet, not present and hidden. A players' packet, or a single character's, is built from the knowledge entries that viewer holds (in OnlyWorlds: a Narrative with subtype `knowledge`, held via `narrator`, `collectives`, or both), never from canonical fields such as a description: those are the GM's view, and GM-only facts stay out. A knowledge entry exposes its text and the names of the elements it is about, so a players' packet may name an element it never describes.
6. **The layout** depends on how the packet is read. Injected whole: standing frame first, the focus near the end, the current situation last (models attend most to the start and the end). Read by a tool that pages and can stop early: the now first, then a "read to here" marker after what the session must have. Every entry names its subject and type and writes links as names, never bare ids.
7. **The budget and the drop order.** A number, and a written order for what goes first when it overflows (background lore before present characters; long descriptions before status). The budget limits detail, never membership: a row that doesn't fit gets one line, not silence.
8. **The header and the gaps.** The packet opens with what it is true as of, and closes with what it could not fill ("no source for the last two sessions", "no current location for X").

### Step 5: Build the smallest working version

- **Chat only**: the recipe file, a brief template, and a fill prompt; run it on a real upcoming session.
- **Local agent / code**: their script or skill. Keep the counting deterministic, so a bad session traces to a bad packet that can be rebuilt and compared.

### Step 6: Run it once and read it

Build one real packet and read it with the user: what is missing that the session will need, what is present that it won't? Change the recipe, not the packet. Test in a fresh session with no project memory or instructions; one that knows the project fills gaps the world does not.

### Step 7: Name the next rung

- a lookup helper the session can call mid-scene
- a pair query before scenes between characters with history: what they have done together, what they have already told each other
- a character decider for key choices: rebuilt from the character's core plus their current view of the world on every call, answering with a choice and a one-line why, allowed to be wrong, so it cannot drift

## Critical Rules

- ❌ Pasting the whole world into every session ✅ loaded layer + reachable layer
- ❌ A running summary appended forever ✅ rebuilt from the world each time; summaries are views, the world is the record
- ❌ Hiding secrets by instruction ("don't reveal X") ✅ leave X out of that viewer's packet
- ❌ A players' packet built from canonical descriptions ✅ built from the knowledge entries the players hold
- ❌ Keyword matching as the only way in ✅ selection by focus and links; "the old man" never matches a name, a link does
- ❌ A silent cut when the packet overflows ✅ a drop order, and a gaps line naming what was left out
- ❌ Porting this unchanged into a real-time game ✅ this loop is human-paced; games prepare context ahead of the player

## Example (Hyperion)

A session focused on the Consul, the evening the fatline message arrives:

```
TRUE AS OF: the evening of the message (the world's time_current)
FOCUS: The Consul · aboard his ship
AROUND HIM: Meina Gladstone (sender of the message) · the Hegemony (his former service)
OPEN: The Shrike Pilgrimage (he has been chosen; not yet accepted)
HE KNOWS: "The Time Tombs show signs of opening" (heard tonight)
NOT LOADED: Tau Ceti Center, the Church of the Shrike, the Time Tombs' history (ask by name)
GAPS: no current location recorded for Gladstone
```

Every line would carry its source (element and field) in the real packet.

## Where OnlyWorlds Helps (optional)

| Recipe need                               | OnlyWorlds field                                                                                                                                                                        |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| true as of                                | `time_current` in `world.json`; `time_range_current` on the v2 API                                                                                                                      |
| who is present                            | `Character.location`, with `Location.parent_location` for "in the city"                                                                                                                 |
| circle and history between two characters | `Relation` (`actor`, `characters`, `intensity`, `start_date`, `end_date`, `events`); `Character.friends` / `rivals` / `family`                                                          |
| what happened                             | `Event` (`characters`, `locations`, `start_date`, `consequences`)                                                                                                                       |
| story threads                             | `Narrative` (`events`, `characters`, `parent_narrative`, `order`)                                                                                                                       |
| what a character or group knows           | knowledge entries: a `Narrative` with subtype `knowledge`, held by `narrator` (one character), `collectives` (a group; members inherit), or both. See **knowledge/atlas-conventions.md** |
| their own categories                      | `supertype` / `subtype`                                                                                                                                                                 |
| custom state                              | `x_*` extension fields                                                                                                                                                                  |

Sources: a world folder on disk (see **knowledge/world-folder.md**), the REST API, or the MCP server (see **knowledge/ai-builders.md**). All of this is buildable without OnlyWorlds too; say so if the user has their own store.

## References

- **knowledge/world-memory.md**: the full loop, the ladder from query to agent, the dials, failure modes by name, and how other tools do it
