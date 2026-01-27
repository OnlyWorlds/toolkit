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
| Documentation | https://onlyworlds.github.io |
| API docs | https://onlyworlds.com/api/docs |
| Discord | https://discord.gg/twCjqvVBwb |
| GitHub (schema) | https://github.com/OnlyWorlds/OnlyWorlds |

---

## API Basics

**Base URL**: `https://www.onlyworlds.com/api/worldapi/`

**Authentication**: Two headers required
- `API-Key`: World-specific key (from world settings)
- `API-Pin`: User's personal PIN (from profile)

**Pattern**:
```
GET/POST     /api/worldapi/{element_type}/
GET/PUT/DELETE /api/worldapi/{element_type}/{uuid}/
```

**Element types in URL** (lowercase): character, creature, species, location, object, etc.

**Getting credentials**:
1. Sign in at onlyworlds.com
2. Go to Profile for your PIN
3. Go to World Settings for the API Key

Each API key is scoped to one world.

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

- `.list()` returns `{ count, next, previous, results: [...] }` (paginated)
- `.get(id)` returns the element directly (not wrapped)
- `.create(data)` returns the created element directly

### Link Fields

When creating/updating elements with relationships:
- Single links use `_id` suffix: `birthplace_id: 'uuid'`
- Multi links use `_ids` suffix: `species_ids: ['uuid1', 'uuid2']`

---

## MCP Server

For AI assistants with MCP support (Claude Desktop, VSCode, etc.):

```bash
npm install @onlyworlds/mcp-client
```

Provides schema lookups and API operations as MCP tools.

---

## Common Patterns

### Static Frontend + OW API

A common pattern for OnlyWorlds tools:
1. Static frontend (TypeScript, React, vanilla JS)
2. Calls OnlyWorlds API directly
3. No backend needed
4. Deploy to Cloudflare Pages, Vercel, or similar

CORS is pre-configured for `*.pages.dev` domains.

Other architectures work too (Node backends, Unity, Python, etc.) - this is just a lightweight starting point.

### Environment Variables

Store credentials in `.env`:
```
ONLYWORLDS_API_KEY=your-api-key
ONLYWORLDS_API_PIN=your-pin
```

Never commit credentials to version control.

### Bulk Operations

For importing/exporting entire worlds, use WorldSync endpoints:
- Export: `POST /api/worldsync/send/` (body auth)
- Import: `POST /api/worldsync/store/` (body auth)

These use body authentication instead of headers.

---

## Key Constraints

**API accepts schema fields only.** The 22 element types have defined fields. Custom fields won't save via API.

**Local apps can extend.** Your application can add custom properties, wrap OW data, or use creative conventions. Just don't expect the API to store non-schema fields.

**IDs are UUIDv7.** Time-sortable. Don't generate your own for API uploads. Let the API assign IDs, or use Base Tool which handles this.

---

## Getting Help

- **Documentation**: onlyworlds.github.io
- **Discord**: Community support and discussion
- **API docs**: OpenAPI specification at /api/docs

---

*This is a lightweight reference. For full schema details, see schema-reference.md. For modeling guidance, see modeling-patterns.md.*
