---
name: onlyworlds-dev
description: "Build a tool, game, app or AI agent on world data. Use when the user says 'npm install @onlyworlds/sdk', 'a React app on my world', 'connect an agent to my world', or wants OnlyWorlds as a backend."
---

# OnlyWorlds Tool Development

Build applications on OnlyWorlds data.

Shared rules (credentials, read before write, verify after write, extension fields) live in `knowledge/principles.md`; this skill applies them to building tools.

## Quick Reference

| Task | Approach |
|------|----------|
| Install SDK | `npm install @onlyworlds/sdk` |
| Quick scaffold | See knowledge/scaffold.md |
| Deployment | See knowledge/deployment.md |
| Personal tool (runs on your machine) | Credentials in a gitignored `.env`, read at runtime; never hardcoded |
| Shared or deployed tool | Read key (`ow_r_...`) for reading; the user enters key and PIN at runtime for writing. A PIN never goes into a build |
| Python/Node script | Direct API calls with curl or requests, credentials from `.env` |

## Instructions

### Step 1: Understand the Goal

What is the user building?

- **Visualization**: Display world data (maps, graphs, timelines) → read-only SDK calls
- **Editor**: Create/modify elements → full CRUD SDK calls
- **Game**: Use world data as content → read + local state
- **Integration**: Connect OW to other systems → API patterns (the api skill)
- **Local tool on a world folder** (pipelines, RAG, offline tools): read the files directly, no account or key → `knowledge/world-folder.md`
- **AI agent with a persistent world**: the MCP server or the API → `knowledge/ai-builders.md`

### Step 2: Load Core Reference

Read for the OnlyWorlds overview, URLs, and the MCP server:

**knowledge/onlyworlds-core.md**

### Step 3: SDK Setup

```bash
npm install @onlyworlds/sdk
```

The SDK (4.x, ESM-only) is v2-only: `OwV2Client`, with types and constants generated from the canonical schema.

```typescript
import { OwV2Client } from '@onlyworlds/sdk';

// Node: load .env first (e.g. `node --env-file=.env`, Node 20.6+); never hardcode keys
const client = new OwV2Client({
  apiKey: process.env.ONLYWORLDS_API_KEY!, // ow_w_ write / ow_r_ read / 10-digit legacy
  apiPin: process.env.ONLYWORLDS_API_PIN   // writes only; leave unset for a read-only tool
});

const page = await client.list('character');   // ONE page (100 by default): {data, has_more, next_cursor}
const one = await client.get('character', 'uuid-here');
```

The SDK also exports the canonical element palette and metadata: `elementColor(type, mode)`, `ELEMENT_FAMILIES`, `ELEMENT_ICONS`, generated from the schema, so tools that use them stay in sync for free.

### Common Operations

```typescript
// World meta (the container)
const world = await client.getWorld();

// Every element of a type: listAll walks the cursors (list() stops at one page)
for await (const el of client.listAll('character')) { /* ... */ }

// Create / patch / delete — type as the first argument
const made = await client.create('location', { name: 'Feltropolis', description: 'Orbital station, seven levels' });
await client.patch('character', 'uuid-here', { description: 'Updated' }); // replaces each field it sends
await client.delete('character', 'uuid-here');

// Add or remove multi-links: atomic server-side merge, no read needed
await client.editLinks('character', 'uuid-here', 'friends', { add: ['uuid-a'], remove: ['uuid-b'] });

// Sync + atomic bulk
const changed = await client.changes({ since: cursor });
await client.bulk(items, { atomic: true });
```

*(The legacy v1 client `OnlyWorldsClient` was removed in 4.0. Pin `@onlyworlds/sdk@3` only to keep old code running.)*

### Link Field Patterns

**Write link fields under their bare names**: single links as a UUID string, multi links as a UUID array. Same names on read and write; no suffixes, in the SDK and raw v2 HTTP alike. On an existing element, change a multi link with `editLinks`: a `patch` that sends the array replaces the whole list.

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

**A PIN never goes into a build or a `VITE_` variable.** Vite compiles every `VITE_` variable into the JavaScript bundle, where anyone who opens the site can read it. A key plus its PIN is write access to the world. (principles §6)

| Tool | API key | PIN |
|------|---------|-----|
| Script on your own machine (Node, Python) | `.env`, gitignored, read at runtime | `.env`, only if the script writes |
| Browser app that only reads | a read key (`ow_r_...`); prefixed keys read without a PIN | none |
| Browser app that writes (shared or deployed) | the user enters it at runtime | the user enters it at runtime |

A read key in a public bundle lets anyone who finds it read that world, so use one only for a world meant to be public. The browser patterns (build-time read key, runtime prompt, read-then-edit hybrid, why the PIN never goes in `localStorage`) are in **knowledge/deployment.md**, "Credential Handling Patterns".

**Code a person will run does not declare itself an agent.** Leave out `agent: true` (`@onlyworlds/sdk` 4.26.0+), `agent=True` (Python `onlyworlds` 0.3.0+) and the `X-OW-Agent` header: what a client does by default, every person using the app does, so each of their edits would be recorded as agent-made. Set it only in code that is itself an AI agent writing to the world.

### Step 5: Local Development

**Plain HTML + JS** (simplest):
```html
<script type="module">
  import { OwV2Client } from 'https://esm.sh/@onlyworlds/sdk';
  const client = new OwV2Client({ apiKey: prompt('Read key (ow_r_...):') ?? '' });
  for await (const ch of client.listAll('character')) console.log(ch.name);
</script>
```

**Python script** (load `.env` first, with python-dotenv or `set -a; . ./.env; set +a`):
```python
import os, requests
headers = {"API-Key": os.environ["ONLYWORLDS_API_KEY"]}  # add "API-Pin" only for writes
url, params, chars = "https://www.onlyworlds.com/api/v2/character", {"limit": 100}, []
while True:
    page = requests.get(url, headers=headers, params=params).json()  # {data, has_more, next_cursor}
    chars += page["data"]
    if not page["has_more"]:
        break
    params["cursor"] = page["next_cursor"]
```

**Vite + React** (for larger tools; needs a current Node LTS, 20 or 22). The `--template` flag skips the interactive prompts:
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm install && npm install @onlyworlds/sdk && npm run dev
```
`index.html` sits at the project root, not in `src/`.

### Step 6: Deployment

For deployment patterns, see **knowledge/deployment.md**.

Quick version: push to GitHub → connect to Cloudflare Pages → build command `npm run build` → output `dist` → set env vars (a read key at most, never a PIN) → deploy.

### Step 7: Full Scaffold

For a complete project structure ready to run, see **knowledge/scaffold.md**.

## Common Patterns

### Map Viewer

A Map's picture is its `image_url`; `width` and `height` are its size in pixels. Each Pin names its `map` and the pinned element (`element_type` + `element_id`), at integer pixel coordinates `x`, `y` measured from the map's **bottom-left** corner. Lists cannot filter by link, so fetch the pins and filter client-side.

```typescript
async function all(type: string) {           // list() returns one page; listAll walks them all
  const out: any[] = [];
  for await (const el of client.listAll(type)) out.push(el);
  return out;
}
const map = (await all('map'))[0];
const pins = (await all('pin')).filter(p => p.map === map.id);
for (const p of pins) {
  const leftPct = (p.x / map.width) * 100;
  const topPct = 100 - (p.y / map.height) * 100;   // flip y: screen origin is top-left
  placePin(p.element_type, p.element_id, leftPct, topPct);
}
```

If a Map has no `width`/`height`, use the image's natural size. Zone outlines are drawn from Markers (see the MARKER and ZONE sections of `knowledge/schema-reference.md`). Render world text with `textContent`, never `innerHTML`: on a public site the text is data, not markup.

### Editor with Save

```typescript
const character = await client.get('character', id);
// User edits in UI, starting from the value just read...
await client.patch('character', id, { description: editedDescription });
const saved = await client.get('character', id); // verify what landed (principles §5)
```

## Resources

- **Developer on-ramp**: https://www.onlyworlds.com/develop
- **API docs**: https://www.onlyworlds.com/api/docs
- **Ecosystem map** (all surfaces + how they wire): `knowledge/ecosystem.md`
- **Documentation**: https://onlyworlds.github.io
- **Discord**: https://discord.gg/twCjqvVBwb
- **SDK types**: Check @onlyworlds/sdk for full field definitions
