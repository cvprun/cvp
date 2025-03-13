# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from pathlib import Path
from typing import Any
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.modules.class_path import ClassPath


class ClassPathTestCase(TestCase):
    def test_default(self):
        cpath0 = ClassPath("pathlib.Path")
        cpath1 = ClassPath(Path)

        self.assertIsInstance(cpath0.type, type)
        self.assertIsInstance(cpath1.type, type)
        self.assertTrue(issubclass(cpath0.type, Path))
        self.assertTrue(issubclass(cpath1.type, Path))

        self.assertEqual(cpath0.type, cpath1.type)
        self.assertEqual(cpath0.path, cpath1.path)

        self.assertEqual(cpath0.path, "pathlib.Path")
        self.assertEqual(cpath1.path, "pathlib.Path")
        self.assertEqual(cpath0.module_path, "pathlib")
        self.assertEqual(cpath1.module_path, "pathlib")
        self.assertEqual(cpath0.class_name, "Path")
        self.assertEqual(cpath1.class_name, "Path")

        path0 = cpath0("./aaa")
        path1 = cpath1("./aaa")
        self.assertIsInstance(path0, Path)
        self.assertIsInstance(path1, Path)

    def test_none_value(self):
        cpath0 = ClassPath(None)
        cpath1 = ClassPath(type(None))
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_none(self):
        cpath0 = ClassPath(type(None))
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_bool(self):
        cpath0 = ClassPath(bool)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_int(self):
        cpath0 = ClassPath(int)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_float(self):
        cpath0 = ClassPath(float)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_bytes(self):
        cpath0 = ClassPath(bytes)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_str(self):
        cpath0 = ClassPath(str)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_object(self):
        cpath0 = ClassPath(object)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_complex(self):
        cpath0 = ClassPath(complex)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_any(self):
        cpath0 = ClassPath(Any)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_serialize_deserialize_path(self):
        cpath0 = ClassPath(Path)
        cpath1 = deserialize(serialize(cpath0), ClassPath)
        self.assertEqual(cpath0, cpath1)

    def test_copy(self):
        cpath0 = ClassPath(Path)
        self.assertEqual(copy(cpath0), cpath0)

    def test_deepcopy(self):
        cpath0 = ClassPath(Path)
        self.assertEqual(deepcopy(cpath0), cpath0)


if __name__ == "__main__":
    main()
