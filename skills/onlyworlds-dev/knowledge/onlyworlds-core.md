# OnlyWorlds Core Reference

What OnlyWorlds is, where a world lives, and where each detail is kept. The rules every skill follows are in `principles.md`.

---

## What OnlyWorlds Is

OnlyWorlds is an open standard for worldbuilding data. 22 element types with defined fields and relationships. Structured format that enables computational use across tools and platforms.

**Not a product. A protocol.** Tools built on OnlyWorlds can exchange data freely. No vendor lock-in.

---

## Where a World Lives

The same data, in one of two homes:

- **A world folder on disk**: `world.json` plus one JSON file per element. No account, no credentials, no network. Atlas stores worlds this way, and every toolkit skill that reads a world can read a folder. Layout and rules: `world-folder.md`.
- **An account world on onlyworlds.com**, reached through the REST API, the SDK, or the MCP server. It adds hosting, sync, and sharing.

Start with a folder unless the user needs what an account adds (principles §1). An account world can be exported to a folder, and a folder can be taken online (`world-folder.md`).

## The Four Stages

| Stage | Skills |
|---|---|
| Structure it | parsing, modeling, schema |
| Grow it | survey, link |
| Play in it and keep it true | context, resolve |
| Build on it | api, dev, council, project-setup |

---

## The 22 Element Types

Character, Creature, Species, Family, Collective, Institution, Location, Object, Construct, Ability, Trait, Title, Language, Law, Event, Narrative, Phenomenon, Relation, Map, Pin, Marker, Zone

Each type has its own fields, from many (Character) to few (Pin). See schema-reference.md for complete field lists.

**Base fields** (all elements): name, description, supertype, subtype, image_url

**Relationships**: Single-link (one reference) and multi-link (array of references)

---

## URLs

| Resource | URL |
|----------|-----|
| Main site | https://www.onlyworlds.com |
| Atlas (flagship app) | https://atlas.onlyworlds.com |
| Documentation | https://onlyworlds.github.io |
| API docs | https://www.onlyworlds.com/api/docs |
| Discord | https://discord.gg/twCjqvVBwb |
| GitHub (schema) | https://github.com/OnlyWorlds/OnlyWorlds |
| Feedback page | https://www.onlyworlds.com/feedback |

For the full surface map (Atlas, show pages, Obsidian plugin, MCP, portal, and how they wire together), see `ecosystem.md`.

---

## The API in Brief

- **Base URL** `https://www.onlyworlds.com/api/v2/` (always `www.`). Endpoints are singular: `/api/v2/character`, `/api/v2/character/{uuid}`.
- **Headers** `API-Key` and `API-Pin`, spelled exactly. A key is scoped to one world: a prefixed key (`ow_w_…` write, `ow_r_…` read) or a legacy 10-digit key. The PIN is required on writes; prefixed keys read without it. Keys: Account → your world → API keys. PIN: the owner writes with their account PIN (Account → Settings → World PIN: one PIN for every world they own). A member of someone else's world writes with their own account PIN. An agent seat writes with its own seat secret (`ow_s_…`), from its invite link or made in one step: **make a seat** under Invite an agent on the owner's world page, or under **Your AI in this world** on a member's; the `.env` lines show once, and a lost key is **new key** beside the seat.
- **Shapes**: lists are paginated (`{data, has_more, next_cursor}`); link fields are flat UUID arrays under bare names; `/api/v2/bulk` uploads many elements at once; `/api/v2/changes` is the sync feed.
- **The world's now**: `time_range_current` on the API, `time_current` in a folder's `world.json`.

Everything else (every route, bulk and its replace semantics, sync, errors, account tokens, the older v1 dialect) is in the api skill: `../../onlyworlds-api/SKILL.md`.

## SDK

```bash
npm install @onlyworlds/sdk
```

Version 4.x is ESM-only and v2-only; the client is `OwV2Client`. Setup, the common calls, and link-field patterns are in the dev skill: `../../onlyworlds-dev/SKILL.md`.

---

## MCP Server

OnlyWorlds runs an MCP server at **`https://www.onlyworlds.com/mcp`**: modern MCP over streamable HTTP, stateless. It exposes your world to any MCP client (Claude Code, Claude Desktop, the API connector) as a set of tools. It is listed in the MCP Registry as `com.onlyworlds/mcp`.

**Connect from Claude Code:**
```bash
claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp \
  --header "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}" --header "API-Pin: ${OW_API_PIN:-$ONLYWORLDS_API_PIN}"
```
Load `.env` into the shell first; the shell fills in the values, so the key is never typed into the command. The PIN is needed for writes; prefixed keys read without it. Only a legacy 10-digit key reading a private world needs it for reads.

**11 tools:**
- **Schema (3, no key required):** `list_element_types`, `get_element_schema`, `search_schema`. Public reference; they work without credentials.
- **Read (4):** `list_elements`, `get_element`, `search_elements`, `get_changes` (paged: default 25, max 1000 per call; walk the cursor for a full export).
- **Write (4):** `create_element`, `update_element` (server-side read-merge: only the fields you pass change), `edit_links` (additive/subtractive link edits), `bulk_apply`.

There is **no delete tool** by design: deletion stays on the REST API and the web portal.

The claude.ai **web** connector is not supported yet (its UI is OAuth-only; OAuth support is planned); header-based keys work in Claude Code, Claude Desktop, and the API connector. The old `@onlyworlds/mcp-client` npm package and `/mcp/messages/` endpoint are legacy; the old endpoint now answers with a pointer to this one.

---

## Building a Tool

A common shape: a static frontend (TypeScript, React, plain JS) that calls the API directly, with no backend, deployed to a static host. Other architectures (Node backends, Unity, Python) work too, and a local tool can read a world folder with no API at all.

Browser calls are subject to CORS. The API accepts them from common static hosts (`*.pages.dev`, `*.netlify.app`, `*.vercel.app`, `*.github.io` and others) and from localhost on any port. A **custom domain is not pre-approved**: browser calls from it are refused until it is added server-side, which you can request at https://www.onlyworlds.com/feedback. The full host list and deploy steps are in `../../onlyworlds-dev/knowledge/deployment.md`.

Credentials: keys and PINs load from a gitignored `.env`, never printed or committed, and a PIN never goes into a browser build (principles §6).

---

## Key Constraints

**Custom data goes in extension fields** (`x_<tool>_...`); unprefixed unknown fields are rejected. The rule is principles §4; how the API stores them is in `schema-reference.md`.

**IDs are UUIDs.** Any RFC-4122 UUID works; v7 is recommended when you mint your own, and ids the server assigns are v7. Minting ids before a `/bulk` upload lets links point at siblings in the same batch and makes retries safe.

---

## Getting Help

- **Documentation**: onlyworlds.github.io
- **Discord**: Community support and discussion
- **API docs**: OpenAPI specification at /api/docs
- **Bugs & feature requests**: onlyworlds.com/feedback (submissions land on the public tracker, github.com/OnlyWorlds/feedback)

---

*This is a lightweight reference. For full schema details, see schema-reference.md. For modeling guidance, see modeling-patterns.md.*
