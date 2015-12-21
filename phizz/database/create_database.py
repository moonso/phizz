import os
import sqlite3
import logging

import click

from .constants import phizz_db
logger = logging.getLogger(__name__)

def get_database(path_to_database = None, database_schema = None):
    """Get the connection to a sqlite3 database
        
        If the databse does not exist create a new one
        according to the schema
        
        Args:
            path_to_database (str): Path to a database
            database_schema (str): Path to a file with the database
                                    schema
        Returns:
            conn (sqlite3.connect): A database connection object
    """
    if not path_to_database:
        path_to_database = phizz_db
    
    db_is_new = not os.path.exists(path_to_database)

    if db_is_new:
        logger.info("Could not find database {0}".format(path_to_database))
        if not database_schema:
            raise IOError("Need to provide a database schema ")
        
        logger.info("Creating database {0}".format(path_to_database))
        conn = sqlite3.connect(path_to_database)
        
        with open(database_schema, 'rt') as f:
            schema = f.read()
        
        conn.executescript(schema)
        logger.debug("Database created")
        
    else:
        logger.debug("Found database {0}".format(path_to_database))
        conn = sqlite3.connect(path_to_database)
    
    return conn

def get_cursor(path_to_database=None, connection=None):
    """Get a cursor for querying the database"""
    if not connection:
        connection = get_database(path_to_database)
    
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    return cursor
    