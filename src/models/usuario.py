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
    
    # metodo privado pra dizer se uma instancia desse objeto foi criada pelo programa (True) ou se foi importada do BD (False)
    def __setIsNew(self, val: bool):
        self.__isnew = val

    # salva o objeto usuario no banco de dados com os atributos que ele tem
    def save(self):
        if self.nome == None:
            self.nome = "NULL"
        if self.email == None:
            return False
        if self.senha == None:
            self.senha = "NULL"
        if self.data_nascimento == None:
            self.data_nascimento = "NULL"
        if self.foto_perfil == None:
            self.foto_perfil = "NULL"

        if self.__isnew:
            sql = f"INSERT INTO usuario (nome, email, senha, data_nascimento, foto_perfil) VALUES ({self.nome}, {self.email}, {self.senha}, {self.data_nascimento}, {self.foto_perfil})"
        else:
            sql = f"UPDATE usuario SET nome={self.nome}, email={self.email}, senha={self.senha}, data_nascimento={self.data_nascimento}, foto_perfil={self.foto_perfil} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False
        
        self.__setIsNew(False)
        
        return True
    
    # retorna todos as instancias no BD que possuem os dados especificados
    # lembra de colocar as aspas simples em volta dos valores que sao text la no BD
    @staticmethod
    def where(data: dict):
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
    def delete(data: dict):
        sql = "DELETE FROM Usuario"
        
        if len(data.keys()) != 0:
            key0 = next(iter(data))
            sql += f" WHERE {key0}={data[key0]}"

            for key in data:
                if key == key0:
                    continue

                sql += f" AND {key}={data[key]}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    # metodos CRUD pra rede social do usuario de email dado lembrando que o email eh unico para cada usuario
    # socMed = qual a rede Social
    # userSocMed = usuario naquela rede social

    @staticmethod
    def findSocialMedia(email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"SELECT rede_social, usuario_rede_social FROM redes_sociais WHERE id_usuario={idUser}"

        data = DBConnection.query(sql, True)
        if data == -1:
            return False
        return data    
    
    @staticmethod
    def addSocialMedia(email: str, socMed: str, userSocMed: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"INSERT INTO redes_sociais(id_usuario, rede_social, usuario_rede_social) VALUES ({idUser}, {socMed}, {userSocMed})"

        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    @staticmethod
    def editSocialMediaUsername(email: str, socMed: str, userSocMed: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"UPDATE redes_sociais SET usuario_rede_social={userSocMed} WHERE id_usuario={idUser} AND rede_social={socMed}"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    @staticmethod
    def deleteSocialMedia(email: str, socMed: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"DELETE FROM redes_sociais WHERE id_usuario={idUser} AND rede_social={socMed}"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # metodo que cria uma relacao indicando que dois usuarios se conectaram, passando o email dos 2
    # (a gente pode mudar pra id, dependendo de como ficar la no front)
    @staticmethod
    def connect(email1: str, email2: str):
        # nao deixa conectar consigo msm
        if (email1 == email2):
            return False        

        user1 = Usuario.where({"email": email1})
        user2 = Usuario.where({"email": email2})

        if user1 == False or user2 == False:
            return False

        idUser1 = user1[0].id
        idUser2 = user2[0].id

        sql = f"INSERT INTO conecta_com (id_usuario1, id_usuario2) VALUES ({idUser1}, {idUser2})"
        if DBConnection.query(sql, False) == -1:
            return False
        return True
    
    # metodo que remove a relacao entre dois usuarios
    def connect(email1: str, email2: str):
        user1 = Usuario.where({"email": email1})
        user2 = Usuario.where({"email": email2})

        if user1 == False or user2 == False:
            return False

        idUser1 = user1[0].id
        idUser2 = user2[0].id

        sql = f"DELETE FROM conecta_com WHERE (id_usuario1={idUser1} OR id_usuario1={idUser2}) AND (id_usuario2={idUser1} OR id_usuario2={idUser2})"
        if DBConnection.query(sql, False) == -1:
            return False
        return True