create table hpo (
    hpo_id      integer primary key,
    name        text,
    description text
);

create table disease (
    disease_id integer primary key,
    mim_nr   integer,
    mim_hpo  integer,
    FOREIGN KEY(mim_hpo) REFERENCES hpo(hpo_id) 
);
