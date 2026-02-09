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

```typescript
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: 'your-api-key',  // from world settings
  apiPin: 'your-api-pin'   // from user profile
});
```

### Common Operations

```typescript
// List all characters
const characters = await client.characters.list();

// Get specific element
const character = await client.characters.get('uuid-here');

// Create element
const location = await client.locations.create({
  name: 'Feltropolis',
  description: 'Capital city of Moppetopia'
});

// Update element
await client.characters.update('uuid-here', { description: 'Updated' });

// Delete element
await client.characters.delete('uuid-here');
```

All collections: `client.characters`, `client.locations`, `client.objects`, `client.constructs`, `client.abilities`, `client.traits`, `client.events`, `client.narratives`, etc.

Each has: `.list()`, `.get(id)`, `.create(data)`, `.update(id, data)`, `.delete(id)`

### Link Field Patterns

```typescript
// Single link — use _id suffix
await client.characters.create({
  name: 'Admiral Fluffington',
  birthplace_id: 'location-uuid'
});

// Multi link — use _ids suffix
await client.characters.create({
  name: 'Admiral Fluffington',
  species_ids: ['species-uuid-1', 'species-uuid-2']
});

// Pin coordinates must be integers
const pin = await client.pins.create({
  map_id: 'map-uuid',
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
const client = new OnlyWorldsClient({
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
  import { OnlyWorldsClient } from 'https://esm.sh/@onlyworlds/sdk';
  const client = new OnlyWorldsClient({ apiKey: 'key', apiPin: 'pin' });
  const chars = await client.characters.list();
  console.log(chars);
</script>
```

**Python script**:
```python
import requests
headers = {"API-Key": "key", "API-Pin": "pin"}
chars = requests.get("https://www.onlyworlds.com/api/worldapi/character/", headers=headers).json()
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
  client.characters.list(),
  client.locations.list(),
  client.events.list()
]);
renderTimeline(events);
renderMap(locations);
```

### Editor with Save

```typescript
const character = await client.characters.get(id);
// User edits in UI...
await client.characters.update(id, { description: editedDescription });
```

### Game Using World Data

```typescript
const locations = await client.locations.list();
const gameWorld = {
  rooms: locations.map(loc => ({
    id: loc.id, name: loc.name, description: loc.description
  }))
};
```

## Resources

- **API docs**: https://onlyworlds.com/api/docs
- **Documentation**: https://onlyworlds.github.io
- **Discord**: https://discord.gg/twCjqvVBwb
- **SDK types**: Check @onlyworlds/sdk for full field definitions
