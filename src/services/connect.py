import psycopg2
from ..services.config import load_config

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
            conn.rollback()
            curs.close()
            conn.close()
            return -1


        data = ()
        if hasReturn:
            data = curs.fetchall()

        conn.commit()
        curs.close()
        conn.close()

        if hasReturn:
            return data
        
    @staticmethod
    def delete_user(id: int):
        conn = psycopg2.connect(**load_config())

        curs = conn.cursor()

        try:
            sql = f"DELETE FROM redes_sociais WHERE id_usuario={id}"
            curs.execute(sql)

            sql = f"DELETE FROM conecta_com WHERE id_usuario_1={id} OR id_usuario_2={id}"
            curs.execute(sql)

            sql = f"DELETE FROM usuario_avalia_musica WHERE id_usuario={id}"
            curs.execute(sql)

            sql = f"DELETE FROM tem_interesse WHERE id_usuario={id}"
            curs.execute(sql)

            sql = f"DELETE FROM participou_de WHERE id_usuario={id}"
            curs.execute(sql)

            sql = f"DELETE FROM usuario WHERE id={id}"
            curs.execute(sql)

            conn.commit()
        except Exception as erro:
            print("Erro na delecao do usuario do SQL:", erro, ", tipo: ", type(erro))
            conn.rollback()
        finally:
            curs.close()
            conn.close()
