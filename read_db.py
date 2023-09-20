import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_rests(conn):
    """
    Query all rows in the restaurant table
    :param conn: the Connection object
    :return: list of tuples (id, name, venId, url, date)
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'restaurants' LIMIT 0,30")

    return cur.fetchall()

def format_rests(rest_tuple):
    '''just return the venId and url'''
    return rest_tuple[2], rest_tuple[3]
    


def get_rest_lists():
    database = "instance/restaurants.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        return select_all_rests(conn)