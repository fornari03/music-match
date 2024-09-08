from ..services.connect import DBConnection
import Usuario

class Evento:

    # Inicializa um objeto do tipo Evento com os dados iniciais
    def __init__(self):
        self.id = None
        self.nome = None
        self.descricao = None
        self.localizacao = None
        self.data_realizacao = None
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

    # metodo privado pra dizer se uma instancia desse objeto foi criada pelo programa (True) ou se foi importada do BD (False)
    def __setIsNew(self, val: bool):
        self.__isnew = val

    # salva o objeto evento no banco de dados com os atributos que ele tem
    def save(self):
        if self.nome == None:
            self.nome = "NULL"
        if self.descricao == None:
            self.descricao = "NULL"
        if self.localizacao == None:
            self.localizacao = "NULL"
        if self.data_realizacao == None:
            self.data_realizacao = "NULL"
        

        if self.__isnew:
            sql = f"INSERT INTO evento (nome, descricao, localizacao, data_realizacao) VALUES ({self.nome}, {self.descricao}, {self.localizacao}, {self.data_realizacao})"
        else:
            sql = f"UPDATE usuario SET nome={self.nome}, descricao={self.descricao}, localizacao={self.senha}, localizacao={self.localizacao}, data_realizacao={self.data_realizacao} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False
        
        self.__setIsNew(False)
        
        return True
    
    # Retorna todos as instancias no BD que possuem os dados especificados
    # Lembra de colocar as aspas simples em volta dos valores que sao text la no BD
    @staticmethod
    def where(data: dict):
        sql = "SELECT id, nome, descricao, localizacao, data_realizacao FROM evento"
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
            new_obj = Evento()
            new_obj.__setIsNew(False)
            read_data = {"id": inst[0], "nome": inst[1], "localizacao": inst[2], "data_realizacao": inst[3]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj
    

    # Relacionamento participou_de com o usuario

    @staticmethod
    def findParticipouDe(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"SELECT * FROM participou_de WHERE id_usuario={idUser} AND id_evento={self.id}"
    
        query = DBConnection.query(sql, True)

        if query == -1:
            return False
        return query
    
    @staticmethod
    def addParticipouDe(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"INSERT INTO participou_de (id_usuario, id_evento) VALUES ({idUser}, {self.id})"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def editParticipouDe(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"UPDATE participou_de SET id_usuario={idUser} WHERE id_usuario={idUser} AND id_evento={self.id}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def deleteParticipouDe(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"DELETE FROM participou_de WHERE id_usuario={idUser} AND id_evento={self.id}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    # Relacionamento tem_interesse com o usuario

    @staticmethod
    def findTemInteresse(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"SELECT * FROM tem_interesse WHERE id_usuario={idUser} AND id_evento={self.id}"
    
        query = DBConnection.query(sql, True)

        if query == -1:
            return False
        return query
    
    @staticmethod
    def addTemInteresse(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"INSERT INTO tem_interesse (id_usuario, id_evento) VALUES ({idUser}, {self.id})"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def editTemInteresse(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"UPDATE tem_interesse SET id_usuario={idUser} WHERE id_usuario={idUser} AND id_evento={self.id}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    
    @staticmethod
    def deleteTemInteresse(self, email: str):
        user = Usuario.where({"email": email})

        if user == False:
            return False

        idUser = user[0].id

        sql = f"DELETE FROM tem_interesse WHERE id_usuario={idUser} AND id_evento={self.id}"

        query = DBConnection.query(sql, False)

        if query == -1:
            return False
        return True
    