# -*- coding: utf-8 -*-

from unittest import TestCase, main

from faker import Faker

from cvp.faker.providers import create_providers, get_language_locale_codes


class ProvidersTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.seed_instance()
        self.providers = create_providers(self.faker)
        self.locales = get_language_locale_codes()

    def test_default(self):
        expect_providers = {
            "Address",
            "Automotive",
            "Bank",
            "Barcode",
            "Color",
            "Company",
            "Credit card",
            "Currency",
            "Date time",
            "Doi",
            "Emoji",
            "File",
            "Geo",
            "Internet",
            "Isbn",
            "Job",
            "Lorem",
            "Misc",
            "Passport",
            "Person",
            "Phone number",
            "Profile",
            "Python",
            "Sbn",
            "Ssn",
            "User agent",
        }
        actual_providers = set(self.providers.keys())
        self.assertSetEqual(expect_providers, actual_providers)


if __name__ == "__main__":
    main()
