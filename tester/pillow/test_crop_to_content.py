# -*- coding: utf-8 -*-

from unittest import TestCase, main

from PIL import Image

from cvp.pillow.crop_to_content import crop_bottom_to_content


class CropToContentTestCase(TestCase):
    def test_crop_bottom_to_content(self):
        image = Image.new("RGBA", size=(10, 10), color=(0, 0, 0, 0))
        red_color = 255, 0, 0, 255

        for y in range(0, 5):
            for x in range(0, 10):
                image.putpixel((x, y), red_color)

        cropped = crop_bottom_to_content(image)
        self.assertTupleEqual((10, 5), cropped.size)
        self.assertTupleEqual(red_color, cropped.getpixel((0, 0)))
        self.assertTupleEqual(red_color, cropped.getpixel((0, 4)))


if __name__ == "__main__":
    main()
