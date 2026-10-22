# The governance pack: the seed

What a fresh governance world starts with, as rows of the plan `write_world.py` reads. A row the answers do not fill is left out and named. The example column is a fictional body, the Lantern Row Allotment Board, which runs a town's allotment gardens.

| Key | Type | supertype | subtype | name | Links | Fills it | Example |
|-----|------|-----------|---------|------|-------|----------|---------|
| `body` | institution | `Board` (or `Council`, `Committee`) | | `{{body}}` | `parent_institution` for a committee | question 2 | Lantern Row Allotment Board |
| `member-<n>` | character | `Member` | | each member | | question 3 | Hal Brennick, Sunniva Dale, Joss Ferrer |
| `office-<n>` | title | `Office` | | each office | `body`: `body`, `holders`: [the current holder] | question 6 | Chair, Secretary, Treasurer |
| `tenure-<n>` | relation | `Tenure` | | `<office>: <holder>` | `actor`, `titles`: [`office-<n>`]; `start_date`: `day:<since>` | question 6 | Chair: Hal Brennick, from 2025-01-15 |
| `membership-<n>` | relation | `Membership` | | `<member>: {{body}}` | `actor`, `institutions`: [`body`]; `start_date` | question 6, when the dates are known | Sunniva Dale: Lantern Row Allotment Board |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [the keeper], `body`: `body` | always | Keeper (held by the secretary) |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{keeper}}` | `actor`, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | always | Keeper: Sunniva Dale |
| `rule-<n>` | law | `Bylaw` or `Policy` (`Constitution` for the founding text) | `in force` | each rule in force | `author`: `body`; `parent_law` when it amends another; `date`: `day:<adopted>` | question 6 | Plot fees (Bylaw, adopted 2024-03-02) |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: the keeper; `characters`: [] | always | "The Board's record is set up. Read the Charter first." |

The charter's own links, in the plan's `charter.links`: `author` = `body`, `adjudicators` = [`keeper-title`].

**Never seeded**: past meetings, decisions, motions and votes (they enter as the minutes do, drafted as proposed and settled by the keeper), a member's AI's Character (its seat makes it).

**Naming**: a tenure `<office>: <holder>`, a vote `<voter> on <motion>`, a decision `<motion>: <outcome>`, the minutes `Minutes <YYYY-MM-DD>`. Relations cannot be filtered by what they link, so the name carries the lookup.
