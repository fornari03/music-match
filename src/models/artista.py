from ..services.connect import DBConnection

class Artista:

    def __init__(self):
        self.id = None
        self.nome = None
        self.foto = None
        self.__isNew = True

    def change_values(self, data: dict):
        for key in data.keys():
            if key == 'id':
                self.id = data[key]
            elif key == 'nome':
                self.nome = data[key]
            elif key == 'foto':
                self.foto = data[key]

    # se eh uma nova instancia da problema do self.id nao ficar atualizado
    def save(self):
        if self.id == None:
            self.id = "NULL"
        if self.nome == None:
            self.nome = "NULL"
        if self.foto == None:
            self.foto = "NULL"

        sql = ""
        if self.__isNew:
            sql = f"INSERT INTO artista (nome, foto) VALUES ({self.nome}, {self.foto})"
        else:
            sql = f"UPDATE artista SET nome={self.nome}, foto={self.foto} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False
        return True

    @staticmethod
    def where(data: dict):
        #TODO
        pass