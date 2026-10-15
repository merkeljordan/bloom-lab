// Golden model for the Bloom bench. Keep in step with sim/bloom_model.py.
(function (global) {
  const SEED = 0;
  const SPROUT = 1;
  const BLOOM = 2;
  const NAMES = { 0: "SEED", 1: "SPROUT", 2: "BLOOM" };

  function bloomLevel1(water, sun) {
    return Boolean(water) && Boolean(sun);
  }

  class GrowPulse {
    constructor() {
      this._both = false;
      this._btn = false;
    }

    reset() {
      this._both = false;
      this._btn = false;
    }

    step(water, sun, growBtn) {
      const both = Boolean(water) && Boolean(sun);
      const bothRise = both && !this._both;
      const btnRise = Boolean(growBtn) && !this._btn;
      this._both = both;
      this._btn = Boolean(growBtn);
      return bothRise || (btnRise && both);
    }
  }

  class FlowerLevel2 {
    constructor() {
      this.state = SEED;
    }

    reset() {
      this.state = SEED;
    }

    step(grow) {
      if (this.state === SEED && grow) this.state = SPROUT;
      else if (this.state === SPROUT && grow) this.state = BLOOM;
      return this.state;
    }

    get leds() {
      return [this.state === SEED, this.state === SPROUT, this.state === BLOOM];
    }

    get stateCode() {
      return this.state;
    }
  }

  class Board {
    constructor() {
      this.pulse = new GrowPulse();
      this.fsm = new FlowerLevel2();
    }

    reset() {
      this.pulse.reset();
      this.fsm.reset();
    }

    step(water, sun, growBtn = false) {
      const grow = this.pulse.step(water, sun, growBtn);
      const state = this.fsm.step(grow);
      return { state, grow };
    }
  }

  global.Bloom = {
    SEED,
    SPROUT,
    BLOOM,
    NAMES,
    bloomLevel1,
    GrowPulse,
    FlowerLevel2,
    Board,
  };
})(window);
