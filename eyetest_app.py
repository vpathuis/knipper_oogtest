"""The EyeTestApp is a tkinter window defining the frames and canvas needed for the eye test."""
import logging
import tkinter as tk
import csv
import datetime
from dataclasses import dataclass

from blinker import Blinker
from grid import EyeTestGrid
from settings import UserSettings

_LOGGER = logging.getLogger(__name__)


class EyeTestApp(tk.Tk):
    """The window where the eye test happens"""

    # switch_timer = None
    max_x: int = 1000
    max_y: int = 800
    blinker_switcher = None

    class UserInput:
        """Defines the fields for user input"""

        def __init__(self, frame: tk.Frame, settings: UserSettings):
            self._frame = frame
            self._settings = settings

        def read(self) -> UserSettings:
            """Update settings from user input."""
            return UserSettings(
                int(self.ent_thickness.get()),
                int(self.ent_speed.get()),
                int(self.ent_size_horizontal.get()),
                int(self.ent_size_vertical.get()),
            )

        def place(self):
            """Place the user setting fields on the frame"""
            self.ent_size_horizontal = add_entry(
                self._frame, "Horizontaal", self._settings.size_horizontal
            )
            self.ent_size_vertical = add_entry(
                self._frame, "Verticaal", self._settings.size_vertical
            )
            self.ent_thickness = add_entry(
                self._frame, "Dikte", self._settings.thickness
            )
            self.ent_speed = add_entry(self._frame, "Snelheid", self._settings.speed)

            self._frame.place(relx=0.3, y=50, anchor=tk.NW)

    def __init__(self):
        # window = tk.Tk()
        super().__init__()
        self._score = []
        self.settings = UserSettings()
        self.blinker = None

        self.title("Knipper Oogtest")

        # Greater layout: right and left
        frm_left = tk.Frame(master=self, width=300, height=800, bg="lightgrey")
        frm_right = tk.Frame(
            master=self, width=1000, height=800, bg="black"
        )  # Initial size only

        # Left frame, containing subframes
        frm_user_input = tk.Frame(master=frm_left)

        self.user_input = self.UserInput(frm_user_input, self.settings)
        self.user_input.place()

        # Frame for buttons and orientation text
        frm_orientation_text = tk.Frame(master=frm_left)

        frm_buttons = tk.Frame(master=frm_orientation_text)
        self.btn_start = add_button(frm_buttons, "Start", self.start_eye_test)
        self.btn_pause = add_button(frm_buttons, "Pauze", self.pause_test)
        self.btn_stop = add_button(frm_buttons, "Stop", self.end_eye_test)
        frm_buttons.pack()

        lbl_orientation_point = tk.Label(
            master=frm_orientation_text,
            text="Kijk hier\nPage up/down: groter/kleiner\nSpatie als je beweging nog ziet\nPijltjes om rond te wandelen",
            font=("Arial 14 bold"),
        )

        # Create updatable text containing the current size of the blinker
        self.size_text = tk.StringVar()
        self.size_text.set("Grootte = ..")
        lbl_size = tk.Label(
            master=frm_orientation_text,
            textvariable=self.size_text,
            font=("Arial 14 bold"),
        )

        # Create updatable text containing the current size of the blinker
        self.status_text = tk.StringVar()
        self.status_text.set("")
        lbl_status = tk.Label(
            master=frm_orientation_text,
            textvariable=self.status_text,
            font=("Arial 14 bold"),
        )

        lbl_orientation_point.pack()
        lbl_size.pack()
        lbl_status.pack()

        frm_orientation_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Show the left frame
        frm_left.pack(fill=tk.BOTH, side=tk.LEFT)

        # Right frame containing the canvas
        self.canvas = tk.Canvas(
            frm_right,
            width=self.max_x,
            height=self.max_y,
            bg="darkgrey",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Show the right frame
        frm_right.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Key bindings
        self.bind("<Up>", self.press_up)
        self.bind("<Down>", self.press_down)
        self.bind("<space>", self.press_space)
        self.bind("<Right>", self.press_right)
        self.bind("<Escape>", self.press_esc)
        self.bind("<Left>", self.press_left)
        self.bind("<Prior>", self.press_bigger)
        self.bind("<Next>", self.press_smaller)

    def start_eye_test(self, _) -> None:
        """Create and start the blinker"""

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        _LOGGER.info(f"Width = %s", width)
        _LOGGER.info(f"Height = %s", height)

        if self.blinker_switcher:
            self.after_cancel(self.blinker_switcher)
        self.canvas.focus_set()
        self.canvas.delete(tk.ALL)

        self.settings = self.user_input.read()

        self.grid = EyeTestGrid(
            self.canvas, self.settings.size_horizontal, self.settings.size_vertical
        )

        self.blinker = Blinker(
            self.canvas, self.settings.thickness, self.grid.screen_position()
        )
        self.blinker_switcher = self.after(self.settings.speed, self.switch_blinker)
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")
        self.report_status()

    def end_eye_test(self, _) -> None:
        """Everything done"""
        if self.blinker:
            self.after_cancel(self.blinker_switcher)
            self.blinker.clear()
            self.blinker = None
            self.export_score()
            self.size_text.set("Klaar! Export is gemaakt.")

    def pause_test(self, _) -> None:
        """Pause the test or continue if paused"""
        if self.blinker:
            if self.blinker_switcher:
                self.after_cancel(self.blinker_switcher)
                self.blinker_switcher = None
                self.blinker.clear()
                self.btn_pause.configure(text="Verder")
            else:
                self.blinker_switcher = self.after(
                    self.settings.speed, self.switch_blinker
                )
                self.btn_pause.configure(text="Pauze")

    def switch_blinker(self):
        """Switch the orientation of the blinker after each second"""
        self.blinker.switch()
        self.blinker_switcher = self.after(self.settings.speed, self.switch_blinker)

    def press_esc(self, _) -> None:
        """End test is Escape is pressed"""
        if self.blinker:
            self.end_eye_test(_)

    def press_bigger(self, _) -> None:
        """Make size bigger"""
        if self.blinker:
            self.blinker.increase_size()
            self.size_text.set(f"Grootte = {str(self.blinker.size)}")
            self.blinker.update()

    def press_smaller(self, _) -> None:
        """Make size smaller"""
        if self.blinker:
            self.blinker.decrease_size()
            self.size_text.set(f"Grootte = {str(self.blinker.size)}")
            self.blinker.update()

    def press_space(self, _) -> None:
        """Report size"""
        if self.blinker:
            # score_id = self.grid.score_lbl_id()
            # if score_id:
            #     self.canvas.delete(score_id)

            self.new_score()
            # self.grid.keep_score(self.blinker.size, score_lbl_id)
            if self.grid.move("F"):
                self.blinker.move(self.grid.screen_position())

            # disable score text if already scored, so test can be seen clearly
            self.disable_score()
            self.report_status()

    def press_right(self, event) -> None:
        """Move to the next grid point"""

        # first enable previous score, if available and disabled
        self.restore_score()

        # Move in the grid
        if self.grid.move("F"):
            # And move to blinker the next position
            self.blinker.move(self.grid.screen_position())

        # disable score text if already scored, so test can be seen clearly
        self.disable_score()
        self.report_status()

    def press_left(self, event) -> None:
        # first enable previous score, if available and disabled
        self.restore_score()

        if self.grid.move("B"):
            # now move to the next position
            self.blinker.move(self.grid.screen_position())

        # disable score text if already scored previously
        self.disable_score()
        self.report_status()

    def press_up(self, event) -> None:
        # first enable previous score, if available and disabled
        self.restore_score()

        if self.grid.move("U"):
            # now move to the next position
            self.blinker.move(self.grid.screen_position())

        # disable score text if already scored previously
        self.disable_score()
        self.report_status()

    def press_down(self, event) -> None:
        # first enable previous score, if available and disabled
        self.restore_score()

        if self.grid.move("D"):
            # now move to the next position
            self.blinker.move(self.grid.screen_position())

        # disable score text if already scored previously
        self.disable_score()
        self.report_status()

    def export_score(self) -> None:
        """Export the score to a csv file."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
        with open(f"score_{now}.csv", "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(self._score)

    def new_score(self):
        """Add a score label to the canvas at the current position"""

        # score_id = self.grid.score_lbl_id()
        # if score_id:
        #     self.canvas.delete(score_id)

        score_lbl_id = self.canvas.create_text(
            self.grid.screen_position().x,
            self.grid.screen_position().y,
            text=str(self.blinker.size),
            fill="lightgrey",
            font="Arial 14 bold",
        )
        self.grid.keep_score(self.blinker.size, score_lbl_id)
        _LOGGER.info(f"New score id for %s: %s", self.grid.position, score_lbl_id)

    def disable_score(self):
        """Disables a score label so the test can be seen clearly. Returns True if it is already scored."""
        score_lbl_id = self.grid.score_lbl_id()
        if score_lbl_id:
            _LOGGER.info(
                f"disabling score id %s for %s", score_lbl_id, self.grid.position
            )
            self.canvas.delete(score_lbl_id)

    def restore_score(self):
        """Add the previous score to a new label on the canvas at the current position"""

        score = self.grid.score()
        if score:
            score_lbl_id = self.canvas.create_text(
                self.grid.screen_position().x,
                self.grid.screen_position().y,
                text=str(score),
                fill="lightgrey",
                font="Arial 14 bold",
            )
            # store new label id:
            self.grid.keep_score(score, score_lbl_id)
            _LOGGER.info(
                f"restored score id %s for %s", score_lbl_id, self.grid.position
            )

    def report_status(self):
        if self.grid:
            score = self.grid.score()
            if score:
                self.status_text.set(f"Deze is al gedaan")
                if self.grid.to_go() == 0:
                    self.status_text.set(f"Allemaal gedaan!")
            else:
                self.status_text.set(f"Deze moet nog")


def add_entry(frame, label: str, value: int | str) -> tk.Entry:
    """Adds a button to a frame, returning the handle for the entry field."""
    tk.Label(
        master=frame,
        text=label,
        font=("Arial 14 bold"),
    ).pack(side=tk.TOP)
    entry = tk.Entry(master=frame, bg="white", width=5)
    entry.insert(0, str(value))
    entry.pack(side=tk.TOP)
    return entry


def add_button(frame, label: str, bind) -> tk.Button:
    """Adds a button, returning the handle."""
    button = tk.Button(master=frame, text=label)
    button.pack(side=tk.LEFT)
    button.bind("<Button-1>", bind)
    return button
