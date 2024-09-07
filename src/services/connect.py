import psycopg2
from config import load_config

class DBConnection:

    # metodo estatico que executa um comando sql
    # sql = comando SQL a ser executado
    # hasReturn = Flag indicando se ha um retorno do comando executado
    # Retorno:
    # caso ocorra um erro na execucao do comando, retorna -1
    # caso nao ocorra um erro e hasReturn == true, retorna o retorno da execucao daquele comando SQL
    @staticmethod
    def query(sql: str, hasReturn: bool):
        conn = psycopg2.connect(**load_config())

        # cursor para realizar operacoes no banco de dados, parece que eh necessario
        curs = conn.cursor()

        # executa o comando fornecido
        try:
            curs.execute(sql)
        except Exception as erro:
            print("Erro na execucao do SQL:", erro, ", tipo: ", type(erro))
            return -1


        data = ()
        if hasReturn:
            data = curs.fetchall()

        conn.commit()
        curs.close()
        conn.close()

        if hasReturn:
            return data
