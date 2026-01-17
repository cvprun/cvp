# -*- coding: utf-8 -*-

import gc
from unittest import TestCase, main

from cvp.nodes.registry.ref import NodeRegistryRef
from cvp.nodes.registry.registry import NodeRegistry


class NodeRegistryRefTestCase(TestCase):
    def test_get_global(self):
        global_registry = NodeRegistryRef.get_global()
        self.assertIsInstance(global_registry, NodeRegistry)

    def test_init_and_get_ref(self):
        registry = NodeRegistry(no_defaults=True)
        ref = NodeRegistryRef(registry)

        result = ref.get_ref()
        self.assertIsNotNone(result)
        self.assertIs(result, registry)

    def test_get_ref_returns_none_when_dereferenced(self):
        registry = NodeRegistry(no_defaults=True)
        ref = NodeRegistryRef(registry)

        self.assertIsNotNone(ref.get_ref())

        del registry
        gc.collect()

        self.assertIsNone(ref.get_ref())

    def test_get_force_returns_ref_when_alive(self):
        # Note: Empty registry (no_defaults=True) is falsy, which causes
        # get_force() to return global registry. Use registry with defaults.
        registry = NodeRegistry(no_defaults=False)
        ref = NodeRegistryRef(registry)

        result = ref.get_force()
        self.assertIs(result, registry)

    def test_get_force_returns_registry_when_dereferenced(self):
        registry = NodeRegistry(no_defaults=True)
        ref = NodeRegistryRef(registry)

        del registry
        gc.collect()

        result = ref.get_force()
        self.assertIsInstance(result, NodeRegistry)

    def test_call_returns_same_as_get_force(self):
        # Use registry with defaults so it's truthy
        registry = NodeRegistry(no_defaults=False)
        ref = NodeRegistryRef(registry)

        self.assertIs(ref(), ref.get_force())

    def test_call_returns_registry_when_dereferenced(self):
        registry = NodeRegistry(no_defaults=True)
        ref = NodeRegistryRef(registry)

        del registry
        gc.collect()

        self.assertIsInstance(ref(), NodeRegistry)


if __name__ == "__main__":
    main()
