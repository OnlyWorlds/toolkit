---
name: onlyworlds-api
description: "Read and write an onlyworlds.com world through its API: fetch, create, update, bulk upload, sync. Use when the user says 'upload this to my world', 'pull my world', or any API work. Better than hand-written curl."
---

# OnlyWorlds API

Read and write world data via the OnlyWorlds REST API.

Shared rules (read before write, verify after write, credentials, extension fields) live in `knowledge/principles.md`; this skill applies them to the API.

## Quick Reference (v2)

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Health check | GET | `/api/v2/health` |
| Get world info | GET | `/api/v2/world` |
| Update world meta (partial) | PATCH | `/api/v2/world` |
| List elements by type | GET | `/api/v2/{type}` |
| Get specific element | GET | `/api/v2/{type}/{uuid}` |
| Create element | POST | `/api/v2/{type}` |
| Update element (partial) | PATCH | `/api/v2/{type}/{uuid}` |
| Upsert element (full replace; 201 created, 200 replaced) | PUT | `/api/v2/{type}/{uuid}` |
| **Add/remove multi-links (server-side merge)** | POST | `/api/v2/{type}/{uuid}/links/{field}` |
| Delete element | DELETE | `/api/v2/{type}/{uuid}` |
| **Bulk upsert (standard upload path)** | POST | `/api/v2/bulk` |
| Sync changes since cursor | GET | `/api/v2/changes?since={cursor}` |
| Current feed tip (no bodies) | GET | `/api/v2/changes?head=true` |
| Field descriptors for a type | GET | `/api/metadata/{type}/` |

**Endpoint names are SINGULAR**: `/character`, `/location`, `/institution`. NOT plural.

**Link fields are FLAT UUID arrays, both directions**: read AND write use the bare field name (`friends`, `species`, `objects`), holding raw UUID strings. There is no `_id`/`_ids` suffix in v2. (The suffix is a v1-only thing, see `references/v1-classic.md`. Sending `friends_ids` to v2 or /bulk is a hard `422 Unknown field: friends_ids`, the #1 new-user error.)

**Teach v2.** Every fresh example here uses `/api/v2/` and `/api/v2/bulk`. The v2 surface returns real pagination, flat UUID link arrays, native creates, and honest Stripe-style errors that name the problem. The older v1 "classic" dialect keeps working indefinitely, but it has traps v2 doesn't; they are in `references/v1-classic.md`. If you're writing new code, stay in v2.

**Credentials in examples.** Every example sends `$ONLYWORLDS_API_KEY` and `$ONLYWORLDS_API_PIN`. Load them from `.env` first (for example `set -a; . ./.env; set +a`; if a name is unset, fill it from its `OW_*` twin: `ONLYWORLDS_API_KEY=${ONLYWORLDS_API_KEY:-$OW_API_KEY}`, likewise the PIN); never print, echo, or paste a key or PIN into chat (principles §6). Reads with a prefixed key (`ow_w_`, `ow_r_`) need no PIN, so read examples send the key only; writes send both. A legacy 10-digit key reading a private world also needs the PIN.

## Critical Rules

1. **Change multi-links through the links route; read before any other PATCH.** `POST /api/v2/{type}/{uuid}/links/{field}` with `{"add": [...], "remove": [...]}` merges on the server in one atomic step, with no read needed (the REST twin of MCP `edit_links`). PATCH *replaces* the fields you send and does not merge: to append text or change a single link, GET the current value first, build the full new value, then PATCH it. Overwriting a field with a partial value is permanent data loss. A read-back body carries `type`, `created_at`, `updated_at` and `change_seq`; strip them before sending a body back (each one is a 422).
2. **Verify after write.** GET the element back and confirm the fields landed (principles §5).
3. **/bulk is the standard upload path** for parse results. One request, mixed types, per-item results, idempotent retry. Don't loop hundreds of individual POSTs; see [Bulk Upload](#bulk-upload-standard-for-parse-results).
4. **Mint your own UUIDs on create.** IDs are UUIDs: any RFC-4122 UUID works, v7 is recommended for index locality, and ids the server assigns when you omit one are v7. Client-minted IDs let you reference an element you're creating in the *same* bulk batch (forward sibling refs are legal, so no topological pre-sorting is needed) and make retries idempotent. Generate one per element before upload.
5. **Read the error envelope.** The API now tells you exactly what's wrong (unknown field, dangling link, bad credentials) with a `code`, `message`, `param`, and `doc_url`. Don't guess: read the message. See [Error Handling](#error-handling).

## Safety Notice

Write operations can modify or delete world data.
- Before a write session to an existing world, export it to a world folder (`knowledge/world-folder.md`, "Exporting an account world to a folder"). That folder is the rollback: re-uploading its elements with /bulk (read-only fields stripped) puts the old values back, but does not remove elements created since; delete those by id.
- Test with a small batch first.
- Read before PATCH (Critical Rule 1). Verify after write (Critical Rule 2).

## Instructions

### Step 1: Get Credentials

Check for `.ow/config.json` in the current directory first:

| Config Found | credential_mode | Action |
|-------------|----------------|--------|
| Yes | full | Load API-Key + API-Pin from `.env` |
| Yes | key-only | Load API-Key from `.env`. For a write, the user adds the PIN line to `.env` first |
| Yes | manual | The user fills `.env` for this session, then load it |
| No | (none) | Check `.env` for `ONLYWORLDS_API_KEY` (or `OW_API_KEY`); if it is not there, run the project-setup skill |

A task that spans several worlds, or a throwaway test world, needs no project setup: the user puts each world's key and PIN in `.env` under names you agree on (for example `WORLD_A_API_KEY`), and each call sends its own world's pair.

**Credentials never go through chat.** The user types them into `.env` themselves (the project-setup skill shows the format); you load them from there and never see, print, or repeat them. If the user pastes one into chat anyway, do not repeat it back, and ask them to put it in `.env` instead.

- **API-Key**: World-scoped key. May be a prefixed key (`ow_w_…` world-write, `ow_r_…` read-share) or a legacy 10-digit key (grandfathered forever; still valid, but no longer issued). Get one on onlyworlds.com under Account → your world → API keys.
- **API-Pin**: The world's PIN (Argon2 wall). Required on **every write** when the world has one. Prefixed keys always read without it; only a legacy 10-digit key reading a private world needs it. See [PIN](#pin-the-world-wall).

A third credential exists for account-level automation: **account tokens** (`ow_a_…`, minted in the portal under Settings → Account, shown once, sent as `Authorization: Bearer` on `/api/v2/account/…` routes). Normal element work never needs one.

| Route (under `/api/v2/account`) | Does |
|---|---|
| `GET` / `PATCH` (the base route) | Read / edit your profile |
| `GET` / `POST` `/worlds` | List your worlds / create one |
| `GET` / `POST` `/worlds/{id}/keys` | List a world's keys (last 4 chars only) / mint a key |
| `DELETE` `/worlds/{id}/keys/{key_id}` | Revoke a key |
| `GET` / `POST` `/watched`, `DELETE` `/watched/{id}` | Watched worlds (other people's worlds you follow by read key) |
| `GET` `/tokens`, `DELETE` `/tokens/{id}` | List / revoke account tokens |

**World meta**: `PATCH /api/v2/world` updates the world's own fields (name, description, image_url, time settings) with the same key and PIN. It is partial like element PATCH, and an unknown field rejects the whole request. The world's current point in time is `time_range_current` on the API (a world folder's `world.json` calls it `time_current`). `GET /api/v2/world` returns an `ETag`; send it back as `If-None-Match` for a cheap `304` when nothing changed.

### Step 2: Validate + Fetch World Info

```bash
curl -s "https://www.onlyworlds.com/api/v2/health"
# → {"status": "ok", "service": "keel"}

curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

If credentials are bad you get a `401` with a Stripe-style envelope naming the problem (`invalid_credentials`); read it rather than re-guessing.

### Step 3: Perform Operations

## API Operations (v2)

### List Elements

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}?limit=100" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

**Response is enveloped and paginated:**
```json
{ "data": [ {...}, {...} ], "has_more": true, "next_cursor": "eyJzIjog..." }
```

- `data`: array of element objects for this page.
- `has_more`: whether more pages exist.
- `next_cursor`: opaque base64 token. Treat it as opaque (don't parse it). To get the next page, pass it back:

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}?limit=100&cursor={next_cursor}" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

Loop, following `next_cursor`, until `has_more` is `false`.

**Element types** (lowercase, singular): character, creature, species, family, collective, institution, location, zone, map, pin, marker, object, construct, title, ability, trait, language, law, event, narrative, phenomenon, relation

**Fields per type**: `knowledge/schema-reference.md`, or `GET /api/metadata/{type}/`. The spatial types carry fields no other type has: Map has `width`, `height`, `depth`, `hierarchy`, `parent_map`, `location` and `background_color`; a Pin names its `map`, the pinned element as `element_type` + `element_id`, and `x`, `y`, `z`; a Marker names its `map` and `zone`, with `x`, `y`, `z` and `order`.

**Query params** (lists; `expand` and `fields` also work on a single GET):

| Param | Effect |
|-------|--------|
| `?name__icontains=value` | Filter by name (case-insensitive partial match) |
| `?supertype=value` / `?subtype=value` | Filter by exact supertype / subtype |
| `?expand=friends,location` | Expand those link fields one level into stubs |
| `?fields=name,supertype` | Return only these fields |
| `?limit=`, `?cursor=` | Page size (default 100, max 1000), next page |

Any other param on a list returns `422 Unknown query parameter`. Lists always come in change order (least recently changed first); `?ordering=` returns `422` too, so sort client-side.

**Link fields in v2 responses are flat UUID arrays**: `"species": ["0698c9df-…"]`, `"friends": ["uuid", "uuid"]`. Plain UUID strings, same names as you write. (v1 expands these into nested `{id, name, …}` objects, see `references/v1-classic.md`.)

### Get Element

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

Returns the **bare element object** (not enveloped: no `data` wrapper on a singular GET). The trailing slash is optional on v2 (it works with or without).

### Create Element

```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/{type}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" \
  -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"id": "{your-uuid}", "name": "Element Name", "description": "...", "friends": ["{uuid}"]}'
```

Returns `201` with the flat element object, including echoed `created_at`/`updated_at` (ISO-8601 UTC). Mint the `id` yourself (Critical Rule 4) so you can reference it elsewhere and so retries are safe. POSTing an id that already exists returns `409 id_conflict`; use PUT to upsert. Link fields use bare names holding UUID arrays. An `Idempotency-Key` header works here too (same rules as [bulk](#bulk-upload-standard-for-parse-results), kept 24h).

### Update Element (PATCH)

```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" \
  -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

**PATCH replaces the fields you send.** To append to `description` or change a single link, GET the current value first, combine, then send the full result (Critical Rule 1). For multi-link arrays use the links route instead.

### Add or Remove Links

```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/{type}/{uuid}/links/{field}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" \
  -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"add": ["{uuid}"], "remove": ["{uuid}"]}'
```

Atomic server-side merge on one multi-link field: `add` skips ids already present, `remove` ignores ids not present, and each added target must exist (`invalid_link` otherwise). Returns the updated element. A single-link or unknown field returns `422`.

### Delete Element

```bash
curl -s -X DELETE "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" -H "API-Pin: $ONLYWORLDS_API_PIN"
```

Returns `204 No Content`. (A `000` curl status is a dropped connection, not a server verdict; retry it.)

Delete is rarely the right tool: it also removes the element from every link that pointed at it. For something that died, left, or ended, retire it instead (mark and date it, principles §2), and delete only what a human approved.

## Bulk Upload (standard for parse results)

`POST /api/v2/bulk` is the standard path for uploading parsed elements. One request, mixed element types, structured per-item results, idempotent retry. **No topological sorting needed**: an element may reference a sibling created later in the same batch (forward refs are legal).

**Request shape**: the key is `items` (not `operations`), and each item wraps a `type` and the `element`:

```json
{
  "items": [
    { "type": "location", "element": { "id": "{uuid-A}", "name": "Feltropolis" } },
    { "type": "character", "element": { "id": "{uuid-B}", "name": "Admiral Fluffington", "location": "{uuid-A}" } }
  ]
}
```

- An element without an `id` is created; one with a new `id` is created under that id.
- **An element whose `id` already exists replaces that element entirely, like PUT.** Every field you don't send is cleared, links and extension fields (`x_*`, `atlas_*`, `shadow_*`) included. Never send a partial element for an existing id: update existing elements with PATCH or the links route.
- The element body holds writable fields only. `type` belongs on the item, not in the element, and `created_at`, `updated_at` and `change_seq` are rejected (422).
- An `op` key is optional and ignored, and there is no delete op.
- Max 1000 items per request.
- Add `"atomic": true` at the top level to make the batch all-or-nothing: any failed item rolls back the whole batch.

```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/bulk" \
  -H "API-Key: $ONLYWORLDS_API_KEY" \
  -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: {a-uuid-for-this-batch}" \
  -d @batch.json
```

**Response** (enveloped, per item):
```json
{
  "errors": false,
  "items": [
    { "status": 201, "id": "{uuid-A}", "created_at": "...", "updated_at": "..." },
    { "status": 201, "id": "{uuid-B}", "created_at": "...", "updated_at": "..." }
  ]
}
```

- Top-level `errors` is `true` if *any* item failed. Committed items still land; failed items are reported per-item with a structured `error` (see below). Without `atomic`, the batch is not all-or-nothing, so scan every item's `status`.
- Results come back in request order. Each carries its `id` when one is known, plus `created_at`/`updated_at` on success. An item that failed validation, or a create sent without an id, has `"id": null`, so match results to items by array index.

**Idempotency-Key retry pattern**: set an `Idempotency-Key` header (a UUID you pick for the batch). If the request times out or the connection drops, resend the *identical* body with the *same* key: the server replays the original result instead of double-creating. A replayed response carries an `idempotent-replay: true` header and identical timestamps. This makes bulk uploads safe to retry blindly. The same key with a *different* body returns `409 idempotency_error`, so a corrected batch needs a new key. Keys are kept 24h.

**Link fields in /bulk use flat bare names** (`friends`, `location`) holding UUIDs, same as v2, never the `_ids` suffix.

### Upload a parse: recommended flow

1. Mint a UUID (v7 recommended) for every element up front (Critical Rule 4).
2. Build one `items` array: all types, links already pointing at your minted UUIDs (forward refs are fine).
3. POST to `/api/v2/bulk` with an `Idempotency-Key`.
4. Scan the response: if `errors: true`, read each failing item's `error.message`/`param`, fix those items, and resend under a **new** Idempotency-Key. Items with ids replace, so resending the same full items that already succeeded is harmless; you can also send only the fixed items.
5. Spot-check with a GET (Critical Rule 2).

No two-pass dance is needed on v2: the batch resolves sibling links itself.

## Sync Changes

`GET /api/v2/changes` returns everything that changed since a cursor, the basis for incremental sync.

```bash
curl -s "https://www.onlyworlds.com/api/v2/changes" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

```json
{
  "cursor": "…",
  "changes": [
    { "op": "upsert", "type": "location", "id": "…", "change_seq": 1, "updated_at": "…", "element": { …full element… } }
  ],
  "has_more": false,
  "head": 1
}
```

- Store `cursor` and pass it back as **`?since={cursor}`** to get only newer changes. `?cursor=` is a `422 Unknown query parameter` here. Treat the cursor as opaque; it is a different mechanism from the list-pagination cursor.
- Pages default to 500 ops (`?limit=`, max 1000). Loop until `has_more` is `false`. Walking from no `since` is a full export in one feed.
- `?head=true` returns only the current tip as `cursor` (no ops, cheap). Use it to start following from now, or to check whether you are behind.
- `head` on every page is the world's current tip. A stored cursor ahead of `head` means the world was restored from backup: re-sync from zero.
- Deletes arrive as `"op": "delete"`. World-meta edits (`PATCH /api/v2/world`) never enter this feed.

## PIN (the world wall)

The PIN is a property of the **world's wall**, not of any dialect. Argon2-hashed on the server.

- **On writes**: required whenever the world has a PIN (both dialects).
- **On reads**: prefixed keys (`ow_w_`, `ow_r_`) always read without a PIN. Only a legacy 10-digit key reading a private world needs it.

Send it as the `API-Pin` header alongside `API-Key`, from `$ONLYWORLDS_API_PIN`. On a prefixed-key read it is ignored, so sending it there does no harm.

Wrong PINs are throttled per key: after 3 failures each retry must wait longer, and 10 failures lock the key for 15 minutes (`429 rate_limited` with a `Retry-After` header).

## Error Handling

The API reports errors honestly: it names the field or credential at fault. **Read the envelope; don't guess.** v2 and /bulk use a Stripe-style envelope; each error carries a `doc_url` into `onlyworlds.github.io/api/errors#<code>`.

**v2 / bulk error envelope:**
```json
{ "error": {
    "type": "invalid_request",
    "code": "invalid_link",
    "message": "friends references Character '…' which does not exist in this world or among the batch's surviving items.",
    "param": "friends",
    "doc_url": "https://onlyworlds.github.io/api/errors#invalid_link"
} }
```

| Situation | What you get (v2 / bulk) | Fix |
|-----------|--------------------------|-----|
| Bad / missing key, or wrong PIN | `401` `authentication_error` / `invalid_credentials`, `"No valid API-Key."` or `"Incorrect PIN."` | Check API-Key; on a write send the right API-Pin |
| Revoked key | `401` `key_revoked` | Get a new key (Account → your world → API keys) |
| Read-only key on a write route | `403` `permission_error` | Use an `ow_w_` key for writes |
| Element not found | `404` `not_found` | Check the type slug and UUID |
| Malformed id in the path | `422` `"id must be a UUID."` | Send a full UUID |
| Unknown field (typo, or v1 `_ids` suffix on v2) | `422` `invalid_request`, `"Unknown field: friends_ids"`, `param` names it | Use the bare canonical field name (no `_ids` in v2) |
| Text too long | `422` `"{field} must be at most {cap} characters"` | Shorten it: `name` 255, `supertype`/`subtype` 128, `image_url` 1024 |
| Unknown query param | `422` `"Unknown query parameter: X"` | Use a listed param (`since`, not `cursor`, on `/changes`) |
| Dangling link (target UUID doesn't exist) | `400` / per-item `invalid_link`, message names the field + missing target | Point at a real UUID, or include the target in the same batch |
| POST of an id that already exists | `409` `id_conflict` | Use PUT to upsert |
| Idempotency-Key reused with a different body | `409` `idempotency_error` | Send the changed body under a new key |
| Bad bulk shape | `422` `"items must be an array."` | Top-level key must be `items`, each entry `{type, element}` |
| Too many wrong PINs on this key | `429` `rate_limited`, `Retry-After` header | Fix the PIN and wait `Retry-After` seconds (up to 15 min). Retrying sooner does not help |

**These are honest errors: nothing is silently dropped.** An unknown field is rejected (not ignored), a dangling link is rejected (not nulled), a write without the right PIN is rejected (not partially applied). If a write returns `2xx`, the fields you sent are the fields that landed, but still verify (Critical Rule 2).

## Schema Notes

Some links are one-directional. Ability has no `characters` field: link via `Character.abilities`. Law has no `institutions` field: use `Law.author`. See `knowledge/schema-reference.md` "Link Direction Summary" for the full table. (In v2, all link fields are the bare name holding UUIDs; the direction table tells you which side owns the link.)

### MCP Server

OnlyWorlds also runs an MCP server at `https://www.onlyworlds.com/mcp` (11 tools: schema, read and write; no delete tool). The connect command and tool list are in `knowledge/onlyworlds-core.md`.

---

## Classic API (v1)

The legacy `/api/worldapi/` dialect (older tools only) and its traps: `references/v1-classic.md`.
