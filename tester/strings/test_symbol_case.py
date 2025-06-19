# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.strings.symbol_case import python_symbol_case as psc


class SymbolCaseTestCase(TestCase):
    def test_python_symbol_case(self):
        self.assertEqual("api_users_get_profile", psc("/api/users/get-profile"))
        self.assertEqual("api_users_id_update", psc("/api/users/{id}/update"))
        self.assertEqual("v1_products_search", psc("/v1/products/search"))
        self.assertEqual("admin_monthly_sales", psc("/admin/monthly-sales"))
        self.assertEqual("auth_login", psc("/auth/login"))
        self.assertEqual("auth_logout", psc("/auth/logout"))
        self.assertEqual("api_v2_users_123_orders", psc("/api/v2/users/123/orders"))
        self.assertEqual("files_upload_image", psc("/files/upload-image"))
        self.assertEqual("settings_user_preferences", psc("/settings/user-preferences"))
        self.assertEqual("_", psc("/"))
        self.assertEqual("_", psc(""))
        self.assertEqual("def_class_import", psc("/def/class/import"))
        self.assertEqual("def_", psc("/def"))  # python keyword
        self.assertEqual("case", psc("/case"))  # python soft-keyword
        self.assertEqual("_2fa_e", psc("/2fa/e"))  # Case starting with a number
        self.assertEqual("api_me", psc("/api/@me"))  # Including special characters
        self.assertEqual("u_profile", psc("__/u___profile"))  # Consecutive underscores
        self.assertEqual("u_profile", psc("//u//profile"))  # Consecutive slashes


if __name__ == "__main__":
    main()
