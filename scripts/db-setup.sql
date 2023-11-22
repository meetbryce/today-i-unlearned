create table lessons
(
    id         integer primary key autoincrement not null,
    content    text                              not null,
    year       integer                           not null,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
create index year on "lessons" (year);

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


-- CREATE TABLE 'transaction'
-- (
--     id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--     user_id INTEGER                           NOT NULL,
--     symbol  TEXT                              NOT NULL,
--     cost    NUMERIC                           NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users (id)
-- );
-- CREATE UNIQUE INDEX id on "transaction" (id);
-- CREATE INDEX user_id on "transaction" (user_id);