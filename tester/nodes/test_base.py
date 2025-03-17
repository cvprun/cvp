# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.nodes.base import NodeBase
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import EmptyNextPin
from cvp.types.override import override


class _TestNode1(NodeBase):
    @override
    def run(self, record: NodeRecord) -> Pin:
        return self.nonext()

    @override
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError


class _TestNode2(NodeBase):
    @override
    def run(self, record: NodeRecord) -> Pin:
        return self.nonext()

    @override
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError


class BaseTestCase(TestCase):
    def test_default(self):
        self.assertIsNone(_TestNode1.get_singleton_instance())
        self.assertIsNone(_TestNode2.get_singleton_instance())

        tn1 = _TestNode1()
        tn2 = _TestNode2()

        self.assertIsNotNone(_TestNode1.get_singleton_instance())
        self.assertIsNotNone(_TestNode2.get_singleton_instance())

        self.assertIsInstance(tn1.run(NodeRecord.empty()), EmptyNextPin)
        self.assertIsInstance(tn2.run(NodeRecord.empty()), EmptyNextPin)

        self.assertIs(_TestNode1.get_singleton_instance(), tn1)
        self.assertIs(_TestNode2.get_singleton_instance(), tn2)

        self.assertIs(_TestNode1.get_singleton_instance(), _TestNode1())
        self.assertIs(_TestNode2.get_singleton_instance(), _TestNode2())

        self.assertIs(_TestNode1(), _TestNode1())
        self.assertIs(_TestNode2(), _TestNode2())

        self.assertIsNot(_TestNode1(), _TestNode2())


if __name__ == "__main__":
    main()
