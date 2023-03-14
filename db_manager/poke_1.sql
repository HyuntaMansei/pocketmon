create DATABASE pokemon;
use pokemon;

drop table if exists pokemon_info_tb;
create TABLE pokemon_info_tb (
	id INT NOT NULL AUTO_INCREMENT,
    poke_number int not null,
    poke_name char(30) not null,
    evol_deg int null,
    is_first_evol char(1) null,
    is_final_evol char(1) null,
    primary key(id),
    UNIQUE key(poke_name)
);

desc pokemon_info_tb;
select * from pokemon_info_tb;

drop table if exists pokemon_evol_tb;
create table pokemon_evol_tb (
	id INT NOT NULL AUTO_INCREMENT,
    name1 char(30),
    name2 char(30),
    name3 char(30),
    name4 char(30),
    name5 char(30),
    evol_deg int not null,
    PRIMARY KEY (id),
    FOREIGN KEY (name1) REFERENCES pokemon_info_tb (poke_name)
);
desc pokemon_evol_tb;
