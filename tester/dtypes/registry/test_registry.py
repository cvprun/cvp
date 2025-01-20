# -*- coding: utf-8 -*-

from typing import Any
from unittest import TestCase, main

from cvp.dtypes.registry.globals import GlobalDtypeRegistry, global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.variables import FLOW_PATH_SEPARATOR


class RegistryTestCase(TestCase):
    def test_global(self):
        registry0 = global_dtype_registry()
        registry1 = GlobalDtypeRegistry()
        registry2 = GlobalDtypeRegistry()
        self.assertEqual(registry0, registry1)
        self.assertEqual(registry0, registry2)

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

    def test_register_dtype_error(self):
        registry = DtypeRegistry(no_defaults=True)
        with self.assertRaises(TypeError):
            registry.add_new(None)  # noqa

    def test_register_dtype_none(self):
        registry = DtypeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry.path2dtypes))
        self.assertEqual(0, len(registry.type2dtypes))

        registry.add_new(type(None))

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        none_dtype = registry.get("builtins.NoneType")
        self.assertEqual(type(None), none_dtype.base)
        self.assertEqual(type(None), registry.get(type(None)).base)

    def test_register_dtype_object(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(object)

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(object, registry.get(object).base)
        self.assertEqual(object, registry.get("builtins.object").base)

    def test_register_dtype_any(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(Any)

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(Any, registry.get(Any).base)
        self.assertEqual(Any, registry.get("typing.Any").base)

    def test_register_dtype_float(self):
        registry = DtypeRegistry(no_defaults=True)
        registry.add_new(float)
        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        self.assertEqual(float, registry.get(float).base)
        self.assertEqual(float, registry.get("builtins.float").base)

    def test_register_dtype_custom(self):
        registry = DtypeRegistry(no_defaults=True)

        @registry.register()
        class _Custom(object):
            pass

        self.assertEqual(1, len(registry.path2dtypes))
        self.assertEqual(1, len(registry.type2dtypes))

        test_path = _Custom.__module__ + FLOW_PATH_SEPARATOR + _Custom.__name__
        self.assertEqual("tester.dtypes.registry.test_registry._Custom", test_path)

        self.assertEqual(_Custom, registry.get(_Custom).base)
        self.assertEqual(_Custom, registry.get(test_path).base)


if __name__ == "__main__":
    main()
