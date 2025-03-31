# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.keyring.keyring import Keyring


class KeyringTestCase(TestCase):
    def test_default(self):
        keyring = Keyring()


if __name__ == "__main__":
    main()
