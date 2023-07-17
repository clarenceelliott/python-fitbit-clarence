import argparse

from rollingCalculator.data.database import create_connection, create_table


parser = argparse.ArgumentParser()

parser.add_argument("-db", "--database", dest="database_name", default="database.db", help="Database name")
# parser.add_argument("-u", "--username",dest ="username", help="User name")
# parser.add_argument("-p", "--password",dest = "password", help="Password")
# parser.add_argument("-size", "--binsize",dest = "binsize", help="Size", type=int)

args = parser.parse_args()


def main():
    # if not database_name:
    #     database_name = 'database.db'

    sql_create_tokens_table = """ 
    CREATE TABLE IF NOT EXISTS UserToken (
    id integer PRIMARY KEY,
    user_name text UNIQUE NOT NULL,
    access_token text,
    refresh_token text,
    expiration datetime_interval_precision 
    );
    """

    sql_create_fitness_data_table = """
    CREATE TABLE IF NOT EXISTS FitnessData (
    id integer PRIMARY KEY,
    user_id integer NOT NULL, 
    measurement_time datetime_interval_precision,
    weight real, 
    bmi real, 
    body_fat_pct real, 
    fat_free_body_weight real, 
    subcutaneous_fat_pct real,
    visceral_fat_pct real, 
    body_water_pct real, 
    muscle_mass_lbs real, 
    bone_mass_lbs real, 
    protein_pct real, 
    bmr_kcal integer, 
    metabolic_age integer, 
    valid boolean,
    FOREIGN KEY(user_id) REFERENCES UserToken(id)
    );
    """

    # create a database connection
    conn = create_connection(args.database_name)

    # create tables
    if conn is not None:
        # create user tokens table
        create_table(conn, sql_create_tokens_table)

        # create fitness data table
        create_table(conn, sql_create_fitness_data_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
