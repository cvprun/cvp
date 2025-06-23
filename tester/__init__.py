# -*- coding: utf-8 -*-

from tester.liveness import TestServerLivenessProbe

MEDIAMTX_SERVER = TestServerLivenessProbe.from_dotenv("MEDIAMTX_SERVER_ADDRESS")
