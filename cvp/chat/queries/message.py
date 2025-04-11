# -*- coding: utf-8 -*-

CREATE_TABLE = """
create table if not exists message
(
    id              integer primary key autoincrement,
    conversation_id integer references conversation (id),
    request         text     not null,
    error           text     not null default(''),
    status          integer default 0,
    created_at      datetime not null,
    updated_at      datetime
);
"""

INSERT = """
insert into message (conversation_id, request, error, status, created_at)
values (?, ?, ?, ?, ?);
"""

UPDATE_ERROR_STATUS = """
update message set error = ?, status = ?, updated_at = ? where id = ?;
"""

DELETE = """
delete from message where id = ?;
"""

SELECT = """
select *
from message
where conversation_id = ?
order by created_at
"""
