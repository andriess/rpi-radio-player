import os
import digitalio

from PIL import Image, ImageOps
from adafruit_rgb_display.st7789 import ST7789


class ProcessImageComponent():
    def __init__(self, width: int, height: int, folder: str) -> None:
        self._width = width
        self._height = height
        self._folder = folder

    def process_image(self, image_name: str) -> Image:
        image_file = os.path.join(self._folder, image_name)
        image_obj = Image.open(image_file)

        processed_image = ImageOps.pad(
            image_obj.convert("RGB"),
            (self._width, self._height),
            method=Image.NEAREST,
            color=(0, 0, 0),
            centering=(0.5, 0.5),
        )

        print(f"Processed image: {image_name}")
        return processed_image

class DisplayComponent():
    def __init__(self, spi, cs_pin, dc_pin, bl_pin, y_offset, baudrate) -> None:
        self._display = ST7789(spi, cs=cs_pin, dc=dc_pin, y_offset=y_offset, baudrate=baudrate)
        self._bl_pin = bl_pin
        self._bl_pin.direction = digitalio.Direction.OUTPUT

    def show_image(self, image: Image) -> None:
        self._display.image(image)

    def backlight_on(self):
        self._bl_pin.value = True

    def backlight_off(self):
        self._bl_pin.value = False
