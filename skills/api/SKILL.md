---
name: onlyworlds-api
description: Interact with the OnlyWorlds REST API — fetch, create, update, or delete world elements. Use when the user wants to query their world, upload parsed data, browse existing elements, or perform any API operations. Requires API-Key and API-Pin headers. Base URL: onlyworlds.com/api/worldapi/. All endpoints use singular names.
---

# OnlyWorlds API

Read and write world data via the OnlyWorlds REST API.

## Quick Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Validate credentials | GET | `/api/accounts/validate/` |
| Get world info | GET | `/api/worldapi/world/` |
| List elements by type | GET | `/api/worldapi/{type}/` |
| Get specific element | GET | `/api/worldapi/{type}/{uuid}/` |
| Create element | POST | `/api/worldapi/{type}/` |
| Update element | PATCH | `/api/worldapi/{type}/{uuid}/` |
| Upsert element | PUT | `/api/worldapi/{type}/{uuid}/` |
| Delete element | DELETE | `/api/worldapi/{type}/{uuid}/` |
| Search by name | GET | `/api/worldapi/{type}/?search=name` |

**CRITICAL: Endpoint names are SINGULAR** — `/character/`, `/location/`, `/institution/`. NOT plural.

## Safety Notice

This skill performs write operations that can modify or delete world data.
- Check `.ow/config.json` for `last_backup` date — if > 7 days, recommend backup before major operations
- Test with small batches first
- Review changes before executing

## Instructions

### Step 1: Get Credentials

Check for `.ow/config.json` in current directory first:

| Config Found | credential_mode | Action |
|-------------|----------------|--------|
| Yes | full | Load API-Key + API-Pin from `.env` |
| Yes | key-only | Load API-Key from `.env`, ask user for PIN |
| Yes | manual | Ask user for both |
| No | — | Ask user for both |

- **API-Key**: World-specific (from world settings on onlyworlds.com)
- **API-Pin**: User's personal PIN (from profile on onlyworlds.com)

### Step 2: Validate Credentials

```bash
curl -s -X GET "https://www.onlyworlds.com/api/accounts/validate/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Also fetch world info to confirm targeting the right world:

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/world/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

### Step 3: Perform Operations

## API Operations

### List Elements

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

**Element types** (lowercase): character, creature, species, family, collective, institution, location, zone, map, pin, marker, object, construct, title, ability, trait, language, law, event, narrative, phenomenon, relation

**Response**: JSON array of all elements of that type.

**Query parameters**: `?search=name`, `?supertype=X`

**Note**: SDK wraps this in `{count, next, previous, results}`. Raw curl returns plain array.

### Get Element

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

### Create Element

```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Element Name", "description": "Description here"}'
```

**Link field suffixes**: Single links use `_id` suffix. Multi links use `_ids` suffix.

### Update Element

```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

### Upsert Element

```bash
curl -s -X PUT "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Element Name", "description": "Description"}'
```

If ID exists → updates. If not → creates with that ID.

### Delete Element

```bash
curl -s -X DELETE "https://www.onlyworlds.com/api/worldapi/{element_type}/{uuid}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

Returns 204 No Content on success.

## Common Workflows

### Upload Parsed Elements

Before uploading, check `.ow/config.json` `last_backup` field. For large uploads (20+ elements), recommend backup first.

Use individual POST requests per element:

```bash
# For each element in parsed JSON:
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/{element_type}/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}" \
  -H "Content-Type: application/json" \
  -d '{...element data...}'
```

Individual POSTs return UUIDs immediately, give clear error messages per element, and work for any batch size.

### Fetch Existing World for Parsing

Fetch all existing elements for reconciliation:

```bash
# For each element type:
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

### Check for Duplicates

```bash
curl -s -X GET "https://www.onlyworlds.com/api/worldapi/character/?search=Thomas%20Oak" \
  -H "API-Key: {api_key}" \
  -H "API-Pin: {api_pin}"
```

If results found, consider updating instead of creating.

## Key Rules

1. **Credentials first** — always validate before operations
2. **Link suffixes matter** — `_id` for single, `_ids` for multi
3. **World-scoped keys** — each API key = one world
4. **Check before create** — search for existing elements to avoid duplicates
5. **Individual POSTs** — one POST per element for clear errors and immediate UUIDs

## Error Handling

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Wrong API-Key or API-Pin | Re-check credentials |
| 403 | Key doesn't have permission | Verify key matches intended world |
| 404 | Element or endpoint doesn't exist | Check type spelling (lowercase, singular) |
| 400 | Invalid data format | Check field names against schema, verify `_id`/`_ids` suffixes |
| 429 | Rate limited | Wait, add delays between requests |
