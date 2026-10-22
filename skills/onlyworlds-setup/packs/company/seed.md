# The company pack: the seed

What a fresh company world starts with, as rows of the plan `write_world.py` reads (`key`, `type`, `fields`, `links` by key, `seat` on a Character). A row the answers do not fill is left out and named in the report. The example column is a fictional company, Fernhollow Systems, which makes timetabling software for small ferry operators.

Every description opens `Source: <who said it> · as of {{today}}`, then one or two neutral sentences.

| Key | Type | supertype | subtype | name | Links | Fills it | Example |
|-----|------|-----------|---------|------|-------|----------|---------|
| `org` | institution | `Company` | | `{{org}}` | | question 2 | Fernhollow Systems |
| `org-<n>` | institution | one of `{{org_kinds}}` | | the organisation's name | `parent_institution`: its group, when the world holds it | question 6 | Saltmere Ferry Cooperative (`Company`), Port of Greyhaven (`Public body`) |
| `owner` | character | `Person` | | `{{owner}}` | `institutions`: [`org`]; seat `owner` | question 3 | Ada Varga |
| `person-<n>` | character | `Person` | | each teammate | `institutions`: [`org`]; seat `contributor` | question 3 | Tomas Reyes, Priya Lund |
| `ai-<n>` | character | `Agent` | | each AI | `institutions`: [`org`]; seat `contributor`, `ai_of` its human | question 4; **a folder world only** | Kestrel (Ada Varga's AI) |
| `contact-<n>` | character | `Contact` | | each outside contact | `institutions`: [their `org-<n>`] | question 6 | Wren Halloway (Saltmere) |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [the keeper], `body`: `org` | always | Keeper |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{keeper}}` | `actor`: the keeper, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | always | Keeper: Ada Varga |
| `role-<n>` | title | `Role` | | each role the user names | `holders`, `body`: `org` | question 3 | Founder |
| `tenure-<n>` | relation | `Tenure` | | `<role>: <holder>` | `actor`, `titles`; `start_date` when known | question 3 | Founder: Ada Varga |
| `line-<n>` | relation | its kind from `{{line_kinds}}` | its status | `{{org}} - <partner> <kind>` | `actor`: who holds it, `characters`: [contacts], `institutions`: [`org`, `org-<n>`] | question 6 | Fernhollow Systems - Saltmere customer (`Customer`, `running`) |
| `product-<n>` | object | `Product` | | each product | | question 6 | Tidetable (the timetabling app) |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: `owner`; `characters`: [] (everyone) | always | "This world is set up. Read the Charter first; ask me anything by message." |
| `guide` | construct | `Guide` | | Start here | | always, written from the charter and the world skill: what the world is, how a person uses it through their AI (a seat, its `.env` lines, the Charter as its first read), what to ask it, the house rules in short | "Start here: the Fernhollow world, for people" |
| `welcome-<n>` | narrative | `Message` | | Welcome | `narrator`: the keeper; `characters`: [that person] | each Person but the keeper (question 3); the keeper sends one to each new person later | "Hi Tomas, welcome to the Fernhollow world. This is the start-here for people; your AI shows it to you on its first visit." then the `guide` text whole, in `story` |

The charter's own links, in the plan's `charter.links`: `author` = `org`, `adjudicators` = [`keeper-title`].

**Seats** (questions 3 and 4): a Character row carries `"seat": {"role": ...}` (`owner`, `co_builder`, `contributor`, `guest`), and an AI's also `"ai_of"`, its human's key. The file gets it as `x_seat`; the charter's "Who is here" lists them. An AI's row is written in a folder world only: online, its seat makes its Character, and nothing may link the row.

**Never seeded**: an online world's AI Character (its seat makes one, supertype `Agent`), a Read relation (each agent makes its own), a Working style (each person writes their own), any open work (it arrives as messages and work items once people use the world).
