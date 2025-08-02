# -*- coding: utf-8 -*-

from concurrent.futures.process import ProcessPoolExecutor
from typing import Final, List, NamedTuple, Optional, Sequence


class _OpenglConfig(NamedTuple):
    force_egl: Optional[bool]
    use_accelerate: Optional[bool]


_TEST_CONFIGS: Final[Sequence[_OpenglConfig]] = (
    _OpenglConfig(None, None),
    _OpenglConfig(None, True),
    _OpenglConfig(None, False),
    _OpenglConfig(True, None),
    _OpenglConfig(True, True),
    _OpenglConfig(True, False),
    _OpenglConfig(False, None),
    _OpenglConfig(False, True),
    _OpenglConfig(False, False),
)


def _fetch_main(config: _OpenglConfig) -> bool:
    from cvp.apps.tester.app import TesterApplication

    try:
        TesterApplication(config.force_egl, config.use_accelerate).start()
        return True
    except:  # noqa
        return False


def fetch_opengl_configs_from_subprocess() -> List[_OpenglConfig]:
    """Run a subprocess to check OpenGL config flags and return the result."""

    with ProcessPoolExecutor() as executor:
        fetch_results = executor.map(_fetch_main, _TEST_CONFIGS)

    return [config for config, flag in zip(_TEST_CONFIGS, fetch_results) if flag]


def select_best_opengl_config(configs: List[_OpenglConfig]) -> _OpenglConfig:
    if not configs:
        raise ValueError("No OpenGL configuration candidates provided.")

    # 1st. Prefer configs with hardware acceleration enabled
    if accelerated_configs := [cfg for cfg in configs if cfg.use_accelerate]:
        return accelerated_configs[0]

    # 2nd. Prefer configs with EGL forced
    if egl_configs := [cfg for cfg in configs if cfg.force_egl is True]:
        return egl_configs[0]

    return configs[0]


def fetch_best_opengl_config_from_subprocess() -> _OpenglConfig:
    return select_best_opengl_config(fetch_opengl_configs_from_subprocess())


if __name__ == "__main__":
    print(fetch_best_opengl_config_from_subprocess())
