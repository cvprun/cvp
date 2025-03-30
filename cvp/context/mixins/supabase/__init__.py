# -*- coding: utf-8 -*-

from cvp.context.mixins.supabase.client import SupabaseClientMixin
from cvp.context.mixins.supabase.session import SupabaseSessionMixin


class SupabaseMixins(SupabaseClientMixin, SupabaseSessionMixin):
    pass
