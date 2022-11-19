class Varejista: #construtor
    def __init__(self, id):
        self.id = ''
        self.listaProdutos = []

    def getId(self): #retorna ID
        id = str(self.id)
        return id
    
    def appendVarejista(self, Produto): #add um Produto 
        listaProdutos = self.listaProdutos.append(Produto)
        return listaProdutos