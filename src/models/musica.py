from ..services.connect import DBConnection
from .usuario import Usuario
from random import shuffle

class Musica:

    def __init__(self):
        self.id = None
        self.nome = None
        self.capa = None
        self.link_spotify = None
        self.__isNew = True

    def change_values(self, data):
        for key in data.keys():
            if key == "id":
                self.id = data[key]
            elif key == "nome":
                self.nome = data[key]
            elif key == "capa":
                self.capa = data[key]
            elif key == "link_spotify":
                self.link_spotify = data[key]

    def save(self):
        if self.nome == None:
            self.nome = "NULL"
        elif self.nome[0] != "'" and self.nome[-1] != "'":
            self.nome = f"'{self.nome}'"
        if self.capa == None:
            self.capa = "NULL"
        if self.link_spotify == None:
            self.link_spotify = "NULL"
        elif self.link_spotify[0] != "'" and self.link_spotify[-1] != "'":
            self.link_spotify = f"'{self.link_spotify}'"

        if self.__isNew:
            sql = f"INSERT INTO musica (nome, capa, link_spotify) VALUES ({self.nome}, {self.capa}, {self.link_spotify})"
        else:
            sql = f"UPDATE musica SET nome={self.nome}, capa={self.capa}, link_spotify={self.link_spotify} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False        
        return True

    @staticmethod
    def where(data: dict):
        sql = "SELECT id, nome, capa, link_spotify FROM musica"
        # se coloca parenteses entre os nomes da coluna o retorno eh uma string que quebra o codigo, n entendi direito o pq :)

        if len(data.keys()) != 0:
            key0 = next(iter(data))
            sql += f" WHERE {key0}={data[key0]}"

            for key in data:
                if key == key0:
                    continue
                
                sql += f" AND {key}={data[key]}"
        
        lines = DBConnection.query(sql, True)

        if lines == -1:
            return False

        obj = []
        for inst in lines:
            new_obj = Musica()
            new_obj.__isNew = False
            read_data = {"id": inst[0], "nome": inst[1], "capa": inst[2], "link_spotify": inst[3]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj

    # esta retornando uma lista de tuplas em que o primeiro elemento da tupla eh o nome do artista
    @staticmethod
    def getArtistsName(idMusic: int):
        sql = f"SELECT a.nome FROM artista a JOIN artista_tem_musica atm ON a.id=atm.id_artista WHERE atm.id_musica={idMusic}"

        query_ans = DBConnection.query(sql, True)
        if query_ans == -1:
            return False
        return query_ans
    
    # retorna duas listas:
    # uma com as musicas que ja tem feedback, uma tupla de um obj musica com o feedback
    # uma com as musicas sem feedback, so com o objeto
    @staticmethod
    def classifyMusic(idUser: int):
        sql_feedback = f"SELECT m.id, m.nome, m.capa, m.link_spotify, uam.feedback FROM musica m JOIN usuario_avalia_musica uam ON m.id=uam.id_musica WHERE uam.id_usuario={idUser}"
        sql_no_feedback = f"SELECT m.id, m.nome, m.capa, m.link_spotify FROM musica m WHERE m.id NOT IN (SELECT uam.id_musica FROM usuario_avalia_musica uam WHERE uam.id_usuario={idUser})"

        lines_feedback = DBConnection.query(sql_feedback, True)
        if lines_feedback == -1:
            return False

        lines_no_feedback = DBConnection.query(sql_no_feedback, True)
        if lines_no_feedback == -1:
            return False
        
        feedback_list = []
        for inst in lines_feedback:
            new_obj = Musica()
            new_obj.__isNew = False
            with open (f"imagem_musica_{inst[0]}.jpg", 'wb') as arquivo:
                arquivo.write(inst[2])
            read_data = {"id": inst[0], "nome": inst[1], "capa": f'imagem_musica_{inst[0]}.jpg', "link_spotify": inst[3]}

            # feedback positivo: True, negativo: False
            feedback_list.append((read_data, inst[4]))
        
        no_feedback_list = []
        for inst in lines_no_feedback:
            new_obj = Musica()
            new_obj.__isNew = False
            with open (f"imagem_musica_{inst[0]}.jpg", 'wb') as arquivo:
                arquivo.write(inst[2])
            read_data = {"id": inst[0], "nome": inst[1], "capa": f"imagem_musica_{inst[0]}.jpg", "link_spotify": inst[3]}

            no_feedback_list.append(read_data)

        return feedback_list, no_feedback_list
    
    # cria um feedback entre a musica e o usuario com os ids especificados
    @staticmethod
    def createFeedback(idMusic: int, idUser: int, feedback: bool):
        sql = f"INSERT INTO usuario_avalia_musica (id_usuario, id_musica, feedback) VALUES ({idUser}, {idMusic}, {feedback})"

        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # retira o feedback do usuario idUser pra musica idMusic
    @staticmethod
    def removeFeedback(idMusic: int, idUser: int):
        sql = f"DELETE FROM usuario_avalia_musica WHERE id_usuario={idUser} AND id_musica={idMusic}"

        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # atualiza o feedback do usuario idUser para a musica idMusic
    @staticmethod
    def updateFeedback(idMusic: int, idUser: int, feedback: bool):
        sql = f"UPDATE usuario_avalia_musica SET feedback = {feedback} WHERE id_usuario = {idUser} AND id_musica = {idMusic}"
        
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # pega os estilos musicais de uma musica
    @staticmethod
    def getEstilosMusicais(idMusic: int):
        sql = f"SELECT em.nome FROM pertence_ao pa JOIN estilo_musical em ON em.id=pa.id_estilo_musical WHERE pa.id_musica={idMusic}"

        query_ans = DBConnection.query(sql, True)
        if query_ans == -1:
            return False
        return query_ans


    @staticmethod
    def getEvaluatedAndNotEvaluatedMusics(idUser: int):
        user = Usuario.where({"id": idUser})
        if user == False:
            return False
        musicas = Musica.classifyMusic(idUser)
        if musicas == False:
            return False
        musicas_avaliadas = musicas[0]
        musicas_nao_avaliadas = musicas[1]
        avaliadas = []
        nao_avaliadas = []

        for musica_avaliada in musicas_avaliadas:
            musica = musica_avaliada[0]
            musica['evaluation'] = 'L' if musica_avaliada[1] else 'D'
            musica['artista'] = [artista[0] for artista in Musica.getArtistsName(musica['id'])]
            musica['estilo'] = [genero[0] for genero in Musica.getEstilosMusicais(musica['id'])]
            avaliadas.append(musica)

        for musica_nao_avaliada in musicas_nao_avaliadas:
            musica = musica_nao_avaliada
            musica['artista'] = [artista[0] for artista in Musica.getArtistsName(musica['id'])]
            musica['estilo'] = [genero[0] for genero in Musica.getEstilosMusicais(musica['id'])]
            nao_avaliadas.append(musica)

        return shuffle(avaliadas), shuffle(nao_avaliadas)