# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
from unittest import TestCase, main

from zeep.xsd import Element

from cvp.config.sections.onvif import OnvifConfig
from cvp.keyring.root import RootKeyring
from cvp.onvif.client import OnvifClient
from cvp.resources.home import HomeDir
from cvp.wsdl.operation import WsdlOperationProxy


class ClientTestCase(TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.home = HomeDir(self.tmpdir.name)
        self.onvif_config = OnvifConfig()
        self.keyring = RootKeyring()
        self.client = OnvifClient(self.onvif_config, self.home, self.keyring)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_devicemgmt_get_services(self):
        devicemgmt_operation = self.client.devicemgmt.service_operations
        get_services0 = devicemgmt_operation["GetServices"]
        get_services1 = self.client.devicemgmt.GetServices
        self.assertIsInstance(get_services0, WsdlOperationProxy)
        self.assertIsInstance(get_services1, WsdlOperationProxy)
        self.assertEqual(get_services0, get_services1)
        self.assertEqual("GetServices", get_services0.name)
        self.assertEqual("GetServices", get_services1.name)

        self.assertEqual(1, len(get_services0.input_elements))
        input_element0 = get_services0.input_elements[0]
        self.assertIsInstance(input_element0, tuple)
        self.assertEqual(2, len(input_element0))

        name = input_element0[0]
        element = input_element0[1]
        self.assertEqual("IncludeCapability", name)
        self.assertEqual("IncludeCapability", element.name)

    def test_media_get_stream_uri(self):
        media_operation = self.client.media.service_operations
        get_stream_uri0 = media_operation["GetStreamUri"]
        get_stream_uri1 = self.client.media.GetStreamUri
        self.assertIsInstance(get_stream_uri0, WsdlOperationProxy)
        self.assertIsInstance(get_stream_uri1, WsdlOperationProxy)
        self.assertEqual(get_stream_uri0, get_stream_uri1)
        self.assertEqual("GetStreamUri", get_stream_uri0.name)
        self.assertEqual("GetStreamUri", get_stream_uri1.name)

        self.assertEqual(2, len(get_stream_uri0.input_elements))

        input_element0 = get_stream_uri0.input_elements[0]
        self.assertIsInstance(input_element0, tuple)
        self.assertEqual(2, len(input_element0))
        self.assertIsInstance(input_element0[0], str)
        self.assertIsInstance(input_element0[1], Element)

        input_element1 = get_stream_uri0.input_elements[1]
        self.assertIsInstance(input_element1, tuple)
        self.assertEqual(2, len(input_element1))
        self.assertIsInstance(input_element1[0], str)
        self.assertIsInstance(input_element1[1], Element)

        name0 = input_element0[0]
        element0 = input_element0[1]
        self.assertEqual("StreamSetup", name0)
        self.assertEqual("StreamSetup", element0.name)

        name1 = input_element1[0]
        element1 = input_element1[1]
        self.assertEqual("ProfileToken", name1)
        self.assertEqual("ProfileToken", element1.name)

        # b = element0.type.accepted_types[0]()
        # a = element0.type.elements[0][1].type
        # c = element0.type.elements[0]
        # d = self.client.media.client.get_type(element0.type.elements[0][1].type.qname)
        # f = self.client.media.client.type_factory("http://www.onvif.org/ver10/schema")


if __name__ == "__main__":
    main()
