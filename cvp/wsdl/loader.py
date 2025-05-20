# -*- coding: utf-8 -*-

from cvp.logging.loggers import wsdl_logger as logger
from cvp.wsdl.declaration import WsdlDeclaration


def load_wsdl_declarations(*args: WsdlDeclaration) -> int:
    wsdls = list(args)
    wsdls_size = len(wsdls)
    success_count = 0

    for i, decl in enumerate(wsdls):
        prefix = f"[{i + 1}/{wsdls_size}]"
        binding = decl.namespace_binding
        try:
            logger.debug(f"{prefix} Load wsdl declaration: {binding}")
            decl.load_document()

            logger.debug(f"{prefix} Load schema declaration: {binding}")
            decl.load_schema()
        except BaseException as e:
            logger.error(e)
        else:
            success_count += 1

    return success_count
