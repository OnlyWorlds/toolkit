---
name: onlyworlds-api
description: Interact with the OnlyWorlds REST API — fetch, create, update, delete, or bulk-upload world elements. Use when the user wants to query their world, upload parsed data, browse existing elements, or perform any API operations. Prefer this skill over raw curl for all API work — provides credential handling, error patterns, and dialect guidance. Requires an API-Key header (and API-Pin for walled worlds / all writes). Base URL: onlyworlds.com/api/v2/. Teaches v2 (modern) and /bulk; a legacy section covers the v1 "classic" dialect for older tools.
---

# OnlyWorlds API

Read and write world data via the OnlyWorlds REST API.

**Teach v2.** Every fresh example here uses `/api/v2/` and `/api/v2/bulk`. The v2 surface returns real pagination, flat UUID link arrays, native creates, and honest Stripe-style errors that name the problem. The older v1 "classic" dialect still serves forever, but it has traps v2 doesn't — it lives in one clearly-marked [Classic API section](#classic-api-v1-dialect--legacy) at the end. If you're writing new code, stay in v2.

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
| Delete element | DELETE | `/api/v2/{type}/{uuid}` |
| **Bulk upsert (standard upload path)** | POST | `/api/v2/bulk` |
| Sync changes since cursor | GET | `/api/v2/changes` |
| Field descriptors for a type | GET | `/api/metadata/{type}/` |

**Endpoint names are SINGULAR** — `/character`, `/location`, `/institution`. NOT plural.

**Link fields are FLAT UUID arrays, both directions** — read AND write use the bare field name (`friends`, `species`, `objects`), holding raw UUID strings. There is no `_id`/`_ids` suffix in v2. (The suffix is a v1-only thing — see Classic section. Sending `friends_ids` to v2 or /bulk is a hard `422 Unknown field: friends_ids`, the #1 new-user error.)

## Critical Rules

1. **Read before PATCH.** PATCH *replaces* the fields you send — for link arrays and text fields, it does not merge. To add a link or append text, GET the current value first, build the full new value, then PATCH it. GET is cheap; overwriting an array with a partial one is permanent data loss.
2. **Verify after write.** GET the element back after a create or update and confirm the fields landed. Cheap insurance on any batch.
3. **/bulk is the standard upload path** for parse results. One request, mixed types, per-item results, idempotent retry. Don't loop hundreds of individual POSTs — see [Bulk Upload](#bulk-upload-standard-for-parse-results).
4. **Mint your own UUIDs on create.** IDs are UUIDv7 (time-sortable). Client-minted IDs let you reference an element you're creating in the *same* bulk batch (forward sibling refs are legal — no topological pre-sorting needed) and make retries idempotent. Generate a v7 UUID per element before upload.
5. **Read the error envelope.** The API now tells you exactly what's wrong (unknown field, dangling link, bad credentials) with a `code`, `message`, `param`, and `doc_url`. Don't guess — read the message. See [Error Handling](#error-handling).

## Safety Notice

Write operations can modify or delete world data.
- Check `.ow/config.json` for `last_backup` — if > 7 days, recommend a backup before major operations.
- Test with a small batch first.
- Read before PATCH (Critical Rule 1). Verify after write (Critical Rule 2).

## Instructions

### Step 1: Get Credentials

Check for `.ow/config.json` in the current directory first:

| Config Found | credential_mode | Action |
|-------------|----------------|--------|
| Yes | full | Load API-Key + API-Pin from `.env` |
| Yes | key-only | Load API-Key from `.env`, ask user for PIN |
| Yes | manual | Ask user for both |
| No | — | Ask user for both |

- **API-Key**: World-scoped key. May be a prefixed key (`ow_w_…` world-write, `ow_r_…` read-share) or a legacy 10-digit key (grandfathered forever; still valid, but no longer issued). Get one from world settings on onlyworlds.com.
- **API-Pin**: The world's PIN (Argon2 wall). Required on **every write**, and on **reads too if the world is walled**. Unwalled/demo worlds read without a PIN. See [PIN](#pin-the-world-wall).

(A third credential exists for account-level automation: **account tokens** (`ow_a_…`, minted in the portal under Settings → Account, sent as `Authorization: Bearer` on `/api/v2/account/…` routes) — they list/create worlds and mint fresh world keys. Normal element work never needs one.)

**World meta**: `PATCH /api/v2/world` updates the world's own fields (description, image_url, time settings) with the same key+PIN — partial like element PATCH, and an unknown field rejects the whole request.

### Step 2: Validate + Fetch World Info

```bash
curl -s "https://www.onlyworlds.com/api/v2/health"
# → {"status": "ok", "service": "keel"}

curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If credentials are bad you get a `401` with a Stripe-style envelope naming the problem (`invalid_credentials`) — read it rather than re-guessing.

### Step 3: Perform Operations

## API Operations (v2)

### List Elements

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}?limit=100" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

**Response is enveloped and paginated:**
```json
{ "data": [ {...}, {...} ], "has_more": true, "next_cursor": "eyJzIjog..." }
```

- `data` — array of element objects for this page.
- `has_more` — whether more pages exist.
- `next_cursor` — opaque base64 token. Treat it as opaque (don't parse it). To get the next page, pass it back:

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}?limit=100&cursor={next_cursor}" \
  -H "API-Key: {api_key}" -H "API-Pin: {api_pin}"
```

Loop, following `next_cursor`, until `has_more` is `false`.

**Element types** (lowercase, singular): character, creature, species, family, collective, institution, location, zone, map, pin, marker, object, construct, title, ability, trait, language, law, event, narrative, phenomenon, relation

**Filtering**:
- `?name__icontains=value` — filter by name (case-insensitive partial match)
- `?supertype=value` — filter by supertype category

**Link fields in v2 responses are flat UUID arrays**: `"species": ["0698c9df-…"]`, `"friends": ["uuid", "uuid"]`. Plain UUID strings, same names as you write. (v1 expands these into nested `{id, name, …}` objects — see Classic section.)

### Get Element

```bash
curl -s "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: {api_key}" -H "API-Pin: {api_pin}"
```

Returns the **bare element object** (not enveloped — no `data` wrapper on a singular GET). The trailing slash is optional on v2 (it works with or without).

### Create Element

```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/{type}" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{"id": "{your-uuidv7}", "name": "Element Name", "description": "...", "friends": ["{uuid}"]}'
```

Returns `200` with the flat element object, including echoed `created_at`/`updated_at` (ISO-8601 UTC). Mint the `id` yourself (Critical Rule 4) so you can reference it elsewhere and so retries are safe. Link fields use bare names holding UUID arrays.

### Update Element (PATCH)

```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

**PATCH replaces the fields you send.** To append to `description` or add to a link array, GET the current value first, combine, then send the full result (Critical Rule 1).

### Delete Element

```bash
curl -s -X DELETE "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: {api_key}" -H "API-Pin: {api_pin}"
```

Returns `204 No Content`. (A `000` curl status is a dropped connection, not a server verdict — retry it.)

## Bulk Upload (standard for parse results)

`POST /api/v2/bulk` is the standard path for uploading parsed elements. One request, mixed element types, structured per-item results, idempotent retry. **No topological sorting needed** — an element may reference a sibling created later in the same batch (forward refs are legal).

**Request shape** — note the key is `items` (not `operations`), and each item wraps an `op`, a `type`, and the `element`:

```json
{
  "items": [
    { "op": "upsert", "type": "location", "element": { "id": "{uuid-A}", "name": "Feltropolis" } },
    { "op": "upsert", "type": "character", "element": { "id": "{uuid-B}", "name": "Admiral Fluffington", "location": "{uuid-A}" } }
  ]
}
```

```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/bulk" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: {a-uuid-for-this-batch}" \
  -d @batch.json
```

**Response** — enveloped, per-item:
```json
{
  "errors": false,
  "items": [
    { "status": 201, "id": "{uuid-A}", "created_at": "...", "updated_at": "..." },
    { "status": 201, "id": "{uuid-B}", "created_at": "...", "updated_at": "..." }
  ]
}
```

- Top-level `errors` — `true` if *any* item failed. Committed items still land; failed items are reported per-item with a structured `error` (see below). The batch is not all-or-nothing at the response level, so scan every item's `status`.
- Each item echoes its `id` (even on failure) plus `created_at`/`updated_at` on success.

**Idempotency-Key retry pattern**: set an `Idempotency-Key` header (a UUID you pick for the batch). If the request times out or the connection drops, resend the *identical* body with the *same* key — the server replays the original result instead of double-creating. A replayed response carries an `idempotent-replay: true` header and identical timestamps. This makes bulk uploads safe to retry blindly.

**Link fields in /bulk use flat bare names** (`friends`, `location`) holding UUIDs — same as v2, never the `_ids` suffix.

### Upload a parse: recommended flow

1. Mint a UUIDv7 for every element up front (Critical Rule 4).
2. Build one `items` array — all types, links already pointing at your minted UUIDs (forward refs are fine).
3. POST to `/api/v2/bulk` with an `Idempotency-Key`.
4. Scan the response: if `errors: true`, read each failing item's `error.message`/`param`, fix, and resend (the same key replays successes harmlessly).
5. Spot-check with a GET (Critical Rule 2).

No two-pass dance is needed on v2 — the batch resolves sibling links itself.

## Sync Changes

`GET /api/v2/changes` returns everything that changed since a cursor — the basis for incremental sync.

```bash
curl -s "https://www.onlyworlds.com/api/v2/changes" \
  -H "API-Key: {api_key}" -H "API-Pin: {api_pin}"
```

```json
{
  "cursor": "1:069ae78f-…",
  "changes": [
    { "op": "upsert", "type": "location", "id": "…", "change_seq": 1, "updated_at": "…", "element": { …full element… } }
  ]
}
```

Store `cursor` and pass it back next time (`?cursor=…`) to get only newer changes. **This cursor is a plain `"<change_seq>:<uuid>"` string** — a different mechanism from the base64 list-pagination cursor. Don't conflate the two.

## PIN (the world wall)

The PIN is a property of the **world's wall**, not of any dialect. Argon2-hashed on the server. A world with a wall requires the PIN:

- **On writes**: always (both dialects, walled or not — writing always demands the PIN on a walled world).
- **On reads**: only if the world is walled. Walled world + no PIN → `401`. Unwalled/demo worlds read with the key alone.

Send it as the `API-Pin` header alongside `API-Key`. When in doubt, send it — it's never wrong to include on a walled world.

## Error Handling

The API reports errors honestly — it names the field or credential at fault. **Read the envelope; don't guess.** v2 and /bulk use a Stripe-style envelope; each error carries a `doc_url` into `onlyworlds.github.io/api/errors#<code>`.

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
| Bad / missing key | `401` `authentication_error` / `invalid_credentials`, `"No valid API-Key."` | Check API-Key; on a walled world send API-Pin too |
| Unknown field (typo, or v1 `_ids` suffix on v2) | `422` `invalid_request`, `"Unknown field: friends_ids"`, `param` names it | Use the bare canonical field name (no `_ids` in v2) |
| Dangling link (target UUID doesn't exist) | `400` / per-item `invalid_link`, message names the field + missing target | Point at a real UUID, or include the target in the same batch |
| Bad bulk shape | `422` `"items must be an array."` | Top-level key must be `items`, each entry `{op, type, element}` |
| Rate limited | `429` | Add a small delay between requests (~1s is comfortable) |

**These are honest errors — nothing is silently dropped.** An unknown field is rejected (not ignored), a dangling link is rejected (not nulled), a walled read without a PIN is rejected (not partially served). If a write returns `2xx`, the fields you sent are the fields that landed — but still verify (Critical Rule 2).

## Schema Notes

Some links are one-directional. Ability has no `characters` field — link via `Character.abilities`. Law has no `institutions` field — use `Law.author`. See `../../knowledge/schema-reference.md` "Link Direction Summary" for the full table. (In v2, all link fields are the bare name holding UUIDs — the direction table tells you which side owns the link.)

### MCP Server

For MCP clients (Claude Code, Claude Desktop, the API connector), OnlyWorlds runs an MCP server at **`https://www.onlyworlds.com/mcp`** — modern MCP over streamable HTTP, stateless. It's a separate integration path from raw REST: instead of curl you get 11 tools.

```bash
claude mcp add --transport http onlyworlds https://www.onlyworlds.com/mcp \
  --header "API-Key: <your key>" --header "API-Pin: <your pin>"
```

- **3 schema tools** (`list_element_types`, `get_element_schema`, `search_schema`) work with **no key**.
- **4 read tools** (`list_elements`, `get_element`, `search_elements`, `get_changes`) and **4 write tools** (`create_element`, `update_element` — server-side read-merge; `edit_links` — additive/subtractive; `bulk_apply`) need the key (and PIN for writes / walled reads).
- **No delete tool** by design — deletion stays on REST (`DELETE /api/v2/{type}/{uuid}`) and the portal.

The claude.ai **web** connector isn't supported in v1 (OAuth-only UI); header keys work in Claude Code / Desktop / the API connector. The old `@onlyworlds/mcp-client` npm package and `/mcp/messages/` endpoint are legacy. Full detail in `../../knowledge/onlyworlds-core.md`.

---

## Classic API (v1 dialect) — legacy

The v1 dialect (`/api/worldapi/…`) still serves and will for years. You'll meet it in **older tools and existing integrations** written before the platform rebuild. Prefer v2 for anything new — but if you're maintaining v1 code, these are its traps.

**Base URL**: `https://www.onlyworlds.com/api/worldapi/{type}/`. Same `API-Key` / `API-Pin` headers.

**v1 gotchas that don't exist in v2:**

1. **Trailing slash is mandatory on singular GET.** `GET /api/worldapi/character/{uuid}` (no slash) → `301` redirect with an empty body; curl/requests don't auto-follow, so it looks like a failure. **Always add the trailing slash**: `/api/worldapi/character/{uuid}/`. (v2 doesn't care either way.)

2. **No pagination — the full array dumps at once.** `?limit=` is silently ignored; a list endpoint returns every element as a **plain JSON array** (no `{data, has_more, …}` envelope). Fine for small worlds, memory-heavy for large ones. (v2 paginates properly.)

3. **`_ids` / `_id` write-suffix, expanded read.** This is the split that bites hardest when moving between dialects:
   - **Write** (POST/PATCH): link fields need a suffix — `_id` for single (`location_id`), `_ids` for multi (`species_ids`, `friends_ids`).
   - **Read** (GET): the field comes back under its **bare name** as **nested expanded objects**: `"species": [{"id": "…", "name": "Puddle Moppet", …}]` — not raw UUIDs.
   - So v1 read shape ≠ v1 write shape, and *neither* matches v2 (which is flat UUIDs, bare names, both directions). Sending `friends_ids` to v2/bulk is a `422`; sending `friends` (bare) as a v1 *write* silently means the link (it's an unknown write field on v1 — send the suffixed form on v1).

**v1 endpoints:** `GET/POST /api/worldapi/{type}/`, `GET/PATCH/PUT/DELETE /api/worldapi/{type}/{uuid}/` (trailing slash!). Names singular, same as v2.

**v1 error envelope** is the legacy shape, not Stripe-style: `{"detail": "Unauthorized", "error": {"code": "unauthorized", …}}` for auth, or a list of ninja `value_error` entries for validation. It still reports honestly — an unknown field on v1 now returns `422 "Unknown field 'X'. Check spelling…"`, and a dangling link returns `400 "Invalid FK: {field} — referenced {Type} with id '…' does not exist."` (v1 no longer silently drops unknown fields or nulls dangling links — that old behavior is gone on both dialects.)

**Still true on both dialects:** must use `www.onlyworlds.com` (bare domain redirect behavior differs); header casing is exact (`API-Key`, `API-Pin`); read-before-PATCH; PIN rules as above.
