# -*- coding: utf-8 -*-

from collections import OrderedDict
from inspect import Signature, signature
from typing import Any, Callable, List, NamedTuple, NewType, Sequence

from faker import Faker
from faker.providers import BaseProvider

from cvp.inspect.argument import ArgumentMapper
from cvp.inspect.bind import BindCallable, force_bind
from cvp.variables import MODULE_PATH_SEPARATOR

ProviderName = NewType("ProviderName", str)
ProviderApi = NewType("ProviderApi", str)


class ApiInfo(NamedTuple):
    name: ProviderApi
    path: str
    function: Callable[..., Any]
    signature: Signature
    arguments: ArgumentMapper

    def bind(self) -> BindCallable:
        return force_bind(self.function, **self.arguments.as_dict())


class ProviderInfo(NamedTuple):
    name: ProviderName
    provider: BaseProvider
    apis: OrderedDict[ProviderApi, ApiInfo]


def create_providers(faker: Faker) -> OrderedDict[ProviderName, ProviderInfo]:
    result = OrderedDict()
    base_provider_key = set(dir(BaseProvider))
    providers = list(faker.providers)
    providers.sort(key=lambda p: type(p).__module__)
    for provider in providers:
        assert isinstance(provider, BaseProvider)
        module = type(provider).__module__
        name = module.removeprefix("faker.providers.")
        name = name.split(".")[0].capitalize()
        name = name.replace("_", " ")
        provider_name = ProviderName(name)
        api_names1 = set(dir(type(provider))) - base_provider_key
        api_names2 = filter(lambda x: callable(getattr(faker, x, None)), api_names1)
        api_names = list(map(lambda x: ProviderApi(x), api_names2))
        api_names.sort()

        apis = OrderedDict()
        for api_name in api_names:
            api_callable = getattr(faker, api_name, None)
            assert api_callable is not None
            assert callable(api_callable)
            api_path = str(provider_name + MODULE_PATH_SEPARATOR + api_name)
            api_signature = signature(api_callable)
            api_arguments = ArgumentMapper.from_signature(api_signature)
            apis[api_name] = ApiInfo(
                api_name,
                api_path,
                api_callable,
                api_signature,
                api_arguments,
            )

        result[provider_name] = ProviderInfo(provider_name, provider, apis)
    return result


def get_language_locale_codes() -> List[str]:
    result = list()
    for country, languages in BaseProvider.language_locale_codes.items():
        assert isinstance(country, str)
        if isinstance(languages, Sequence):
            for lang in languages:
                result.append(f"{country}_{lang}")
        elif isinstance(languages, str):
            result.append(f"{country}_{languages}")
        else:
            assert False, "Inaccessible section"
    return result
