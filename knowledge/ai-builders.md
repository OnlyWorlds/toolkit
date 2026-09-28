# OnlyWorlds for AI Builders

OnlyWorlds is a typed, persistent, portable world-state layer an AI system can read and write. 22 element types, real relationships (UUID links between elements), a change-feed for sync, and an open format that lives equally well on disk (the world folder) or behind a REST API. Free and open source.

## The honest positioning

The agent-memory field (Zep, Mem0, MCP memory servers) keeps independently rediscovering that **typed schema beats freeform extraction**, and hand-rolls a bespoke entity schema per project, unshared and unportable. OnlyWorlds is the mature, shared instance of that insight: a schema refined against real worlds since 2012, with an ecosystem already speaking it.

Claim precisely:

| Defensible | Not our claim |
|---|---|
| Typed world-state with real relationships, portable across tools | A general agent-memory replacement |
| Open + exportable: no lock-in, speaks a shared vocabulary | Episodic memory, embeddings, auto-extraction |
| Working change-feed sync (`/changes` cursor) for multi-client state | "Solved" multi-agent memory or coordination |
| The graph slot in a hybrid memory stack: the pre-modeled domain layer | Retrieval-latency benchmarks (we don't do vector recall) |

Complement memory layers, don't compete with them: OW holds the MODELED world (who rules what, who knows whom, what exists where); episodic/vector layers hold conversation history. Game NPCs, DM copilots, simulation agents, and story systems need the first kind.

## The connect surfaces, fastest first

| Surface | One-liner | Best for |
|---|---|---|
| **MCP server** | `https://www.onlyworlds.com/mcp`: 11 tools (schema, read, write; no delete), listed in the MCP Registry as `com.onlyworlds/mcp`. Connect command: onlyworlds-core.md | Claude Code/Desktop agents, zero code |
| **World folder** | Read JSON files straight off disk (see world-folder.md) | Local pipelines, RAG corpora, zero network |
| **REST API v2** | `www.onlyworlds.com/api/v2/`: bare-name link fields, `/bulk` upload, `/changes` sync (the api skill) | Any language, production apps |
| **SDK** | `npm install @onlyworlds/sdk`: typed client, all 22 types (the dev skill) | TypeScript tools |
| **LLM guide** | https://onlyworlds.github.io/assets/ow_llm_guide.txt: a single document that teaches any assistant the full schema + API, proven to one-shot working tools | Non-Claude assistants, GPTs |

Start page for developers and AI builders: https://www.onlyworlds.com/develop

## Patterns that work

- **Agent with a world**: connect the MCP server; the agent queries typed elements instead of guessing from context. `update_element` is a server-side read-merge, so partial writes are safe.
- **World as RAG corpus**: the folder IS a clean, typed, chunked corpus: one JSON file per entity, relationships explicit. No preprocessing needed.
- **AI proposes, a human approves, one writer applies** (principles §2): the agent drafts a batch of elements with its own minted UUIDs (links can reference siblings in the same batch), a human rules on the list, and only the approved items go up via `/bulk`. Atlas is where people read the result back.
- **Game/sim state**: characters, factions, locations, and their relations as the NPC knowledge base; the app reads typed truth, the LLM voices it. Proven live (a running app uses an OW world as its backend).
- **Custom machine data**: your tool's own fields go in `x_<tool>_...` extension fields, which round-trip through the API and the folder (principles §4, `schema-reference.md`).

## Rules of the road

The shared rules are in `principles.md`, and API detail is in the api skill. The ones that matter most here:

- Every world has a wall: key (+ PIN for writes). Read keys cannot write. Keys load from `.env`; a PIN never goes into a build, a chat, or a log (§6).
- Propose, review, apply on shared worlds: read before you patch (MCP's update tool does it for you), let a human rule on changes, and retire rather than delete (§2).
- Write only your own `x_<tool>_*` namespace (§4).
