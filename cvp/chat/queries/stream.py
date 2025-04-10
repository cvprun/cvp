# -*- coding: utf-8 -*-

CREATE_TABLE = """
create table if not exists stream
(
    id         integer primary key autoincrement,
    message_id integer references message (id),
    chunk      text     not null,
    created_at datetime not null
);
"""

INSERT = """
insert into stream (message_id, chunk, created_at)
values (?, ?, ?);
"""

DELETE = """
delete from stream where id = ?;
"""

SELECT = """
select *
from stream
where message_id = ?
order by created_at
"""
