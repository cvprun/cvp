# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from pathlib import Path
from typing import Any
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.nodes.base import NodeBase
from cvp.nodes.ntype import Ntype, isnode
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import EmptyNextPin
from cvp.types.override import override


class _TestNode(NodeBase):
    @override
    def run(self, record: NodeRecord) -> Pin:
        return self.nonext()

    @override
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError


class NtypeTestCase(TestCase):
    def test_default(self):
        nt = Ntype(abs)

        self.assertTrue(isnode(nt.type))
        self.assertIs(nt.type, abs)

        self.assertEqual(nt.path, "builtins.abs")
        self.assertEqual(nt.module_path, abs.__module__)
        self.assertEqual(nt.class_name, abs.__name__)

    def test_serialize_deserialize_bool(self):
        ntype0 = Ntype(bool)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, bool)
        self.assertEqual("builtins.bool", ntype0.path)
        self.assertEqual(True, ntype0(1))

    def test_serialize_deserialize_int(self):
        ntype0 = Ntype(int)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, int)
        self.assertEqual("builtins.int", ntype0.path)
        self.assertEqual(10, ntype0(10))

    def test_serialize_deserialize_float(self):
        ntype0 = Ntype(float)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, float)
        self.assertEqual("builtins.float", ntype0.path)
        self.assertEqual(10.1, ntype0(10.1))

    def test_serialize_deserialize_str(self):
        ntype0 = Ntype(str)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, str)
        self.assertEqual("builtins.str", ntype0.path)
        self.assertEqual("abc", ntype0("abc"))

    def test_serialize_deserialize_bytes(self):
        ntype0 = Ntype(bytes)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, bytes)
        self.assertEqual("builtins.bytes", ntype0.path)
        self.assertEqual(b"abc", ntype0(b"abc"))

    def test_serialize_deserialize_object(self):
        ntype0 = Ntype(object)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, object)
        self.assertEqual("builtins.object", ntype0.path)
        self.assertIsInstance(ntype0(), object)

    def test_serialize_deserialize_complex(self):
        ntype0 = Ntype(complex)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, complex)
        self.assertEqual("builtins.complex", ntype0.path)
        self.assertEqual(10 + 5j, ntype0(complex(10, 5)))

    def test_serialize_deserialize_any(self):
        ntype0 = Ntype(Any)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, Any)
        self.assertEqual("typing.Any", ntype0.path)

    def test_serialize_deserialize_path(self):
        ntype0 = Ntype(Path)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, Path)
        self.assertEqual("pathlib.Path", ntype0.path)

        downloads_path = ntype0("Downloads")
        self.assertIsInstance(downloads_path, Path)
        self.assertEqual("Downloads", str(downloads_path))

    def test_serialize_deserialize_test(self):
        node = _TestNode()
        ntype0 = Ntype.from_node(node)
        ntype1 = deserialize(serialize(ntype0), Ntype)
        self.assertEqual(ntype0, ntype1)
        self.assertEqual(ntype0.type, _TestNode)
        self.assertEqual("tester.nodes.test_ntype._TestNode", ntype0.path)
        self.assertIsInstance(ntype0(), EmptyNextPin)

    def test_copy(self):
        ntype0 = Ntype(Path)
        self.assertEqual(copy(ntype0), ntype0)

    def test_deepcopy(self):
        ntype0 = Ntype(Path)
        self.assertEqual(deepcopy(ntype0), ntype0)


if __name__ == "__main__":
    main()
