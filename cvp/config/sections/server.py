# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.variables import DEFAULT_SUPABASE_ADDRESS


@dataclass
class ServerConfig:
    supabase_url: str = DEFAULT_SUPABASE_ADDRESS
    supabase_key: str = field(default_factory=str)
    username: str = field(default_factory=str)

    def join_suffix(self, suffix: str):
        return self.supabase_url.removesuffix("/") + suffix

    @property
    def rest(self):
        return self.join_suffix("/rest/v1/")

    @property
    def auth(self):
        return self.join_suffix("/auth/v1/")

    @property
    def storage(self):
        return self.join_suffix("/storage/v1/")

    @property
    def realtime(self):
        return self.join_suffix("/realtime/v1/")
