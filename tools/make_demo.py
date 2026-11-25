"""Builds the demo version: placeholder pictures in demo/stimuli/ and demo/config.js.

The placeholders are plain labelled boxes (correct options carry a small tick so
you can test scoring). They contain nothing from any real test.

Run from the repo folder:  python3 tools/make_demo.py
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo" / "stimuli"
LETTERS = "ABCD"
rng = random.Random(7)


def box(path, w, h, title, sub, tick=False, fill="#e9edf3"):
    tick_svg = ('<text x="%d" y="30" font-size="26" fill="#2e8b57" text-anchor="end">&#10003;</text>' % (w - 12)) if tick else ""
    path.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect x="2" y="2" width="{w-4}" height="{h-4}" rx="10" fill="{fill}" stroke="#9aa5b5" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="{w/2}" y="{h/2 - 4}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="#4a5568" text-anchor="middle">{title}</text>
  <text x="{w/2}" y="{h/2 + 20}" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#718096" text-anchor="middle">{sub}</text>
  {tick_svg}
</svg>
''')


def row_image(path, name, key):
    """One picture holding the whole item (target + 4 labelled options)."""
    w, h, cell = 900, 190, 170
    parts = []
    x = 10
    for i, label in enumerate(["Target"] + list(LETTERS)):
        fill = "#dde3ec" if i == 0 else "#e9edf3"
        parts.append(f'<rect x="{x}" y="10" width="{cell}" height="140" rx="10" fill="{fill}" stroke="#9aa5b5" stroke-width="2" stroke-dasharray="6 5"/>')
        parts.append(f'<text x="{x+cell/2}" y="88" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#4a5568" text-anchor="middle">{name} {label}</text>')
        if i > 0:
            parts.append(f'<text x="{x+cell/2}" y="178" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="#333" text-anchor="middle">{label}</text>')
            if label in key:
                parts.append(f'<text x="{x+cell-10}" y="38" font-size="24" fill="#2e8b57" text-anchor="end">&#10003;</text>')
        x += cell + (20 if i == 0 else 8)
        if i == 0:
            parts.append(f'<line x1="{x-12}" y1="10" x2="{x-12}" y2="150" stroke="#333" stroke-width="2"/>')
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>\n")


def separate_item(prefix, name, key):
    box(OUT / f"{prefix}_target.svg", 220, 170, name, "target", fill="#dde3ec")
    for l in LETTERS:
        box(OUT / f"{prefix}_{l}.svg", 220, 170, name, f"option {l}", tick=l in key)
    return {"target": f"{prefix}_target.svg", "options": [f"{prefix}_{l}.svg" for l in LETTERS]}


OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*.svg"):
    f.unlink()

practice = []
for n in (1, 2):
    key = sorted(rng.sample(LETTERS, 2))
    practice.append({"id": f"P{n}", "label": f"Example {n}", **separate_item(f"p{n}", f"Example {n}", key),
                     "answer": key,
                     "feedback": f"<p>[Placeholder] Explain here why {key[0]} and {key[1]} are correct for example {n}.</p>"})
key = sorted(rng.sample(LETTERS, 2))
row_image(OUT / "p3_row.svg", "Example 3", key)
practice.append({"id": "P3", "label": "Example 3", "image": "p3_row.svg", "answer": key,
                 "feedback": f"<p>[Placeholder] This example uses the one-picture-per-item layout. Correct: {key[0]} and {key[1]}.</p>"})

parts = []
num = 1
items = []
for _ in range(24):
    key = sorted(rng.sample(LETTERS, 2))
    items.append({"id": num, **separate_item(f"item{num:02d}", f"Item {num}", key), "answer": key})
    num += 1
parts.append({"label": "Test", "items": items})
for i in range(1, 4):
    box(OUT / f"intro_{i}.svg", 220, 170, f"Figure {i}", "instruction picture", fill="#f3f0e6")

instructions = [
    {"blocks": [
        {"html": "<p><b>[Placeholder instructions: replace with your test's own wording in config.js.]</b></p>"
                 "<p>Instruction pages can mix text and rows of pictures:</p>"},
        {"figures": ["intro_1.svg", "intro_2.svg", "intro_3.svg"]},
        {"html": "<p>Each problem shows one figure on the left of a line and four figures on the right. "
                 "Two of the four figures on the right are the same as the figure on the left, only turned.</p>"},
    ]},
    {"html": "<p>Try these examples. Click a figure to choose it and click it again to unchoose it. "
             "Choose two figures for each example, then check your answer.</p>",
     "practice": ["P1", "P2"],
     "feedback": "<p>[Placeholder] Feedback for the whole page can go here as well as per item.</p>"},
    {"html": "<p>This example is shown the other way the task can display items.</p>", "practice": ["P3"]},
    {"html": "<p>There are 24 problems on 4 pages of 6. You have 6 minutes in total, and you can move "
             "back and forth between pages until time runs out.</p>"
             "<p>Press <kbd>spacebar</kbd> or click below when you are ready to begin.</p>"},
]

config = {
    "demo": True,
    "title": "Mental Rotation Test (demo)",
    "taskName": "mentalrotation",
    "stimuliPath": "demo/stimuli/",
    "letters": LETTERS,
    "correctPerItem": 2,
    "maxSelections": 2,
    "partSeconds": 360,
    "itemsPerPage": 6,
    "instructions": instructions,
    "practice": practice,
    "parts": parts,
    "breakHtml": "<p>You have finished this part. You may take a short break.</p>",
}

(ROOT / "demo" / "config.js").write_text(
    "// DEMO config, generated by tools/make_demo.py. Placeholder pictures only.\n"
    "// To set up the real test, copy config.example.js to config.js (see README).\n"
    "window.MRT_CONFIG = " + json.dumps(config, indent=2) + ";\n")
print(f"Wrote {len(list(OUT.glob('*.svg')))} placeholder pictures and demo/config.js")
