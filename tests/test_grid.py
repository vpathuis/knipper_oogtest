import unittest

from grid import EyeTestGrid, coordinates
import tkinter as tk

from unittest.mock import MagicMock


class TestGrid(unittest.TestCase):
    def test_move_grid(self):
        canvas = tk.Canvas()
        size_x = 3
        size_y = 2
        grid = EyeTestGrid(canvas, size_x, size_y)

        # Check we can move around the grid, but not outside of it
        for step in range(5):
            assert grid.move("F")
        assert not grid.move("F")
        assert not grid.move("D")
        for step in range(4):
            assert grid.move("B")
        assert grid.move("D")
        assert grid.move("U")
        assert not grid.move("U")
        assert grid.move("B")
        assert not grid.move("B")
        assert grid.move("D")

        # test illegal move
        assert not grid.move("E")

    def test_keep_score(self):
        canvas = tk.Canvas()
        grid = EyeTestGrid(canvas, 3, 2)
        grid.keep_score(5, 10)
        self.assertEqual(grid.score(), 5)
        self.assertEqual(grid.score_lbl_id(), 10)

    def test_to_go(self):
        canvas = tk.Canvas()
        grid = EyeTestGrid(canvas, 3, 2)
        self.assertEqual(grid.to_go(), 6)
        grid.keep_score(5, 10)
        grid.move("F")
        grid.keep_score(10, 20)
        self.assertEqual(grid.to_go(), 4)

    def test_screen_position(self):
        canvas = MagicMock()
        canvas.winfo_width.return_value = 1000
        canvas.winfo_height.return_value = 1000
        size_x = 3
        size_y = 2
        grid = EyeTestGrid(canvas, 3, 2)
        self.assertEqual(grid.screen_position(), coordinates(40, 333))
        grid.move("F")
        grid.move("D")
        self.assertEqual(grid.screen_position(), coordinates(373, 666))


if __name__ == "__main__":
    unittest.main()
