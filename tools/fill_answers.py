"""Fills in the answer key in config.js from a text file, on your own computer.

1. Paste the answer key into stimuli/answers.txt (git ignores that folder).
   Entries like "1ab", one per line or several per line, all work:
       1ab 2cd 3ad
       4. B C
       5: a, d
2. Run from the repo folder:   python3 tools/fill_answers.py
3. Open index.html?check=1 to compare the key with the pictures.

It only changes the  answer: [...]  of test items with numeric ids. Practice
items are left alone. A copy of config.js is saved to stimuli/config.backup.js
first. It never prints the answers themselves.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_key(text, letters):
    """Returns {item number: "AC"} and a list of problems."""
    L = re.escape(letters + letters.lower())
    entry = re.compile(rf"(\d+)\s*[.:)\-]?\s*((?:[{L}][\s,&/+]*)+)")
    key, problems = {}, []
    for m in entry.finditer(text):
        n = int(m.group(1))
        ans = "".join(sorted(re.sub(r"[^A-Za-z]", "", m.group(2)).upper()))
        if n in key:
            problems.append(f"item {n} appears more than once in the key")
        key[n] = ans
    leftover = entry.sub(" ", text)
    if re.search(r"\d", leftover):
        problems.append("some numbers in the key weren't followed by answer letters; check for typos")
    return key, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default=str(ROOT / "stimuli" / "answers.txt"), help="answer key file (default stimuli/answers.txt)")
    ap.add_argument("--config", default=str(ROOT / "config.js"), help="config to update (default config.js)")
    ap.add_argument("--letters", default="ABCD", help="option letters (default ABCD)")
    ap.add_argument("--per-item", type=int, default=2, help="correct options per item (default 2)")
    args = ap.parse_args()

    key_path, cfg_path = Path(args.key), Path(args.config)
    if not key_path.exists():
        sys.exit(f"Can't find the answer key at {key_path}. Paste it into that file first.")
    if not cfg_path.exists():
        sys.exit(f"Can't find {cfg_path}.")

    key, problems = parse_key(key_path.read_text(), args.letters)
    for n, ans in sorted(key.items()):
        if len(ans) != args.per_item:
            problems.append(f"item {n} has {len(ans)} letter(s), expected {args.per_item}")
        elif len(set(ans)) != len(ans):
            problems.append(f"item {n} lists the same letter twice")

    cfg = cfg_path.read_text()
    # A test item line looks like:  { id: 12, target: "...", options: [...], answer: [] },
    item_line = re.compile(r"^(?P<pre>.*\bid:\s*(?P<id>\d+)\s*,.*?\banswer:\s*)\[[^\]]*\]", re.M)
    ids = [int(m.group("id")) for m in item_line.finditer(cfg)]
    missing = [n for n in ids if n not in key]
    extra = [n for n in key if n not in ids]
    if missing:
        problems.append(f"no answer in the key for item(s) {', '.join(map(str, missing))}")
    if extra:
        problems.append(f"the key has item(s) {', '.join(map(str, sorted(extra)))}, which aren't in config.js")
    if not ids:
        problems.append("found no test items with numeric ids in config.js")

    if problems:
        print("Nothing changed. Please fix these first:\n  " + "\n  ".join(problems))
        return 1

    backup = ROOT / "stimuli" / "config.backup.js"
    backup.parent.mkdir(exist_ok=True)
    shutil.copyfile(cfg_path, backup)
    new = item_line.sub(lambda m: m.group("pre") + "[" + ", ".join(f'"{c}"' for c in key[int(m.group("id"))]) + "]", cfg)
    cfg_path.write_text(new)
    print(f"Filled in {len(ids)} answers in {cfg_path.name}. Backup of the old file: stimuli/config.backup.js")
    print("Next: open index.html?check=1 and compare the green-outlined options with the key.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
