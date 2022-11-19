class MarketPlace: #construtor
    def __init__(self, listaVarejistas, nome):
        self.nome = '' #troquei endereço por nome
        self.listaVarejistas = [] #lista de objeto Varejistas      


    def getNome(self): #retorna nome
        nome = str(self.nome)
        return nome

    def appendVarejista(self, Varejista): #add um varejista
        listaVarejistas = self.listaVarejistas.append(Varejista)
        return listaVarejistas