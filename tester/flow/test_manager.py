# -*- coding: utf-8 -*-

from concurrent.futures.thread import ThreadPoolExecutor
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.flow.manager import FlowManager
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
        var0.initial = 10
        var1.initial = 20
        var0get = self.manager.add_getter_node(graph, var0)
        var1get = self.manager.add_getter_node(graph, var1)
        var0get_value = var0get.find_pin("value")
        var1get_value = var1get.find_pin("value")

        add = self.manager.add_node(graph, "cvp.nodes.defaults.operators.arithmetic.add.AddOperator")
        add_first = add.find_pin("first")
        add_second = add.find_pin("second")
        add_return = add.find_pin("return")

        self.manager.add_wire(graph, var0get, var0get_value, add, add_first)
        self.manager.add_wire(graph, var1get, var1get_value, add, add_second)

        entrypoint = self.manager.add_node(graph, "cvp.nodes.defaults.essential.entrypoint.Entrypoint")
        start = entrypoint.find_pin("start")

        var2 = self.manager.add_variable(graph, "value2", int)
        var2set = self.manager.add_setter_node(graph, var2)
        var2set_prev = var2set.find_pin("prev")
        self.assertIsNotNone(var2set.find_pin("next"))
        var2set_value = var2set.find_pin("value")

        self.manager.add_wire(graph, entrypoint, start, var2set, var2set_prev)
        self.manager.add_wire(graph, add, add_return, var2set, var2set_value)

        with ThreadPoolExecutor(max_workers=1) as executor:
            runner = self.manager.add_runner(graph, entrypoint, executor)

        self.assertTrue(runner.future.done())
        self.assertEqual(30, var2.get())

        result = runner.result()
        self.assertEqual(5, len(result))
        self.assertEqual(entrypoint.uuid, result[0].node_uuid)
        self.assertEqual(var0get.uuid, result[1].node_uuid)
        self.assertEqual(var1get.uuid, result[2].node_uuid)
        self.assertEqual(add.uuid, result[3].node_uuid)
        self.assertEqual(var2set.uuid, result[4].node_uuid)


if __name__ == "__main__":
    main()
