create table hpo (
    hpo_id      integer primary key,
    name        text,
    description text
);

create table disease (
    disease_id integer primary key,
    mim_nr   integer,
    mim_hpo  integer,
    hgnc_symbol text,
    FOREIGN KEY(mim_hpo) REFERENCES hpo(hpo_id) 
);

create table gene (
    gene_id         integer primary key,
    ensembl_id      text not null,
    hgnc_symbol     text,
    hgnc_id     integer,
    description     text,
    chrom           text not null,
    start           integer not null,
    stop            integer not null,
    hi_score        float,
    constraint_score  float
);

create table transcript (
    transcript_id       integer primary key,
    ensembl_id          text,
    gene_id             text,
    refseq_id           text,
    chrom               text,
    start               integer,
    stop                integer,
    FOREIGN KEY(gene_id) REFERENCES gene(ensembl_id)
);
