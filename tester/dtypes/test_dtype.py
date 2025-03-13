# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype


class DtypeTestCase(TestCase):
    def test_default(self):
        dt = Dtype(Path)

        self.assertIsInstance(dt.type, type)
        self.assertTrue(issubclass(dt.type, Path))
        self.assertIs(dt.type, Path)

        self.assertEqual(dt.module_path, Path.__module__)
        self.assertEqual(dt.class_name, Path.__name__)

        downloads_path = dt("Downloads")
        self.assertIsInstance(downloads_path, Path)
        self.assertEqual("Downloads", str(downloads_path))

    def test_serialize_deserialize_none(self):
        dtype0 = Dtype(type(None))
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, type(None))
        self.assertEqual("builtins.NoneType", dtype0.base.path)

    def test_serialize_deserialize_bool(self):
        dtype0 = Dtype(bool)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, bool)
        self.assertEqual("builtins.bool", dtype0.base.path)
        self.assertEqual(True, dtype0(1))

    def test_serialize_deserialize_int(self):
        dtype0 = Dtype(int)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, int)
        self.assertEqual("builtins.int", dtype0.base.path)
        self.assertEqual(10, dtype0(10))

    def test_serialize_deserialize_float(self):
        dtype0 = Dtype(float)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, float)
        self.assertEqual("builtins.float", dtype0.base.path)
        self.assertEqual(10.1, dtype0(10.1))

    def test_serialize_deserialize_object(self):
        dtype0 = Dtype(object)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, object)
        self.assertEqual("builtins.object", dtype0.base.path)

    def test_serialize_deserialize_complex(self):
        dtype0 = Dtype(complex)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, complex)
        self.assertEqual("builtins.complex", dtype0.base.path)

    def test_serialize_deserialize_any(self):
        dtype0 = Dtype(Any)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, Any)
        self.assertEqual("typing.Any", dtype0.base.path)

    def test_serialize_deserialize_path(self):
        dtype0 = Dtype(Path)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.base.type, Path)
        self.assertEqual("pathlib.Path", dtype0.base.path)


if __name__ == "__main__":
    main()
