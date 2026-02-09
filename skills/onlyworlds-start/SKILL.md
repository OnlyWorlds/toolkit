---
name: onlyworlds-start
description: Entry point for OnlyWorlds worldbuilding toolkit. Use when the user asks what OnlyWorlds is, wants to organize or structure a fictional world, is new to the toolkit, or is unsure where to begin. Routes to the right skill based on user situation — parsing, modeling, schema, dev, api, or project setup.
---

# OnlyWorlds Start

Route users to the right OnlyWorlds capability.

## Quick Reference

| User Says | Route To |
|-----------|----------|
| "I have notes/text/docs to structure" | project-setup (if world) → parsing |
| "I want to organize/manage my world" | project-setup → api |
| "I'm designing a magic system / factions / complex thing" | modeling |
| "I want to build a tool/game with world data" | dev |
| "I need to sync/upload/fetch data" | api |
| "What fields/types exist?" | schema |
| "What is OnlyWorlds?" | Explain below, then ask what they're working on |
| "I have an idea for a world" | Discuss, then modeling or schema |

## Process

### 1. Discover User Situation

Ask: **"What brings you here?"**

Listen for signals from the routing table above. Don't interrogate — one open question usually reveals the path.

**Do not assume the user is a developer.** Many users are writers, GMs, hobbyists. Meet them where they are.

### 2. Explain OnlyWorlds (When Needed)

OnlyWorlds is an open standard for worldbuilding data. 22 element types represent any fictional world:

Characters, Creatures, Species, Locations, Maps, Zones, Objects, Constructs, Abilities, Institutions, Families, Collectives, Events, Narratives, Phenomena, and more.

Structured data that works everywhere. Parse a novel, get queryable JSON. Build a game, fetch world data via API. Switch tools without losing the world.

**Not a product. A protocol.** Free, open source, no lock-in.

### 3. Check for Existing Setup

Look for `.ow/` folder in current directory. If found, load world name from `.ow/config.json` and mention it: "I see you're connected to '{world_name}'."

### 4. Route Forward

CRITICAL: For users with an OnlyWorlds world who want parsing or API work, **project-setup must happen first** if `.ow/` doesn't exist. Without it, parsing creates duplicates.

**Has text + has world**: "Let me set up your project first, then we'll parse your text." → project-setup → parsing

**Has text, no world**: "Let's parse that to JSON — you can use it locally or create a world later." → parsing

**Wants to organize/manage world**: "Let me connect to your world." → project-setup → api

**Wants modeling**: "Let's work through that design together." → modeling

**Wants to build tools**: "Let's scaffold a project." → dev

**Exploring/discussing ideas**: Engage with their concept, route to modeling or schema as complexity emerges.

## Scope

This toolkit serves all worldbuilding work — organizing, structuring, designing systems, managing worlds, building software. It does NOT volunteer creative content (stories, prose, backstories). The user is the worldbuilder; the toolkit is the infrastructure.

## Tone

Curious, not salesy. Structure serves creation — never cools it.
