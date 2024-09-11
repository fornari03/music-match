from ..services.connect import DBConnection
from ..utils.encrypt import encrypt_password

class Usuario:

    # inicializa um objeto do tipo Usuario com os dados iniciais dados
    def __init__(self):
        self.id = None
        self.nome = None
        self.email = None
        self.senha = None
        self.data_nascimento = None
        self.foto_perfil = None
        self.__setIsNew(True)

    # troca os valores dos atributos
    def change_values(self, data: dict):
        """
        Metodo para mudar os valores do usuario para os valores passados no dicionario
        """
        for key in data.keys():
            # tem que ter + condicao pro id, nem sei se eh bom deixar mudar id
            if key == 'id' and not self.__isnew:
                self.id = data[key]
            elif key == "nome":
                self.nome = data[key]
            elif key == "email":
                self.email = data[key]
            elif key == "senha":
                if self.__isnew:
                    self.senha = encrypt_password(data[key])
                else:
                    self.senha = data[key]
            elif key == "data_nascimento":
                self.data_nascimento = data[key]
            elif key == "foto_perfil":
                self.foto_perfil = data[key]
            elif key == "nova_senha":
                self.senha = encrypt_password(data[key])
    
    # metodo privado pra dizer se uma instancia desse objeto foi criada pelo programa (True) ou se foi importada do BD (False)
    def __setIsNew(self, val: bool):
        """
        Método privado pra dizer se uma instancia desse objeto foi criada pelo programa (True) ou se foi importada do BD (False)
        """
        self.__isnew = val

    # salva o objeto usuario no banco de dados com os atributos que ele tem
    def save(self):
        """
        Metodo para salvar o usuario no banco de dados
        """
        str_nasc = ""
        str_senha = ""
        if self.nome == None:
            self.nome = "NULL"
        elif self.nome[0] != "'" and self.nome[-1] != "'":
            self.nome = f"'{self.nome}'"
        if self.email == None:
            return False
        elif self.email[0] != "'" and self.email[-1] != "'":
            self.email = f"'{self.email}'"
        if self.senha == None:
            self.senha = "NULL"
        elif self.senha[0] != "'" and self.senha[-1] != "'":
            str_senha = f"'{self.senha}'"
        else:
            str_senha = self.senha
        if self.data_nascimento == None:
            self.data_nascimento = "NULL"
        else:
            str_nasc = "'" + self.data_nascimento.strftime("%Y-%m-%d") + "'"
        if self.foto_perfil == None:
            self.foto_perfil = "NULL"

        if self.__isnew:
            sql = f"INSERT INTO usuario (nome, email, senha, data_nascimento, foto_perfil) VALUES ({self.nome}, {self.email}, {str_senha}, {str_nasc}, {self.foto_perfil})"
        else:
            sql = f"UPDATE usuario SET nome={self.nome}, email={self.email}, senha={str_senha}, data_nascimento={str_nasc}, foto_perfil={self.foto_perfil} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False
        
        self.__setIsNew(False)
        
        return True
    
    # retorna todos as instancias no BD que possuem os dados especificados
    # lembra de colocar as aspas simples em volta dos valores que sao text la no BD
    @staticmethod
    def where(data: dict):
        """
        Metodo para buscar usuarios no banco de dados
        """
        sql = "SELECT id, nome, email, senha, data_nascimento, foto_perfil FROM usuario"
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
            new_obj = Usuario()
            new_obj.__setIsNew(False)
            read_data = {"id": inst[0], "nome": inst[1], "email": inst[2], "senha": inst[3], "data_nascimento": inst[4], "foto_perfil": inst[5]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj

    # apaga as instancias no BD com aqueles dados
    @staticmethod
    def delete(idUser: int):
        """
        Metodo para deletar um usuario do banco de dados
        """
        return DBConnection.delete_user(idUser)
    
    # metodos CRUD pra rede social do usuario de email dado lembrando que o email eh unico para cada usuario
    # socMed = qual a rede Social
    # userSocMed = usuario naquela rede social

    @staticmethod
    def findSocialMedia(id: int):
        """
        Busca as redes sociais de um usuario
        """
        user = Usuario.where({"id": id})

        if user == False:
            return False

        sql = f"SELECT rede_social, usuario_rede_social FROM redes_sociais WHERE id_usuario={id}"

        data = DBConnection.query(sql, True)
        if data == -1:
            return False
        return data    
    
    @staticmethod
    def addSocialMedia(id: int, socMed: str, userSocMed: str):
        """
        Adiciona uma rede social a um usuario
        """
        user = Usuario.where({"id": id})

        # deveria ter um check bonitinho pra ver se tem as aspas simples, mas fazer o que

        if user == False:
            return False

        sql = f"INSERT INTO redes_sociais(id_usuario, rede_social, usuario_rede_social) VALUES ('{id}', '{socMed}', '{userSocMed}')"

        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    @staticmethod
    def editSocialMediaUsername(id: int, socMed: str, userSocMed: str):
        """
        Atualiza o user de uma rede social de um usuario
        """
        user = Usuario.where({"id": id})

        if user == False:
            return False

        sql = f"UPDATE redes_sociais SET usuario_rede_social={userSocMed} WHERE id_usuario={id} AND rede_social='{socMed}'"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    @staticmethod
    def deleteSocialMedia(id: int, socMed: str):
        """
        Deleta uma rede social de um usuario
        """
        user = Usuario.where({"id": id})

        if user == False:
            return False

        sql = f"DELETE FROM redes_sociais WHERE id_usuario={id} AND rede_social='{socMed}'"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # metodo que cria uma relacao indicando que dois usuarios se conectaram, passando o email dos 2
    # (a gente pode mudar pra id, dependendo de como ficar la no front)
    @staticmethod
    def connect(id1: int, id2: int):
        """
        Cria uma conexao entre dois usuarios
        """
        # nao deixa conectar consigo msm
        if (id1 == id2):
            return False        

        user1 = Usuario.where({"id": id1})
        user2 = Usuario.where({"id": id2})

        if user1 == False or user2 == False:
            return False

        sql = f"INSERT INTO conecta_com (id_usuario_1, id_usuario_2) VALUES ({id1}, {id2})"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # metodo que remove a relacao entre dois usuarios
    @staticmethod
    def disconnect(id1: int, id2: int):
        """
        Deleta a conexao entre dois usuarios
        """
        user1 = Usuario.where({"id": id1})
        user2 = Usuario.where({"id": id2})

        if user1 == False or user2 == False:
            return False

        sql = f"DELETE FROM conecta_com WHERE (id_usuario_1={id1} OR id_usuario_1={id2}) AND (id_usuario_2={id1} OR id_usuario_2={id2})"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # encontra as conexoes de um usuario
    # da pra gente fazer um join table pra gente retornar os emails, mas por enquanto so retorna os ids
    @staticmethod
    def findConnections(id: int):
        """
        Busca as conexões de um usuario
        """
        user = Usuario.where({"id": id})

        if user == False:
            return False

        sql = f"""SELECT u.id, u.nome, music_match.sintonia FROM calcular_sintonia_musical({id}) music_match JOIN usuario u ON music_match.id_usuario=u.id
                    WHERE music_match.id_usuario IN (
                        SELECT 
                            CASE 
                            WHEN {id}=cc.id_usuario_1 THEN cc.id_usuario_2 
                            ELSE cc.id_usuario_1 
                            END 
                        FROM conecta_com cc WHERE cc.id_usuario_1={id} OR cc.id_usuario_2={id})
                    ORDER BY music_match.sintonia DESC"""
        
        query_ret = DBConnection.query(sql, True)
        if query_ret == -1:
            return False
        return query_ret
    

    @staticmethod
    def findNotConnections(id: int):
        """
        Busca os usuários que não são conexões de um usuário
        """
        user = Usuario.where({"id": id})

        if user == False:
            return False

        sql = f"""SELECT u.id, u.nome, music_match.sintonia FROM calcular_sintonia_musical({id}) music_match JOIN usuario u ON music_match.id_usuario=u.id
                    WHERE music_match.id_usuario NOT IN (
                        SELECT 
                            CASE 
                            WHEN {id}=cc.id_usuario_1 THEN cc.id_usuario_2 
                            ELSE cc.id_usuario_1 
                            END 
                        FROM conecta_com cc WHERE cc.id_usuario_1={id} OR cc.id_usuario_2={id})
                    ORDER BY music_match.sintonia DESC"""
        
        query_ret = DBConnection.query(sql, True)
        if query_ret == -1:
            return False
        return query_ret
    
    @staticmethod
    def get_connections(id: int):
        """
        Retorna os usuarios conectados a um usuario
        """
        user = Usuario.where({"id": id})
        if user == False:
            return False
        
        otherUsers = Usuario.findConnections(f"'{id}'")
        if otherUsers == False:
            return False
        
        otherDicts = []
        for otherUser in otherUsers:
            sintonia = otherUser[2]
            otherUser = Usuario.others_to_dict(otherUser[0])
            otherUser["sintonia"] = sintonia
            sql = f"""SELECT ar.nome FROM usuario_avalia_musica av
                        JOIN artista_tem_musica atm ON av.id_musica = atm.id_musica
                        JOIN artista ar ON atm.id_artista = ar.id
                        WHERE av.id_usuario = {otherUser['id']} 
                              AND av.feedback = TRUE
                        GROUP BY ar.id, ar.nome
                        ORDER BY COUNT(*) DESC
                        LIMIT 3;
                        """
            artistas = DBConnection.query(sql, True)
            if artistas == -1:
                return False
            otherUser["artists"] = [artista[0] for artista in artistas]

            sql = f"""SELECT em.nome FROM usuario_avalia_musica av
                        JOIN pertence_ao pa ON av.id_musica = pa.id_musica
                        JOIN estilo_musical em ON pa.id_estilo_musical = em.id
                        WHERE av.id_usuario = {otherUser['id']} 
                              AND av.feedback = TRUE
                        GROUP BY em.id, em.nome
                        ORDER BY COUNT(*) DESC
                        LIMIT 3;
                        """
            gosto_musical = DBConnection.query(sql, True)
            if gosto_musical == -1:
                return False
            otherUser["musical_taste"] = [genero[0] for genero in gosto_musical]

            otherDicts.append(otherUser)
        return otherDicts
    
    @staticmethod
    def get_not_connections(id: int):
        """
        Retorna os usuarios que não são conectados a um usuario
        """
        user = Usuario.where({"id": id})
        if user == False:
            return False
        
        otherUsers = Usuario.findNotConnections(f"'{id}'")
        if otherUsers == False:
            return False
        
        otherDicts = []
        for otherUser in otherUsers:
            sintonia = otherUser[2]
            otherUser = Usuario.others_to_dict(otherUser[0])
            otherUser["sintonia"] = sintonia
            sql = f"""SELECT ar.nome FROM usuario_avalia_musica av
                        JOIN artista_tem_musica atm ON av.id_musica = atm.id_musica
                        JOIN artista ar ON atm.id_artista = ar.id
                        WHERE av.id_usuario = {otherUser['id']} 
                              AND av.feedback = TRUE
                        GROUP BY ar.id, ar.nome
                        ORDER BY COUNT(*) DESC
                        LIMIT 3;
                        """
            artistas = DBConnection.query(sql, True)
            if artistas == -1:
                return False
            otherUser["artists"] = [artista[0] for artista in artistas]

            sql = f"""SELECT em.nome FROM usuario_avalia_musica av
                        JOIN pertence_ao pa ON av.id_musica = pa.id_musica
                        JOIN estilo_musical em ON pa.id_estilo_musical = em.id
                        WHERE av.id_usuario = {otherUser['id']} 
                              AND av.feedback = TRUE
                        GROUP BY em.id, em.nome
                        ORDER BY COUNT(*) DESC
                        LIMIT 3;
                        """
            gosto_musical = DBConnection.query(sql, True)
            if gosto_musical == -1:
                return False
            otherUser["musical_taste"] = [genero[0] for genero in gosto_musical]

            otherDicts.append(otherUser)
        return otherDicts
    
    @staticmethod
    def others_to_dict(id: int):
        """
        Transforma parte de um usuario em um dicionario
        """
        user = Usuario.where({"id": id})[0]
        return {
            "id": user.id,
            "nome": user.nome,
            "redes_sociais": Usuario.findSocialMedia(f"'{user.id}'"),

        }