---
name: onlyworlds-start
description: "Where to begin with worldbuilding material: notes, a novel, campaign docs, a folder of world files, or nothing yet. Use when the user asks 'what is OnlyWorlds', 'where do I start', 'help me organise my world', 'which tool should I use', or wants to connect this folder to their onlyworlds.com account (a key and PIN in .env). Routes to the right skill; no account needed."
---

# OnlyWorlds Start

Route users to the right capability. The toolkit is a general worldbuilding companion for the whole life of a world: it works on whatever the user has (notes, manuscripts, folders, nothing yet), with no account required. OnlyWorlds is the shared language underneath, and the optional power layer (hosting, the API, the apps) when they want it.

Shared rules every skill follows: `../../knowledge/principles.md`. A world folder on disk: `../../knowledge/world-folder.md`.

## Quick Reference

A world folder on disk (`world.json` + `elements/`) never needs credentials; only an account world goes through [Connect an account](#connect-an-account).

| User says | Route to |
|---|---|
| "I have notes / a book / a wiki / a campaign bible to structure" | import (into a world folder; an account world: Connect an account first) |
| "I have an export from World Anvil, LegendKeeper, Kanka, Campfire or Notion" / an `.owworld` / "back up my world" / "send my world to a friend" | carry |
| "I have an Azgaar map" / "I want my world in Foundry VTT" / "I work in Obsidian" | carry (the public converters, the Obsidian plugin) |
| "How do I model a magic system / factions / a religion" / "what type is this" / "is there a field for X" / "what fields exist" | model |
| "What do I actually have" · "my elements feel disconnected" · "does my world contradict itself" | read (its survey, link or consistency lens) |
| "Show my world as a graph" / "a map of my world" / "my events on a timeline" | draw |
| "I run a campaign, roleplay or story with AI and it loses canon" / "my AI forgets my lore" | context (load the world each session), then update (write each session back) |
| "Update my world from these session notes" / "a character died in play" | update |
| "Keep my world's history" / "try an alternate timeline or a what-if" | `../../knowledge/world-folder.md`, "Keeping history: a world folder in git" (a knowledge page) |
| "Build a tool, game, app or AI agent on my world" / "upload, sync or fetch data" / "set up the MCP server" | develop (an account world: Connect an account first) |
| "Set up a world for my company, team, AI, council, workshop or repo" / "invite my AI" | setup (a starter pack: charter, world skill, seed, invites) |
| "The schema should have X" / "are there motions about X?" | council |
| "Connect this folder to my onlyworlds.com world" | [Connect an account](#connect-an-account) |

| User wants | Point them to |
|---|---|
| Which tools exist | The tools page, `https://onlyworlds.github.io/docs/tools/` |
| A visual app to build and browse their world | **Atlas** (`atlas.onlyworlds.com`) |
| To share a world publicly | Atlas publish, then the world's public page |
| To read the schema in their own tool | schema-dist (`github.com/OnlyWorlds/schema-dist`): vendor its walk; the develop skill |
| To report a bug or ask for a feature | `onlyworlds.com/feedback` |

**Import or update?** Import is a one-off parse of existing material (a novel, a notes folder, a wiki, a backlog of old session notes). Update is the repeating loop after each session: what happened in play is written back into the world. A campaign with old notes starts with import, then uses update after every new session.

**Import or carry?** Notes and prose are import's; another app's export, or a world moving between homes, is carry's.

## Process

### 1. Discover User Situation

Ask: **"What brings you here?"**

Listen for signals from the routing table above. Don't interrogate: one open question usually reveals the path.

**Do not assume the user is a developer.** Many users are writers, GMs, hobbyists. Meet them where they are.

### 2. Explain OnlyWorlds (When Needed)

OnlyWorlds is an open standard for worldbuilding data: 22 element types with defined fields and links, free and open source. A world is a folder of JSON files on disk, or a hosted world on onlyworlds.com behind the API. It is a protocol, not a product: tools built on it exchange worlds freely, with no lock-in. The full picture: `https://onlyworlds.github.io/docs/`.

### 3. Check for Existing Setup

Look in the current directory (or the folder the user names) for either:

- **A world folder**: `world.json` plus an `elements/` folder. Read the world name from `world.json` and mention it: "I see a world folder for '{world_name}'." No credentials needed for anything on it.
- **An account connection**: a `.ow/` folder. Load the world name from `.ow/config.json` and mention it: "I see you're connected to '{world_name}'."

If BOTH are there and the user hasn't said which to use, ask: a local folder may be stale relative to a synced account, so the user picks the source of truth.

### 4. Route Forward

CRITICAL: for users with an **account world** who want import or API work, **Connect an account comes first** if `.ow/` doesn't exist. Without its local copy, import's Step 5 has nothing to reconcile against and the parse creates duplicates. A world folder never goes through credential setup: import into it, read it, and draw it as files.

**Has text + account world**: "Let me connect your project first, then we'll import your text." → Connect an account → import

**Has text + world folder**: "Let's import that into your folder." → import (it reads the folder to avoid duplicates; no credentials)

**Has text, no world**: "Let's import that. You can keep the result as files (a world folder Atlas can open) or create an OnlyWorlds world later." → import, with a world folder as the output. Ask for no account and no key; never make an account feel required.

**Has another app's export, or a world to move or back up**: "Let's plan the move." → carry

**Wants modelling**: "Let's work through that design together." → model

**Wants to organise or manage a world**: a folder on disk, "Let me read your world folder." → read (no credentials). On onlyworlds.com, "Let me connect to your world." → Connect an account → read, or develop for writes

**Wants to understand a world, or connect its elements**: "Let me read your world and write you a brief." → read, survey lens; "Let me analyse your world's connections." → read, link lens

**Wants to see it**: "Let me draw it." → draw (a file to open in a browser; it never changes the world)

**Wants history or an alternate timeline**: "Let's put your world folder under git." → open `../../knowledge/world-folder.md`, "Keeping history", and walk them through it. In a folder linked to an account, turn on Stay offline in Atlas before switching away from the branch the account follows.

**Runs sessions with AI (campaign, roleplay, co-written story) and wants canon to hold**: "Let's work out what each session needs from your world." → context. Once sessions are running: "Let's work out how each session gets written back." → update. Both work on a folder, the user's own notes, or an account world.

**Wants to build tools**: "Let's scaffold a project." → develop

**Wants to propose schema changes**: "Let's check what's already been discussed." → council

**Exploring or discussing ideas** ("I have an idea for a world"): engage with their concept, route to model as complexity emerges.

## Scope

This toolkit serves all worldbuilding work: organising, structuring, designing systems, managing worlds, building software. It does NOT volunteer creative content (stories, prose, backstories). The user is the worldbuilder; the toolkit is the infrastructure.

## Tone

Curious, not salesy. Structure serves creation; it never cools it.

## Connect an account

Connect a project folder to one world on onlyworlds.com. Run this only when the user names an account world; a world folder on disk needs none of it (`../../knowledge/world-folder.md`). Shared rules for credentials and checking your work: principles §5 and §6.

| Situation | Do |
|---|---|
| New setup | Steps 1-8 |
| Already set up | Report the world, then check [Cache Freshness](#cache-freshness) |
| Key or PIN changed | The user edits `.env`; rerun Step 5 |
| A second world | A second project folder: one world per folder |

**What gets created**:

```
project/
├── .env                    # API credentials, typed in by the user (gitignored)
├── .ow/                    # OnlyWorlds project data (gitignored)
│   ├── config.json         # World info and settings
│   └── world-cache.json    # Cached elements (name, uuid, type)
└── .gitignore              # Updated to ignore .env and .ow/
```

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
3. **Create `.env` with empty values.** If `.env` already exists, add only the lines it lacks; a `.env` that already holds the older `ONLYWORLDS_*` names lacks nothing, so leave it as it is. Leave out the PIN line in key-only mode.

```
OW_API_KEY=
OW_API_PIN=
```

4. **Ask the user to fill it in** in their own editor and say when done: the API key from onlyworlds.com (Account → your world → API keys) and the world PIN (Account → Settings → World PIN). Without an account, point them to onlyworlds.com first. For an AI's own seat in a world (theirs or one they are a member of), they press **make a seat** on that world's page (the owner under Invite an agent, a member under Your AI in this world) and paste the `.env` lines it shows once: `OW_API_PIN` there is the seat's own secret, not their PIN. A lost key is **new key** beside the seat.

The API key may be a **prefixed key** (`ow_w_…` world-write, `ow_r_…` read-share) or a **legacy 10-digit key** (still valid, no longer issued); any of these works as-is. The PIN is required for writes. Prefixed keys read without it; only a legacy key reading a private world needs it.

`OW_API_KEY`, `OW_API_PIN` and `OW_WORLD` are the names (an OnlyWorlds agent invite writes the same). A folder may instead hold the older names `ONLYWORLDS_API_KEY`, `ONLYWORLDS_API_PIN`, `ONLYWORLDS_WORLD_UUID`; they still work: the skills read `OW_*` first and fall back to them (in shell, `${OW_API_KEY:-$ONLYWORLDS_API_KEY}`). Keep whichever names a folder already uses.

If the user pastes a credential into chat anyway, do not repeat it back; ask them to put it in `.env`.

### Step 5: Validate Credentials + Fetch World Info

Load `.env` without printing it (`set -a; . ./.env; set +a`), then fill any unset `OW_*` name from its older `ONLYWORLDS_*` twin: `OW_API_KEY=${OW_API_KEY:-$ONLYWORLDS_API_KEY}; OW_API_PIN=${OW_API_PIN:-$ONLYWORLDS_API_PIN}`. To confirm the values are present, test them without showing them: `[ -n "$OW_API_KEY" ] && echo "key set"`. Then test the key with `GET https://www.onlyworlds.com/api/v2/me`: a 401 means the key text is wrong, often the short `ow_w_…abcd` form the key list shows instead of the full key shown once. Then:

```bash
curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"
```

A prefixed key reads without a PIN; a legacy 10-digit key on a private world also sends `-H "API-Pin: ${OW_API_PIN:-$ONLYWORLDS_API_PIN}"`. A `200` with the world object confirms the key and gives you the world name and UUID in one call; append `OW_WORLD=<uuid>` to `.env` (older setups: `ONLYWORLDS_WORLD_UUID`). On a `401`, read the error envelope (it names the problem: bad or revoked key, or wrong PIN) and ask the user to re-check `.env`. With a prefixed key the PIN is checked only on writes, so this read proves the key, not the PIN.

### Step 6: Build World Cache

First record where the world's change feed stands, so the cache has a true-as-of point:

```bash
curl -s "https://www.onlyworlds.com/api/v2/changes?head=true" \
  -H "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"
# → {"cursor": 1234, "changes": [], "has_more": false, "head": 1234}
```

Keep `head` for `.ow/config.json`. Then fetch existing elements. World info carries no element counts, so page all 22 types (an empty type costs one request):

```bash
curl -s "https://www.onlyworlds.com/api/v2/character?limit=100" \
  -H "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"
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
- Ready for import with reconciliation
```

### Cache Freshness

Ask the world, not the clock. `GET /api/v2/changes?head=true` is one cheap request (no element bodies) that returns the world's current `head`. Compare it with `changes_head` in `.ow/config.json`:

| Result | Behavior |
|--------|----------|
| Same `head` | Cache is current; use it |
| Higher `head` | The world changed since caching. Refresh, or apply just the changes: `GET /api/v2/changes?since={changes_head}`, following `cursor` until `has_more` is false |
| Lower `head` | The world was restored from a backup. Rebuild the cache from scratch |

World-meta edits (name, description) do not enter the change feed, so re-read `GET /api/v2/world` if those matter. Without network access, fall back to `cached_at` and tell the user how old the cache is.

### After connecting

Other skills detect the `.ow/` folder and:
1. Check `credential_mode` in config
2. Load credentials from `.env` (may be partial; never print them)
3. Check [Cache Freshness](#cache-freshness), then load `world-cache.json`
4. Reconcile against the cache automatically (import's Step 5)
