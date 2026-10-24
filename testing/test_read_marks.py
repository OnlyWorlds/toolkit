"""The read skill's counters name the marks a world carries (reads register rows 42 to 48).

The fixture `testing/read-marks/` is seven elements: Ada, who links to a hidden Wren, to Pell (an
AI seat's element still proposed, x_review_proposed) and to a known-of stub, the stranger;
Bram, whose description mentions Wren and the stranger with no link; the siege, a settled Event
whose dates run backwards; the raid, a proposed Event whose dates run backwards.

1. count.py leaves the proposed out of the counts and the top tables and says how many;
   --proposed counts them back, each labelled "proposed, not yet reviewed".
2. A known-of stub is counted but never thin (no orphan, no near-orphan, no text row) and never
   a link target (no mention candidate).
3. A hidden element is counted, named in its row, and the report says how many.
4. consistency.py reads a proposed element's disagreement as not yet canon: its own level,
   outside the contradictions, while the settled one stays a contradiction.

Runs under pytest, or alone:
    python testing/test_read_marks.py

Python 3.12, stdlib only.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "read-marks"
sys.path.insert(0, str(ROOT / "skills" / "onlyworlds-read" / "scripts"))
import consistency  # noqa: E402
import count as counter  # noqa: E402

SCHEMA = ROOT / "knowledge" / "schema-reference.md"


def names(rows):
    return sorted(r["name"] for r in rows)


def test_proposed_left_out_and_said():
    r = counter.count(FIXTURE, schema=SCHEMA)
    assert r["total"] == 7 and r["elements"] == 5, (r["total"], r["elements"])
    assert r["left_out"]["proposed"] == 2
    every = names(r["most_linked"]) + names(r["most_text"])
    assert "Pell" not in every and "The raid" not in every, every
    md = counter.markdown(r, 40)
    assert "Left out: proposed, not yet reviewed, 2 elements" in md, md


def test_proposed_counted_on_request_and_labelled():
    r = counter.count(FIXTURE, schema=SCHEMA, proposed=True)
    assert r["elements"] == 7 and r["left_out"]["proposed"] == 0
    pell = next(x for x in r["most_linked"] if x["name"] == "Pell")
    assert pell["marks"] == ["proposed, not yet reviewed"]
    assert "| Pell (proposed, not yet reviewed) |" in counter.markdown(r, 40)


def test_known_of_never_thin_never_a_target():
    r = counter.count(FIXTURE, schema=SCHEMA, mentions=True)
    assert r["marks"]["known_of"] == 1
    stub = next(x for x in r["most_linked"] if x["name"] == "The stranger")
    assert stub["marks"] == ["known of"] and stub["degree"] == 1
    assert "The stranger" not in names(r["orphans"]) + names(r["near_orphans"])
    assert "The stranger" not in names(r["most_text"])
    assert [m["names"]["name"] for m in r["mentions"]] == ["Wren"], r["mentions"]


def test_hidden_counted_and_said():
    r = counter.count(FIXTURE, schema=SCHEMA)
    assert r["marks"]["hidden"] == 1
    wren = next(x for x in r["most_linked"] if x["name"] == "Wren")
    assert wren["marks"] == ["hidden"]
    md = counter.markdown(r, 40)
    assert "1 hidden (counted" in md and "| Wren (hidden) |" in md, md


def test_consistency_reads_a_proposal_as_not_yet_canon():
    links, dates, _ = consistency.load_schema(SCHEMA)
    world, els, _ = consistency.load_world(FIXTURE)
    rep = consistency.Report()
    consistency.check_dates(els, world, dates, links, rep, [])
    by_name = {x["element"]["name"]: x for x in rep.findings["dates"]}
    assert by_name["The siege"]["level"] == "contradiction"
    assert by_name["The raid"]["level"] == "proposal"
    assert by_name["The raid"]["message"].startswith("Not yet canon (a proposed element): ")
    md = consistency.markdown(world, len(els), 0, rep, ["dates"], [], [], [])
    assert "1 contradictions, 0 possible. 1 more involve a proposed element" in md, md


def test_review_mark_reads_the_profile():
    rm = consistency.review_mark
    assert rm({}) is None and rm({"x_review_proposed": None}) is None
    assert rm({"x_review_proposed": {"by": "s", "evidence": "e", "expires": "2099-01-01"}}) == "proposed"
    assert rm({"x_review_proposed": "yes"}) == "doubt" and rm({"x_review_proposed": {"by": "s"}}) == "doubt"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
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
