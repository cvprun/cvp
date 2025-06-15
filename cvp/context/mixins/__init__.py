# -*- coding: utf-8 -*-

from cvp.context.mixins.activity import ActivityMixin
from cvp.context.mixins.appearance import AppearanceMixin
from cvp.context.mixins.canvas import CanvasMixin
from cvp.context.mixins.chat import ChatMixin
from cvp.context.mixins.download import DownloadMixin
from cvp.context.mixins.flow import FlowMixins
from cvp.context.mixins.navigation import NavigationMixin
from cvp.context.mixins.onvif import OnvifMixin
from cvp.context.mixins.service import ServiceMixin
from cvp.context.mixins.supabase import SupabaseMixins
from cvp.context.mixins.toast import ToastMixin


class ContextMixins(
    ActivityMixin,
    AppearanceMixin,
    CanvasMixin,
    ChatMixin,
    DownloadMixin,
    FlowMixins,
    NavigationMixin,
    OnvifMixin,
    SupabaseMixins,
    ServiceMixin,
    ToastMixin,
):
    pass
