"""Find where a world folder contradicts itself: dates, places, names, links.

Reads a world folder (world.json + elements/<type>/*.json, plus a legacy spatial/ folder) and
prints a Markdown report: counts at the top, one section per class, one line per finding. Each
finding names the file, the field, the two values that disagree, and the other element.
"possible" findings are questions, not verdicts. It writes nothing and always exits 0 on a
report (2 only when the folder cannot be read): a report, not a gate.

The link fields and date fields come from the skill's own copy of the schema reference
(../knowledge/schema-reference.md), so the check follows the schema the toolkit ships.

Usage:
    python consistency.py WORLD_FOLDER [--dates] [--places] [--names] [--links]
                          [--json] [--mutual Type.field ...] [--schema PATH]

    No class flag runs all four; one or more flags run only those.
    --mutual Character.friends  treats that field as mutual in this world (the schema names
                                no field as mutual, so nothing is checked for it by default).

Python 3, stdlib only.
"""
import json
import re
import sys
from pathlib import Path

CLASSES = ("dates", "places", "names", "links")
SPATIAL = {"map", "pin", "marker"}
TYPES = ["ability", "character", "collective", "construct", "creature", "event", "family",
         "institution", "language", "law", "location", "map", "marker", "narrative", "object",
         "phenomenon", "pin", "relation", "species", "title", "trait", "zone"]
PLURAL = {t + "s": t for t in TYPES}
PLURAL.update({"abilities": "ability", "families": "family", "phenomena": "phenomenon",
               "species": "species"})
PLACE_FIELDS = {"location", "parent_location"}
LINK_RE = re.compile(r"^- (\w+) \((single|multi)-link → (\w+)\)")
INT_RE = re.compile(r"^- (\w+) \(integer\)")
INT_TOKEN = re.compile(r"(?<![\w.\-])-?\d+(?!\w|\.\d)")
DECEASED = re.compile(r"^\s*\[deceased\]", re.I)
YEAR_AFTER = re.compile(r"^\s*(-?\d+)(?!\w|\.\d)")
DEATH_FIELD = {"character": "physicality", "creature": "status"}
DEATH_LINE = re.compile(r"\b(death|died)\b", re.I)


# ---------------------------------------------------------------- reading

def read_json(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return json.loads(fh.read())


def load_schema(path):
    """Link fields {type: {field: (single|multi, target)}} and date fields {type: [field]}."""
    with open(path, encoding="utf-8", newline="") as fh:
        lines = fh.read().splitlines()
    links, dates, unmapped = {}, {}, []
    cur, involves = None, False
    for line in lines:
        h = re.match(r"^## ([A-Z]+)\s*$", line)
        if h:
            cur = h.group(1).lower() if h.group(1).lower() in TYPES else None
            involves = False
            if cur:
                links.setdefault(cur, {})
                dates.setdefault(cur, [])
            continue
        if not cur:
            continue
        s = line.strip()
        if s.startswith("**Involves"):
            involves = True
            continue
        names = None
        if involves and s and not s.startswith("**"):
            names, involves = s, False
        elif s.startswith("- multi-link fields:"):
            names = s.split(":", 1)[1]
        if names is not None:
            for n in (x.strip() for x in names.split(",")):
                if n in PLURAL:
                    links[cur][n] = ("multi", PLURAL[n])
                elif n:
                    unmapped.append(f"{cur}.{n}")
            continue
        m = LINK_RE.match(s)
        if m:
            links[cur][m.group(1)] = (m.group(2), m.group(3).lower())
            continue
        m = INT_RE.match(s)
        if m and (m.group(1) == "date" or m.group(1).endswith("_date")):
            dates[cur].append(m.group(1))
    return links, dates, unmapped


def load_world(folder):
    world = {}
    if (folder / "world.json").exists():
        world = read_json(folder / "world.json")
    elements, skipped = {}, []
    for base in ("elements", "spatial"):
        for f in sorted((folder / base).glob("*/*.json")):
            try:
                d = read_json(f)
            except (ValueError, OSError) as e:
                skipped.append(f"{f.relative_to(folder).as_posix()}: does not parse ({e})")
                continue
            if not isinstance(d, dict) or not d.get("id"):
                skipped.append(f"{f.relative_to(folder).as_posix()}: no id")
                continue
            t = str(d.get("type") or f.parent.name).lower()
            rel = f.relative_to(folder).as_posix()
            if rel.startswith("elements/"):
                rel = rel[len("elements/"):]
            if d["id"] in elements:
                skipped.append(f"{rel}: id {d['id']} also in {elements[d['id']]['_file']}")
                continue
            d["_type"], d["_file"] = t, rel
            # Atlas's older pin and marker spellings (world-folder.md, writer rules)
            for old, new in (("map_id", "map"), ("zone_id", "zone")):
                if old in d and new not in d:
                    d[new] = d[old]
            elements[d["id"]] = d
    return world, elements, skipped


# ---------------------------------------------------------------- helpers

def an(word):
    return ("an " if word[:1] in "aeiou" else "a ") + word


def label(e):
    return e.get("name") or f"(unnamed {str(e['id'])[:8]})"


def ref(e):
    return {"id": e["id"], "name": label(e), "type": e["_type"], "file": e["_file"]}


def as_int(v):
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


def ids_of(v):
    if isinstance(v, str):
        return [v] if v else []
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str) and x]
    return []


class Report:
    def __init__(self):
        self.findings = {c: [] for c in CLASSES}

    def add(self, cls, level, e, field, value, other_value, other=None, text=""):
        self.findings[cls].append({
            "level": level, "file": e["_file"], "element": ref(e), "field": field,
            "value": value, "other_value": other_value,
            "other": ref(other) if other else None,
            "message": f"{text} ({e['_file']})"})


def death_of(e):
    """(is_dead, death_date or None, field) under the schema skill's convention: a
    "[Deceased] " prefix on a Character's physicality or a Creature's status marks the death.
    The date: a year right after the prefix; else background's death line (one naming death
    or died, with one year), where the convention writes it; else a lone integer in the rest
    of the field."""
    field = DEATH_FIELD.get(e["_type"])
    m = DECEASED.match(str(e.get(field) or "")) if field else None
    if not m:
        return False, None, None
    rest = str(e[field])[m.end():]
    y = YEAR_AFTER.match(rest)
    if y:
        return True, int(y.group(1)), field
    for line in str(e.get("background") or "").splitlines():
        if DEATH_LINE.search(line):
            years = INT_TOKEN.findall(line)
            if len(years) == 1:
                return True, int(years[0]), "background"
    nums = INT_TOKEN.findall(rest)
    if len(nums) == 1:
        return True, int(nums[0]), field
    return True, None, field


# ---------------------------------------------------------------- the classes

def check_dates(els, world, dates_by_type, links, rep, notes):
    lo, hi = as_int(world.get("time_range_min")), as_int(world.get("time_range_max"))
    if lo is None or hi is None:
        notes.append("dates: the world has no time_range_min/time_range_max; the range check was skipped")
    births = {}
    for e in els.values():
        n = label(e)
        for f in dates_by_type.get(e["_type"], []):
            v = as_int(e.get(f))
            if v is None:
                continue
            if lo is not None and v < lo:
                rep.add("dates", "contradiction", e, f, v, lo,
                        text=f"{n}'s {f} {v} is before the world's time_range_min {lo}")
            if hi is not None and v > hi:
                rep.add("dates", "contradiction", e, f, v, hi,
                        text=f"{n}'s {f} {v} is after the world's time_range_max {hi}")
        for a, b in (("start_date", "end_date"), ("grant_date", "revoke_date")):
            va, vb = as_int(e.get(a)), as_int(e.get(b))
            if va is not None and vb is not None and vb < va:
                rep.add("dates", "contradiction", e, b, vb, va,
                        text=f"{n}'s {b} {vb} is before its {a} {va}")
        if e["_type"] in ("character", "creature"):
            birth = as_int(e.get("birth_date"))
            dead, death, where = death_of(e)
            if birth is not None:
                births[e["id"]] = birth
            if dead and birth is not None and death is not None and birth > death:
                rep.add("dates", "contradiction", e, "birth_date", birth, death,
                        text=f"{n}'s birth_date {birth} is after the death date {death} in its {where}")
    # an Event or Relation dated before the birth of a Character it links
    for e in els.values():
        if e["_type"] not in ("event", "relation"):
            continue
        start = as_int(e.get("start_date"))
        if start is None:
            continue
        via = {}
        for f, (_, target) in links.get(e["_type"], {}).items():
            if target == "character":
                for i in ids_of(e.get(f)):
                    via.setdefault(i, []).append(f)
        for i, fs in via.items():
            c = els.get(i)
            if c and i in births and start < births[i]:
                rep.add("dates", "possible", e, "start_date", start, births[i], c,
                        text=f"possible: {label(e)}'s start_date {start} is before the birth_date "
                             f"{births[i]} of {label(c)} ({c['id']}), linked in its {' and '.join(fs)}")


def check_places(els, rep):
    for e in els.values():
        for f in PLACE_FIELDS:
            for i in ids_of(e.get(f)):
                t = els.get(i)
                if t is None:
                    rep.add("places", "contradiction", e, f, i, None,
                            text=f"{label(e)}'s {f} {i} names no element in the folder")
                elif t["_type"] != "location":
                    rep.add("places", "contradiction", e, f, i, t["_type"], t,
                            text=f"{label(e)}'s {f} is {label(t)} ({i}), {an(t['_type'])}, not a Location")
    seen = set()
    for start in els.values():
        if start["_type"] != "location" or start["id"] in seen:
            continue
        path, cur = [], start
        while cur is not None and cur["id"] not in seen:
            if cur in path:
                cyc = path[path.index(cur):]
                chain = " -> ".join(label(x) for x in cyc + [cur])
                head = cyc[0]
                nxt = cyc[1] if len(cyc) > 1 else head
                rep.add("places", "contradiction", head, "parent_location", nxt["id"],
                        head["id"], nxt,
                        text=f"{label(head)}'s parent_location {label(nxt)} ({nxt['id']}) leads "
                             f"back to {label(head)}: the cycle {chain}")
                break
            path.append(cur)
            p = cur.get("parent_location")
            cur = els.get(p) if isinstance(p, str) else None
            if cur is not None and cur["_type"] != "location":
                cur = None
        seen.update(x["id"] for x in path)


def within_one(a, b):
    if abs(len(a) - len(b)) > 1 or a == b:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1:]


def contains_words(short, long):
    return re.search(r"(?<!\w)" + re.escape(short) + r"(?!\w)", long) is not None


def check_names(els, rep, notes):
    by_type = {}
    for e in els.values():
        if e["_type"] in SPATIAL or not e.get("name"):
            continue
        key = " ".join(str(e["name"]).casefold().split())
        by_type.setdefault(e["_type"], []).append((key, e))
    notes.append("names: map, pin and marker are skipped (numbered by design)")
    for t, items in by_type.items():
        items.sort(key=lambda x: (x[0], x[1]["id"]))
        for i, (ka, a) in enumerate(items):
            for kb, b in items[i + 1:]:
                if ka == kb:
                    rep.add("names", "contradiction", b, "name", b["name"], a["name"], a,
                            text=f"two {t} elements share the name '{b['name']}': this one and "
                                 f"{label(a)} ({a['id']}, {a['_file']})")
                elif within_one(ka, kb) or (min(len(ka), len(kb)) >= 3 and (
                        contains_words(ka, kb) or contains_words(kb, ka))):
                    rep.add("names", "possible", b, "name", b["name"], a["name"], a,
                            text=f"possible: {t} '{b['name']}' is close to '{a['name']}' "
                                 f"({a['id']}, {a['_file']}); the same thing twice?")


def count_links(els, links):
    n = sum(len(ids_of(e.get(f))) for e in els.values() for f in links.get(e["_type"], {}))
    return n + sum(1 for e in els.values() if e["_type"] == "pin" and e.get("element_id"))


def check_links(els, links, rep, notes, mutual):
    for e in els.values():
        fields = links.get(e["_type"], {})
        for f, (_, target) in fields.items():
            for i in ids_of(e.get(f)):
                if f in PLACE_FIELDS:
                    continue  # places owns location and parent_location
                t = els.get(i)
                if t is None:
                    rep.add("links", "contradiction", e, f, i, None,
                            text=f"{label(e)}'s {f} holds {i}, which names no element in the folder")
                elif t["_type"] != target:
                    rep.add("links", "contradiction", e, f, i, t["_type"], t,
                            text=f"{label(e)}'s {f} points at {label(t)} ({i}), {an(t['_type'])}, "
                                 f"where the schema expects {an(target)}")
        if e["_type"] == "pin" and e.get("element_id"):
            i, want = e["element_id"], str(e.get("element_type") or "").lower()
            t = els.get(i)
            if t is None:
                rep.add("links", "contradiction", e, "element_id", i, None,
                        text=f"{label(e)}'s element_id holds {i}, which names no element in the folder")
            elif want and t["_type"] != want:
                rep.add("links", "contradiction", e, "element_type", want, t["_type"], t,
                        text=f"{label(e)}'s element_type {want} does not match {label(t)} ({i}), {an(t['_type'])}")
        if e["_type"] == "relation" and isinstance(e.get("actor"), str) and e["actor"]:
            for f, (_, target) in fields.items():
                if f != "actor" and e["actor"] in ids_of(e.get(f)):
                    o = els.get(e["actor"])
                    rep.add("links", "contradiction", e, f, e["actor"], "actor", o,
                            text=f"{label(e)} has {label(o) if o else e['actor']} at both ends "
                                 f"(actor and {f})")
    if mutual:
        for t, fs in mutual.items():
            for f in fs:
                if links.get(t, {}).get(f, (None, None))[1] != t:
                    notes.append(f"links: --mutual {t}.{f} skipped; it is not a link from {t} to {t} in the schema")
        for e in els.values():
            for f in mutual.get(e["_type"], []):
                for i in ids_of(e.get(f)):
                    t = els.get(i)
                    if t and t["_type"] == e["_type"] and f in t and e["id"] not in ids_of(t.get(f)):
                        rep.add("links", "contradiction", e, f, i, "missing", t,
                                text=f"{label(e)} lists {label(t)} ({i}) in {f}; {label(t)}'s {f} "
                                     f"does not list {label(e)} (declared mutual)")
    else:
        notes.append("links: one-way bonds not checked; the schema names no field as mutual "
                     "(pass --mutual Character.friends if this world treats it so)")


def text_reads(els, links):
    """Dead elements and who links to them: the model's reading list for the text class."""
    dead = {i: e for i, e in els.items() if death_of(e)[0]}
    out = []
    for i, d in dead.items():
        refs = []
        for e in els.values():
            for f in links.get(e["_type"], {}):
                if i in ids_of(e.get(f)):
                    refs.append(f"{label(e)} ({e['_file']}, {f})")
        out.append({"element": ref(d), "linked_from": refs})
    return out


# ---------------------------------------------------------------- output

def markdown(world, n_el, n_links, rep, run, notes, skipped, reads):
    c = sum(1 for k in run for x in rep.findings[k] if x["level"] == "contradiction")
    p = sum(1 for k in run for x in rep.findings[k] if x["level"] == "possible")
    out = [f"# Consistency: {world.get('name') or '(unnamed world)'}", "",
           f"Checked {n_el} elements, {n_links} links; {c} contradictions, {p} possible.",
           f"Classes run: {', '.join(run)}."]
    for k in run:
        out += ["", f"## {k}", ""]
        items = rep.findings[k]
        out += [f"- {x['message']}" for x in items] or ["- none found"]
    if reads:
        out += ["", "## text (for the model to read, not findings)", ""]
        for r in reads:
            e = r["element"]
            refs = "; ".join(r["linked_from"]) or "nothing links to it"
            out.append(f"- {e['name']} is marked dead ({e['file']}); linked from: {refs}")
    if notes or skipped:
        out += ["", "## not checked", ""] + [f"- {x}" for x in notes + skipped]
    return "\n".join(out) + "\n"


def main(argv):
    args, run, mutual_raw, schema, as_json = [], [], [], None, False
    it = iter(argv)
    for a in it:
        if a == "--json":
            as_json = True
        elif a == "--mutual":
            mutual_raw.append(next(it, ""))
        elif a == "--schema":
            schema = next(it, None)
        elif a.startswith("--") and a[2:] in CLASSES:
            run.append(a[2:])
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
    run = [c for c in CLASSES if c in run] or list(CLASSES)
    schema = Path(schema) if schema else Path(__file__).resolve().parent.parent / "knowledge" / "schema-reference.md"
    if not schema.exists():
        print(f"schema reference not found at {schema}; pass --schema PATH")
        return 2
    links, dates, unmapped = load_schema(schema)
    world, els, skipped = load_world(folder)
    notes = [f"schema: involves field {u} maps to no type" for u in unmapped]
    mutual = {}
    for m in mutual_raw:
        t, _, f = m.partition(".")
        mutual.setdefault(t.lower(), []).append(f)
    rep = Report()
    n_links = count_links(els, links)
    if "links" in run:
        check_links(els, links, rep, notes, mutual)
    if "dates" in run:
        check_dates(els, world, dates, links, rep, notes)
    if "places" in run:
        check_places(els, rep)
    if "names" in run:
        check_names(els, rep, notes)
    reads = text_reads(els, links)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if as_json:
        c = sum(1 for k in run for x in rep.findings[k] if x["level"] == "contradiction")
        p = sum(1 for k in run for x in rep.findings[k] if x["level"] == "possible")
        print(json.dumps({"world": world.get("name"), "elements": len(els), "links": n_links,
                          "contradictions": c, "possible": p, "classes": run,
                          "findings": {k: rep.findings[k] for k in run}, "text_reads": reads,
                          "not_checked": notes + skipped}, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(markdown(world, len(els), n_links, rep, run, notes, skipped, reads))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
