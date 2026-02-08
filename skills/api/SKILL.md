---
name: onlyworlds-api
description: This skill should be used when a user wants to interact with the OnlyWorlds REST API - fetching elements from their world, uploading parsed data, syncing changes, checking for duplicates, or any CRUD operations. Requires API-Key (from world settings) and API-Pin (from user profile). Base URL is onlyworlds.com/api/worldapi/.
---

# OnlyWorlds API

Read and write world data via the OnlyWorlds REST API.

**⚠️ Safety Notice:** This skill performs write operations that can modify or delete world data. Always:
- Review changes before executing
- Test with small batches first
- Keep backups of your world (export data regularly)
- Check `.ow/config.json` for `last_backup` date - if > 7 days, consider backing up before major operations

## Quick Start

When user wants to interact with OnlyWorlds API:

1. Get credentials (API-Key and API-Pin)
2. Validate connection
3. Perform requested operations (fetch, create, update, export)

## Instructions

### Step 1: Get Credentials

**Check for existing project setup first:**

1. Look for `.ow/config.json` in current directory
2. If found, read `credential_mode` and load `.env`:
   - **full**: Both API-Key and API-Pin available in `.env` — use them
   - **key-only**: API-Key in `.env`, PIN missing — ask user for PIN
   - **manual**: Nothing in `.env` — ask user for both
3. If no `.ow/` folder, ask user for both:
   - **API-Key**: World-specific key (found in OnlyWorlds world settings)
   - **API-Pin**: User's personal PIN (found in OnlyWorlds profile)

Note: Each API key is scoped to ONE world. The key determines which world you're working with.

### Step 2: Preflight Check

Test credentials before doing anything else:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/accounts/validate/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Success response includes token info. If it fails, credentials are wrong.

**Recommended**: Also fetch world info to confirm you're targeting the right world:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If user says "preflight" or "status check", run both validations and report:
- Credentials: VALID / INVALID
- World: {name}
- Ready for operations: YES / NO

### Step 3: Choose Operation

Based on user request:

**Fetching data:**
- Get world info → [Get World](#get-world)
- List elements → [List Elements](#list-elements)
- Get specific element → [Get Element](#get-element)
- Export entire world → [Fetch Existing World](#fetch-existing-world-for-parsing)

**Writing data:**
- Create element → [Create Element](#create-element)
- Update element → [Update Element](#update-element)
- Delete element → [Delete Element](#delete-element)
- Upload parsed data → [Upload Multiple Elements](#upload-multiple-elements)

## API Operations

### Get World

Get info about the world associated with this API key:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Returns single world object (not paginated).

### List Elements

Get all elements of a specific type:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

**Element types** (lowercase in URL):
- character, creature, species, family, collective, institution
- location, zone, map, pin, marker
- object, construct, title
- ability, trait, language, law
- event, narrative, phenomenon, relation

**Response format:** Returns a JSON array of all elements of that type.

```json
[
  {"id": "uuid", "name": "Element Name", "description": "...", ...},
  ...
]
```

**Optional query parameters:**
- `?search=name` - Filter by name
- `?supertype=X` - Filter by supertype (e.g., `?supertype=honger` for narratives, `?supertype=schedule` for constructs)

**Note:** The SDK wraps this in `{count, next, previous, results}` for pagination. Raw curl returns a plain array.

**IMPORTANT: Endpoint names are SINGULAR** (not plural):
- CORRECT: `/character/`, `/location/`, `/institution/`
- WRONG: `/characters/`, `/locations/`, `/institutions/`

### Get Element

Get a specific element by ID:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

### Create Element

Create a new element:

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Element Name",
    "description": "Description here"
  }'
```

**Important - Link field suffixes:**
- Single links: use `_id` suffix (e.g., `"birthplace_id": "uuid-here"`)
- Multi links: use `_ids` suffix (e.g., `"species_ids": ["uuid1", "uuid2"]`)

### Update Element

Update an existing element:

```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

### Upsert Element

Create or update in one call (useful when you don't know if element exists):

```bash
curl -s -X PUT "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Element Name",
    "description": "Description"
  }'
```

If ID exists → updates. If ID doesn't exist → creates with that ID.

### Delete Element

Delete a specific element:

```bash
curl -s -X DELETE "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Returns 204 No Content on success.

### Upload Multiple Elements

**DEFAULT: Use individual POST requests per element.**

For parsing workflows, upload each element individually:

```bash
# For each element in your parsed JSON:
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{...element data...}'
```

**Why individual POSTs:**
- Returns UUID immediately (needed for linking)
- Clear error messages per element
- Easy to track what succeeded/failed
- Works for any batch size (1 to 1000+)

**Performance:** Even 100+ elements work fine with individual POSTs. The overhead is minimal and the benefits (UUIDs, error clarity) are worth it.

## Common Workflows

### Upload Parsed Elements

**Before uploading**, check backup status:

1. Read `.ow/config.json`
2. Check `last_backup` field
3. If null or > 7 days ago, remind user: "Your last backup was [X days/never]. Consider exporting your world before this upload."
4. For large uploads (20+ elements), always recommend backup first

**Standard upload flow** (use this for parsed content):

```python
# Pseudocode for uploading parsed elements
for element in parsed_json:
    response = POST(f"/worldapi/{element.type.lower()}/", element.data)
    uuid = response["id"]
    # Store uuid for linking dependent elements
```

Use individual POST requests. Batch size doesn't matter - 10 elements or 100 elements, same approach.

**After large uploads**, offer to update `last_backup` date if user wants to mark this as backed up.

### Fetch Existing World for Parsing

When parsing skill needs existing world data for reconciliation:

1. Validate credentials
2. Get world info (name, settings)
3. Fetch all existing elements

Use individual GET requests per type:
```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"

curl -s -X GET "https://www.onlyworlds.com/api/worldapi/location/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"

# ... repeat for each type you need
```

This gives you clean, predictable data per type.

### Check for Duplicates

Before creating, check if element exists:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/?search=Thomas%20Oak" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If results found, consider updating instead of creating.

## Key Rules

1. **Credentials first** - Always validate before operations
2. **Link suffixes matter** - `_id` for single, `_ids` for multi
3. **World-scoped keys** - Each API key = one world
4. **Check before create** - Search for existing elements to avoid duplicates
5. **Individual POSTs** - Use one POST per element for clear errors and immediate UUIDs

## Error Handling

**401 Unauthorized**: Wrong API-Key or API-Pin
**403 Forbidden**: Key doesn't have permission for this world
**404 Not Found**: Element or endpoint doesn't exist
**400 Bad Request**: Invalid data format (check field names and _id suffixes)
**429 Rate Limited**: Too many requests, slow down

### Recovery Patterns

**401/403**: Re-check credentials. Verify API key matches intended world. Get fresh key from world settings.

**404**: Verify element type spelling (lowercase in URL). Confirm element UUID exists with a list query first.

**400**: Schema validation failed. Check field names against schema-reference.md. Verify link fields use correct suffixes. Ensure required fields present (name is required).

**429**: Wait and retry. Add delays between requests (e.g., 100ms between POSTs).

## Integration with Parsing Skill

This skill complements `onlyworlds-parsing`:

1. **Before parsing**: Use this skill to fetch existing world data
2. **After parsing**: Use this skill to upload the generated JSON (individual POSTs)
3. **Existing world flow**: Fetch → Parse → Match → Upload

When user says "existing world", fetch the world data first, then pass to parsing skill for matching.

