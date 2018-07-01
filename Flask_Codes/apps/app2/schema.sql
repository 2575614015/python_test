drop table if exists test_database;
create table test_database (
id integer primary key auto_increment,
title VARCHAR(20) not null,
text VARCHAR (100) not null);