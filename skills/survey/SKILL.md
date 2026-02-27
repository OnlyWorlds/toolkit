---
name: survey
description: Survey an OnlyWorlds world and produce a creative brief. Use when user says 'survey', 'survey world','read the world', 'feel the world', or wants an in-depth creative/emotional overview of a world's contents. Fetches all element types via API, synthesizes into a rich document that captures the soul of the world.  
---

# Survey

Fetch an entire OnlyWorlds world via API and produce a creative brief — not a data dump, but a reading of the world's soul.

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Get credentials (API-Key + API-Pin) |
| 2 | Validate + fetch world info |
| 3 | Fetch all element types (parallel) |
| 4 | Read, connect, synthesize |
| 5 | Write the brief |

| World Size | Brief Length | Approach |
|-----------|-------------|----------|
| Under 20 elements | Short (~60-80 lines) | Go deep on each element |
| 20-100 elements | Standard (~100-150 lines) | Cover shape and highlights |
| 100-300 elements | Full (~150-200 lines) | Find clusters and themes |
| 300+ elements | Focused (~150-200 lines) | Find the skeleton, don't cover everything |

## Instructions

### Step 1: Get Credentials

Check for `.ow/config.json` in current directory first:

| Config Found | credential_mode | Action |
|-------------|----------------|--------|
| Yes | full | Load API-Key + API-Pin from `.env` |
| Yes | key-only | Load API-Key from `.env`, ask user for PIN |
| Yes | manual | Ask user for both |
| No | — | Check `.env` for OW_API_KEY / OW_API_PIN, then ask user |

### Step 2: Validate + Fetch World

```bash
curl -s "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {key}" -H "API-Pin: {pin}"
```

Report: world name, description, element count. Confirm before proceeding — large worlds mean many API calls.

### Step 3: Fetch All Elements

Fetch every narrative element type. Run parallel curl calls:

```
character, creature, species, family, collective, institution,
location, zone, object, construct, title, ability, trait,
language, law, event, narrative, phenomenon, relation
```

Skip: map, pin, marker (spatial data, not narrative content).

Endpoint pattern: `GET https://www.onlyworlds.com/api/worldapi/{type}/`

**CRITICAL**: Endpoints are singular — `/character/`, not `/characters/`. Use `www.onlyworlds.com` (not bare domain). Headers are exactly `API-Key` and `API-Pin`.

### Step 4: Read the World

This is the creative step. Read all fetched data and find:

- **The skeleton**: What types dominate? Character-heavy? Institution-heavy? The distribution tells a story.
- **The web**: Trace link fields. Find clusters (elements that reference each other heavily), bridges (elements connecting clusters), and orphans (elements referencing nothing).
- **The heat**: Long descriptions signal care. Dense link webs signal importance. Named Relations signal explicit bonds.
- **The gaps**: What's conspicuously absent? A world full of Characters but no Institutions tells a story about individuals against chaos.
- **The darkness**: Tensions, contradictions, Events that changed everything.

### Step 5: Write the Brief

**Element Distribution Table** — include before prose. Quick snapshot of what exists:

```markdown
| Type | Count |
|------|-------|
| Character | 11 |
| Location | 8 |
| ... | ... |
| **Total** | **N** |
```

**Brief sections** (adapt to what the world gives you):

1. **The One Sentence** — What is this world, in one line? A feeling, not a genre label.
2. **What This World Actually Is** — Surface and underneath.
3. **The Physical World** — How it feels to be there. Locations, atmosphere, texture.
4. **The Characters** — Who they are in your gut, not stat blocks.
5. **The Emotional Core** — 2-4 things this world is *about*.
6. **What's Dark / Funny / Strange** — Whatever applies.
7. **The Web** — How things connect. Surprising links. Bridge elements.
8. **What's Missing** — Gaps as observation, not criticism.
9. **One Last Thing** — The single detail that says everything. The image or connection that lingers. End the brief here.

## Voice

**Match the world's register.** Blood Meridian shouldn't be cheery. A puppet world shouldn't be grim. The world sets the atmosphere — bring observation and wit to the reading, not a fixed tone.

The brief should feel like a friend who read your entire world overnight and is telling you about it — catching things you forgot, connecting things you didn't realize were connected, occasionally making you laugh at your own creation.

**Allowed:**
- Observations about what the data implies ("they share three Events but have no Relation — whatever's between them hasn't been named")
- Patterns the creator may not have intended ("every Location has a water source — you may not have planned a water theme, but you've got one")
- Reading emotional weight from description density and link patterns

**Not allowed:**
- Inventing facts not in the data
- Stating implications as fact ("they're in love" vs "they orbit each other")
- Filling gaps with assumptions
- Being dismissive about any world, regardless of size or quality

**The line**: Every claim traces back to element data. Interpretive readings are framed as readings ("this looks like...", "the web suggests...", "hard not to read this as...").

## Zone Filtering

Zones with no description or generic names (poly1, new zone, TRE) are likely map test data. Skip or note as artifacts — don't interpret them.

## Output

Save the brief as markdown. Suggest filename: `survey-{world-name}.md` in the current directory. The user chooses where to save.
