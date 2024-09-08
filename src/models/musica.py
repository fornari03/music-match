from ..services.connect import DBConnection

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
        if self.capa == None:
            self.capa = "NULL"
        if self.link_spotify == None:
            self.link_spotify = "NULL"

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

    @staticmethod
    def getArtists(idMusic: int):
        #TODO
        pass