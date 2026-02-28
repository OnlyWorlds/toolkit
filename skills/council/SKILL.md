---
name: onlyworlds-council
description: Browse and participate in OnlyWorlds schema governance. Use when the user encounters a schema limitation, wants to propose a change (motion), check existing motions or amendments, draft a precedent showing existing solutions, or discuss how the schema could evolve. Covers browsing, drafting, and submitting motions via the council proxy API.
---

# OnlyWorlds Council

Browse, discuss, and participate in schema governance.

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

The OnlyWorlds Council is where worldbuilders propose and discuss schema changes. Characters from across all worlds serve as **delegates** — committed representatives who submit motions on behalf of their world.

Council data lives at `council.onlyworlds.com`. The toolkit browses via a public proxy and submits via an authenticated one.

## Prerequisites for Submitting

Browsing is free. Submitting requires:

1. **An OnlyWorlds world** with an API key and PIN
2. **A delegate** — a Character from the user's world that has been committed as a council delegate at `council.onlyworlds.com` (costs 1000 tokens, one-time)
3. **Tokens** — each submission stakes 100-1000 tokens, deducted from the user's daily quota

If the user hasn't committed a delegate yet, direct them to `council.onlyworlds.com` → log in → Quarters → Commit a Character. They cannot submit via the toolkit until a delegate exists.

## Instructions

### Step 1: Browse Existing Motions

Before drafting anything, check what already exists.

```bash
curl -s "https://www.onlyworlds.com/api/worldapi/council/browse/"
```

Response JSON contains:
- `motions[]` — each with `id`, `name`, `description` (human text, metadata stripped), `supertype` (Motion/Precedent/Amendment), `subtype` (element type), `meta` (author, votes, status, parent, etc.), `created_at`
- `delegates[]` — each with `id`, `name`, `image_url`
- `total_motions`, `total_delegates`

Browse is public, no auth needed. Rate limited to 100/hour per IP, cached 5 minutes.

### Step 2: Analyze Results

Present motions readably, grouped by status (active first, then fresh, flagged, passed, declined, implemented):

```markdown
## Character Motions (3 active)

### "Characters need a death_date field"
- **Status**: active (47 votes)
- **Author**: Admiral Fluffington of Moppetopia
- **Amendments**: 1
- **Precedents**: 0
```

Link amendments/precedents to their parent motions via `meta.parentMotionId`.

### Step 3: Draft Content

Draft in the exact format the submit endpoint expects.

**Motion** — a schema limitation or question:
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

**Precedent** — the schema already handles this:
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

**Amendment** — the schema needs to change:
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

To submit, collect three things:

1. **World API key + PIN** — same credentials used for the api skill. Check `.ow/config.json` and `.env` first.
2. **Delegate ID** — UUID of a committed delegate Character in the council world. Browse the `/browse/` response's `delegates[]` to find delegates from the user's world, or ask the user for their delegate's name and match it.

If no delegate from their world appears in the browse results, they need to commit one at `council.onlyworlds.com` first.

### Step 5: Submit

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/council/submit/" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "motion",
    "title": "Characters need a death_date field",
    "description": "Lifespan visualization requires knowing when characters died.",
    "element_type": "character",
    "field": "death_date",
    "stake": 100,
    "proposer_key": "{world_api_key}",
    "proposer_pin": "{user_pin}",
    "delegate_id": "{delegate_uuid}"
  }'
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
| 400 | Invalid delegate | delegate_id not found or not committed |
| 403 | Invalid credentials | Wrong key/PIN combo |
| 403 | Delegate ownership mismatch | Delegate doesn't belong to user's world |
| 403 | Insufficient tokens | Not enough daily tokens for the stake |
| 403 | Demo worlds cannot submit | Demo/public world keys blocked |
| 429 | Rate limit exceeded | 10 submissions per world per day |

Rate limit: 10 submissions per world per day.

## Motion Statuses

| Status | Meaning |
|--------|---------|
| fresh | New (< 24h), no responses yet |
| active | Has engagement or > 24h old |
| flagged | Hit vote threshold, awaiting curator |
| passed | Curator approved for implementation |
| declined | Curator rejected (with reason) |
| implemented | Merged into schema |

## Conversational Use

When the user hits a genuine schema boundary that decision-trees doesn't resolve:

1. Browse council for related motions on that element type
2. If found: surface it ("there's an active council motion about this")
3. If not: suggest drafting one ("this might be worth a council motion")

This bridges individual worldbuilding work and collective schema evolution.
