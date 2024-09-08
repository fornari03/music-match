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
        sql = "SELECT id, nome, foto FROM artista"

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
            new_obj = Artista()
            new_obj.__isNew = False
            read_data = {"id": inst[0], "nome": inst[1], "foto": inst[2]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj