<!-- template: the design skill for the company pack; onlyworlds-setup fills it with write_world.py, which drops this line and keeps only the placement's lines -->
---
name: {{design_skill_name}}
description: Think a {{org}} question through with a person, on what the {{world_name}} world already holds - a new product, a change to one, a new direction, or what is decided about a part. Use when someone says "design", "what if we", "should we add", "how should this work", "I want to think about", brings a new feature or idea, or asks what is decided about something. Not for doing work already decided ({{work_skill_name}}).
---

# {{design_skill_name}}: thinking a design through

A design talk goes well when you know what the world holds before you speak, take the ask at its full size, and leave a record someone else can act on. It goes badly in one common way: an answer written from the ask alone, beside decisions the world already held.

A plain lookup ("what is decided about X?") is moves 1 and 2 only.

## Before the first move: read

- Run `{{skill_name}}` first if you have not this session: it gives you your Character, your role, your lenses and what changed.
- Read yourself, not through a helper: the elements the ask touches, their links, and what hangs under them.
<!-- if folder -->
- Search the world's files for the person's own words and for any key they name (a ticket, a screen): `grep -ril "<word>" {{world_folder}}elements/`.
- What is under a part: the files whose `parent_object` is its id.
- Open questions are work items: the Relation files with supertype `Work item` and subtype `open` or `taken` that name the part (in `x_packet_elements` or a link field).
<!-- end -->
<!-- if online -->
- Search the world for the person's own words and any key they name: `GET /search?q=<words>&limit=200` finds the elements whose name or text holds every word whole, ignoring case; `truncated` true means more matched than came back. A hit carries only a snippet, and a key with a hyphen is searched as two words: read the hits (`GET /<type>?ids=<hit ids>&fields=id,name,description`) and keep those that hold the key whole. Nothing found is not proof: read the parts the ask names.
- What is under a part: `GET /object?parent_object=<its id>`.
- Open questions are work items: page `GET /relation?supertype=Work%20item&subtype=open` and keep those that name the part (in `x_packet_elements` or a link field).
<!-- end -->
- A part's design state is its `subtype`: `in design` or `locked`. An unset state is not stated: say so, and do not build on it as locked; the keeper's AI sets it when it next completes a report that touches the part. A locked part can still change: say that it is locked, and that changing it is a decision for whoever owns it.
- How far something is built is not in the world. Read that where it lives ({{elsewhere}}) when it matters, or say you have not.

## The five moves

1. **Say the size back first**, in one sentence ("this is a new product, not a change to one"), and let the person correct you. A small ask may go to details soon; a large one may not.
2. **Say what is already decided** that touches the ask, and what the world does not hold. A few lines, each with where you read it; not an inventory. "The world does not hold this" is an answer. Never say someone was asked, or agreed, unless you read it.
3. **Widen the scope; do not execute it yet.** People bring a narrow ask, and the real question is usually wider: what is this for, where does it start from, what would make it a success. Take from the world what it can tell you, then ask the person at most three questions, told as a story about one person who would use it ("a new customer opens it on their first morning: what do they need to see?"). Offer the wider frame yourself and ask if it is right. When the frame is clear and they want details, go to details.
4. **Stay in the person's lane.** Think the whole question through with them, whatever their role. What another role decides, you write as a question for whoever owns that part (a Role's holders; unsure: the keeper), never as a spec and never as a settled line.
5. **End by filing.** When the talk decided or opened something, hand in a report as `{{work_skill_name}}` says, its text holding: what was decided; what is open, each with who decides it (the keeper's AI makes each a work item on its part); what in the world should change because of this talk.

## A large design: its anchor

A large design starts by placing its anchor: the element the thing will become (in this world, a Product: `object`, supertype `Product`), never a separate design element that would age beside it. It carries `subtype` `in design`, and its description, after its `Source:` line, holds four short lines:

```
For: <what it is for>
Who: <who it is for>
From: <what it starts from>
Fixed: <what is already fixed>
```

Name the anchor and its four lines in your report; the keeper places it in the world. From then on everything about it hangs there: each open question is a work item that names it, each session's report links it, and the parts under it link to it as their `parent_object`. It is done when its parts are `locked`.

You change the world yourself only if you are the keeper's AI (the Charter says who). Otherwise the report is how your work arrives.
