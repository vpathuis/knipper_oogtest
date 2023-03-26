import tkinter as tk
from blinker import Blinker
import csv
import datetime


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
            font=("Arial 14 bold"),
        )

        # Create updatable text containing the current size of the blinker
        self.size_text = tk.StringVar()
        self.size_text.set(f"Grootte = ..")
        lbl_size = tk.Label(
            master=frm_orientation_text,
            textvariable=self.size_text,
            font=("Arial 14 bold"),
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
        """Switch the orientation of the blinker after each second"""
        self.blinker.switch()
        self.blinker_switcher = self.after(1000, self.switch_blinker)

    def press_esc(self, event) -> None:
        """End test is Escape is pressed"""
        self.end_eye_test()

    def press_up(self, event) -> None:
        """Make size bigger"""
        self.blinker.increase_size()
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")
        self.blinker.update()

    def press_down(self, event) -> None:
        """Make size smaller"""
        self.blinker.decrease_size()
        self.size_text.set(f"Grootte = {str(self.blinker.size)}")
        self.blinker.update()

    def press_space(self, event) -> None:
        # Report size
        if self.blinker:
            self.canvas.create_text(
                self.blinker.x,
                self.blinker.y,
                text=str(self.blinker.size),
                fill="white",
                font=("Arial 14 bold"),
            )
            if len(self._score) <= self.blinker.row:
                self._score.append([])
            self._score[self.blinker.row].append(self.blinker.size)
            if self.blinker.move():
                self.blinker.update()
            else:
                self.end_eye_test()

    def export_score(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
        with open(f"score_{now}.csv", "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(self._score)
