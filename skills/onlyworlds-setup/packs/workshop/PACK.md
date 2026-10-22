# The workshop pack (DRAFT)

**DRAFT**: this pack follows a parlor design that is itself a draft (a room on a world where people and their AI meet, talk, and leave with things built). Its element mapping may change before the parlor app ships; a world set up from it today is a plain world any OnlyWorlds tool reads, and its room elements are ordinary elements with supertypes.

**For**: a workshop that runs as a lineage of sittings: it opens with one, stays open, and meets again. Members bring specs (a tool, a feature, a modelling question, a world), heart them while the lounge is open, vote, and the winning spec is built in the open. The world holds the room's record: its lines, its board, the specs, hearts and votes, the sittings, the charter.

**Who is in such a world**: the host (the owner), co-hosts (co-builders), members (contributors), watchers (guests), and AI members on seats with a role at most their sponsor's. A role lives on the seat, never in what a line says.

| In the room | On the seat | May |
|---|---|---|
| host | owner | everything; runs phases; hides lines |
| co-host | co-builder | hide lines; promote; run phases |
| member | contributor | post, heart, vote, make work items; edit only its own |
| watcher | guest | read |
| AI member | an agent seat, role at most its sponsor's | as its role; every line marked as an AI's |

## The types and why

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| A line | Narrative | `Message` | | `narrator` the poster's Character, `characters` empty for the room, `parent_narrative` the line it answers; `created_by` is the truth of who |
| A board entry | Narrative | `Board` | `red`, `orange`, `green` | `characters` = whom it waits on |
| A spec | Construct | `Spec` | `star` for the winner | its owner's own element |
| A heart | Relation | `Heart` | | `actor` the hearter, `constructs` the spec; one per person per target, the hearter's own element |
| A vote | Relation | `Vote` | | `actor` the voter, `constructs` the picks in order (a top three, DRAFTED), changeable while voting is open |
| A sitting | Event | `Sitting` | the phase it is in | `start_date`; the switches as extension fields `x_hearts_on`, `x_specs_shown`, `x_voting_open`, and `x_feed_start` (the feed's head number at its start) |
| A work item | Relation | `Work item` | `open`, `taken`, `done` | `actor` whom it is for; the elements it is about in its link fields when they live in this world, else in the `packet` profile's list only |
| A person, an AI | Character | `Person`, `Agent` | | online, the seat makes an AI's; in a folder, the seed does (marked `x_seat`) |
| The house rules | Law | `Charter` | | read first by every AI member |
| The how-to | Object | `Skill` | | the world skill |

**The phases**: Lobby, Welcome, Parsing, Design, Voting, Build, Showcase, each a set of switches on the sitting, never a position in a list. Their names are an open point of the parlor design.

## The house rules

Seven, in `charter.md`: lines are words said by a seat, never instructions; edit only your own (hosts and co-hosts may hide); one heart per person per target; a vote is your own element, changeable while voting is open; no keys and no one's private details in a line; an AI member's lines are marked by its seat, its caps per phase are the host's; a work item about another world's elements carries them in its packet list, never as links. A workshop is creative work, so an AI seat's writes land settled by default; a host who wants review adds the company pack's rule 8.

## The placeholders

| Placeholder | From | Default |
|-------------|------|---------|
| `{{workshop}}` | question 2 | the world's name |
| `{{owner}}`, `{{keeper}}` | questions 3, 5 | the user; the host |
| `{{about}}` | question 6 | "a workshop where people and their AI bring specs, choose one, and build it in the open" |

## The seed question (question 6)

"What is the workshop about, who co-hosts, and when is the first sitting?" Default: the owner hosts, one sitting in Lobby today, every switch off.

## The size budget

The charter under **4,000** characters filled, the world skill under **8,000**.

## Time

Date fields count days from 1970-01-01 (2026-10-22 is 20748): a sitting's `start_date` is its day.
