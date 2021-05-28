create database testdb;
create table testdb.user (
    id int,
    name varchar(256)
);

insert into testdb.user values(1, "John");
insert into testdb.user values(2, "Tom");
