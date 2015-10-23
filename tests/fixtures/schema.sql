create table hpo (
    hpo_id      integer primary key,
    hpo_name    text
);

create table disease (
    disease_id integer primary key,
    mim_nr   integer,
    hgnc_id  text,
    mim_hpo  integer,
    FOREIGN KEY(mim_hpo) REFERENCES hpo(hpo_id) 
);
