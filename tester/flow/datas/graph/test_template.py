# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.datas.graph import Graph
from tester.flow.datas.templates.samples.simple_1on1 import GRAPH_TEMPLATE


class TemplateTestCase(TestCase):
    def test_default(self):
        graph = Graph.from_template(GRAPH_TEMPLATE, reissue=False)
        template = graph.as_template(reissue=False)
        self.assertEqual(GRAPH_TEMPLATE, template)


if __name__ == "__main__":
    main()
