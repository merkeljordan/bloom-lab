"""Golden model for the Bloom lab (matches rtl/flower_level*.sv + grow pulse)."""

from __future__ import annotations

SEED, SPROUT, BLOOM = 0, 1, 2
NAMES = {SEED: "SEED", SPROUT: "SPROUT", BLOOM: "BLOOM"}


def bloom_level1(water: bool, sun: bool) -> bool:
    return bool(water) and bool(sun)


class GrowPulse:
    """Rising-edge of (water & sun), or rising-edge of grow_btn while both are on."""

    def __init__(self) -> None:
        self._both = False
        self._btn = False

    def reset(self) -> None:
        self._both = False
        self._btn = False

    def step(self, water: bool, sun: bool, grow_btn: bool) -> bool:
        both = bool(water) and bool(sun)
        both_rise = both and not self._both
        btn_rise = bool(grow_btn) and not self._btn
        self._both = both
        self._btn = bool(grow_btn)
        return both_rise or (btn_rise and both)


class FlowerLevel2:
    def __init__(self) -> None:
        self.state = SEED

    def reset(self) -> None:
        self.state = SEED

    def step(self, grow: bool) -> int:
        if self.state == SEED and grow:
            self.state = SPROUT
        elif self.state == SPROUT and grow:
            self.state = BLOOM
        return self.state

    @property
    def leds(self) -> tuple[bool, bool, bool]:
        return (self.state == SEED, self.state == SPROUT, self.state == BLOOM)

    @property
    def state_code(self) -> int:
        return self.state


class Board:
    """Level 2 wrapper: switches + grow button + FSM."""

    def __init__(self) -> None:
        self.pulse = GrowPulse()
        self.fsm = FlowerLevel2()

    def reset(self) -> None:
        self.pulse.reset()
        self.fsm.reset()

    def step(self, water: bool, sun: bool, grow_btn: bool = False) -> int:
        grow = self.pulse.step(water, sun, grow_btn)
        return self.fsm.step(grow)
