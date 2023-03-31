"""Class for storing user settings"""
from dataclasses import dataclass


@dataclass
class UserSettings:
    thickness: int = 3
    speed: int = 500
    size_horizontal: int = 5
    size_vertical: int = 3
