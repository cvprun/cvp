# -*- coding: utf-8 -*-

from typing import Any
from unittest import TestCase, main

from cvp.dtypes.dtype import default_dtype_path_with_type
from cvp.dtypes.registry.registry import DtypeRegistry


class RegistryTestCase(TestCase):
    def test_empty_register_dtype(self):
        registry = DtypeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry.path2dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry))

    def test_default_register_dtype(self):
        registry = DtypeRegistry()
        self.assertNotEqual(0, len(registry.path2dtypes))
        self.assertNotEqual(0, len(registry.type2dtypes))
        self.assertNotEqual(0, len(registry))

    def test_register_dtype_none(self):
        registry = DtypeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry.path2dtypes))
        self.assertEqual(0, len(registry.type2dtypes))

        registry.add_new(type(None))

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        none_dtype = registry.get("builtins.NoneType")
        self.assertEqual(type(None), none_dtype.type)
        self.assertEqual(type(None), registry.get(type(None)).type)

    def test_register_dtype_object(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(object)

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(object, registry.get(object).type)
        self.assertEqual(object, registry.get("builtins.object").type)

    def test_register_dtype_any(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(Any)

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(Any, registry.get(Any).type)
        self.assertEqual(Any, registry.get("typing.Any").type)

    def test_register_dtype_float(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(float)
        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(float, registry.get(float).type)
        self.assertEqual(float, registry.get("builtins.float").type)

    def test_register_dtype_custom(self):
        registry = DtypeRegistry(no_defaults=True)

        @registry.register()
        class _Custom(object):
            pass

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        test_path = default_dtype_path_with_type(_Custom)
        self.assertEqual("tester.dtypes.registry.test_registry._Custom", test_path)

        self.assertEqual(_Custom, registry.get(_Custom).type)
        self.assertEqual(_Custom, registry.get(test_path).type)


if __name__ == "__main__":
    main()
