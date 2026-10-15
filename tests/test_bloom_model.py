"""Golden-model tests mirroring rtl/tb_flower_level*.sv."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sim"))

from bloom_model import (  # noqa: E402
    BLOOM,
    SEED,
    SPROUT,
    Board,
    FlowerLevel2,
    bloom_level1,
)


class Level1Tests(unittest.TestCase):
    def test_truth_table(self) -> None:
        rows = [
            (False, False, False),
            (False, True, False),
            (True, False, False),
            (True, True, True),
        ]
        for water, sun, exp in rows:
            with self.subTest(water=water, sun=sun):
                self.assertEqual(bloom_level1(water, sun), exp)


class Level2Tests(unittest.TestCase):
    def test_reset_seed(self) -> None:
        f = FlowerLevel2()
        f.state = BLOOM
        f.reset()
        self.assertEqual(f.state_code, SEED)
        self.assertEqual(f.leds, (True, False, False))

    def test_no_grow_stays_seed(self) -> None:
        f = FlowerLevel2()
        for _ in range(4):
            f.step(False)
        self.assertEqual(f.state, SEED)

    def test_two_grows_to_bloom(self) -> None:
        f = FlowerLevel2()
        self.assertEqual(f.step(True), SPROUT)
        self.assertEqual(f.step(False), SPROUT)
        self.assertEqual(f.step(False), SPROUT)
        self.assertEqual(f.step(True), BLOOM)
        self.assertEqual(f.step(True), BLOOM)

    def test_three_grows_holds_bloom(self) -> None:
        f = FlowerLevel2()
        f.step(True)
        f.step(True)
        f.step(True)
        self.assertEqual(f.state, BLOOM)


class GrowPulseBoardTests(unittest.TestCase):
    def test_holding_both_switches_is_one_advance(self) -> None:
        b = Board()
        self.assertEqual(b.step(True, True), SPROUT)
        self.assertEqual(b.step(True, True), SPROUT)
        self.assertEqual(b.step(True, True), SPROUT)

    def test_release_and_apply_again_blooms(self) -> None:
        b = Board()
        b.step(True, True)
        b.step(False, False)
        self.assertEqual(b.step(True, True), BLOOM)

    def test_water_only_does_not_grow(self) -> None:
        b = Board()
        b.step(True, False)
        b.step(True, False)
        self.assertEqual(b.fsm.state, SEED)

    def test_grow_button_while_both_on(self) -> None:
        b = Board()
        b.step(True, True)  # edge of both -> SPROUT
        self.assertEqual(b.fsm.state, SPROUT)
        self.assertEqual(b.step(True, True, grow_btn=True), BLOOM)

    def test_grow_button_without_both_does_nothing(self) -> None:
        b = Board()
        b.step(False, False, grow_btn=True)
        self.assertEqual(b.fsm.state, SEED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
