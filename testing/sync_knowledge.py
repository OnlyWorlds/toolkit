"""Copy the shared knowledge files into each skill that reads them.

A skills directory (`npx skills add OnlyWorlds/toolkit`) installs each skill's own folder
and nothing else, so a skill cannot point at the root `knowledge/`. The root `knowledge/`
stays the one copy to edit; this script mirrors each file a skill reads into
`skills/<skill>/knowledge/` and rewrites the skill's reference to the skill-relative form:

    ../../knowledge/<file>.md     (from SKILL.md)                  -> knowledge/<file>.md
    ../../../knowledge/<file>.md  (from references/ or knowledge/) -> ../knowledge/<file>.md

What gets copied: every root file the skill's own files reference (as above), plus, one hop
out, every root file those copies name (`world-folder.md`, `./world-folder.md`). A copy is
the root file byte for byte except its pointers, rewritten for its new home:

    ../skills/<s>/...    -> ../../<s>/...                (another skill, from skills/<x>/knowledge/)
    <other>.md           kept when <other>.md is copied into the same skill;
                         otherwise -> ../../../knowledge/<other>.md (the root form; listed with -v)

The copies are committed (the directory installs from the main branch). A skill's own
knowledge file (no root namesake, like dev's deployment.md) is left alone; it must not take
a root knowledge file's name. Run after editing anything in `knowledge/`, then commit.

Usage:
    python testing/sync_knowledge.py [-v] [TOOLKIT_DIR]           sync: copy, rewrite, prune
    python testing/sync_knowledge.py --check [-v] [TOOLKIT_DIR]   exit 1 if anything is out of sync

Python 3, stdlib only.
"""
import re
import sys
from pathlib import Path

# A knowledge reference not preceded by a path segment, so `../onlyworlds-parsing/knowledge/x.md`
# (another skill's file) and URLs are not taken for one.
REF = re.compile(r"(?<![\w./-])((?:\.\./)*)knowledge/([A-Za-z0-9_.-]+\.md)")
SKILLS_PTR = re.compile(r"(?<![\w./-])\.\./skills/")


def read_text(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def write_text(p, text):
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def sibling_re(names):
    alt = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    return re.compile(r"(?<![\w./-])(\./)?(" + alt + r")(?![\w-]|\.\w)")


def transform(text, keep, sib, rooted):
    """A root file's text as it reads from skills/<x>/knowledge/, given the files copied there."""
    text = SKILLS_PTR.sub("../../", text)

    def fix(m):
        if m.group(2) in keep:
            return m.group(0)
        rooted.append(m.group(2))
        return "../../../knowledge/" + m.group(2)

    return sib.sub(fix, text)


def main(argv):
    check = "--check" in argv
    verbose = "-v" in argv
    args = [a for a in argv if a not in ("--check", "-v")]
    tk = Path(args[0]).resolve() if args else Path(__file__).resolve().parent.parent
    root_kn = tk / "knowledge"
    root_names = {p.name for p in root_kn.glob("*.md")}
    sib = sibling_re(root_names)
    problems, notes = [], []
    stats = {"rewritten": 0, "copies": 0, "rooted": 0}
    writes, copies, prunes = [], [], []  # applied only when the whole tree is clean

    for skill in sorted(p.parent for p in (tk / "skills").glob("*/SKILL.md")):
        local_kn = skill / "knowledge"
        wanted, fresh = set(), set()
        # Files that carry references: everything in the skill except the mirrored copies.
        sources = [f for f in sorted(skill.rglob("*.md"))
                   if not (f.parent == local_kn and f.name in root_names)]
        for f in sources:
            text = read_text(f)
            depth = len(f.relative_to(skill).parts) - 1
            rel = f.relative_to(tk).as_posix()

            def fix(m):
                ups, name = m.group(1), m.group(2)
                target = (f.parent / ups / "knowledge" / name).resolve()
                if target == (root_kn / name).resolve():
                    if not (root_kn / name).exists():
                        problems.append(f"{rel}: {m.group(0)} names no root knowledge file")
                        return m.group(0)
                    if check:
                        problems.append(f"{rel}: reaches outside the skill: {m.group(0)}")
                        return m.group(0)
                    wanted.add(name)
                    fresh.add(name)
                    stats["rewritten"] += 1
                    return "../" * depth + "knowledge/" + name
                if target == (local_kn / name).resolve():
                    if name in root_names:
                        wanted.add(name)
                    elif not target.exists():
                        problems.append(f"{rel}: {m.group(0)} does not resolve")
                    return m.group(0)
                problems.append(f"{rel}: {m.group(0)} resolves outside the skill's knowledge/")
                return m.group(0)

            new = REF.sub(fix, text)
            if new != text and not check:
                writes.append((f, new))

        # One hop out: the root files that the directly read files name.
        for name in sorted(wanted):
            wanted |= {m.group(2) for m in sib.finditer(read_text(root_kn / name))}

        for name in sorted(wanted):
            rooted = []
            expected = transform(read_text(root_kn / name), wanted, sib, rooted)
            dst = local_kn / name
            stats["copies"] += 1
            stats["rooted"] += len(rooted)
            for r in rooted:
                notes.append(f"{dst.relative_to(tk).as_posix()}: {r} -> ../../../knowledge/{r} (not copied)")
            if dst.exists() and read_text(dst) == expected:
                continue
            if check:
                problems.append(f"{dst.relative_to(tk).as_posix()}: "
                                f"{'missing' if not dst.exists() else 'differs from knowledge/' + name}")
                continue
            if dst.exists() and name in fresh:
                problems.append(f"{dst.relative_to(tk).as_posix()}: a skill-local file has the name of "
                                f"root knowledge/{name}; rename one of them")
                continue
            copies.append((dst, expected))

        for dst in sorted(local_kn.glob("*.md")) if local_kn.is_dir() else []:
            if dst.name in root_names and dst.name not in wanted:
                if check:
                    problems.append(f"{dst.relative_to(tk).as_posix()}: copy no file in the skill reads")
                else:
                    prunes.append(dst)

    if not check and not problems:
        for f, new in writes:
            write_text(f, new)
        for dst, text in copies:
            dst.parent.mkdir(exist_ok=True)
            write_text(dst, text)
        for dst in prunes:
            dst.unlink()
    elif problems and not check:
        print("nothing written")
        writes, copies, prunes = [], [], []
        stats["rewritten"] = 0

    if verbose:
        for n in notes:
            print("root form:", n)
    for p in problems:
        print("FAIL", p)
    mode = "check" if check else "sync"
    print(f"{mode}: {stats['copies']} copies across skills ({stats['rooted']} pointers left in root form); "
          f"rewritten {stats['rewritten']} references, wrote {len(copies)} files, pruned {len(prunes)}; "
          f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
