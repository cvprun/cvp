# -*- coding: utf-8 -*-

from datetime import date, datetime, time
from typing import Final

UNIX_EPOCH_START_DATETIME: Final[datetime] = datetime.fromtimestamp(0.0)
UNIX_EPOCH_START_DATE: Final[date] = date.fromtimestamp(0.0)
MIDNIGHT_TIME: Final[time] = time()
