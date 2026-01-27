---
name: onlyworlds-api
description: Interact with the OnlyWorlds REST API to read and write world data. Use when user wants to fetch existing world elements, upload parsed data, check for duplicates, or sync with OnlyWorlds. Works with API-Key and API-Pin authentication.
disable-model-invocation: true
---

# OnlyWorlds API

Read and write world data via the OnlyWorlds REST API.

## Quick Start

When user wants to interact with OnlyWorlds API:

1. Get credentials (API-Key and API-Pin)
2. Validate connection
3. Perform requested operations (fetch, create, update, export)

## Instructions

### Step 1: Get Credentials

Ask user for:
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
- Export entire world → [Bulk Export](#bulk-export)

**Writing data:**
- Create element → [Create Element](#create-element)
- Update element → [Update Element](#update-element)
- Delete element → [Delete Element](#delete-element)
- Import parsed data → [Bulk Import](#bulk-import)

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

**Response format:**
```json
{
  "count": 42,
  "next": null,
  "previous": null,
  "results": [...]
}
```

**Optional query parameters:**
- `?search=name` - Filter by name
- `?limit=10&offset=0` - Pagination
- `?ordering=-created_at` - Sort order

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

### Bulk Export

Export entire world as JSON:

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldsync/send/" \
  -H "Content-Type: application/json" \
  -d '{"pin": "{api_pin}", "api_key": "{api_key}"}'
```

Note: WorldSync endpoints use body auth, not headers.

Returns complete world data with all elements grouped by type.

### Bulk Import

Import world data from JSON:

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldsync/store/" \
  -H "Content-Type: application/json" \
  -d '{
    "pin": "{api_pin}",
    "api_key": "{api_key}",
    "Character": [...],
    "Location": [...]
  }'
```

Note: WorldSync endpoints use body auth, not headers. Include credentials alongside element data.

Use this to upload parsed data in bulk.

## Common Workflows

### Fetch Existing World for Parsing

When parsing skill needs existing world data:

1. Validate credentials
2. Get world info (name, settings)
3. List all elements by type (or bulk export)
4. Return data for parsing skill to match against

```bash
# Get everything at once
curl -s -X POST "https://www.onlyworlds.com/api/worldsync/send/" \
  -H "Content-Type: application/json" \
  -d '{"pin": "{api_pin}", "api_key": "{api_key}"}'
```

### Upload Parsed Elements

After parsing skill generates JSON:

1. Validate credentials
2. Convert element names to IDs for relationships (if linking to existing)
3. Create elements via POST or bulk import

**For small batches** (< 20 elements): Create individually with POST
**For large imports**: Use bulk import endpoint

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
5. **Use bulk for large data** - Don't create 100 elements one by one

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

**429**: Wait and retry. Consider bulk operations (WorldSync) instead of rapid individual calls.

## Integration with Parsing Skill

This skill complements `onlyworlds-parsing`:

1. **Before parsing**: Use this skill to fetch existing world data
2. **After parsing**: Use this skill to upload the generated JSON
3. **Existing world flow**: Fetch → Parse → Match → Upload

When user says "existing world", fetch the world data first, then pass to parsing skill for matching.
