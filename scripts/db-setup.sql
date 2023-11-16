create table lessons
(
    id         integer primary key autoincrement not null,
    content    text                              not null,
    year       integer                           not null,
    created_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
create index year on "lessons" (year);

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