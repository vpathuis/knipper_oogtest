"""Main module for the Eye test."""

import logging
from eyetest_app import EyeTestApp

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    _LOGGER.info("started")

    eye_test_app = EyeTestApp()
    eye_test_app.mainloop()
