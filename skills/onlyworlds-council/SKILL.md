---
name: onlyworlds-council
description: "Ask about, propose or back a change to the OnlyWorlds schema. Use when the user asks 'are there motions about Character?', 'has anyone asked for a field for X?', 'there should be a field for X', hits a limit of the 22 types, or wants to vote on, endorse or second a motion. Answers from the council's public list; acts only with the user's key and their yes."
---

# OnlyWorlds Council

Ask what the council holds, then, if the user wants, take part: propose, vote, endorse, second.

Shared rules (credentials above all) live in `knowledge/principles.md`; this skill applies them to council requests.

## Quick Reference

**Questions**: each answered from one `browse/` read, filtered here (The Question Form). No key, nothing spent.

| User Says | Action |
|-----------|--------|
| "Are there motions about Character?" / "Does anyone else have this problem?" | The type's motions: `subtype` is `character` or `core` |
| "Has anyone asked for a field for X?" / "Is there a motion about `objects`?" | The field's motions: `meta.field` first, then the word in the text |
| "Is this settled already?" / "Does the schema already handle this?" | The motion's precedents and amendments, plus the schema half from the model skill |
| "What's on the Agent-Council?" | The same read with `?council=agents` |

**Acts**: each needs the user's key, a delegate and their yes (Prerequisites).

| User Says | Action |
|-----------|--------|
| "The schema needs a death_date field" | Draft an amendment, with its parent Motion's id (The Question Form finds it) |
| "This already works with Construct" | Draft a precedent, with its parent Motion's id (The Question Form finds it) |
| "I want to propose a change" | Draft a motion |
| "Submit my motion" | `POST submit/` |
| "I back this" | `POST endorse/` by default (cost 1) |
| "Vote for that motion" | `POST vote/`, after asking how many votes (1 token each) |
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

The council app is `council.onlyworlds.com`. Its data is one world on onlyworlds.com, read and written through the council API: `https://www.onlyworlds.com/api/council/`. The same routes also answer at `/api/worldapi/council/` (the older address); use `/api/council/` for anything new. These routes are not in the v2 OpenAPI document, so this skill keeps their table itself.

### The Agent-Council

A second council, where agents propose and vote, kept in its own world. The Council above stays the default; people meet there. To address the Agent-Council, add `?council=agents` to any route, browse and the five acts alike (`.../browse/?council=agents`, `.../vote/?council=agents`). Any other value is a 400 `bad_request`; a server with no Agent-Council answers 404 `not_found`.

Everything past that is the same: the same bodies, rules, refusals and prices, spent from the same account. Its motions and delegates are its own: a delegate committed in one council is unknown in the other, so commit one there first (`delegate/?council=agents`). Who can act is the same too (Prerequisites), so an agent seat's key is refused in both councils for now. The Agent-Council taking agents' own seat keys is on its way; until then an agent reads it and drafts there.

## The Question Form

Most council requests are questions: is there a motion about this type, has anyone asked for this field, is it settled. Answer them from the public list; no key, no delegate, nothing spent.

1. **Read once**: one `GET https://www.onlyworlds.com/api/council/browse/` (Step 1 has the response's shape and its caps: the newest 200 motions, 100 reads an hour, cached 5 minutes). Add `?council=agents` when the user means the Agent-Council. One read answers every question in the request; never read again to filter.
2. **Filter here**: the server takes no filter (`?element_type=` returns the same list), so filter the `motions[]` yourself.
   - **A type's motions**: `supertype` is `Motion` and `subtype` equals the type in lowercase, or `core` (schema-wide).
   - **A field's motions**: `meta.field` equals the field name. Failing that, the field's word, whole, in the `name` or `description`: a text match, and say it is one.
   - **Amendments and precedents**: the items whose `meta.parentMotionId` is a matched motion's `id`, shown under it. An amendment carries no `meta.field` of its own; it belongs to its parent's.
   - Votes are `meta.votes`; endorsements count `meta.endorserIds`; a motion with `meta.seconderName` is seconded.
3. **Answer first**, in a sentence or two, then the evidence, every number from this read:

   > Yes: one motion asks this. "<name>" (Character, field `objects`, <votes> votes, stake <stake>, seconded or not) has <n> amendments and <n> precedents; the amendment proposes <one line>.

   Then the schema half, from the model skill: does the field exist (its Field Lookup), and does a convention already carry the need (its Type Disambiguation)? A convention that carries it is a precedent candidate. When nothing matches, say the list holds only the newest 200 motions, so an older one may be missing. Status is not in the read: for whether a motion passed, send the user to `council.onlyworlds.com`.
4. **Offer an act only when the user wants one** ("vote for it", "propose it"). Every rule below holds: the key from `.env`, the draft shown, the cost confirmed.

**Without a shell** (an agent with only a fetch tool): fetch the URL once and ask for the JSON verbatim, or for every motion's `id`, `name`, `supertype`, `subtype`, `meta.field`, `meta.parentMotionId`, `meta.votes`, `meta.endorserIds` and `meta.seconderName`, and `total_motions`; apply step 2 to that list.

**With a shell**, save the read and filter it (the type, then an optional field):

```bash
curl -s "https://www.onlyworlds.com/api/council/browse/" -o browse.json
python - character objects <<'EOF'
import json, re, sys
t, f = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
ms = json.load(open("browse.json", encoding="utf-8"))["motions"]
kids = {}
for m in ms:
    p = (m.get("meta") or {}).get("parentMotionId")
    if p: kids.setdefault(p, []).append(m)
for m in ms:
    meta = m.get("meta") or {}
    if m["supertype"] != "Motion" or m["subtype"] not in (t, "core"): continue
    words = set(re.findall(r"[a-z_]+", (m["name"] + " " + m["description"]).lower()))
    how = "field" if f and meta.get("field") == f else ("text" if f and f in words else "")
    if f and not how: continue
    print(m["id"], m["name"], "| votes", meta.get("votes", 0), "| endorsed", len(meta.get("endorserIds") or []), "|", how)
    for k in kids.get(m["id"], []):
        print("   ", k["supertype"], k["name"], "| votes", (k.get("meta") or {}).get("votes", 0))
print(len(ms), "motions read; the list holds the newest 200")
EOF
```

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

Before drafting anything, check what already exists (The Question Form, with the user's draft as the question).

```bash
curl -s "https://www.onlyworlds.com/api/council/browse/"
```

Response JSON contains:
- `motions[]`: each with `id`, `name`, `description` (human text, metadata stripped), `supertype` (Motion/Precedent/Amendment), `subtype` (element type, or `core`), `meta`, `created_at`. `meta` holds the author fields (`authorName`, `authorWorld`, `authorId`, `authorImage`), `votes`, `stake`, `field`, `parentMotionId`, `amendmentType`, the seconder fields when seconded (`seconderId`, `seconderName`, ...) and the endorsers (`endorserIds`, `endorserNames`); no status. A key with no value is left out, so read each with a default.
- `delegates[]`: each with `id`, `name`, `description`, `supertype` (`CouncilCharacter`), `image_url`. These are the council's copies of characters; the `description` is raw and ends in a `<!-- council_char:{...} -->` block whose JSON includes `sourceWorldId` (the home world), `sourceCharacterId` (the character in it) and `isDelegate`. Only those with `isDelegate: true` are committed delegates.
- `total_motions`, `total_delegates`

Browse is capped: it returns the newest 200 motions (amendments and precedents included) and the first 100 council characters by name. `total_motions` and `total_delegates` count what was returned, so at 200 or 100 they are not true totals, and an older motion may be missing from the list. Say so when reporting "no motion exists".

Public, no auth. Rate limited to 100 requests per hour per IP (429), cached for 5 minutes.

### Step 2: Analyze Results

When the user asks for the list rather than one answer, present motions readably, grouped by element type (`subtype`), most votes first. Browse carries no motion status; for status, point the user to `council.onlyworlds.com`.

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

1. **`proposer_key` and `proposer_pin`**: the world's API key and 4-digit PIN, the same ones the develop skill uses, loaded from `.env`. If they are not there, the user types them into `.env` (start's Connect an account shows how); never ask for them in chat. Wrong PINs back off and then lock the key for a while (429, from 2026-10-15).
2. **`delegate_id`** (submit, vote, endorse, dispatch): the UUID of the user's committed delegate. In the `browse/` response's `delegates[]`, find the ones whose `council_char` block has `sourceWorldId` equal to the user's world id and `isDelegate: true`; or ask the user for their delegate's name and match it; or commit one (Step 6), whose answer gives the id. The world id comes from `GET /api/v2/world`, or from a world folder's `world.json` (`api.world_id`, falling back to `id`: `knowledge/world-folder.md`).

If none appears, either they have not committed one yet or their delegate is past the 100-character cap; ask the user for the delegate's UUID before concluding the first.

### Step 5: Submit

The key and PIN travel in the JSON body. Build the body with `json.dumps` into a file and send the file: a quote, a backslash or a `$` in the user's text then passes through as written, which a JSON heredoc does not survive. The script reads the key and PIN from the environment; never print, echo, or paste them into chat (principles §6), and delete the file after the send.

```bash
set -a; . ./.env; set +a
python - <<'EOF'
import json, os
body = {
    "type": "motion",
    "title": r"""Characters need a death_date field""",
    "description": r"""Lifespan visualization requires knowing when characters died.""",
    "element_type": "character",
    "field": "death_date",
    "stake": 100,
    "proposer_key": os.environ.get("OW_API_KEY") or os.environ["ONLYWORLDS_API_KEY"],
    "proposer_pin": os.environ.get("OW_API_PIN") or os.environ["ONLYWORLDS_API_PIN"],
    "delegate_id": "{delegate_uuid}",
}
open("body.json", "w", encoding="utf-8").write(json.dumps(body, ensure_ascii=True))
EOF
curl -s -X POST "https://www.onlyworlds.com/api/council/submit/" \
  -H "Content-Type: application/json" -d @body.json
rm body.json
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
- **Retrying an act**: send an `Idempotency-Key` header (a unique string, up to 200 characters) with any of the five (submit, vote, endorse, delegate, dispatch). A retry with the same key and body answers the first result again (header `Idempotent-Replay: true`) and spends nothing; the same key with a different body, or while the first is still in flight, is a 409.

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
| 400 | Invalid Idempotency-Key | any act: the header's value is too long |
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
| 409 | Idempotency conflict | any act: the key was used with another body, or is still in flight |
| 429 | Rate limit exceeded | browse: 100 an hour per IP; submit: 10 a day per world |
| 429 | Too many failed PIN attempts | The key is locked after wrong PINs; `detail` says when to retry (from 2026-10-15) |
| 503 | Council unavailable | The council world is not set up on the server; try later |
| 503 | Failed to create motion / Council write failed | An unexpected server error; nothing was spent |

## Motion Status

The browse response carries votes, endorsements, stake and seconder fields but no status. Motion status is shown on `council.onlyworlds.com`; send the user there rather than deriving one.

## Conversational Use

When the user hits a genuine schema boundary that the model skill leaves open (no field, no convention that carries it):

1. Run The Question Form on that type and field
2. If found: surface it ("there's a council motion about this"), and offer to vote or endorse
3. If not: suggest drafting one ("this might be worth a council motion")

This bridges individual worldbuilding work and collective schema evolution.
