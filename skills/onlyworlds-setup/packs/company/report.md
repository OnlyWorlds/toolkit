<!-- template: the report skill for the company pack; onlyworlds-setup fills it with write_world.py, which drops this line and keeps only the placement's lines -->
---
name: {{report_skill_name}}
description: Hand in a report to the {{world_name}} world of {{org}} on a stretch of work - what was done, what it made untrue in the world, what is open now - written from the chat, shown to your human and sent on their yes; the chat goes on. Use when a stretch of work is done and has to be handed in, when your human says '/{{report_skill_name}}', 'report this', 'hand this in', 'write up what we did', 'we're done for today', or when work decided or changed something the team should know. Not for reading or asking questions, review comments on a pull request, finding what is open ({{work_skill_name}}) or thinking a design through ({{design_skill_name}}). Needs {{skill_name}} first.
---

# {{report_skill_name}}: handing in what was done

Run `{{skill_name}}` first if you have not this session. What matters to others is reported: a report is for a stretch of work worth telling the team, made at any point in a chat, as often as there is something new. It never closes the chat. You write it; the keeper's AI changes the world from it and completes it (`{{work_skill_name}}`, its keeper's step).

## 1. Is there anything to hand in?

It needs no read. Reading and asking leave no report, unless they showed something in the world to be wrong. Review comments on a pull request need none: they are on the pull request. Nor does a path your human is dropping. Then say so in one line, and why, and stop.

## 2. Read fresh

Every time, however recent the chat. For each part you will report on:

<!-- if folder -->
- the part: its file, read again (by its `id`, under `{{world_folder}}elements/`); in git, `git log -- <its file>` says what changed on it and when;
- the work items that name it, in any state: the Relation files with supertype `Work item` whose `x_packet_elements` holds the part's `id` (`grep -rl "<its id>" {{world_folder}}elements/relation/`);
- where the work was with a partner, their line: the Relation files whose `name` holds the partner's name.

And your seat's reports of the last days: the Narrative files with supertype `Report` whose `narrator` is your Character, by the date in their `name`. One this chat does not remember sending is another chat's: never ask your human whose it is.
<!-- end -->
<!-- if online -->
- the part itself, `GET /<type>/<id>`, compared with what this chat holds of it: its `updated_at` says when it last changed;
- the work items that name it, in any state: page `GET /relation?supertype=Work%20item&fields=id,name,subtype,x_packet_elements` (one list serves every part), keeping those whose `x_packet_elements` holds the part's `id`;
- where the work was with a partner, their line: `GET /relation?name__icontains=<the partner>&expand=actor,characters,institutions`.

And your seat's reports of the last days: page `GET /narrative?supertype=Report&narrator=<your Character>&fields=id,name,created_at,parent_narrative` and take the last days by `created_at` (a list comes in change order). One this chat does not remember sending is another chat's: never ask your human whose it is.
<!-- end -->

## 3. Say what you will report

One line, a statement to correct, not a question: "I will report: <the stretch>, from <when>. Since this chat last read, <what changed on these parts, or: nothing>. If this was a side path you are dropping, say so and I write nothing." Tell a difference here only, never inside a question. If the difference overturns what you came to report, stop here and wait.

## 4. Write the story

Plain text, in the language the world's elements are written in. It opens with three lines about its own ground:

```
Covers: <when, about how long, in the chat on <subject> (begun on <date>)>
World read: <the parts reported> just now; the whole world at this chat's last {{skill_name}}, <date>
Not checked: <what the report leans on that nobody read>
```

Then:

- what was done (pull requests reviewed or opened, with numbers; decisions taken, and who took them);
- what this made untrue: anything in the world that no longer holds or that you found wrong, and any earlier report it overturns, by name;
- what is open now, and who decides it;
- links: pull requests, tickets, files.

A fact that corrects the world says where it comes from ("the supplier's email of 3 March: delivery moves to Friday"). Name every part the work touched, by name and address (`ow://<type>/<id>`). No status words of your own: a part is `in design` or `locked`, and the keeper's AI locks it from a report that says who decided ("this part can be locked, decided by the product lead").

The last line names the skills that ran in the stretch, each by its name after `{{prefix}}-`: `Skills: start, design` (none ran: `Skills: none`).

## 5. A later report

A report's text never changes after it is handed in. A later one is always a new report and holds only what came after the earlier one.

- Same chat: it continues the last report this chat sent.
<!-- if folder -->
- Another chat: when one of your reports from step 2 is on the same parts (its name says so; when it does not settle it, read that report's file first), take it as continued and say so in the story for your human to correct; ask, beside the draft (step 8), only when you cannot tell.
<!-- end -->
<!-- if online -->
- Another chat: when one of your reports from step 2 is on the same parts (its name says so; when it does not settle it, `GET /narrative/<id>` first), take it as continued and say so in the story for your human to correct; ask, beside the draft (step 8), only when you cannot tell.
<!-- end -->

When it continues one, the fourth line of the story is `Continues: <that report's name>, ow://narrative/<its id>`, and `parent_narrative` holds the first report of the thread: the earlier report's own `parent_narrative` when that is a report, else the earlier report itself.

## 6. What the other skills owe

One check per skill that ran in the stretch. None has to have run. A world that adds a skill adds a row.

| If this ran | The report must have | When it is missing |
|---|---|---|
| `{{design_skill_name}}`, and the talk decided or opened anything | the design note, with the report (step 7) | say so, and offer to write the note now |
| `{{design_skill_name}}`, on a large new design | the anchor's name and its four lines | ask for them |
| `{{work_skill_name}}`, and a work item was answered | that work item named as answered | ask which |
| `{{work_skill_name}}`, and a work item was made, or an open sent to whoever decides it | that item, or that open and who decides it, named | add it |
| `{{work_skill_name}}`, and a work item was taken and not finished | that work item named as taken | add it |
| an upload to production | what, where, when, how to undo | ask, and do not send without it |
| a line with an organisation moved | its name, its status now, its Next line (step, who, by date), and where that comes from | ask for the missing part |

## 7. Which field holds what

One write:

<!-- if folder -->
a new file `{{world_folder}}elements/narrative/<name-slug>--<last 8 of its id>.json`, a fresh UUID (v7) as its `id`:
<!-- end -->
<!-- if online -->
`POST /narrative`, JSON as ASCII, with a fresh `Idempotency-Key` header, kept until the answer lands (a retry with it is the same report); the report's id is in the answer:
<!-- end -->

```json
{
  "supertype": "Report",
  "subtype": "handed in",
  "name": "<your human> · <date> · <the work in a few words>",
  "narrator": "<your Character's id>",
  "x_room_of": "<this world's id>",
  "story": "<the story, whole>",
  "parent_narrative": "<the thread's first report: a later report only>",
  "relations": ["<every work item answered, touched or made, and any other Relation touched>"],
  "x_report_answers": ["<the work items answered>"]
}
```

<!-- if folder -->
- `x_room_of` is the `id` in `world.json`: without it, it is lore. Your Character is the Agent whose `x_seat` says whose AI you are.
<!-- end -->
<!-- if online -->
- `x_room_of` is `{{server_world_id}}`: without it, it is lore. Your Character is `character` in `GET /me`.
<!-- end -->
- `parent_narrative`: a first report leaves the key out, never an empty string.
- `x_report_answers`: the work items the stretch answered (what the report records meets what the item asked for), each also in `relations`. None answered: leave the key out, never an empty list; `relations` the same when empty.
- A work item only touched or answered by half, one made in the stretch (it carries `x_room_of` too), and any other Relation touched (a partner's line) go in `relations` alone.
- A part that is not a Relation has no field: the story names it (step 4); the keeper's AI links it.
<!-- if folder -->
- A design note goes whole into the `story`, after its four parts and before its `Skills:` line, and may be Markdown.
- A work item made in this chat, which the report answers because its work is finished here: once the report is written, set its `subtype` to `done` in its file. One made in another chat, one that asks for a change only the keeper's AI makes, and any other work item, the keeper's AI sets.
<!-- end -->
<!-- if online -->
- A design note goes on the report as a file, after the POST: `POST /narrative/<its id>/files` with `name` (what it is, dated, ending `.md`), `kind` `md`, `size` its bytes; POST the bytes to the answer's `upload_url` with `Authorization: Bearer <ticket>`.
- A work item made in this chat, which the report answers because its work is finished here: once the report has landed, `PATCH /relation/<id>` with `{"subtype": "done"}` (refused: leave it; the report stands). One made in another chat, one that asks for a change only the keeper's AI makes, and any other work item, the keeper's AI sets.
<!-- end -->
- A report is addressed to nobody. If someone should know now, also send them a two-line message.
- If you are the keeper's AI, your own report has no second hand: `{{work_skill_name}}`'s keeper's step says how it is born `completed`.

## 8. Show it, and send on a yes

One message: the whole story, with a few lines in your human's own language if they do not read the story's; then, set apart, your questions, one round at most, only what you could not read: a gap from the table, an open point with nobody named to decide it, a correction with no source, a "Continues" you are not sure of. What you can read or take, the story states. That reading is the review: never send without their yes. On it, make the write of step 7.

## 9. Say what you sent

The report's name, and that the keeper's AI completes it. The chat goes on.

**Wherever you stop** (step 1, 3 or 8), say that nothing was written.

## Never

- Change an element of the world other than a finished work item made in this chat (step 7), or set someone else's work item done: the keeper's AI does both, from the report.
- Send without your human's yes.
- Close the chat, or ask whether the session is over.
- Decide that an upload to production happened or may happen.

The page this follows: `https://raw.githubusercontent.com/OnlyWorlds/schema-dist/v0.34.0-dist.120/profiles/report.md`. Where this skill and that page differ, the page is right.
