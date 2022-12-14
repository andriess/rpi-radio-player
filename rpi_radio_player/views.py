from adafruit_rgb_display.rgb import DisplaySPI
from PIL import Image

class StationListView():
    def __init__(self, display: DisplaySPI) -> None:
        self._display = display
        print("Initialized the display.")

    def show(self, image: Image) -> None:
        self._display.image(image)
