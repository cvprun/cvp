-- drop table public.chat_conversation;
-- drop table public.chat_message;

create table
    public.chat_conversation
(
    id         uuid primary key                                 default gen_random_uuid(),
    owner      uuid references auth.users (id) on delete set null on update cascade,
    title      text        not null check (length(title) < 256) default '',
    created_at timestamptz not null                             default now(),
    updated_at timestamptz                                      default now()
);

create table
    public.chat_message
(
    id              uuid primary key     default gen_random_uuid(),
    conversation_id uuid references chat_conversation (id) on delete set null on update cascade,
    request         jsonb       not null default '{}'::jsonb,
    response        jsonb       not null default '{}'::jsonb,
    created_at      timestamptz not null default now()
);

create index chat_conversation_owner_idx
    on chat_conversation (owner);
create index chat_message_conversation_id_idx
    on chat_message (conversation_id);

alter table public.chat_conversation
    enable row level security;
alter table public.chat_message
    enable row level security;

create policy "Users can view own conversations"
    on public.chat_conversation for select
    using (auth.uid() = owner);

create policy "Users can insert own conversations"
    on public.chat_conversation for insert
    with check (auth.uid() = owner);

create policy "Users can update own conversations"
    on public.chat_conversation for update
    using (auth.uid() = owner);

create policy "Users can view messages in own conversations"
    on public.chat_message for select
    using ((select owner
            from public.chat_conversation as cc
            where cc.id = conversation_id) = auth.uid());

create policy "Users can insert messages in own conversations"
    on public.chat_message for insert
    with check ((select owner
                 from public.chat_conversation as cc
                 where cc.id = conversation_id) = auth.uid());
