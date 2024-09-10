from ..services.connect import DBConnection
from ..models.usuario import Usuario
from datetime import datetime

class Evento:

    # Inicializa um objeto do tipo Evento com os dados iniciais
    def __init__(self):
        self.id = None
        self.nome = None
        self.descricao = None
        self.localizacao = None
        self.data_realizacao = None
        self.imagem = None
        self.__setIsNew(True)

    # Troca os valores dos atributos
    def change_values(self, data:dict):
        for key in data.keys():
            if key == 'id' and not self.__isnew:
                self.id = data[key]
            elif key == "nome":
                self.nome = data[key]
            elif key == "descricao":
                self.descricao = data[key]
            elif key == "localizacao":
                self.localizacao = data[key]
            elif key == "data_realizacao":
                self.data_realizacao = data[key]
            elif key == "imagem":
                self.imagem = data[key]

    # metodo privado pra dizer se uma instancia desse objeto foi criada pelo programa (True) ou se foi importada do BD (False)
    def __setIsNew(self, val: bool):
        self.__isnew = val

    # salva o objeto evento no banco de dados com os atributos que ele tem
    def save(self):
        if self.nome == None:
            self.nome = "NULL"
        elif self.nome[0] != "'" and self.nome[-1] != "'":
            self.nome = f"'{self.nome}'"
        if self.descricao == None:
            self.descricao = "NULL"
        elif self.descricao[0] != "'" and self.descricao[-1] != "'":
            self.descricao = f"'{self.descricao}'"
        if self.localizacao == None:
            self.localizacao = "NULL"
        elif self.localizacao[0] != "'" and self.localizacao[-1] != "'":
            self.localizacao = f"'{self.localizacao}'"
        if self.data_realizacao == None:
            self.data_realizacao = "NULL"
        elif self.data_realizacao[0] != "'" and self.data_realizacao[-1] != "'":
            self.data_realizacao = f"'{self.data_realizacao}'"
        if self.imagem == None:
            self.imagem = "NULL"
        elif self.imagem[0] != "'" and self.imagem[-1] != "'":
            self.imagem = f"'{self.imagem}'"
        

        if self.__isnew:
            sql = f"INSERT INTO evento (nome, descricao, localizacao, data_realizacao, imagem) VALUES ({self.nome}, {self.descricao}, {self.localizacao}, {self.data_realizacao}, {self.imagem})"
        else:
            sql = f"UPDATE usuario SET nome={self.nome}, descricao={self.descricao}, localizacao={self.senha}, localizacao={self.localizacao}, data_realizacao={self.data_realizacao}, imagem={self.imagem} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False
        
        self.__setIsNew(False)
        
        return True
    
    # Retorna todos as instancias no BD que possuem os dados especificados
    # Lembra de colocar as aspas simples em volta dos valores que sao text la no BD
    @staticmethod
    def where(data: dict):
        sql = "SELECT id, nome, descricao, localizacao, data_realizacao, imagem FROM evento "
        # se coloca parenteses entre os nomes da coluna o retorno eh uma string que quebra o codigo, n entendi direito o pq :)

        if len(data.keys()) != 0:
            key0 = next(iter(data))
            sql += f" WHERE {key0}={data[key0]}"

            for key in data:
                if key == key0:
                    continue
                
                sql += f" AND {key}={data[key]}"
        
        sql += "ORDER BY data_realizacao ASC"

        lines = DBConnection.query(sql, True)

        if lines == -1:
            return False

        obj = []
        for inst in lines:
            new_obj = Evento()
            new_obj.__setIsNew(False)
            with open (f"images/imagem_evento_{inst[0]}.jpg", 'wb') as arquivo:
                arquivo.write(inst[5])
            read_data = {"id": inst[0], "nome": inst[1], "descricao": inst[2], "localizacao": inst[3], "data_realizacao": inst[4], "imagem": f'images/imagem_evento_{inst[0]}.jpg'}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj
    

    # Relacionamento participou_de com o usuario

    @staticmethod
    def findParticipouDe(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"SELECT * FROM participou_de WHERE id_usuario={idUser} AND id_evento={idEvent}"
    
        query = DBConnection.query(sql, True)

        if query == -1:
            return False
        return query
    
    @staticmethod
    def addParticipouDe(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"INSERT INTO participou_de (id_usuario, id_evento) VALUES ({idUser}, {idEvent})"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def editParticipouDe(idUser: int, idEvent: int):
        user = Usuario.where({"id": id})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"UPDATE participou_de SET id_usuario={idUser} WHERE id_usuario={idUser} AND id_evento={idEvent}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def deleteParticipouDe(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"DELETE FROM participou_de WHERE id_usuario={idUser} AND id_evento={idEvent}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    # Relacionamento tem_interesse com o usuario

    @staticmethod
    def findTemInteresse(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False
          
        sql = f"SELECT * FROM tem_interesse WHERE id_usuario={idUser} AND id_evento={idEvent}"
    
        query = DBConnection.query(sql, True)

        if query == -1:
            return False
        return query
    
    @staticmethod
    def addTemInteresse(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"INSERT INTO tem_interesse (id_usuario, id_evento) VALUES ({idUser}, {idEvent})"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def editTemInteresse(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False

        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"UPDATE tem_interesse SET id_usuario={idUser} WHERE id_usuario={idUser} AND id_evento={idEvent}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def deleteTemInteresse(idUser: int, idEvent: int):
        user = Usuario.where({"id": idUser})

        if user == False:
            return False
    
        event = Evento.where({"id": idEvent})

        if event == False:
            return False

        sql = f"DELETE FROM tem_interesse WHERE id_usuario={idUser} AND id_evento={idEvent}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def getArtists(idEvento: int):
        sql = f"SELECT a.nome FROM artista a JOIN participa p ON a.id=p.id_artista WHERE p.id_evento={idEvento}"

        query_ans = DBConnection.query(sql, True)
        if query_ans == -1:
            return False
        return query_ans
    
    @staticmethod
    def getEstilosMusicais(idEvento: int):
        sql = f"SELECT em.nome FROM evento_tem_estilo_musical eem JOIN estilo_musical em ON em.id=eem.id_estilo_musical WHERE eem.id_evento={idEvento}"

        query_ans = DBConnection.query(sql, True)
        if query_ans == -1:
            return False
        return query_ans
    
    @staticmethod
    def get_eventos(idUsuario: int, conexoes: list[dict]):
        eventos = Evento.where({})
        if eventos == False:
            return False
        
        eventos_dict = []
        for evento in eventos:
            evento = evento.__dict__
            evento["estilos"] = [estilo[0] for estilo in Evento.getEstilosMusicais(evento["id"])]
            evento["artistas"] = [artista[0] for artista in Evento.getArtists(evento["id"])]
            if evento["data_realizacao"] >= datetime.now():
                evento["conexoes_interessadas"] = []
                for conexao in conexoes:
                    interesse = Evento.findTemInteresse(conexao["id"], evento["id"])
                    if interesse == False:
                        return False
                    if len(interesse) == 1:
                        evento["conexoes_interessadas"].append(conexao)
                status = Evento.findTemInteresse(idUsuario, evento["id"])
                if status == False:
                    return False
                if len(status) == 1:
                    evento["status"] = "I"
                else:
                    evento["status"] = "N"
                
            else:
                evento["conexoes_foram"] = []
                for conexao in conexoes:
                    participacao = Evento.findParticipouDe(conexao["id"], evento["id"])
                    if participacao == False:
                        return False
                    if len(participacao) == 1:
                        evento["conexoes_foram"].append(conexao)
                status = Evento.findParticipouDe(idUsuario, evento["id"])
                if status == False:
                    return False
                if len(status) == 1:
                    evento["status"] = "P"
                else:
                    evento["status"] = "N"
            
            eventos_dict.append(evento)
        
        return eventos_dict