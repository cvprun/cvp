# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from typing import NewType
from unittest import TestCase, main

from cvp.resources.formats.yaml import YamlFormatPath
from cvp.resources.manager.manager import ResourceManager

_TestKey = NewType("_TestKey", str)


@dataclass
class _TestConfig:
    value: int = 0


class ManagerTestCase(TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.root_path = YamlFormatPath(self.tmpdir.name)
        self.manager = ResourceManager(_TestKey, _TestConfig, self.root_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_default(self):
        self.assertTrue(os.path.isdir(self.tmpdir.name))
        self.assertTrue(self.manager.root_dir.is_dir())

        filename0 = _TestKey("filename0")
        self.manager.add(filename0, _TestConfig(100))
        self.assertTrue(self.manager.exists_config_file(filename0))
        self.assertIn(filename0, self.manager)
        self.assertEqual(1, len(self.manager))

        filename1 = _TestKey("filename1")
        self.manager.add(filename1, _TestConfig(200))
        self.assertTrue(self.manager.exists_config_file(filename1))
        self.assertIn(filename1, self.manager)
        self.assertEqual(2, len(self.manager))

        path0 = self.root_path.as_path() / (filename0 + self.root_path.extension)
        self.assertTrue(path0.is_file())
        path1 = self.root_path.as_path() / (filename1 + self.root_path.extension)
        self.assertTrue(path1.is_file())
        self.assertEqual(2, len(list(self.root_path.iterdir())))

        path0.unlink()
        self.assertFalse(path0.exists())
        self.assertEqual(1, len(list(self.root_path.iterdir())))

        manager2 = deepcopy(self.manager)
        self.assertEqual(self.manager, manager2)

        manager2[filename0].value = 300
        del manager2[filename1]
        self.assertEqual(1, len(manager2))

        manager2.sync()
        self.assertEqual(2, len(manager2))
        self.assertEqual(300, manager2[filename0].value)
        self.assertEqual(200, manager2[filename1].value)


if __name__ == "__main__":
    main()
