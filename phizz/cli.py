# -*- coding: utf-8 -*-
import sys
import os
import logging
import gzip
import json

import click

from codecs import open

from configobj import ConfigObj

from phizz.database import (get_database, build_database)
from phizz.database.constants import (config_file, schema_path, phizz_db)
from phizz.utils import (query_hpo, query_disease, build_gene_trees, query_gene_symbol)
from phizz import __version__

from .log import configure_stream, LEVELS

logger = logging.getLogger(__name__)


@click.group()
@click.option('-v', '--verbose', 
    count=True, 
    default=2
)
@click.version_option(__version__)
@click.pass_context
def cli(ctx, verbose):
    """phizz: query hpo and omim resources."""
    # configure root logger to print to STDERR
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)


@cli.command()
@click.option('--db_name', default=phizz_db)
##TODO database should be somewhere else
@click.option('--path', default=os.path.abspath("./"))
@click.pass_context
def init(ctx, db_name, path):
    """Create a config file for phizz."""
    config = ConfigObj()
    config.filename = config_file
    
    database = db_name
    
    if os.path.exists(database):
        logger.error("Databse already exists in {0}".format(database))
        sys.exit(1)
    
    logger.info("Set database to {0}".format(database))
    config["database"] = database
    
    config.write()
    
    conn = get_database(
        path_to_database=database, 
        database_schema=schema_path
    )
    
    build_database(conn)

@cli.command()
@click.argument('gene_file',
    type=click.Path(exists=True)
)
@click.option('--db_name', default="genes.db")
##TODO database should be somewhere else
@click.option('--path', default=os.path.abspath("./"))
@click.pass_context
def build_genes(ctx, gene_file, db_name, path):
    """Create a gene database."""
    database = db_name
    
    if os.path.exists(database):
        logger.error("Databse already exists in {0}".format(database))
        sys.exit(1)
    
    logger.info("Set database to {0}".format(database))
    gene_db = os.path.join(path, db_name)
    
    gene_trees = build_gene_trees(gene_file, gene_db)
    

@cli.command()
@click.option('--db_name', 
            default=phizz_db,
            type=click.Path()
            )
##TODO database should be somewhere else
@click.option('--path', default=os.path.abspath("./"))
@click.pass_context
def delete(ctx, db_name, path):
    """Delete the database."""
    
    if not os.path.exists(db_name):
        logger.error("Databse {0} does not exist".format(db_name))
        sys.exit(1)
    
    logger.info("Deleting database {0}".format(db_name))
    
    os.remove(db_name)
    
    logger.info("Database {0} deleted".format(db_name))
    


@cli.command()
@click.option('-c', '--config',
    type=click.Path(),
)
@click.option('-h', '--hpo_term',
    multiple=True,
    help="Specify a hpo term"
)
@click.option('-m', '--mim_term',
    multiple=True,
    help="Specify a omim id"
)
@click.option('-o', '--outfile',
    type=click.File('w'),
    help="Specify path to outfile"
)
@click.option('-j', '--to_json',
    is_flag=True,
    help="If output should be in json format"
)
@click.option('--chrom',
    help="The chromosome",
    type=str
)
@click.option('--start',
    type=int,
)
@click.option('--stop',
    type=int,
)
@click.pass_context
def query(ctx, config, hpo_term, mim_term, outfile, to_json, chrom, start, stop):
    """Query the hpo database.\n
    
        Print the result in csv format as default.
    """
    if not (hpo_term or mim_term or chrom):
        logger.error("Please provide at least one hpo- or mim term")
        logger.info("Exiting")
        sys.exit(1)
    
    database = phizz_db
    if config:
        config = ConfigObj(config)
        database = config['database']
    
    logger.info("Using database {0}".format(database))
    
    header = "#{0}\t{1}".format('hpo_id', 'description')
    results = []
    
    if chrom and start and stop:
        for hgnc_symbol in query_gene_symbol(chrom, start, stop):
            results.append(hgnc_symbol)
        header = "#hgnc_symbol"
    
    if hpo_term:
        try:
            for result in query_hpo(hpo_terms=hpo_term, database=database):
                results.append(result)
        except ValueError:
            logger.info("Exiting")
            sys.exit(1)
    
    if mim_term:
        try:
            for result in query_disease(disease_terms=mim_term, database=database):
                results.append(result)
        except ValueError:
            logger.info("Exiting")
            sys.exit(1)
    
    if to_json:
        if outfile:
            json.dump(results, outfile)
        else:
            print(json.dumps(results))
                
    else:
        if outfile:
            outfile.write(header+'\n')
        else:
            print(header)
        
        for result in results:
            if chrom:
                print_line = result
            else:
                print_line = "{0}\t{1}".format(
                    result['hpo_term'], result['description'])
            if outfile:
                outfile.write(print_line+'\n')
            else:
                print(print_line) 
    
