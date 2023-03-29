"""Class for managing the grid where the test takes place."""
from dataclasses import dataclass

import logging
import tkinter as tk


@dataclass
class coordinates:
    x: int
    y: int


_LOGGER = logging.getLogger(__name__)


class EyeTestGrid:
    """Grid where the blinker moves through"""

    def __init__(self, canvas: tk.Canvas, grid_size_x: int, grid_size_y: int):
        self._canvas = canvas

        # Grid size are coordinates, eg 10,5 is a grid of 10 wide and 5 high
        self._size = coordinates(grid_size_x, grid_size_y)

        # Grid position are coordinates, eg 1,1 is starting position top left
        self.position = coordinates(1, 1)

        # Create empty arrays to keep score for each grid coordinate, as well as the text item on the canvas
        self._score = [[None for x in range(self._size.x)] for y in range(self._size.y)]
        self._score_lbl_id = [
            [None for x in range(self._size.x)] for y in range(self._size.y)
        ]

    def score_lbl_id(self, position=None) -> str | int | None:
        pos = position if position else self.position
        return (self._score_lbl_id[pos.y - 1])[
            pos.x - 1
        ]  # watch out, first get y-list, than x-element

    def score(self, position=None) -> int | None:
        pos = position if position else self.position
        return (self._score[pos.y - 1])[
            pos.x - 1
        ]  # watch out, first get y-list, than x-element

    def screen_position(self) -> coordinates:
        """Calculates the screen position from the grid position"""
        x = self.position.x * self._canvas.winfo_width() // (self._size.x + 1)
        y = self.position.y * self._canvas.winfo_height() // (self._size.y + 1)
        return coordinates(x, y)

    def move(self, direction: str) -> bool:
        dir = direction.upper()
        if dir == "F":
            return self._move_forward()
        if dir == "U":
            return self._move_up()
        if dir == "B":
            return self._move_backward()
        if dir == "D":
            return self._move_down()
        return False  # unknown direction

    def _move_forward(self) -> bool:
        """Move the position forward in the grid. Returns False if at the end"""
        if self.position == self._size:
            _LOGGER.info("Not moving, end of grid")
            return False

        if self.position.x >= self._size.x:
            self.position = coordinates(1, self.position.y + 1)
        else:
            self.position = coordinates(self.position.x + 1, self.position.y)
        _LOGGER.info(f"Move to %s", self.position)
        return True

    def _move_backward(self) -> bool:
        """Move the position backward in the grid. Returns False if at the beginning"""
        if self.position == coordinates(1, 1):
            _LOGGER.info("Not moving, beginning of grid")
            return False

        if self.position.x <= 1:
            self.position = coordinates(self._size.x, self.position.y - 1)
        else:
            self.position = coordinates(self.position.x - 1, self.position.y)
        _LOGGER.info(f"Move to %s", self.position)
        return True

    def _move_up(self) -> bool:
        """Move the position upward in the grid. Returns False if at the top"""
        if self.position.y == 1:
            _LOGGER.info("Not moving, top of grid")
            return False

        self.position = coordinates(self.position.x, self.position.y - 1)
        _LOGGER.info(f"Move to %s", self.position)
        return True

    def _move_down(self) -> bool:
        """Move the position upward in the grid. Returns False if at the top"""
        if self.position.y == self._size.y:
            _LOGGER.info("Not moving, bottom of grid")
            return False

        self.position = coordinates(self.position.x, self.position.y + 1)
        _LOGGER.info(f"Move to %s", self.position)
        return True

    def keep_score(self, size: int, score_lbl_id):
        (self._score[self.position.y - 1])[
            self.position.x - 1
        ] = size  # watch out, first get y-list, than x-element
        (self._score_lbl_id[self.position.y - 1])[self.position.x - 1] = score_lbl_id

    def to_go(self) -> int:
        """How many more to go"""
        return sum(x.count(None) for x in self._score)
