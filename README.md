# Worldbuilding Toolkit

A general worldbuilding companion for AI assistants. Bring whatever you have — messy notes, a novel, campaign docs, a folder of world files, or nothing yet — and structure, organize, explore, and build with it.

No account required. [OnlyWorlds](https://onlyworlds.com) — an open standard for worldbuilding data — is the shared language underneath, and the optional power layer when you want one.

Works with any AI that reads markdown. Optimized for Claude Code.

## What It Does

**Structure** — Parse any text into world elements. Paste a paragraph, a chapter, upload files, point at folders. Out comes a structured world: standalone JSON, or a world folder you can open directly in [Atlas](https://atlas.onlyworlds.com).

**Organize** — Work with worlds wherever they live. Survey a world and get a creative brief, find missing connections, design complex systems (magic, factions, timelines) — from files on disk or over the API, your choice.

**Build** — Use world data as a backend for tools, games, and AI agents. REST API, TypeScript SDK, a live MCP server, no infrastructure to manage.

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

Point at the knowledge files:

- [onlyworlds-core.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/onlyworlds-core.md)
- [modeling-patterns.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/modeling-patterns.md)
- [schema-reference.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/schema-reference.md)
- [world-folder.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/world-folder.md)
- [ai-builders.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/ai-builders.md)

## Skills

| Skill | Purpose |
|-------|---------|
| **onlyworlds-start** | Entry point — understands your situation, routes you forward |
| **parsing** | Text, files, or folders → a structured world (JSON or an Atlas-openable folder) |
| **modeling** | Design consultation for complex world systems |
| **schema** | Field reference across all 22 types |
| **survey** | Read a world — from a folder on disk or the API — and get a creative brief |
| **link** | Find missing connections, enrich links, resolve orphans — folder or API |
| **api** | Fetch, create, update, delete, natural language CRUD |
| **dev** | SDK integration, project scaffolding, deployment |
| **council** | Browse and participate in schema governance |
| **project-setup** | Connect to an OnlyWorlds world (runs automatically when needed) |

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
"I'm building a game with world data"
"Connect my AI agent to a persistent world"
```

## Your Files, Your World

Most of the toolkit runs on nothing but your files:

- **Parsing, modeling, schema** work fully standalone — structured output you can use anywhere.
- **Survey and link** read a world folder straight off disk — an Atlas world, converter output, or anything in the [world folder shape](knowledge/world-folder.md).
- Parsing can emit that folder shape directly: your notes become a world Atlas opens, no account involved.

With a free OnlyWorlds account ([onlyworlds.com](https://onlyworlds.com)), the same world gains cloud sync, API access, sharing, and the growing ecosystem of apps and games. The toolkit connects automatically — and everything stays exportable, always.

## For AI Builders

OnlyWorlds is a typed, persistent, portable world-state layer for AI systems — the modeled-domain slot in a memory stack. Connect an agent through the [MCP server](https://www.onlyworlds.com/mcp), read a world folder as a clean typed corpus, or build on the API/SDK. See [ai-builders.md](knowledge/ai-builders.md) for honest positioning, connect surfaces, and patterns.

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Reference](https://www.onlyworlds.com/api/docs)
- [MCP Server](https://www.onlyworlds.com/mcp) — connect an MCP client (Claude Code/Desktop) to your world
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk)
- [Atlas](https://atlas.onlyworlds.com) — the flagship worldbuilding app (local-first: the folder is the world)
- [Feedback](https://github.com/OnlyWorlds/feedback) — bugs & feature requests, all tools
- [Discord](https://discord.gg/twCjqvVBwb)

## License

MIT
