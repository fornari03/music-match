from ..services.connect import DBConnection

class EstiloMusical:
    
    def __init__(self):
        self.id = None
        self.nome = None
        self.__isNew = True

    def change_values(self, data: dict):
        for key in data:
            if key == 'id':
                self.id = data[key]
            elif key == 'nome':
                self.nome = data[key]

    def save(self):
        if self.nome == None:
            self.nome = "NULL"
        elif self.nome[0] != "'" and self.nome[-1] != "'":
            self.nome = f"'{self.nome}'"

        if self.__isNew:
            sql = f"INSERT INTO estilo_musical (nome) VALUES ({self.nome})"
        else:
            sql = f"UPDATE estilo_musical SET nome={self.nome} WHERE id={self.id}"

        if DBConnection.query(sql, False) == -1:
            return False        
        return True

    @staticmethod
    def where(data: dict):
        sql = "SELECT id, nome FROM estilo_musical"
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
            new_obj = EstiloMusical()
            new_obj.__isNew = False
            read_data = {"id": inst[0], "nome": inst[1]}
            new_obj.change_values(read_data)

            obj.append(new_obj)
            
        return obj
