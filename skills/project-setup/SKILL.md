---
name: onlyworlds-project-setup
description: Connect a local project to an OnlyWorlds world. Creates .env credentials, caches world data locally, configures .gitignore. Use when the user has an OnlyWorlds account and wants to set up their workspace for parsing or API access. Offers full, key-only, or manual credential modes.
---

# OnlyWorlds Project Setup

Connect your project to your OnlyWorlds world.

## CRITICAL: Confirm Location Before Creating Files

This skill writes files to disk (.env, .ow/, .gitignore). Show the user where setup will happen and get explicit confirmation before creating anything.

## What Gets Created

```
project/
├── .env                    # API credentials (gitignored)
├── .ow/                    # OnlyWorlds project data (gitignored)
│   ├── config.json         # World info and settings
│   ├── world-cache.json    # Cached elements (name, uuid, type)
│   └── last-parse.md       # Last parse status
└── .gitignore              # Updated to ignore .env and .ow/
```

## Instructions

### Step 1: Confirm Location

```bash
pwd
```

Show user: "Setting up OnlyWorlds project in: {pwd}. This creates .ow/ folder, .env file, and updates .gitignore. Is this the right place?"

Wait for explicit "yes" before proceeding. If they want a different location, they specify or `cd` there first.

### Step 2: Check Existing Setup

Look for `.ow/` in current directory.

- **Exists**: "Project already connected to '{world_name}'. Refresh cache / Add world / Continue?"
- **Not exists**: Proceed with new setup.

### Step 3: Get Credentials

Ask for API-Key (from world settings) and API-Pin (from profile). If user doesn't have these, direct them to onlyworlds.com.

Then ask credential storage preference:

| Mode | Stored in .env | Behavior |
|------|---------------|----------|
| **full** (default) | API-Key + API-Pin | Fully automated |
| **key-only** | API-Key only | PIN asked for write ops |
| **manual** | Nothing | Both asked each session |

### Step 4: Validate Credentials

```bash
curl -s -X GET "https://www.onlyworlds.com/api/accounts/validate/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If invalid, ask user to re-check credentials.

### Step 5: Fetch World Info

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Extract world name and UUID.

### Step 6: Build World Cache

Fetch all existing elements for local cache. Check world info for element counts per type, then fetch each type with count > 0:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Parse into lightweight cache: name, uuid, type per element. Skip fetching for empty worlds.

### Step 7: Create Files

**`.env`** (varies by credential mode):

```
# full mode:
ONLYWORLDS_API_KEY=your-api-key
ONLYWORLDS_API_PIN=your-pin
ONLYWORLDS_WORLD_UUID=world-uuid

# key-only mode: omit PIN line
# manual mode: omit KEY and PIN lines
```

**`.ow/config.json`**:
```json
{
  "world_name": "World Name",
  "world_uuid": "uuid",
  "credential_mode": "full",
  "cached_at": "2026-02-04T12:00:00Z",
  "last_backup": null,
  "element_counts": {"Character": 45, "Location": 23}
}
```

**`.ow/world-cache.json`**:
```json
{
  "elements": [
    {"name": "Marcus", "uuid": "abc123", "type": "Character"}
  ],
  "cached_at": "2026-02-04T12:00:00Z"
}
```

### Step 8: Update .gitignore

Append `.env` and `.ow/` only if not already listed. Create .gitignore if none exists.

### Step 9: Confirm

Report:
```
Connected to: "World Name"
- Cached X elements (Y Characters, Z Locations, ...)
- Credential mode: {full / key-only / manual}
- Ready for parsing with reconciliation
```

## Cache Freshness

| Cache Age | Behavior |
|-----------|----------|
| < 1 hour | Use silently |
| 1-24 hours | Note age, proceed |
| > 24 hours | Prompt to refresh |
| > 7 days | Strongly recommend refresh |

## Multi-World Support

To add another world to an existing setup:

1. Create `.ow/worlds/` if needed
2. Create `.ow/active-world` file (default world name)
3. Run setup, save to `.ow/worlds/{world-name}/`
4. Switch with: update `.ow/active-world`

## Integration

After setup, other skills detect `.ow/` folder and:
1. Check `credential_mode` in config
2. Load credentials from `.env` (may be partial)
3. Load cache from `world-cache.json`
4. Enable reconciliation automatically
