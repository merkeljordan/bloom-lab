// Interactive bench + the same checks as tests/test_bloom_model.py.
(function () {
  const { SEED, SPROUT, BLOOM, NAMES, bloomLevel1, FlowerLevel2, Board } = window.Bloom;
  const EMOJI = { 0: "🌱", 1: "🌿", 2: "🌸" };

  const banner = document.getElementById("test-banner");
  const tabL1 = document.getElementById("tab-l1");
  const tabL2 = document.getElementById("tab-l2");
  const emoji = document.getElementById("emoji");
  const label = document.getElementById("label");
  const detail = document.getElementById("detail");
  const leds = [0, 1, 2].map((i) => document.getElementById("led" + i));
  const sw0 = document.getElementById("sw0");
  const sw1 = document.getElementById("sw1");
  const l2Only = document.getElementById("l2-only");
  const btnGrow = document.getElementById("btn-grow");
  const btnReset = document.getElementById("btn-reset");
  const hint = document.querySelector(".controls .tiny");
  const tW = document.getElementById("t-w");
  const tS = document.getElementById("t-s");
  const tG = document.getElementById("t-g");
  const tO = document.getElementById("t-o");

  let mode = "l1";
  let water = false;
  let sun = false;
  let lastGrow = false;
  const board = new Board();

  function assertEqual(failures, actual, expected, name) {
    if (actual !== expected) failures.push(name + ": got " + actual + ", expected " + expected);
  }

  function runSelfTests() {
    const failures = [];

    const rows = [
      [false, false, false],
      [false, true, false],
      [true, false, false],
      [true, true, true],
    ];
    rows.forEach(([w, s, exp]) => {
      assertEqual(failures, bloomLevel1(w, s), exp, "L1 " + Number(w) + Number(s));
    });

    const resetFlower = new FlowerLevel2();
    resetFlower.state = BLOOM;
    resetFlower.reset();
    assertEqual(failures, resetFlower.stateCode, SEED, "reset seed");
    assertEqual(failures, resetFlower.leds.join(","), "true,false,false", "reset leds");

    const stay = new FlowerLevel2();
    for (let i = 0; i < 4; i++) stay.step(false);
    assertEqual(failures, stay.state, SEED, "no grow stays seed");

    const two = new FlowerLevel2();
    assertEqual(failures, two.step(true), SPROUT, "first grow");
    assertEqual(failures, two.step(false), SPROUT, "hold sprout");
    assertEqual(failures, two.step(false), SPROUT, "hold sprout 2");
    assertEqual(failures, two.step(true), BLOOM, "second grow");
    assertEqual(failures, two.step(true), BLOOM, "bloom holds");

    const three = new FlowerLevel2();
    three.step(true);
    three.step(true);
    three.step(true);
    assertEqual(failures, three.state, BLOOM, "three grows");

    const hold = new Board();
    assertEqual(failures, hold.step(true, true).state, SPROUT, "both switches once");
    assertEqual(failures, hold.step(true, true).state, SPROUT, "holding both");
    assertEqual(failures, hold.step(true, true).state, SPROUT, "still holding");

    const again = new Board();
    again.step(true, true);
    again.step(false, false);
    assertEqual(failures, again.step(true, true).state, BLOOM, "release and apply");

    const waterOnly = new Board();
    waterOnly.step(true, false);
    waterOnly.step(true, false);
    assertEqual(failures, waterOnly.fsm.state, SEED, "water only");

    const withBtn = new Board();
    withBtn.step(true, true);
    assertEqual(failures, withBtn.fsm.state, SPROUT, "edge to sprout");
    assertEqual(failures, withBtn.step(true, true, true).state, BLOOM, "grow button");

    const btnAlone = new Board();
    btnAlone.step(false, false, true);
    assertEqual(failures, btnAlone.fsm.state, SEED, "grow without both");

    return failures;
  }

  function setSwitch(el, on) {
    el.classList.toggle("on", on);
    el.setAttribute("aria-pressed", on ? "true" : "false");
  }

  function render() {
    const level1 = mode === "l1";
    tabL1.classList.toggle("active", level1);
    tabL2.classList.toggle("active", !level1);
    l2Only.hidden = level1;
    setSwitch(sw0, water);
    setSwitch(sw1, sun);
    tW.textContent = water ? "1" : "0";
    tS.textContent = sun ? "1" : "0";

    if (level1) {
      const bloom = bloomLevel1(water, sun);
      emoji.textContent = bloom ? "🌸" : "🌱";
      label.textContent = bloom ? "BLOOM" : "OFF";
      detail.textContent = "bloom = water AND sun";
      hint.textContent = "Level 1 has no memory. Bloom is on only while both switches are on.";
      tG.textContent = "—";
      tO.textContent = bloom ? "bloom 1" : "bloom 0";
      leds.forEach((led, i) => led.classList.toggle("on", i === 2 && bloom));
      return;
    }

    const state = board.fsm.state;
    emoji.textContent = EMOJI[state];
    label.textContent = NAMES[state];
    detail.textContent = "SEED → SPROUT → BLOOM, one grow pulse each";
    hint.textContent = "Holding both switches is one grow (edge detect). Release and turn both on again to bloom.";
    tG.textContent = lastGrow ? "1" : "0";
    tO.textContent = NAMES[state] + " (" + state + ")";
    const on = board.fsm.leds;
    leds.forEach((led, i) => led.classList.toggle("on", on[i]));
  }

  function clock(growBtn) {
    const result = board.step(water, sun, growBtn);
    lastGrow = result.grow;
    return result;
  }

  function toggleWater() {
    water = !water;
    if (mode === "l2") clock(false);
    render();
  }

  function toggleSun() {
    sun = !sun;
    if (mode === "l2") clock(false);
    render();
  }

  function pressGrow() {
    if (mode !== "l2") return;
    clock(true);
    const shown = lastGrow;
    board.step(water, sun, false);
    lastGrow = shown;
    render();
  }

  function pressReset() {
    if (mode !== "l2") return;
    board.reset();
    lastGrow = false;
    render();
  }

  tabL1.addEventListener("click", () => {
    mode = "l1";
    render();
  });
  tabL2.addEventListener("click", () => {
    mode = "l2";
    render();
  });
  sw0.addEventListener("click", toggleWater);
  sw1.addEventListener("click", toggleSun);
  btnGrow.addEventListener("click", pressGrow);
  btnReset.addEventListener("click", pressReset);

  document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    if (key === "w") toggleWater();
    else if (key === "s") toggleSun();
    else if (key === "g") pressGrow();
    else if (key === "r") pressReset();
    else return;
    event.preventDefault();
  });

  const failures = runSelfTests();
  if (failures.length === 0) {
    banner.className = "pass";
    banner.textContent = "All bench checks passed — same cases as tests/test_bloom_model.py";
  } else {
    banner.className = "fail";
    banner.textContent = failures.length + " checks failed: " + failures.join("; ");
  }

  window.BloomBench = {
    failures,
    get mode() { return mode; },
    get water() { return water; },
    get sun() { return sun; },
    get state() { return board.fsm.state; },
    get lastGrow() { return lastGrow; },
    toggleWater,
    toggleSun,
    pressGrow,
    pressReset,
    setMode(next) {
      mode = next;
      render();
    },
  };

  render();
})();
