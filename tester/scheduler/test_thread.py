# -*- coding: utf-8 -*-

from datetime import datetime
from unittest import TestCase, main

from cvp.scheduler.item import JobItem, JobKey
from cvp.scheduler.thread import SchedulerThread


class ThreadTestCase(TestCase):
    def setUp(self):
        n1 = JobItem(uuid="1", name="n1", cron="* * * * * */3", enabled=True, repeat=3)
        n2 = JobItem(uuid="2", name="n2", cron="* * * * * */5", enabled=True, repeat=2)
        n3 = JobItem(uuid="3", name="n3", cron="* * * * * */7", enabled=True, repeat=1)
        self.jobs = {n1.key: n1, n2.key: n2, n3.key: n3}

    def test_find_min_next_schedule(self):
        def scheduled_callback(key: JobKey, scheduled: datetime) -> None:
            print(key, scheduled)

        with SchedulerThread(scheduled_callback) as thread:
            self.assertTrue(thread.opened)
            self.assertFalse(thread.is_alive())
            self.assertFalse(thread.is_done())
            try:
                thread.start()
                self.assertTrue(thread.is_alive())
            finally:
                thread.quit()
                self.assertTrue(thread.is_done())
                thread.join()
                self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    main()
