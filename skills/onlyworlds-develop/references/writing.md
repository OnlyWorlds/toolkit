# Writing to a world

What a write needs: the rules, the PIN, create, PATCH, links, delete, pictures, bulk upload, the errors a write meets and the Blocked page.
Open it before the first write to a world; its examples use `$B`, `$K` and `${W[@]}` from the `.env` block in `../SKILL.md`, Credentials.

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

- **API-Pin**: on every write. The owner writes with their account PIN (Account → Settings → World PIN: one for every world they own); a member of someone else's world with their own account PIN; an AI seat with its seat secret (`ow_s_…`). See [PIN](#pin-the-world-wall).
- **X-OW-Agent**: as an AI agent, send `X-OW-Agent: 1` on every write (create, PUT, PATCH, DELETE, links, bulk), so your writes are recorded as agent-made (`changed_via: declared`); only its presence counts. A seat's key and the MCP server count as agents without it. Code for a person's app leaves it off ([Step 4](building.md#step-4-credential-handling)).
- **Account tokens** (`ow_a_…`, Account settings → Account tokens, sent as `Authorization: Bearer`) serve the `/api/v2/account/…` routes, and also read a world named by `world=<id>`: its elements, search, field metadata and the world itself, as the account may read it (the whole world if it is theirs, their own view as a member, what the public reads otherwise). A token never writes an element: writes take a world key and its PIN.
- **No account yet**: the practice world's key and PIN are published on the docs' [Keys page](https://onlyworlds.github.io/docs/getting-started/keys.html#the-practice-world), shared by everyone. It is a copy of Moppetopia under its own ids, reset to that copy every night at 03:00 UTC, and anyone holding the key reads what you write: put nothing private in it. It takes no files, members or seats, holds 2,000 elements at most, and counts 60 requests a minute per address, not per key.

## Create Element

```bash
curl -s -X POST "$B/{type}" "${W[@]}" \
  -d '{"id": "{your-uuid}", "name": "Element Name", "description": "...", "friends": ["{uuid}"]}'
```

Returns `201` with the element. POSTing an id that exists is `409 id_conflict`; `PUT $B/{type}/{uuid}` upserts (201 created, 200 replaced), replacing the whole element. An `Idempotency-Key` header works here too.

## Update Element (PATCH)

`curl -s -X PATCH "$B/{type}/{uuid}" "${W[@]}" -d '{"description": "Updated"}'`

**PATCH replaces the fields you send** (Critical Rule 1); for multi-link arrays use the links route.

**Extension fields** (`x_*`, `atlas_*`, `shadow_*`, principles §4) are stored verbatim and returned on v2 reads. PATCH merges extension keys (omitting one keeps it); PUT, and a /bulk item with an existing id, replace the whole element, extension fields included; v1 does not return them.

**Base fields**: `world` is ignored on write (the key decides). Numbers are integers in the world's units; a fraction is truncated. Ranges are advisory: out-of-range values are stored, so tools clamp.

## Add or Remove Links

```bash
curl -s -X POST "$B/{type}/{uuid}/links/{field}" "${W[@]}" -d '{"add": ["{uuid}"], "remove": ["{uuid}"]}'
```

Atomic server-side merge on one multi-link field: `add` skips ids already present, `remove` ignores ids not present, and each added target must exist (`invalid_link` otherwise). Returns the updated element. A single-link or unknown field is a `422`.

**Some links are one-directional**: Ability has no `characters` (link from `Character.abilities`), Law no `institutions` (use `Law.author`). Which side owns each link, and every type's fields: the model skill.

## Delete Element

`curl -s -X DELETE "$B/{type}/{uuid}" "${W[@]}"` returns `204`. (A `000` curl status is a dropped connection: retry.) Delete is rarely right: it also strips the element from every link to it. Retire what died, left or ended (principles §2); delete only what a human approved.

## Pictures and Files

A picture is an element's `image_url`. `POST $B/media/ticket` (a write key and its PIN, no body) answers a single-use `ticket` and its `upload_url`; POST the image's raw bytes there with `Authorization: Bearer <ticket>` (webp, png, jpeg or avif, no SVG, at most the ticket's `max_bytes`), then PATCH the answer's `url` into `image_url`. The SDK's `uploadImage` does both. Each upload counts toward the world's daily limit and the account's image storage. [Images](https://onlyworlds.github.io/docs/development/api/images.html).

A file kept beside an element is at most 25 MB, and a world's files 250 MB in all. The SDK: `listFiles`, `uploadFile`, `fileDownloadLink`, `removeFile`, `worldFiles`.

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
- The element holds writable fields only: `type` belongs on the item, and `created_at`, `updated_at`, `change_seq` are rejected (422). There is no delete op.
- The body takes `items`, `atomic` and `create_only`, and an item takes `type` and `element`. Any other key on the body or an item (an `op`, say), any query parameter, or one of these names sent twice is a 422 for the whole request that names it, and nothing is written; a key inside `element` that is no field is that item's own 422.
- Max 1000 items per request. `"atomic": true` at the top level makes the batch all-or-nothing.
- `"create_only": true` at the top level makes an item with an `id` create and never replace: an item whose `id` is already held is refused (409 `id_conflict`) and nothing is written for it.

```bash
curl -s -X POST "$B/bulk" "${W[@]}" -H "Idempotency-Key: {a-uuid-for-this-batch}" -d @batch.json
```

The response is `{"errors": false, "items": [{"status": 201, "id": "{uuid-A}", ...}, ...]}`, in request order. `errors` is `true` if *any* item failed; without `atomic`, committed items still land and each failure carries a structured `error`, so scan every `status`. A failed item has `"id": null` when it sent none or failed a field check (an unknown field or type, a read-only field): match results to items by index.

**Idempotency-Key retry**: if the request times out or drops, resend the *identical* body with the *same* key: the server replays the original result (an `idempotent-replay: true` header) instead of double-creating, so a bulk upload is safe to retry blindly. The same key with a *different* body is `409 idempotency_error`: a corrected batch needs a new key. Keys are kept 24h.

### Upload a parse: recommended flow

1. Mint a UUID (v7 recommended) for every element up front (Critical Rule 4).
2. Build one `items` array: all types, links already pointing at your minted UUIDs.
3. POST to `/api/v2/bulk` with an `Idempotency-Key`.
4. If `errors: true`, read each failing item's `error.message`/`param`, fix those items, and resend under a **new** key (without `create_only`, full items with ids replace, so resending the ones that succeeded is harmless).
5. Spot-check with a GET (Critical Rule 2).

## PIN (the world wall)

The PIN is the **world's wall**, not a dialect's: on a world that has one, every write needs it. A person's PIN is Argon2-hashed on the server; an AI seat sends its own secret in its place. Prefixed keys read without it. A PIN sent on a read beside a key that can write is checked, and a wrong one is a 401 (an owner's key on any read, REST or MCP; a member's or an AI seat's on `GET /me` and `get_me`); beside a key that cannot write a PIN is never read. A legacy 10-digit key sends it on every read of a world that has a PIN, public or private (a demo-range key never does). A missing or empty PIN where one is needed is the 401 and is not counted. Every PIN that is checked is counted as it arrives, on the key and across every key of the account whose PIN it is (a world's PIN is its owner's; a member's own key counts on the member; a seat's secret on the seat's key alone, so a seat's **New key** starts its own count); a right PIN takes only itself back out, and the practice world counts nothing. Ten different wrong PINs within fifteen minutes, on one key or across the keys of the account whose PIN it is, close the PIN wall until the oldest of them is fifteen minutes old: every PIN sent there meanwhile, the right one too, on every one of those keys, a key made during the lock included, is answered `429 rate_limited` (`param` `API-Pin`, with `Retry-After`), and the same wrong PIN sent again counts once. A request that sends no PIN where none is checked (a prefixed key's read) is never refused by the wall.

## Errors

| You get | Fix |
|---|---|
| `422` `Unknown field: friends_ids`: a typo, or v1's `_ids` suffix; `param` names it | The bare canonical field name |
| `400` / per-item `invalid_link`: a link names a UUID that does not exist | A real UUID, or the target in the same batch |
| `409` `id_conflict`: POST of an id that exists, or a `create_only` bulk item whose id is held | An id you sent before: it may have landed, GET it first. Else a new id; PUT only when you mean to replace |
| `403` `not_author`: a contributor's or a guest's key changed, replaced, relinked or deleted an element someone else created | Change only what that key made, or ask a keeper |
| `403` with an HTML page titled "Blocked" and no JSON: the host in front of the platform refused the request before the platform saw it | Nothing was written. Reword the command the text holds ([the Blocked page](#the-blocked-page)), then send again |
| `412` `precondition_failed`: an `If-Match` change_seq the element has moved past; the reply's `current` is the element now | Nothing was written: re-read `current`, then re-send or ask the user |
| `413` `payload_too_large`: a body over 2.5 MB | Split a large /bulk into several calls |
| `409` `idempotency_in_flight`: a request with this Idempotency-Key is still running | Retry after `Retry-After`; the same key and body then replay its answer |
| `429` `rate_limited`: failed PINs, counted per key and per account ([PIN](#pin-the-world-wall)) | Wait `Retry-After` seconds; sooner does not help |

**These are honest errors: nothing is silently dropped.** An unknown field is rejected (not ignored), a dangling link rejected (not nulled), a write without the right PIN rejected (not partly applied). A `2xx` means what you sent landed; still verify. A `202` is not a write: it answers `{"proposal": …}` where the owner takes an AI seat's writes as proposals, and nothing changes until a keeper accepts.

### The Blocked page

One answer is not the envelope above: a `403` whose body is an HTML page titled "Blocked". The host in front of the platform sent it and the platform never saw the request, so nothing was written and no item of a /bulk landed.

Seen on 2026-11-16 on POST, PATCH and /bulk, in `name` and in `description`, when a text in the body had one of these directly after a backtick, a semicolon or a pipe (spaces or a line break between them change nothing): `python -m`, `python -c`, `perl -e`, `curl` or `wget` with a URL. Each was tried after a backtick; `python -m` and `curl` also after a semicolon and after a pipe. In Markdown the refused places are an inline code span, a fenced block with no language word, and a table cell. The list is what was tried, not the host's whole rule (`python` with other flags was refused once too), and the rule is the host's to change.

What passes: the command behind a prompt inside the code span (`$ python -m ...`); in a fenced block whose first line names a language; or in plain text with no backtick, semicolon or pipe just before it. Writing the backtick as a JSON escape does not pass.

To find the text in a large /bulk without writing anything, POST each item's JSON to a route that does not exist: an answer in JSON (a `404`) means the platform read it, the page means that item holds the text.

## The answer says

- Before a write session to an existing world, the export that is its rollback (Safety Notice).
- After a bulk upload, every item's `status` read, and each failure named by its index (Bulk Upload).
- Each write read back (Critical Rule 2; principles §5).
