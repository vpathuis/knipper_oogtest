import tkinter as tk
import unittest

from src.eyetest_app import EyeTestApp
from src.settings import UserSettings


class TestEyeTestApp(unittest.TestCase):
    def test_settings(self):
        eye_test_app = EyeTestApp()
        eye_test_app.user_input.ent_thickness.delete(0, tk.END)
        eye_test_app.user_input.ent_thickness.insert(0, "5")
        eye_test_app.user_input.ent_speed.delete(0, tk.END)
        eye_test_app.user_input.ent_speed.insert(0, "100")
        eye_test_app.user_input.ent_size_horizontal.delete(0, tk.END)
        eye_test_app.user_input.ent_size_horizontal.insert(0, "3")
        eye_test_app.user_input.ent_size_vertical.delete(0, tk.END)
        eye_test_app.user_input.ent_size_vertical.insert(0, "2")
        settings = eye_test_app.user_input.read()
        expected_settings = UserSettings(5, 100, 3, 2)
        self.assertEqual(settings, expected_settings)

    def test_run(self):
        eye_test_app = EyeTestApp()
        eye_test_app.user_input.ent_speed.delete(0, tk.END)
        eye_test_app.user_input.ent_speed.insert(0, "100")
        eye_test_app.start_eye_test("")
        eye_test_app.press_space("")
        self.assertEqual(eye_test_app.grid.to_go(), 14)

        # eye_test_app.end_eye_test("")
        # # with patch("builtins.open") as mock_file:
        # with patch("csv.writer") as mock_csv_writer:
        #     mock_csv_writer.writerow.assert_has_calls([call("bla")])
        #


if __name__ == "__main__":
    unittest.main()
