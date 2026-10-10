---
name: onlyworlds-project-setup
description: Connect a local project to an OnlyWorlds account world. Configures .gitignore, a .env the user fills with their key and PIN, and a local cache of the world. Use when the user has an OnlyWorlds account and wants API access for parsing or other skills. API worlds only; a world folder on disk needs no setup.
---

# OnlyWorlds Project Setup

Connect a project folder to one world on onlyworlds.com.

Shared rules (credentials, checking your work) live in `knowledge/principles.md`; this skill applies them to connecting a project. A world folder on disk (`world.json` + `elements/`) needs none of this: skills read it directly (`knowledge/world-folder.md`).

## Quick Reference

| Situation | Do |
|-----------|----|
| New setup | Steps 1-8 |
| Already set up | Report the world, then check [Cache Freshness](#cache-freshness) |
| Key or PIN changed | The user edits `.env`; rerun Step 5 |
| A second world | A second project folder: one world per folder |

## What Gets Created

```
project/
├── .env                    # API credentials, typed in by the user (gitignored)
├── .ow/                    # OnlyWorlds project data (gitignored)
│   ├── config.json         # World info and settings
│   └── world-cache.json    # Cached elements (name, uuid, type)
└── .gitignore              # Updated to ignore .env and .ow/
```

## Instructions

### Step 1: Location

Run `pwd` and tell the user: "Setting up OnlyWorlds in: {pwd}. This adds `.ow/` and `.env` and updates `.gitignore`." Proceed unless they name another folder.

### Step 2: Check Existing Setup

If `.ow/config.json` exists, the project is already connected: report the world name and run [Cache Freshness](#cache-freshness), unless the user asked for something else. Otherwise continue.

### Step 3: Choose the Credential Mode

Use **full** unless the user does not want the PIN stored in the project.

| Mode | Stored in `.env` | Writes |
|------|------------------|--------|
| **full** (default) | API-Key + API-Pin | Automated |
| **key-only** | API-Key only | The user adds the PIN line to `.env` for a write session and removes it after |
| **manual** | Nothing between sessions | The user fills `.env` at the start of each session and clears it after |

**Credentials never go through chat** (principles §6). The user types them into `.env`; you never see, print, or repeat them.

### Step 4: Protect, Then Create `.env`

Ignore first, write second:

1. **Update `.gitignore`.** Append `.env` and `.ow/` only if not already listed. Create `.gitignore` if none exists.
2. **Check that `.env` is not already tracked:** `git ls-files .env`. Ignoring a tracked file does nothing. If it prints `.env`, stop: the user runs `git rm --cached .env` and commits that, and any key already committed should be revoked and replaced (Account → your world → API keys).
3. **Create `.env` with empty values.** If `.env` already exists, add only the lines it lacks. Leave out the PIN line in key-only mode.

```
ONLYWORLDS_API_KEY=
ONLYWORLDS_API_PIN=
```

4. **Ask the user to fill it in** in their own editor and say when done: the API key from onlyworlds.com (Account → your world → API keys) and the world PIN (Account → Settings → World PIN). Without an account, point them to onlyworlds.com first.

The API key may be a **prefixed key** (`ow_w_…` world-write, `ow_r_…` read-share) or a **legacy 10-digit key** (still valid, no longer issued); any of these works as-is. The PIN is required for writes. Prefixed keys read without it; only a legacy key reading a private world needs it.

If the user pastes a credential into chat anyway, do not repeat it back; ask them to put it in `.env`.

### Step 5: Validate Credentials + Fetch World Info

Load `.env` without printing it (`set -a; . ./.env; set +a`). To confirm the values are present, test them without showing them: `[ -n "$ONLYWORLDS_API_KEY" ] && echo "key set"`. Then:

```bash
curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

A prefixed key reads without a PIN; a legacy 10-digit key on a private world also sends `-H "API-Pin: $ONLYWORLDS_API_PIN"`. A `200` with the world object confirms the key and gives you the world name and UUID in one call; append `ONLYWORLDS_WORLD_UUID=<uuid>` to `.env`. On a `401`, read the error envelope (it names the problem: bad or revoked key, or wrong PIN) and ask the user to re-check `.env`. With a prefixed key the PIN is checked only on writes, so this read proves the key, not the PIN.

### Step 6: Build World Cache

First record where the world's change feed stands, so the cache has a true-as-of point:

```bash
curl -s "https://www.onlyworlds.com/api/v2/changes?head=true" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
# → {"cursor": 1234, "changes": [], "has_more": false, "head": 1234}
```

Keep `head` for `.ow/config.json`. Then fetch existing elements. World info carries no element counts, so page all 22 types (an empty type costs one request):

```bash
curl -s "https://www.onlyworlds.com/api/v2/character?limit=100" \
  -H "API-Key: $ONLYWORLDS_API_KEY"
```

v2 lists are paginated: the response is `{data, has_more, next_cursor}`. Follow `next_cursor` (`?limit=100&cursor={next_cursor}`) until `has_more` is false. Parse into a lightweight cache: name, uuid, type per element. Alternative: walk `GET /api/v2/changes` from zero (no `since`, then `?since={cursor}` until `has_more` is false; skip `delete` ops), which returns every element in one feed; keep the `head` from its last page. Record the per-type totals as `element_counts`.

### Step 7: Write the Cache Files

**`.ow/config.json`**:
```json
{
  "world_name": "World Name",
  "world_uuid": "uuid",
  "credential_mode": "full",
  "cached_at": "2026-02-04T12:00:00Z",
  "changes_head": 1234,
  "element_counts": {"Character": 45, "Location": 23}
}
```

**`.ow/world-cache.json`**:
```json
{
  "elements": [
    {"name": "Marcus", "uuid": "abc123", "type": "Character"}
  ],
  "cached_at": "2026-02-04T12:00:00Z",
  "changes_head": 1234
}
```

### Step 8: Confirm

Report:
```
Connected to: "World Name"
- Cached X elements (Y Characters, Z Locations, ...)
- Credential mode: {full / key-only / manual}
- Ready for parsing with reconciliation
```

## Cache Freshness

Ask the world, not the clock. `GET /api/v2/changes?head=true` is one cheap request (no element bodies) that returns the world's current `head`. Compare it with `changes_head` in `.ow/config.json`:

| Result | Behavior |
|--------|----------|
| Same `head` | Cache is current; use it |
| Higher `head` | The world changed since caching. Refresh, or apply just the changes: `GET /api/v2/changes?since={changes_head}`, following `cursor` until `has_more` is false |
| Lower `head` | The world was restored from a backup. Rebuild the cache from scratch |

World-meta edits (name, description) do not enter the change feed, so re-read `GET /api/v2/world` if those matter. Without network access, fall back to `cached_at` and tell the user how old the cache is.

## Integration

After setup, other skills detect the `.ow/` folder and:
1. Check `credential_mode` in config
2. Load credentials from `.env` (may be partial; never print them)
3. Check [Cache Freshness](#cache-freshness), then load `world-cache.json`
4. Enable reconciliation automatically
