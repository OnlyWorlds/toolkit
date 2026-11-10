<!-- template: the design skill for the software-project pack; onlyworlds-setup fills it with write_world.py, which drops this line and keeps only the placement's lines -->
---
name: {{design_skill_name}}
description: Think a {{project}} design question through with a person, on what the {{world_name}} world already holds - a new component, a change to one, a decision to make or revisit, or what is decided about a part. Use when someone says "design", "what if we", "should we add", "how should this work", "I want to think about", brings a new feature or idea, or asks what is decided about something. Not for doing work already decided ({{work_skill_name}}).
---

# {{design_skill_name}}: thinking a design through

A design talk goes well when you know what the world holds before you speak, take the ask at its full size, and leave a record someone else can act on. It goes badly in one common way: an answer written from the ask alone, beside decisions the world already held.

A plain lookup ("what is decided about X?") is moves 1 and 2 only.

## Before the first move: read

- Run `{{skill_name}}` first if you have not this session: it gives you your Character, your role, your lenses and what changed.
- Read yourself, not through a helper: the components the ask touches, what each depends on, who maintains it, and the decisions that name it.
<!-- if folder -->
- Search the world's files for the person's own words and for any key they name (an issue, a file): `grep -ril "<word>" {{world_folder}}elements/`.
- A decision's history: follow `parent_law` up; the files whose `parent_law` is its id amend or replace it.
- Open questions about the world itself are work items: the Relation files with supertype `Work item` and subtype `open` or `taken` that name the part.
<!-- end -->
<!-- if online -->
- Search the world for the person's own words and any key they name: `GET /search?q=<words>&limit=200` finds the elements whose name or text holds every word whole, ignoring case; `truncated` true means more matched than came back. A hit carries only a snippet, and a key with a hyphen is searched as two words: read the hits (`GET /<type>?ids=<hit ids>&fields=id,name,description`) and keep those that hold the key whole. Nothing found is not proof: read the parts the ask names.
- A decision's history: follow `parent_law` up; `GET /law?parent_law=<its id>` lists what amends or replaces it.
- Open questions about the world itself are work items: page `GET /relation?supertype=Work%20item&subtype=open` and keep those that name the part.
<!-- end -->
- The design's state is in the subtypes: a Decision `proposed` is in design, `accepted` is locked, `superseded` is history; a Component `planned` is in design. An unset state is not stated: say so, and do not build on it as locked; the keeper's AI sets it when it next completes a report that touches the part. An accepted decision can still change, by a new decision that supersedes it: say that, and that it is for the component's maintainers (its `characters`) to decide.
- How far something is built is not in the world: the code and {{tracker}} hold it. Read it there when it matters, or say you have not.

## The five moves

1. **Say the size back first**, in one sentence ("this is a new component, not a change to one"), and let the person correct you. A small ask may go to details soon; a large one may not.
2. **Say what is already decided** that touches the ask, and what the world does not hold. A few lines, each with where you read it (a decision, a commit, a path); not an inventory. "The world does not hold this" is an answer. Never say someone was asked, or agreed, unless you read it.
3. **Widen the scope; do not execute it yet.** People bring a narrow ask, and the real question is usually wider: what is this for, where does it start from, what would make it a success. Take from the world and the code what they can tell you, then ask the person at most three questions, told as a story about one person who would use it ("someone runs it on two files from different months: what do they expect to see?"). Offer the wider frame yourself and ask if it is right. When the frame is clear and they want details, go to details.
4. **Stay in the person's lane.** Think the whole question through with them, whatever their role. What another maintainer decides, you write as a question for them, never as a spec and never as a settled line. The code wins: a description that disagrees with the code is a question for the component's maintainer.
5. **End by filing.** When the talk decided or opened something, hand in a report as `{{work_skill_name}}` says, its text holding: what was decided (each a decision to record, with its why); what is open, each with who decides it (the keeper's AI makes each a work item on its part); what in the world should change because of this talk.

## A large design: its anchor

A large design starts by placing its anchor: the element the thing will become, a Component (`construct`, supertype `Component`) with `subtype` `planned`, never a separate design element that would age beside it. Its description, after its `Source:` line, holds four short lines:

```
For: <what it is for>
Who: <who it is for>
From: <what it starts from>
Fixed: <what is already fixed>
```

Name the anchor and its four lines in your report; the keeper places it in the world. From then on everything about it hangs there: each decision about it names it in its text, each open question is a work item that names it, each session's report links it.

You change the world yourself only if you are the keeper's AI (the Charter says who). Otherwise the report is how your work arrives.
