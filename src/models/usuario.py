from ..services.connect import DBConnection

class Usuario:

    # inicializa um objeto do tipo Usuario com os dados iniciais dados
    def __init__(self):
        #TODO
        pass

    # troca os valores dos atributos
    def change_values(self, data: dict):
        for key in data.keys():
            if key == 'id' and not self.__isnew:
                self.id = data[key]
            elif key == "nome":
                self.nome = data[key]
            elif key == "email":
                self.email = data[key]
            elif key == "senha":
                if self.__isnew:
                    self.senha = self.encrypt_password(data[key])
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
        #TODO
        pass

    # faz a codificacao da senha
    def encrypt_password(self, password: str):
        #TODO
        pass
    
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
            return -1

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

if __name__ == '__main__':
    for u in Usuario.where({"nome": "'aurelio'"}):
        print(u.id)
        print(u.nome)
        print(u.email)
        print(u.senha)
        print(u.data_nascimento)
        print(u.foto_perfil)

        print()