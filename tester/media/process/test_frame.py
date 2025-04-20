# -*- coding: utf-8 -*-

from io import StringIO
from shutil import which
from unittest import TestCase, main, skipIf

import numpy as np

from cvp.media.process.frame import FrameReaderProcess


class FrameTestCase(TestCase):
    @skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
    def test_default(self):
        ffmpeg = which("ffmpeg")
        self.assertIsInstance(ffmpeg, str)

        duration = 3
        rate = 10
        width = 1920
        height = 1080
        pix_fmt = "rgb24"
        channels = 3
        frame_shape = width, height, channels
        array_shape = height, width, channels

        total_frames = duration * rate
        color = 253, 0, 0  # red

        input_buffer = StringIO()
        input_buffer.write("color=")
        input_buffer.write("c=red")
        input_buffer.write(f":duration={duration}")
        input_buffer.write(f":size={width}x{height}")
        input_buffer.write(f":rate={rate}")
        input_file = input_buffer.getvalue()

        args = (
            ffmpeg,
            "-f",
            "lavfi",
            "-i",
            input_file,
            "-pix_fmt",
            pix_fmt,
            "-f",
            "rawvideo",
            "pipe:1",
        )

        frames = list()

        def on_frame(data: bytes) -> None:
            frames.append(np.ndarray(array_shape, dtype=np.uint8, buffer=data))

        popen = FrameReaderProcess(
            type(self).__name__,
            args,
            frame_shape,
            target=on_frame,
        )
        popen.thread.start()
        popen.thread.join()

        self.assertIsNone(popen.thread_error)
        self.assertEqual(total_frames, len(frames))
        for frame in frames:
            self.assertTrue(np.all(frame[:, :] == color))


if __name__ == "__main__":
    main()
