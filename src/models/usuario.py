from ..services.connect import DBConnection

class Usuario:

    # inicializa um objeto do tipo Usuario com os dados iniciais dados
    def __init__(self):
        #TODO
        pass

    # troca os valores dos atributos
    def change_values(self, data: dict):
        #TODO
        pass

    # salva o objeto usuario no banco de dados com os atributos que ele tem
    def save(self):
        #TODO
        pass

    # faz a codificacao da senha
    def encrypt_password(self):
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

        obj = []
        for inst in lines:
            new_obj = Usuario()
            read_data = {"id": inst[0], "nome": inst[1], "email": inst[2], "senha": inst[3], "data_nascimento": inst[4], "foto_perfil": inst[5]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj

    # apaga as instancias no BD com aqueles dados
    @staticmethod
    def delete(data: dict):
        #TODO? nem sei se eh bom fazer esse metodo
        pass

if __name__ == '__main__':
    print(Usuario.where({"nome": "'aurelio'"}))