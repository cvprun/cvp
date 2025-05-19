# -*- coding: utf-8 -*-

from PIL.Image import Image

from cvp.variables import NOT_FOUND_INDEX


def find_last_opaque_y(image: Image) -> int:
    if image.mode != "RGBA":
        raise ValueError("Only RGBA images are supported")

    width, height = image.size
    pixels = image.load()
    if pixels is None:
        raise ValueError("Inaccessible pixels")

    # Scan from the bottom upward to find the last non-transparent y-coordinate
    for y in reversed(range(height)):
        for x in range(width):
            pixel = pixels[x, y]
            assert isinstance(pixel, tuple)
            assert 4 == len(pixel)
            r, g, b, a = pixel
            if a != 0:
                return y

    return NOT_FOUND_INDEX


def crop_bottom_to_content(image: Image) -> Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    last_opaque_y = find_last_opaque_y(image)

    # If the whole image is transparent, avoid cropping to height 0
    if last_opaque_y <= 0:
        last_opaque_y = 0

    return image.crop((0, 0, image.width, last_opaque_y + 1))
