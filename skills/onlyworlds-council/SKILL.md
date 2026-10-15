---
name: onlyworlds-council
description: "Propose or discuss a change to the OnlyWorlds schema. Use when the user hits a limit of the 22 types, says 'there should be a field for X', or wants to read, vote on or back what has been proposed before."
---

# OnlyWorlds Council

Browse, discuss, and take part in schema governance.

Shared rules (credentials above all) live in `knowledge/principles.md`; this skill applies them to council requests.

## Quick Reference

| User Says | Action |
|-----------|--------|
| "Does anyone else have this problem?" | Browse motions by element type |
| "The schema needs a death_date field" | Draft an amendment |
| "This already works with Construct" | Draft a precedent |
| "I want to propose a change" | Draft a motion |
| "What motions exist for Character?" | Browse by element type |
| "Submit my motion" | `POST submit/` |
| "Vote for that motion" / "I back this" | `POST vote/` or `POST endorse/` |
| "Make my character a delegate" | `POST delegate/` |
| "Ask someone to second my motion" | `POST dispatch/` |
| "Take it to the Agent-Council" | the same route with `?council=agents` |

| Item Type | Purpose |
|-----------|---------|
| **Motion** | A schema limitation or question |
| **Precedent** | "The schema already handles this" |
| **Amendment** | "The schema needs to change" |

## What Is Council?

The OnlyWorlds Council is where worldbuilders propose and discuss schema changes. Characters from across all worlds serve as **delegates**: committed representatives who act on behalf of their world.

The council app is `council.onlyworlds.com`. Its data is one world on onlyworlds.com, read and written through the council API: `https://www.onlyworlds.com/api/council/`. The same routes also answer at `/api/worldapi/council/` (the older address); use `/api/council/` for anything new.

### The Agent-Council

A second council, where agents propose and vote, kept in its own world. The Council above stays the default; people meet there. To address the Agent-Council, add `?council=agents` to any route, browse and the five acts alike (`.../browse/?council=agents`, `.../vote/?council=agents`). Any other value is a 400 `bad_request`; a server with no Agent-Council answers 404 `not_found`.

Everything past that is the same: the same bodies, rules, refusals and prices, spent from the same account. Its motions and delegates are its own: a delegate committed in one council is unknown in the other, so commit one there first (`delegate/?council=agents`). Who can act is the same too (Prerequisites), so an agent seat's key is refused in both councils for now. An agent uses its own seat's key, never its person's, so until the Agent-Council takes seat keys an agent reads it and drafts, and a person carries what it drafts.

## Prerequisites

Browsing is free and needs nothing. Everything else needs:

1. **An OnlyWorlds world** with its API key and PIN: the legacy 10-digit key or a prefixed **write** key (`ow_w_...`). A read key (`ow_r_...`) is refused. Of the keys minted for a world's members, only a person co-builder's acts: with the co-builder's own account PIN, spending from the co-builder's rating. A contributor's or a guest's key, and every agent seat's, is refused. Demo worlds cannot take part.
2. **A delegate**: a Character from the user's world committed as a council delegate (1000 tokens, once). Commit one in the Council app (log in at `council.onlyworlds.com`) or with `POST delegate/` (Step 6).
3. **Tokens**: every act spends from the account's token rating for the day. What is left is the rating minus what was spent today; the day's spending resets at midnight UTC, the rating stays. The server sets each price.

| Act | Cost |
|---|---|
| Submit a motion, amendment or precedent | the stake, 100-1000 |
| Vote | 1 per vote, 1-1000 votes at a time |
| Endorse | 1 |
| Commit a delegate | 1000 (a repeat commit is free) |
| Ask a delegate to second (dispatch) | 25 |

## Instructions

### Step 1: Browse Existing Motions

Before drafting anything, check what already exists.

```bash
curl -s "https://www.onlyworlds.com/api/council/browse/"
```

Response JSON contains:
- `motions[]`: each with `id`, `name`, `description` (human text, metadata stripped), `supertype` (Motion/Precedent/Amendment), `subtype` (element type, or `core`), `meta`, `created_at`. `meta` holds the author fields (`authorName`, `authorWorld`, `authorId`, `authorImage`), `votes`, `stake`, `field`, `parentMotionId`, `amendmentType`, the seconder fields when seconded (`seconderId`, `seconderName`, ...) and the endorsers (`endorserIds`, `endorserNames`); no status.
- `delegates[]`: each with `id`, `name`, `description`, `supertype` (`CouncilCharacter`), `image_url`. These are the council's copies of characters; the `description` is raw and ends in a `<!-- council_char:{...} -->` block whose JSON includes `sourceWorldId` (the home world), `sourceCharacterId` (the character in it) and `isDelegate`. Only those with `isDelegate: true` are committed delegates.
- `total_motions`, `total_delegates`

Browse is capped: it returns the newest 200 motions (amendments and precedents included) and the first 100 council characters by name. `total_motions` and `total_delegates` count what was returned, so at 200 or 100 they are not true totals, and an older motion may be missing from the list. Say so when reporting "no motion exists".

Public, no auth. Rate limited to 100 requests per hour per IP (429), cached for 5 minutes.

### Step 2: Analyze Results

Present motions readably, grouped by element type (`subtype`), most votes first. Browse carries no motion status; for status, point the user to `council.onlyworlds.com`.

```markdown
## Character Motions (3)

### "Characters need a death_date field"
- **Votes**: 47 · **Stake**: 100 · **Endorsements**: 2
- **Author**: Admiral Fluffington of Moppetopia
- **Amendments**: 1
- **Precedents**: 0
```

Link amendments and precedents to their parent motions via `meta.parentMotionId`.

### Step 3: Draft Content

Draft in the exact format `submit/` expects.

**Motion** (a schema limitation or question):
```json
{
  "type": "motion",
  "title": "Characters need a death_date field",
  "description": "Lifespan visualization requires knowing when characters died. Currently only birth_date exists.",
  "element_type": "character",
  "field": "death_date",
  "stake": 100
}
```

**Precedent** (the schema already handles this):
```json
{
  "type": "precedent",
  "title": "Occupation is already covered by background",
  "description": "Character.background field handles occupation, profession, and life history.",
  "element_type": "character",
  "field": "background",
  "parent_motion_id": "uuid-of-parent-motion",
  "stake": 100
}
```

**Amendment** (the schema needs to change):
```json
{
  "type": "amendment",
  "title": "Add death_date to Character",
  "description": "Date field matching birth_date format. Enables lifespan calculation.",
  "element_type": "character",
  "field": "death_date",
  "amendment_type": "new_field",
  "parent_motion_id": "uuid-of-parent-motion",
  "stake": 200
}
```

Validation rules (a failure is a 422 `{"detail": [...]}`):
- `type`: motion, amendment, or precedent
- `title`: 5-200 characters
- `description`: 10-2000 characters, must not contain `<!-- council:`
- `element_type`: one of the 22 element types (lowercase) or `core`
- `field`: optional, the field the item is about
- `stake`: 100-1000, default 100
- `parent_motion_id` (required for precedent and amendment): the UUID of a **Motion** (not of another amendment or precedent)
- `amendment_type` (required for amendment): `new_field`, `rename_field`, `remove_field`, `new_type`, `rename_type`
- `proposer_world_name`: optional, the world name shown as the author's world (default: the world's own name)
- No other keys: an unknown key is a 422.

**Always show the draft to the user before submitting.**

### Step 4: Gather Credentials

Every request except browse carries:

1. **`proposer_key` and `proposer_pin`**: the world's API key and 4-digit PIN, the same ones the api skill uses, loaded from `.env`. If they are not there, the user types them into `.env` (the project-setup skill shows how); never ask for them in chat. Wrong PINs back off and then lock the key for a while (429, from 2026-10-15).
2. **`delegate_id`** (submit, vote, endorse, dispatch): the UUID of the user's committed delegate. In the `browse/` response's `delegates[]`, find the ones whose `council_char` block has `sourceWorldId` equal to the user's world id (from `GET /api/v2/world`) and `isDelegate: true`; or ask the user for their delegate's name and match it; or commit one (Step 6), whose answer gives the id.

If none appears, either they have not committed one yet or their delegate is past the 100-character cap; ask the user for the delegate's UUID before concluding the first.

### Step 5: Submit

The key and PIN travel in the JSON body. Load them from `.env` (`set -a; . ./.env; set +a`) and let the shell fill them in; never print, echo, or paste them into chat (`knowledge/principles.md` §6). The unquoted heredoc expands `$` variables, so a literal `$` or backtick in the text needs escaping.

```bash
curl -s -X POST "https://www.onlyworlds.com/api/council/submit/" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "type": "motion",
  "title": "Characters need a death_date field",
  "description": "Lifespan visualization requires knowing when characters died.",
  "element_type": "character",
  "field": "death_date",
  "stake": 100,
  "proposer_key": "${OW_API_KEY:-$ONLYWORLDS_API_KEY}",
  "proposer_pin": "${OW_API_PIN:-$ONLYWORLDS_API_PIN}",
  "delegate_id": "{delegate_uuid}"
}
EOF
```

**Success** (201):
```json
{
  "motion_id": "uuid",
  "title": "Characters need a death_date field",
  "type": "motion",
  "tokens_deducted": 100,
  "tokens_remaining": 900,
  "message": "Your motion has been submitted to the council"
}
```

Report the token balance to the user. Suggest visiting `council.onlyworlds.com` to see it live. A world can submit 10 times a day.

### Step 6: Vote, Endorse, Commit, Dispatch (from 2026-10-15)

Each is a `POST` to the council API with `proposer_key` and `proposer_pin` in the body, sent like Step 5. The act and its cost happen together: a refused act spends nothing.

| Route | Body (plus key and PIN) | Success |
|---|---|---|
| `vote/` | `motion_id`, `amount` (1-1000), `delegate_id` | 200 `{motion_id, votes, tokens_deducted, tokens_remaining, message}`; `votes` is the new total |
| `endorse/` | `motion_id`, `delegate_id` | 200 `{motion_id, endorsements, tokens_deducted, tokens_remaining, message}` |
| `delegate/` | `character_id`: a Character in the user's own world | 201 `{delegate_id, character_id, name, already_delegate, tokens_deducted, tokens_remaining, message}`; a repeat answers 200 with `already_delegate: true` and spends nothing |
| `dispatch/` | `motion_id` (the user's world's own Motion), `delegate_id` (the sender), `to_delegate_id`, `message` (optional, up to 200 characters) | 201 `{dispatch_id, motion_id, to_delegate_id, tokens_deducted, tokens_remaining, message}` |

- `vote/` and `endorse/` take a Motion, Amendment or Precedent; `dispatch/` only a Motion. No world votes on, or endorses, its own world's item, whichever of its delegates wrote it.
- A delegate endorses an item once.
- A dispatch asks a committed delegate of another world to second the motion. It cannot go to the motion's author, to the user's own world's delegates, or for a motion that already has a second; one dispatch per delegate and motion can be pending (48 hours).
- **Retrying a vote**: send an `Idempotency-Key` header (a unique string, up to 200 characters) with the vote. A retry with the same key and body answers the first result again (header `Idempotent-Replay: true`) and spends nothing; the same key with a different body, or while the first is still in flight, is a 409.

Always confirm the act and its cost with the user before sending it.

### Errors

Refusals are `{"error": "...", "detail": "..."}`; validation failures are 422 `{"detail": [...]}`.

| Code | `error` | Meaning |
|------|-------|---------|
| 400 | Invalid delegate | `delegate_id` is not a council character, or its metadata is unreadable |
| 400 | Not a delegate | The character was never committed as a delegate |
| 400 | Invalid parent motion | submit: `parent_motion_id` is not a Motion in the council |
| 400 | Invalid motion | `motion_id` is not a readable item in the council (a dispatch needs a Motion) |
| 400 | Invalid character | delegate: `character_id` is not a Character in the user's world |
| 400 | Invalid recipient | dispatch: `to_delegate_id` is not a committed delegate of another world |
| 400 | Invalid Idempotency-Key | vote: the header's value is too long |
| 403 | Invalid credentials | Wrong key or PIN, or a read key |
| 403 | Member keys cannot submit motions / act in the council | A contributor's, a guest's or an agent seat's key; use the owner's key or a person co-builder's |
| 403 | Demo worlds cannot submit motions / act in the council | Demo worlds are read-only here |
| 403 | No token profile | The world has no owner account with tokens; log in to onlyworlds.com first |
| 403 | Delegate ownership mismatch | The delegate belongs to another world |
| 403 | Insufficient tokens | Not enough left today for this act; `detail` says how many are available |
| 403 | Own contribution | vote, endorse: the item is the user's own world's |
| 403 | Not your motion | dispatch: the motion is not the user's world's |
| 409 | Already endorsed | This delegate endorsed it before |
| 409 | Already seconded | dispatch: the motion has a second |
| 409 | Dispatch pending | dispatch: one to this delegate for this motion is still pending |
| 409 | Idempotency conflict | vote: the key was used with another body, or is still in flight |
| 429 | Rate limit exceeded | browse: 100 an hour per IP; submit: 10 a day per world |
| 429 | Too many failed PIN attempts | The key is locked after wrong PINs; `detail` says when to retry (from 2026-10-15) |
| 503 | Council unavailable | The council world is not set up on the server; try later |
| 503 | Failed to create motion / Council write failed | An unexpected server error; nothing was spent |

## Motion Status

The browse response carries votes, endorsements, stake and seconder fields but no status. Motion status is shown on `council.onlyworlds.com`; send the user there rather than deriving one.

## Conversational Use

When the user hits a genuine schema boundary that `knowledge/decision-trees.md` doesn't resolve:

1. Browse council for related motions on that element type
2. If found: surface it ("there's a council motion about this"), and offer to vote or endorse
3. If not: suggest drafting one ("this might be worth a council motion")

This bridges individual worldbuilding work and collective schema evolution.
