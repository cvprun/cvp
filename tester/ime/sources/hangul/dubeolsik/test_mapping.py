# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.sources.hangul.dubeolsik.mapping import (
    create_dubeolsik_hangul_consonants_mapping,
    create_dubeolsik_hangul_mapping,
    create_dubeolsik_hangul_vowels_mapping,
)
from cvp.unicode.hangul.checker import is_hangul_unicode
from cvp.unicode.hangul.compatibility_jamo import (
    is_modern_hangul_compatibility_choseong_unicode,
    is_modern_hangul_compatibility_jungseong_unicode,
)


class MappingTestCase(TestCase):
    def test_total(self):
        mapping = create_dubeolsik_hangul_mapping()
        self.assertTrue(all([k.isalpha() for k in mapping.keys()]))
        self.assertTrue(all([is_hangul_unicode(k) for k in mapping.values()]))

    def test_consonants(self):
        mapping = create_dubeolsik_hangul_consonants_mapping()
        self.assertTrue(all([k.isalpha() for k in mapping.keys()]))

        is_hangul_choseong = is_modern_hangul_compatibility_choseong_unicode
        self.assertTrue(all([is_hangul_choseong(k) for k in mapping.values()]))

    def test_vowels(self):
        mapping = create_dubeolsik_hangul_vowels_mapping()
        self.assertTrue(all([k.isalpha() for k in mapping.keys()]))

        is_hangul_jungseong = is_modern_hangul_compatibility_jungseong_unicode
        self.assertTrue(all([is_hangul_jungseong(k) for k in mapping.values()]))


if __name__ == "__main__":
    main()
