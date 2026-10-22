# The company pack: the seed

What a fresh company world starts with, as rows of the plan `write_world.py` reads (`key`, `type`, `fields`, `links` by key). A row the answers do not fill is left out and named in the report. The example column is a fictional company, Fernhollow Systems, which makes timetabling software for small ferry operators.

Every description opens `Source: <who said it> · as of {{today}}`, then one or two neutral sentences.

| Key | Type | supertype | subtype | name | Links | Fills it | Example |
|-----|------|-----------|---------|------|-------|----------|---------|
| `org` | institution | `Company` | | `{{org}}` | | question 2 | Fernhollow Systems |
| `org-<n>` | institution | one of `{{org_kinds}}` | | the organisation's name | `parent_institution`: its group, when the world holds it | question 6 | Saltmere Ferry Cooperative (`Company`), Port of Greyhaven (`Public body`) |
| `owner` | character | `Person` | | `{{owner}}` | `institutions`: [`org`] | question 3 | Ada Varga |
| `person-<n>` | character | `Person` | | each teammate | `institutions`: [`org`] | question 3 | Tomas Reyes, Priya Lund |
| `contact-<n>` | character | `Contact` | | each outside contact | `institutions`: [their `org-<n>`] | question 6 | Wren Halloway (Saltmere) |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [the keeper], `body`: `org` | always | Keeper |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{keeper}}` | `actor`: the keeper, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | always | Keeper: Ada Varga |
| `role-<n>` | title | `Role` | | each role the user names | `holders`, `body`: `org` | question 3 | Founder |
| `tenure-<n>` | relation | `Tenure` | | `<role>: <holder>` | `actor`, `titles`; `start_date` when known | question 3 | Founder: Ada Varga |
| `line-<n>` | relation | its kind from `{{line_kinds}}` | its status | `{{org}} - <partner> <kind>` | `actor`: who holds it, `characters`: [contacts], `institutions`: [`org`, `org-<n>`] | question 6 | Fernhollow Systems - Saltmere customer (`Customer`, `running`) |
| `product-<n>` | object | `Product` | | each product | | question 6 | Tidetable (the timetabling app) |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: `owner`; `characters`: [] (everyone) | always | "This world is set up. Read the Charter first; ask me anything by message." |

The charter's own links, in the plan's `charter.links`: `author` = `org`, `adjudicators` = [`keeper-title`].

**Never seeded**: an AI's Character (its seat makes one, supertype `Agent`), a Read relation (each agent makes its own), a Working style (each person writes their own), any open work (it arrives as messages and work items once people use the world).
