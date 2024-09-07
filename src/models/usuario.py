from services.connect import DBConnection

class Usuario:

    # inicializa um objeto do tipo Usuario com os dados iniciais dados
    def __init__(self):
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
    @staticmethod
    def where(dados: dict):
        #TODO
        pass

    # apaga as instancias no BD com aqueles dados
    @staticmethod
    def delete(dados: dict):
        #TODO? nem sei se eh bom fazer esse metodo
        pass