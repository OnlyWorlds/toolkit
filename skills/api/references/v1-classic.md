# Classic API (v1 dialect), legacy

The v1 dialect (`/api/worldapi/…`) keeps working indefinitely. You'll meet it in **older tools and existing integrations** written before the platform rebuild. Prefer v2 for anything new; if you're maintaining v1 code, these are its traps.

**Base URL**: `https://www.onlyworlds.com/api/worldapi/{type}/`. Same `API-Key` / `API-Pin` headers.

**v1 gotchas that don't exist in v2:**

1. **Trailing slash is mandatory on singular GET.** `GET /api/worldapi/character/{uuid}` (no slash) → `301` redirect with an empty body; curl/requests don't auto-follow, so it looks like a failure. **Always add the trailing slash**: `/api/worldapi/character/{uuid}/`. (v2 doesn't care either way.)

2. **No pagination: the full array dumps at once.** `?limit=` is silently ignored; a list endpoint returns every element as a **plain JSON array** (no `{data, has_more, …}` envelope). Fine for small worlds, memory-heavy for large ones. (v2 paginates properly.)

3. **`_ids` / `_id` write-suffix, expanded read.** This is the split that bites hardest when moving between dialects:
   - **Write** (POST/PATCH): link fields need a suffix: `_id` for single (`location_id`), `_ids` for multi (`species_ids`, `friends_ids`).
   - **Read** (GET): the field comes back under its **bare name** as **nested expanded objects**: `"species": [{"id": "…", "name": "Puddle Moppet", …}]`, not raw UUIDs.
   - So v1 read shape ≠ v1 write shape, and *neither* matches v2 (which is flat UUIDs, bare names, both directions). Sending `friends_ids` to v2/bulk is a `422`; sending `friends` (bare) as a v1 *write* is likewise rejected as an unknown field (v1 answers with an honest `422` too), so send the suffixed form on v1.

**v1 endpoints:** `GET/POST /api/worldapi/{type}/`, `GET/PATCH/DELETE /api/worldapi/{type}/{uuid}/` (trailing slash!). Names singular, same as v2. v1 serves no PUT; use v2 `PUT /api/v2/{type}/{uuid}`.

**v1 error envelope** is the legacy shape, not Stripe-style: `{"detail": "Unauthorized", "error": {"code": "unauthorized", …}}` for auth, or a list of ninja `value_error` entries for validation. It still reports honestly: an unknown field on v1 now returns `422 "Unknown field 'X'. Check spelling…"`, and a dangling link returns `400 "Invalid FK: {field} — referenced {Type} with id '…' does not exist."` (v1 no longer silently drops unknown fields or nulls dangling links; that old behavior is gone on both dialects.)

**Still true on both dialects:** must use `www.onlyworlds.com` (bare domain redirect behavior differs); header names are exact (`API-Key`, `API-Pin`; `Pin` or `X-Api-Key` fail with `401`, while casing does not matter); read-before-PATCH; PIN rules as in `../SKILL.md`.
