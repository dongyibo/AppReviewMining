create table raw_review(
	id bigint auto_increment,
	reviewer_name varchar(255) null,
	title varchar(255) null,
	date varchar(255) null,
	content text null,
	rate int null,
	category int null,
	constraint `PRIMARY`
		primary key (id)
);


create table app(
  id int,
  name varchar(255),
  constraint `PRIMARY`
		primary key (id)
);