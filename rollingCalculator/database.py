import sqlite3
from sqlite3 import Error
from datetime import datetime

from rollingCalculator.commandline_args import args


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def select_user_token(conn, user_name):
    return conn.execute("SELECT * FROM UserToken WHERE user_name = %s;" % user_name).fetchall()


def insert_user_token(conn, user_token_info):
    """
        Insert a new user token into the token table
        :param conn:
        :param user_token_info:
        :return: usertoken id
        """
    sql = ''' INSERT INTO UserToken(user_name, access_token, refresh_token, expiration)
                  VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user_token_info)
    conn.commit()
    return cur.lastrowid


def update_user_token(conn, user_token_info):
    """
    update user token info
    :param conn:
    :param user_token_info:
    :return: user_token id
    """
    sql = ''' UPDATE UserToken
                  SET user_name = ? ,
                      access_token = ? ,
                      refresh_token = ?,
                      expiration = ?
                  WHERE user_name = ?'''
    cur = conn.cursor()
    cur.execute(sql, user_token_info)
    conn.commit()


def select_fitness_data(conn, user_name):
    return conn.execute("SELECT * FROM FitnessData WHERE user_name = %s;" % user_name).fetchall()


def insert_fitness_data(conn, user_id, **kwargs):
    sql, values = _build_fitness_data_query('INSERT', user_id, **kwargs)
    # print('query:' + sql + '\n')
    # print('\n\n' + str(values))

    cur = conn.cursor()
    cur.execute(sql, tuple(values))
    conn.commit()


def update_fitness_data(conn, user_id, **kwargs):
    sql, values = _build_fitness_data_query('UPDATE', user_id, **kwargs)
    # print('query:' + sql + '\n')
    # print('\n\n' + str(values))

    cur = conn.cursor()
    cur.execute(sql, values) # fitness_data_update_values)
    conn.commit()


def _build_fitness_data_query(verb, user_id, **kwargs):
    # set fields from **kwargs in provided dict for real fields
    fitness_columns = {
        'id': None,  # Required for UPDATE operation
        'user_id': user_id,
        'measurement_time': None,
        'weight': None,
        'bmi': None,
        'body_fat_pct': None,
        'fat_free_body_weight': None,
        'subcutaneous_fat_pct': None,
        'visceral_fat_pct': None,
        'body_water_pct': None,
        'muscle_mass_lbs': None,
        'bone_mass_lbs': None,
        'protein_pct': None,
        'bmr_kcal': None,
        'metabolic_age': None,
        'valid boolean': None,
    }

    for key, value in kwargs.items():
        print(key, value)
        if key in fitness_columns.keys():
            fitness_columns[key] = value

    sql = ''
    fitness_values = []

    if verb == 'INSERT': 
        sql += '''INSERT INTO FitnessData('''
        # fitness_data_insert_values = []

        for key, value in fitness_columns.items():
            if value is not None:
                sql += "%s, " % key
                fitness_values.append(value)

        # Removing the extra trailing comma from the string
        sql = sql[:-2]

        sql += ''') VALUES( ''' + ('''?, ''' * (len(fitness_values)-1)) + '''?);'''

    elif verb == 'UPDATE':
        if not fitness_columns['id']:
            raise Error("FitnessData ID Required to do update!!")

        sql += ''' UPDATE FitnessData SET '''
        # fitness_data_update_values = []

        for key, value in fitness_columns.items():
            if value is not None:
                sql += "%s = ?, " % key
                fitness_values.append(value)

        # Removing the extra trailing comma from the string
        sql = sql[:-2]
        sql += ''' WHERE user_id = ? AND id = ?'''
        fitness_values.append(fitness_columns['user_id'])
        fitness_values.append(fitness_columns['id'])

    else: 
        raise Error(message="Unsupported operation")

    return sql, fitness_values
   

def main():
    # create a database connection
    conn = create_connection(args.database_name)

    # insert/update user tables
    if conn is not None:
        #insert_user_token(conn, ('clarence', None, None, datetime.now()))
        # insert_user_token(conn, ('testUser', 'access_token', 'refresh_token', datetime.now()))
        #update_user_token(conn, ('testUser', 'access_token', 'refresh_token', datetime.now(),  'testUser'))

        # insert_fitness_data(conn, 1, weight=9000)
        # update_fitness_data(conn, 1, id=2, weight=5555555)

        print("Data:" + str(conn.execute("SELECT  * FROM UserToken;").fetchall()))
        print("Data:" + str(conn.execute("SELECT  * FROM FitnessData;").fetchall()))

    else:
        raise Error("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
