# -*- coding: utf-8 -*-

from typing import Any, List, Tuple

from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element

from cvp.inspect.argument import Argument, ArgumentMapper
from cvp.logging.loggers import wsdl_logger as logger
from cvp.resources.formats.json import JsonFormatPath
from cvp.types.override import override
from cvp.wsdl.annotation import ElementAnnotation
from cvp.wsdl.schema import XsdSchema
from cvp.wsdl.serialize import serialize_object


class WsdlOperationProxy(OperationProxy):
    def __init__(
        self,
        jsons: JsonFormatPath,
        uuid: str,
        binding_name: str,
        operation_name: str,
        service_proxy: ServiceProxy,
        operation: Operation,
        schema: XsdSchema,
    ):
        super().__init__(service_proxy, operation_name)
        self._uuid = uuid
        self._jsons = jsons
        self._binding_name = binding_name
        self._operation = operation

        input_elements = self._operation.input.body.type.elements
        self._arguments = self._create_arguments(input_elements, schema)
        self._latest = None

    @staticmethod
    def _create_arguments(input_elements: List[Tuple[str, Element]], schema: XsdSchema):
        result = ArgumentMapper()
        for name, element in input_elements:
            annotation = ElementAnnotation(element, schema)
            result[name] = Argument.from_details(name, annotation=annotation)
        return result

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        return self._operation.input.body.type.elements

    @property
    def arguments(self):
        return self._arguments

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def binding_name(self) -> str:
        return self._binding_name

    @property
    def name(self) -> str:
        assert isinstance(self._op_name, str)
        return self._op_name

    @property
    def latest(self) -> Any:
        return self._latest

    @latest.setter
    def latest(self, value: Any) -> None:
        self._latest = value

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self.uuid, self.binding_name, self.name

    def has_latest(self) -> bool:
        return self._latest is not None

    def has_cache(self) -> bool:
        return self._jsons.has_object(*self.cache_args)

    def read_cache(self) -> Any:
        return self._jsons.read_object(*self.cache_args)

    def write_cache(self, o: Any) -> int:
        return self._jsons.write_object(o, *self.cache_args)

    def remove_cache(self) -> None:
        self._jsons.remove_object(*self.cache_args)

    def clear_latest(self) -> None:
        self._latest = None

    @override
    def __call__(self, *args, **kwargs):
        prefix = f"Call {self.name}(args={args}, kwargs={kwargs})"

        if self._latest is not None:
            logger.info(f"{prefix} memory cache")
        elif self.has_cache():
            logger.info(f"{prefix} file cache")
            self._latest = self.read_cache()
        else:
            logger.info(f"{prefix} operation")
            response = super().__call__(*args, **kwargs)
            self._latest = serialize_object(response)
            self.write_cache(self._latest)

        return self._latest

    def call_with_arguments(self):
        return self.__call__(**self._arguments.kwargs())
