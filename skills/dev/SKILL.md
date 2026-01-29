---
name: onlyworlds-dev
description: Build tools and games on OnlyWorlds data. Use when user wants to create visualizations, editors, games, or any application using world data. Covers SDK setup (npm install @onlyworlds/sdk), project scaffolding, credential handling, and deployment. OnlyWorlds works as a headless backend - world data lives in the cloud, your app just fetches and renders.
---

# OnlyWorlds Tool Development

Build applications on OnlyWorlds. SDK patterns, project setup, deployment.

## When to Use This

User wants to BUILD something with OnlyWorlds:

- "How do I use the OnlyWorlds SDK?"
- "I want to build a faction tracker"
- "How do I deploy to Cloudflare Pages?"
- "How do I set up API credentials in my app?"

For modeling/design questions (how to structure data), the modeling skill handles that.

## Instructions

### Step 1: Understand the Goal

What is the user building?

- **Visualization tool**: Display world data (maps, graphs, timelines)
- **Editor tool**: Create/modify world elements
- **Game**: Use world data as game content
- **Integration**: Connect OnlyWorlds to other systems

This shapes the architecture and which SDK features matter.

### Step 2: Load Core Reference

For OnlyWorlds overview, URLs, and SDK basics:

**../../knowledge/onlyworlds-core.md**

Contains:
- What OnlyWorlds is
- The 22 element types
- SDK quick start
- API basics
- MCP server mention

### Step 3: SDK Setup

#### Installation

```bash
npm install @onlyworlds/sdk
```

#### Basic Client

```typescript
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: 'your-api-key',  // from world settings
  apiPin: 'your-api-pin'   // from user profile
});
```

#### Common Operations

```typescript
// List all characters in the world
const characters = await client.characters.list();

// Get specific element
const character = await client.characters.get('uuid-here');

// Create new element
const location = await client.locations.create({
  name: 'Feltropolis',
  description: 'Capital city of Moppetopia',
  supertype: 'City',
  subtype: 'Capital'
});

// Update element
await client.characters.update('uuid-here', {
  description: 'Updated description'
});

// Delete element
await client.characters.delete('uuid-here');
```

#### All Collections

`client.characters`, `client.locations`, `client.objects`, `client.constructs`, `client.abilities`, `client.traits`, `client.events`, `client.narratives`, etc.

Each has: `.list()`, `.get(id)`, `.create(data)`, `.update(id, data)`, `.delete(id)`

#### Link Field Patterns

When creating/updating with relationships:

```typescript
// Single link - use _id suffix
await client.characters.create({
  name: 'Admiral Fluffington',
  birthplace_id: 'location-uuid-here'  // single link
});

// Multi link - use _ids suffix
await client.characters.create({
  name: 'Admiral Fluffington',
  species_ids: ['species-uuid-1', 'species-uuid-2']  // multi link
});

// Pin creation - placing an element on a map
// Note: Coordinates must be integers - use Math.round() for calculated values
const pin = await client.pins.create({
  map_id: 'map-uuid',
  element_type: 'character',
  element_id: 'character-uuid',
  x: Math.round(450),
  y: Math.round(720),
  z: 0
});

// Marker creation - defining zone boundaries
// Connect markers in order to draw the zone polygon
const markers = await Promise.all([
  client.markers.create({ map_id: 'map-uuid', zone_id: 'zone-uuid', x: 100, y: 100, order: 1 }),
  client.markers.create({ map_id: 'map-uuid', zone_id: 'zone-uuid', x: 200, y: 100, order: 2 }),
  client.markers.create({ map_id: 'map-uuid', zone_id: 'zone-uuid', x: 200, y: 200, order: 3 }),
  client.markers.create({ map_id: 'map-uuid', zone_id: 'zone-uuid', x: 100, y: 200, order: 4 }),
]);
```

### Step 4: Project Architecture

A common pattern: static frontend calling the OnlyWorlds API directly.

```
┌─────────────────┐     ┌─────────────────┐
│  Your Tool      │────▶│  OnlyWorlds API │
│  (static site)  │◀────│  (hosted)       │
└─────────────────┘     └─────────────────┘
```

**No backend needed** for this pattern. Your code runs locally or in browser, calls OnlyWorlds API directly. Good for visualizations, editors, simple games.

Other architectures work too: Node.js backends, Unity games, Python scripts, whatever fits your use case.

#### Minimal Project Structure

```
my-ow-tool/
├── src/
│   ├── main.ts
│   └── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.local          # credentials (gitignored)
```

#### package.json

```json
{
  "name": "my-ow-tool",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "@onlyworlds/sdk": "latest"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Step 5: Credential Handling

**For personal tools**: Environment variables

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

**For shared tools**: User provides credentials

```typescript
const apiKey = localStorage.getItem('ow_api_key') || prompt('API Key:');
const apiPin = localStorage.getItem('ow_api_pin') || prompt('API PIN:');
```

### Step 6: Local Development (Personal Tools)

Not everything needs deployment. For personal vibe coding, local scripts, or tools just for yourself:

**Plain HTML + JS**
```html
<!-- index.html - open directly in browser -->
<script type="module">
  // Option 1: esm.sh (usually works)
  import { OnlyWorldsClient } from 'https://esm.sh/@onlyworlds/sdk';

  // Option 2: unpkg (if esm.sh has issues)
  // import { OnlyWorldsClient } from 'https://unpkg.com/@onlyworlds/sdk/dist/index.esm.js';

  const client = new OnlyWorldsClient({
    apiKey: 'your-key',
    apiPin: 'your-pin'
  });

  const chars = await client.characters.list();
  console.log(chars);
</script>
```

Note: ESM imports require modern browser and internet connection.

**Python script**
```python
import requests

API_KEY = "your-key"
API_PIN = "your-pin"
BASE = "https://www.onlyworlds.com/api/worldapi"

headers = {"API-Key": API_KEY, "API-Pin": API_PIN}

# List characters
chars = requests.get(f"{BASE}/character/", headers=headers).json()

# Create something
requests.post(f"{BASE}/location/", headers=headers, json={
    "name": "My Location",
    "description": "Created from Python"
})
```

**Node.js script**
```javascript
// script.js - run with: node script.js
// Note: Requires "type": "module" in package.json, or rename to script.mjs
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: process.env.OW_API_KEY,
  apiPin: process.env.OW_API_PIN
});

const locations = await client.locations.list();
console.log(locations);
```

**Local dev server** (for more complex tools)
```bash
npm create vite@latest my-tool
cd my-tool
npm install @onlyworlds/sdk
npm run dev  # runs on localhost:5173
```

For personal tools, hardcoding credentials is fine. Just don't commit them if you ever push to GitHub.

### Step 7: Deployment (If Sharing)

For detailed deployment patterns:

**knowledge/deployment.md**

Covers:
- Cloudflare Pages (recommended, free)
- Vercel (alternative)
- GitHub Pages (alternative)
- Environment variables in hosting
- CORS notes

Quick version:
1. Push to GitHub
2. Connect to Cloudflare Pages
3. Build command: `npm run build`
4. Output: `dist`
5. Set environment variables
6. Deploy

## Common Tool Patterns

### Read-Only Visualization

```typescript
// Fetch all data on load
const [characters, locations, events] = await Promise.all([
  client.characters.list(),
  client.locations.list(),
  client.events.list()
]);

// Render visualization
renderTimeline(events);
renderMap(locations);
renderGraph(characters);
```

### Editor with Save

```typescript
// Load element
const character = await client.characters.get(id);

// User edits in UI...

// Save changes
await client.characters.update(id, {
  description: editedDescription,
  physicality: editedPhysicality
});
```

### Game Using World Data

```typescript
// Load world as game content
const locations = await client.locations.list();
const characters = await client.characters.list();
const items = await client.objects.list();

// Build game state from OW data
const gameWorld = {
  rooms: locations.map(loc => ({
    id: loc.id,
    name: loc.name,
    description: loc.description,
    // ... game-specific properties
  })),
  npcs: characters.filter(c => c.supertype === 'NPC'),
  inventory: items.filter(i => i.supertype === 'Collectible')
};
```

### Integration with Other Systems

```typescript
// Export to another format
const world = await client.worlds.get();
const allData = await exportWorld(); // bulk export

// Transform to target format
const otherFormat = transformToOtherFormat(allData);
```

## Bulk Operations

For importing/exporting entire worlds:

```typescript
// Export whole world (WorldSync uses body auth, not SDK)
const response = await fetch('https://www.onlyworlds.com/api/worldsync/send/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ pin: apiPin, api_key: apiKey })
});
const worldData = await response.json();

// Import data
await fetch('https://www.onlyworlds.com/api/worldsync/store/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    pin: apiPin,
    api_key: apiKey,
    Character: [...],
    Location: [...]
  })
});
```

Note: WorldSync uses body auth, not headers.

## MCP Integration

For AI assistants with MCP support:

```bash
npm install @onlyworlds/mcp-client
```

Provides OnlyWorlds operations as MCP tools. Useful if building AI-powered OnlyWorlds tools.

## Quick Start Scaffold

When user wants instant project setup, generate this complete structure:

```bash
mkdir my-ow-tool && cd my-ow-tool
npm init -y
npm install @onlyworlds/sdk
npm install -D vite typescript
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src"]
}
```

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite';
export default defineConfig({
  server: { port: 3000 }
});
```

**src/main.ts**:
```typescript
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: prompt('API Key:') || '',
  apiPin: prompt('API PIN:') || ''
});

async function main() {
  const world = await client.worlds.get();
  document.body.innerHTML = `<h1>Connected to: ${world.name}</h1>`;

  const characters = await client.characters.list();
  console.log('Characters:', characters.results);
}

main();
```

**index.html**:
```html
<!DOCTYPE html>
<html>
<head>
  <title>My OnlyWorlds Tool</title>
  <style>body { font-family: sans-serif; padding: 2rem; }</style>
</head>
<body>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

Run with `npx vite` - building on OnlyWorlds data in under a minute.

## Getting Help

- **API docs**: https://onlyworlds.com/api/docs
- **Documentation**: https://onlyworlds.github.io
- **Discord**: https://discord.gg/twCjqvVBwb
- **SDK source**: Check @onlyworlds/sdk types for full field definitions

---

*For data modeling questions, use the modeling skill. For API operations in current session, use the api skill.*
