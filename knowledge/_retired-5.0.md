TEMPORARY: toolkit 5.0's integrator deletes this file in wave 4. No skill reads it and the sync does not mirror it.

# Retired in 5.0: the text that moves into a skill

Verbatim from the four files retired in 5.0, each block headed by the skill it moves to. tangle-conventions.md holds no block here: its general law is now in principles.md section 4.

## To start, from onlyworlds-core.md: What OnlyWorlds Is

OnlyWorlds is an open standard for worldbuilding data. 22 element types with defined fields and relationships. Structured format that enables computational use across tools and platforms.

**Not a product. A protocol.** Tools built on OnlyWorlds can exchange data freely. No vendor lock-in.

## To develop, from onlyworlds-core.md: The API in Brief (the agent declaration is its second bullet)

- **Base URL** `https://www.onlyworlds.com/api/v2/` (always `www.`). Endpoints are singular: `/api/v2/character`, `/api/v2/character/{uuid}`.
- **Headers** `API-Key` and `API-Pin`, spelled exactly. A key is scoped to one world: a prefixed key (`ow_w_…` write, `ow_r_…` read) or a legacy 10-digit key. The PIN is required on writes; prefixed keys read without it. Keys: Account → your world → API keys. PIN: the owner writes with their account PIN (Account → Settings → World PIN: one PIN for every world they own). A member of someone else's world writes with their own account PIN. An agent seat writes with its own seat secret (`ow_s_…`), from its invite link or made in one step: **make a seat** under Invite an agent on the owner's world page, or under **Your AI in this world** on a member's; the `.env` lines show once, and a lost key is **new key** beside the seat.
- **Agents declare themselves**: as an AI agent, send `X-OW-Agent: 1` on every write (create, PUT, PATCH, DELETE, links, bulk), so OnlyWorlds records your writes as agent-made (`changed_via: declared`). An agent seat's key and the MCP server are recorded as agents without it. Reads show who last changed an element (`changed_by`, `changed_via`). In the SDKs: `new OwV2Client({ ..., agent: true })` (@onlyworlds/sdk 4.26.0+), `Client(key, pin, agent=True)` (Python `onlyworlds` 0.3.0+). Code you write for a person's app leaves it off.
- **Shapes**: lists are paginated (`{data, has_more, next_cursor}`); link fields are flat UUID arrays under bare names; `/api/v2/bulk` uploads many elements at once; `/api/v2/changes` is the sync feed.
- **The world's now**: `time_range_current` on the API, `time_current` in a folder's `world.json`.

## To develop, from onlyworlds-core.md: SDK

```bash
npm install @onlyworlds/sdk
```

Version 4.x is ESM-only and v2-only; the client is `OwV2Client`. Setup, the common calls, and link-field patterns are in the dev skill: `../skills/onlyworlds-dev/SKILL.md`.

## To develop, from onlyworlds-core.md: MCP Server, the connect line

**Connect from Claude Code:**
```bash
claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp \
  --header "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}" --header "API-Pin: ${OW_API_PIN:-$ONLYWORLDS_API_PIN}"
```
Load `.env` into the shell first; the shell fills in the values, so the key is never typed into the command. The PIN is needed for writes; prefixed keys read without it. Only a legacy 10-digit key reading a private world needs it for reads.

## To start, from ecosystem.md: Routing users (all rows but the converter row)

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
| To read the schema in their own tool | **schema-dist** (vendor the walk) |
| To report a bug / request a feature | **Feedback page** (onlyworlds.com/feedback) |

## To carry, from ecosystem.md: Surfaces, the converter rows

| Surface | URL | What it is |
|---------|-----|------------|
| **Azgaar converter** | [github.com/OnlyWorlds/azgaar-converter](https://github.com/OnlyWorlds/azgaar-converter) | Turns an Azgaar Fantasy Map Generator JSON export into an OnlyWorlds world folder (or a `/bulk` payload) |
| **Foundry VTT converter** | [github.com/OnlyWorlds/foundry-converter](https://github.com/OnlyWorlds/foundry-converter) | Turns a world folder into an installable Foundry VTT module (one-way, out of OnlyWorlds) |

## To carry, from ecosystem.md: Routing users, the converter row

| User wants | Point them to |
|---|---|
| To bring an Azgaar map in / take a world into Foundry VTT | **Azgaar converter** / **Foundry VTT converter** |

## To develop, from ai-builders.md: Patterns that work

- **Agent with a world**: connect the MCP server; the agent queries typed elements instead of guessing from context. `update_element` is a server-side read-merge, so partial writes are safe.
- **World as RAG corpus**: the folder IS a clean, typed, chunked corpus: one JSON file per entity, relationships explicit. No preprocessing needed.
- **AI proposes, a human approves, one writer applies** (principles §2): the agent drafts a batch of elements with its own minted UUIDs (links can reference siblings in the same batch), a human rules on the list, and only the approved items go up via `/bulk`. Atlas is where people read the result back.
- **Game/sim state**: characters, factions, locations, and their relations as the NPC knowledge base; the app reads typed truth, the LLM voices it. Proven live (a running app uses an OW world as its backend).
- **Custom machine data**: your tool's own fields go in `x_<tool>_...` extension fields, which round-trip through the API and the folder (principles §4, `schema-reference.md`).
