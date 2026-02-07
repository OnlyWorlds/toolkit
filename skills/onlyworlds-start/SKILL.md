---
name: onlyworlds-start
description: This skill should be used when a user is new to OnlyWorlds, asks what OnlyWorlds is, wants to know what this toolkit can do, or is unsure where to begin. Entry point for orientation and discovery - understands user situation then routes to appropriate skills (parsing, modeling, dev, api, schema, project-setup).
---

# OnlyWorlds Start

Entry point for users new to OnlyWorlds or unsure where to begin.

## Process

### 1. Discover User Situation

Ask about worldbuilding context:

- **What exists?** Notes, manuscripts, campaign logs, wiki pages, scattered docs, nothing yet?
- **What's being built?** Novel, TTRPG campaign, game, tool, personal project?
- **What's the challenge?** Organizing chaos, designing systems, building tools, just exploring?

**Do not assume full OnlyWorlds adoption is the goal.** Some users just want structured JSON from their notes. Some want design consultation. Some want to explore the schema without committing to anything. Some are developers needing a backend. All of these are valid uses.

### 1b. Check for Existing Project Setup

Look for `.ow/` folder in current directory:

- **If exists**: Project already connected. Load world name from `.ow/config.json`. Mention: "I see you're connected to '{world_name}'."
- **If not**: No setup yet (fine for many workflows).

### 2. Explain OnlyWorlds (When Relevant)

OnlyWorlds is an open standard for worldbuilding data. 22 element types represent any fictional world:

- Characters, Creatures, Species
- Locations, Maps, Zones
- Objects, Constructs, Abilities
- Institutions, Families, Collectives
- Events, Narratives, Phenomena 

The point: structured data that works everywhere. Parse a novel, get queryable JSON. Build a game, fetch world data via API. Switch tools without losing the world.

**Not a product. A protocol.** Free, open source, no lock-in.

### 3. Match Needs to Skills

Based on user situation, explain relevant capabilities:

| User Need | Skill(s) | What Happens |
|-----------|----------|--------------|
| "I have existing text" | project-setup (if world) → parsing | If user has OnlyWorlds world, setup runs first automatically. Then parsing extracts elements from prose → structured JSON |
| "I'm designing something complex" | modeling | Design consultation for magic systems, factions, tech trees - compositional thinking |
| "I want to build tools/games" | dev | SDK setup, project scaffolding, deployment - OnlyWorlds as headless backend |
| "I need to sync data" | api | CRUD operations - fetch, upload, sync with OnlyWorlds |
| "What fields exist?" | schema | All 22 types, all fields - reference and validation |

**Note on project-setup**: This isn't a user-facing skill - it's infrastructure that runs automatically when needed. Users never invoke it directly. They say "I want to parse" and we ensure setup happens first if they have a world.

### 4. Account Check (For Parsing/API Work)

If user wants to parse text or use the API, ask:

> "Do you have an OnlyWorlds account with a world you'd like to use?"

**If NO**:
- "No problem! You can parse text to JSON and use it locally."
- "Want to create an account? It's free at onlyworlds.com"
- Route to parsing skill (outputs local JSON only)

**If YES - MANDATORY Setup Check**:

**BEFORE doing anything else** (before reading files, before parsing, before asking more questions), check for project setup:

1. **Check for `.ow/` folder** in current directory
   ```bash
   test -d .ow && echo "EXISTS" || echo "NOT_EXISTS"
   ```

2. **If output is "NOT_EXISTS":**
   - **STOP** - Do NOT proceed to parsing, file reading, or further questions
   - Tell user: "Let's set up your project connection first - this enables reconciliation and prevents duplicates"
   - **Immediately invoke** `Skill(skill: "onlyworlds:project-setup")`
   - **Wait** for project-setup to complete (it will create .ow/ folder and cache)
   - Only AFTER project-setup completes: proceed to parsing

3. **If output is "EXISTS":**
   - Load world name from `.ow/config.json`
   - Confirm: "I see you're connected to '{world_name}'"
   - Load cache from `.ow/world-cache.json`
   - Proceed with reconciliation-aware parsing

**This check is NON-NEGOTIABLE for users with OnlyWorlds accounts.** Without it, parsing creates duplicates and breaks reconciliation.

**Why this matters:**
- Without setup: No cache = duplicate elements, no reconciliation, manual UUID resolution
- With setup: Cache enables smart matching, prevents duplicates, tracks changes

**Don't skip project-setup for users with worlds** - it's essential for reconciliation. But for users without worlds, parsing works great standalone.

### 5. Standalone Use

The toolkit works without an OnlyWorlds account. Parsing outputs clean JSON you can use anywhere. Modeling and schema knowledge work standalone too.

With an account, you get cloud storage, API sync, visual tools, and collaboration. Many users start local, add a world later. Both paths are valid.

### 6. Route Forward

Once situation is clear, suggest next steps:

**If user has text + OnlyWorlds world:**
- "Let me set up your project first (quick - just need credentials), then we'll parse your text"
- Setup enables reconciliation and prevents duplicates - don't skip it

**If user has text, no world:**
- "Let's parse that text to JSON - you can use it locally or create a world later"

**If user wants modeling:**
- "Let's work through that {system} design together"

**If user wants to build tools:**
- "Let's scaffold a project and set up the SDK"

Or continue exploring if the user is still figuring things out.

### 7. When to Suggest the Agent

For complex ongoing work, mention the ow-agent:

> "For ongoing parsing projects (like parsing Day 1, Day 2, Day 3 of a story), the ow-agent can help orchestrate the workflow and track state across sessions."

The agent is optional - skills handle most cases. But for power users doing sequential parsing with reconciliation, the agent provides better orchestration.

## Tone

Curious, not salesy. Help users find what fits.  