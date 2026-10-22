# The ai-home pack: the seed

What a fresh AI home starts with, as rows of the plan `write_world.py` reads. A row the answers do not fill is left out and named. The example column is a fictional AI, Moth, who helps a fictional illustrator, Juno Castell, run her studio.

| Key | Type | supertype | subtype | name | Links | Fills it | Example |
|-----|------|-----------|---------|------|-------|----------|---------|
| `self` | character | `Agent` | | `{{ai}}` | | question 2; **a folder world only** (online, the seat makes it) | Moth |
| `owner` | character | `Person` | | `{{owner}}` | | question 3 | Juno Castell |
| `person-<n>` | character | `Person` | | each person the AI works with | | question 6 | Ravi Okafor (Juno's printer) |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [`self`] | always (online: empty until the AI adds itself on its first visit) | Keeper |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{ai}}` | `actor`: `self`, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | a folder world; online, the AI's first write | Keeper: Moth |
| `project-<n>` | construct | `Project` | `active` | each project | `characters`: [who is in it]; `start_date` when known | question 6 | The spring print run |
| `style` | construct | `Working style` | | How `{{ai}}` works | `characters`: [`self`] | question 6, in the user's words; else the AI writes it on its first visit | "Short answers first; asks before sending anything out." |
| `tool-<n>` | object | `Tool` | | each tool | | question 6 | The studio's order sheet |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: `owner`; `characters`: [`self`] | always | "This is your home. Read the Charter, then write your Working style and your first memory." |

The charter's own links, in the plan's `charter.links`: `adjudicators` = [`keeper-title`] (no `author`: an AI's home has no Institution).

**Never seeded**: a memory of the AI's own (it writes its first at the end of its first session), a Read relation, a visitor's anything. A memory the user dictates at setup is seeded as theirs: `Source: <the user> · as of {{today}}`.
