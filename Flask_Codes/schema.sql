drop table if exists test_database;
create table test_database (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);