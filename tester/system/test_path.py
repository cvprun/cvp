# -*- coding: utf-8 -*-

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.paths.flavour import PathFlavour


class _TestPath(PathFlavour):
    pass


class PathTestCase(TestCase):
    def test_home(self):
        home_dir0 = _TestPath.home()
        home_dir1 = Path.home()
        self.assertEqual(home_dir0.resolve(), home_dir1.resolve())

    def test_same_dir(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))
            self.assertTrue(_TestPath(tmpdir).is_dir())
            self.assertEqual(os.path.abspath(tmpdir), str(_TestPath(tmpdir).resolve()))

    def test_truediv(self):
        download_dirname = "Downloads"

        down_dir0 = _TestPath.home() / download_dirname
        self.assertIsInstance(down_dir0, _TestPath)

        down_dir1 = os.path.join(os.path.expanduser("~"), download_dirname)
        self.assertEqual(down_dir1, str(down_dir0))


if __name__ == "__main__":
    main()
