# -*- coding: utf-8 -*-

CREATE_TABLE_CONVERSATION = """
create table if not exists conversation
(
    id         integer primary key autoincrement,
    title      text     not null default '',
    created_at datetime not null default (datetime('now')),
    updated_at datetime
);
"""

CREATE_TABLE_MESSAGE = """
create table if not exists message
(
    id              integer primary key autoincrement,
    conversation_id integer references conversation (id),
    request         text,
    response        text,
    error           text,
    created_at      datetime not null default (datetime('now'))
);
"""

INSERT_CONVERSATION = """
insert into conversation (title, created_at) values (?, ?);
"""

UPDATE_CONVERSATION_TITLE = """
update conversation set title = ?, updated_at = datetime('now') where id = ?;
"""

DELETE_CONVERSATION = """
delete from conversation where id = ?;
"""

SELECT_CONVERSATION_LATEST = """
select id,
       title,
       strftime('%Y-%m-%d %H:%M:%f%z', created_at)
from conversation
order by created_at desc
limit ?;
"""

SELECT_CONVERSATION_LATEST_AFTER_ID = """
select * from conversation
where id >= ?
order by created_at desc
limit ?;
"""
