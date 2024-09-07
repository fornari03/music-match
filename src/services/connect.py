import psycopg2
from config import load_config

class DBConnection:

    # metodo estatico que executa um comando sql
    # sql = comando SQL a ser executado
    # hasReturn = Flag indicando se ha um retorno do comando executado
    @staticmethod
    def query(sql: str, hasReturn: bool):
        conn = psycopg2.connect(**load_config())

        # cursor para realizar operacoes no banco de dados, parece que eh necessario
        curs = conn.cursor()

        # executa o comando fornecido
        curs.execute(sql)

        data = ()
        if hasReturn:
            data = curs.fetchall()

        conn.commit()
        curs.close()
        conn.close()

        if hasReturn:
            return data
