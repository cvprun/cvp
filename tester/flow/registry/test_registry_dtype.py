# -*- coding: utf-8 -*-

from typing import Any
from unittest import TestCase, main

from cvp.flow.registry.registry import FlowRegistry
from cvp.variables import FLOW_PATH_SEPARATOR


class RegistryDtypeTestCase(TestCase):
    def test_register_dtype_builtins(self):
        registry = FlowRegistry(no_builtins=True)
        self.assertEqual(0, len(registry.dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        registry.register_builtin_dtypes()
        self.assertNotEqual(0, len(registry.dtypes))
        self.assertNotEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

    def test_register_dtype_none(self):
        registry = FlowRegistry(no_builtins=True)

        with self.assertRaises(TypeError):
            registry.add_new_type(None)  # noqa

        self.assertEqual(0, len(registry.dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        registry.add_new_type(type(None))

        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        self.assertEqual(type(None), registry.get_dtype_with_type(type(None)).base)
        self.assertEqual(type(None), registry.get_dtype("builtins.NoneType").base)

    def test_register_dtype_object(self):
        registry = FlowRegistry(no_builtins=True)
        registry.add_new_type(object)

        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        self.assertEqual(object, registry.get_dtype_with_type(object).base)
        self.assertEqual(object, registry.get_dtype("builtins.object").base)

    def test_register_dtype_any(self):
        registry = FlowRegistry(no_builtins=True)
        registry.add_new_type(Any)

        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        self.assertEqual(Any, registry.get_dtype_with_type(Any).base)
        self.assertEqual(Any, registry.get_dtype("typing.Any").base)

    def test_register_dtype_float(self):
        registry = FlowRegistry(no_builtins=True)
        registry.add_new_type(float)
        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        self.assertEqual(float, registry.get_dtype_with_type(float).base)
        self.assertEqual(float, registry.get_dtype("builtins.float").base)

    def test_register_dtype_custom(self):
        registry = FlowRegistry(no_builtins=True)

        @registry.register_dtype()
        class _Custom(object):
            pass

        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        test_path = _Custom.__module__ + FLOW_PATH_SEPARATOR + _Custom.__name__
        self.assertEqual("tester.flow.registry.test_registry_dtype._Custom", test_path)

        self.assertEqual(_Custom, registry.get_dtype_with_type(_Custom).base)
        self.assertEqual(_Custom, registry.get_dtype(test_path).base)


if __name__ == "__main__":
    main()
