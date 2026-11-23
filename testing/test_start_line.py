"""The texts that must say one thing in the same words, across this repository.

    python -m pytest testing/test_start_line.py -q

1. The start line: the start skill's Connect quotes it, and the set-up skill's writer writes it
   (`START_LINE` in write_world.py), so the two copies in this repository are one sentence. The start
   skill's sentence is found by its opening words, never by a line number.
Python 3, stdlib only.
"""
import importlib.util
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
WRITER = SKILLS / "onlyworlds-setup" / "scripts" / "write_world.py"


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def writer():
    spec = importlib.util.spec_from_file_location("write_world_start_line", WRITER)
    ww = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ww)
    return ww


def sentences_from(text, opening):
    """Every run of text from `opening` to the end of its line, one per place it opens."""
    return [m.group(0).rstrip() for m in re.finditer(re.escape(opening) + r"[^\r\n]*", text)]


class TextsAgree(unittest.TestCase):

    def test_start_line_is_the_writers(self):
        line = writer().START_LINE
        opening = line.split("{")[0]
        self.assertGreater(len(opening), 30, "the line opens with words before its placeholder")
        found = sentences_from(read(SKILLS / "onlyworlds-start" / "SKILL.md"), opening)
        self.assertEqual(len(found), 1, f"the start skill quotes the line once: {found}")
        self.assertEqual(found[0], line)


if __name__ == "__main__":
    unittest.main()
