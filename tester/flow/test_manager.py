# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.graph import FlowGraph
from cvp.flow.manager import FlowManager
from cvp.flow.node import FlowNode
from cvp.resources.home import HomeDir


class ManagerTestCase(TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.home = HomeDir(self.tmpdir.name)
        self.manager = FlowManager(self.home)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add(self):
        graph = self.manager.create_graph()
        var0 = self.manager.add_variable(graph, "value0", int)
        var1 = self.manager.add_variable(graph, "value1", int)
        var2 = self.manager.add_variable(graph, "value2", int)

        var0.set(10)
        var1.set(20)

        var0get = self.manager.add_getter_node(graph, var0)
        var1get = self.manager.add_getter_node(graph, var1)
        var2set = self.manager.add_setter_node(graph, var2)

        entrypoint = self.manager.add_node(graph, "cvp.essential.entrypoint")
        add = self.manager.add_node(graph, "cvp.operators.arithmetic.add")

        start = entrypoint.find_pin("start")
        add_prev = add.find_pin("prev")

        first = add.find_pin("first")
        second = add.find_pin("second")

        # node0.
        # node0.find_pin("start")
        # node0.exec_outputs[""]

        # node1 = self.manager.add_node(graph, "cvp.entrypoint")
        # var0 = self.manager.add_variable(graph, "value1", int)


if __name__ == "__main__":
    main()
