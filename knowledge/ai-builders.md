# OnlyWorlds for AI Builders

OnlyWorlds is a typed, persistent, portable world-state layer an AI system can read and write. 22 element types, real relationships (UUID links between elements), a change-feed for sync, and an open format that lives equally well on disk (the world folder) or behind a REST API. Free and open source.

## The honest positioning

The agent-memory field (Zep, Mem0, MCP memory servers) keeps independently rediscovering that **typed schema beats freeform extraction** — and hand-rolls a bespoke entity schema per project, unshared and unportable. OnlyWorlds is the mature, shared instance of that insight: a schema refined against real worlds since 2012, with an ecosystem already speaking it.

Claim precisely:

| Defensible | Not our claim |
|---|---|
| Typed world-state with real relationships, portable across tools | A general agent-memory replacement |
| Open + exportable — no lock-in, speaks a shared vocabulary | Episodic memory, embeddings, auto-extraction |
| Working change-feed sync (`/changes` cursor) for multi-client state | "Solved" multi-agent memory or coordination |
| The graph slot in a hybrid memory stack — the pre-modeled domain layer | Retrieval-latency benchmarks (we don't do vector recall) |

Complement memory layers, don't compete with them: OW holds the MODELED world (who rules what, who knows whom, what exists where); episodic/vector layers hold conversation history. Game NPCs, DM copilots, simulation agents, and story systems need the first kind.

## The connect surfaces, fastest first

| Surface | One-liner | Best for |
|---|---|---|
| **MCP server** | `claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp --header "API-Key: <key>" --header "API-Pin: <pin>"` — 11 tools (schema/read/write, no delete) | Claude Code/Desktop agents, zero code |
| **World folder** | Read JSON files straight off disk (see world-folder.md) | Local pipelines, RAG corpora, zero network |
| **REST API v2** | `www.onlyworlds.com/api/v2/` — bare-name link fields, `/bulk` upsert, `/changes` sync | Any language, production apps |
| **SDK** | `npm install @onlyworlds/sdk` — typed client, all 22 types | TypeScript tools |
| **LLM guide** | A single document that teaches any assistant the full schema + API — proven to one-shot working tools | Non-Claude assistants, GPTs |

## Patterns that work

- **Agent with a world**: connect the MCP server; the agent queries typed elements instead of guessing from context. `update` is server-side read-merge — safe partial writes by construction.
- **World as RAG corpus**: the folder IS a clean, typed, chunked corpus — one JSON file per entity, relationships explicit. No preprocessing needed.
- **AI writes, humans curate**: agents create elements via `/bulk` (mint your own UUIDs — any RFC-4122, v7 preferred for index locality; links can reference siblings in the same batch); humans review in Atlas.
- **Game/sim state**: characters, factions, locations, and their relations as the NPC knowledge base — the app reads typed truth, the LLM voices it. Proven live (a running app uses an OW world as its backend).
- **Custom machine data**: prefix fields with `x_` and they round-trip verbatim through the API and the folder — your tool's config rides the world without schema changes.

## Rules of the road

- Every world has a wall: key (+ PIN for writes). Read keys physically cannot write.
- Be a good citizen of shared worlds: read before you patch (or use MCP's update tool, which does it for you); never delete without a human.
- Foreign extension namespaces (`atlas_*`, `shadow_*`) are read-only to you; yours is `x_*`.
