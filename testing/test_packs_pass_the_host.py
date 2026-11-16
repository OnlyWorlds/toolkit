"""No pack text holds a command the host in front of onlyworlds.com refuses.

A pack's texts (the charter, the skills, the seed) become element bodies when a world goes online.
The host answers a write with `403` and an HTML page titled "Blocked", before the platform sees it,
when a text in the body has one of a few commands directly after a backtick, a semicolon or a pipe:
`python -m`, `python -c`, `perl -e`, or `curl` or `wget` with a URL (seen 2026-11-16; develop's
section The Blocked page says what was tried). A world set up from such a pack could not be
uploaded as written.

The pattern here is wider than what was seen refused (any flag after `python`, any argument after
`curl` or `wget`), so a pack text stays clear of the edge of it: the list above is what was tried,
not the host's whole rule. What passes, and what a pack uses instead: a prompt inside the code span
(`$ python -m ...`), a fenced block whose first line names a language, or plain text with no
backtick, semicolon or pipe just before the command.

Run under pytest; the file checks its own pattern first on texts known to be refused and to pass.
"""
import re
from pathlib import Path

PACKS = Path(__file__).resolve().parent.parent / "skills" / "onlyworlds-setup" / "packs"
BT = "`"
REFUSED = re.compile(r"(`{1,3}|;|\|)\s*(python\s+-[a-z]|perl\s+-e|(curl|wget)\s+\S)", re.I)

KNOWN_REFUSED = [
    f"Run {BT}python -m onlyworlds.doctor --api{BT} to check.",
    f"Run {BT}python -c pass{BT} to check.",
    f"Run {BT} python  -M onlyworlds.doctor{BT} to check.",
    f"Run {BT}curl https://www.onlyworlds.com/api/v2/health{BT} first.",
    f"Run {BT}wget https://example.com/world.zip{BT} first.",
    f"Run:\n{BT * 3}\npython -m onlyworlds.doctor\n{BT * 3}\n",
    "| check | python -m onlyworlds.doctor |",
    "Check it; curl https://www.onlyworlds.com/api/v2/health",
]
KNOWN_PASSING = [
    f"Run {BT}$ python -m onlyworlds.doctor --api{BT} to check.",
    "Run python -m onlyworlds.doctor --api to check.",
    f"Run:\n{BT * 3}bash\npython -m onlyworlds.doctor\n{BT * 3}\n",
    f"Run {BT}pip install onlyworlds{BT} first.",
    f"Run {BT}python3 -m onlyworlds.doctor{BT} to check.",
    f"The {BT}curl{BT} tool.",
]
# Not seen refused, caught all the same: the pattern's margin.
ALSO_CAUGHT = [
    f"Run {BT}python -u run.py{BT} to check.",
    f"Run {BT}curl --version{BT} first.",
]


def test_the_pattern_reads_known_texts_right():
    for t in KNOWN_REFUSED:
        assert REFUSED.search(t), f"the pattern misses a text the host refuses: {t!r}"
    for t in KNOWN_PASSING:
        assert not REFUSED.search(t), f"the pattern catches a text the host lets through: {t!r}"
    for t in ALSO_CAUGHT:
        assert REFUSED.search(t), f"the pattern's margin no longer holds: {t!r}"


def test_no_pack_text_holds_a_refused_command():
    files = sorted(p for p in PACKS.rglob("*") if p.is_file() and p.suffix in (".md", ".json"))
    assert len(files) >= 20, f"only {len(files)} pack files found under {PACKS}"
    found = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        for m in REFUSED.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            found.append(f"{p.relative_to(PACKS).as_posix()}:{line}: {m.group(0)!r}")
    assert not found, ("a pack text holds a command the host refuses in an upload "
                       "(use a prompt inside the code span, a fenced block with a language, or no "
                       "code marks):\n" + "\n".join(found))
    print(f"read {len(files)} pack files")
