import psycopg2
from config import load_config

class DBConnection:

    def __init__(self):
        try:
            self.con = psycopg2.connect(**load_config())
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def __del__(self):
        try:
            self.con.close()
        except:
            pass