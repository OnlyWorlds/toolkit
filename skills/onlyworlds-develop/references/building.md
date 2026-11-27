# Building a tool

What building on a world needs: the API document, the SDK, credentials in a build, sign-in, local development, deployment, the map viewer and editor patterns, games and engines, addresses.
Open it before a line of client code; the routes a reader uses are in `../SKILL.md`, the writes in `writing.md`.

**First, before a line of client code**: fetch `https://www.onlyworlds.com/api/v2/openapi.json` ([Read What Is Served](#read-what-is-served)), the one source for any route, param or error (memory is not one), and say in your answer which routes and fields you took from it.

## Read What Is Served

The OpenAPI document is the one route table: every route, parameter, body and response code, described. This skill names the routes most work needs; for any other, or any detail you are unsure of, fetch the document once and read that path's entry (it is megabytes: print one path, never the whole).

```bash
curl -s -A "my-tool/1.0" https://www.onlyworlds.com/api/v2/openapi.json -o openapi.json
python -c "import json,sys; p=json.load(open('openapi.json',encoding='utf-8'))['paths']; print(json.dumps(p['/api/v2/'+sys.argv[1]],indent=1)[:6000] if sys.argv[1:] else '\n'.join(p))" bulk
```

With no argument it lists the paths; name one without its `/api/v2/`. A type's field descriptors: `GET /api/metadata/{type}/`. Concepts: https://onlyworlds.github.io/docs/. A version you state is one you read from npm or PyPI this session.

## Building a Tool

### Step 1: Understand the Goal

A **visualization** (maps, graphs, timelines) reads; an **editor** does full CRUD; a **game** reads plus keeps local state; an **integration** uses [The API](../SKILL.md#the-api-v2); a **local tool on a world folder** (pipelines, RAG, offline) reads the files with no account (`../knowledge/world-folder.md`); an **AI agent with a persistent world** goes to [Agents](agents.md#agents).

### Step 2: Read What Is Served

Fetch the OpenAPI document and read the paths you will call ([Read What Is Served](#read-what-is-served)); the on-ramp is https://www.onlyworlds.com/develop.

### Step 3: SDK Setup

`npm install @onlyworlds/sdk`: ESM-only, v2-only, client `OwV2Client`, types generated from the canonical schema. Its major is the one npm shows this session, read before you state it ([Read What Is Served](#read-what-is-served)).

```typescript
import { OwV2Client } from '@onlyworlds/sdk';
// Node: load .env first (`node --env-file=.env`); never hardcode keys
const client = new OwV2Client({
  apiKey: (process.env.OW_API_KEY ?? process.env.ONLYWORLDS_API_KEY)!,
  apiPin: process.env.OW_API_PIN ?? process.env.ONLYWORLDS_API_PIN   // writes only (a seat's ow_s_ too); unset to read
});
for await (const el of client.listAll('character')) { /* all pages; list() is one */ }
const made = await client.create('location', { name: 'Feltropolis' });
await client.patch('character', id, { description: 'Updated' });   // replaces each field it sends
await client.editLinks('character', id, 'friends', { add: ['uuid-a'], remove: ['uuid-b'] });
const feed = client.changesAll(cursor);                             // no cursor = full export
let step; while (!(step = await feed.next()).done) applyChange(step.value);
cursor = step.value.cursor;                                         // save for the next pull
// a guest's or contributor's tool also keeps .head and .epoch: a moved epoch, walk again
const res = await client.bulk(items, { atomic: true });             // does not throw on a failed item
if (res.errors) console.warn(res.items.filter((s) => s.status >= 400)); // nothing written; record no ids
```

Every other method (`get`, `delete`, `upsert`, seats, pictures, sign-in) is typed in `dist/index.d.ts`. The schema-generated palette and metadata (`elementColor`, `ELEMENT_GROUPS`, `ELEMENT_ICONS`, `FIELD_SCHEMA`) keep a tool in sync for free. The v1 client is gone; for old code, pin the last major that carried it, read from npm's version list.

Link fields are as on the wire; on an existing element, change a multi link with `editLinks` (a `patch` with the array replaces the list). Pin coordinates are integers; a Pin's `element_type` and `element_id` are schema fields, not link suffixes.

### Step 4: Credential Handling

**A PIN never goes into a build or a `VITE_` variable**: Vite compiles every `VITE_` variable into the bundle, readable by anyone who opens the site, and a key plus its PIN is write access (principles §6).

| Tool | API key | PIN |
|------|---------|-----|
| Script on your own machine | `.env`, gitignored, read at runtime | `.env`, only if it writes |
| Browser app that only reads | a read key (`ow_r_...`) | none |
| Browser app that writes | the user enters it at runtime | the user enters it at runtime |

A read key in a public bundle lets anyone read that world: use one only for a public world. Browser patterns (build-time read key, runtime prompt, hybrid, no PIN in `localStorage`): `../knowledge/deployment.md`, "Credential Handling Patterns".

**Code a person will run does not declare itself an agent.** Leave out `agent: true`, `agent=True` and the `X-OW-Agent` header: what a client does by default, every person using the app does, so each of their edits would be recorded as agent-made.

#### Sign in with OnlyWorlds

A tool whose users have an onlyworlds.com account can sign them in without ever seeing a password: OAuth 2.1's authorization code with PKCE (S256), the browser sent to `https://www.onlyworlds.com/signin/authorize` and the code traded once at `POST /api/v2/auth/token` for an `ow_a_` account token. The SDK does both ends: `signInWithOnlyWorlds` sends the person, `completeSignIn` on the return page answers the token. Only a tool in the registry can sign people in (`GET /api/v2/auth/clients`, no credential); how a tool is added: [Sign in with OnlyWorlds](https://onlyworlds.github.io/docs/development/api/signin.html). With the token, the account's AI uses: `GET /api/v2/account/ai` lists them, `POST /api/v2/account/ai/ask` answers a question from the elements your own search sends, and `POST /api/v2/account/ai/sort` turns notes into proposed changes, which the tool applies only as the person accepts them. Each spends from the account's daily token rating.

### Step 5: Local Development

**Plain HTML + JS**:
```html
<script type="module">
  import { OwV2Client } from 'https://esm.sh/@onlyworlds/sdk';
  const client = new OwV2Client({ apiKey: prompt('Read key (ow_r_...):') ?? '' });
  for await (const ch of client.listAll('character')) console.log(ch.name);
</script>
```

**Python** (`pip install onlyworlds`; load `.env` first):
```python
import os
from onlyworlds import Client
client = Client(os.environ.get("OW_API_KEY") or os.environ["ONLYWORLDS_API_KEY"])  # the PIN second, only for writes
for ch in client.iter_elements("character"):   # walks every page
    print(ch["name"])
```

**Vite + React** for larger tools: `../knowledge/deployment.md`, "Project Structure".

### Step 6: Deployment

`../knowledge/deployment.md`. In short: GitHub → Cloudflare Pages, build `npm run build`, output `dist`, a read key at most in the env vars, never a PIN.

### Step 7: Full Scaffold

A complete project ready to run: `../knowledge/scaffold.md`.

## Common Patterns

### Map Viewer

A Map's picture is its `image_url`; `width` and `height` are its size in pixels. Each Pin names its `map` and the pinned element (`element_type` + `element_id`) at integer pixel `x`, `y` from the map's **bottom-left** corner. The pin list filters by map (`GET /pin?map={map id}`); the marker list takes `map` and `zone`.

```typescript
const map = await client.get('map', mapId);
for await (const p of client.listAll('pin', { filter: { map: map.id } }))
  placePin(p.element_type, p.element_id, (p.x / map.width) * 100, 100 - (p.y / map.height) * 100); // left %, top %: flip y
```

No `width` or `height`: the map-space profile measures the missing one from the map's own placed pins and markers; with no point either, use the image's natural size. Zone outlines come from Markers (each names its `map` and `zone`, with `x`, `y`, `z`, `order`), in `order` and then by id, joined by the Zone's `shape` (`line` an open path, anything else a closed polygon); `mapSpace` returns frames and outlines read this way.

A Map whose `x_layout` holds a non-empty `method` is a layout map: its Pins were laid out by that method, or by hand on a board (`"hand"`). `x_layout.settings.ground.map` names the Map whose picture it stands on, and on a layout map a Pin with `x_hand: true` was placed by hand: a new lay-out keeps it where it is. A tool that places or drags a Pin by hand on a layout map sets `x_hand: true`; a tool that cannot run the method draws the Pins where they are and never lays them out again. `layoutOf(map, maps, pins)` in the SDK (`layout_of` in Python) answers `{layout, ground, hand}`: the profile's rules 8 to 10. Render world text with `textContent`, never `innerHTML`: it is data, not markup.

### Editor with Save

```typescript
const character = await client.get('character', id);
// the user edits it; ifMatch saves only if nobody changed it since the read, else nothing is
// written and it throws OwPreconditionFailedError, whose `current` is the element now
await client.patch('character', id, { description: edited }, { ifMatch: character.change_seq });
const saved = await client.get('character', id); // verify what landed (principles §5)
```

## Games and Engines

A game takes a world with no key and no network: a world folder, or one `.owworld` file (the carry skill packs it). The API comes in when the game writes back.

- **Unity**: the `unity-sdk` package (Package Manager, Add package from git URL, `https://github.com/OnlyWorlds/unity-sdk.git?path=/Packages/com.onlyworlds.sdk`) reads a folder, an `.owworld` or an account world into typed elements and writes them back; its README is the truth for its calls.
- **Godot, Unreal and others**: no public package yet. Read the folder (`../knowledge/world-folder.md`: one JSON file per element) or the archive by spec §4.7 ([World folders](https://onlyworlds.github.io/docs/schema/folders)).
- **The map as space**: a Pin's and a Marker's `x`, `y` count in pixels from the Map's bottom-left (an engine whose y runs down flips it); the picture is the Map's `image_url`; Maps nest by `parent_map`. Height is optional: a Pin's and a Marker's `z` is its elevation in the same pixels, upward, and a Map's `depth` is the z extent; few worlds fill them, so a game brings its own. The rules are the map-space profile (`profiles/map-space.md` in github.com/OnlyWorlds/schema-dist, with its fixture), read by `mapSpace` in the SDK and `map_space` in the Python package: each Map's frame, each Zone's outline, each Pin's point, and the scale in metres per pixel from a Map's `x_metres_per_pixel` (none without it).
- **An archive reader of your own** is graded by schema-dist's `fixtures/owworld/` (each zip with its verdict): run every case before trusting it. A runtime's own zip reader, JSON parser (numbers as floats) and Unicode tables each fail some.

## Addresses

An element has one address in three spellings: `https://www.onlyworlds.com/w/<world id>/<type>/<id>` (the site's page; **Copy address** on a world's or an element's page on the site copies it), `ow://<type>/<id>` inside a world's text, and `ow://<world id>/<type>/<id>` across worlds. A world alone is `https://www.onlyworlds.com/w/<world id>` or `ow://<world id>`. Any of them may end in a moment, `@<step>`, then a lens, `?lens=<id>`. Write and read them with the packages, never a pattern of your own: `elementAddress` and `parseOwLink` in the SDK, `element_address` and `parse_ow_link` in the Python package. A field holding an address is text: never fetch or resolve it on the server. The one link opens for everyone: the owner and a member land on their own page for it, anyone else on the world's public page when it has one. The profile: `profiles/address.md` in github.com/OnlyWorlds/schema-dist, with its fixture.

## The answer says

- For client code, the OpenAPI document by its URL, and the routes and fields taken from it (the first line; Read What Is Served).
- A version only as read from npm or PyPI this session (Read What Is Served).
- In client code, no PIN in a build or a `VITE_` variable, and no agent header in a person's app (Step 4).
