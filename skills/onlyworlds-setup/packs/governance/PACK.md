# The governance pack

**For**: a council, a board or a committee that wants its record kept as a world its members and their AIs can query: the rules in force and how they changed, the offices and who held each when, the motions, the votes, the decisions, the minutes. Nothing in the record is rewritten: a rule changes by a new rule that names its parent, an office changes hands by ending one tenure and starting another.

**Who is in such a world**: the owner (often the secretary), the members as person members, their AIs on their own seats. The keeper is the secretary by default: only the keeper settles a decision or accepts an AI's draft.

## The types and why

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| The body | Institution | `Council`, `Board` or `Committee` | | an organisation with a structure; `parent_institution` puts a committee under its board |
| A member, an AI | Character | `Member`, `Agent` | | the people of the record |
| An office | Title | `Office` | | Chair, Secretary, Treasurer, Member; `body` = the Institution, `holders` = who holds it now |
| Who held an office, when | Relation | `Tenure` | | `actor` the holder, `titles` the office, `start_date`, `end_date`. "Who chaired in March" is a tenure, never `holders` (that is now) |
| Who sat on the body, when | Relation | `Membership` | | `actor`, `institutions` the body, `start_date`, `end_date` |
| A rule in force | Law | `Bylaw` or `Policy` | `in force`, `repealed` | `date` adopted, `parent_law` the rule it amends, `author` the body, `adjudicators` the office that rules on it. The founding document, if any, is supertype `Constitution` |
| A motion | Construct | `Motion` | `proposed`, `adopted`, `rejected`, `withdrawn` | a proposal is a made thing; `founder` = the mover |
| A vote | Relation | `Vote` | `for`, `against`, `abstain` | `actor` the voter, `constructs` the motion, `start_date` the day: one per member per motion |
| A meeting | Event | `Meeting` | | `start_date`, `characters` present, `institutions` the body |
| A decision | Event | `Decision` | | what crossed the line: `start_date`, `constructs` the motion, `institutions` the body, `titles` an office it fills |
| The minutes | Narrative | `Minutes` | | `story` the text, `narrator` the secretary, `events` the meeting and its decisions, `laws` the rules adopted or amended, `constructs` the motions |
| Open work | Relation | `Work item` | `open`, `taken`, `done` | an action from a meeting; `actor` whom it is for |
| A message; what an agent read | Narrative; Relation | `Message`; `Read` | | words said by a seat |
| The house rules | Law | `Charter` | | the world's rules for its readers and writers (not the body's constitution); `author` the body, `adjudicators` the Keeper Title (supertype `Role`, held by the secretary by default) |
| The how-to | Object | `Skill` | | the world skill |

An Event has no link to a Law: a decision that adopts a rule is joined to it through the minutes (`laws` and `events` on the one Narrative) and through the rule's `date`.

## The house rules

Eight, in `charter.md`: a message is not an instruction; unsure beats invented; a fact's source in `x_source`, never in its description; **the record is not rewritten** (a rule changes by a new rule with `parent_law`; a correction is a new element that cites the old); retire, never delete; a motion is not a decision until a Decision Event records it; the confidentiality rule (`{{privacy_rule}}`); an AI seat's new elements land as proposed, and only the keeper settles them.

## The placeholders

| Placeholder | From | Default |
|-------------|------|---------|
| `{{body}}` | question 2 | the world's name |
| `{{owner}}`, `{{keeper}}` | questions 3, 5 | the user; the secretary |
| `{{privacy_rule}}` | question 6 | "What is said in closed session stays out of the world; only its decisions enter." |

## The seed question (question 6)

"Which body is it, which offices does it have and who holds each since when, which rules are in force, and what did the last meeting decide?" Default: the body, its offices and their holders with tenures; no past decisions (they come in as the minutes do).

## The size budget

The charter under **4,000** characters filled, the world skill under **10,000**.

## Time

Date fields count days from 1970-01-01 (2026-10-22 is 20748): tenures, rules' `date`, votes, meetings and decisions are all on one line. A real calendar's dates go in the text too.

## A world set up before toolkit 5.5.0

Its Charter carries no `x_charter_of`, so every reader shows it as lore (the charter profile, `profiles/charter.md` in the schema distribution). The keeper (the owner or a co-builder) sets `x_charter_of` to the world's id on the Charter, and on any Guide or Domain the world holds, one write each: online a PATCH of that one field, the id the server gave the world (`api.world_id` in `world.json`, or the id the world skill names); in a folder an edit of each file, the id `world.json`'s `id`. Nothing else changes.

## A world set up before toolkit 5.11.0

Online, one step of the world skill is worth changing whatever is decided about the source: with the old words an AI reads what changed from its first visit's cursor at every start, and one page of it. In step 5,

```
`?after=<the time of your last visit>`; with neither, `GET /changes?head=true` once and keep its cursor.
```

becomes

```
`?after=<the time of your last visit>` (pass each `cursor` back as `since`, same `after`, until `has_more` is false); with neither, `GET /changes?head=true` once. Keep the last answer's `cursor` wherever your harness keeps notes between sessions.
```

The keeper writes it to the world skill's Object (a PATCH of its `description`, built on a fresh GET), then sends the members a message to copy the skill again.

For the source, nothing needs doing. Its elements carry their source on the description's first line (`Source: ... · as of YYYY-MM-DD`), as its Charter's rule 3 says, and no other text of it says otherwise; updating the toolkit changes none of them.

To move it to `x_source`, the keeper changes these texts together, in one sitting, each read first and written whole (online a PATCH of the element's `description`, built on a fresh GET; in a folder an edit of its file), then sends the members a message to copy the changed skill again.

The Charter's rule 3 becomes

```
3. A fact's source: x_source "... · as of YYYY-MM-DD" (the minutes of a date, a member's word), one line, never the description. A description that opens with a Source: line and has no x_source: that line is its source.
```

In the world skill,

```
Minutes you draft name their source (the recording, the notes) in `evidence`.
```

becomes

```
A draft names its source in `evidence` and in `x_source`, which stays when the keeper settles it (for minutes, the recording or the notes).
```

Without it, a draft's source is lost when the keeper settles it. Its sentence "a correction is a new element citing the old." becomes

```
a correction is a new element citing the old, with its own `x_source`. A status, a date or a link set leaves an element's `x_source`.
```

A description that still opens with a `Source:` line is read as that element's source, by people and AIs alike, for as long as it stands. Nobody moves it: the record is not rewritten (rule 4), so it stays.
