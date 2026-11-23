---
name: onlyworlds-start
description: "Where to begin with worldbuilding material: notes, a novel, campaign docs, a folder of world files, or nothing yet. Use when the user asks 'what is OnlyWorlds', 'where do I start', 'help me organise my world', 'which tool should I use', 'give my world a public page', or wants to connect this folder to their onlyworlds.com account (a key and PIN in .env). Routes to the right skill; no account needed."
---

# OnlyWorlds Start

Route users to the right capability. The toolkit is a general worldbuilding companion for the whole life of a world: it works on whatever the user has (notes, manuscripts, folders, nothing yet), with no account required. OnlyWorlds is the shared language underneath, and the optional power layer (hosting, the API, the apps) when they want it.

Shared rules every skill follows: `knowledge/principles.md`. A world folder on disk: `knowledge/world-folder.md`.

## Quick Reference

A world folder on disk (`world.json` + `elements/`) never needs credentials; only an account world goes through [Connect an account](#connect-an-account).

| User says | Route to |
|---|---|
| "I have notes / a book / a wiki / a campaign bible to structure" | import (into a world folder; an account world: Connect an account first) |
| "I have an export from World Anvil, LegendKeeper, Kanka, Campfire or Notion" / an `.owworld` / "back up my world" / "send my world to a friend" | carry |
| "I have an Azgaar map" / "I want my world in Foundry VTT" / "I work in Obsidian" | carry (the public converters, the Obsidian plugin) |
| "Copy my account world to a folder" / "put my folder on my account" | carry (moving a world between a folder and an account is carry's; develop is for building on it) |
| "How do I model a magic system / factions / a religion" / "what type is this" / "is there a field for X" / "what fields exist" | model |
| "What do I actually have" · "my elements feel disconnected" · "does my world contradict itself" | read (its survey, links or consistency report) |
| "Show my world as a graph" / "a map of my world" / "my events on a timeline" | draw |
| "I run a campaign, roleplay or story with AI and it loses canon" / "my AI forgets my lore" | context (load the world each session: a brief from the files, or on an account world one character's draught or a saved lens), then update (write each session back) |
| "Update my world from these session notes" / "a character died in play" | update |
| "Keep my world's history" / "try an alternate timeline or a what-if" | `knowledge/world-folder.md`, "Keeping history: a world folder in git" (a knowledge page) |
| "Build a tool, game, app or AI agent on my world" / "upload, sync or fetch data" / "set up the MCP server" | develop (an account world: Connect an account first) |
| "Set up a world for my company, team, AI, council, workshop or repo" / "invite my AI" | setup (a starter pack: charter, world skill, seed, invites) |
| "The schema should have X" / "are there motions about X?" | council |
| "Connect this folder to my onlyworlds.com world" | [Connect an account](#connect-an-account) |

| User wants | Point them to |
|---|---|
| Which tools exist | The tools page, `https://onlyworlds.github.io/docs/tools/` |
| A visual app to build and browse their world | **Atlas** (`atlas.onlyworlds.com`) |
| To open an account world to everyone | the world page, **Settings**, **Who can see this world**: **Anyone can read it, with no account** (the API and tools then read it keyless), and **Give it a public page** for a public page at `onlyworlds.com/w/<address>`, with its graph; hidden elements stay hidden. [The public page](https://onlyworlds.github.io/docs/development/api/public.html) |
| To try the API with no account | the practice world: a shared key and PIN on the docs' [Keys page](https://onlyworlds.github.io/docs/getting-started/keys.html#the-practice-world), reset every night; the develop skill's Credentials |
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
- **A link to an account world**, either of two marks: a `world.json` with an `api` block (Atlas links a folder this way; never print the block), or a `.ow/` folder (Connect an account's; the world name is in `.ow/config.json`). Mention it: "I see you're connected to '{world_name}'."

A link mark beside world files means one world in two homes. Unless the user has said which to use, ask which is the source of truth: the folder may be stale against the account, or hold edits not yet sent.

### 4. Route Forward

The Quick Reference routes; three cases it cannot carry:

- **An account world connects first.** For import or API work on an account world, Connect an account comes first if `.ow/` doesn't exist: without its local copy, import's Step 5 has nothing to reconcile against and the parse creates duplicates. A world folder never goes through credential setup, and a user with no world gets a world folder: never make an account feel required.
- **Both a folder and an account link**: Step 3's source-of-truth question comes before any route.
- **History or an alternate timeline**: "Let's put your world folder under git." → open `knowledge/world-folder.md`, "Keeping history", and walk them through it; a folder linked to an account is never committed: version an unlinked copy (same section).

## Scope

This toolkit serves all worldbuilding work: organising, structuring, designing systems, managing worlds, building software. It does NOT volunteer creative content (stories, prose, backstories). The user is the worldbuilder; the toolkit is the infrastructure.

## Tone

Curious, not salesy. Structure serves creation; it never cools it.

## Connect an account

Connect a project folder to one world on onlyworlds.com. Run this only when the user names an account world; a world folder on disk needs none of it (`knowledge/world-folder.md`). Shared rules for credentials and checking your work: principles §5 and §6. Handed an address on onlyworlds.com with `/join` and a code after `#`: fetch `https://www.onlyworlds.com/join` as text and do what that page says.

| Situation | Do |
|---|---|
| New setup | Steps 1-8 |
| Already set up | Step 2: the world's door first, then report the world and check [Cache Freshness](#cache-freshness) |
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

If `.ow/config.json` exists, the project is already connected. Read the world's door first, whatever the user asked: load `.env` as Step 5 does and, when it holds a key, read `GET /api/v2/me`; when its `front_door.charter` is set, read that Charter whole (`GET /api/v2/law/<id>`), then each Object in `front_door.charter_skill` (`GET /api/v2/object/<id>`), before anything is answered from the cache: they are the world's house rules. With no key in `.env` (manual mode between sessions), say so: what you answer comes from the cache, without the world's door. A world with no door (`front_door.charter` null) costs that one read and goes on as before. Then report the world name and run [Cache Freshness](#cache-freshness), unless the user asked for something else. Where `.ow/config.json` holds no `start_line`, no line in the start file holds the world's id (`world_uuid`) and the key's shape (Step 8) is `prefixed`, offer the start line as Step 8 does; otherwise say nothing of it. Otherwise continue.

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
2. **Check that `.env` is not already tracked:** `git ls-files .env`. Ignoring a tracked file does nothing. If it prints `.env`, stop: the user runs `git rm --cached .env` and commits that, and any key already committed should be revoked and replaced (**Worlds** → the world → **Access** → **Keys**).
3. **Create `.env` with empty values.** If `.env` already exists, add only the lines it lacks; a `.env` that already holds the older `ONLYWORLDS_*` names lacks nothing, so leave it as it is. Leave out the PIN line in key-only mode.

```
OW_API_KEY=
OW_API_PIN=
```

4. **Ask the user to fill it in** in their own editor and say when done: the API key from onlyworlds.com (**Worlds** → the world → **Access** → **Keys**, then **Make a key**; it shows once) and the world PIN (Account → Settings → World PIN). Without an account, point them to onlyworlds.com first. For an AI's own seat in a world (theirs or one they are a member of), they press **Make a seat** on its world page (the owner on **Access**, under **Let someone in**, **An AI**, **A seat here**; a member under **Your AI in this world**) and paste the `.env` lines it shows once: `OW_API_PIN` there is the seat's own secret, not their PIN. A lost key is **New key** beside the seat.

What each key shape can do, the PIN's part, the `OW_*` names (the older `ONLYWORLDS_*` ones still work: keep whichever a folder already uses) and the headers every call sends: the develop skill's Credentials.

If the user pastes a credential into chat anyway, do not repeat it back; ask them to put it in `.env`.

### Step 5: Validate Credentials + Fetch World Info

Load `.env` without printing it (`set -a; . ./.env; set +a`), then fill any unset `OW_*` name from its older `ONLYWORLDS_*` twin: `OW_API_KEY=${OW_API_KEY:-$ONLYWORLDS_API_KEY}; OW_API_PIN=${OW_API_PIN:-$ONLYWORLDS_API_PIN}`. To confirm the values are present, test them without showing them: `[ -n "$OW_API_KEY" ] && echo "key set"`. Then test the key with `GET https://www.onlyworlds.com/api/v2/me`: a 401 means the key text is wrong, often the short `ow_w_…abcd` form the key list shows instead of the full key shown once. Then:

```bash
curl -s "https://www.onlyworlds.com/api/v2/world" \
  -H "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"
```

A legacy 10-digit key on a world that has a PIN, public or private, also sends the PIN header. A `200` with the world object confirms the key and gives you the world name and UUID in one call; append `OW_WORLD=<uuid>` to `.env` (older setups: `ONLYWORLDS_WORLD_UUID`). On a `401`, read the error envelope (it names the problem: bad or revoked key, or wrong PIN) and ask the user to re-check `.env`. With a prefixed key the PIN is checked only on writes, so this read proves the key, not the PIN.

### Step 6: Build World Cache

First record where the world's change feed stands, so the cache has a true-as-of point:

```bash
curl -s "https://www.onlyworlds.com/api/v2/changes?head=true" \
  -H "API-Key: ${OW_API_KEY:-$ONLYWORLDS_API_KEY}"
# → {"cursor": 1234, "changes": [], "has_more": false, "head": 1234}
```

Keep `head` for `.ow/config.json`. Then fetch existing elements. The world info from Step 5 carries `counts`, how many elements this key may read in all (`total`) and per type (`types`): page each type with a count above zero, and check the totals against it:

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

So the next session here opens the world first, offer the start line. First the key's shape, read from `.env` alone; it prints one word, never the key:

```
(unset OW_API_KEY; if [ -f .env ]; then set -a; command . ./.env 2>/dev/null; set +a; fi; k=${OW_API_KEY:-}; k=${k%"$(printf '\r')"}; case "$k" in "") echo no-ow-name;; [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]) echo classic;; *) echo prefixed;; esac)
```

No offer on `classic`, a 10-digit key (on a world with a PIN it reads nothing without the PIN, and the line sends none), or on `no-ow-name`, a key `.env` holds only under an older `ONLYWORLDS_*` name. Say why, and that a key made on the world's page (**Access** → **Keys**), kept as `OW_API_KEY`, gets the line. On `prefixed` alone, offer this line, with the world's UUID from Step 5 for `{world_id}` (any other word, or none, is no offer):

```
This folder works in the OnlyWorlds world with id {world_id}. Each session starts with GET https://www.onlyworlds.com/api/v2/me, header API-Key from OW_API_KEY in .env, then reads the Charter its front_door names, when there is one; a 401 means the key is gone: ask your person. Where .env here holds no OW_API_KEY, this line is not for you.
```

It goes in the start file, the file your tool reads at the start of each session, and always one in this folder, never one in a folder above: this folder's own `CLAUDE.md` when your tool is Claude Code and a `CLAUDE.md` stands in this folder or in any folder above it, else `AGENTS.md`; either is made if it is not there. Say the line and the file, and add it on the user's yes; a user who asked for it ("set up for next time", "remember this world") has said yes. With no yes, write nothing: the report gives the line and the file, so the user can say yes later. A no is kept: add `"start_line": "declined"` to `.ow/config.json`. In a git repository, say the file is tracked there and other people's AI tools read it. Add it once: where a line in that file already holds this world's id, leave it and add none. A line there with another world's id: say so, and offer to replace it.

Report:
```
Connected to: "World Name"
- Cached X elements (Y Characters, Z Locations, ...)
- Credential mode: {full / key-only / manual}
- Start line: {added to the file / not added: why, the line and its file}
- Ready for import with reconciliation
```

### Cache Freshness

Ask the world, not the clock. `GET /api/v2/changes?head=true` is one cheap request (no element bodies) that returns the world's current `head`. Compare it with `changes_head` in `.ow/config.json`:

| Result | Behavior |
|--------|----------|
| Same `head` | Cache is current; use it |
| Higher `head` | The world changed since caching. Refresh, or apply just the changes: `GET /api/v2/changes?since={changes_head}`, following `cursor` until `has_more` is false |
| Lower `head` | The world was restored from a backup. Rebuild the cache from scratch |

A guest's or contributor's key also reads `epoch` on each page: keep it beside `changes_head`. An `epoch` other than the kept one, at any `head`, means what the key may see changed (a Character given or taken, a role, an element hidden or unhidden): pull again from `since=0`. A stored cursor then answers `409 resync_required`, whose `reason` says what to do with what the new walk does not name: `role`, keep it; `view`, drop it.

World-meta edits (name, description) do not enter the change feed, so re-read `GET /api/v2/world` if those matter. Without network access, fall back to `cached_at` and tell the user how old the cache is.

### After connecting

Other skills detect the `.ow/` folder and:
1. Check `credential_mode` in config
2. Load credentials from `.env` (may be partial; never print them)
3. Check [Cache Freshness](#cache-freshness), then load `world-cache.json`
4. Reconcile against the cache automatically (import's Step 5)

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- The route: the skill the user's words point to in the Quick Reference (Route Forward).
- That no account is needed where none is: a world folder never needs credentials (Quick Reference; Route Forward).
- A world folder or account link found, by its world's name; with both, the source-of-truth question before any route (Check for Existing Setup).
- After Connect an account, its report: the world, the cached counts, the credential mode, the start line added or why not; offline, the cache's age (Step 8; Cache Freshness).
- No key or PIN asked for, printed or repeated in chat (Connect an account, Step 3).
- What was checked and how (principles §5).
