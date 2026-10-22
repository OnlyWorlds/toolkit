"""Write a new world folder from a starter pack and a filled plan (the onlyworlds-setup skill).

    python write_world.py PLAN.json OUT_FOLDER [--bulk BULK.json]

The model fills the plan from the interview; this script does the counting: it mints the ids,
fills every placeholder, writes each file by the folder format's writer rules, checks the size
budget, and writes the harness copies of the world skill. It refuses, and writes nothing, when
OUT_FOLDER already holds files, a placeholder is left unfilled, a link names no element, or the
charter or the world skill is over its budget. It never deletes anything.

The plan (JSON):

    {
      "pack": "company",                       # a folder name under ../packs/
      "today": "2026-10-22",                   # the setup day (ISO date)
      "world": {"name": "...", "slug": "...", "description": "..."},
      "values": {"org": "...", "keeper": "...", ...},   # every {{name}} the pack's texts use
      "charter": {"links": {"author": "org", "adjudicators": ["keeper-title"]}},
      "skill": {"utility": "one line: what the skill is for"},
      "elements": [
        {"key": "org", "type": "institution",
         "fields": {"name": "...", "supertype": "Company", "description": "..."},
         "links": {"parent_institution": "other-key", "characters": ["a", "b"]}}
      ],
      "copies": "project",                     # "project" (beside world.json), "none", or a folder (a home)
      "agents_md": true,                       # write the one-line AGENTS.md (never over an existing one)
      "repo": false                            # true: .gitattributes and .gitignore for a shared repository
    }

Placeholders: `{{name}}` from "values", plus the ones this script knows: world_name, world_slug,
world_id, charter_id, skill_id, skill_name (ow-<slug>), today (ISO), today_day (the day number),
and `{{id:<key>}}` for any element's id. They are filled in the charter, the skill and every
string field of every element. A date field written as "day:YYYY-MM-DD" becomes its day number:
a work world counts time in days, day 0 = 1970-01-01.

Python 3, stdlib only.
"""
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

CHARTER_MAX = 4000
SKILL_MAX = 8000
FORMAT_VERSION = "0.3.12"
EPOCH = datetime.date(1970, 1, 1)
PACKS = Path(__file__).resolve().parent.parent / "packs"
PH = re.compile(r"\{\{([a-z_]+(?::[A-Za-z0-9_-]+)?)\}\}")
DAY = re.compile(r"^day:(\d{4}-\d{2}-\d{2})$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def uuid7():
    b = bytearray(int(time.time() * 1000).to_bytes(6, "big") + os.urandom(10))
    b[6] = (b[6] & 0x0F) | 0x70
    b[8] = (b[8] & 0x3F) | 0x80
    h = b.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def day_number(iso):
    return (datetime.date.fromisoformat(iso) - EPOCH).days


def slug(text, cap=40):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower().encode("ascii", "ignore").decode()).strip("-")
    return s[:cap].strip("-")


def template(path):
    """A pack text without its leading template-note comment lines."""
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    while lines and lines[0].startswith("<!--") and lines[0].rstrip().endswith("-->"):
        lines.pop(0)
    return "\n".join(lines).strip("\n") + "\n"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def main(argv):
    bulk_arg = argv[argv.index("--bulk") + 1] if "--bulk" in argv and argv.index("--bulk") + 1 < len(argv) else None
    bulk = Path(bulk_arg) if bulk_arg else None
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and not (bulk_arg and i == argv.index("--bulk") + 1)]
    if len(args) != 2:
        sys.exit(__doc__.split("\n\n")[1])
    plan = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    out = Path(args[1])
    problems = []
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} already holds files: this script only writes new folders")
    pack = PACKS / plan["pack"]
    if not (pack / "PACK.md").exists():
        sys.exit(f"no pack {plan['pack']!r} under {PACKS}")

    w = plan["world"]
    world_slug = w.get("slug") or slug(w["name"])
    skill_name = "ow-" + world_slug
    if not SKILL_NAME.match(skill_name) or len(skill_name) > 64:
        problems.append(f"skill name {skill_name!r}: lowercase letters, digits and hyphens, 64 at most")
    today = plan["today"]
    ids = {e["key"]: uuid7() for e in plan["elements"]}
    world_id, charter_id, skill_id = uuid7(), uuid7(), uuid7()
    values = dict(plan.get("values", {}))
    values.update(world_name=w["name"], world_slug=world_slug, world_id=world_id,
                  charter_id=charter_id, skill_id=skill_id, skill_name=skill_name,
                  today=today, today_day=str(day_number(today)))

    def fill(text, where):
        def sub(m):
            name = m.group(1)
            if name.startswith("id:"):
                if name[3:] in ids:
                    return ids[name[3:]]
            elif name in values:
                return str(values[name])
            problems.append(f"{where}: {{{{{name}}}}} is not filled")
            return m.group(0)
        return PH.sub(sub, text)

    def fields_of(raw, where):
        body = {}
        for k, v in raw.items():
            if isinstance(v, str):
                m = DAY.match(v)
                body[k] = day_number(m.group(1)) if m else fill(v, f"{where}.{k}")
            else:
                body[k] = v
        return body

    def links_of(raw, where):
        body = {}
        for field, target in (raw or {}).items():
            keys = target if isinstance(target, list) else [target]
            missing = [k for k in keys if k not in ids]
            if missing:
                problems.append(f"{where}.{field}: no element with key {missing}")
                continue
            body[field] = [ids[k] for k in keys] if isinstance(target, list) else ids[target]
        return body

    charter_text = fill(template(pack / "charter.md"), "charter.md")
    skill_text = fill(template(pack / "skill.md"), "skill.md")
    if len(charter_text) >= CHARTER_MAX:
        problems.append(f"charter: {len(charter_text)} characters, the budget is under {CHARTER_MAX}")
    if len(skill_text) >= SKILL_MAX:
        problems.append(f"world skill: {len(skill_text)} characters, the budget is under {SKILL_MAX}")
    fm = re.match(r"---\n(.*?)\n---\n", skill_text, re.S)
    keys = [ln.split(":", 1)[0] for ln in fm.group(1).split("\n") if ln and not ln.startswith(" ")] if fm else []
    if keys != ["name", "description"]:
        problems.append(f"world skill front matter: keys {keys}, want exactly name and description")

    files = {}  # relative path -> text
    world_json = {"id": world_id, "name": w["name"], "description": fill(w.get("description", ""), "world"),
                  "format_version": FORMAT_VERSION, "charter": charter_id,
                  "time_basic_unit": "Day", "time_format_names": ["Day", "Week", "Year"],
                  "time_format_equivalents": [1, 7, 365], "time_range_min": 0,
                  "time_range_max": day_number("2099-12-31"), "time_current": day_number(today)}
    files["world.json"] = dump(world_json)

    charter = {"id": charter_id, "name": "Charter", "supertype": "Charter", "description": charter_text,
               "date": day_number(today)}
    charter.update(links_of(plan.get("charter", {}).get("links"), "charter"))
    files["elements/law/charter.json"] = dump(charter)
    skill = {"id": skill_id, "name": f"{w['name']} world skill", "supertype": "Skill", "description": skill_text,
             "utility": fill(plan.get("skill", {}).get("utility", "How an agent reaches this world. Copy the "
                             "description, whole, to where your harness reads skills, as SKILL.md."), "skill")}
    files[f"elements/object/{world_slug}-skill.json"] = dump(skill)

    counts = {"law": 1, "object": 1}
    taken = set(files)
    for e in plan["elements"]:
        where = e["key"]
        body = {"id": ids[e["key"]]}
        body.update(fields_of(e["fields"], where))
        body.update(links_of(e.get("links"), where))
        t = e["type"]
        name = slug(body.get("name", "")) or ids[e["key"]]
        rel = f"elements/{t}/{name}--{ids[e['key']][-8:]}.json" if name != ids[e["key"]] else f"elements/{t}/{name}.json"
        if rel in taken:
            rel = f"elements/{t}/{ids[e['key']]}.json"
        taken.add(rel)
        files[rel] = dump(body)
        counts[t] = counts.get(t, 0) + 1

    copy_text = skill_text
    if fm:
        head = fm.group(0)
        copy_text = (head + f"<!-- copied from the world: Object {skill_id}; updated_at none yet "
                     f"(made by the set-up skill on {today}) -->\n" + skill_text[len(head):])
    copies = plan.get("copies", "project")
    copy_root = None if copies == "none" else (out if copies == "project" else Path(copies))
    copy_paths = []
    if copy_root is not None:
        for harness in (".agents", ".claude"):
            p = copy_root / harness / "skills" / skill_name / "SKILL.md"
            if p.exists():
                problems.append(f"{p} exists: a copy is the user's; not overwritten")
            copy_paths.append(p)
    if plan.get("agents_md"):
        files["AGENTS.md"] = (f"This folder holds the {w['name']} world (OnlyWorlds): read its charter first "
                              f"(elements/law/charter.json, or GET /law?supertype=Charter online), "
                              f"then load the {skill_name} skill.\n")
    if plan.get("repo"):
        files[".gitattributes"] = "* text=auto eol=lf\n"
        files[".gitignore"] = ".*/\n!.agents/\n!.claude/\n.env\n.env.*\n"

    if problems:
        for p in problems:
            print("REFUSED", p)
        print(f"nothing written; {len(problems)} problem(s)")
        return 1

    for rel, text in files.items():
        write(out / rel, text)
    for p in copy_paths:
        write(p, copy_text)
    if bulk:
        items = [{"type": rel.split("/")[1], "element": json.loads(text)}
                 for rel, text in files.items() if rel.startswith("elements/")]
        if len(items) > 1000:
            print(f"bulk: {len(items)} items, over 1000 a request: split it before sending")
        write(bulk, json.dumps({"items": items}, ensure_ascii=True, indent=1) + "\n")
    n = sum(1 for r in files if r.startswith("elements/"))
    print(f"wrote {out}: world.json and {n} elements ({', '.join(f'{t} {c}' for t, c in sorted(counts.items()))})")
    print(f"charter {len(charter_text)} of under {CHARTER_MAX} characters; "
          f"world skill {len(skill_text)} of under {SKILL_MAX}; skill name {skill_name}")
    for p in copy_paths:
        print(f"copy: {p}")
    if bulk:
        print(f"bulk body: {bulk} ({n} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
