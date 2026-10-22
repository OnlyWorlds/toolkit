# The software-project pack: the seed

What a fresh project world starts with, as rows of the plan `write_world.py` reads (with `"repo": true` when the folder is the repository). A row the answers do not fill is left out and named. The example column is a fictional open-source project, Quarrel, a command-line tool that diffs two spreadsheets.

| Key | Type | supertype | subtype | name | Links and fields | Fills it | Example |
|-----|------|-----------|---------|------|------------------|----------|---------|
| `project` | institution | `Project` | | `{{project}}` | | question 2 | Quarrel |
| `owner` | character | `Person` | | `{{owner}}` | seat `owner` | question 3 | Lena Morrow |
| `person-<n>` | character | `Person` | | each maintainer or contributor | seat `contributor` | question 3 | Sami Kettunen |
| `ai-<n>` | character | `Agent` | | each AI | seat `contributor`, `ai_of` its human | question 4; **a folder world only** | Burr (Lena Morrow's AI) |
| `maintainer` | title | `Role` | | Maintainer | `holders`, `body`: `project` | question 3 | Maintainer |
| `tenure-<n>` | relation | `Tenure` | | `Maintainer: <name>` | `actor`, `titles`: [`maintainer`]; `start_date` when known | question 3 | Maintainer: Lena Morrow, from 2024-06-01 |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [the keeper], `body`: `project` | always | Keeper |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{keeper}}` | `actor`, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | always | Keeper: Lena Morrow |
| `component-<n>` | construct | `Component` | `active` | each component | `constructs`: what it depends on; `characters`: its maintainers; `objects`: services it calls | question 6 | Reader (parses the two files), Differ (depends on Reader), Report |
| `service-<n>` | object | `Service` | | each outside service or key dependency | `utility` | question 6 | The package registry |
| `decision-<n>` | law | `Decision` | `accepted` | each decision already made | `author`: `project`; `parent_law` when it replaced one; `date`: `day:<the day>`; `declaration`, `purpose`; the source line names the commit or the person | question 6 | "Rows match by key column, never by position" (2024-09-12, because inserted rows broke every diff after them) |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: `owner`; `characters`: [] | always | "This repository has a context world. Read the Charter first." |

The charter's own links, in the plan's `charter.links`: `author` = `project`, `adjudicators` = [`keeper-title`].

**Seats** (questions 3 and 4): a Character row carries `"seat": {"role": ...}` (`owner`, `co_builder`, `contributor`, `guest`), and an AI's also `"ai_of"`, its human's key. The file gets it as `x_seat`; the charter's "Who is here" lists them. An AI's row is written in a folder world only: online, its seat makes its Character, and nothing may link the row.

**Never seeded**: issues and tasks (the tracker keeps them), an online world's AI Character (its seat makes it), any secret.
