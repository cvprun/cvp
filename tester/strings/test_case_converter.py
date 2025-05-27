# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.strings.case_converter import (
    camel_case,
    dot_case,
    kebab_case,
    pascal_case,
    sentence_case,
    snake_case,
    space_case,
    title_case,
    title_kebab_case,
    upper_case,
)


class CaseConverterTestCase(TestCase):
    def test_camelcase_to_snakecase(self):
        from cvp.strings.case_converter import camelcase_to_snakecase as camel2snake

        self.assertEqual("camel_case_example", camel2snake("CamelCaseExample"))
        self.assertEqual("camel_case_example", camel2snake("CAMELCaseExample"))
        self.assertEqual("camel_case_example", camel2snake("CamelCASEExample"))
        self.assertEqual("camel_case_example", camel2snake("CamelCaseEXAMPLE"))
        self.assertEqual("camel_case_example", camel2snake("Camel_CASE_Example"))
        self.assertEqual("_camel_case_example_", camel2snake("_CamelCaseExample_"))
        self.assertEqual("__camel_case_example__", camel2snake("__CamelCaseExample__"))

    def test_camel_case(self):
        expected = "helloWorld"
        self.assertEqual(expected, camel_case("hello_world"))
        self.assertEqual(expected, camel_case("HelloWorld"))
        self.assertEqual(expected, camel_case("hello-world"))
        self.assertEqual(expected, camel_case("hello world"))
        self.assertEqual(expected, camel_case("HELLO_WORLD"))
        self.assertEqual(expected, camel_case("helloWorld"))

    def test_dot_case(self):
        expected = "hello.world"
        self.assertEqual(expected, dot_case("hello_world"))
        self.assertEqual(expected, dot_case("HelloWorld"))
        self.assertEqual(expected, dot_case("hello-world"))
        self.assertEqual(expected, dot_case("hello world"))
        self.assertEqual(expected, dot_case("HELLO_WORLD"))
        self.assertEqual(expected, dot_case("helloWorld"))

    def test_kebab_case(self):
        expected = "hello-world"
        self.assertEqual(expected, kebab_case("hello_world"))
        self.assertEqual(expected, kebab_case("HelloWorld"))
        self.assertEqual(expected, kebab_case("hello-world"))
        self.assertEqual(expected, kebab_case("hello world"))
        self.assertEqual(expected, kebab_case("HELLO_WORLD"))
        self.assertEqual(expected, kebab_case("helloWorld"))

    def test_pascal_case(self):
        expected = "HelloWorld"
        self.assertEqual(expected, pascal_case("hello_world"))
        self.assertEqual(expected, pascal_case("HelloWorld"))
        self.assertEqual(expected, pascal_case("hello-world"))
        self.assertEqual(expected, pascal_case("hello world"))
        self.assertEqual(expected, pascal_case("HELLO_WORLD"))
        self.assertEqual(expected, pascal_case("helloWorld"))

    def test_sentence_case(self):
        expected = "Hello world"
        self.assertEqual(expected, sentence_case("hello_world"))
        self.assertEqual(expected, sentence_case("HelloWorld"))
        self.assertEqual(expected, sentence_case("hello-world"))
        self.assertEqual(expected, sentence_case("hello world"))
        self.assertEqual(expected, sentence_case("HELLO_WORLD"))
        self.assertEqual(expected, sentence_case("helloWorld"))

    def test_snake_case(self):
        expected = "hello_world"
        self.assertEqual(expected, snake_case("hello_world"))
        self.assertEqual(expected, snake_case("HelloWorld"))
        self.assertEqual(expected, snake_case("hello-world"))
        self.assertEqual(expected, snake_case("hello world"))
        self.assertEqual(expected, snake_case("HELLO_WORLD"))
        self.assertEqual(expected, snake_case("helloWorld"))

    def test_space_case(self):
        expected = "hello world"
        self.assertEqual(expected, space_case("hello_world"))
        self.assertEqual(expected, space_case("HelloWorld"))
        self.assertEqual(expected, space_case("hello-world"))
        self.assertEqual(expected, space_case("hello world"))
        self.assertEqual(expected, space_case("HELLO_WORLD"))
        self.assertEqual(expected, space_case("helloWorld"))

    def test_title_case(self):
        expected = "Hello World"
        self.assertEqual(expected, title_case("hello_world"))
        self.assertEqual(expected, title_case("HelloWorld"))
        self.assertEqual(expected, title_case("hello-world"))
        self.assertEqual(expected, title_case("hello world"))
        self.assertEqual(expected, title_case("HELLO_WORLD"))
        self.assertEqual(expected, title_case("helloWorld"))

    def test_title_kebab_case(self):
        expected = "Hello-World"
        self.assertEqual(expected, title_kebab_case("hello_world"))
        self.assertEqual(expected, title_kebab_case("HelloWorld"))
        self.assertEqual(expected, title_kebab_case("hello-world"))
        self.assertEqual(expected, title_kebab_case("hello world"))
        self.assertEqual(expected, title_kebab_case("HELLO_WORLD"))
        self.assertEqual(expected, title_kebab_case("helloWorld"))

    def test_upper_case(self):
        expected = "HELLO_WORLD"
        self.assertEqual(expected, upper_case("hello_world"))
        self.assertEqual(expected, upper_case("HelloWorld"))
        self.assertEqual(expected, upper_case("hello-world"))
        self.assertEqual(expected, upper_case("hello world"))
        self.assertEqual(expected, upper_case("HELLO_WORLD"))
        self.assertEqual(expected, upper_case("helloWorld"))

    def test_special_word_01(self):
        original = "XML_HTTP_Request"
        self.assertEqual(camel_case(original), "xmlHttpRequest")
        self.assertEqual(dot_case(original), "xml.http.request")
        self.assertEqual(kebab_case(original), "xml-http-request")
        self.assertEqual(pascal_case(original), "XmlHttpRequest")
        self.assertEqual(sentence_case(original), "Xml http request")
        self.assertEqual(snake_case(original), "xml_http_request")
        self.assertEqual(space_case(original), "xml http request")
        self.assertEqual(title_case(original), "Xml Http Request")
        self.assertEqual(title_kebab_case(original), "Xml-Http-Request")
        self.assertEqual(upper_case(original), "XML_HTTP_REQUEST")


if __name__ == "__main__":
    main()
