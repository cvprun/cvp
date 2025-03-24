# -*- coding: utf-8 -*-

import json
from traceback import format_exc
from typing import Any, Dict, Sequence, Tuple

from imgui_bundle import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.imgui.begin_child import begin_child, end_child
from cvp.imgui.button import button
from cvp.imgui.clipboard import put_clipboard_text
from cvp.imgui.flags.child import BORDERS
from cvp.imgui.push_item_width import item_width
from cvp.imgui.slider_float import slider_float
from cvp.imgui.text_colored import text_colored
from cvp.onvif.client import OnvifClient
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX
from cvp.widgets.tab import TabItem
from cvp.widgets.wsdl_operation import WsdlOperationWidget
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.operation import WsdlOperationProxy


class StepDone(ValueError):
    pass


class ResponseTraceBack(ValueError):
    pass


class OnvifApisTab(TabItem[OnvifConfig]):
    _response_cache: Dict[Tuple[str, str, str], str]
    _response_error: Dict[Tuple[str, str, str], BaseException]

    def __init__(self, context: RendererContext):
        super().__init__(context, "APIs")
        self._operation_widget = WsdlOperationWidget()
        self._request_runner = self.context.pm.create_thread_runner(self.on_api_request)
        self._response_cache = dict()
        self._response_error = dict()
        self._show_copied_message = False

    def on_api_request(self, operation: WsdlOperationProxy):
        key = operation.cache_args
        try:
            response = operation.call_with_arguments()
            result = json.dumps(response, indent=2, sort_keys=True)
            self._response_cache[key] = result
            self._response_error.pop(key, None)
        except BaseException as e:
            error = ResponseTraceBack(format_exc())
            error.__cause__ = e
            self._response_cache.pop(key, None)
            self._response_error[key] = error
            raise

    @property
    def api_select_width(self) -> float:
        return self.context.config.onvif_manager.api_select_width

    @api_select_width.setter
    def api_select_width(self, value: float) -> None:
        self.context.config.onvif_manager.api_select_width = value

    @property
    def min_api_select_width(self) -> float:
        return self.context.config.onvif_manager.min_api_select_width

    @min_api_select_width.setter
    def min_api_select_width(self, value: float) -> None:
        self.context.config.onvif_manager.min_api_select_width = value

    @property
    def max_api_select_width(self) -> float:
        return self.context.config.onvif_manager.max_api_select_width

    @max_api_select_width.setter
    def max_api_select_width(self, value: float) -> None:
        self.context.config.onvif_manager.max_api_select_width = value

    @property
    def success_color(self):
        return self.context.config.onvif_manager.success_color

    @property
    def error_color(self):
        return self.context.config.onvif_manager.error_color

    @property
    def warning_color(self):
        return self.context.config.onvif_manager.warning_color

    @property
    def typename_color(self):
        return self.context.config.onvif_manager.typename_color

    def text_success(self, text: str) -> None:
        text_colored(text, self.success_color)

    def text_error(self, text: str) -> None:
        text_colored(text, self.error_color)

    def text_warning(self, text: str) -> None:
        text_colored(text, self.warning_color)

    def slider_api_select_width(self) -> None:
        result = slider_float(
            "## API List Width",
            self.api_select_width,
            self.min_api_select_width,
            self.max_api_select_width,
            "List width (%.3f)",
        )
        if result:
            self.api_select_width = result.value

    @override
    def on_item(self, item: OnvifConfig) -> None:
        try:
            onvif = self.process_onvif_client(item)
            binding_index, binding_name = self.process_binding_index(item, onvif.wsdls)
            apis = self.process_apis(onvif.wsdls, binding_index)
            api_name = self.process_select_api(item, apis)
            imgui.same_line()
            self.process_api_details(apis, api_name)
        except StepDone:
            pass

    def process_onvif_client(self, item: OnvifConfig) -> OnvifClient:
        onvif = self.context.om.get(item.uuid)

        if onvif is None:
            self.text_warning("ONVIF service instance does not exist")
            self.text_warning("Please create a service instance first")
            raise StepDone("ONVIF service instance does not exist")

        return onvif

    def process_binding_index(
        self,
        item: OnvifConfig,
        wsdls: Sequence[WsdlClient],
    ) -> Tuple[int, str]:
        bindings = [wsdl.binding_name for wsdl in wsdls]

        if not bindings:
            self.text_warning("There are no bindings to choose from")
            raise StepDone("ONVIF binding does not exist")

        try:
            binding_index = bindings.index(item.select_binding)
        except ValueError:
            binding_index = NOT_FOUND_INDEX

        with item_width(-1):
            binding_result = imgui.combo(
                "## Binding",
                binding_index,
                bindings,
            )

        binding_changed = binding_result[0]
        binding_index = binding_result[1]
        assert isinstance(binding_changed, bool)
        assert isinstance(binding_index, int)

        if binding_changed and 0 <= binding_index < len(bindings):
            item.select_binding = bindings[binding_index]

        if not item.select_binding:
            self.text_warning("You must select a binding service")
            raise StepDone("ONVIF binding is not selected")

        return binding_index, item.select_binding

    def process_apis(
        self,
        wsdls: Sequence[WsdlClient],
        binding_index: int,
    ) -> Dict[str, WsdlOperationProxy]:
        apis = wsdls[binding_index].service_operations

        if not apis:
            self.text_warning("There are no APIs to choose from")
            raise StepDone("ONVIF API does not exist")

        return apis

    def process_select_api(
        self,
        item: OnvifConfig,
        apis: Dict[str, WsdlOperationProxy],
    ) -> str:
        if begin_child("API List", width=self.api_select_width):
            try:
                with item_width(-1):
                    self.slider_api_select_width()
                    if imgui.begin_list_box("## API List Box", (-1, -1)):
                        try:
                            for i, key in enumerate(apis.keys()):
                                if imgui.selectable(key, key == item.select_api)[1]:
                                    item.select_api = key
                        finally:
                            imgui.end_list_box()
            finally:
                end_child()

        return item.select_api

    def process_api_details(
        self,
        apis: Dict[str, WsdlOperationProxy],
        api_name: str,
    ) -> None:
        if begin_child("API Details", child_flags=BORDERS):
            try:
                if api_name not in apis:
                    self.text_warning("You must select an API")
                    raise StepDone("ONVIF API is not selected")

                imgui.text(api_name)
                imgui.separator()

                imgui.text("Parameters:")
                operation = apis[api_name]

                mishandling = self._operation_widget.process_operation(operation)
                disable_request = (
                    mishandling >= 1
                    or not operation.arguments.requestable
                    or bool(self._request_runner)
                )

                if button("Request", disabled=disable_request):
                    self._request_runner(operation)

                imgui.same_line()

                has_latest = operation.has_latest()
                has_cache = operation.has_cache()
                disable_remove_cache = not has_latest and not has_cache

                if button("Remove Cache", disabled=disable_remove_cache):
                    if has_latest:
                        operation.clear_latest()
                        has_latest = False
                    if has_cache:
                        operation.remove_cache()
                        has_cache = False

                error = self._response_error.get(operation.cache_args)
                if error is not None:
                    assert isinstance(error, ResponseTraceBack)
                    assert isinstance(error.__cause__, BaseException)
                    base_error = error.__cause__

                    imgui.text("Response error:")

                    if self.context.debug and self.context.verbose >= 1:
                        imgui.same_line()
                        if imgui.small_button("Copy"):
                            put_clipboard_text(str(error))

                    for line in str(base_error).splitlines():
                        self.text_error(line)

                    if self.context.debug and self.context.verbose >= 1:
                        if begin_child("Error Area", BORDERS):
                            try:
                                imgui.text_unformatted(str(error))
                            finally:
                                end_child()

                    raise StepDone(
                        "An error occurred in the operation request"
                    ) from error

                if has_latest or has_cache:
                    imgui.text("Response result:")

                    if has_latest:
                        response = operation.latest
                    elif has_cache:
                        response = operation.read_cache()
                        if not has_latest:
                            operation.latest = response
                    else:
                        assert False, "Inaccessible section"

                    content = self.format_response(operation.cache_args, response)

                    imgui.same_line()
                    if imgui.small_button("Copy"):
                        self._show_copied_message = True
                        put_clipboard_text(content)

                    if self._show_copied_message:
                        imgui.same_line()
                        self.text_success("copied")

                    content_key = ".".join(operation.cache_args)
                    if begin_child(f"Result Area###{content_key}", BORDERS):
                        try:
                            if imgui.is_window_appearing():
                                self._show_copied_message = False
                            imgui.text_unformatted(content)
                        finally:
                            end_child()
            finally:
                end_child()

    def format_response(self, key: Tuple[str, str, str], response: Any) -> str:
        if key in self._response_cache:
            return self._response_cache[key]
        else:
            result = json.dumps(response, indent=2, sort_keys=True)
            self._response_cache[key] = result
            return result
