# -*- coding: utf-8 -*-

from typing import Final

YEARLY: Final[str] = r"0 0 1 1 *"
"""Run once a year at midnight of 1 January"""

ANNUALLY: Final[str] = YEARLY

MONTHLY: Final[str] = r"0 0 1 * *"
"""Run once a month at midnight of the first day of the month"""

WEEKLY: Final[str] = r"0 0 * * 0"
"""Run once a week at midnight on Sunday"""

DAILY: Final[str] = r"0 0 * * *"
"""Run once a day at midnight"""

MIDNIGHT: Final[str] = DAILY

HOURLY: Final[str] = r"0 * * * *"
"""Run once an hour at the beginning of the hour"""

EVERY_MINUTE: Final[str] = r"* * * * *"

# ---------------------------------------------
# Nonstandard predefined scheduling definitions
# ---------------------------------------------

AT_YEARLY: Final[str] = "@yearly"
AT_ANNUALLY: Final[str] = "@annually"
AT_MONTHLY: Final[str] = "@monthly"
AT_WEEKLY: Final[str] = "@weekly"
AT_DAILY: Final[str] = "@daily"
AT_MIDNIGHT: Final[str] = "@midnight"
AT_HOURLY: Final[str] = "@hourly"
