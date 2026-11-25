// ════════════════════════════════════════════════════════════════════
//  REAL TEST CONFIG: MRT-A (Peters, 1995)
//  Not committed to git (see .gitignore).
//  Instructions and practice figures come from the two instruction pages.
//  Still to do: add the 24 test items' pictures to stimuli/ and fill in
//  each answer below, then open index.html?check=1 to verify.
// ════════════════════════════════════════════════════════════════════
const U = s => `<u>${s}</u>`;
const F = (prefix) => ({ target: `instructions/${prefix}_target.png`,
                         options: ["A", "B", "C", "D"].map(l => `instructions/${prefix}_${l}.png`) });

window.MRT_CONFIG = {
  title: "Mental Rotations Test",
  taskName: "mentalrotation",
  stimuliPath: "stimuli/",

  letters: "ABCD",
  correctPerItem: 2,
  maxSelections: 2,
  partSeconds: 360,             // CHECK: time limit for all 24 problems (6 min = the usual 2 × 3 min)
  itemsPerPage: 6,              // 24 problems on 4 pages, like the paper copy
  warnAtSeconds: 60,
  urgentAtSeconds: 30,
  confirmEarlySubmit: true,
  showScoreAtEnd: true,

  instructions: [
    // Page 1 of the paper instructions: what "the same object" means
    { blocks: [
      { html: `<h1>Mental Rotations Test (MRT-A)</h1>
               <p class="note">This test is composed of the figures provided by Shepard and Metzler (1978), and is,
               essentially, an Autocad-redrawn version of the Vandenberg &amp; Kuse MRT test.
               &copy; Michael Peters, PhD, July 1995</p>
               <p style="margin-top:28px">Please look at these five figures.</p>` },
      { figures: [1, 2, 3, 4, 5].map(i => `instructions/intro_same_${i}.png`) },
      { html: `<p>Note that these are all pictures of the same object which is shown from different angles.
               Try to imagine moving the object (or yourself with respect to the object), as you look from
               one drawing to the next.</p>` },
    ]},
    { blocks: [
      { figures: ["instructions/intro_diff_1.png", "instructions/intro_diff_2.png"] },
      { html: `<p>Here are two drawings of a new figure that is different from the one shown in the first
               5 drawings. Satisfy yourself that these two drawings show an object that is different and
               cannot be "rotated" to be identical with the object shown in the first five drawings.</p>
               <p class="note">The first five drawings, for comparison:</p>` },
      { figures: [1, 2, 3, 4, 5].map(i => `instructions/intro_same_${i}.png`) },
    ]},

    // First practice problem
    { html: `<p>Now look at the object on the left of the line. Two of the four drawings on the right show
             the same object. Can you find those two? Click on them to choose them (click again to unchoose),
             then check your answer.</p>`,
      practice: ["ex1"],
      feedback: `<p>If you chose the first and third drawings (A and C), you made the correct choice.</p>` },

    // Page 2 of the paper instructions: three more problems
    { html: `<p>Here are three more problems. Again, the target object is shown ${U("twice")} in each set of
             four alternatives from which you choose the correct ones.</p>`,
      practice: ["ex2a", "ex3a", "ex4a"],
      feedback: `<p>Correct choices:<br>
                 2.a: second and third (B and C)<br>
                 3.a: first and fourth (A and D)<br>
                 4.a: first and third (A and C)</p>` },

    // Rules, then start
    { html: `<p>When you do the test, please remember that for each problem set there are ${U("two")} and
             ${U("only two")} figures that match the target figure.</p>
             <p>You will only be given a point if you mark off ${U("both")} correct matching figures; marking
             off only one of these will result in no marks.</p>
             <p>The test has 24 problems, shown on 4 pages of 6. You will have 6 minutes in total. Use the
             <b>Next page</b> and <b>Previous page</b> buttons to move between pages; you can go back and
             change your answers until time runs out. When you have finished, click <b>Submit</b>. If time
             runs out, your answers will be submitted automatically.</p>
             <p>Press <kbd>spacebar</kbd> or click below when you are ready to begin.</p>` },
  ],

  practice: [
    { id: "ex1",  label: "1.",  ...F("ex1"), answer: ["A", "C"] },
    { id: "ex2a", label: "2.a", ...F("ex2"), answer: ["B", "C"] },
    { id: "ex3a", label: "3.a", ...F("ex3"), answer: ["A", "D"] },
    { id: "ex4a", label: "4.a", ...F("ex4"), answer: ["A", "C"] },
  ],

  // The 24 test problems. Put their pictures in stimuli/ with these names
  // (or change the names here) and fill in each answer, e.g. answer: ["B", "D"].
  parts: [
    { label: "Test", items: [
      { id:  1, target: "item01_target.png", options: ["item01_A.png", "item01_B.png", "item01_C.png", "item01_D.png"], answer: ["A", "C"] },
      { id:  2, target: "item02_target.png", options: ["item02_A.png", "item02_B.png", "item02_C.png", "item02_D.png"], answer: ["A", "D"] },
      { id:  3, target: "item03_target.png", options: ["item03_A.png", "item03_B.png", "item03_C.png", "item03_D.png"], answer: ["B", "D"] },
      { id:  4, target: "item04_target.png", options: ["item04_A.png", "item04_B.png", "item04_C.png", "item04_D.png"], answer: ["B", "C"] },
      { id:  5, target: "item05_target.png", options: ["item05_A.png", "item05_B.png", "item05_C.png", "item05_D.png"], answer: ["A", "C"] },
      { id:  6, target: "item06_target.png", options: ["item06_A.png", "item06_B.png", "item06_C.png", "item06_D.png"], answer: ["A", "D"] },
      { id:  7, target: "item07_target.png", options: ["item07_A.png", "item07_B.png", "item07_C.png", "item07_D.png"], answer: ["B", "D"] },
      { id:  8, target: "item08_target.png", options: ["item08_A.png", "item08_B.png", "item08_C.png", "item08_D.png"], answer: ["B", "C"] },
      { id:  9, target: "item09_target.png", options: ["item09_A.png", "item09_B.png", "item09_C.png", "item09_D.png"], answer: ["B", "D"] },
      { id: 10, target: "item10_target.png", options: ["item10_A.png", "item10_B.png", "item10_C.png", "item10_D.png"], answer: ["A", "D"] },
      { id: 11, target: "item11_target.png", options: ["item11_A.png", "item11_B.png", "item11_C.png", "item11_D.png"], answer: ["C", "D"] },
      { id: 12, target: "item12_target.png", options: ["item12_A.png", "item12_B.png", "item12_C.png", "item12_D.png"], answer: ["B", "C"] },
      { id: 13, target: "item13_target.png", options: ["item13_A.png", "item13_B.png", "item13_C.png", "item13_D.png"], answer: ["A", "B"] },
      { id: 14, target: "item14_target.png", options: ["item14_A.png", "item14_B.png", "item14_C.png", "item14_D.png"], answer: ["B", "D"] },
      { id: 15, target: "item15_target.png", options: ["item15_A.png", "item15_B.png", "item15_C.png", "item15_D.png"], answer: ["B", "C"] },
      { id: 16, target: "item16_target.png", options: ["item16_A.png", "item16_B.png", "item16_C.png", "item16_D.png"], answer: ["A", "D"] },
      { id: 17, target: "item17_target.png", options: ["item17_A.png", "item17_B.png", "item17_C.png", "item17_D.png"], answer: ["B", "D"] },
      { id: 18, target: "item18_target.png", options: ["item18_A.png", "item18_B.png", "item18_C.png", "item18_D.png"], answer: ["B", "C"] },
      { id: 19, target: "item19_target.png", options: ["item19_A.png", "item19_B.png", "item19_C.png", "item19_D.png"], answer: ["A", "C"] },
      { id: 20, target: "item20_target.png", options: ["item20_A.png", "item20_B.png", "item20_C.png", "item20_D.png"], answer: ["A", "D"] },
      { id: 21, target: "item21_target.png", options: ["item21_A.png", "item21_B.png", "item21_C.png", "item21_D.png"], answer: ["B", "D"] },
      { id: 22, target: "item22_target.png", options: ["item22_A.png", "item22_B.png", "item22_C.png", "item22_D.png"], answer: ["B", "C"] },
      { id: 23, target: "item23_target.png", options: ["item23_A.png", "item23_B.png", "item23_C.png", "item23_D.png"], answer: ["A", "D"] },
      { id: 24, target: "item24_target.png", options: ["item24_A.png", "item24_B.png", "item24_C.png", "item24_D.png"], answer: ["A", "C"] },
    ]},
  ],
};
