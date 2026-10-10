---
name: onlyworlds-survey
description: "Read a whole world and say what it contains and what carries weight: a creative brief. Use when the user says 'survey my world', 'read my world', 'what do I actually have'. A world folder or an account world."
---

# Survey

Read a world (from a folder on disk or via the API) and write a creative brief: a reading of what the world is about and where its weight sits. Code counts the world; the model reads the parts that matter.

Shared rules every skill follows: `knowledge/principles.md` (here especially §2 "Code counts, the model judges" and §5).

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Pick the source: world FOLDER (read world.json + walk elements/*/, see `knowledge/world-folder.md`) or API (credentials) |
| 2 | API: fetch world info |
| 3 | API: fetch all element types in parallel |
| 4 | Count: distribution, link degree, orphans, clusters, bridges, text weight (a script, not the model) |
| 5 | Read: everything in a small world; the top-N elements in a large one |
| 6 | Write the brief (true-as-of + not-read lines, then the distribution table) |

| World Size | Brief Length | Approach |
|-----------|-------------|----------|
| Under 20 elements | Short (~60-80 lines) | Go deep on each element |
| 20-100 elements | Standard (~100-150 lines) | Count, then read everything; cover shape and highlights |
| 100-300 elements | Full (~150-200 lines) | Count first; read the top ~40 plus every bridge |
| 300+ elements | Focused (~150-200 lines) | Count first; read the top ~40 plus bridges and a sample per cluster |

## Instructions

### Step 1: Pick the Source

- **World folder** (no account, no network): the user has an Atlas world folder, converter output, or any OW-shaped folder. Read `world.json` for meta, walk `elements/*/` keying on internal `id`, never the filename (`knowledge/world-folder.md`), then skip to Step 4.
- **API**: check for `.ow/config.json` in the current directory first. `credential_mode` full: load API-Key + API-Pin from `.env`. key-only: load API-Key and proceed; a PIN is needed only if a read returns 401 (legacy key on a private world). No config: check `.env` for ONLYWORLDS_API_KEY / ONLYWORLDS_API_PIN. Anything missing (or manual mode): ask the user to add it to `.env` themselves, as project-setup does, rather than paste it into chat. Never print a credential.

### Step 2: Validate + Fetch World

```bash
curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: $ONLYWORLDS_API_KEY" -H "API-Pin: $ONLYWORLDS_API_PIN"
```

Report: world name and description. The element count comes from Step 4 (the distribution table in Step 6).

### Step 3: Fetch All Elements

Fetch every narrative element type. Run parallel curl calls:

```
character, creature, species, family, collective, institution,
location, zone, object, construct, title, ability, trait,
language, law, event, narrative, phenomenon, relation
```

Skip: map, pin, marker (spatial data, not narrative content).

Endpoint pattern: `GET https://www.onlyworlds.com/api/v2/{type}?limit=1000` (the maximum page size)

Follow the api skill's list rules (singular endpoints, `www.`, exact headers). Paginate: follow `next_cursor` until `has_more` is false, or you survey page one only. Link fields come back as UUIDs; resolve names through the id map you build while fetching.

### Step 4: Count the World

Counting is a job for a short script or query over the folder or the fetched data, never for the model reading prose. Write a small throwaway script for the user's setup (no script ships with the toolkit). Build an id → element map, then compute:

- **Distribution**: element count per type.
- **Link degree**: per element, outgoing links plus incoming links (backlinks). A link is any field whose value is an id, or a list of ids, found in the id map.
- **Orphans**: elements with degree 0.
- **Clusters**: connected groups in the link graph, with their sizes.
- **Bridges**: elements that connect two clusters, or whose removal splits one.
- **Text weight**: characters of `description` plus `story` per element.

Save the numbers in a small table or file. The brief cites them; the model does not recount them.

### Step 5: Read the World

This is the creative step. Under ~100 elements, read everything. Above that, read only the top-N elements (~40, scaled to the brief length) by link degree and by text weight, every bridge, and a few from each cluster. The rest are known by their counts, and the brief says so.

From what you read, find:

- **The skeleton**: What types dominate? Character-heavy? Institution-heavy? The distribution tells a story.
- **The web**: Which clusters form, what the bridges join, what the orphans are.
- **The heat**: Long descriptions signal care. Dense link webs signal importance. Named Relations signal explicit bonds. Narrative `story` holds the prose; read it as the densest heat signal.
- **The gaps**: What's conspicuously absent? A world full of Characters but no Institutions tells a story about individuals against chaos.
- **The darkness**: Tensions, contradictions, Events that changed everything.

### Step 6: Write the Brief

**Head the brief with two lines** (principles §2 "Say what you didn't do" and §5):

```markdown
True as of: {when the data was read} from {folder path or API world name}
Not read: {M} of {N} elements read in full; the rest known only by their counts. Skipped: {map, pin, marker, test zones}
```

**Element Distribution Table**: include before prose. Quick snapshot of what exists:

```markdown
| Type | Count |
|------|-------|
| Character | 11 |
| Location | 8 |
| ... | ... |
| **Total** | **N** |
```

**Brief sections** (adapt to what the world gives you):

1. **The One Sentence**: What is this world, in one line? A feeling, not a genre label.
2. **What This World Actually Is**: Surface and underneath.
3. **The Physical World**: How it feels to be there. Locations, atmosphere, texture.
4. **The Characters**: Who they are in your gut, not stat blocks.
5. **The Emotional Core**: 2-4 things this world is *about*.
6. **What's Dark / Funny / Strange**: Whatever applies.
7. **The Web**: How things connect. Surprising links. Bridge elements.
8. **What's Missing**: Gaps as observation, not criticism.
9. **One Last Thing**: The single detail that says everything. The image or connection that lingers. End the brief here.

## Voice

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

## Zone Filtering

Zones with no description or generic names (poly1, new zone, TRE) are likely map test data. Skip or note as artifacts; don't interpret them.

## Output

Write the brief to `survey-{world-name}.md` in the current directory (or where the user asked) and report the path. Then offer the next step: orphans and bridges feed the link skill; preparing a session from this world is the context skill.
