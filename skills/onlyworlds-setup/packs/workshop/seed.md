# The workshop pack: the seed (DRAFT)

What a fresh workshop world starts with, as rows of the plan `write_world.py` reads. A row the answers do not fill is left out and named. The example column is a fictional workshop, the Kiln Street Toolmakers, where people bring ideas for small tools and build one each sitting.

| Key | Type | supertype | subtype | name | Links and fields | Fills it | Example |
|-----|------|-----------|---------|------|------------------|----------|---------|
| `host` | character | `Person` | | `{{owner}}` | seat `owner` | question 3 | Mira Solberg |
| `cohost-<n>` | character | `Person` | | each co-host | seat `co_builder` | question 6 | Dev Anand |
| `ai-<n>` | character | `Agent` | | each AI member | seat `contributor`, `ai_of` its sponsor | question 4; **a folder world only** | Tinder (Mira Solberg's AI) |
| `keeper-title` | title | `Role` | | Keeper | `holders`: [the keeper] | always | Keeper (the host) |
| `keeper-tenure` | relation | `Tenure` | | Keeper: `{{keeper}}` | `actor`, `titles`: [`keeper-title`]; `start_date`: `day:{{today}}` | always | Keeper: Mira Solberg |
| `sitting-1` | event | `Sitting` | `Lobby` | `{{workshop}}`, sitting 1 | `start_date`: `day:<the day>`; `x_hearts_on`: false, `x_specs_shown`: false, `x_voting_open`: false | question 6 | Kiln Street Toolmakers, sitting 1 (2026-11-07) |
| `board-welcome` | narrative | `Board` | `green` | How this room works | `characters`: []; the description says the phases and the house rules in two lines | always | "Bring a spec; heart what you like; we vote at Voting." |
| `welcome` | narrative | `Message` | | Welcome | `narrator`: `host`; `characters`: [] | always | "Welcome. Read the Charter, then bring a spec." |

The charter's own links, in the plan's `charter.links`: `adjudicators` = [`keeper-title`].

**Seats** (questions 3 and 4): a Character row carries `"seat": {"role": ...}` (`owner`, `co_builder`, `contributor`, `guest`), and an AI's also `"ai_of"`, its human's key. The file gets it as `x_seat`; the charter's "Who is here" lists them. An AI's row is written in a folder world only: online, its seat makes its Character, and nothing may link the row.

**Never seeded**: specs, hearts, votes and work items (each is its maker's own element), an online world's AI member Character (its seat makes it), `x_feed_start` (the host sets it from `GET /changes?head=true` when the sitting opens online).
