# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.resources.formats.yaml import YamlFormatPath
from cvp.resources.manager.manager import ResourceManager


@dataclass
class TestConfig:
    value: int = 0


class ManagerTestCase(TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.root_path = YamlFormatPath(self.tmpdir.name)
        self.manager = ResourceManager[TestConfig](TestConfig, self.root_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_default(self):
        self.assertTrue(os.path.isdir(self.tmpdir.name))
        self.assertTrue(self.manager.root_dir.is_dir())

        filename0 = "filename0"
        self.manager.add(filename0, TestConfig(100))
        self.assertTrue(self.manager.exists(filename0))
        self.assertIn(filename0, self.manager)
        self.assertEqual(1, len(self.manager))

        filename1 = "filename1"
        self.manager.add(filename1, TestConfig(200))
        self.assertTrue(self.manager.exists(filename1))
        self.assertIn(filename1, self.manager)
        self.assertEqual(2, len(self.manager))

        path0 = self.root_path.as_path() / (filename0 + self.root_path.extension)
        self.assertTrue(path0.is_file())

        path1 = self.root_path.as_path() / (filename1 + self.root_path.extension)
        self.assertTrue(path1.is_file())

        manager2 = deepcopy(self.manager)
        self.assertEqual(self.manager, manager2)
        manager2.clear()


if __name__ == "__main__":
    main()
