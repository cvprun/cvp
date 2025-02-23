# -*- coding: utf-8 -*-

from collections import deque
from io import BytesIO
from unittest import TestCase, main

from cvp.buffers.frame import FrameBuffer


class FrameTestCase(TestCase):
    def test_default(self):
        pipe = BytesIO(bytearray(i for i in range(7)))
        frames = deque()

        def on_frame(data: bytes) -> None:
            frames.append(data)

        reader = FrameBuffer(pipe, 5, target=on_frame)
        reader.read()
        self.assertEqual(1, len(frames))
        self.assertIsNone(reader.remain)

        frame0 = frames.popleft()
        self.assertEqual(0, len(frames))
        self.assertEqual(b"\x00\x01\x02\x03\x04", frame0)

        reader.read()
        self.assertEqual(0, len(frames))
        self.assertEqual(b"\x05\x06", reader.remain)

        pipe.seek(0)
        pipe.write(bytearray(i for i in range(7, 27)))
        pipe.seek(0)

        reader.read()
        self.assertEqual(1, len(frames))
        self.assertIsNone(reader.remain)

        frame1 = frames.popleft()
        self.assertEqual(0, len(frames))
        self.assertEqual(b"\x05\x06\x07\x08\x09", frame1)

        reader.read()
        self.assertEqual(1, len(frames))
        self.assertIsNone(reader.remain)

        frame2 = frames.popleft()
        self.assertEqual(0, len(frames))
        self.assertEqual(b"\x0a\x0b\x0c\x0d\x0e", frame2)

        reader.flush()
        reader.read_eof()
        self.assertEqual(2, len(frames))
        self.assertIsNotNone(reader.remain)

        frame3 = frames.popleft()
        frame4 = frames.popleft()
        self.assertEqual(0, len(frames))
        self.assertEqual(b"\x0f\x10\x11\x12\x13", frame3)
        self.assertEqual(b"\x14\x15\x16\x17\x18", frame4)
        self.assertEqual(b"\x19\x1a", reader.remain)

        reader.clear_remain()
        reader.read()
        self.assertEqual(0, len(frames))
        self.assertIsNone(reader.remain)

        reader.read_eof()
        self.assertEqual(0, len(frames))
        self.assertIsNone(reader.remain)


if __name__ == "__main__":
    main()
