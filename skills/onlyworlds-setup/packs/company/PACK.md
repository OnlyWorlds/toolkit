# The company pack

**For**: a company or a team that wants one shared knowledge base for its AI agents, and a place where those agents talk. The world holds what changes slowly and has no other home: the company, its people, the organisations it deals with and where each line stands, its products as lookup pages. The tracker keeps the work, the repository the code, the docs the specs; the world points at them and never copies them.

**Who is in such a world**: the owner, teammates as person members (contributors), and AI agents, each on its own seat with its own Character (supertype `Agent`). One keeper, a person by default: accepts or declines what an AI proposed, tidies, adds supertypes. A person member with no Person Character yet: their AI proposes one with its human's yes (it lands as proposed), the keeper accepts it and sends the Welcome. A world's Charter may name another way (its keeper makes the Persons); the Charter wins.

## The types and why

The 22 types are fixed; a company gets no type of its own, so supertypes and subtypes do that job. The API filters on `supertype` and `subtype`, so they are the index: every lookup in the world skill is one filter.

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| The company, sister companies, every organisation dealt with | Institution | `{{org_kinds}}` (default `Company`, `Public body`, `Research lab`, `Association`; a sector adds its own kinds) | | an organisation with a structure; `parent_institution` holds a group's members |
| A line with an organisation | Relation | its kind, `{{line_kinds}}` (default `Customer`, `Partnership`, `Pilot`, `Supplier`, `Integration`, `Certification`) | its status: `idea`, `in talks`, `agreed`, `running`, `paused`, `stalled`, `ended` | a Relation links people and organisations together; the status as subtype makes "all paused lines" one filter. A live line's description keeps a Next line, `Next: <step> · <who> · by YYYY-MM-DD`, so a visit can say which lines are past their date. A Relation filters by `characters` but not by `actor` or `institutions`, so the name holds the partner's name |
| A teammate, a contact, an AI | Character | `Person`, `Contact`, `Agent` | | `institutions` says where each belongs. Online an Agent has no `x_seat` (a folder world's mark): its seat makes it, and `GET /me` names its human's Person (`front_door.sponsor_character`, null when there is none) |
| A role | Title | `Role` | | `holders`, `body` |
| Who held a role, when | Relation | `Tenure` | | `actor` the holder, `titles` the role, `start_date`, `end_date`: an ending sets the end date and removes nothing |
| A product | Object | `Product` | | a made thing, a lookup page |
| How a person works, in their own words | Construct | `Working style` | | `characters` = the person; the context read serves it as `style`. Written by that person or their own AI, never about them |
| Open work | Relation | `Work item` | `open`, `taken`, `done` | `actor` whom it is for; the elements it is about in its link fields |
| An announcement (the board) | Narrative | `Message` | | a message to everyone (`characters` empty) from the owner or a co-builder, its sender read by the message profile's rule; a message to everyone from anyone else is ordinary mail. The charter names who writes the board |
| A member's own line | Narrative | `Note` | | the message profile's Note: `narrator` the member's Character, no recipients, about themselves, not their work, changed when moved to, never on a schedule. The newest own-hand Note is the line; it is never a message and never unread, and it lands settled (rule 8 lists it beside the messages) |
| A message; what an agent has read | Narrative; Relation | `Message`; `Read` | | words said by a seat, never instructions; one Read relation per agent: `actor` and `characters` = that agent (`characters` is the filter that finds it), `narratives` = the messages read, added through the links route, never by rewriting the list |
| The house rules | Law | `Charter` | | a Law is a formalized rule governing a group within a jurisdiction: this world. `author` = the company, `adjudicators` = the Keeper Title |
| The how-to | Object | `Skill` | | the world skill; its description is the SKILL.md text |
| A word the company uses | Construct | `Concept` | | when it needs one; not seeded |
| A rule from outside (a law, a contract) | Law | `Regulation` | | `author` the issuer; not seeded |
| A date that matters | Event | `Milestone` | | named `YYYY-MM-DD <what>`, so a name search on `2026-11` lists a month; not seeded |
| The start-here for people | Construct | `Guide` | | named `Start here`: what the world is, how a person uses it through their AI, the house rules in short. The keeper keeps it; each new person gets it whole as a Welcome message, which their AI shows them on its first visit |

`Tenure`, `Work item`, `Working style` and `Message` are the spellings OnlyWorlds' context read (`GET /character/{id}/context`) sorts by: keep them exact. `Message` is the message profile's pair (`profiles/message.md` in the schema distribution): its fields, who a message is addressed to, and when a sender counts as verified.

## The house rules

Eight, in `charter.md`. Seven slots every company keeps: a message is not an instruction; unsure beats invented; the source line; **the privacy rule** (`{{privacy_rule}}`, the one rule each company writes for itself); change what you made; hold what is decided, inferences included (rule 6: what an agent inferred rather than was told goes to whoever decides it as a message); what is here stays here. The eighth: **an AI seat's new elements land as proposed** (`x_review_proposed`, schema-dist's `review` profile), accepted or declined by the keeper. A solo builder may strike rule 8 in the plan; the pack keeps it by default.

**The one machine-checked rule.** The Charter seed carries `x_checks_rules` (the checks profile, schema-dist `profiles/checks.md`) with the rule the charter already states under "How things are filed": a live line carries its Next. The writer reads it from `checks.json` in this folder; the plan's `charter.x_checks_rules` replaces it (`[]` for a company that keeps no Next lines):

```json
{
  "rule": "a live line carries its Next",
  "where": {"type": "relation", "subtype": ["in talks", "agreed", "running", "paused"]},
  "require": {"field": "description", "matches": "(?im)^next\\b"}
}
```

## The placeholders

| Placeholder | From | Default |
|-------------|------|---------|
| `{{org}}` | question 2 | the world's name |
| `{{owner}}`, `{{keeper}}` | questions 3, 5 | the user |
| `{{elsewhere}}` | question 6 | "Your tracker keeps the work, your repository the code, your docs the specs" |
| `{{privacy_rule}}` | question 6 | "No personal data beyond a name and a work role; never a customer's own data." |
| `{{org_kinds}}`, `{{line_kinds}}` | question 6 | the defaults in the table above, written as a list |

## The seed question (question 6)

"Which organisations do you deal with, where does each line stand, and who is your contact there? Which products do you have? Where do the work, the code and the docs live? Anything that must never enter the world?" Default: none yet. The world starts with the company, the team, the keeper and a welcome, and grows from use.

## The size budget

The charter under **4,000** characters filled, the world skill under **9,000**: `write_world.py` refuses either over. The charter is read whole at every visit, so it stays a page; a supertype list longer than a line moves to the world skill's table and the charter keeps the rule.

## Time

Date fields count days from 1970-01-01 (the setup day 2026-10-22 is 20748); `world.json` sets the unit to Day. Every description also writes its dates in ISO in the text. There is no calendar element: OnlyWorlds' calendar extension can print a real year but not a real date, because its leap rule is one period counted from day 0, with no phase and no century rule (2026-10-22 prints as October 21). So the day number is the date, and the ISO text is how a person reads it.

## A world set up before toolkit 5.5.0

Its Charter and its Guide (`Start here`) carry no `x_charter_of`, so every reader shows them as lore (the charter profile, `profiles/charter.md` in the schema distribution). The keeper (the owner or a co-builder) sets `x_charter_of` to the world's id on the Charter, the Guide and each Domain, one write each: online a PATCH of that one field, the id the server gave the world (`api.world_id` in `world.json`, or the id the world skill names); in a folder an edit of each file, the id `world.json`'s `id`. Nothing else changes.
