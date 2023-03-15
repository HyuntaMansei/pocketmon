show DATABASES;
drop DATABASE pocketmon;
use pokemon;
show TABLES;

drop table pokemon_info_tb;
select * from pokemon_info_tb;

drop table pokemon_evol_tb;

drop table if exists pokemon_info_tb;
create table pokemon_info_tb (
 id int AUTO_INCREMENT,
 `이름` char(50),
 `번호`char(4),
 `타입1`char(20),
 `타입2`char(20),
 `단일타입` char(2),
 `진화 비용`char(10),
 `최대 CP` int,
 `공격력` int,
 `방어력` int,
 `체력` int,
 `포획 확률` char(10),
 `노말` float,
 `격투` float,
 `비행` float,
 `독` float,
 `땅` float,
 `바위` float,
 `벌레` float,
 `고스트` float,
 `강철` float,
 `불꽃` float,
 `물` float,
 `풀` float,
 `전기` float,
 `에스퍼` float,
 `얼음` float,
 `드래곤` float,
 `악` float,
 `페어리` float,
 `단계` int,
 `최종진화` char(2),
  primary key(id),
  unique key(이름)
);

select * from pokemon_info_tb;