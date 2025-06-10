# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from unittest import TestCase, main

from cvp.scheduler.find import find_jobs_in_time_range, find_min_next_schedule
from cvp.scheduler.item import JobItem


class FindTestCase(TestCase):
    def setUp(self):
        n1 = JobItem(uuid="1", name="n1", cron="* * * * * */3", enabled=True, repeat=3)
        n2 = JobItem(uuid="2", name="n2", cron="* * * * * */5", enabled=True, repeat=2)
        n3 = JobItem(uuid="3", name="n3", cron="* * * * * */7", enabled=True, repeat=1)
        self.jobs = {n1.key: n1, n2.key: n2, n3.key: n3}

    def test_find_min_next_schedule(self):
        jobs = deepcopy(self.jobs)
        first = datetime(2000, 1, 1, 0, 0, 0)

        expect1 = datetime(2000, 1, 1, 0, 0, 3)
        actual1 = find_min_next_schedule(jobs, first)
        self.assertEqual(expect1, actual1)

        expect2 = datetime(2000, 1, 1, 0, 0, 5)
        actual2 = find_min_next_schedule(jobs, actual1)
        self.assertEqual(expect2, actual2)

        expect3 = datetime(2000, 1, 1, 0, 0, 6)
        actual3 = find_min_next_schedule(jobs, actual2)
        self.assertEqual(expect3, actual3)

        expect4 = datetime(2000, 1, 1, 0, 0, 7)
        actual4 = find_min_next_schedule(jobs, actual3)
        self.assertEqual(expect4, actual4)

        expect5 = datetime(2000, 1, 1, 0, 0, 9)
        actual5 = find_min_next_schedule(jobs, actual4)
        self.assertEqual(expect5, actual5)

        expect6 = datetime(2000, 1, 1, 0, 0, 10)
        actual6 = find_min_next_schedule(jobs, actual5)
        self.assertEqual(expect6, actual6)

        expect7 = datetime(2000, 1, 1, 0, 0, 12)
        actual7 = find_min_next_schedule(jobs, actual6)
        self.assertEqual(expect7, actual7)

        expect8 = datetime(2000, 1, 1, 0, 0, 14)
        actual8 = find_min_next_schedule(jobs, actual7)
        self.assertEqual(expect8, actual8)

        expect9 = datetime(2000, 1, 1, 0, 0, 15)
        actual9 = find_min_next_schedule(jobs, actual8)
        self.assertEqual(expect9, actual9)

    def test_find_jobs_in_time_range(self):
        jobs = deepcopy(self.jobs)

        begin1 = datetime(2000, 1, 1, 0, 0, 0)
        end1 = datetime(2000, 1, 1, 0, 0, 3)
        expect1 = [("1", datetime(2000, 1, 1, 0, 0, 3))]
        actual1 = find_jobs_in_time_range(jobs, begin1, end1, sort=True)
        self.assertEqual(expect1, actual1)

        begin2 = datetime(2000, 1, 1, 0, 0, 3)
        end2 = datetime(2000, 1, 1, 0, 0, 10)
        expect2 = [
            ("2", datetime(2000, 1, 1, 0, 0, 5)),
            ("1", datetime(2000, 1, 1, 0, 0, 6)),
            ("3", datetime(2000, 1, 1, 0, 0, 7)),
            ("1", datetime(2000, 1, 1, 0, 0, 9)),
            ("2", datetime(2000, 1, 1, 0, 0, 10)),
        ]
        actual2 = find_jobs_in_time_range(jobs, begin2, end2, sort=True)
        self.assertEqual(expect2, actual2)


if __name__ == "__main__":
    main()
