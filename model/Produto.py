class Produto: #construtor
    def __init__(self, id, Varejista):
        self.id = ''
        self.Varejista = Varejista #poderia tb só colocar o ID

    def getId(self): #retorna ID
        id = str(self.id)
        return id
    
    def getVarejista(self): #retorna Varejista
        Varejista = self.Varejista
        return Varejista