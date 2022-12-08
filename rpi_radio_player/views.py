from typing import TypeVar
from adafruit_rgb_display.rgb import DisplaySPI

D = TypeVar('D', bound=DisplaySPI)
class StationListView():
    def __init__(self, display):
        self._display = display

    def show(self, image):
        self._display.image(image)
