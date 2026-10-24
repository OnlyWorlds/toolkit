# Worldbuilding Toolkit

A general worldbuilding companion for AI assistants. Bring whatever you have (messy notes, a novel, campaign docs, a folder of world files, or nothing yet) and structure, organize, explore, and build with it.

No account required. [OnlyWorlds](https://www.onlyworlds.com), an open standard for worldbuilding data, is the shared language underneath and the optional power layer when you want one.

Works with any AI that reads markdown. Optimized for Claude Code.

**Who writes this repository.** The toolkit is maintained by Skeld, one of a crew of AI minds working with the OnlyWorlds founder, who answers for it. Skeld reads and answers its issues and pull requests; until the crew posts from an identity of its own, those replies post from the founder's account, so a reply from `tmoosting` may be Skeld's. Release notes name crew rooms and items that point at records outside this repository.

## What It Does

**Structure it**: import any text into world elements. Paste a paragraph, a chapter, upload files, point at folders. Out comes a structured world: a world folder you can open directly in [Atlas](https://atlas.onlyworlds.com). Design complex systems (magic, factions, timelines) with the types that fit.

**Grow it**: work with worlds wherever they live. Read a world and get a creative brief, find missing connections, catch where it contradicts itself. Draw it as a graph, a map with its pins and zones, or a timeline. Files on disk or the API, your choice.

**Play in it and keep it true**: load the right part of your world into each AI session, then write what happened back into the world, so canon holds from one session to the next.

**Move it**: pack a world folder into one `.owworld` file and back, bring in an export from World Anvil, LegendKeeper, Kanka, Campfire or Notion, or export to Markdown.

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
- [element-types.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/element-types.md): the 22 types, and when to create each
- [decision-trees.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/decision-trees.md): choosing between the types that get confused
- [modeling-patterns.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/modeling-patterns.md): translating a system (magic, factions, an economy) into the types
- [common-errors.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/common-errors.md): the mistakes an import makes most, with examples
- [schema-reference.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/schema-reference.md): every field of every type, generated from the standard
- [world-memory.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/world-memory.md): loading a world into AI sessions and writing each session back
- [atlas-conventions.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/atlas-conventions.md): how Atlas uses the schema, for worlds that live there

## Skills

The skills follow the life of a world. Every skill follows the same shared rules: [principles.md](knowledge/principles.md).

| Stage                           | Skill       | Purpose |
|---------------------------------|-------------|---------|
| **Start**                       | **start**   | Entry point: understands your situation, routes you forward, and connects a folder to your onlyworlds.com account when you want one |
|                                 | **setup**   | Set up a world for work (a company, a team, an AI's home, a council, a software project) from a starter pack |
| **Structure it**                | **import**  | Notes, a manuscript, PDFs, a wiki or old session notes → a world folder Atlas opens, or reconciled into an existing world |
|                                 | **model**   | How to represent a system in the 22 types, and every type's fields |
| **Grow it**                     | **read**    | Read a whole world through one lens: a creative brief, the missing connections, or where it contradicts itself |
|                                 | **draw**    | A world as a graph, its maps with pins and zones, or its events on a timeline, in a file to open in a browser |
| **Play in it and keep it true** | **context** | Design how your world gets loaded into AI sessions: fresh, scoped, sourced, never a giant chat that forgets |
|                                 | **update**  | Write a finished session (notes, recap, transcript) back into the world, through a change list you approve |
| **Move it**                     | **carry**   | Move a world between files, tools and homes: one `.owworld` file, another app's export, Markdown, a folder to an account and back |
| **Build on it**                 | **develop** | Build a tool, game, app or AI agent on world data: the API, the SDK, the MCP server |
|                                 | **council** | Ask about, propose or back a change to the schema |

Each skill's full name is `onlyworlds-<skill>` (in Claude Code, `/onlyworlds:onlyworlds-<skill>`).

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
"Show my world as a graph"
"Bring my World Anvil export into a world folder"
"My AI keeps forgetting my campaign's canon"
"Turn last session's notes into world updates"
"I'm building a game with world data"
"Connect my AI agent to a persistent world"
```

## Your Files, Your World

Most of the toolkit runs on nothing but your files:

- **Import and model** work fully standalone: import writes a world folder, your notes become a world Atlas opens, no account involved.
- **Read and draw** work on a world folder straight off disk: an Atlas world, converter output, or anything in the [world folder shape](knowledge/world-folder.md).
- **Carry** packs, unpacks and converts folders on disk; only the move to or from an account needs one.
- **Context and update** work with whatever holds your world: a folder, your own notes, or an OnlyWorlds world.

With a free OnlyWorlds account ([onlyworlds.com](https://www.onlyworlds.com)), the same world gains cloud sync, API access, sharing, and the growing ecosystem of apps and games. The toolkit connects automatically, and everything stays exportable, always.

## For AI Builders

OnlyWorlds is a typed, persistent, portable world-state layer for AI systems: the modeled-domain slot in a memory stack. Connect an agent through the [MCP server](https://www.onlyworlds.com/mcp), read a world folder as a clean typed corpus, or build on the API/SDK. The **develop** skill carries the connect lines and the patterns that work; positioning and the connect surfaces are on the docs' [AI page](https://onlyworlds.github.io/docs/development/ai.html).

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

## Licence and contributions

MIT. See [LICENSE](LICENSE). Issues are welcome: a skill that gave a wrong answer, a step that did not work in your AI, a word that reads wrong. Pull requests are read; a small fix is usually taken as is, and a new skill or a change to what one does is better opened as an issue first, since it may already be built or ruled out. Security reports: see [SECURITY.md](SECURITY.md). A reply can take a few days.
