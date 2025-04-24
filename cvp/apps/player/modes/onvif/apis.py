# -*- coding: utf-8 -*-

import json
from traceback import format_exc
from typing import Any, Dict, Sequence, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.onvif._base import BaseOnvifTab
from cvp.apps.player.modes.onvif._operation import WsdlOperation
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.clipboard import put_clipboard_text
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.push_item_width import item_width
from cvp.imgui.text_colored import text_colored
from cvp.onvif.client import OnvifClient
from cvp.onvif.config import OnvifConfig
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.operation import WsdlOperationProxy


class StepDone(ValueError):
    pass


class ResponseTraceBack(ValueError):
    pass


class OnvifApisTab(BaseOnvifTab):
    __cvp_onvif_tab_name__ = "APIs"

    _response_cache: Dict[Tuple[str, str, str], str]
    _response_error: Dict[Tuple[str, str, str], BaseException]

    def __init__(self, context: Context):
        super().__init__(context)
        self._operation_widget = WsdlOperation()
        self._request_runner = self.context.create_thread_runner(self._on_api_request)
        self._response_cache = dict()
        self._response_error = dict()
        self._show_copied_message = False

    def _on_api_request(self, operation: WsdlOperationProxy):
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
    def success_color(self):
        return self.context.config.appearance.success_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @property
    def warning_color(self):
        return self.context.config.appearance.warning_color

    @property
    def typename_color(self):
        return self.context.config.appearance.typename_color

    def text_success(self, text: str) -> None:
        text_colored(text, self.success_color)

    def text_error(self, text: str) -> None:
        text_colored(text, self.error_color)

    def text_warning(self, text: str) -> None:
        text_colored(text, self.warning_color)

    @override
    def do_process(self, onvif: OnvifConfig) -> None:
        try:
            client = self.do_process_onvif_client(onvif)
            binding = self.do_process_binding_index(onvif, client.wsdls)

            binding_index = binding[0]
            binding_name = binding[1]
            assert isinstance(binding_index, int)
            assert isinstance(binding_name, str)

            apis = self.do_process_apis(client.wsdls, binding_index)
            api_name = self.do_process_select_api(onvif, apis)

            imgui.same_line()
            self.do_process_api_details(apis, api_name)
        except StepDone:
            pass

    def do_process_onvif_client(self, onvif: OnvifConfig) -> OnvifClient:
        client = self.context.onvifs.get_client(onvif.uuid)

        if client is None:
            self.text_warning("ONVIF service instance does not exist")
            self.text_warning("Please create a service instance first")
            raise StepDone("ONVIF service instance does not exist")

        return client

    def do_process_binding_index(
        self,
        onvif: OnvifConfig,
        wsdls: Sequence[WsdlClient],
    ) -> Tuple[int, str]:
        bindings = [wsdl.binding_name for wsdl in wsdls]

        if not bindings:
            self.text_warning("There are no bindings to choose from")
            raise StepDone("ONVIF binding does not exist")

        try:
            binding_index = bindings.index(onvif.select_binding)
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
            onvif.select_binding = bindings[binding_index]

        if not onvif.select_binding:
            self.text_warning("You must select a binding service")
            raise StepDone("ONVIF binding is not selected")

        return binding_index, onvif.select_binding

    def do_process_apis(
        self,
        wsdls: Sequence[WsdlClient],
        binding_index: int,
    ) -> Dict[str, WsdlOperationProxy]:
        apis = wsdls[binding_index].service_operations

        if not apis:
            self.text_warning("There are no APIs to choose from")
            raise StepDone("ONVIF API does not exist")

        return apis

    @staticmethod
    def do_process_select_api(
        item: OnvifConfig,
        apis: Dict[str, WsdlOperationProxy],
        split_x=200,
        child_flags=RESIZE_X | BORDERS,
    ) -> str:
        with begin_child_context("API List", (split_x, 0), child_flags=child_flags):
            if imgui.begin_list_box("##APIList", FIT_SIZE):
                try:
                    for i, key in enumerate(apis.keys()):
                        if imgui.selectable(key, key == item.select_api)[1]:
                            item.select_api = key
                finally:
                    imgui.end_list_box()

        return item.select_api

    def do_process_api_details(
        self,
        apis: Dict[str, WsdlOperationProxy],
        api_name: str,
    ) -> None:
        with begin_child_context("API Details"):
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
                    with begin_child_context("Error Area", child_flags=BORDERS):
                        imgui.text_unformatted(str(error))

                raise StepDone("An error occurred in the operation request") from error

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
                result_label = f"Result Area###{content_key}"
                with begin_child_context(result_label, child_flags=BORDERS):
                    if imgui.is_window_appearing():
                        self._show_copied_message = False
                    imgui.text_unformatted(content)

    def format_response(self, key: Tuple[str, str, str], response: Any) -> str:
        if key in self._response_cache:
            return self._response_cache[key]
        else:
            result = json.dumps(response, indent=2, sort_keys=True)
            self._response_cache[key] = result
            return result
