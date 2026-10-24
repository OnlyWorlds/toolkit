---
name: onlyworlds-develop
description: "Build a tool, game, app or AI agent on world data, and read or write an onlyworlds.com world through its API. Use when the user says 'npm install @onlyworlds/sdk', 'a React app on my world', 'connect my agent to my world', 'upload this to my world', 'bulk upload', 'sync changes', 'set up the MCP server', or wants OnlyWorlds as a backend. Reads the live API document for routes."
---

# OnlyWorlds Develop

Read and write an onlyworlds.com world through its API, and build tools, games and agents on world data. The shared rules (read before write, verify after write, credentials, extension fields) are `knowledge/principles.md`.

**First, before a line of client code**: fetch `https://www.onlyworlds.com/api/v2/openapi.json` ([Read What Is Served](#read-what-is-served)), the one source for any route, param or error (memory is not one), and say in your answer which routes and fields you took from it.

## Quick Reference

| You need | Go to |
|---|---|
| Read and write a world | [Critical Rules](#critical-rules), then [The API](#the-api-v2) |
| Many elements at once | [Bulk Upload](#bulk-upload) |
| Keep a copy in sync | [Sync Changes](#sync-changes) |
| An AI agent on a world | [Agents](#agents): the MCP connect line or a seat; `X-OW-Agent: 1` on writes |
| A TypeScript tool | [Building a Tool](#building-a-tool), `knowledge/scaffold.md`, `knowledge/deployment.md` |
| Python | `pip install onlyworlds` (Python 3.12+), its `Client` |
| A tool on a world folder, no account | `knowledge/world-folder.md` |
| Old v1 code (`/api/worldapi/`) | `references/v1-classic.md` |

## Read What Is Served

The OpenAPI document is the one route table: every route, parameter, body and response code, described. This skill names the routes most work needs; for any other, or any detail you are unsure of, fetch the document once and read that path's entry (it is megabytes: print one path, never the whole).

```bash
curl -s -A "my-tool/1.0" https://www.onlyworlds.com/api/v2/openapi.json -o openapi.json
python -c "import json,sys; p=json.load(open('openapi.json',encoding='utf-8'))['paths']; print(json.dumps(p['/api/v2/'+sys.argv[1]],indent=1)[:6000] if sys.argv[1:] else '\n'.join(p))" bulk
```

With no argument it lists the paths; name one without its `/api/v2/`. A type's field descriptors: `GET /api/metadata/{type}/`. Concepts: https://onlyworlds.github.io/docs/. A version you state is one you read from npm or PyPI this session.

## Critical Rules

1. **Change multi-links through the links route; read before any other PATCH.** `POST /api/v2/{type}/{uuid}/links/{field}` with `{"add": [...], "remove": [...]}` merges on the server in one atomic step, no read needed. PATCH *replaces* the fields you send: to append text or change a single link, GET the current value, build the full new value, then PATCH it. Overwriting a field with a partial value is permanent data loss. A read-back body carries `type`, `created_at`, `updated_at` and `change_seq`; strip them before sending a body back (each one is a 422).
2. **Verify after write.** GET the element back and confirm the fields landed (principles §5).
3. **/bulk is the standard upload path** for parse results. One request, mixed types, per-item results, idempotent retry. Don't loop hundreds of individual POSTs; see [Bulk Upload](#bulk-upload).
4. **Mint your own UUIDs on create.** Any RFC-4122 UUID works; v7 is recommended (the server's own are v7). Client-minted ids let a batch reference its own new elements and make retries idempotent.
5. **Read the error envelope.** The API names what's wrong (unknown field, dangling link, bad credentials) with a `code`, `message`, `param` and `doc_url`. Don't guess: read the message ([Errors](#errors)).

## Safety Notice

Writes can modify or delete world data.
- Before a write session to an existing world, export it to a world folder (carry's `export_world`). That folder is the rollback: re-uploading its elements with /bulk (read-only fields stripped) puts the old values back, but does not remove elements created since; delete those by id.
- Test with a small batch first.
- Read before PATCH (Critical Rule 1). Verify after write (Critical Rule 2).

## Credentials

Look for `.ow/config.json` first: its `credential_mode` says what `.env` holds, `full` (key and PIN), `key-only` (for a write, the user adds the PIN line) or `manual` (the user fills `.env` for this session). No config: look in `.env` for `OW_API_KEY` (older: `ONLYWORLDS_API_KEY`), else run start's Connect an account. Several worlds, or a throwaway test world, need no setup: each world's pair goes in `.env` under names you agree on (`WORLD_A_API_KEY`).

**Credentials never go through chat.** The user types them into `.env`; you load them and never print or repeat them, even one pasted into chat (ask for it in `.env`).

- **API-Key**: one world's. Prefixed (`ow_w_…` write, `ow_r_…` read, made for sharing) or a legacy 10-digit key (valid, no longer issued): Account → your world → API keys.
- **API-Pin**: on every write. The owner writes with their account PIN (Account → Settings → World PIN: one for every world they own); a member of someone else's world with their own account PIN; an agent seat with its seat secret (`ow_s_…`). See [PIN](#pin-the-world-wall).
- **X-OW-Agent**: as an AI agent, send `X-OW-Agent: 1` on every write (create, PUT, PATCH, DELETE, links, bulk), so your writes are recorded as agent-made (`changed_via: declared`); only its presence counts. A seat's key and the MCP server count as agents without it. Code for a person's app leaves it off ([Step 4](#step-4-credential-handling)).
- **Account tokens** (`ow_a_…`, Settings → Account, sent as `Authorization: Bearer`) serve the `/api/v2/account/…` routes. Element work never needs one.

**The examples** load `.env` into the shell first and build two header sets (reads with a prefixed key need no PIN):

```bash
set -a; . ./.env; set +a
K="API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"; P="API-Pin: ${OW_API_PIN:-$ONLYWORLDS_API_PIN}"
W=(-H "$K" -H "$P" -H "X-OW-Agent: 1" -H "Content-Type: application/json")   # every write
B=https://www.onlyworlds.com/api/v2
```

## The API (v2)

**Base URL** `https://www.onlyworlds.com/api/v2/` (always `www.`). **Endpoint names are SINGULAR**, the type in lowercase: `/character`, `/location`, `/institution`.

**Link fields are FLAT UUID arrays, both directions**: read AND write use the bare field name (`friends`, `species`), holding raw UUID strings; a single link is one UUID string. There is no `_id`/`_ids` suffix in v2 (v1 only). Sending `friends_ids` to v2 or /bulk is a hard `422 Unknown field: friends_ids`, the #1 new-user error.

```bash
curl -s "$B/health"                  # {"status": "ok", "service": "keel"}
curl -s "$B/world" -H "$K"           # world meta; PATCH it (partial) with "${W[@]}"
```

The world's now is `time_range_current` (a folder's `world.json` says `time_current`).

### List Elements

`curl -s "$B/{type}?limit=100" -H "$K"` returns `{"data": [...], "has_more": true, "next_cursor": "..."}`. Pass `next_cursor` (opaque) back as `?cursor=` until `has_more` is `false`. Lists come in change order; sort client-side. The filters (`name__icontains`, `supertype`, `ids`, `fields`, more) are that path's parameters in the document; any other is a `422`.

### Get Element

`GET $B/{type}/{uuid}` returns the **bare element object** (no `data` wrapper); the trailing slash is optional.

### Create Element

```bash
curl -s -X POST "$B/{type}" "${W[@]}" \
  -d '{"id": "{your-uuid}", "name": "Element Name", "description": "...", "friends": ["{uuid}"]}'
```

Returns `201` with the element. POSTing an id that exists is `409 id_conflict`; `PUT $B/{type}/{uuid}` upserts (201 created, 200 replaced), replacing the whole element. An `Idempotency-Key` header works here too.

### Update Element (PATCH)

`curl -s -X PATCH "$B/{type}/{uuid}" "${W[@]}" -d '{"description": "Updated"}'`

**PATCH replaces the fields you send** (Critical Rule 1); for multi-link arrays use the links route.

**Extension fields** (`x_*`, `atlas_*`, `shadow_*`, principles §4) are stored verbatim and returned on v2 reads. PATCH merges extension keys (omitting one keeps it); PUT, and a /bulk item with an existing id, replace the whole element, extension fields included; v1 does not return them.

**Base fields**: `world` is ignored on write (the key decides). Numbers are integers in the world's units; a fraction is truncated. Ranges are advisory: out-of-range values are stored, so tools clamp.

### Add or Remove Links

```bash
curl -s -X POST "$B/{type}/{uuid}/links/{field}" "${W[@]}" -d '{"add": ["{uuid}"], "remove": ["{uuid}"]}'
```

Atomic server-side merge on one multi-link field: `add` skips ids already present, `remove` ignores ids not present, and each added target must exist (`invalid_link` otherwise). Returns the updated element. A single-link or unknown field is a `422`.

**Some links are one-directional**: Ability has no `characters` (link from `Character.abilities`), Law no `institutions` (use `Law.author`). Which side owns each link, and every type's fields: the model skill.

### Delete Element

`curl -s -X DELETE "$B/{type}/{uuid}" "${W[@]}"` returns `204`. (A `000` curl status is a dropped connection: retry.) Delete is rarely right: it also strips the element from every link to it. Retire what died, left or ended (principles §2); delete only what a human approved.

## Bulk Upload

`POST /api/v2/bulk` is the standard upload path: one request, mixed types, per-item results, idempotent retry. **No topological sorting needed**: an element may reference a sibling created later in the same batch.

```json
{ "items": [
    { "type": "location", "element": { "id": "{uuid-A}", "name": "Feltropolis" } },
    { "type": "character", "element": { "id": "{uuid-B}", "name": "Admiral Fluffington", "location": "{uuid-A}" } }
] }
```

- The key is `items` (not `operations`); each item wraps a `type` and the `element`. An element without an `id`, or with a new one, is created.
- **An element whose `id` already exists replaces that element entirely, like PUT.** Every field you don't send is cleared, links and extension fields included. Never send a partial element for an existing id: update with PATCH or the links route.
- The element holds writable fields only: `type` belongs on the item, and `created_at`, `updated_at`, `change_seq` are rejected (422). An `op` key is ignored, and there is no delete op.
- Max 1000 items per request. `"atomic": true` at the top level makes the batch all-or-nothing.

```bash
curl -s -X POST "$B/bulk" "${W[@]}" -H "Idempotency-Key: {a-uuid-for-this-batch}" -d @batch.json
```

The response is `{"errors": false, "items": [{"status": 201, "id": "{uuid-A}", ...}, ...]}`, in request order. `errors` is `true` if *any* item failed; without `atomic`, committed items still land and each failure carries a structured `error`, so scan every `status`. A failed item, or a create sent without an id, has `"id": null`: match results to items by index.

**Idempotency-Key retry**: if the request times out or drops, resend the *identical* body with the *same* key: the server replays the original result (an `idempotent-replay: true` header) instead of double-creating, so a bulk upload is safe to retry blindly. The same key with a *different* body is `409 idempotency_error`: a corrected batch needs a new key. Keys are kept 24h.

### Upload a parse: recommended flow

1. Mint a UUID (v7 recommended) for every element up front (Critical Rule 4).
2. Build one `items` array: all types, links already pointing at your minted UUIDs.
3. POST to `/api/v2/bulk` with an `Idempotency-Key`.
4. If `errors: true`, read each failing item's `error.message`/`param`, fix those items, and resend under a **new** key (full items with ids replace, so resending the ones that succeeded is harmless).
5. Spot-check with a GET (Critical Rule 2).

## Sync Changes

`GET /api/v2/changes` returns everything changed since a cursor: `curl -s "$B/changes" -H "$K"`.

```json
{ "cursor": "…", "has_more": false, "head": 1,
  "changes": [ { "op": "upsert", "type": "location", "id": "…", "change_seq": 1, "element": { … } } ] }
```

- Store `cursor` (opaque) and pass it back as **`?since={cursor}`** for only newer changes. `?cursor=` is a `422` here: list pagination is a different mechanism.
- Pages default to 500 ops (`?limit=`, max 1000). Loop until `has_more` is `false`. Walking from no `since` is a full export.
- `?head=true` returns only the tip as `cursor` (no ops, cheap): follow from now, or check whether you are behind.
- `head` on every page is the world's tip. A stored cursor ahead of `head` means the world was restored from backup: re-sync from zero.
- Deletes arrive as `"op": "delete"`. World-meta edits never enter this feed.

## PIN (the world wall)

The PIN is the **world's wall**, not a dialect's, Argon2-hashed on the server: every write needs it. Prefixed keys read without it (sending it does no harm); only a legacy 10-digit key reading a private world sends it on reads. Wrong PINs are throttled per key: after 3 failures each retry waits longer, and 10 lock the key for 15 minutes (`429 rate_limited`, `Retry-After`).

## Errors

v2 and /bulk answer `{"error": {"type", "code", "message", "param", "doc_url"}}`: the `message` names the field or credential at fault. Every code a route returns is in that path's responses in the document; the ones a first build hits:

| You get | Fix |
|---|---|
| `401` `invalid_credentials`: bad or missing key, or a wrong PIN on a write (`key_revoked`: revoked) | Check `API-Key` and `API-Pin`; a revoked key needs a new one |
| `422` `Unknown field: friends_ids`: a typo, or v1's `_ids` suffix; `param` names it | The bare canonical field name |
| `400` / per-item `invalid_link`: a link names a UUID that does not exist | A real UUID, or the target in the same batch |
| `409` `id_conflict`: POST of an id that exists | PUT to upsert |
| `429` `rate_limited`: failed PINs, throttled per key ([PIN](#pin-the-world-wall)) | Wait `Retry-After` seconds; sooner does not help |
| `429` `too_many_requests`: over the request budget (the document's Limits) | Wait `Retry-After`; `RateLimit-Remaining` says where you stand |
| `503` `server_busy`: every request slot is busy | Retry after `Retry-After` |

**These are honest errors: nothing is silently dropped.** An unknown field is rejected (not ignored), a dangling link rejected (not nulled), a write without the right PIN rejected (not partly applied). A `2xx` means what you sent landed; still verify. A `202` is not a write: it answers `{"proposal": …}` where the owner takes an agent seat's writes as proposals, and nothing changes until a keeper accepts.

## Agents

**Connect the MCP server from Claude Code** (`.env` loaded into the shell, so the key is never typed):
```bash
claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp \
  --header "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}" --header "API-Pin: ${OW_API_PIN:-$ONLYWORLDS_API_PIN}"
```
The server has schema, read and write tools, and no delete tool.

**A seat of its own** suits an agent that writes to someone's world: **Make a seat** on the owner's Access page (Let someone in, An AI agent, More options), or under **Your AI in this world** on a member's; the `.env` lines show once, and a lost key is **New key** beside the seat. Its `ow_s_` secret is its PIN, and its writes count as agent-made. Otherwise declare: the header, `agent: true` in the SDK, `agent=True` in Python's `Client`.

**Patterns that work**:
- **Agent with a world**: the agent queries typed elements over MCP instead of guessing from context. `update_element` is a server-side read-merge, so partial writes are safe.
- **World as RAG corpus**: the folder IS a typed, chunked corpus, one JSON file per entity.
- **AI proposes, a human approves, one writer applies** (principles §2): the agent drafts a batch with its own minted UUIDs, a human rules on the list, only the approved items go up via `/bulk`, and people read the result back in Atlas.
- **Game/sim state**: the world as the NPC knowledge base; the app reads typed truth, the LLM voices it. A tool's own data goes in `x_<tool>_...` fields.

## Building a Tool

### Step 1: Understand the Goal

A **visualization** (maps, graphs, timelines) reads; an **editor** does full CRUD; a **game** reads plus keeps local state; an **integration** uses [The API](#the-api-v2); a **local tool on a world folder** (pipelines, RAG, offline) reads the files with no account (`knowledge/world-folder.md`); an **AI agent with a persistent world** goes to [Agents](#agents).

### Step 2: Read What Is Served

Fetch the OpenAPI document and read the paths you will call ([Read What Is Served](#read-what-is-served)); the on-ramp is https://www.onlyworlds.com/develop.

### Step 3: SDK Setup

`npm install @onlyworlds/sdk`. Its major is 4: ESM-only, v2-only, client `OwV2Client`, types generated from the canonical schema.

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

Every other method (`get`, `delete`, `upsert`, seats, pictures, sign-in) is typed in `dist/index.d.ts`. The schema-generated palette and metadata (`elementColor`, `ELEMENT_FAMILIES`, `ELEMENT_ICONS`, `FIELD_SCHEMA`) keep a tool in sync for free. The v1 client is gone; pin `@onlyworlds/sdk@3` only for old code.

Link fields are as on the wire; on an existing element, change a multi link with `editLinks` (a `patch` with the array replaces the list). Pin coordinates are integers; a Pin's `element_type` and `element_id` are schema fields, not link suffixes.

### Step 4: Credential Handling

**A PIN never goes into a build or a `VITE_` variable**: Vite compiles every `VITE_` variable into the bundle, readable by anyone who opens the site, and a key plus its PIN is write access (principles §6).

| Tool | API key | PIN |
|------|---------|-----|
| Script on your own machine | `.env`, gitignored, read at runtime | `.env`, only if it writes |
| Browser app that only reads | a read key (`ow_r_...`) | none |
| Browser app that writes | the user enters it at runtime | the user enters it at runtime |

A read key in a public bundle lets anyone read that world: use one only for a public world. Browser patterns (build-time read key, runtime prompt, hybrid, no PIN in `localStorage`): `knowledge/deployment.md`, "Credential Handling Patterns".

**Code a person will run does not declare itself an agent.** Leave out `agent: true`, `agent=True` and the `X-OW-Agent` header: what a client does by default, every person using the app does, so each of their edits would be recorded as agent-made.

### Step 5: Local Development

**Plain HTML + JS**:
```html
<script type="module">
  import { OwV2Client } from 'https://esm.sh/@onlyworlds/sdk@4';
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

**Vite + React** for larger tools: `knowledge/deployment.md`, "Project Structure".

### Step 6: Deployment

`knowledge/deployment.md`. In short: GitHub → Cloudflare Pages, build `npm run build`, output `dist`, a read key at most in the env vars, never a PIN.

### Step 7: Full Scaffold

A complete project ready to run: `knowledge/scaffold.md`.

## Common Patterns

### Map Viewer

A Map's picture is its `image_url`; `width` and `height` are its size in pixels. Each Pin names its `map` and the pinned element (`element_type` + `element_id`) at integer pixel `x`, `y` from the map's **bottom-left** corner. A pin list cannot filter by map: fetch the pins, filter client-side.

```typescript
const map = await client.get('map', mapId);
for await (const p of client.listAll('pin')) if (p.map === map.id)
  placePin(p.element_type, p.element_id, (p.x / map.width) * 100, 100 - (p.y / map.height) * 100); // left %, top %: flip y
```

No `width`/`height`: use the image's natural size. Zone outlines come from Markers (each names its `map` and `zone`, with `x`, `y`, `z`, `order`). Render world text with `textContent`, never `innerHTML`: it is data, not markup.

### Editor with Save

```typescript
const character = await client.get('character', id);
// the user edits it; ifMatch saves only if nobody changed it since the read, else nothing is
// written and it throws OwPreconditionFailedError, whose `current` is the element now
await client.patch('character', id, { description: edited }, { ifMatch: character.change_seq });
const saved = await client.get('character', id); // verify what landed (principles §5)
```

## Classic API (v1)

The legacy `/api/worldapi/` dialect and its traps: `references/v1-classic.md`.

## Resources

- The API document, browsable: https://www.onlyworlds.com/api/docs
- For AI builders: https://onlyworlds.github.io/docs/development/ai.html
- Discord: https://discord.gg/twCjqvVBwb
