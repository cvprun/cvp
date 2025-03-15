# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from pathlib import Path
from typing import Any
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.inspect.parameter import NoDefault


class DtypeTestCase(TestCase):
    def test_default(self):
        dt = Dtype(Path)

        self.assertIsInstance(dt.type, type)
        self.assertTrue(issubclass(dt.type, Path))
        self.assertIs(dt.type, Path)

        self.assertEqual(dt.path, "pathlib.Path")
        self.assertEqual(dt.module_path, Path.__module__)
        self.assertEqual(dt.class_name, Path.__name__)

    def test_none(self):
        cpath0 = Dtype(None)
        cpath1 = Dtype(type(None))
        cpath2 = Dtype.none()
        self.assertEqual(cpath0, cpath1)
        self.assertEqual(cpath0, cpath2)

    def test_any(self):
        cpath0 = Dtype(Any)
        cpath1 = Dtype(NoDefault)
        cpath2 = Dtype.any()
        self.assertEqual(cpath0, cpath1)
        self.assertEqual(cpath0, cpath2)

    def test_serialize_deserialize_none(self):
        dtype0 = Dtype(None)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, type(None))
        self.assertEqual("builtins.NoneType", dtype0.path)

    def test_serialize_deserialize_bool(self):
        dtype0 = Dtype(bool)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, bool)
        self.assertEqual("builtins.bool", dtype0.path)
        self.assertEqual(True, dtype0(1))

    def test_serialize_deserialize_int(self):
        dtype0 = Dtype(int)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, int)
        self.assertEqual("builtins.int", dtype0.path)
        self.assertEqual(10, dtype0(10))

    def test_serialize_deserialize_float(self):
        dtype0 = Dtype(float)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, float)
        self.assertEqual("builtins.float", dtype0.path)
        self.assertEqual(10.1, dtype0(10.1))

    def test_serialize_deserialize_str(self):
        dtype0 = Dtype(str)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, str)
        self.assertEqual("builtins.str", dtype0.path)
        self.assertEqual("abc", dtype0("abc"))

    def test_serialize_deserialize_bytes(self):
        dtype0 = Dtype(bytes)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, bytes)
        self.assertEqual("builtins.bytes", dtype0.path)
        self.assertEqual(b"abc", dtype0(b"abc"))

    def test_serialize_deserialize_object(self):
        dtype0 = Dtype(object)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, object)
        self.assertEqual("builtins.object", dtype0.path)
        self.assertIsInstance(dtype0(), object)

    def test_serialize_deserialize_complex(self):
        dtype0 = Dtype(complex)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, complex)
        self.assertEqual("builtins.complex", dtype0.path)
        self.assertEqual(10 + 5j, dtype0(complex(10, 5)))

    def test_serialize_deserialize_any(self):
        dtype0 = Dtype(Any)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, Any)
        self.assertEqual("typing.Any", dtype0.path)

    def test_serialize_deserialize_path(self):
        dtype0 = Dtype(Path)
        dtype1 = deserialize(serialize(dtype0), Dtype)
        self.assertEqual(dtype0, dtype1)
        self.assertEqual(dtype0.type, Path)
        self.assertEqual("pathlib.Path", dtype0.path)

        downloads_path = dtype0("Downloads")
        self.assertIsInstance(downloads_path, Path)
        self.assertEqual("Downloads", str(downloads_path))

    def test_copy(self):
        dtype0 = Dtype(Path)
        self.assertEqual(copy(dtype0), dtype0)

    def test_deepcopy(self):
        dtype0 = Dtype(Path)
        self.assertEqual(deepcopy(dtype0), dtype0)


if __name__ == "__main__":
    main()
