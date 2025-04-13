# -*- coding: utf-8 -*-

from cvp.context.mixins.activity import ActivityMixin
from cvp.context.mixins.appearance import AppearanceMixin
from cvp.context.mixins.chat import ChatMixin
from cvp.context.mixins.supabase import SupabaseMixins


class ContextMixins(ActivityMixin, AppearanceMixin, ChatMixin, SupabaseMixins):
    pass
