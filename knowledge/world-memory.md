# World Memory: the loop, the dials, and how others build it

Shared reference for the context and update skills: the session loop. The general rules they rest on live in `principles.md`. Read the section the conversation needs, not the whole file.

## Contents
1. The loop
2. The ladder: from a query to an agent
3. The dials
4. Failure modes, by name
5. How others build it
6. What a typed, linked world adds
7. Three worked shapes

---

## 1. The loop

```
  world ──assemble──▶ fresh session ──play / write──▶ transcript ──handover──▶ next session
    ▲                                                     │
    └─────────────────────── resolve ◀─────────────────────┘
```

- **The world is the record** (`principles.md` §1); chats, summaries, and context blocks are views of it.
- **Assemble** reads; **resolve** is the only thing that writes. The session in between writes nothing to the world.
- **The handover** is cheap and happens every session. **The resolve** is the careful pass; it can trail a session or two behind, but the longer it trails, the staler the world the next sessions read.
- **Code counts, the model writes and judges** (`principles.md` §2). Who is present, which threads are open, what is due, what a session mentioned: counting jobs. In practice this split is the largest single gain in both halves: most errors in model-only versions are counting the model redid and got wrong.
- **Two clocks.** Where the story stands (OnlyWorlds: `time_current` in `world.json`, `time_range_current` on the v2 API) and how far the world data has caught up with it. When the story runs ahead of the data, the context says so, and the resolve closes the gap.
- **History in git.** Commit the world folder after each resolve, with the change list as the message; `main` is canon and a branch is a timeline (a what-if, an alternate ending). A linked folder keeps its API key in `world.json`'s `api` block; `world-folder.md` (keeping history) says how to keep it out of a public repo.

## 2. The ladder: from a query to an agent

Climb a rung only when the one below stops being enough.

| Rung | What it is | When it's enough |
|---|---|---|
| 1. A recipe | a written list of what goes into a session brief, filled by hand or by a prompt | small worlds, chat-only setups |
| 2. A script or skill | the recipe run automatically over the world files | once the world outgrows copy-paste |
| 3. A lookup helper | something the session can ask mid-scene ("what happened between these two?") | when briefs keep missing the odd fact |
| 4. A stateless decider | a character rebuilt from her core plus her current view of the world on every call, answering with a choice and a one-line why, allowed to be wrong | "run this character" (an NPC, a roleplay partner) without her drifting |
| 5. A persistent agent | a character with memory of its own | rarely needed; it drifts, and its memory is a second world to resolve |

Real-time play (a game loop) changes the timing, not the ladder: context is prepared ahead of the player's likely moves instead of at the click.

## 3. The dials

Each is the user's choice. Name the setting and the cost.

| Dial | One end | Other end | The cost of the far end |
|---|---|---|---|
| Review | every change read | only flags read | wrong entries that everything downstream trusts |
| Resolve lag | resolve after every session | several sessions, then resolve | stale world under the new sessions; name collisions pile up |
| Similarity search | none, joins only | a vector store beside the world | results you cannot reproduce or explain; useful for "has anything like this happened?" over loose prose |
| Summaries | views, rebuilt from the record | the summary is the record | detail lost unevenly, compounding with each pass |
| Canon levels | one level: true | draft / established / locked, rumour / fact | more to decide at each resolve |
| Provenance | a side record (which session, which passage) | a tag on every fact | clutter in the world if it lives inside descriptions |
| Automation | a human rules every flag | a model rules them | the one step that stays human longest is ruling on flags |

## 4. Failure modes, by name

| Name | What happens | Guard |
|---|---|---|
| Context rot | quality falls as the context grows, even on easy tasks; related-but-wrong material hurts most ([Chroma](https://www.trychroma.com/research/context-rot)) | budget; leave near-neighbours out |
| Lost in the middle | the middle of a long context gets used least ([Liu et al.](https://arxiv.org/abs/2307.03172)) | frame first, scene last |
| Literal-match dependence | "the old man" never finds the entry called Aldric ([NoLiMa](https://arxiv.org/abs/2502.05167)) | select by who and where, not by the words in the chat |
| Silent truncation | an overflowing budget quietly drops entries | a drop order, and a line naming what was dropped |
| Summary drift | summaries lose detail and invent it; summaries of summaries compound it ([SillyTavern](https://docs.sillytavern.app/extensions/summarize/)) | summaries as views over a kept record |
| Context poisoning | one wrong fact in the context gets reused until it is canon ([Breunig](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)) | rebuild the block from the world; never carry it forward |
| Premature leak | a later fact (a scar, a death) appears in an earlier scene | assemble "as of" a moment |
| Old-cast gravity | the circle ranked by all-time appearances surfaces last year's cast | rank by current threads and declared bonds; all-time only breaks ties |
| Plan presented as fact | "planned for tomorrow" renders as happened; a next step reads as done | plans are their own kind, never rendered as recent or done |
| Ghost presence | a character appears where they aren't, because their position was never updated | presence from data; the resolve moves people |
| Silent overwrite | the newer version replaces canon without anyone deciding | flags with both versions; retire, don't delete |
| Over-broad retirement | an unscoped contradiction check retires unrelated facts ([Graphiti issue 1728](https://github.com/getzep/graphiti/issues/1728)) | a new value replaces only the same field on the same thing |
| Name collision | two people merged into one, or one split in two | type plus one anchor for every match; a human read of every near-name (`principles.md` §3) |
| Dropped fact | the resolve missed something; every consistency check still passes | resolve a known session against its expected result, now and then |
| Stale entries | out-of-date lore keeps being injected | demote what finished; keep the world current |

## 5. How others build it

Useful as vocabulary when the user already knows one of these tools.

- **Lorebooks** (SillyTavern [World Info](https://docs.sillytavern.app/usage/core-concepts/worldinfo/), [NovelAI](https://docs.novelai.net/en/text/lorebook/), KoboldAI): entries inserted when a keyword appears, with recursion (entries triggering entries), budgets, priorities, and "sticky" entries that stay for N messages. The honest version of this is a link walk.
- **Novelcrafter's codex** ([progressions](https://www.novelcrafter.com/help/docs/codex/progressions-additions), [inclusion modes](https://www.novelcrafter.com/help/docs/codex/codex-tracking)): facts tied to a point in the manuscript (so later facts never leak into earlier scenes); entries set to always / when mentioned / only via a relation / never.
- **AI Dungeon** ([memory system](https://help.aidungeon.com/faq/the-memory-system)): Plot Essentials always loaded, Story Cards on trigger, fixed shares of the context per layer so no layer starves the others.
- **Letta / MemGPT** ([memory blocks](https://docs.letta.com/guides/agents/memory-blocks/)): small always-visible core blocks with size limits, a large archive searched on demand, and background "sleep-time" passes that consolidate between sessions.
- **Zep / Graphiti** ([paper](https://arxiv.org/html/2501.13956)): the raw conversation kept as the source, facts extracted from it with the time they were true and the time they were recorded; contradicted facts retired, not deleted.
- **Mem0** ([paper](https://arxiv.org/html/2504.19413)): each extracted fact becomes one of add / update / delete / no-op; "no-op" is a decision, not a default.
- **Generative Agents** ([Park et al.](https://arxiv.org/html/2304.03442)): higher-level reflections that cite the observations they rest on.
- **The Alexandrian's campaign status document** ([post](https://thealexandrian.net/wordpress/42961/roleplaying-games/smart-prep-part-4-campaign-status-documents)): the original notes stay untouched; a per-session status document records what changed, split into what the players will run into and what happened offstage; improvised facts live in a "known facts" list until they grow up. A resolve, by hand, decades before AI.
- **Sly Flourish's Lazy DM** ([eight steps](https://slyflourish.com/eight_steps_2023.html)): prep starts from the characters; unrevealed secrets carry forward to the next session. An assembly recipe, by hand.
- **Anthropic on context** ([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)): the smallest set of high-signal tokens; lightweight references loaded just in time; a progress file read at the start of every session; state in structured files, which models are less likely to casually rewrite than prose.

## 6. What a typed, linked world adds

Everything above is buildable on plain files. A world with types and links (OnlyWorlds or the user's own) makes some of it cheaper:

- **Selection by relation, not by string**: "this place, the people in it, their families and factions, the open threads touching them" is a walk over links, the same every time.
- **Cuts by kind**: drop species lore before present characters, long descriptions before status fields, and say what was cut in the world's own terms.
- **Change as a field-level diff**: a new location replaces the old location on the same character and nothing else, so the scope of a contradiction is given, not guessed.
- **One world, many readers**: narrator, a single character, and a group of players each get their own view of the same data. In OnlyWorlds this is already a convention: a knowledge entry is a Narrative with subtype `knowledge` whose text is the knowledge, held by one character (`narrator`) or a group (`collectives`, whose members inherit it); what someone knows is computed from the entries they hold, so a secret needs no visibility flag, only an entry the players' group does not hold. See `atlas-conventions.md`.
- **Time on the world, not the chat**: dated events let a session assemble "the world as of day 212", even when sessions are played out of order.
- **Canon status as data**: provisional and contested facts can be assembled and marked, and promotion to canon is an explicit resolve decision.

## 7. Three worked shapes

**The GM** (a campaign, sessions every week). Prep assembles the characters' open threads, the carried-forward secrets, and the places the players are likely to reach. The GM's packet may hold everything; the players' packet is built only from the knowledge entries their group holds, never from canonical fields such as a place's description, so GM-only facts stay out. After play, the notes become a change list: who moved, who died (retired, dated), which secret got revealed, what the players now believe that isn't true. The per-session handover is kept; session 30 can still ask what was known at session 12.

**The chat-only roleplayer** (a big lore bible in PDFs, ChatGPT, losing details as chats compress). First a written recipe: "for a session, include the place, who is there, their open threads, and three lines of each lead's voice; everything else stays out." Then only the documents the next session needs become entries (plain markdown, one file per character or place, is enough); the rest of the bible follows over time, one document at a time, each checked for what it contributed. A build prompt fills the recipe from the entries into a brief; the session starts fresh with the brief. At the end, a resolve prompt lists changes in a fixed format; the user approves them and edits the entry files by hand. Character cognition waits for rung 4.

**The novelist with a local agent** (chapters on disk, a world folder). A skill writes `context/current.md` before each writing session: the chapter's place and date, who is present, their last scenes together, what the reader knows so far. After each chapter, a resolve skill proposes a change list into `resolves/chapter-14.md`; the author rules on the flags; the approved changes are applied to the world files; a check confirms every link resolves.
