# -*- coding: utf-8 -*-

import typing

if hasattr(typing, "_AnnotatedAlias"):
    AnnotatedAlias = typing._AnnotatedAlias  # noqa
else:
    import typing_extensions

    if hasattr(typing_extensions, "_AnnotatedAlias"):
        AnnotatedAlias = typing_extensions._AnnotatedAlias  # noqa
    else:
        raise RuntimeError("Cannot find _AnnotatedAlias in typing or typing_extensions")


# def _strip_annotations(t):
#     """Strip the annotations from a given type."""
#     if isinstance(t, _AnnotatedAlias):
#         return _strip_annotations(t.__origin__)
#     if hasattr(t, "__origin__") and t.__origin__ in (Required, NotRequired):
#         return _strip_annotations(t.__args__[0])
#     if isinstance(t, _GenericAlias):
#         stripped_args = tuple(_strip_annotations(a) for a in t.__args__)
#         if stripped_args == t.__args__:
#             return t
#         return t.copy_with(stripped_args)
#     if isinstance(t, GenericAlias):
#         stripped_args = tuple(_strip_annotations(a) for a in t.__args__)
#         if stripped_args == t.__args__:
#             return t
#         return GenericAlias(t.__origin__, stripped_args)
#     if isinstance(t, types.UnionType):
#         stripped_args = tuple(_strip_annotations(a) for a in t.__args__)
#         if stripped_args == t.__args__:
#             return t
#         return functools.reduce(operator.or_, stripped_args)
#
#     return t
