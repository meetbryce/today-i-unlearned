create table lessons
(
    id         integer primary key autoincrement not null,
    title      text                              not null,
    content    text                              not null,
    start_year integer                           not null,
    end_year   integer                           not null,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
create index start_year on "lessons" (start_year);
create index end_year on "lessons" (end_year);

create table votes
(
    id         integer primary key autoincrement not null,
    is_upvote  boolean   default true            not null,
    user_ip    string                            not null,
    lesson_id  integer                           not null,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons (id)
);
create unique index unique_user_lesson on "votes" (user_ip, lesson_id);
create index lesson_id on "votes" (lesson_id);