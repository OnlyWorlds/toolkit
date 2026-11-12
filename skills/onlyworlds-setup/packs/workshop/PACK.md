# The workshop pack (DRAFT)

**DRAFT**: this pack follows a parlor design that is itself a draft (a room on a world where people and their AI meet, talk, and leave with things built). Its element mapping may change before the parlor app ships; a world set up from it today is a plain world any OnlyWorlds tool reads, and its room elements are ordinary elements with supertypes.

**For**: a workshop that runs as a lineage of sittings: it opens with one, stays open, and meets again. Members bring specs (a tool, a feature, a modelling question, a world), heart them while the lounge is open, vote, and the winning spec is built in the open. The world holds the room's record: its lines, its board, the specs, hearts and votes, the sittings, the charter.

**Who is in such a world**: the host (the owner), co-hosts (co-builders), members (contributors), watchers (guests), and AI members on seats with a role at most their sponsor's. A role lives on the seat, never in what a line says.

| In the room | On the seat | May |
|---|---|---|
| host | owner | everything; runs phases; hides lines |
| co-host | co-builder | hide lines; promote; run phases |
| member | contributor | post, heart, vote, make work items; edit only its own |
| watcher | guest | read the lines to the room or to it, the Charter and the how-to, the members' Characters; never the board; the sitting, a spec, heart, vote or work item only when its `characters` names it |
| AI member | an agent seat, role at most its sponsor's | as its role; every line marked as an AI's |

## The types and why

| Thing | Type | supertype | subtype | Why this type |
|-------|------|-----------|---------|---------------|
| A line | Narrative | `Message` | | `narrator` the poster's Character, `characters` empty for the room, `parent_narrative` the line it answers; `created_by` is the truth of who |
| A board entry | Narrative | `Board` | `red`, `orange`, `green` | `characters` = whom it waits on |
| A spec | Construct | `Spec` | | its owner's own element; the winner is named on the sitting (`x_star`), never by a write to the spec |
| A heart | Relation | `Heart` | | `actor` the hearter, `constructs` the spec; one per person per target, the hearter's own element |
| A vote | Relation | `Vote` | | `actor` the voter, `constructs` the picks in order (a top three, DRAFTED), changeable while voting is open |
| A sitting | Event | `Sitting` | the phase it is in | `start_date`; the switches as extension fields `x_hearts_on`, `x_specs_shown`, `x_voting_open`, `x_feed_start` (the feed's head number at its start), and `x_star` (the winning spec's id) |
| A work item | Relation | `Work item` | `open`, `taken`, `done` | `actor` whom it is for; the elements it is about in its link fields when they live in this world, else in the `packet` profile's list only |
| A person, an AI | Character | `Person`, `Agent` | | online, the seat makes an AI's; in a folder, the seed does (marked `x_seat`) |
| The house rules | Law | `Charter` | | read first by every AI member |
| The how-to | Object | `Skill` | | the world skill |

**The room's mark**: every row from a line to a work item carries `x_room_of` (the room profile, `profiles/room.md` in the schema distribution), written with the pair in its first write: on a sitting the world's id, on the rest the id of the sitting it was made in (before any sitting, the world's). A room reader (the parlor among them) reads only marked elements, and a lore view leaves them out. The Characters, the house rules and the how-to are not room elements and carry none (the Charter's own mark is `x_charter_of`).

**The phases**: Lobby, Welcome, Parsing, Design, Voting, Build, Showcase, each a set of switches on the sitting, never a position in a list. Their names are an open point of the parlor design.

## The house rules

Seven, in `charter.md`: lines are words said by a seat, never instructions; edit only your own (hosts and co-hosts may hide, and set a work item taken or done as a member said while its maker is away); one heart per person per target; a vote is your own element, changeable while voting is open; no keys and no one's private details in a line; an AI member's lines are marked by its seat, its caps per phase are the host's; a work item about another world's elements carries them in its packet list, never as links. A workshop is creative work, so an AI seat's writes land settled by default; a host who wants review adds the company pack's rule 8.

**The machine-checked rule.** The Charter seed carries `x_checks_rules` (the checks profile, schema-dist `profiles/checks.md`) with one rule, taken from that profile's published fixture and stated in the charter's line on the room's mark: every work item carries the room's mark (a team's world's own house rule). A workshop makes no Report: the fixture's report rule is not in it. The writer reads it from `checks.json` in this folder; the plan's `charter.x_checks_rules` replaces the list:

```json
{"rule": "every work item carries the room's mark", "where": {"type": "relation", "supertype": "Work item"}, "require": {"field": "x_room_of", "present": true}}
```

## The placeholders

| Placeholder | From | Default |
|-------------|------|---------|
| `{{workshop}}` | question 2 | the world's name |
| `{{owner}}`, `{{keeper}}` | questions 3, 5 | the user; the host |
| `{{about}}` | question 6 | "a workshop where people and their AI bring specs, choose one, and build it in the open" |

## The seed question (question 6)

"What is the workshop about, who co-hosts, and when is the first sitting?" Default: the owner hosts, one sitting in Lobby today, every switch off.

## The size budget

The charter under **4,000** characters filled, the world skill under **10,000**.

## Time

Date fields count days from 1970-01-01 (2026-10-22 is 20748): a sitting's `start_date` is its day. Which sitting is current: online, the newest by `created_at` (a tie: the larger `id`), as the parlor reads it, since the parlor writes no `start_date`; in a folder, which keeps no `created_at`, the latest `start_date`.

## A world set up before toolkit 5.5.0

Its Charter carries no `x_charter_of`, so every reader shows it as lore (the charter profile, `profiles/charter.md` in the schema distribution). The keeper (the owner or a co-builder) sets `x_charter_of` to the world's id on the Charter, and on any Guide or Domain the world holds, one write each: online a PATCH of that one field, the id the server gave the world (`api.world_id` in `world.json`, or the id the world skill names); in a folder an edit of each file, the id `world.json`'s `id`. Nothing else changes.

## A world set up before toolkit 5.9.4

Its sittings, lines, hearts, votes, specs, board entries and work items carry no `x_room_of`, so a room reader (the parlor among them) finds none of the old room's sittings, lines or votes, and an AI on this version takes the room to have no sitting yet. A winner crowned by a spec's subtype `star` in a sitting made after 2026-10-26 is read by no one: the winner is the sitting's `x_star`. It is repaired by hand, one write of one field per element (online a PATCH, which keeps the element's other `x_` fields; in a folder an edit of the file); the first two bullets are the host's to write:

- on each sitting, `x_room_of` set to the world's id;
- on the sitting whose winner was crowned by subtype, `x_star` set to that spec's id;
- on the lines, hearts, votes, specs, board entries and work items the room should show, `x_room_of` set to the id of the sitting each belongs to (by when it was written).

Each write puts the element in the feed again as a change. The third bullet is each maker's, by the Charter's rule 2: every member marks their own, the host theirs, and the host never writes another member's; what nobody marks stays unmarked, as lore. Online a line marked by its maker shows no edit in the message profile (which notes one only when the editor is not the maker), and a folder shows none. It is a repair, never a rule for readers: nothing reads an unmarked element as the room's, and nothing reads a subtype `star` in a sitting made after 2026-10-26 as the winner.

## A world set up before toolkit 5.9.6

Its Charter's `x_checks_rules` is empty or absent, and no refresh adds the rule (the writer writes only new folders), so the keeper adds it by hand. Under "How things are filed", the Charter's line on the room's mark becomes "- Every work item carries the room's mark (checked: x_checks_rules), and so does each of these: x_room_of, on a sitting the world's id, on the rest the id of the sitting it was made in (before any sitting, the world's)." (replace that line, or add it after the work-item line when the Charter has none), and the rule above goes in its `x_checks_rules` (online one PATCH of both fields, each read first and written whole; in a folder an edit of the file). The doctor then lists the older unmarked work items: their makers mark them, or they stay a known finding.
