---
name: onlyworlds-project-setup
description: Set up a local project to work with an OnlyWorlds world. Creates credentials file, caches world data, prepares for reconciliation parsing. Use when user has an OnlyWorlds account and wants to connect their project. Supports multiple worlds per project.
---

# OnlyWorlds Project Setup

Connect your project to your OnlyWorlds world for ongoing work.

**CRITICAL: This skill creates files on disk. Always confirm location with user FIRST before creating anything.**

## When to Use

- User says "I have an OnlyWorlds world"
- User wants to parse into existing world
- User wants to use API from their project
- Starting new project that will use OnlyWorlds data
- Adding a second/third world to existing project

## What This Creates

### Single World (Default)

```
project/
├── .env                    # API credentials (gitignored)
├── .ow/                    # OnlyWorlds project data (gitignored)
│   ├── config.json         # World info and settings
│   ├── world-cache.json    # Cached elements (name, uuid, type)
│   └── last-parse.md       # Last parse status (overwrites each parse)
└── .gitignore              # Updated to ignore .env and .ow/
```

### Multiple Worlds (When Added)

```
project/
├── .env                    # Default world credentials
├── .ow/
│   ├── active-world        # Text file with active world name
│   ├── config.json         # Default world config
│   ├── world-cache.json    # Default world cache
│   ├── last-parse.md
│   └── worlds/             # Additional worlds
│       └── secondary-world/
│           ├── .env
│           ├── config.json
│           ├── world-cache.json
│           └── last-parse.md
└── .gitignore
```

## Process

**IMPORTANT: Do NOT change directories automatically.** Work in the user's current directory. If they want setup elsewhere, they can `cd` there first or specify a path.

### Step 1: Show Location and Get Explicit Confirmation

**ALWAYS start by showing where setup will happen:**

```bash
pwd
```

Then tell user:

```
Setting up OnlyWorlds project in: {pwd}

This will create:
- .ow/ folder (world cache)
- .env file (credentials)
- .gitignore (to protect secrets)

Is this the right place for your project?
```

**STOP HERE. Ask the question. Use the AskUserQuestion tool or wait for their response in conversation.**

Do NOT proceed to Step 2 until user explicitly says:
- "yes" / "y" / "proceed" / "that's fine" / "go ahead" / etc.

If user says "no" or asks questions:
- "Where would you prefer? You can provide a path or cd there first."
- Explain common setups if they seem unsure:
  - Content folder (if that IS the project)
  - Working/toolkit folder (if parsing multiple sources)
  - App/game folder (if world is part of larger project)
- After they respond, ask again: "So where should I set up?"

**Do not assume silence means yes. Wait for explicit confirmation.**

### Step 2: Check Existing Setup

Look for `.ow/` folder in current directory (use `pwd` to show user where this is).

**If exists:**
- "Project already connected to '{world_name}'. What would you like to do?"
- Options: Refresh cache / Add another world / Switch world / Continue

**If not exists:**
- Proceed with new setup

### Step 3: Get Credentials

Ask user for:
- **API-Key**: "Found in your world settings on onlyworlds.com"
- **API-Pin**: "Found in your profile on onlyworlds.com"

If user doesn't have these:
> "To get your credentials:
> 1. Sign in at onlyworlds.com
> 2. Go to your Profile for your API-Pin
> 3. Go to World Settings for the API-Key (each world has its own key)"

### Step 4: Validate Credentials

```bash
curl -s -X GET "https://www.onlyworlds.com/api/accounts/validate/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If invalid: "Those credentials didn't work. Double-check your API-Key and API-Pin."

### Step 5: Fetch World Info

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Extract: world name, UUID.

### Step 6: Build World Cache

Fetch all existing elements to build local cache. Use the world info endpoint to get counts first, then fetch each type:

```bash
# Get world info (shows element counts per type)
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"

# For each element type that has count > 0, fetch:
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"

# Repeat for location, species, institution, etc.
```

Parse responses into lightweight cache (name, uuid, type for each element).

**For empty worlds:** Skip fetching if all counts are 0.

### Step 7: Create Project Files

**`.env`**:
```
ONLYWORLDS_API_KEY=your-api-key
ONLYWORLDS_API_PIN=your-pin
ONLYWORLDS_WORLD_UUID=world-uuid
```

**`.ow/config.json`**:
```json
{
  "world_name": "World Name",
  "world_uuid": "uuid",
  "cached_at": "2026-02-04T12:00:00Z",
  "last_backup": null,
  "element_counts": {
    "Character": 45,
    "Location": 23
  }
}
```

Note: `last_backup` tracks when full world export was last done. Used to remind user to backup.

**`.ow/world-cache.json`**:
```json
{
  "elements": [
    {"name": "Marcus", "uuid": "abc123", "type": "Character"},
    {"name": "Willowbrook", "uuid": "def456", "type": "Location"}
  ],
  "cached_at": "2026-02-04T12:00:00Z"
}
```

### Step 8: Update .gitignore

Check if .gitignore exists. Append if not already present:
```
# OnlyWorlds credentials and cache
.env
.ow/
```

If no .gitignore, create one with these entries.

### Step 9: Confirm Setup and Safety Notice

Report to user:
```
Connected to world: "World Name"
- Cached X elements (Y Characters, Z Locations, ...)
- Credentials stored in .env
- Ready for reconciliation parsing

⚠️  Important: AI operations can modify/delete data.
- Back up your world regularly (export world data periodically)
- Review changes before approving uploads
- Test with small batches first

Next: Parse some text with `/onlyworlds:parsing`
```

## Cache Freshness

Before important operations (parsing, API uploads), other skills should check cache age:

| Cache Age | Behavior |
|-----------|----------|
| < 1 hour | Silent, use cache |
| 1-24 hours | Note age, proceed |
| > 24 hours | Prompt to refresh |
| > 7 days | Strongly recommend refresh |

## Adding Another World

If `.ow/` exists and user wants to add another world:

1. Create `.ow/worlds/` if doesn't exist
2. Create `.ow/active-world` file (set to current default world name)
3. Run setup process, save to `.ow/worlds/{world-name}/`
4. Ask: "Make this the active world? [y/N]"

## Switching Worlds

```
"Switch to {world-name}"
→ Update .ow/active-world
→ "Now working with {world-name}"
```

## Refreshing Cache

```
"Refresh cache"
→ Re-fetch world via API
→ Update .ow/world-cache.json and .ow/config.json
→ Report element counts
```

## Error Handling

**Invalid credentials**: Clear message, prompt to re-enter.

**Network error**: "Couldn't reach OnlyWorlds. Check your internet connection."

**Empty world**: Still create setup. Note: "World is empty - all parses will create new elements."

## Integration with Other Skills

After setup, other skills should:

1. Detect `.ow/` folder exists
2. Load credentials from `.env`
3. Load cache from `.ow/world-cache.json`
4. Enable reconciliation mode automatically
5. Check cache freshness before operations
