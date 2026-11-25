# mental-rotation_task
Mental Rotation Task

This is a mental imagery outcome measure, intended to be given both pre- and post-experiment. It is a browser version of a paper-and-pencil mental rotation test, coded in JavaScript with the assistance of Claude (Opus 5.5, November 2026). It works the same way as our [paper folding task](https://github.com/erbschille/paper-folding_task).

**This repository contains no test items.** The conditions of use of the test don't allow sharing the items, so the code is a general engine. The real items, answers and instructions live in two places that git ignores: `config.js` and the `stimuli/` folder. Without them, the task runs a demo with placeholder pictures.

**Collaborators or those interested in using this task should fork this repo and get the test materials from the test's authors. Please do not use our link (it will mess with data collection).**

## Files

| File | What it is |
|---|---|
| `index.html` | The task. Open it in a browser. |
| `config.example.js` | Template for the real test. Copy to `config.js` and fill in. |
| `stimuli/` | Put the real test pictures here (ignored by git). |
| `demo/` | Demo config and placeholder pictures, used when there's no `config.js`. |
| `tools/make_demo.py` | Rebuilds the demo files. |
| `tools/crop_items.py` | Crops the items out of a PDF of the test, on your own computer (see below). |
| `tools/fill_answers.py` | Fills in the answer key in `config.js` from a pasted text file (see below). |

## Setting up the real test

1. Copy `config.example.js` to `config.js`.
2. Put the pictures in `stimuli/`. Each item can be either:
   - **separate pictures:** one target picture and four option pictures (`target` plus `options`), or
   - **one picture of the whole row** (`image`). The picture must show the A–D labels, and participants click A–D buttons under it.
   You can use different layouts for different items.
3. Fill in `config.js`: the instruction pages, practice items, each item's file names and its correct letters (`answer: ["A", "C"]`). Instruction pages can mix text and rows of pictures (`blocks`). Practice pages can show feedback after "Check my answer" (`feedback`).
4. Open `index.html?check=1` (via a local server, e.g. `python3 -m http.server` then <http://localhost:8000/?check=1>, or by double-clicking `index.html` and adding `?check=1` to the address). This shows every item with its correct options outlined in green. It also lists config problems, such as missing pictures or answers with the wrong number of letters. This view only opens on your own computer, not on a hosted copy.
5. Run through the task yourself once, then check the CSV.

### Cropping the items from a PDF

If your copy of the test is a PDF whose figures are drawn in frames (like the MRT-A), `tools/crop_items.py` finds every row of 5 framed figures (target + 4 options) and saves them with the file names `config.js` expects (`item01_target.png`, `item01_A.png` … `item24_D.png`). It runs entirely on your Mac (macOS PDF engine plus numpy) and saves into the git-ignored `stimuli/` folder.

```bash
python3 tools/crop_items.py ~/path/to/test.pdf --pages 3-6 --dry-run
```

`--dry-run` only reports what it finds, e.g. `Page 3: 6 item row(s) -> items 1–6`. Use `--pages` to skip the instruction pages, or their example figures will be counted as items. When the report shows 6 items per page and 24 in all, run it again without `--dry-run`. Rows with a different number of figures are skipped and listed under "Check these". Other options: `--start` (first item number), `--prefix`, `--out`, `--per-row`, `--dpi`. Then fill in the answers and check everything with `?check=1`.

### Filling in the answer key

Paste the key into `stimuli/answers.txt` in the form `1ab 2cd …`, one or several per line (`4. B C` and `5: a, d` work too). Then run:

```bash
python3 tools/fill_answers.py
```

It checks that every test item has exactly two letters and that nothing is missing or repeated. If all is well, it writes the answers into `config.js` and saves a copy of the old file to `stimuli/config.backup.js`. If anything is wrong it changes nothing and lists the problems by item number. It never prints the answers. Practice items are left alone.

Before committing, `git status` should never list `config.js` or anything in `stimuli/` other than `stimuli/README.txt`.

## Hosting

Because the real files are not in git, a GitHub Pages site built from this repo only shows the demo. To run the real test, host `index.html`, `config.js` and `stimuli/` together somewhere access-controlled, such as a university web server. Anything shown in a browser can be saved by a determined participant (right-click saving is blocked, but screenshots aren't), so check that the test's conditions of use allow online administration.

## Running it

Same URL parameters as the paper folding task:

```
index.html?pid=K7M2QX&session=1&embedded=1
```

- `pid`: participant ID (skips the ID entry screen)
- `session`: copied into the data (e.g. 1 = pre, 2 = post)
- `embedded=1`: inside Qualtrics. Results are sent to the parent page with `postMessage` as `{type: "task_complete", task: "mentalrotation", data: {...}}`, and no score screen is shown.

Not embedded: the score screen is shown and a CSV downloads automatically.

## Flow

ID entry → instruction pages (with practice items and "Check my answer" feedback) → the timed test → end. By default the 24 problems are one timed part shown on 4 pages of 6 (`itemsPerPage`), matching the paper copy. Participants can move back and forth between pages until time runs out. To give the test as separately timed parts with a break in between, list more than one part in `parts`. Participants click a figure to choose it and click again to unchoose it. They can choose up to `maxSelections` (default 2) per item. Submitting early asks for confirmation. When time runs out the part is submitted automatically. The timer runs off the real clock, so it stays accurate if the tab is in the background.

## Data

One CSV row per test item:

| Column | Meaning |
|---|---|
| `participant_id`, `session`, `session_start` | From the URL / start time |
| `part`, `page`, `position`, `item_id` | Where the item was |
| `response` | Letters chosen, e.g. `AC` (empty = no answer) |
| `correct_answer` | Correct letters from the config |
| `n_selected`, `hits`, `false_alarms` | Number chosen, number correct, number wrong |
| `both_correct` | 1 if exactly the correct options were chosen |
| `answered` | 1 if anything was chosen |
| `first_click_ms`, `last_click_ms`, `n_clicks` | Timing from the start of the part |
| `part_time_used_ms`, `submitted_manually` | How long the part took; 1 = clicked Submit, 0 = time ran out |

Qualtrics summary fields: `responses` (all answers in order, separated by `|`, `-` = no answer), `strict`, `hits`, `false_alarms`, `answered`, plus `p1_…` / `p2_…` per part when there is more than one part.

**Scoring.** `strict` is the usual MRT score: one point per item where both correct figures were chosen. Other scoring rules (e.g. hits minus false alarms) can be computed from the per-item columns.
