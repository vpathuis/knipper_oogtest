"""The Blinker class contains the logic for the blinking cross in the eye test."""

import datetime
import logging
import tkinter as tk

_LOGGER = logging.getLogger(__name__)


class Blinker:
    """A `blinking` cross that moves over the canvas."""

    _min_size = 1
    _max_size = 100
    _default_size: int = 10

    def __init__(
        self, canvas: tk.Canvas, max_x: int, max_y: int, step_size: int
    ) -> None:
        self.canvas = canvas
        self._max_x = max_x
        self._max_y = max_y
        self._step_size = step_size
        self._x: int = self._step_size
        self._y: int = self._step_size
        self._size: int = self._default_size
        self._orientation: int = 0  # horizontal / vertical
        self._row: int = 0
        self._column: int = 0
        self._vertical_line = None
        self._horizontal_line = None
        self.update()

    @property
    def x(self):
        """Getter for x"""
        return self._x

    @property
    def y(self):
        """Getter for y"""
        return self._y

    @property
    def size(self):
        """Getter for size"""
        return self._size

    @property
    def row(self):
        """Getter for row"""
        return self._row

    @property
    def column(self):
        """Getter for column"""
        return self._column

    def clear(self):
        """Clears the entire canvas"""
        self.canvas.delete(self._horizontal_line)
        self.canvas.delete(self._vertical_line)

    def update(self):
        """Update the blinker on the canvas."""
        self.clear()
        if self._orientation == 0:
            self._horizontal_line = self.canvas.create_line(
                (self._x - self._size, self._y, self._x + self._size, self._y),
                fill="white",
                width=1,
            )
        else:
            self._vertical_line = self.canvas.create_line(
                (self._x, self._y - self._size, self._x, self._y + self._size),
                fill="white",
                width=1,
            )

    def switch(self) -> None:
        """Switch orientation between vertical and horizontal"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._orientation = 1 - self._orientation
        _LOGGER.info("%s switch to %s", now,self._orientation)
        self.update()

    def move(self) -> bool:
        """Moves the blinker to the next postion. Returns False if last position is reached."""
        self._x = self._x + self._step_size
        self._column = self._column + 1
        if self._x > self._max_x - self._step_size:
            self._x = self._step_size
            self._y = self.y + self._step_size
            self._row = self._row + 1
            self._column = 1

        if self._y > self._max_y - self._step_size:
            # no more positions to move to
            _LOGGER.info("no more positions to move to")
            return False

        return True

    def increase_size(self) -> int:
        """Increases the size of the blinker and returns te size."""
        self._size = self._size + 1 if self._size < self._max_size else self._max_size
        return self._size

    def decrease_size(self) -> int:
        """Increases the size of the blinker and returns te size."""
        self._size = self._size - 1 if self._size > self._min_size else self._min_size
        return self._size
