# mental-rotation_task
Mental Rotation Task

This is a mental imagery outcome measure, intended to be given both pre- and post-experiment. It is a browser version of a paper-and-pencil mental rotation test, coded in JavaScript with the assistance of Claude (Opus 5.5, November 2026). It works the same way as our [paper folding task](https://github.com/erbschille/paper-folding_task).

## Files

| File | What it is |
|---|---|
| `index.html` | The task. Open it in a browser. |
| `config.js` | The real test: instructions, practice items, item file names and answer key. |
| `stimuli/` | The real test pictures. |
| `config.example.js` | Blank template, for setting up a different test. |
| `demo/` | Demo config and placeholder pictures, used when there's no `config.js`. |
| `tools/make_demo.py` | Rebuilds the demo files. |
| `tools/crop_items.py` | Crops the items out of a PDF of the test, on your own computer (see below). |
| `tools/fill_answers.py` | Fills in the answer key in `config.js` from a pasted text file (see below). |


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
