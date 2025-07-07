# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.protocols import has_input_protocol, has_output_protocol


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class ProtocolsTestCase(TestCase):
    def test_has_http(self):
        self.assertTrue(has_input_protocol("http"))
        self.assertTrue(has_output_protocol("http"))

    def test_has_pipe(self):
        self.assertTrue(has_input_protocol("pipe"))
        self.assertTrue(has_output_protocol("pipe"))


if __name__ == "__main__":
    main()
