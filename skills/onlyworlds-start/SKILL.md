---
name: onlyworlds-start
description: This skill should be used when a user is new to OnlyWorlds, asks what OnlyWorlds is, wants to know what this toolkit can do, or is unsure where to begin. Entry point for orientation and discovery - understands user situation then routes to appropriate skills (parsing, modeling, dev, api, schema).
---

# OnlyWorlds Start

Entry point for users new to OnlyWorlds or unsure where to begin.

## Process

### 1. Discover User Situation

Ask about worldbuilding context:

- **What exists?** Notes, manuscripts, campaign logs, wiki pages, scattered docs, nothing yet?
- **What's being built?** Novel, TTRPG campaign, game, tool, personal project?
- **What's the challenge?** Organizing chaos, designing systems, building tools, just exploring?

Do not assume full OnlyWorlds adoption is the goal. Some users want to parse notes. Some want design help. Some are developers wanting a backend.

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

| User Need | Skill | What It Does |
|-----------|-------|--------------|
| "I have existing text" | parsing | Extracts elements from prose - chapters, notes, manuscripts → structured JSON |
| "I'm designing something complex" | modeling | Design consultation for magic systems, factions, tech trees - compositional thinking |
| "I want to build tools/games" | dev | SDK setup, project scaffolding, deployment - OnlyWorlds as headless backend |
| "I need to sync data" | api | CRUD operations - fetch, upload, sync with OnlyWorlds |
| "What fields exist?" | schema | All 22 types, all fields - reference and validation |

### Parsing Depth

Parsing works at any depth:

**Raw** - Dump text, extract what's visible. Works immediately, no context needed.

**Focused** - Prioritize certain elements. A novel might care most about Characters and Events; a TTRPG about Locations and Objects.

**Vocabulary-aware** - Know project terms. "Threads" = Narrative. "Factions" = Institution. "Hongers" = Narrative with specific supertype.

**Project-aware** - Watch for things that matter to this world. Story arcs in progress. Recurring themes. Elements that need tracking.

These layers build naturally. First parse is raw. As the project develops, focus emerges. Vocabulary gets established. Awareness accumulates.

For ongoing projects, a short conversation about what matters can help - but it's not required. The parser adapts to whatever context exists.

### 4. Standalone Use

The toolkit works without an OnlyWorlds account:

- Parsing outputs JSON usable anywhere
- Modeling patterns apply to any structured worldbuilding
- Knowledge files work in any AI (ChatGPT, local LLMs)

OnlyWorlds account adds: cloud storage, API access, visual tools (maps, graphs, timelines). Optional.

### 5. Route Forward

Once situation is clear, suggest next steps:

- "There's text to organize - try parsing a sample?"
- "That magic system needs modeling - work through it together?"
- "For that visualization, scaffold a project?"

Or continue exploring if the user is still figuring things out.

## Tone

Curious, not salesy. Help users find what fits.  