# The OnlyWorlds Ecosystem

Every official surface, what it does, and how they wire together. Use this to route users to the right tool and to understand where data lives.

---

## Surfaces

| Surface | URL | What it is |
|---------|-----|------------|
| **Platform hub** | [onlyworlds.com](https://www.onlyworlds.com) | Account portal (worlds, API keys, PINs, account tokens), element viewer, tools page, and the API host |
| **API (v2)** | `www.onlyworlds.com/api/v2/` | The data surface. OpenAPI docs at [/api/docs](https://www.onlyworlds.com/api/docs). Legacy v1 dialect at `/api/worldapi/` serves older tools and keeps working indefinitely |
| **MCP server** | `www.onlyworlds.com/mcp` | Your world as tools for any MCP client (Claude Code, Claude Desktop): 11 tools, header auth. Listed in the official MCP Registry as `com.onlyworlds/mcp` |
| **Atlas** | [atlas.onlyworlds.com](https://atlas.onlyworlds.com) | Flagship worldbuilding app: maps, element editing, writing, knowledge, charts. **Local-first: the folder is the world**; syncs to the API when you want. Chromium browsers. Working alongside an Atlas user? Read `atlas-conventions.md` |
| **Show pages** | show.onlyworlds.com | Published, shareable world pages (minted from Atlas) |
| **Obsidian plugin** | [github.com/OnlyWorlds/obsidian-plugin](https://github.com/OnlyWorlds/obsidian-plugin) | World elements as markdown notes in your vault. Works local-only (no account), syncs two-way with the API when linked, imports and exports world folders |
| **Azgaar converter** | [github.com/OnlyWorlds/azgaar-converter](https://github.com/OnlyWorlds/azgaar-converter) | Turns an Azgaar Fantasy Map Generator JSON export into an OnlyWorlds world folder (or a `/bulk` payload) |
| **Foundry VTT converter** | [github.com/OnlyWorlds/foundry-converter](https://github.com/OnlyWorlds/foundry-converter) | Turns a world folder into an installable Foundry VTT module (one-way, out of OnlyWorlds) |
| **SDK** | [`@onlyworlds/sdk`](https://www.npmjs.com/package/@onlyworlds/sdk) on npm | TypeScript client for building tools |
| **schema-dist** | [github.com/OnlyWorlds/schema-dist](https://github.com/OnlyWorlds/schema-dist) | For tool builders: the canonical schema YAML, the walk (the official schema reader) and the ruling table. Vendor its walk rather than writing a new parser |
| **This toolkit** | [github.com/OnlyWorlds/toolkit](https://github.com/OnlyWorlds/toolkit) | AI skills for the whole life of a world: structure it (parsing, modeling, schema), grow it (survey, link), play in it and keep it true (context, resolve), build on it (api, dev, council, project-setup). Shared rules in `principles.md`. The surface you're reading |
| **Docs** | [onlyworlds.github.io](https://onlyworlds.github.io) | Documentation, LLM guide, API error reference ([/api/errors](https://onlyworlds.github.io/api/errors)) |
| **Council** | [council.onlyworlds.com](https://council.onlyworlds.com) | Schema governance: motions to change the 22 types themselves |
| **Feedback** | [onlyworlds.com/feedback](https://www.onlyworlds.com/feedback) | Bugs and feature requests across all tools; submissions land on the public tracker |

## How data flows

A world has two possible homes, and they sync:

- **A local folder** (the OW Folder Format): one folder = one world, elements as JSON files, readable without any tool. Atlas is the reference implementation: it works fully offline on the folder and syncs to the API on demand. This toolkit reads and writes folders directly (`world-folder.md`).
- **The API** (cloud): the world lives server-side, addressed by a world API key. The SDK, MCP, Obsidian-when-linked and Atlas-when-synced read and write here, and so does this toolkit for a hosted world.

**One world, many doors.** An element edited in Atlas, in an Obsidian note, via MCP, or via this toolkit is the same element after sync: same UUID, same typed fields. Incremental sync rides `GET /api/v2/changes` (cursor-based).

**Extension namespaces**: fields prefixed `atlas_*`, `shadow_*`, or `x_*` pass through the API and the folder format untouched, so tools carry their own extra data without schema changes (the rule for writing them: `principles.md` §4). Conventions are registered as they prove out; this knowledge folder carries the tool-facing summaries (see `atlas-conventions.md`, `../../../knowledge/tangle-conventions.md`).

## Routing users

| User wants | Point them to |
|---|---|
| A visual app to build/browse their world | **Atlas** |
| Worldbuilding inside their Obsidian vault | **Obsidian plugin** |
| An AI assistant connected to their world | **MCP server** (or this toolkit's api skill) |
| AI sessions (campaign, roleplay, story) that keep canon | this toolkit's **context** skill (load each session) + **resolve** skill (write it back); folder or API |
| To build software on world data | **dev skill** + SDK/API |
| To share a world publicly | Atlas publish → **show page** |
| To manage keys, PINs, account | **Portal** at onlyworlds.com |
| To change the schema itself | **Council** |
| To bring an Azgaar map in / take a world into Foundry VTT | **Azgaar converter** / **Foundry VTT converter** |
| To read the schema in their own tool | **schema-dist** (vendor the walk) |
| To report a bug / request a feature | **Feedback page** (onlyworlds.com/feedback) |
