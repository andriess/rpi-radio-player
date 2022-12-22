from adafruit_rgb_display.rgb import DisplaySPI
from adafruit_rgb_display import color565

from PIL import Image

from rpi_radio_player.components import  DisplayComponent

class StationListView():
    def __init__(self, display: DisplayComponent) -> None:
        self._display = display
        print("Initialized the display.")

    def show(self, image: Image) -> None:
        self._display.show_image(image)
