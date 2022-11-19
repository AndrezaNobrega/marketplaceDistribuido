class MarketPlace: #construtor
    def __init__(self, listaVarejistas, nome):
        self.nome = '' #troquei endereço por nome
        self.listaVarejistas = [] #lista de objeto Varejistas    
        self.relogioVetorial = [] #irá se inicializar vazia

    def getNome(self): #retorna nome
        nome = str(self.nome)
        return nome
        
    def appendVarejista(self, Varejista): #add um varejista
        listaVarejistas = self.listaVarejistas.append(Varejista)
        return listaVarejistas
    
    def setRelogioVetorial(self, relogioVetorial): #quando formos modificar o relógio vetorial
        self.relogioVetorial = relogioVetorial
        return relogioVetorial
    
    def novaLoja(self):#toda vez que uma loja for inicializada, daremos append 0 no relogógio vetorial
        self.relogioVetorial = self.relogioVetorial.append(0)
    