class Produto: #construtor
    def __init__(self, id, nome, valor,  Varejista):
        self.id = ''
        self.nome = ''
        self.valor = ''
        self.Varejista = '' #poderia tb só colocar o ID

    def getId(self): #retorna ID
        id = str(self.id)
        return id
    
    def getVarejista(self): #retorna Varejista
        Varejista = self.Varejista
        return Varejista