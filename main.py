# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import datetime
import logging
import tkinter as tk

logging.basicConfig(level=logging.INFO)

class Blinker:
    """A `blinking` cross that moves over the canvas."""

    _min_size = 1
    _max_size = 100
    _default_size: int = 10

    def __init__(self, canvas: tk.Canvas, max_x: int, max_y: int, step_size: int) -> None:
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
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def size(self):
        return self._size

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def clear(self):
        self.canvas.delete(self._horizontal_line)
        self.canvas.delete(self._vertical_line)

    def update(self):
        """ Update the blinker on the canvas. """
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
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._orientation = 1 - self._orientation
        _LOGGER.info(f"{now} switch to {self._orientation}")
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


class EyeTestApp(tk.Tk):
    """The window where the eye test happens"""

    # switch_timer = None
    max_x: int = 1000
    max_y: int = 800
    blinker_switcher = None

    def __init__(self):
        # window = tk.Tk()
        super().__init__()
        self._step_size = 100
        self._score = []

        self.title("Knipper Oogtest")

        # Greater layout: right and left
        frm_left = tk.Frame(master=self, width=300, height=800, bg="white")
        frm_right = tk.Frame(master=self, width=1000, height=800, bg="black")

        # Left frame, containing subframes
        frm_user_input = tk.Frame(master=frm_left)
        frm_orientation_text = tk.Frame(master=frm_left)

        # Frame for user input
        lbl_step_size = tk.Label(
            master=frm_user_input,
            text="Stapgrootte",
            font=("Arial 14 bold"),
        )
        lbl_step_size.pack(side=tk.LEFT)
        self.ent_step_size = tk.Entry(master=frm_user_input, bg="white", width=5)
        self.ent_step_size.insert(0, str(self._step_size))
        self.ent_step_size.pack(side=tk.LEFT)
        frm_user_input.place(x=50, y=50, anchor=tk.NW)

        btn_start = tk.Button(master=frm_user_input, text="Start")
        btn_start.pack(side=tk.LEFT)
        btn_start.bind("<Button-1>", self.start_eye_test)

        # Frame for orientation text
        lbl_orientation_point = tk.Label(
            master=frm_orientation_text,
            text="Kijk hier\nPijltjes: groter/kleiner\nSpatie als je beweging nog ziet",
            font=("Arial 14 bold")
        )

        # Create updatable text containing the current size of the blinker
        self.size_text = tk.StringVar()
        self.size_text.set(f"Grootte = ..")
        lbl_size = tk.Label(
            master=frm_orientation_text,
            textvariable=self.size_text,
            font=("Arial 14 bold")
        )
        lbl_orientation_point.pack()
        lbl_size.pack()

        frm_orientation_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Show the left frame
        frm_left.pack(fill=tk.BOTH, side=tk.LEFT)

        # Right frame containing the canvas
        self.canvas = tk.Canvas(
            frm_right,
            width=self.max_x,
            height=self.max_y,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH)

        # Show the right frame
        frm_right.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Key bindings
        self.bind("<Up>", self.press_up)
        self.bind("<Down>", self.press_down)
        self.bind("<space>", self.press_space)
        self.bind("<Escape>", self.press_esc)

    def start_eye_test(self, event) -> None:
        # Create and start the blinker
        if self.blinker_switcher:
            self.after_cancel(self.blinker_switcher)
        self.canvas.focus_set()
        self.canvas.delete(tk.ALL)
        self._step_size = int(self.ent_step_size.get())
        self._score = []

        self.blinker = Blinker(self.canvas, self.max_x, self.max_y, self._step_size)
        self.blinker_switcher = self.after(1000, self.switch_blinker)
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")

    def end_eye_test(self):
        """Everything done"""
        self.after_cancel(self.blinker_switcher)
        self.blinker.clear()
        self.blinker = None
        self.export_score()
        self.size_text.set("Klaar!")

    def switch_blinker(self):
        self.blinker.switch()
        self.blinker_switcher = self.after(1000, self.switch_blinker)

    def press_esc(self, event) -> None:
        self.end_eye_test()

    def press_up(self, event) -> None:
        """Make size bigger"""
        self.blinker.increase_size()
        # self.size = self.size + 1 if self.size < self._max_size else self._max_size
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")
        self.blinker.update()

    def press_down(self, event) -> None:
        """Make size smaller"""
        self.blinker.decrease_size()
        # self.size = self.size - 1 if self.size > self._min_size else self._min_size
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")
        self.blinker.update()

    def press_space(self, event) -> None:
        # Report size
        if self.blinker:
            self.canvas.create_text(self.blinker.x, self.blinker.y, text=str(self.blinker.size), fill="white",
                                    font=("Arial 14 bold"))
            if len(self._score) <= self.blinker.row:
                self._score.append([])
            self._score[self.blinker.row].append(self.blinker.size)
            if self.blinker.move():
                self.blinker.update()
            else:
                self.end_eye_test()

    def export_score(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
        with open(f"score_{now}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f,  delimiter=";")
            writer.writerows(self._score)


if __name__ == "__main__":
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("started")

    eye_test_app = EyeTestApp()
    eye_test_app.mainloop()
