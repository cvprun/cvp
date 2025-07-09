# -*- coding: utf-8 -*-

from inspect import isclass
from unittest import TestCase, main

from cvp.types.annotations import AnnotatedAlias


class AnnotationsTestCase(TestCase):
    def test_annotated_alias(self):
        self.assertIsInstance(AnnotatedAlias, type)
        self.assertTrue(isclass(AnnotatedAlias))


if __name__ == "__main__":
    main()
