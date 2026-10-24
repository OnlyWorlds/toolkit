# API paragraphs from the hand-written schema reference

The toolkit's `knowledge/schema-reference.md` is generated from schema-dist since 5.0 and carries schema facts only. These paragraphs are about the API, not the schema; they are kept here verbatim from the hand-written page before 5.0 for the develop skill to take. Each is headed by where it stood on that page.

## From the introduction

Field descriptors for any type are also available live at `GET /api/metadata/{type}/`.

## From the whitelist rule (extension fields)

API behaviour: they are stored verbatim on v2 writes and /bulk, and returned on v2 reads and the portal export (Atlas sync keeps them). PATCH merges extension keys (omitting one keeps it); PUT, and a /bulk item with an existing id, replace the whole element, extension fields included; the v1 dialect does not return them.

## Link field names (v2 and v1)

**Note on link field names**: Fields are listed by their canonical names (e.g., `birthplace`). On the modern **v2 / bulk** API these names are used as-is, holding UUIDs: no suffix, same in reads and writes. (The legacy **v1** dialect uses `_id`/`_ids` write suffixes, such as `birthplace_id` and `species_ids`, and expands links into nested objects on read; the SDK's 3.x line converted these, and 4.x speaks v2 only. See the api skill for both dialects.)

## API response format

**API response format (v2)**: list endpoints return `{data, has_more, next_cursor}` (paginated, opaque cursor); detail returns the bare element object; link fields are flat UUID arrays. (v1 returns plain arrays with no pagination and nested `{id, name, supertype, subtype, image_url}` link objects.)

## From Base Fields

- **id** (UUID; any RFC-4122, v7 recommended when minting) - optional on create (the server mints a v7 if omitted)

Rejected on write (422): `type` (reads include it), `created_at`, `updated_at`, `change_seq`. Strip them from a read-back body before PATCH, PUT or /bulk. `world` is ignored (the key decides the world).

All numeric fields are integers in the world's own units (TIME / MASS / LENGTH / DISTANCE); fractions are truncated on write. Numeric ranges are advisory: the API stores out-of-range values; tools should clamp.

## The Link Direction table, with its API column

Some relationships are one-directional (only one type "owns" the link field):

| Relationship | Direction | How to link |
|-------------|-----------|-------------|
| Character ↔ Ability | Character.abilities → Ability | PATCH Character (Ability has NO characters field) |
| Character ↔ Species | Character.species → Species | PATCH Character |
| Title → Character | Title.holders/characters → Character | PATCH Title |
| Object → Location | Object.location → Location | PATCH Object |
| Law → Institution | Law.author → Institution | PATCH Law (Law has NO institutions field) |
| Event → everything | `Event.<links>` → targets | POST/PATCH Event |
| Construct → everything | `Construct.<links>` → targets | POST/PATCH Construct (18 M2M fields) |
