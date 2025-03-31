# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main, skipIf

from cvp.keyring.details import (
    KEYRING_PLAIN_TEXT,
    KEYRING_SAGECIPHER,
    delete_password,
    get_keyring,
    get_password,
    is_file_backed,
    is_valid_sagecipher,
    keyring_context,
    list_keyring_names,
    load_keyring,
    set_file_path,
    set_keyring,
    set_password,
)


class DetailsTestCase(TestCase):
    def test_list_keyring_names(self):
        actual_backends = set(list_keyring_names())
        self.assertIn(KEYRING_PLAIN_TEXT, actual_backends)
        self.assertIn(KEYRING_SAGECIPHER, actual_backends)

    def test_keyring_context(self):
        prev_backend = get_keyring()
        with keyring_context():
            keyring = load_keyring(KEYRING_PLAIN_TEXT)
            set_keyring(keyring)
            self.assertEqual(keyring, get_keyring())
        self.assertEqual(prev_backend, get_keyring())

    def _run_backend_unit_test(self, backend_name: str) -> None:
        with TemporaryDirectory() as tmp:
            self.assertTrue(os.path.isdir(tmp))

            with keyring_context(backend_name) as backend:
                keyring_filepath = os.path.join(tmp, "keyring.cfg")
                self.assertFalse(os.path.exists(keyring_filepath))

                self.assertTrue(is_file_backed(backend))
                set_file_path(backend, keyring_filepath)
                self.assertEqual(type(backend).file_path, keyring_filepath)

                service = "test"
                username = "cvp"
                password = "pass"

                self.assertIsNone(get_password(service, username))
                set_password(service, username, password)
                self.assertTrue(os.path.isfile(keyring_filepath))

                self.assertEqual(password, get_password(service, username))
                delete_password(service, username)
                self.assertIsNone(get_password(service, username))

    def test_plain_text(self):
        self._run_backend_unit_test(KEYRING_PLAIN_TEXT)

    @skipIf(not is_valid_sagecipher(), "sagecipher is not available")
    def test_sagecipher(self):
        self._run_backend_unit_test(KEYRING_SAGECIPHER)


if __name__ == "__main__":
    main()
