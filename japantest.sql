/*==============================================================*/
/* Table: spender                                               */
/*==============================================================*/
create table spender
(
   spender_id           int not null auto_increment,
   spender_name         text not null,
   primary key (spender_id)
);

/*==============================================================*/
/* Table: account_type                                          */
/*==============================================================*/
create table account_type
(
   type_id              int not null auto_increment,
   type_name            text not null,
   primary key (type_id)
);

/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account
(
   account_id            int not null auto_increment,
   account_description   text not null,
   account_currency      text not null,
   account_cost          decimal(10,2) not null,
   account_spenderid     int not null,
   account_date          date not null,
   account_time          time,
   account_typeid        int not null,
   primary key (account_id),
   foreign key (account_spenderid) references spender(spender_id),
   foreign key (account_typeid) references account_type(type_id)
);

insert into spender(spender_name) values ("WPS");
insert into spender(spender_name) values ("FXT");
insert into spender(spender_name) values ("GDM");
insert into spender(spender_name) values ("ZYF");

insert into account_type(type_name) values ("Food & Beverage");
insert into account_type(type_name) values ("Room Charge");
insert into account_type(type_name) values ("Traffic");
insert into account_type(type_name) values ("Entertainment");
insert into account_type(type_name) values ("Shopping");
insert into account_type(type_name) values ("Clothing");
insert into account_type(type_name) values ("Household Items");
insert into account_type(type_name) values ("Others");