// ════════════════════════════════════════════════════════════════════
//  YOUR REAL TEST CONFIG
//  1. Copy this file to "config.js" (same folder as index.html).
//  2. Put your pictures in the "stimuli" folder.
//  3. Fill in the instructions, file names and answers below.
//  4. Open index.html?check=1 to see every item with its answer key.
//  config.js and stimuli/ are listed in .gitignore, so they are never
//  committed or pushed to GitHub. Don't remove those lines.
// ════════════════════════════════════════════════════════════════════
window.MRT_CONFIG = {
  title: "Mental Rotation Test",
  taskName: "mentalrotation",   // name used in the Qualtrics message and CSV filename
  stimuliPath: "stimuli/",      // folder the picture file names below are relative to

  letters: "ABCD",              // one letter per option, in left-to-right order
  correctPerItem: 2,            // how many options are correct in each item
  maxSelections: 2,             // the most a participant may choose per item
  partSeconds: 360,             // time limit per part (a part can override with seconds: …)
  itemsPerPage: 6,              // split each part into pages of this many items (0 = all on one page)
  warnAtSeconds: 60,            // timer turns orange
  urgentAtSeconds: 30,          // timer turns red
  confirmEarlySubmit: true,     // ask "are you sure?" when submitting with time left
  showScoreAtEnd: true,         // show the score screen (never shown when embedded in Qualtrics)

  // ── Instruction pages, shown in order ─────────────────────────────
  //  { html: "..." }                          a page of text
  //  { blocks: [ {html: "..."}, {figures: ["a.png", "b.png"]}, ... ] }
  //                                           text and rows of pictures, in order
  //  { html: "...", practice: ["P1", "P2"], feedback: "..." }
  //                                           practice items with "Check my answer";
  //                                           feedback is shown after checking
  //  The last page's button starts the test.
  instructions: [
    { blocks: [
      { html: "<p>Replace with the test's instructions.</p>" },
      { figures: ["instructions/fig1.png", "instructions/fig2.png"] },
      { html: "<p>More instructions.</p>" },
    ]},
    { html: "<p>Now try these examples.</p>", practice: ["P1", "P2"], feedback: "" },
    { html: "<p>Replace with the final instructions before the test begins.</p>" },
  ],

  // ── Practice items ────────────────────────────────────────────────
  //  Each item is EITHER separate pictures:
  //    target: "file.png", options: ["a.png", "b.png", "c.png", "d.png"]
  //  OR one picture of the whole row (participants click A–D buttons under it):
  //    image: "row.png"
  //  answer:   the correct letters, e.g. ["A", "C"]
  //  feedback: HTML shown after "Check my answer" (optional)
  practice: [
    { id: "P1", label: "Example 1", target: "P1_target.png", options: ["P1_A.png", "P1_B.png", "P1_C.png", "P1_D.png"], answer: [], feedback: "" },
    { id: "P2", label: "Example 2", target: "P2_target.png", options: ["P2_A.png", "P2_B.png", "P2_C.png", "P2_D.png"], answer: [], feedback: "" },
  ],

  // ── Test parts ────────────────────────────────────────────────────
  //  ids must be unique across practice and test items.
  //  Items appear in the order listed. Either picture layout works here too.
  //  To split the test into timed parts with a break in between, list more
  //  than one part, e.g. [{ label: "Part One", items: [...] }, { label: "Part Two", items: [...] }].
  parts: [
    { label: "Test", items: [
      { id:  1, target: "item01_target.png", options: ["item01_A.png", "item01_B.png", "item01_C.png", "item01_D.png"], answer: [] },
      { id:  2, target: "item02_target.png", options: ["item02_A.png", "item02_B.png", "item02_C.png", "item02_D.png"], answer: [] },
      { id:  3, target: "item03_target.png", options: ["item03_A.png", "item03_B.png", "item03_C.png", "item03_D.png"], answer: [] },
      { id:  4, target: "item04_target.png", options: ["item04_A.png", "item04_B.png", "item04_C.png", "item04_D.png"], answer: [] },
      { id:  5, target: "item05_target.png", options: ["item05_A.png", "item05_B.png", "item05_C.png", "item05_D.png"], answer: [] },
      { id:  6, target: "item06_target.png", options: ["item06_A.png", "item06_B.png", "item06_C.png", "item06_D.png"], answer: [] },
      { id:  7, target: "item07_target.png", options: ["item07_A.png", "item07_B.png", "item07_C.png", "item07_D.png"], answer: [] },
      { id:  8, target: "item08_target.png", options: ["item08_A.png", "item08_B.png", "item08_C.png", "item08_D.png"], answer: [] },
      { id:  9, target: "item09_target.png", options: ["item09_A.png", "item09_B.png", "item09_C.png", "item09_D.png"], answer: [] },
      { id: 10, target: "item10_target.png", options: ["item10_A.png", "item10_B.png", "item10_C.png", "item10_D.png"], answer: [] },
      { id: 11, target: "item11_target.png", options: ["item11_A.png", "item11_B.png", "item11_C.png", "item11_D.png"], answer: [] },
      { id: 12, target: "item12_target.png", options: ["item12_A.png", "item12_B.png", "item12_C.png", "item12_D.png"], answer: [] },
      { id: 13, target: "item13_target.png", options: ["item13_A.png", "item13_B.png", "item13_C.png", "item13_D.png"], answer: [] },
      { id: 14, target: "item14_target.png", options: ["item14_A.png", "item14_B.png", "item14_C.png", "item14_D.png"], answer: [] },
      { id: 15, target: "item15_target.png", options: ["item15_A.png", "item15_B.png", "item15_C.png", "item15_D.png"], answer: [] },
      { id: 16, target: "item16_target.png", options: ["item16_A.png", "item16_B.png", "item16_C.png", "item16_D.png"], answer: [] },
      { id: 17, target: "item17_target.png", options: ["item17_A.png", "item17_B.png", "item17_C.png", "item17_D.png"], answer: [] },
      { id: 18, target: "item18_target.png", options: ["item18_A.png", "item18_B.png", "item18_C.png", "item18_D.png"], answer: [] },
      { id: 19, target: "item19_target.png", options: ["item19_A.png", "item19_B.png", "item19_C.png", "item19_D.png"], answer: [] },
      { id: 20, target: "item20_target.png", options: ["item20_A.png", "item20_B.png", "item20_C.png", "item20_D.png"], answer: [] },
      { id: 21, target: "item21_target.png", options: ["item21_A.png", "item21_B.png", "item21_C.png", "item21_D.png"], answer: [] },
      { id: 22, target: "item22_target.png", options: ["item22_A.png", "item22_B.png", "item22_C.png", "item22_D.png"], answer: [] },
      { id: 23, target: "item23_target.png", options: ["item23_A.png", "item23_B.png", "item23_C.png", "item23_D.png"], answer: [] },
      { id: 24, target: "item24_target.png", options: ["item24_A.png", "item24_B.png", "item24_C.png", "item24_D.png"], answer: [] },
    ]},
  ],

  breakHtml: "<p>You have finished this part. You may take a short break.</p>",
};
