import os

from PIL import Image, ImageOps

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

        return processed_image
