# -*- coding: utf-8 -*-

from unittest import TestCase, main, skipIf

from cvp.mediamtx.client import MediamtxApi, PathConfList
from tester import MEDIAMTX_SERVER


@skipIf(not MEDIAMTX_SERVER, "MEDIAMTX_SERVER is not alive")
class ClientTestCase(TestCase):
    def setUp(self):
        self.client = MediamtxApi(MEDIAMTX_SERVER.address)

    def test_configPathsList(self):
        result = self.client.configPathsList()
        self.assertIsInstance(result, PathConfList)


if __name__ == "__main__":
    main()
