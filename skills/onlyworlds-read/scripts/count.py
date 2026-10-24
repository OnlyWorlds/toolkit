"""Count a world folder: the numbers the survey and link lenses start from.

Reads a world folder with consistency.py's loader (world.json + elements/<type>/*.json, plus a
legacy spatial/ folder, keyed on the id inside each file) and prints a Markdown report:
distribution, link degree, orphans and near-orphans, clusters, bridges and text weight. It
writes nothing; the model cites its numbers and never recounts them.

A link is any field whose value is an id, or a list of ids, found in the id map (extension
fields included). The room (the room profile: one of its eight type-and-supertype pairs AND the
mark x_room_of) and placement (map, pin, marker and zone: the draw skill's graph.py names the
same four) are dropped from the id map before counting, so their links drop with them; the
report opens with the world's whole count and the split, and says how many were left out.

The marks a world carries are named. A proposed element (x_review_proposed, the review
profile; a doubtful value counts with them) is not yet canon: left out like the room unless
asked for, and said. A known-of stub (keel's `known_of: true`) is counted but never thin and
never a link target: its unset fields are unknown, not missing. A hidden element (folder spec
4.8) is counted, since the folder's holder sees it, and the report says how many, since a brief
is often handed on.

Usage:
    python count.py WORLD_FOLDER [--top N] [--mentions] [--room] [--placement] [--proposed]
                    [--json] [--schema PATH]

    --top N      how many elements the "most linked" and "most text" tables list (default 40)
    --mentions   list ow:// mentions in a description or story that no link field backs
                 (the link lens's strongest evidence); the field names come from the skill's
                 copy of the schema reference (../knowledge/schema-reference.md)
    --room       count the room too (only when the user asks)
    --placement  count map, pin, marker and zone too (--spatial, the older name, still works)
    --proposed   count proposed elements too, each labelled "proposed, not yet reviewed"
    --json       the same report as JSON, with every list in full

Python 3, stdlib only. Exit 0 on a report, 2 when the folder cannot be read.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from consistency import ids_of, is_hidden, is_known_of, label, load_schema, load_world, review_mark  # noqa: E402

# Placement, not lore: the same four types the draw skill's graph.py leaves out.
PLACEMENT = {"map", "pin", "marker", "zone"}

ROOM_PAIRS = {("narrative", "message"), ("narrative", "board"), ("relation", "work item"),
              ("construct", "spec"), ("relation", "heart"), ("relation", "vote"),
              ("event", "sitting"), ("character", "member")}
NOT_LINKS = {"id", "world"}
MENTION = re.compile(r"\[([^\]]*)\]\(ow://([A-Za-z]+)/([0-9A-Fa-f-]{36})\)")
LIST_CAP = 150


def fold(v):
    return str(v).strip().casefold() if isinstance(v, str) else ""


def is_room(e):
    """The room profile's reader rule: the pair, trimmed and case-folded, AND a non-empty mark."""
    pair = (fold(e.get("type") or e["_type"]), fold(e.get("supertype")))
    mark = e.get("x_room_of")
    return pair in ROOM_PAIRS and isinstance(mark, str) and mark != ""


def malformed_mark(e):
    mark = e.get("x_room_of")
    return isinstance(mark, str) and mark != "" and not is_room(e)


def text_weight(e):
    return sum(len(e[f]) for f in ("description", "story") if isinstance(e.get(f), str))


def components(nodes, adj):
    seen, out = set(), []
    for n in nodes:
        if n in seen:
            continue
        stack, comp = [n], []
        seen.add(n)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        out.append(comp)
    return out


def articulation(nodes, adj):
    """{node: parts its removal splits its cluster into}, by an iterative Tarjan walk."""
    disc, low, parts, timer = {}, {}, {}, 0
    for root in nodes:
        if root in disc:
            continue
        disc[root] = low[root] = timer
        timer += 1
        root_children = 0
        stack = [(root, None, iter(sorted(adj[root])))]
        while stack:
            v, parent, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                if parent is not None:
                    low[parent] = min(low[parent], low[v])
                    if parent != root and low[v] >= disc[parent]:
                        parts[parent] = parts.get(parent, 1) + 1
                continue
            if nxt == parent:
                continue
            if nxt in disc:
                low[v] = min(low[v], disc[nxt])
            else:
                disc[nxt] = low[nxt] = timer
                timer += 1
                if v == root:
                    root_children += 1
                stack.append((nxt, v, iter(sorted(adj[nxt]))))
        if root_children >= 2:
            parts[root] = root_children
    return parts


def marks_of(e):
    """The words a row carries: what a reader of the brief must not read past."""
    words = []
    r = review_mark(e)
    if r == "proposed":
        words.append("proposed, not yet reviewed")
    elif r == "doubt":
        words.append("doubtful review mark, handed on as proposed")
    if is_known_of(e):
        words.append("known of")
    if is_hidden(e):
        words.append("hidden")
    return words


def count(folder, room=False, spatial=False, schema=None, mentions=False, proposed=False):
    world, raw, skipped = load_world(folder)
    notes = list(skipped)
    left_room = [e for e in raw.values() if is_room(e)]
    left_spatial = [e for e in raw.values() if e["_type"] in PLACEMENT and not is_room(e)]
    left_proposed = [e for e in raw.values()
                     if review_mark(e) and not is_room(e) and e["_type"] not in PLACEMENT]
    for e in raw.values():
        if malformed_mark(e):
            notes.append(f"{e['_file']}: carries x_room_of but none of the room's pairs; "
                         "a malformed mark, counted as lore")
        if review_mark(e) == "doubt":
            notes.append(f"{e['_file']}: x_review_proposed is not an object with by, evidence and "
                         "expires; a doubt, counted with the proposed (the review profile, rule 4)")
    drop = set()
    if not room:
        drop |= {e["id"] for e in left_room}
    if not spatial:
        drop |= {e["id"] for e in left_spatial}
    if not proposed:
        drop |= {e["id"] for e in left_proposed}
    els = {i: e for i, e in raw.items() if i not in drop}
    stubs = {i for i, e in els.items() if is_known_of(e)}

    out_links = {i: [] for i in els}
    in_links = {i: [] for i in els}
    adj = {i: set() for i in els}
    for i, e in els.items():
        seen = set()
        for f, v in e.items():
            if f.startswith("_") or f in NOT_LINKS:
                continue
            for t in ids_of(v):
                if t in els and t != i and (f, t) not in seen:
                    seen.add((f, t))
                    out_links[i].append((f, t))
                    in_links[t].append((f, i))
                    adj[i].add(t)
                    adj[t].add(i)

    def row(i):
        e = els[i]
        return {"id": i, "name": label(e), "type": e["_type"], "file": e["_file"],
                "out": len(out_links[i]), "in": len(in_links[i]),
                "degree": len(out_links[i]) + len(in_links[i]), "text": text_weight(e),
                "marks": marks_of(e)}

    rows = {i: row(i) for i in els}
    dist = {}
    for e in els.values():
        dist[e["_type"]] = dist.get(e["_type"], 0) + 1
    order = sorted(els, key=lambda i: (rows[i]["name"].casefold(), i))
    comps = [c for c in components(order, adj) if len(c) > 1]
    comps.sort(key=lambda c: (-len(c), min(rows[i]["name"].casefold() for i in c)))
    parts = articulation(order, adj)

    def top_of(c, n=3):
        return [rows[i]["name"] for i in sorted(c, key=lambda i: (-rows[i]["degree"], rows[i]["name"]))[:n]]

    near = []
    for i in order:
        if rows[i]["degree"] == 1 and i not in stubs:
            f, other = (out_links[i] or in_links[i])[0]
            way = "out" if out_links[i] else "in"
            near.append(dict(rows[i], link=f"{f} ({way}) {rows[other]['name']}"))

    found = []
    if mentions:
        links = {}
        if schema and schema.exists():
            links = load_schema(schema)[0]
        else:
            notes.append("mentions: no schema reference found, so no field is suggested; pass --schema PATH")
        dangling = 0
        for i in order:
            e = els[i]
            linked = {t for _, t in out_links[i]}
            for f in ("description", "story"):
                text = e.get(f) if isinstance(e.get(f), str) else ""
                for m in MENTION.finditer(text):
                    t = m.group(3)
                    if t not in raw:
                        dangling += 1
                        continue
                    if t not in els or t in linked or t == i or t in stubs:
                        continue  # a known-of stub is never a link target: its reader cannot see it whole
                    target = els[t]["_type"]
                    fields = sorted(k for k, (_, tt) in links.get(e["_type"], {}).items() if tt == target)
                    found.append({"element": rows[i], "in": f, "names": rows[t],
                                  "fields": fields})
                    linked.add(t)
        if dangling:
            notes.append(f"mentions: {dangling} ow:// mention(s) name an id not in the folder "
                         "(the consistency lens reads link fields, not prose)")

    return {
        "world": world.get("name"), "folder": str(folder),
        "total": len(raw), "placement": len(left_spatial), "elements": len(els), "links": sum(len(v) for v in out_links.values()),
        "left_out": {"room": len(left_room) if not room else 0,
                     "placement": len(left_spatial) if not spatial else 0,
                     "proposed": len(left_proposed) if not proposed else 0},
        "marks": {"hidden": sum(1 for e in els.values() if is_hidden(e)),
                  "known_of": len(stubs),
                  "proposed": len(left_proposed)},
        "distribution": dict(sorted(dist.items(), key=lambda kv: (-kv[1], kv[0]))),
        "most_linked": sorted(rows.values(), key=lambda r: (-r["degree"], r["name"].casefold())),
        "most_text": sorted((r for i, r in rows.items() if i not in stubs),
                            key=lambda r: (-r["text"], r["name"].casefold())),
        "clusters": [{"size": len(c), "top": top_of(c), "ids": sorted(c)} for c in comps],
        "bridges": sorted((dict(rows[i], splits_into=n) for i, n in parts.items()),
                          key=lambda r: (-r["splits_into"], -r["degree"], r["name"].casefold())),
        "orphans": [rows[i] for i in order if rows[i]["degree"] == 0 and i not in stubs],
        "near_orphans": near,
        "mentions": found if mentions else None,
        "notes": notes,
    }


def n_of(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def capped(items, fmt, what):
    lines = [fmt(x) for x in items[:LIST_CAP]] or ["- none"]
    if len(items) > LIST_CAP:
        lines.append(f"- and {len(items) - LIST_CAP} more {what}; --json lists every one")
    return lines


def markdown(r, top):
    out = [f"# Count: {r['world'] or '(unnamed world)'}", "",
           f"{n_of(r['total'], 'element')} in the folder, of which {r['placement']} placement "
           f"(map, pin, marker, zone). Counted {r['elements']} elements and {r['links']} links "
           f"in {r['folder']}."]
    lo = r["left_out"]
    gone = []
    if lo["room"]:
        gone.append(f"the room, {n_of(lo['room'], 'element')}")
    if lo["placement"]:
        gone.append(f"placement, {n_of(lo['placement'], 'element')}")
    if lo["proposed"]:
        gone.append(f"proposed, not yet reviewed, {n_of(lo['proposed'], 'element')} (--proposed counts them)")
    if gone:
        out.append("Left out: " + "; ".join(gone) + ".")
    mk = r["marks"]
    said = []
    if mk["hidden"]:
        said.append(f"{mk['hidden']} hidden (counted, as this folder's holder sees them; "
                    "a brief handed on says so)")
    if mk["known_of"]:
        said.append(f"{mk['known_of']} known of (stubs: their empty fields are unknown, so never "
                    "thin and never a link target)")
    if mk["proposed"] and not lo["proposed"]:
        said.append(f"{mk['proposed']} proposed, not yet reviewed (counted on request, labelled)")
    if said:
        out.append("Marks: " + "; ".join(said) + ".")
    out.append(f"Orphans {len(r['orphans'])} · near-orphans {len(r['near_orphans'])} · "
               f"clusters {len(r['clusters'])} · bridges {len(r['bridges'])}.")
    out += ["", "## Distribution", "", "| Type | Count |", "|------|-------|"]
    out += [f"| {t.capitalize()} | {n} |" for t, n in r["distribution"].items()]
    out.append(f"| **Total** | **{r['elements']}** |")
    head = "| Element | Type | Out | In | Degree | Text | File |"
    bar = "|---|---|---|---|---|---|---|"

    def named(x):
        return x["name"] + (f" ({', '.join(x['marks'])})" if x["marks"] else "")

    def line(x):
        return (f"| {named(x)} | {x['type']} | {x['out']} | {x['in']} | {x['degree']} | "
                f"{x['text']} | {x['file']} |")

    out += ["", f"## Most linked (top {top})", "", head, bar] + [line(x) for x in r["most_linked"][:top]]
    out += ["", f"## Most text (top {top}; characters of description plus story)", "", head, bar]
    out += [line(x) for x in r["most_text"][:top] if x["text"]] or ["| (no text) | | | | | | |"]
    out += ["", "## Clusters (two or more linked elements)", ""]
    out += capped(r["clusters"], lambda c: f"- {c['size']} elements, led by {', '.join(c['top'])}",
                  "clusters")
    out += ["", "## Bridges (removing one splits its cluster)", ""]
    out += capped(r["bridges"], lambda x: f"- {x['name']} ({x['type']}, degree {x['degree']}): "
                  f"splits its cluster into {x['splits_into']} ({x['file']})", "bridges")
    out += ["", "## Orphans (no link in or out)", ""]
    out += capped(r["orphans"], lambda x: f"- {named(x)} ({x['type']}, {x['file']})", "orphans")
    out += ["", "## Near-orphans (one link)", ""]
    out += capped(r["near_orphans"], lambda x: f"- {named(x)} ({x['type']}): {x['link']} "
                  f"({x['file']})", "near-orphans")
    if r["mentions"] is not None:
        out += ["", "## Mentions no link backs (ow:// in a description or story)", ""]
        out += capped(r["mentions"], lambda m: (
            f"- {m['element']['name']} ({m['element']['type']}) mentions {m['names']['name']} "
            f"({m['names']['type']}) in its {m['in']}; candidate fields: "
            f"{', '.join(m['fields']) or 'none on this type'} ({m['element']['file']})"), "mentions")
    if r["notes"]:
        out += ["", "## Not counted", ""] + [f"- {n}" for n in r["notes"]]
    return "\n".join(out) + "\n"


def main(argv):
    args, top, room, spatial, mentions, as_json, schema, proposed = [], 40, False, False, False, False, None, False
    it = iter(argv)
    for a in it:
        if a == "--top":
            try:
                top = int(next(it, "40"))
            except ValueError:
                print(f"--top takes a number\n{__doc__}")
                return 2
        elif a == "--room":
            room = True
        elif a in ("--placement", "--spatial"):
            spatial = True
        elif a == "--mentions":
            mentions = True
        elif a == "--proposed":
            proposed = True
        elif a == "--json":
            as_json = True
        elif a == "--schema":
            schema = next(it, None)
        elif a.startswith("-"):
            print(f"unknown option {a}\n{__doc__}")
            return 2
        else:
            args.append(a)
    if len(args) != 1:
        print(__doc__)
        return 2
    folder = Path(args[0])
    if not (folder / "world.json").exists() and not (folder / "elements").is_dir():
        print(f"{folder}: no world.json or elements/ here. Point at the world's own folder "
              "(for Atlas, the world's subfolder, not the onlyworlds-atlas/ wrapper).")
        return 2
    schema = Path(schema) if schema else Path(__file__).resolve().parent.parent / "knowledge" / "schema-reference.md"
    r = count(folder, room=room, spatial=spatial, schema=schema, mentions=mentions, proposed=proposed)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if as_json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(markdown(r, top))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
