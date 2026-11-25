"""The set-up skill's writer names an element's file as the standard does.

write_world.py's `slug` makes the name part of `<name part>--<id tail>.json`. The standard's rule
is the sentence under "The example world" in schema-dist's README, and its cases are
`fixtures/file-names.fixture.json` (38 at serial 147): each element name and the name part a
conforming writer gives it, `""` where a name leaves none (the file is then named by the full id).

- test_the_published_file_name_cases: every case gives the fixture's name part (the eight whose
  name leaves none among them); the failing cases are named with what the writer gave.

OW_FILE_NAMES_FIXTURE points at another copy of the fixture; else schema-dist's beside the
toolkit's main checkout (from a worktree too), which must not sit behind its fetched
origin/main. OW_WRITE_WORLD points at another copy of write_world.py (an older one, to show this
test is red on it); simple_fold.py must sit beside it.

Runs under pytest, or alone:
    python testing/test_file_names.py

Python 3, stdlib only.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WRITE_WORLD = Path(os.environ.get("OW_WRITE_WORLD")
                   or ROOT / "skills" / "onlyworlds-setup" / "scripts" / "write_world.py")


def writer():
    sys.path.insert(0, str(WRITE_WORLD.parent))
    try:
        spec = importlib.util.spec_from_file_location("write_world_under_test", WRITE_WORLD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(WRITE_WORLD.parent))
    return mod


def fixture_path():
    """The file-names fixture: the file OW_FILE_NAMES_FIXTURE names, else schema-dist's beside the
    toolkit's main checkout. Loud when there is none, and loud when that checkout sits behind its
    own fetched origin/main."""
    if os.environ.get("OW_FILE_NAMES_FIXTURE"):
        path = Path(os.environ["OW_FILE_NAMES_FIXTURE"])
        assert path.exists(), f"OW_FILE_NAMES_FIXTURE names a file that is not there: {path}"
        return path
    roots = [ROOT]
    common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            check=False, capture_output=True, text=True).stdout.strip()
    if common:
        roots.insert(0, Path(common).parent)
    path = next((p for p in (r.parent / "schema-dist" / "fixtures" / "file-names.fixture.json" for r in roots)
                 if p.exists()), None)
    assert path is not None, (f"no schema-dist checkout beside {ROOT.parent}: clone it there, "
                              "or set OW_FILE_NAMES_FIXTURE to a file-names.fixture.json")
    repo = path.parent.parent
    behind = subprocess.run(["git", "-C", str(repo), "rev-list", "--count", "HEAD..origin/main"],
                            check=False, capture_output=True, text=True).stdout.strip()
    assert behind in ("", "0"), f"schema-dist is {behind} commits behind its fetched origin/main: git -C {repo} pull"
    return path


def cases():
    found = json.loads(fixture_path().read_text(encoding="utf-8"))["cases"]
    assert len(found) >= 38, f"the fixture holds {len(found)} cases, serial 147 has 38"
    return found


def test_the_published_file_name_cases():
    slug, all_cases = writer().slug, cases()
    wrong = [f"{c['name']}: {c['element_name']!a} gave {slug(c['element_name'])!r}, the case says {c['slug']!r}"
             for c in all_cases if slug(c["element_name"]) != c["slug"]]
    print(f"{len(all_cases) - len(wrong)} of {len(all_cases)} file-name cases agree")
    assert not wrong, f"{len(wrong)} of {len(all_cases)} cases differ:\n" + "\n".join(wrong)


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
