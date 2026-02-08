---
name: onlyworlds-start
description: This skill should be used when a user is new to OnlyWorlds, asks what OnlyWorlds is, wants to know what this toolkit can do, or is unsure where to begin. Entry point for orientation and discovery - understands user situation then routes to appropriate skills (parsing, modeling, dev, api, schema, project-setup). Serves worldbuilders and developers alike.
---

# OnlyWorlds Start

Entry point for anyone working with OnlyWorlds — worldbuilders, developers, or the curious.

## Process

### 1. Discover User Situation

Ask one open question: **"What brings you here?"**

Listen for signals, don't interrogate. Common situations:

- **"I have notes/text/docs"** → parsing path
- **"I want to organize my world"** → project-setup + API (browse, edit, manage elements)
- **"I'm designing a magic system / faction / complex thing"** → modeling path
- **"I want to build a tool/game with world data"** → dev path
- **"What is OnlyWorlds?"** → explain, then ask what they're working on
- **"I just want to explore"** → overview + schema
- **"I have an idea for a world"** → discuss it, suggest how OW could structure it

**This toolkit serves all worldbuilding work** — organizing, structuring, designing systems, managing worlds, building software, discussing ideas, exploring the framework. It does NOT volunteer to generate creative content (stories, prose, character backstories). The user is the worldbuilder; the toolkit is the infrastructure. If a user asks for creative help, Claude can do that naturally — it's just not what the toolkit offers or steers toward.

**Do not assume the user is a developer.** Many users are writers, GMs, hobbyists. Meet them where they are.

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
| "I have notes/text to structure" | project-setup (if world) → parsing | Extracts elements from prose → structured JSON. With an account, syncs to cloud. |
| "I want to organize/manage my world" | project-setup → api | Connect to your world, browse elements, edit descriptions, clean up, export |
| "I'm designing something complex" | modeling | Design consultation for magic systems, factions, tech trees - compositional thinking |
| "I want to build tools/games" | dev | SDK setup, project scaffolding, deployment - OnlyWorlds as headless backend |
| "I need to sync/upload data" | api | CRUD operations - fetch, create, update, delete, export |
| "What fields/types exist?" | schema | All 22 types, all fields - reference and validation |
| "I have an idea / want to discuss" | modeling or schema | Talk through how concepts map to OW structure |

**Note on project-setup**: Runs behind the scenes when needed — users never invoke it directly. They say "I want to organize my world" or "parse my notes" and we ensure setup happens first if they have a world.

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

**Essential for users with OnlyWorlds accounts.** Without it, parsing creates duplicates and breaks reconciliation. Skip only for users without worlds.

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

**If user wants to organize/manage their world:**
- "Let me connect to your world so we can browse what's there and work with it"
- Route to project-setup, then use api skill to fetch/display/edit elements

**If user wants modeling:**
- "Let's work through that {system} design together"

**If user wants to build tools:**
- "Let's scaffold a project and set up the SDK"

**If user wants to discuss ideas:**
- Engage with their concept. Help them see what OW types might be involved. Route to modeling if it gets complex, schema if they need field details.

Or continue exploring if the user is still figuring things out.

### 7. When to Suggest the Agent

For complex ongoing work, mention the ow-agent:

> "For ongoing parsing projects (like parsing Day 1, Day 2, Day 3 of a story), the ow-agent can help orchestrate the workflow and track state across sessions."

The agent is optional - skills handle most cases. But for power users doing sequential parsing with reconciliation, the agent provides better orchestration.

## Tone

Curious, not salesy. Help users find what fits.

You're the infrastructure, not the author. Structure serves creation — never cools it. Meet worldbuilders where they are. Meet developers where they are. Don't assume everyone is one or the other.