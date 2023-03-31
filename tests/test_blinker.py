import unittest
from src.blinker import Blinker
import tkinter as tk

from src.grid import coordinates


class TestBlinker(unittest.TestCase):
    def test_blinker_move(self):
        canvas = tk.Canvas()
        blinker = Blinker(canvas=canvas, thickness=3, position=coordinates(1, 1))
        blinker.move(position=coordinates(2, 1))
        blinker.switch()

    def test_blinker_size(self):
        canvas = tk.Canvas()
        blinker = Blinker(canvas=canvas, thickness=3, position=coordinates(1, 1))
        blinker.increase_size()
        self.assertEqual(blinker.size, 11)
        for step in range(10):
            blinker.decrease_size()
        self.assertEqual(blinker.size, 1)
        blinker.decrease_size()
        self.assertEqual(blinker.size, 1)
        for step in range(100):
            blinker.increase_size()
        self.assertEqual(blinker.size, 100)


if __name__ == "__main__":
    unittest.main()
