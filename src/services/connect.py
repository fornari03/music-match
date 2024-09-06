import psycopg2
from config import load_config

class DBConnection:

    def __init__(self):
        self.conn_data = load_config()

    # metodo que executa um comando sql
    # sql = comando SQL a ser executado
    # hasReturn = Flag indicando se ha um retorno do comando executado
    def query(self, sql: str, hasReturn: bool):
        conn = psycopg2.connect(**self.conn_data)

        # cursor para realizar operacoes no banco de dados, parece que eh necessario
        curs = conn.cursor()

        # executa o comando fornecido
        curs.execute(sql)

        data = ()
        if hasReturn:
            data = curs.fetchone()

        conn.commit()
        curs.close()
        conn.close()

        if hasReturn:
            return data

'''
# teste feito para ver se a classe esta acessando o BD
if __name__ == '__main__':
    x = DBConnection()
    #x.query("INSERT INTO artista(id, nome) VALUES (1, 'Fulano')", False)
    print(x.query("SELECT * FROM artista", True))
'''