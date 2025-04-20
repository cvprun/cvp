# -*- coding: utf-8 -*-

from cvp.context.mixins.activity import ActivityMixin
from cvp.context.mixins.appearance import AppearanceMixin
from cvp.context.mixins.chat import ChatMixin
from cvp.context.mixins.onvif import OnvifMixin
from cvp.context.mixins.supabase import SupabaseMixins
from cvp.context.mixins.toast import ToastMixin


class ContextMixins(
    ActivityMixin,
    AppearanceMixin,
    ChatMixin,
    OnvifMixin,
    SupabaseMixins,
    ToastMixin,
):
    pass
