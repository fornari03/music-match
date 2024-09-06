import psycopg2
from config import load_config

class DBConnection:

    def __init__(self):
        self.conn_data = load_config()

    def query(self, sql: str, hasReturn: bool):
        conn = psycopg2.connect(**self.conn_data)

        # cursor para realizar operacoes no banco de dados, parece que eh necessario
        curs = conn.cursor()

        # executa o comando fornecido
        curs.execute(sql)

        data = ()
        if hasReturn:
            data = curs.fecthone()

        conn.commit()
        curs.close()
        conn.close()

        if hasReturn:
            return data
