CREATE DATABASE fleetmgr;
USE fleetmgr;

CREATE TABLE  vehicle_data(
    id int(100) primary key auto_increment not null,
    vehicle_id int(100) not null,
    location text not null,
    speed decimal,
    created_at datetime,
  modified_at datetime
)engine=innodb;

CREATE TABLE mobile_epq(
  id int(10) auto_increment primary key not null,
  equipment varchar(250) not null,
  model varchar(250) not null,
  specification varchar(250) not null,
  quantity int(10)  not  null,
  created_at datetime,
  modified_at datetime
)engine=innodb;


CREATE TABLE equipment(
  id int(10) auto_increment primary key not null,
  equipment varchar(250) not null,
  lastDayOfService varchar(250) not null,
  lastOfService varchar(250) not null,
  NextDue varchar(250) not null,
  meID varchar(10)  not  null,
  Status enum('Down','Ready','Shift Change'),
  created_at datetime,
  modified_at datetime
)engine=innodb;



-- Haulage Movement
CREATE TABLE shifts(
  id int(10) primary key auto_increment,
  Morning varchar(250) not null,
  Afternoon varchar(250) not null,
  Target varchar(250) not null,
  Total varchar(250) not null,
  created_at datetime,
  modified_at datetime
)engine = innodb;


-- Hourly Tonnages
CREATE TABLE hourly_Ore(
  id int(10) primary key auto_increment,
  actual_hour_from time not null,
  actual_hour_to time not null,
  actual_volume varchar(250) not null,
  ShiftName varchar(250) not null,
  shifID int(20) not null,
  foreign key(shifID) references shifts(id),
  created_at datetime,
  modified_at datetime
)engine = innodb;

-- Hourly waste Tonnages
CREATE TABLE hourly_waste(
  id int(10) primary key auto_increment,
  actual_hour_from time not null,
  actual_hour_to time not null,
  actual_volume varchar(250) not null,
  ShiftName varchar(250) not null,
  shifID int(20) not null,
  foreign key(shifID) references shifts(id),
  created_at datetime,
  modified_at datetime
)engine = innodb;


-- Drill and Blaster KPI
CREATE TABLE drill_blast(
  id int(10) primary key auto_increment,
  blastedVolume int(100) not null,
  numberOfDaysRequired int(100) not null,
  actual_volumeMovedPayDay int(100) not null,
  created_at datetime,
  modified_at datetime
)engine = innodb;


--Database Triggers for drill blast table
CREATE TRIGGER numberOfDaysRequired_to_deplete_material BEFORE INSERT ON drill_blast
FOR EACH ROW SET @bl = NEW.blastedVolume / 20*(SELECT quantity FROM mobile_epq WHERE equipment='Tiper')


SELECT quantity FROM mobile_epq INNER JOIN equipment as e ON e.equipment = mobile_epq.equipment WHERE e.equipment='Tiper' AND e.Status='Ready';

SELECT*FROM equipment;
-- 1. Crusher Tonnages
CREATE TABLE Crushertonnages(
  id int(10) auto_increment primary key not null,


);

-- 2. stock pile tonnages 
CREATE TABLE stockPile(
  id int(10) auto_increment primary key not null,


);




CREATE TABLE inputOutput (
    id int(10) primary key auto_increment not null,
    SectionName varchar(250) not null,
    plannedInput varchar(250) not null,
    actualinputs varchar(250) not null,
    Utilisation varchar(250) not null

)engine=innodb;
