# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.dtypes.registry.globals import GlobalDtypeRegistry, global_dtype_registry


class GlobalsTestCase(TestCase):
    def test_singleton(self):
        registry0 = global_dtype_registry()
        registry1 = GlobalDtypeRegistry()
        registry2 = GlobalDtypeRegistry()
        self.assertEqual(registry0, registry1)
        self.assertEqual(registry0, registry2)


if __name__ == "__main__":
    main()
