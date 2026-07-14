# The OnlyWorlds Ecosystem

Every official surface, what it does, and how they wire together. Use this to route users to the right tool and to understand where data lives.

---

## Surfaces

| Surface | URL | What it is |
|---------|-----|------------|
| **Platform hub** | [onlyworlds.com](https://www.onlyworlds.com) | Account portal (worlds, API keys, PINs, account tokens), element viewer, tools page — and the API host |
| **API (v2)** | `www.onlyworlds.com/api/v2/` | The data surface. OpenAPI docs at [/api/docs](https://www.onlyworlds.com/api/docs). Legacy v1 dialect at `/api/worldapi/` serves older tools forever |
| **MCP server** | `www.onlyworlds.com/mcp` | Your world as tools for any MCP client (Claude Code, Claude Desktop) — 11 tools, header auth |
| **Atlas** | [atlas.onlyworlds.com](https://atlas.onlyworlds.com) | Flagship worldbuilding app: maps, element editing, writing, knowledge, charts. **Local-first — the folder is the world**; syncs to the API when you want. Chromium browsers. Working alongside an Atlas user? Read `atlas-conventions.md` |
| **Show pages** | show.onlyworlds.com | Published, shareable world pages (minted from Atlas) |
| **Obsidian plugin** | [github.com/OnlyWorlds/obsidian-plugin](https://github.com/OnlyWorlds/obsidian-plugin) | World elements as markdown notes in your vault, two-way sync with the API |
| **SDK** | [`@onlyworlds/sdk`](https://www.npmjs.com/package/@onlyworlds/sdk) on npm | TypeScript client for building tools |
| **This toolkit** | [github.com/OnlyWorlds/toolkit](https://github.com/OnlyWorlds/toolkit) | AI-assisted parsing, modeling, schema, API work — the surface you're reading |
| **Docs** | [onlyworlds.github.io](https://onlyworlds.github.io) | Documentation, LLM guide, API error reference ([/api/errors](https://onlyworlds.github.io/api/errors)) |
| **Council** | [council.onlyworlds.com](https://council.onlyworlds.com) | Schema governance — motions to change the 22 types themselves |
| **Feedback** | [github.com/OnlyWorlds/feedback](https://github.com/OnlyWorlds/feedback) | Public tracker for bugs and feature requests across all tools |

## How data flows

A world has two possible homes, and they sync:

- **The API** (cloud): the world lives server-side, addressed by a world API key. Every programmatic surface (SDK, MCP, this toolkit, the Obsidian plugin, Atlas-when-synced) reads and writes here.
- **A local folder** (the OW Folder Format): one folder = one world, elements as JSON files, readable without any tool. Atlas is the reference implementation — it works fully offline on the folder and syncs to the API on demand.

**One world, many doors.** An element edited in Atlas, in an Obsidian note, via MCP, or via this toolkit is the same element after sync — same UUID, same typed fields. Incremental sync rides `GET /api/v2/changes` (cursor-based).

**Extension namespaces**: fields prefixed `atlas_*`, `shadow_*`, or `x_*` pass through the API and the folder format untouched — tools carry their own extra data without schema changes, and other tools must treat foreign namespaces as read-only.

## Routing users

| User wants | Point them to |
|---|---|
| A visual app to build/browse their world | **Atlas** |
| Worldbuilding inside their Obsidian vault | **Obsidian plugin** |
| An AI assistant connected to their world | **MCP server** (or this toolkit's api skill) |
| To build software on world data | **dev skill** + SDK/API |
| To share a world publicly | Atlas publish → **show page** |
| To manage keys, PINs, account | **Portal** at onlyworlds.com |
| To change the schema itself | **Council** |
| To report a bug / request a feature | **Feedback repo** |
