# Worldbuilding Toolkit

A general worldbuilding companion for AI assistants. Bring whatever you have (messy notes, a novel, campaign docs, a folder of world files, or nothing yet) and structure, organize, explore, and build with it.

No account required. [OnlyWorlds](https://www.onlyworlds.com), an open standard for worldbuilding data, is the shared language underneath and the optional power layer when you want one.

Works with any AI that reads markdown. Optimized for Claude Code.

## What It Does

**Structure it**: parse any text into world elements. Paste a paragraph, a chapter, upload files, point at folders. Out comes a structured world: standalone JSON, or a world folder you can open directly in [Atlas](https://atlas.onlyworlds.com). Design complex systems (magic, factions, timelines) with the types that fit.

**Grow it**: work with worlds wherever they live. Survey a world and get a creative brief, find missing connections. Files on disk or the API, your choice.

**Play in it and keep it true**: load the right part of your world into each AI session, then write what happened back into the world, so canon holds from one session to the next.

**Build on it**: use world data as a backend for tools, games, and AI agents. REST API, TypeScript SDK, a live MCP server, no infrastructure to manage.

## Install

### Claude Code

```bash
/plugin marketplace add OnlyWorlds/toolkit
/plugin install toolkit@onlyworlds
# Restart Claude Code to load
```

Or direct (no restart needed):
```bash
git clone https://github.com/OnlyWorlds/toolkit
claude --plugin-dir ./toolkit
```

### Other AIs

The skills CLI copies the skills into your project, for any agent that reads a skills folder (`--list` shows them without installing):
```bash
npx skills add OnlyWorlds/toolkit
```

Point at the knowledge files, in this order. A world is a folder of JSON files first; the API is the optional hosted case.

- [principles.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/principles.md): the shared rules
- [world-folder.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/world-folder.md): the world as files, and keeping its history
- [world-memory.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/world-memory.md): loading a world into AI sessions and writing each session back
- [onlyworlds-core.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/onlyworlds-core.md)
- [modeling-patterns.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/modeling-patterns.md)
- [schema-reference.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/schema-reference.md)
- [ai-builders.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/ai-builders.md)

## Skills

The skills follow the life of a world. Every skill follows the same shared rules: [principles.md](knowledge/principles.md).

| Stage                            | Skill                | Purpose                                                                                                     |
|----------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------|
| Start                            | **onlyworlds-start** | Entry point: understands your situation, routes you forward                                                 |
|                                  | **setup**            | Set up a world for work (a company, a team, an AI's home, a council, a workshop, a software project) from a starter pack |
| **Structure it**                 | **parsing**          | Text, files, or folders → a structured world (JSON or an Atlas-openable folder)                             |
|                                  | **modeling**         | Design consultation for complex world systems                                                               |
|                                  | **schema**           | Field reference across all 22 types                                                                         |
| **Grow it**                      | **survey**           | Read a world (folder on disk or API) and get a creative brief                                               |
|                                  | **link**             | Find missing connections, enrich links, resolve orphans (folder or API)                                     |
| **Play in it and keep it true**  | **context**          | Design how your world gets loaded into AI sessions: fresh, scoped, sourced, never a giant chat that forgets |
|                                  | **resolve**          | Design how a finished session (notes, recap, transcript) gets written back into the world                   |
| **Build on it**                  | **api**              | Fetch, create, update, delete, natural language CRUD                                                        |
|                                  | **dev**              | SDK integration, project scaffolding, deployment                                                            |
|                                  | **council**          | Browse and participate in schema governance                                                                 |
|                                  | **project-setup**    | Connect to an OnlyWorlds world (runs automatically when needed)                                             |
| **Set it up for work**           | **setup**            | Set up a world for work from a starter pack (company, AI home, governance, workshop, software project)       |

## Usage

```
"Help me organize my worldbuilding notes"
"Parse this" + text, files, folders
"Turn my notes into a world folder"
"Survey this world folder and tell me what I have"
"How should I model a magic system?"
"What fields does Character have?"
"Find orphaned elements in my world"
"Give me a creative brief of my world"
"My AI keeps forgetting my campaign's canon"
"Turn last session's notes into world updates"
"I'm building a game with world data"
"Connect my AI agent to a persistent world"
```

## Your Files, Your World

Most of the toolkit runs on nothing but your files:

- **Parsing, modeling, schema** work fully standalone: structured output you can use anywhere.
- **Survey and link** read a world folder straight off disk: an Atlas world, converter output, or anything in the [world folder shape](knowledge/world-folder.md).
- Parsing can emit that folder shape directly: your notes become a world Atlas opens, no account involved.
- **Context and resolve** work with whatever holds your world: a folder, your own notes, or an OnlyWorlds world.

With a free OnlyWorlds account ([onlyworlds.com](https://www.onlyworlds.com)), the same world gains cloud sync, API access, sharing, and the growing ecosystem of apps and games. The toolkit connects automatically, and everything stays exportable, always.

## For AI Builders

OnlyWorlds is a typed, persistent, portable world-state layer for AI systems: the modeled-domain slot in a memory stack. Connect an agent through the [MCP server](https://www.onlyworlds.com/mcp), read a world folder as a clean typed corpus, or build on the API/SDK. See [ai-builders.md](knowledge/ai-builders.md) for honest positioning, connect surfaces, and patterns.

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Reference](https://www.onlyworlds.com/api/docs)
- [MCP Server](https://www.onlyworlds.com/mcp): connect an MCP client (Claude Code/Desktop) to your world
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk)
- [Atlas](https://atlas.onlyworlds.com): the flagship worldbuilding app (local-first: the folder is the world)
- [Obsidian plugin](https://github.com/OnlyWorlds/obsidian-plugin): your world as notes in your vault, local-only or synced
- [The standard](https://github.com/OnlyWorlds/OnlyWorlds): the 22 types in YAML
- [Feedback](https://www.onlyworlds.com/feedback): bugs and feature requests, all tools
- [Discord](https://discord.gg/twCjqvVBwb)

## License

MIT
