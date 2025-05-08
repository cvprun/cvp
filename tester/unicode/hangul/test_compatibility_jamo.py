# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.unicode.hangul.compatibility_jamo import (
    MODERN_CHOSEONG,
    MODERN_JUNGSEONG,
    is_modern_hangul_compatibility_choseong_unicode,
    is_modern_hangul_compatibility_jungseong_unicode,
)


class CompatibilityJamoTestCase(TestCase):
    def test_modern_choseong(self):
        choseong = MODERN_CHOSEONG
        res = [is_modern_hangul_compatibility_choseong_unicode(x) for x in choseong]
        self.assertTrue(all(res))

    def test_modern_jungseong(self):
        jungseong = MODERN_JUNGSEONG
        res = [is_modern_hangul_compatibility_jungseong_unicode(x) for x in jungseong]
        self.assertTrue(all(res))


if __name__ == "__main__":
    main()
