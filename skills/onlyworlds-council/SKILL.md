---
name: onlyworlds-council
description: "Propose or discuss a change to the OnlyWorlds schema. Use when the user hits a limit of the 22 types, says 'there should be a field for X', or wants to read what has been proposed before."
---

# OnlyWorlds Council

Browse, discuss, and participate in schema governance.

Shared rules (credentials above all) live in `knowledge/principles.md`; this skill applies them to council submissions.

## Quick Reference

| User Says | Action |
|-----------|--------|
| "Does anyone else have this problem?" | Browse motions by element type |
| "The schema needs a death_date field" | Draft an amendment |
| "This already works with Construct" | Draft a precedent |
| "I want to propose a change" | Draft a motion |
| "What motions exist for Character?" | Browse by element type |
| "Submit my motion" | Submit via proxy endpoint |

| Item Type | Purpose |
|-----------|---------|
| **Motion** | A schema limitation or question |
| **Precedent** | "The schema already handles this" |
| **Amendment** | "The schema needs to change" |

## What Is Council?

The OnlyWorlds Council is where worldbuilders propose and discuss schema changes. Characters from across all worlds serve as **delegates**: committed representatives who submit motions on behalf of their world.

Council data lives at `council.onlyworlds.com`. The toolkit browses via a public proxy and submits via an authenticated one.

## Prerequisites for Submitting

Browsing is free. Submitting requires:

1. **An OnlyWorlds world** with an API key and PIN. Submission accepts either the legacy 10-digit numeric key or a prefixed **write** key (`ow_w_...`). A bare read key (`ow_r_...`) is rejected: submission needs write scope
2. **A delegate**: a Character from the user's world that has been committed as a council delegate at `council.onlyworlds.com` (costs 1000 tokens, one-time)
3. **Tokens**: each submission stakes 100-1000 tokens, deducted from the user's daily quota

If the user hasn't committed a delegate yet, direct them to `council.onlyworlds.com` → log in → Quarters → Commit a Character. They cannot submit via the toolkit until a delegate exists.

## Instructions

### Step 1: Browse Existing Motions

Before drafting anything, check what already exists.

```bash
curl -s "https://www.onlyworlds.com/api/worldapi/council/browse/"
```

Response JSON contains:
- `motions[]`: each with `id`, `name`, `description` (human text, metadata stripped), `supertype` (Motion/Precedent/Amendment), `subtype` (element type), `meta` (author fields, `votes`, `stake`, seconder fields, `field`, `parentMotionId`; no status), `created_at`
- `delegates[]`: each with `id`, `name`, `description`, `supertype` (`CouncilCharacter`), `image_url`. The `description` is raw: it ends in a `<!-- council_char:{...} -->` block whose JSON includes `sourceWorldId` (the delegate's home world) and `isDelegate`
- `total_motions`, `total_delegates`

Browse is capped: it returns the newest 200 motions (amendments and precedents included) and the first 100 delegates by name. `total_motions` and `total_delegates` count what was returned, so at 200 or 100 they are not true totals, and an older motion may be missing from the list. Say so when reporting "no motion exists".

Browse is public, no auth needed. Rate limited to 100/hour per IP, cached 5 minutes.

### Step 2: Analyze Results

Present motions readably, grouped by element type (`subtype`), most votes first. Browse carries no motion status; for status, point the user to `council.onlyworlds.com`.

```markdown
## Character Motions (3)

### "Characters need a death_date field"
- **Votes**: 47 · **Stake**: 100
- **Author**: Admiral Fluffington of Moppetopia
- **Amendments**: 1
- **Precedents**: 0
```

Link amendments/precedents to their parent motions via `meta.parentMotionId`.

### Step 3: Draft Content

Draft in the exact format the submit endpoint expects.

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

Validation rules:
- `type`: motion, amendment, or precedent (lowercase)
- `title`: 5-200 characters
- `description`: 10-2000 characters, must not contain `<!-- council:` markers
- `element_type`: one of the 22 element types or `core`
- `stake`: 100-1000 (tokens deducted from user's daily quota)
- `parent_motion_id` (required for precedent and amendment): UUID of the parent motion
- `amendment_type` (required for amendment): `new_field`, `rename_field`, `remove_field`, `new_type`, `rename_type`

**Always show the draft to the user before submitting.**

### Step 4: Gather Credentials

To submit, collect two things:

1. **World API key + PIN**: the same credentials the api skill uses, loaded from `.env`. If they are not there, the user types them into `.env` (the project-setup skill shows how); never ask for them in chat.
2. **Delegate ID**: UUID of a committed delegate Character in the council world. In the `/browse/` response's `delegates[]`, find the ones whose `council_char` block has `sourceWorldId` equal to the user's world id (from `GET /api/v2/world`) and `isDelegate: true`; or ask the user for their delegate's name and match it.

If none appears, either they have not committed one yet (do it at `council.onlyworlds.com`) or their delegate is past the 100-delegate cap; ask the user for the delegate's UUID before concluding the first.

### Step 5: Submit

The key and PIN travel in the JSON body. Load them from `.env` (`set -a; . ./.env; set +a`) and let the shell fill them in; never print, echo, or paste them into chat (`knowledge/principles.md` §6). The unquoted heredoc expands `$` variables, so a literal `$` or backtick in the text needs escaping.

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/council/submit/" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "type": "motion",
  "title": "Characters need a death_date field",
  "description": "Lifespan visualization requires knowing when characters died.",
  "element_type": "character",
  "field": "death_date",
  "stake": 100,
  "proposer_key": "${ONLYWORLDS_API_KEY:-$OW_API_KEY}",
  "proposer_pin": "${ONLYWORLDS_API_PIN:-$OW_API_PIN}",
  "delegate_id": "{delegate_uuid}"
}
EOF
```

**Success response** (201):
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

Report the token balance to the user. Suggest visiting `council.onlyworlds.com` to see it live.

**Error responses**:

| Code | Error | Meaning |
|------|-------|---------|
| 400 | Invalid delegate | delegate_id not found in the council world |
| 400 | Not a delegate | Character exists but was never committed as a delegate (1000 tokens in council) |
| 400 | Invalid parent motion | parent_motion_id does not match a motion |
| 403 | Invalid credentials | Wrong key/PIN combo |
| 403 | No token profile | The world has no owner account with tokens; log in to onlyworlds.com first |
| 403 | Delegate ownership mismatch | Delegate doesn't belong to user's world |
| 403 | Insufficient tokens | Not enough daily tokens for the stake |
| 403 | Demo worlds cannot submit | Demo/public world keys blocked |
| 422 | `{"detail": [...]}` | Field validation failed (length, stake range, amendment type) |
| 429 | Rate limit exceeded | 10 submissions per world per day |
| 503 | Council unavailable | Council world not configured on the server; try later |

Rate limit: 10 submissions per world per day.

## Motion Status

The browse response carries votes, stake and seconder fields but no status. Motion status is shown on `council.onlyworlds.com`; send the user there rather than deriving one.

## Conversational Use

When the user hits a genuine schema boundary that `knowledge/decision-trees.md` doesn't resolve:

1. Browse council for related motions on that element type
2. If found: surface it ("there's a council motion about this")
3. If not: suggest drafting one ("this might be worth a council motion")

This bridges individual worldbuilding work and collective schema evolution.
