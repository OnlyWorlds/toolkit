"""Write knowledge/schema-reference.md from schema-dist's schema.json at a pinned release.

The page is generated, never edited by hand. Its source is one schema-dist release:

    https://raw.githubusercontent.com/OnlyWorlds/schema-dist/<tag>/schema.json
    https://raw.githubusercontent.com/OnlyWorlds/schema-dist/<tag>/VERSION
    https://raw.githubusercontent.com/OnlyWorlds/schema-dist/<tag>/MANIFEST.json

schema.json is checked against the sha256 MANIFEST.json lists for it, and a mismatch stops
the run. schema.json is the dist's own walk (walk/schema_walk.py) already run over the
schema YAMLs, so this script reads the walk's result and decodes nothing itself. The keys it
reads: `kinds` (what each kind means), `base` (the shared fields), and `types` (each type's
fields in YAML order); per field `name`, `kind`, `target`, `section`, `desc`, `required`, and
for the generic link `type_key` and `id_key`. `--walk` also runs the walk itself at the tag
(it needs PyYAML) and stops unless its output equals schema.json byte for byte.

The page's grammar is what skills/*/scripts/consistency.py parses: `## TYPE` headings, one
field per line as `- field (single-link → Type)`, `- field (multi-link → Type)`,
`- field (integer)`, `- field (text)`. Groups are `### Section` lines, so no line starts
with `**Involves`, which that parser reads as a comma list.

The page's `Generated` date changes only when the page's content does, so two runs at one
tag write the same bytes. The page is written with LF endings.

Usage:
    python testing/gen_schema_page.py [--tag TAG] [--walk] [TOOLKIT_DIR]
    python testing/gen_schema_page.py --check [--tag TAG] [TOOLKIT_DIR]

    --tag    a schema-dist release tag (default: the newest release; with --check, the tag
             in the page's own header)
    --check  regenerate in memory; exit 1 if the page on disk differs
    --walk   also run the dist's walk at the tag and compare it with schema.json

Python 3.12, stdlib only (PyYAML for --walk alone).
"""
import datetime
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/OnlyWorlds/schema-dist/{tag}/{path}"
LATEST = "https://api.github.com/repos/OnlyWorlds/schema-dist/releases/latest"
UA = "onlyworlds-toolkit-gen-schema-page/1.0"
PAGE = Path("knowledge") / "schema-reference.md"

# The page's type order (alphabetical, as before 5.0). A type schema.json adds or drops stops
# the run rather than vanishing from the page.
ORDER = ["ability", "character", "collective", "construct", "creature", "event", "family",
         "institution", "language", "law", "location", "map", "marker", "narrative", "object",
         "phenomenon", "pin", "relation", "species", "title", "trait", "zone"]

KIND_LABEL = {"scalar_str": "text", "scalar_int": "integer"}

# Fields that do not exist, the common mistakes. Each claim is checked against schema.json:
# (type, the missing field, the type that holds the bond, its field). When the holder is
# another type, its field must link to the first type; when it is the same type, the field
# must exist.
NOT_FIELDS = [
    ("character", "titles", "title", "holders"),
    ("character", "status", "creature", "status"),
    ("object", "constructs", "construct", "objects"),
    ("location", "zones", "location", "zone"),
    ("ability", "characters", "character", "abilities"),
    ("law", "institutions", "law", "author"),
]

# One-sided bonds the Link Direction table shows: the type that holds the field, and the field.
DIRECTIONS = [
    ("character", "abilities"),
    ("character", "species"),
    ("character", "objects"),
    ("construct", "objects"),
    ("title", "holders"),
    ("object", "location"),
    ("law", "author"),
]

TAG_LINE = re.compile(r"^\*\*Release\*\*: schema-dist (\S+) ", re.M)
GEN_LINE = re.compile(r"^\*\*Generated\*\*: (\d{4}-\d{2}-\d{2}) ", re.M)


def die(msg):
    print(f"gen_schema_page: {msg}", file=sys.stderr)
    raise SystemExit(2)


def fetch(url, tries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for n in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            die(f"{url} answered {e.code}")
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if n == tries:
                die(f"{url} did not answer after {tries} tries ({getattr(e, 'reason', e)})")


def latest_tag():
    return json.loads(fetch(LATEST))["tag_name"]


def fetch_verified(tag, path, manifest):
    """One dist file at the tag, checked against the sha256 MANIFEST.json lists for it."""
    want = manifest["files"].get(path)
    if not want:
        die(f"MANIFEST.json at {tag} lists no {path}")
    data = fetch(RAW.format(tag=tag, path=path))
    got = hashlib.sha256(data).hexdigest()
    if got != want:
        die(f"{path} at {tag} has sha256 {got}; MANIFEST.json lists {want}. Refusing to generate.")
    return data


def load_release(tag):
    """(schema, version dict, schema.json sha256) for one release tag."""
    manifest = json.loads(fetch(RAW.format(tag=tag, path="MANIFEST.json")))
    raw = fetch_verified(tag, "schema.json", manifest)
    version = {}
    for line in fetch(RAW.format(tag=tag, path="VERSION")).decode("utf-8").splitlines():
        k, sep, v = line.partition(":")
        if sep:
            version[k.strip()] = v.strip()
    for k in ("canonical", "serial", "published"):
        if k not in version:
            die(f"VERSION at {tag} has no `{k}` line")
    schema = json.loads(raw)
    if sorted(schema.get("types", {})) != sorted(ORDER):
        die(f"schema.json at {tag} has types {sorted(schema.get('types', {}))}; the page knows {ORDER}")
    return schema, version, manifest["files"]["schema.json"], manifest, raw


def run_walk(tag, manifest, raw_schema):
    """Run the dist's own walk over the dist's YAMLs at the tag; it must reproduce schema.json."""
    try:
        import yaml  # noqa: F401  (the walk imports it)
    except ImportError:
        die("--walk needs PyYAML (pip install pyyaml)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "schema").mkdir()
        walk = tmp / "schema_walk.py"
        walk.write_bytes(fetch_verified(tag, "walk/schema_walk.py", manifest))
        for path in sorted(p for p in manifest["files"] if p.startswith("schema/") and p.endswith(".yaml")):
            (tmp / path).write_bytes(fetch_verified(tag, path, manifest))
        spec = importlib.util.spec_from_file_location("schema_walk_at_tag", walk)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out = mod.dumps_schema(mod.decode_schema(tmp / "schema")).encode("ascii")
    if out != raw_schema:
        die(f"the walk at {tag} does not reproduce schema.json")
    return True


def one_line(text):
    return " ".join(str(text or "").split())


def title(slug):
    return slug.capitalize()


def field_line(f):
    desc = one_line(f.get("desc"))
    req = " [Required]" if f.get("required") else ""
    kind = f["kind"]
    if kind in ("single", "multi"):
        if not f.get("target"):
            die(f"{f['name']}: a link with no target")
        head = f"- {f['name']} ({kind}-link → {title(f['target'])})"
    elif kind in KIND_LABEL:
        head = f"- {f['name']} ({KIND_LABEL[kind]})"
    elif kind == "generic":
        tk, ik = f["type_key"], f["id_key"]
        return (f"- {tk} + {ik} (generic link, any type) - {desc}. In data it is two keys, "
                f"not `{f['name']}`: `{tk}` holds the type's lowercase slug (such as "
                f"\"character\"), `{ik}` the element's id; set both or neither{req}")
    else:
        die(f"{f['name']}: kind `{kind}` the page cannot write")
    return f"{head} - {desc}{req}" if desc else head + req


def fields_of(schema, slug):
    return {f["name"]: f for f in schema["types"][slug]}


def kind_word(f):
    return f"{f['kind']}-link → {title(f['target'])}" if f["kind"] in ("single", "multi") else KIND_LABEL.get(f["kind"], f["kind"])


def not_field_lines(schema):
    out = []
    for t, missing, holder, hf in NOT_FIELDS:
        if missing in fields_of(schema, t):
            die(f"claim broken: {t} now has `{missing}`")
        h = fields_of(schema, holder).get(hf)
        if h is None:
            die(f"claim broken: {holder} has no `{hf}`")
        if holder == t:
            out.append(f"- {title(t)} has no `{missing}` field: it has `{hf}` "
                       f"({kind_word(h)}) instead.")
        elif h["kind"] in ("single", "multi"):
            if h["target"] != t:
                die(f"claim broken: {holder}.{hf} links to {h['target']}, not {t}")
            out.append(f"- {title(t)} has no `{missing}` field: the bond is "
                       f"{title(holder)}.{hf} ({kind_word(h)}), set on the {title(holder)}.")
        else:
            out.append(f"- {title(t)} has no `{missing}` field: `{hf}` is a "
                       f"{title(holder)} field.")
    return out


def direction_rows(schema):
    rows = []
    for holder, hf in DIRECTIONS:
        f = fields_of(schema, holder).get(hf)
        if f is None or f["kind"] not in ("single", "multi"):
            die(f"direction broken: {holder}.{hf} is not a link")
        tgt = f["target"]
        back = [b["name"] for b in schema["types"][tgt]
                if b["kind"] in ("single", "multi") and b.get("target") == holder]
        other = (f"{title(tgt)} has no field that links to {title(holder)}" if not back else
                 f"{title(tgt)} links to {title(holder)} only through "
                 + ", ".join(f"{title(tgt)}.{b}" for b in back)
                 + (", separate bonds" if len(back) > 1 else ", a separate bond"))
        rows.append(f"| {title(holder)} → {title(tgt)} | {title(holder)}.{hf} "
                    f"({f['kind']}-link) | {other} |")
    return rows


def render(schema, version, tag, sha, date):
    types = schema["types"]
    kinds = schema["kinds"]
    multi = {t: sum(f["kind"] == "multi" for f in types[t]) for t in ORDER}
    involves = [title(t) for t in ORDER if any(f.get("section") == "Involves" for f in types[t])]
    L = ["# OnlyWorlds Schema Reference", "",
         f"**Canonical schema**: {version['canonical']}",
         f"**Release**: schema-dist {tag} (serial {version['serial']}, published "
         f"{version['published']}), github.com/OnlyWorlds/schema-dist",
         f"**schema.json sha256**: `{sha}` (as the release's MANIFEST.json lists it)",
         f"**Generated**: {date} by `testing/gen_schema_page.py` from that release; do not edit "
         "by hand. A change to a field is a change to the schema; the page follows on the next run.",
         "",
         "Every field of the 22 element types. For a newer schema than the release above, the "
         "live `schema.json` at github.com/OnlyWorlds/schema-dist wins. Shared rules: "
         "`principles.md`.",
         "",
         "**Types**: " + " · ".join(title(t) for t in ORDER) + " (alphabetical, one `##` "
         "section each, its groups as `###`), then Fields That Do Not Exist and the Link "
         "Direction Summary.",
         "",
         "**Whitelist rule**: only the fields listed here exist. An unlisted, unprefixed field "
         "fails on import (422). Don't invent plausible-sounding fields; check this list, under "
         "the element's own type plus the Base Fields: a field listed under another type does "
         "not exist on this one (`status` is on Creature, not Character). **Exception**: fields "
         "prefixed `x_`, `atlas_` or `shadow_` are extension fields (who writes which namespace: "
         "principles §4).",
         "",
         "**One line per field**: `- name (kind) - description`. The kinds, as the schema "
         "defines them:",
         f"- `text`: {one_line(kinds['scalar_str'])}",
         f"- `integer`: {one_line(kinds['scalar_int'])}, in the world's own units (TIME, MASS, "
         "LENGTH, DISTANCE)",
         f"- `single-link → Type`: {one_line(kinds['single']).replace('`target`', 'the arrow')}",
         f"- `multi-link → Type`: {one_line(kinds['multi']).replace('`target`', 'the arrow')}",
         "- `generic link`: a link to an element of any type, carried as two keys (Pin's "
         "`element_type` + `element_id`); both set or both null",
         "",
         "---", "",
         "## Base Fields (All Elements)", "",
         "Every element has these fields; the type sections below do not repeat them.",
         ""]
    L += [field_line(f) for f in schema["base"]]
    for t in ORDER:
        L += ["", "---", "", f"## {t.upper()}"]
        section = None
        for f in types[t]:
            if f.get("section") != section:
                section = f.get("section")
                L += ["", f"### {section}", ""]
            L.append(field_line(f))
    L += ["", "---", "",
          "## Fields That Do Not Exist", "",
          "The common mistakes, each checked against the schema at the release above:", ""]
    L += not_field_lines(schema)
    top = sorted(ORDER, key=lambda t: (-multi[t], t))[:6]
    L += ["", "---", "",
          "## Link Direction Summary", "",
          "A bond is a field on one side. Set the field where it lives; the other side does not "
          "hold it.", "",
          "| Bond | The field | The other side |",
          "|------|-----------|----------------|"]
    L += direction_rows(schema)
    L += ["",
          f"**Links to most types**: {', '.join(involves[:-1])} and {involves[-1]} carry an "
          "Involves group, a multi-link field per type they touch; link from them, not to them.",
          "",
          "**Most connected types** (by multi-link field count): "
          + ", ".join(f"{title(t)} ({multi[t]})" for t in top) + "."]
    return "\n".join(L) + "\n"


def page_date(text):
    m = GEN_LINE.search(text)
    return m.group(1) if m else None


def build(root, tag, walk=False, check=False):
    """Returns (status, page text, path). status: 'same', 'written' or 'differs'."""
    path = Path(root) / PAGE
    old = path.read_bytes().decode("utf-8").replace("\r\n", "\n") if path.exists() else None
    if not tag and check and old:
        m = TAG_LINE.search(old)
        tag = m.group(1) if m else None  # --check holds the page to its own pinned tag
    tag = tag or latest_tag()
    schema, version, sha, manifest, raw = load_release(tag)
    if walk:
        run_walk(tag, manifest, raw)
    old_date = page_date(old) if old else None
    if old_date and render(schema, version, tag, sha, old_date) == old:
        return "same", old, path
    if check:
        return "differs", render(schema, version, tag, sha, old_date or "(none)"), path
    text = render(schema, version, tag, sha, datetime.date.today().isoformat())
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return "written", text, path


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    root, tag, check, walk = None, None, False, False
    it = iter(argv)
    for a in it:
        if a == "--check":
            check = True
        elif a == "--walk":
            walk = True
        elif a == "--tag":
            tag = next(it, None) or die("--tag needs a value")
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("-"):
            print(f"unknown option {a}\n{__doc__}")
            return 2
        else:
            root = a
    root = Path(root) if root else Path(__file__).resolve().parent.parent
    status, text, path = build(root, tag, walk=walk, check=check)
    if walk:
        print("the dist's walk at the tag reproduces schema.json")
    if status == "differs":
        print(f"{path}: differs from a fresh generation; run testing/gen_schema_page.py")
        return 1
    print(f"{path}: {status} ({len(text.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
