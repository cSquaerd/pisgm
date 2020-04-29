import base64, random, sqlite3
from sqlite3 import Error
from Crypto.Random import get_random_bytes

import pisgmRSA as rsa

def create_connection(db_file):
    """ create a database connection to a SQLite database
    :param db_file: fullpath to database file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_tables(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    sql_create_pisgmmasterkeys_table = """ CREATE TABLE IF NOT EXISTS pisgmmasterkey (
                                 group_id INTEGER PRIMARY KEY,
                                 key TEXT NOT NULL
                                 ); """
    sql_create_pisgmusers_table = """ CREATE TABLE IF NOT EXISTS pisgmusers (
                                 user_id INTEGER PRIMARY KEY,
                                 public_key TEXT NOT NULL
                                 ); """

    sql_create_pisgmmembership_table = """CREATE TABLE IF NOT EXISTS pisgmmembers (
                        group_id INTEGER NOT NULL,
                        user_id INTEGER  NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES pisgmmasterkey (group_id)
                        FOREIGN KEY (user_id) REFERENCES pisgmusers (user_id)
                        CONSTRAINT PK_MEMBERGROUP PRIMARY KEY (group_id, user_id)
                                );"""

    try:
        c = conn.cursor()
        c.execute(sql_create_pisgmmasterkeys_table)
        c.execute(sql_create_pisgmusers_table)
        c.execute(sql_create_pisgmmembership_table)
    except Error as e:
        print(e)

def create_group(conn):
    """
    Create a new group, generate group_id and key randomly 
    Requires database to be connected and tables created
    :param conn: Connection to the database being used
    :return: group_id
    """
#    new_group_id = random.getrandbits(64)
    new_group_id = random.randrange(1,2**63-1)
    new_key = base64.b64encode(get_random_bytes(32))
    new_group = (new_group_id, new_key)

    sql = ''' INSERT INTO pisgmmasterkey(group_id, key)
              VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, new_group)
        conn.commit()
    except Error as e:
        print(e)

    return new_group_id

def create_user(conn,public_key):
    """
    Create a new user, generate user_id randomly and link with group_id
    Requires database to be connected, tables created, and group_id
    :param conn: Connection to the database being used
    :param group_id: string of the group user to be added to
    :return: user_id
    """
    new_user_id = random.randrange(1,2**63-1)
    new_user = (new_user_id, public_key)

    sql = ''' INSERT INTO pisgmusers(user_id, public_key)
              VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, new_user)
        conn.commit()
    except Error as e:
        print(e)

    return new_user_id

def add_member(conn, group_id, user_id):
    """
    Create a new user, generate user_id randomly and link with group_id
    Requires database to be connected, tables created, and group_id
    :param conn: Connection to the database being used
    :param group_id: string of the group user to be added to
    :return: user_id
    """
    membership = (group_id, user_id)

    sql = ''' INSERT INTO pisgmmembers(group_id, user_id)
              VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, membership)
        conn.commit()
    except Error as e:
        print(e)

    return 



def get_keys(conn,group_id,user_id):
    """
    Find the masterkey (if is exists) for the user_id, group_id combination
    Requires database to be connected, tables created, group_id and user_id
    :param conn: Connection to the database being used
    :param group_id: group_id of requested group
    :param user_id: user_id in requested group
    :return: group master key if found
    """
    sql = '''SELECT public_key, key FROM pisgmmembers JOIN pisgmmasterkey 
             ON pisgmmembers.group_id = pisgmmasterkey.group_id
             JOIN pisgmusers 
             ON pisgmmembers.user_id = pisgmusers.user_id
             WHERE pisgmmembers.group_id=? AND pisgmmembers.user_id=?
          '''
    membership = (group_id, user_id)
    try:
        cur = conn.cursor()
        cur.execute(sql, membership)
        keys = cur.fetchone()
    except Error as e:
        print(e)

    return keys[0], keys[1]

def get_public_key(conn,user_id):
    """
    Find the masterkey (if is exists) for the user_id, group_id combination
    Requires database to be connected, tables created, group_id and user_id
    :param conn: Connection to the database being used
    :param group_id: group_id of requested group
    :param user_id: user_id in requested group
    :return: group master key if found
    """
    sql = '''SELECT public_key FROM pisgmmembers
             WHERE user_id=?
          '''
    user = (user_id)
    try:
        cur = conn.cursor()
        cur.execute(sql, user)
        keys = cur.fetchone()
    except Error as e:
        print(e)

    return keys[0]





def main():
    database = r"./data/pisgm.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        create_tables(conn)
    else:
        print("Error! cannot create the database connection.")
    add_member(conn, 7482413770505460036, 8270950596653088861)
    add_member(conn, 7968397989709198061, 4994496195162594573)
    


if __name__ == '__main__':
    #print('Nothing')
    main()
