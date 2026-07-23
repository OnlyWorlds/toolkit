---
name: onlyworlds-dev
description: Build tools, games, or applications using OnlyWorlds world data. Use when the user wants to set up a project with the OnlyWorlds SDK (npm install @onlyworlds/sdk), scaffold a React/web app, fetch and display world data, or integrate OnlyWorlds as a headless backend. Covers SDK setup, credential handling, and deployment patterns.
---

# OnlyWorlds Tool Development

Build applications on OnlyWorlds data.

## Quick Reference

| Task | Approach |
|------|----------|
| Install SDK | `npm install @onlyworlds/sdk` |
| Quick scaffold | See knowledge/scaffold.md |
| Deployment | See knowledge/deployment.md |
| Personal tool | Hardcode credentials, run locally |
| Shared tool | User-provided credentials, deploy to Cloudflare/Vercel |
| Python/Node script | Direct API calls with curl or requests |

## Instructions

### Step 1: Understand the Goal

What is the user building?

- **Visualization**: Display world data (maps, graphs, timelines) → read-only SDK calls
- **Editor**: Create/modify elements → full CRUD SDK calls
- **Game**: Use world data as content → read + local state
- **Integration**: Connect OW to other systems → API patterns

### Step 2: Load Core Reference

Read for OnlyWorlds overview, URLs, SDK basics:

**../../knowledge/onlyworlds-core.md**

### Step 3: SDK Setup

```bash
npm install @onlyworlds/sdk
```

The SDK (3.x) is v2-native: `OwV2Client`, with types and constants generated from the canonical schema.

```typescript
import { OwV2Client } from '@onlyworlds/sdk';

const client = new OwV2Client({
  apiKey: 'ow_w_your_world_key', // ow_w_ write / ow_r_ read / 10-digit legacy
  apiPin: 'your-pin'             // needed for writes on a PIN-protected world
});

const characters = await client.list('character');        // {data, has_more, next_cursor}
const one = await client.get('character', 'uuid-here');
```

The SDK also exports the canonical element palette and metadata: `elementColor(type, mode)`, `ELEMENT_FAMILIES`, `ELEMENT_ICONS` — generated from the schema, so tools that use them stay in sync for free.

### Common Operations

```typescript
// World meta (the container)
const world = await client.getWorld();

// Walk a whole type without touching cursors
for await (const el of client.listAll('character')) { /* ... */ }

// Create / patch / delete — type as the first argument
const made = await client.create('location', { name: 'Feltropolis', description: 'Capital city of Moppetopia' });
await client.patch('character', 'uuid-here', { description: 'Updated' });
await client.delete('character', 'uuid-here');

// Sync + atomic bulk
const changed = await client.changes({ since: cursor });
await client.bulk(items, { atomic: true });
```

*(A legacy v1 resource-style client, `OnlyWorldsClient`, stays exported for pre-3.x code — new tools should not use it.)*

### Link Field Patterns

**Write link fields under their bare names** — single links as a UUID string, multi links as a UUID array. Same names on read and write; no suffixes, in the SDK and raw v2 HTTP alike.

```typescript
// Single link — bare name, UUID string
await client.create('character', {
  name: 'Admiral Fluffington',
  birthplace: 'location-uuid'
});

// Multi link — bare name, UUID array
await client.create('character', {
  name: 'Admiral Fluffington',
  species: ['species-uuid-1', 'species-uuid-2']
});

// Pin coordinates must be integers
// (element_type/element_id are literal Pin schema fields, not link suffixes)
const pin = await client.create('pin', {
  map: 'map-uuid',
  element_type: 'character',
  element_id: 'character-uuid',
  x: Math.round(450),
  y: Math.round(720),
  z: 0
});
```

### Step 4: Credential Handling

**Personal tools**: Environment variables

```
# .env.local (gitignored)
VITE_ONLYWORLDS_API_KEY=your-key
VITE_ONLYWORLDS_API_PIN=your-pin
```

```typescript
const client = new OwV2Client({
  apiKey: import.meta.env.VITE_ONLYWORLDS_API_KEY,
  apiPin: import.meta.env.VITE_ONLYWORLDS_API_PIN
});
```

**Shared tools**: User provides credentials

```typescript
const apiKey = localStorage.getItem('ow_api_key') || prompt('API Key:');
const apiPin = localStorage.getItem('ow_api_pin') || prompt('API PIN:');
```

**PIN security**: The API-Pin grants write access. For personal tools, env vars are fine. For shared/public tools, never commit the PIN.

### Step 5: Local Development

**Plain HTML + JS** (simplest):
```html
<script type="module">
  import { OwV2Client } from 'https://esm.sh/@onlyworlds/sdk';
  const client = new OwV2Client({ apiKey: 'key', apiPin: 'pin' });
  const chars = await client.list('character');
  console.log(chars.data);
</script>
```

**Python script**:
```python
import requests
headers = {"API-Key": "key", "API-Pin": "pin"}
resp = requests.get("https://www.onlyworlds.com/api/v2/character?limit=100", headers=headers).json()
chars = resp["data"]  # v2 lists are enveloped: {data, has_more, next_cursor}
```

**Vite dev server** (for complex tools):
```bash
npm create vite@latest my-tool
cd my-tool && npm install @onlyworlds/sdk && npm run dev
```

### Step 6: Deployment

For deployment patterns, see **knowledge/deployment.md**.

Quick version: push to GitHub → connect to Cloudflare Pages → build command `npm run build` → output `dist` → set env vars → deploy.

### Step 7: Full Scaffold

For a complete project structure ready to run, see **knowledge/scaffold.md**.

## Common Patterns

### Read-Only Visualization

```typescript
const [characters, locations, events] = await Promise.all([
  client.list('character'),
  client.list('location'),
  client.list('event')
]);
renderTimeline(events.data);
renderMap(locations.data);
```

### Editor with Save

```typescript
const character = await client.get('character', id);
// User edits in UI...
await client.patch('character', id, { description: editedDescription });
```

### Game Using World Data

```typescript
const locations = await client.list('location');
const gameWorld = {
  rooms: locations.data.map(loc => ({
    id: loc.id, name: loc.name, description: loc.description
  }))
};
```

## Resources

- **API docs**: https://www.onlyworlds.com/api/docs
- **Ecosystem map** (all surfaces + how they wire): `knowledge/ecosystem.md`
- **Documentation**: https://onlyworlds.github.io
- **Discord**: https://discord.gg/twCjqvVBwb
- **SDK types**: Check @onlyworlds/sdk for full field definitions
