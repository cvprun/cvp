# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from cvp.scheduler.item import JobItem, JobKey


def find_min_next_schedule(
    jobs: Dict[JobKey, JobItem],
    base: datetime,
) -> Optional[datetime]:
    if not jobs:
        return None

    result: Optional[datetime] = None

    for job in jobs.values():
        if not job.enabled:
            continue
        if not job.cron:
            continue
        if job.is_done:
            continue

        job_schedule = job.next_schedule(base)
        assert base <= job_schedule

        if result is None:
            result = job_schedule
        else:
            if job_schedule < result:
                result = job_schedule

    return result


def find_jobs_in_time_range(
    jobs: Dict[JobKey, JobItem],
    begin: datetime,
    end: datetime,
    *,
    sort=False,
) -> List[Tuple[JobKey, datetime]]:
    if end <= begin:
        raise ValueError("End time must be greater than begin time")

    result = list()

    for key, job in jobs.items():
        if not job.enabled:
            continue
        if not job.cron:
            continue
        if job.is_done:
            continue

        job_iter = job.create_croniter(begin)
        while True:
            job_schedule = job_iter.get_next(datetime)
            assert isinstance(job_schedule, datetime)
            if end < job_schedule:
                break
            result.append((key, job_schedule))

    if sort and result:
        result = sorted(result, key=lambda j: j[1])

    return result
