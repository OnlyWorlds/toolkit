# OnlyWorlds Core Reference

Quick reference for OnlyWorlds integration. Overview, URLs, SDK patterns, credentials.

---

## What OnlyWorlds Is

OnlyWorlds is an open standard for worldbuilding data. 22 element types with defined fields and relationships. Structured format that enables computational use across tools and platforms.

**Not a product. A protocol.** Tools built on OnlyWorlds can exchange data freely. No vendor lock-in.

---

## The 22 Element Types

Character, Creature, Species, Family, Collective, Institution, Location, Object, Construct, Ability, Trait, Title, Language, Law, Event, Narrative, Phenomenon, Relation, Map, Pin, Marker, Zone

Each type has specific fields. Some have many (Character has 42), some have few (Pin has 6). See schema-reference.md for complete field lists.

**Base fields** (all elements): name, description, supertype, subtype

**Relationships**: Single-link (one reference) and multi-link (array of references)
 
---

## URLs

| Resource | URL |
|----------|-----|
| Main site | https://onlyworlds.com |
| Atlas (flagship app) | https://atlas.onlyworlds.com |
| Documentation | https://onlyworlds.github.io |
| API docs | https://www.onlyworlds.com/api/docs |
| Discord | https://discord.gg/twCjqvVBwb |
| GitHub (schema) | https://github.com/OnlyWorlds/OnlyWorlds |
| Feedback tracker | https://github.com/OnlyWorlds/feedback |

For the full surface map (Atlas, show pages, Obsidian plugin, MCP, portal — and how they wire together), see `ecosystem.md`.

---

## API Basics

**Base URL** (modern v2 dialect): `https://www.onlyworlds.com/api/v2/`

**Authentication**:
- `API-Key`: World-scoped key. May be a prefixed key (`ow_w_…` world-write, `ow_r_…` read-share) or a legacy 10-digit key (still valid forever, no longer issued). From world settings.
- `API-Pin`: The world's PIN. Required on every **write**. Reads: prefixed keys (`ow_r_`/`ow_w_`) always read PIN-less; only a legacy 10-digit write key on a private world needs the PIN for reads. Unwalled/demo worlds read with any key alone.

**Pattern** (v2 — singular type names, envelope + flat UUID links):
```
GET/POST         /api/v2/{element_type}
GET/PATCH/DELETE /api/v2/{element_type}/{uuid}
PUT              /api/v2/{element_type}/{uuid}   # upsert: 201 created / 200 replaced
POST             /api/v2/bulk        # batch upsert (standard upload path)
GET              /api/v2/changes     # incremental sync cursor
```

PUT is the upsert -- and the answer to a 409 `id_conflict` when you mint your own UUIDs: PUT the same id to create-or-replace deterministically.

v2 list responses are enveloped and paginated (`{data, has_more, next_cursor}`); link fields are flat UUID arrays with bare names (no `_ids` suffix). The older `/api/worldapi/…` (v1) dialect still serves for legacy tools — see the `onlyworlds-api` skill's Classic API section.

**Element types in URL** (lowercase, singular): character, creature, species, location, object, etc.

**Getting credentials**:
1. Sign in at onlyworlds.com
2. Go to Profile for your PIN
3. Go to World Settings for the API Key

Each API key is scoped to one world.

**World meta is writable**: `PATCH /api/v2/world` updates the world's own fields (description, image_url, time settings) with the same key+PIN. Partial — send only what changes; an unknown field rejects the whole PATCH.

**Account tokens** (`ow_a_…`): minted in the portal under Settings → Account, sent as a `Authorization: Bearer` header on `/api/v2/account/…` routes. They operate at account level — list your worlds, create new worlds, mint fresh world keys programmatically. Tokens are shown once at mint; a token can't re-view existing keys, but it can always mint new ones. Only needed for multi-world/account automation — normal world work uses the world key.

---

## SDK Quick Start

### Installation

```bash
npm install @onlyworlds/sdk
```

### Basic Usage

```typescript
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: 'your-api-key',
  apiPin: 'your-api-pin'
});

// List characters
const characters = await client.characters.list();

// Create a location
const location = await client.locations.create({
  name: 'Feltropolis',
  description: 'Capital city of Moppetopia'
});

// Get specific element
const character = await client.characters.get('uuid-here');

// Update element
await client.characters.update('uuid-here', {
  description: 'Updated description'
});

// Delete element
await client.characters.delete('uuid-here');
```

### Available Collections

All 22 element types: `client.characters`, `client.creatures`, `client.species`, `client.families`, `client.collectives`, `client.institutions`, `client.locations`, `client.objects`, `client.constructs`, `client.abilities`, `client.traits`, `client.titles`, `client.languages`, `client.laws`, `client.events`, `client.narratives`, `client.phenomena`, `client.relations`, `client.maps`, `client.pins`, `client.markers`, `client.zones`

Each collection has: `.list()`, `.get(id)`, `.create(data)`, `.update(id, data)`, `.delete(id)`

**World** (special): `client.worlds.get()` returns the world for your API key. World is the container, not one of the 22 element types.

### Response Formats

- `.list(options)` returns a paginated wrapper `{ count, results, next, previous }` — `results` is the element array, `next`/`previous` are page URLs. `.get(id)` returns the element directly; `.create(data)` returns the created element directly.

**Dialect note:** the SDK (2.2.x) currently targets the classic **v1** dialect — its default base URL is `https://www.onlyworlds.com/api/worldapi`, and its list wrapper is the v1 `{count, results, next, previous}` shape (not v2's `{data, has_more, next_cursor}`). If you want the v2 surface, call the raw HTTP API directly (a v2 list GET returns `{ data: [...], has_more, next_cursor }` — follow `next_cursor` until `has_more` is false; a singular GET returns the bare element object), or check the SDK changelog for a v2 release.

### Link Fields (SDK)

The SDK accepts link fields under their **bare** relationship names — single links as `birthplace: 'uuid'`, multi links as `species: ['uuid1', 'uuid2']` — and converts them to the v1 wire format (`birthplace_id`, `species_ids`) for you. You write bare names; the SDK adds the suffix.

If you call the raw HTTP API instead of the SDK, the wire format depends on the dialect: **v2** uses bare field names holding UUID arrays with no suffix (`birthplace`, `species`); **v1** uses the `_id`/`_ids` suffix on writes. See the `onlyworlds-api` skill for both.

---

## MCP Server

OnlyWorlds runs an MCP server at **`https://www.onlyworlds.com/mcp`** — modern MCP over streamable HTTP, stateless. It exposes your world to any MCP client (Claude Code, Claude Desktop, the API connector) as a set of tools.

**Connect from Claude Code:**
```bash
claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp \
  --header "API-Key: <your key>" --header "API-Pin: <your pin>"
```
The PIN is needed for writes and for reads on a walled world; a read-only key on an unwalled world needs no PIN.

**11 tools:**
- **Schema (3, no key required):** `list_element_types`, `get_element_schema`, `search_schema` — public reference, work without credentials.
- **Read (4):** `list_elements`, `get_element`, `search_elements`, `get_changes` (paged: default 25, max 1000 per call — cursor-walk for a full export).
- **Write (4):** `create_element`, `update_element` (server-side read-merge — only the fields you pass change), `edit_links` (additive/subtractive link edits), `bulk_apply`.

There is **no delete tool** by design — deletion stays on the REST API and the web portal.

The claude.ai **web** connector is not supported yet (its UI is OAuth-only; OAuth support is planned); header-based keys work in Claude Code, Claude Desktop, and the API connector. The old `@onlyworlds/mcp-client` npm package and `/mcp/messages/` endpoint are legacy — the old endpoint now answers with a pointer to this one.

---

## Common Patterns

### Static Frontend + OW API

A common pattern for OnlyWorlds tools:
1. Static frontend (TypeScript, React, vanilla JS)
2. Calls OnlyWorlds API directly
3. No backend needed
4. Deploy to Cloudflare Pages, Vercel, or similar

Browser apps call the API directly. CORS is deliberately community-tool friendly: mainstream static hosts are pre-granted by wildcard (`*.pages.dev`, `*.netlify.app`, `*.vercel.app`, `*.github.io`, `*.gitlab.io`, `*.surge.sh`, `*.onrender.com`, `*.up.railway.app`) plus `localhost` on any port — deploy there and it just works. A **custom domain** needs its grant added server-side: open an issue on the repo or ask on Discord.

Other architectures work too (Node backends, Unity, Python, etc.) - this is just a lightweight starting point.

### Environment Variables

Store credentials in `.env`:
```
ONLYWORLDS_API_KEY=your-api-key
ONLYWORLDS_API_PIN=your-pin
```

Never commit credentials to version control.

### Fetching Multiple Elements

To fetch elements of a type (v2, paginated):
```
GET /api/v2/{element_type}?limit=100
```

Returns `{data, has_more, next_cursor}`. Follow `next_cursor` until `has_more` is false to page through all elements. Use this to build caches or display full lists.

---

## Key Constraints

**API accepts schema fields plus namespaced extensions.** The 22 element types have defined fields; unprefixed unknown fields 422. Fields prefixed `x_`/`atlas_`/`shadow_` DO save -- stored verbatim server-side and returned top-level on read. Your custom data goes in `x_*`; foreign namespaces are read-only to you.

**Local apps can extend.** Your application can add custom properties, wrap OW data, or use creative conventions. Just don't expect the API to store non-schema fields.

**IDs are UUIDv7.** Time-sortable. On v2 you can (and for `/bulk` should) mint your own UUIDv7 per element before upload — this lets links point at siblings created in the same batch and makes retries idempotent. The API also assigns one if you omit it.

---

## Getting Help

- **Documentation**: onlyworlds.github.io
- **Discord**: Community support and discussion
- **API docs**: OpenAPI specification at /api/docs
- **Bugs & feature requests**: github.com/OnlyWorlds/feedback — public tracker, all tools

---

*This is a lightweight reference. For full schema details, see schema-reference.md. For modeling guidance, see modeling-patterns.md.*
