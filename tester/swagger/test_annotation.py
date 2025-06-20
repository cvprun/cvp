# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.swagger.annotation import openapi_enum_to_python_literal


class AnnotationTestCase(TestCase):
    def test_openapi_enum_to_python_literal(self):
        expect1 = 'typing.Literal["a"]'
        actual1 = openapi_enum_to_python_literal(["a"])
        self.assertEqual(expect1, actual1)

        expect2 = 'typing.Literal["a", "b"]'
        actual2 = openapi_enum_to_python_literal(["a", "b"])
        self.assertEqual(expect2, actual2)


if __name__ == "__main__":
    main()
