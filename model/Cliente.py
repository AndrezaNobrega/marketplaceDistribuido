class Cliente: #construtor
    def __init__(self, id):
        self.id = ''
        self.carrinho = [] #lista de itens

    def getCarrinho(self): #retorna Carrinho
        carrinho = self.carrinho
        return carrinho

    def appendCarrinho(self, produto): #add um Produto 
        carrinho = self.carrinho.append(produto)
        return carrinho