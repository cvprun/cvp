# -*- coding: utf-8 -*-

from cvp.debugging._mark import Mark, MarkBeginEndPair, MarkTodo

__MSG_ADD_A_NEW_TODO__ = MarkTodo("To add a new 'msg'")

__TOAST_MARK__ = Mark("Toast message events")
__TOAST_FS_EVENTS_PAIR__ = MarkBeginEndPair.from_mark(__TOAST_MARK__)

__WATCHDOG_MARK__ = Mark("Watchdog filesystem events")
__WATCHDOG_FS_EVENTS_PAIR__ = MarkBeginEndPair.from_mark(__WATCHDOG_MARK__)
