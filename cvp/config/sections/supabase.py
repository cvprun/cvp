# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.variables import SUPABASE_ADDRESS


@dataclass
class SupabaseConfig:
    supabase_url: str = SUPABASE_ADDRESS
    supabase_key: str = field(default_factory=str)
    username: str = field(default_factory=str)
