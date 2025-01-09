# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.formats.cvp.file import CvpFile
from cvp.variables import CVP_EXTENSION, CVP_ROOT_INFO_FILENAME


class FileTestCase(TestCase):
    def test_variables(self):
        self.assertEqual(CVP_EXTENSION, CvpFile.EXTENSION)
        self.assertEqual(CVP_ROOT_INFO_FILENAME, CvpFile.ROOT_INFO_FILENAME)

    def test_file(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(str(tmpdir)))


if __name__ == "__main__":
    main()
