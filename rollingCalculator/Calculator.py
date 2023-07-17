import json
import os
# from data.database import create_connection, insert_user_token
import sqlite3
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from fitbit import Fitbit
# create_connection, insert_user_token


#database stuff because the imports are being weird
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert_user_token(conn, user_token_info):
    """
        Insert a new user token into the token table
        :param conn:
        :param user_token_info:
        :return: usertoken id
        """
    sql = ''' INSERT INTO user_tokens(username, access_token, refresh_token, expiration)
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
    sql = ''' UPDATE user_tokens
                  SET username = ? ,
                      access_token = ? ,
                      refresh_token = ?,
                      expiration = ?
                  WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, user_token_info)
    conn.commit()


class RollingCalculator(object):
    def __init__(self, **kwargs):
        self.username = 'clarence'
        self.user_id = None
        self.conn = create_connection('/Users/clarenceelliott/PycharmProjects/python-fitbit-clarence/rollingCalculator/data/database.db')

    def read_secrets(self, filename=None) -> dict:
        if not filename:
            filename = os.path.join('/Users/clarenceelliott/PycharmProjects/python-fitbit-clarence/secrets.json')
        try:
            with open(filename, mode='r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return {}

    def write_secrets(self, secrets, filename=None):
        if not filename:
            filename = os.path.join('/Users/clarenceelliott/PycharmProjects/python-fitbit-clarence/secrets.json')
        try:
            with open(filename, mode='w') as f:
                return f.write(json.dumps(secrets, indent=4))
        except FileNotFoundError:
            return {}

    def refresh_cb(self, token):
        # TODO get correct expiration
        insert_user_token(self.conn, ('clarence', self.access_token, token, datetime.now()))
        return


def dostuff():
    #TODO: Research PKCE later
    #https://help.aweber.com/hc/en-us/articles/360036524474-How-do-I-use-Proof-Key-for-Code-Exchange-PKCE-
    # verifier_bytes = os.urandom(32)
    # code_verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b'=')
    #
    # challenge_bytes = hashlib.sha256(code_verifier).digest()
    # code_challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=')

    rolling_calculator = RollingCalculator()

    secrets = rolling_calculator.read_secrets()
    print(secrets)

    fitbit_api = Fitbit(secrets["client_id"], secrets["client_secret"], refresh_cb=rolling_calculator.refresh_cb)

    # print(fitbit_api)

    auth_url, state = fitbit_api.client.authorize_token_url()
    print(auth_url)
    print(state)

    redirect_url_full = input(" Please click url and past redirected url below:")

    code = parse_qs(urlparse(redirect_url_full).query)['code'][0]
    print(code)
    # code = "2279b842a3d8685a69366c7f389a460ed8bcd6c4"
    # state = "NhIRuqka9XaH5pwgKnbpNYN2nOQC33"


    # Figure out how to automate this....
    access_token = fitbit_api.client.fetch_access_token(code=code)
    rolling_calculator.access_token = access_token['access_token']
    rolling_calculator.refre
    refresh_token = ''
    print(access_token)


    body_weight = fitbit_api.get_bodyweight(period='1w')
    print(body_weight)


if __name__ == "__main__":
    dostuff()

  # read/ write tests

