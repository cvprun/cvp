# -*- coding: utf-8 -*-

CREATE_TABLE = """
create table if not exists conversation
(
    id         integer primary key autoincrement,
    title      text     not null,
    created_at datetime not null,
    updated_at datetime
);
"""

INSERT = """
insert into conversation (title, created_at) values (?, ?);
"""

UPDATE_TITLE = """
update conversation set title = ?, updated_at = ? where id = ?;
"""

DELETE = """
delete from conversation where id = ?;
"""

SELECT_LATEST = """
select *
from conversation
order by created_at desc
limit ?;
"""

SELECT_LATEST_AFTER_ID = """
select * from conversation
where id > ?
order by created_at desc
limit ?;
"""
