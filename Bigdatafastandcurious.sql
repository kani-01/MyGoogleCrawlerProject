-- Google PlayStore Apps Information Project
-- Author    : Kanimozhi Kalaichelvan
-- Professor : Dr.Haroon Malik

show databases;
use playstoreinfo;


set sql_safe_updates =0;

show tables;


-- ----------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------

-- Task 1 :::

-- ---------------------------------------------------------------------------------------------------------------------------------
-- PageInfo Table Contains URL information of the Pages Crawled so far

create table PageInfo(linkprovided varchar(1000) primary key, timestamp datetime)ENGINE=InnoDB DEFAULT CHARSET=latin1;

desc PageInfo;

select * from PageInfo order by timestamp asc;

-- ----------------------------------------------------------------------------------------------------------------------------------
-- task1Appdata Table Contains all Apps and App Data information from the Pages Crawled so far

create table task1Appdata(docid varchar(500) primary key, Title varchar(200),linkaddress varchar(1000), CurrentTimestamp datetime); -- ENGINE=InnoDB DEFAULT CHARSET=latin1;

desc task1Appdata;

select * from task1Appdata order by CurrentTimestamp asc;

select count(*) as Total_count_of_Apps from task1Appdata;


-- ----------------------------------------------------------------------------------------------------------------------------------


-- Task 2 :::
-- ------------------------------------------------------------------------------------------------------------------------------------
-- taskappbraincategoryinfo Table Contains URL information of the Categories Crawled so far in APPBRAIN WEBSITE

-- Pagevisited gives the Category selected in AppBrain Website 
create table taskappbraincategoryinfo(Pagevisited varchar(500), CurrentTimestamp datetime, primary key(Pagevisited))ENGINE=InnoDB DEFAULT CHARSET=latin1;

select * from taskappbraincategoryinfo order by CurrentTimestamp asc;

-- select * from taskappbraincategoryinfo where Pagevisited ='';

desc taskappbraincategoryinfo;

-- ----------------------------------------------------------------------------------------------------------------------------------

-- task2appbrain Table Contains all Apps and App Data such as Rating, Name, link information from the Pages Crawled so far in Appbrain

create table task2appbrain(href varchar(500), NameofApp varchar(500), Rating float, CurrentTimestamp datetime, statusflag int(10), primary key(href,NameofApp))ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- insert into task2appbrain VALUES (500,'/app/yahoo-mail/jhfjk','Yahoo', 4.3, 'sefsef', '2018-11-01 01:43:14',1);

desc task2appbrain;

select * from task2appbrain;

select * from task2appbrain order by Rating desc;

select * from task2appbrain order by CurrentTimestamp desc;

select * from task2appbrain order by CurrentTimestamp asc;

select count(*) as Total_count_of_Entries from task2appbrain;

-- ----------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------













