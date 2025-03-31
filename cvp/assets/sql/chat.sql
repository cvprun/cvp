drop table public.chat_conversations;
drop table public.chat_messages;

create table
    public.chat_conversations
(
    id         uuid primary key         default gen_random_uuid(),
    owner      uuid references auth.users (id) on delete set null on update cascade,
    title      text not null check (length(title) < 256),
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

create table
    public.chat_messages
(
    id              uuid primary key         default gen_random_uuid(),
    conversation_id uuid references chat_conversations (id) on delete set null on update cascade,
    request         jsonb,
    response        jsonb,
    created_at      timestamp with time zone default now()
);

create index chat_conversations_owner_idx
    on chat_conversations (owner);
create index chat_messages_conversation_id_idx
    on chat_messages (conversation_id);

alter table public.chat_conversations
    enable row level security;
alter table public.chat_messages
    enable row level security;

create policy "Users can view own conversations"
    on public.chat_conversations for select
    using (auth.uid() = owner);

create policy "Users can insert own conversations"
    on public.chat_conversations for insert
    with check (auth.uid() = owner);

create policy "Users can update own conversations"
    on public.chat_conversations for update
    using (auth.uid() = owner);

create policy "Users can view messages in own conversations"
    on public.chat_messages for select
    using ((select owner
            from public.chat_conversations as cc
            where cc.id = conversation_id) = auth.uid());

create policy "Users can insert messages in own conversations"
    on public.chat_messages for insert
    with check ((select owner
                 from public.chat_conversations as cc
                 where cc.id = conversation_id) = auth.uid());
