create database moviedb;
use moviedb;

create table user(
	id int,
    name varchar(150),
    email varchar(150),
    password varchar(150)
);

alter table user
add primary key(id);

create table watched(
	id int,
    movie_id varchar(10),
    title varchar(255)
);

alter table watched
add column userid int;

alter table watched
add foreign key (userid) references user(id);

alter table watched
add column rating int;


insert into watched(id, movie_id, title, userid)
values (1, '49026', 'The Dark Knight Rises', 1);

insert into watched(id, movie_id, title, userid)
values (2, '37724', 'Skyfall', 1);

insert into user (id, name, email, password)
values (1, 'Shubhaditya Singh', 'shubh@email.com', 'pbkdf2:sha256:260000$dlhycZ50MMt3JtCb$8b450747559ecf023981108fc1ed8f2c01bb5ee98a7f917385f3e8defddaeac4');