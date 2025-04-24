# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.config.sections.ffmpeg import FFmpegConfig


class FFmpegTestCase(TestCase):
    def test_proxy(self):
        config = FFmpegConfig()
        proxy1 = config.create_ffmpeg_proxy()
        proxy2 = config.create_ffmpeg_proxy()

        self.assertEqual("ffmpeg", config.ffmpeg)
        self.assertEqual("ffmpeg", proxy1.get())
        self.assertEqual("ffmpeg", proxy2.get())

        config.ffmpeg = "0"
        self.assertEqual("0", config.ffmpeg)
        self.assertEqual("0", proxy1.get())
        self.assertEqual("0", proxy2.get())

        proxy1.set("1")
        self.assertEqual("1", config.ffmpeg)
        self.assertEqual("1", proxy1.get())
        self.assertEqual("1", proxy2.get())

        proxy2.set("2")
        self.assertEqual("2", config.ffmpeg)
        self.assertEqual("2", proxy1.get())
        self.assertEqual("2", proxy2.get())


if __name__ == "__main__":
    main()
