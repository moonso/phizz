# -*- coding: utf-8 -*-
import sys
import os
import logging
import gzip
from codecs import open

import click

from configobj import ConfigObj

from query_hpo.database import (get_database, build_database)
from query_hpo.database.constants import (config_file, schema_path)
from query_hpo import __version__

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
    """Puzzle: manage DNA variant resources."""
    # configure root logger to print to STDERR
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)


@cli.command()
@click.option('--db_name', default='hpo.db')
##TODO database should be somewhere else
@click.option('--path', default=os.path.abspath("./"))
@click.pass_context
def init(ctx, db_name, path):
    """Create a config file for query hpo."""
    config = ConfigObj()
    config.filename = config_file
    
    database = os.path.join(path, db_name)
    
    if os.path.exists(database):
        logger.error("Databse already exists!")
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
@click.option('-c', '--config',
    type=click.Path(),
    default=config_file
)
@click.pass_context
def query(ctx, config):
    """Query the hpo database.\n
    
        If no databse was found, build a new one according to the config.
    """
    if not os.path.exists(config):
        print("Hj")
        logger.error("There is no config file. Please run 'query_hpo init'")
        logger.info("Exiting")
        sys.exit(1)
    
    config = ConfigObj(config)
    
