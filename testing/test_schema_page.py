"""The generated schema page says what schema.json says, and carries nothing from inside.

1. consistency.py's own loader, run on knowledge/schema-reference.md, returns exactly the link
   fields and date fields that schema-dist's schema.json holds at the tag in the page's header,
   for every type; and the page lists every field of every type, no more, no fewer.
2. The page carries no `../` pointer and no word the public-material gate refuses
   (keel's codegen/public_words.py; set OW_PUBLIC_WORDS to its path, or keep keel beside
   this repo).
3. The page is what gen_schema_page.py writes at that tag (the same test as --check).

Needs the network (raw.githubusercontent.com). Runs under pytest, or alone:
    python testing/test_schema_page.py

Python 3.12, stdlib only.
"""
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ beside the skills this test imports
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "knowledge" / "schema-reference.md"
sys.path.insert(0, str(HERE))
import gen_schema_page as gen  # noqa: E402

# consistency.py moves from its own skill into read in 5.0; the test follows it.
CONSISTENCY = [ROOT / "skills" / "onlyworlds-read" / "scripts" / "consistency.py",
               ROOT / "skills" / "onlyworlds-consistency" / "scripts" / "consistency.py"]
FIELD_LINE = re.compile(r"^- (\w+)(?: \+ (\w+))? \(")


def page_text():
    return PAGE.read_bytes().decode("utf-8").replace("\r\n", "\n")


def release():
    m = gen.TAG_LINE.search(page_text())
    assert m, "the page names no schema-dist release in its header"
    tag = m.group(1)
    schema, version, sha, _, _ = gen.load_release(tag)
    return tag, schema, sha


def load_schema_fn():
    for p in CONSISTENCY:
        if p.exists():
            spec = importlib.util.spec_from_file_location("consistency_under_test", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.load_schema
    raise AssertionError(f"consistency.py not found at {[str(p) for p in CONSISTENCY]}")


def expected(schema):
    links, dates = {}, {}
    for t, fields in schema["types"].items():
        links[t] = {f["name"]: (f["kind"], f["target"]) for f in fields
                    if f["kind"] in ("single", "multi")}
        dates[t] = [f["name"] for f in fields if f["kind"] == "scalar_int"
                    and (f["name"] == "date" or f["name"].endswith("_date"))]
    return links, dates


def page_fields():
    """{type: [field names as data spells them]} read off the page's `- name (` lines."""
    out, cur = {}, None
    for line in page_text().splitlines():
        h = re.match(r"^## ([A-Z]+)\s*$", line)
        if h:
            cur = h.group(1).lower()
            out[cur] = []
            continue
        if line.startswith("## "):
            cur = None
            continue
        m = FIELD_LINE.match(line)
        if cur and m:
            out[cur] += [n for n in m.groups() if n]
    return out


def test_loader_matches_schema_json():
    tag, schema, sha = release()
    assert f"`{sha}`" in page_text(), "the header's sha256 is not the manifest's"
    links, dates, unmapped = load_schema_fn()(PAGE)
    want_links, want_dates = expected(schema)
    assert unmapped == [], f"fields the loader could not map: {unmapped}"
    assert sorted(links) == sorted(want_links), "types differ"
    for t in want_links:
        assert links[t] == want_links[t], f"{t} links: page {links[t]} vs schema.json {want_links[t]}"
        assert dates[t] == want_dates[t], f"{t} dates: page {dates[t]} vs schema.json {want_dates[t]}"
    got = page_fields()
    for t, fields in schema["types"].items():
        names = []
        for f in fields:
            names += [f["type_key"], f["id_key"]] if f["kind"] == "generic" else [f["name"]]
        assert got.get(t) == names, f"{t} fields: page {got.get(t)} vs schema.json {names}"


def test_no_pointer_and_no_inside_word():
    text = page_text()
    assert "../" not in text, "the page carries a ../ pointer"
    words = Path(os.environ.get("OW_PUBLIC_WORDS")
                 or ROOT.parent / "keel" / "codegen" / "public_words.py")
    assert words.exists(), f"public_words.py not found at {words}; set OW_PUBLIC_WORDS"
    r = subprocess.run([sys.executable, str(words), str(PAGE)], capture_output=True, text=True)
    assert r.returncode == 0, f"inside words in the page:\n{r.stdout}{r.stderr}"


def test_page_is_generated():
    tag, _, _ = release()
    status, _, _ = gen.build(ROOT, tag, check=True)
    assert status == "same", "the page differs from a fresh generation; run testing/gen_schema_page.py"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests =[v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
