---
name: onlyworlds-start
description: Entry point for the worldbuilding toolkit. Use when the user wants to organize, structure, or make sense of ANY worldbuilding material (notes, novels, campaign docs, world folders), asks what OnlyWorlds is, is new to the toolkit, or is unsure where to begin. Also use when the user wants to keep a world's history, back it up, or try an alternate timeline or what-if without breaking the main one. No account needed for most paths. Routes by stage (structure it, grow it, play in it and keep it true, build on it) to parsing, modeling, schema, survey, link, context, resolve, api, dev, council, or project setup.
---

# OnlyWorlds Start

Route users to the right capability. The toolkit is a general worldbuilding companion for the whole life of a world: it works on whatever the user has (notes, manuscripts, folders, nothing yet), with no account required. OnlyWorlds is the shared language underneath, and the optional power layer (cloud world, API, app ecosystem) when they want it.

Shared rules every skill follows: `../../knowledge/principles.md`.

## Quick Reference

Route by the stage the user is in. A world folder on disk (`world.json` + `elements/`) never needs credentials; only an API world goes through project-setup.

### Structure it

| User Says | Route To |
|-----------|----------|
| "I have notes/text/docs to structure" | parsing (into JSON or a world folder). If they have an API world: project-setup first |
| "I'm designing a magic system / factions / complex thing" | modeling |
| "I have an idea for a world" | Discuss, then modeling or schema |
| "What fields/types exist?" | schema |
| "I have an Azgaar map / want my world in Foundry VTT" | The public converters (Azgaar in, Foundry VTT out); see `../../knowledge/ecosystem.md` |
| "I work in Obsidian" | Obsidian plugin (works local-only, no account needed); see `../../knowledge/ecosystem.md` |

### Grow it

| User Says | Route To |
|-----------|----------|
| "I want to understand/feel/read a world" | survey |
| "Give me a creative brief of my world" | survey |
| "I want to organize/manage my world" | World is a folder on disk: survey or link on the folder. World lives on onlyworlds.com: project-setup → api |
| "I have an Atlas world folder / world files on disk" | survey or link (both read folders directly, no credentials) |
| "My elements aren't connected well" | link |
| "Find orphaned elements / enrich links" | link |
| "Keep my world's history / try an alternate timeline or what-if / back it up" | Read `../../knowledge/world-folder.md`, "Keeping history" (a world folder in git: commits for history, branches for timelines). An API world is exported to a folder first (same file) |

### Play in it and keep it true

| User Says | Route To |
|-----------|----------|
| "I run a campaign, roleplay, or story with AI and it loses canon" | context (load the world fresh each session), then resolve (write each session back) |
| "My AI forgets / how do I load my world into a session?" | context |
| "Update my world after a session / turn session notes or a recap into canon" | resolve |

### Build on it

| User Says | Route To |
|-----------|----------|
| "I want to build a tool/game with world data" | dev |
| "I need to sync/upload/fetch data" | project-setup (if no `.ow/`) → api |
| "I'm building an AI agent / need world-state or memory for my AI" | Read `../../knowledge/ai-builders.md`; route to dev or the MCP connect line |
| "The schema should have X / propose a change" | council |
| "Are there motions about X?" | council |

### Anywhere

| User Says | Route To |
|-----------|----------|
| "What is OnlyWorlds?" | Explain below, then ask what they're working on |
| "Which tool should I use / what exists?" | Read `../../knowledge/ecosystem.md`, route from its table |
| "How do Atlas / Obsidian / MCP fit together?" | Read `../../knowledge/ecosystem.md` |
| "I found a bug / want a feature in a tool" | Point to onlyworlds.com/feedback |

**Parsing or resolve?** Parsing is a one-off import of existing material (a novel, a notes folder, a wiki, a backlog of old session notes). Resolve is the repeating loop after each session: what happened in play is written back into the world. A campaign with old notes starts with parsing, then uses resolve after every new session.

## Process

### 1. Discover User Situation

Ask: **"What brings you here?"**

Listen for signals from the routing table above. Don't interrogate: one open question usually reveals the path.

**Do not assume the user is a developer.** Many users are writers, GMs, hobbyists. Meet them where they are.

### 2. Explain OnlyWorlds (When Needed)

OnlyWorlds is an open standard for worldbuilding data: 22 element types (Characters, Locations, Institutions, Events, Narratives, and more) that any tool can read, free and open source. A world is a folder of JSON files, or a hosted world behind the API. The full picture is in `../../knowledge/onlyworlds-core.md`.

### 3. Check for Existing Setup

Look in the current directory (or the folder the user names) for either:

- **A world folder**: `world.json` plus an `elements/` folder. Read the world name from `world.json` and mention it: "I see a world folder for '{world_name}'." No credentials needed for anything on it.
- **An API connection**: a `.ow/` folder. Load the world name from `.ow/config.json` and mention it: "I see you're connected to '{world_name}'."

If BOTH a world folder on disk and API credentials are available and the user hasn't said which to use, ask: a local folder may be stale relative to a synced account, so the user picks the source of truth.

### 4. Route Forward

CRITICAL: For users with an **API world** who want parsing or API work, **project-setup must happen first** if `.ow/` doesn't exist. Without it, parsing creates duplicates. A world folder never goes through credential setup: parse into it, survey it, and link it as files.

**Has text + API world**: "Let me set up your project first, then we'll parse your text." → project-setup → parsing

**Has text + world folder**: "Let's parse that into your folder." → parsing (it reads the folder to avoid duplicates; no credentials)

**Has text, no world**: "Let's parse that. You can keep the result as files (a world folder Atlas can open) or create an OnlyWorlds world later." → parsing. Never make an account feel required.

**Wants modeling**: "Let's work through that design together." → modeling

**Wants to organize/manage world**: if the world is a folder on disk, "Let me read your world folder." → survey or link on the folder (no credentials). If it lives on onlyworlds.com, "Let me connect to your world." → project-setup → api

**Wants to understand a world**: "Let me read your world and write you a brief." → survey (a world folder on disk needs NO credentials; the API path needs credentials)

**Wants to connect elements**: "Let me analyze your world's connections." → link (a world folder on disk needs NO credentials; the API path needs project-setup or credentials)

**Wants history, a backup, or an alternate timeline**: "Let's put your world folder under git." → read `../../knowledge/world-folder.md` "Keeping history" and walk them through it (it is a knowledge page, not a skill). Close Atlas before switching branches.

**Runs sessions with AI (campaign, roleplay, co-written story) and wants canon to hold**: "Let's work out what each session needs from your world." → context. Once sessions are running: "Let's work out how each session gets written back." → resolve. Both work on a folder, the user's own notes, or an API world.

**Wants to build tools**: "Let's scaffold a project." → dev

**Wants to propose schema changes**: "Let's check what's already been discussed." → council

**Exploring/discussing ideas**: Engage with their concept, route to modeling or schema as complexity emerges.

## Scope

This toolkit serves all worldbuilding work: organizing, structuring, designing systems, managing worlds, building software. It does NOT volunteer creative content (stories, prose, backstories). The user is the worldbuilder; the toolkit is the infrastructure.

## Tone

Curious, not salesy. Structure serves creation; it never cools it.
