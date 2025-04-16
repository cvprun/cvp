# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field
from tempfile import TemporaryDirectory
from typing import NewType
from unittest import TestCase, main
from uuid import uuid4

from cvp.resources.formats.yaml import YamlFormatPath
from cvp.resources.manager.manager import ResourceManager

TestConfigFilename = NewType("TestConfigFilename", str)


@dataclass
class TestConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    value: int = 0


TestManager = ResourceManager[TestConfigFilename, TestConfig]


class ManagerTestCase(TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.root_path = YamlFormatPath(self.tmpdir.name)
        self.manager = TestManager(TestConfig, self.root_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_default(self):
        self.assertTrue(os.path.isdir(self.tmpdir.name))
        self.assertTrue(self.manager.root_dir.is_dir())
        self.assertFalse(self.manager.list_config_filenames())


if __name__ == "__main__":
    main()
