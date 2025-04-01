# -*- coding: utf-8 -*-

from unittest import TestCase, main
from uuid import uuid4

from cvp.keyring.root import RootKeyring


class RootTestCase(TestCase):
    def test_singleton(self):
        keyring1 = RootKeyring()
        keyring2 = RootKeyring()
        self.assertIs(keyring1, keyring2)

    def test_default(self):
        test_service = type(self).__name__
        test_key = str(uuid4())

        keyring = RootKeyring()
        service_key = keyring.gen_cache_key(test_service, test_key)
        self.assertTrue(service_key not in keyring)

        keyring[service_key] = "ABCD1234"
        self.assertTrue(service_key in keyring)
        self.assertEqual("ABCD1234", keyring[service_key])
        keyring.clear_cache()
        del keyring[service_key]

        self.assertTrue(service_key not in keyring)
        self.assertIsNone(keyring[service_key])


if __name__ == "__main__":
    main()
