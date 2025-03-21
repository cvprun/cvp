# -*- coding: utf-8 -*-

from dataclasses import fields, is_dataclass
from typing import Final, List

from imgui_bundle import imgui

from cvp.cv.stitching.props import StitcherProps
from cvp.cv.stitching.types import (
    BLEND_KEYS,
    BUNDLE_ADJUSTER_KEYS,
    DEFAULT_ETC_MATCH_CONF,
    DEFAULT_ORB_MATCH_CONF,
    ESTIMATOR_KEYS,
    EXPOS_COMP_KEYS,
    FEATURES_FINDER_KEYS,
    MATCHER_KEYS,
    SEAM_FINDER_KEYS,
    STITCHER_MODE_KEYS,
    WARP_KEYS,
    WAVE_CORRECT_KEYS,
)
from cvp.inspect.docstring import get_attribute_docstring

# [IMPORTANT]
# The data type required for the imgui combo is 'list'.
_STITCHER_MODE_CHOICES: Final[List[str]] = list(STITCHER_MODE_KEYS)
_EXPOS_COMP_CHOICES: Final[List[str]] = list(EXPOS_COMP_KEYS)
_BUNDLE_ADJUSTER_CHOICES: Final[List[str]] = list(BUNDLE_ADJUSTER_KEYS)
_FEATURES_FINDER_CHOICES: Final[List[str]] = list(FEATURES_FINDER_KEYS)
_SEAM_FINDER_CHOICES: Final[List[str]] = list(SEAM_FINDER_KEYS)
_ESTIMATOR_CHOICES: Final[List[str]] = list(ESTIMATOR_KEYS)
_MATCHER_CHOICES: Final[List[str]] = list(MATCHER_KEYS)
_WARP_CHOICES: Final[List[str]] = list(WARP_KEYS)
_WAVE_CORRECT_CHOICES: Final[List[str]] = list(WAVE_CORRECT_KEYS)
_BLEND_CHOICES: Final[List[str]] = list(BLEND_KEYS)


def generate_stitcher_props_tooltips(props: StitcherProps):
    assert is_dataclass(props)
    cls = type(props)
    result = dict()
    for field in fields(cls):  # type: ignore[arg-type]
        result[field.name] = get_attribute_docstring(cls, field.name)
    return result


class StitchingTab:
    def __init__(self, props: StitcherProps):
        super().__init__()
        self._props = props
        self._tooltips = generate_stitcher_props_tooltips(props)
        self.clicked_stitch = False
        self.changed_stitcher_mode = False

    def _hovered_tooltip(self, key: str):
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(self._tooltips[key])

    def _main(self) -> None:
        self.changed_stitcher_mode, self._props.stitcher_mode_index = imgui.combo(
            "Stitcher Mode",
            self._props.stitcher_mode_index,
            _STITCHER_MODE_CHOICES,
        )
        self._hovered_tooltip("stitcher_mode_index")

    def _main_extra_params(self) -> None:
        self._props.work_mega_pixel = imgui.input_float(
            "Work MegaPix",
            self._props.work_mega_pixel,
            0.6,
        )[1]
        self._hovered_tooltip("work_mega_pixel")

        changed_features_find, self._props.features_finder_index = imgui.combo(
            "Features Find",
            self._props.features_finder_index,
            _FEATURES_FINDER_CHOICES,
        )
        self._hovered_tooltip("features_finder_index")
        if changed_features_find:
            ff_name = _FEATURES_FINDER_CHOICES[self._props.features_finder_index]
            if ff_name.lower() == "orb":
                self._props.match_conf = DEFAULT_ORB_MATCH_CONF
            else:
                self._props.match_conf = DEFAULT_ETC_MATCH_CONF

        self._props.matcher_index = imgui.combo(
            "Matcher",
            self._props.matcher_index,
            _MATCHER_CHOICES,
        )[1]
        self._hovered_tooltip("matcher_index")

        self._props.estimator_index = imgui.combo(
            "Estimator",
            self._props.estimator_index,
            _ESTIMATOR_CHOICES,
        )[1]
        self._hovered_tooltip("estimator_index")

        self._props.match_conf = imgui.input_float(
            "Matching Confidence",
            self._props.match_conf,
            0.1,
        )[1]
        self._hovered_tooltip("match_conf")

        self._props.conf_thresh = imgui.input_float(
            "Threshold",
            self._props.conf_thresh,
            0.1,
        )[1]
        self._hovered_tooltip("conf_thresh")

        self._props.bundle_adjuster_index = imgui.combo(
            "Bundle Adjuster",
            self._props.bundle_adjuster_index,
            _BUNDLE_ADJUSTER_CHOICES,
        )[1]
        self._hovered_tooltip("bundle_adjuster_index")

        self._props.ba_refine_mask = imgui.input_text(
            "Refinement Mask",
            self._props.ba_refine_mask,
        )[1]
        self._hovered_tooltip("ba_refine_mask")

        self._props.wave_correct_index = imgui.combo(
            "Wave Correct",
            self._props.wave_correct_index,
            _WAVE_CORRECT_CHOICES,
        )[1]
        self._hovered_tooltip("wave_correct_index")

        self._props.warp_index = imgui.combo(
            "Warp",
            self._props.warp_index,
            _WARP_CHOICES,
        )[1]
        self._hovered_tooltip("warp_index")

        self._props.seam_mega_pixel = imgui.input_float(
            "SEAM MegaPix",
            self._props.seam_mega_pixel,
            0.1,
        )[1]
        self._hovered_tooltip("seam_mega_pixel")

        self._props.seam_find_index = imgui.combo(
            "SEAM Find",
            self._props.seam_find_index,
            _SEAM_FINDER_CHOICES,
        )[1]
        self._hovered_tooltip("seam_find_index")

        self._props.compose_mega_pixel = imgui.input_float(
            "Comp MegaPix",
            self._props.compose_mega_pixel,
            -1.0,
        )[1]
        self._hovered_tooltip("compose_mega_pixel")

        self._props.expos_comp_index = imgui.combo(
            "ExposComp Method",
            self._props.expos_comp_index,
            _EXPOS_COMP_CHOICES,
        )[1]
        self._hovered_tooltip("expos_comp_index")

        self._props.expos_comp_nr_feeds = imgui.drag_int(
            "Num ExposComp Feed",
            self._props.expos_comp_nr_feeds,
        )[1]
        self._hovered_tooltip("expos_comp_nr_feeds")

        self._props.expos_comp_nr_filtering = imgui.drag_float(
            "Num ExposComp Filter",
            self._props.expos_comp_nr_filtering,
        )[1]
        self._hovered_tooltip("expos_comp_nr_filtering")

        self._props.expos_comp_block_size = imgui.drag_int(
            "Num ExposComp Feed",
            self._props.expos_comp_block_size,
        )[1]
        self._hovered_tooltip("expos_comp_block_size")

        self._props.blend_index = imgui.combo(
            "Blend Method",
            self._props.blend_index,
            _BLEND_CHOICES,
        )[1]
        self._hovered_tooltip("blend_index")

        self._props.blend_strength = imgui.slider_int(
            "Blend Strength",
            self._props.blend_strength,
            0,
            100,
        )[1]
        self._hovered_tooltip("blend_strength")

        self._props.range_width = imgui.input_int(
            "Range Width",
            self._props.range_width,
        )[1]
        self._hovered_tooltip("range_width")

        self._props.use_cuda = imgui.checkbox("Use CUDA", self._props.use_cuda)[1]
        self._hovered_tooltip("use_cuda")
