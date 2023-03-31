"""The Blinker class contains the logic for the blinking cross in the eye test."""

import datetime
import logging
import tkinter as tk

from grid import coordinates

_LOGGER = logging.getLogger(__name__)


class Blinker:
    """A `blinking` cross that moves over the canvas."""

    _min_size = 1
    _max_size = 100
    _default_size: int = 10

    def __init__(
        self, canvas: tk.Canvas, thickness: int, position: coordinates
    ) -> None:
        self.canvas = canvas
        # self._max_x = max_x
        # self._max_y = max_y
        # self._step_size_x = step_size_x
        # self._step_size_y = step_size_y
        self._thickness = thickness
        self._x: int
        self._y: int

        self._size: int = self._default_size
        self._orientation: int = 0  # horizontal / vertical
        self._vertical_line = None
        self._horizontal_line = None
        self.move(position)
        self.update()

    @property
    def size(self):
        """Getter for size"""
        return self._size

    def clear(self):
        """Clears the entire canvas"""
        self.canvas.delete(self._horizontal_line)
        self.canvas.delete(self._vertical_line)

    def update(self):
        """Update the blinker on the canvas."""
        self.clear()
        scaled_thickness = ((self._thickness * self._size) // 10) + 1
        if self._orientation == 0:
            self._horizontal_line = self.canvas.create_line(
                (self._x - self._size, self._y, self._x + self._size, self._y),
                fill="white",
                width=scaled_thickness,
            )
        else:
            self._vertical_line = self.canvas.create_line(
                (self._x, self._y - self._size, self._x, self._y + self._size),
                fill="white",
                width=scaled_thickness,
            )

    def switch(self) -> None:
        """Switch orientation between vertical and horizontal"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._orientation = 1 - self._orientation
        self.update()

    def move(self, position):
        """Moves the blinker to the given position"""
        self._x = position.x
        self._y = position.y
        self.update()

    def increase_size(self) -> int:
        """Increases the size of the blinker and returns te size."""
        self._size = self._size + 1 if self._size < self._max_size else self._max_size
        return self._size

    def decrease_size(self) -> int:
        """Increases the size of the blinker and returns te size."""
        self._size = self._size - 1 if self._size > self._min_size else self._min_size
        return self._size
