from flask import Flask, jsonify, render_template, redirect, request, session, Response

from random import *
import json

from controller import eventController


# # Instantiate Flask object named app
app = Flask(__name__)
CLOCK = [0,0,0]
PORTA = int(input("PORTA="))
this_id = (PORTA-3030)
# NOME = input('Nome que deseja para a loja:')
# # Configure sessions
# Session(app)

# # db sqlite - será substituido pelo json de visualização 
# db = SQL( "sqlite:///data.db" )
DATABASE = 'bdMarketplace.json'



#TODO tela de cadastro de produtos 
#TODO colocar quantidade de cada produto no banco de dados
#TODO colocar as refs bootstrap nos arquivos p/ n depender da rede

#index
@app.route("/")
def index():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0

    # vai abrir o arquivo de  JSON visualização e mostrar todos os produtos que estão dispo 
    # Opening JSON file
    with open('produtos.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        camisas = json_object['produtos'] 
        
    #ele abre o carrinho
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 
        shopLen = len(shoppingCart)

    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    shirts = camisas
    shirtsLen = len(shirts)
    return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display)

#cadastro de produtos
#no BdMarketplace
#também atualizamos a propria galeria do marketplace
@app.route('/cadastroProdutos/')
def form():
    return render_template('cadastroProdutos.html') 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':

        time = request.form['team']
        quantidade = request.form['quantidade']
        preco = request.form['price']
        pais = request.form['Country']
        continente = request.form['Continent']
        tipo = request.form['kind']
        print (time + preco + pais + continente + tipo)

        id = str(randint(1000,9999)) #gera ID
        produto = {"continent": continente,
                    "quantidade": quantidade,
                    "id": id,
                    "image": "brasil.jpg",
                    "kind": tipo,
                    "onSale": 0,
                    "onSalePrice": float(preco),
                    "price": float(preco),
                    "team": time
        }

        # function to add to JSON
        def write_json(new_data, filename):
            with open(filename,'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data['produtos'].append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
        
        write_json(produto, 'bdMarketplace.json') #escrevendo o novo produto no BD  
        write_json(produto, 'produtos.json') #envia para a sua própria galeria 
        #-----------------------------------------------------------------------------------------------
        #aqui tem que enviar uma mensagem para sincronizar com os outros marketplaces
        #--------------------------------------------------------------------------------------------------------------------
        res = eventController.addEvent(produto)
        #para recarregar a página index ao escrever a nova camisa no db
        shoppingCart = []
        shopLen = len(shoppingCart)
        totItems, total, display = 0, 0, 0

        # vai abrir o arquivo de  JSON visualização e mostrar todos os produtos que estão dispo 
        # Opening JSON file
        with open('produtos.json', 'r') as openfile:    
            # Reading from json file
            json_object = json.load(openfile)
            camisas = json_object['produtos'] 
            
        #abre o arquivo do carrinho
        with open('carrinho.json', 'r') as openfile:    
            # Reading from json file
            json_object = json.load(openfile)
            shoppingCart = json_object['carrinho'] 
            shopLen = len(shoppingCart)

        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        shirts = camisas
        shirtsLen = len(shirts)

        return render_template("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session)

#para pesquisar na galeria.
#aqui é possível pesquisar os produtos disponíveis em todos os 
#marketplaces
@app.route('/pesquisar/')
def pesquisa():
    return render_template('pesquisa.html') 
@app.route('/pesquisa/', methods = ['POST', 'GET'])
def resultadoPesquisa():
    if request.method == 'POST':
        pesquisa = request.form['pesquisa']


        with open('produtos.json', 'r') as openfile:    
        # Reading from json file
            json_object = json.load(openfile)
        camisas = json_object['produtos'] 
        print(camisas)

        # Select info of selected shirt from database
        def buscarCamisa(camisas, pesquisa):
            pesquisaR = []
            for camisa in camisas:
                print('for',camisa)
                if camisa['team'] == pesquisa:
                    print('team')
                    pesquisaR.append(camisa)
                elif camisa['kind'] == pesquisa:
                    pesquisaR.append(camisa)
                elif camisa['continent'] == pesquisa:
                    pesquisaR.append(camisa)
            return pesquisaR
        pesquisaResultado = buscarCamisa(camisas, pesquisa)
        print(pesquisaResultado)
    shirts = pesquisaResultado
    shirtsLen = len(shirts)
    #inicializando as variaveis 
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0

    #abre o arquivo do carrinho
    #para retornar para o indice
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 
        shopLen = len(shoppingCart)

    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Render filtered view
    return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session)
 
#para inserir no carrinho
#está funcionando
@app.route("/buy/")
def buy():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    #quantidade inserida pelo usuário
    qty = int(request.args.get('quantity'))
    # id da camisa selecionada
    id = int(request.args.get('id'))

    # abre o dataBase para que a pesquisa seja feita
    with open('produtos.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        camisas = json_object['produtos'] 

    # Select info of selected shirt from database
    def buscarCamisa(camisas, id):
        for camisa in camisas:
            if camisa['id'] == id:
                goods = camisa
        return camisa
    goods = buscarCamisa(camisas, id)

    # Extract values from selected shirt record
    # Check if shirt is on sale to determine price
    if(goods["onSale"] == 1):
        price = goods["onSalePrice"]
    else:
        price = goods["price"]
    team = goods["team"]
    image = goods["image"]
    subTotal = qty * price

    # Insert selected shirt into shopping cart
    #cria o novo produto 
    produto = {"id": id,
                "SUM(qty)": qty,
                "team": team,
                "image": image,
                "price": price,
                "SUM(subTotal)": subTotal

    }
    # function to add to JSON
    def inserirProduto(new_data, filename='carrinho.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data['carrinho'].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        
    inserirProduto(produto) #escrevendo o novo produto no BD  
    
    #recarrega carrinho
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 

    shopLen = len(shoppingCart)
    # Rebuild shopping cart

    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Select all shirts for home page view
    with open('produtos.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shirts = json_object['produtos'] 

    shirtsLen = len(shirts)
    # Go back to home page
    return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session)



#update do carrinho
@app.route("/update/")
def update():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    #recebe quantidade e id das camisas selecionadas
    qty = int(request.args.get('quantity'))
    id = int(request.args.get('id'))

    #remove produto
    with open('carrinho.json', 'r') as json_file:    
        # Reading from json file
        json_object = json.load(json_file)
    tamanho = len(json_object['carrinho'])
    camisas = json_object
    for i in range(tamanho):	
        if camisas['carrinho'][i]['id'] == id:
            camisas['carrinho'].pop(i)
            break
    #reescrevebd
    open("carrinho.json", "w").write(json.dumps(camisas, indent=4))


    # abre o dataBase para que a pesquisa seja feita
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        camisas = json_object['carrinho'] 

    # Select info of selected shirt from database
    def buscarCamisa(camisas, id):
        for camisa in camisas:
            if camisa['id'] == id:
                goods = camisa
        return camisa
    goods = buscarCamisa(camisas, id)
    # Extract values from selected shirt record
    price = goods["price"]
    team = goods["team"]
    image = goods["image"]
    subTotal = qty * price
    # Insert selected shirt into shopping cart
   # Insert selected shirt into shopping cart
    #cria o novo produto 
    produto = {"id": id,
                "SUM(qty)": qty,
                "team": team,
                "image": image,
                "price": price,
                "SUM(subTotal)": subTotal

    }
    # function to add to JSON
    def inserirProduto(new_data, filename='carrinho.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data['carrinho'].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        
    inserirProduto(produto) #escrevendo o novo produto no BD  

     #recarrega carrinho
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 

    shopLen = len(shoppingCart)
    # Rebuild shopping cart

    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Go back to cart page
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

def ler_json(arquivo, atributo):
    with open(arquivo, 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        json_file = json_object[atributo]
    return json_file

def compraAutorizada(list):
    for it in range(0, len(list)):
        if (list[it]['res'] != 'OK'): 
            return False
    return True

def limparCarrinho():
    with open('carrinho.json', 'r') as openfile:
        json_object = json.load(openfile)
        json_object['carrinho'] = []
        json_file = json_object['carrinho']
    return json_file

def vector_compare(vector1,vector2):
    vector = [max(value) for value in zip(vector1,vector2)]
    return vector

# ---------------------------- funções de acesso ao db compartilhado -----------------------------------------------------

#quando marketplace efetua a compra
#essa parte ta dando erro pois puxa no carrinho o uid que fazia parte da sessão do ususário e tirei
#mas como n vamos utilizar, deixei dessa maneira msm, pra gente só ter uma base
@app.get("/checkout/")
def checkout():
    #   order = lista de dicts
    order = ler_json('carrinho.json', 'carrinho')
    # precisa enviar para todas as lojas a requisição
    CLOCK[this_id] += 1
    res = json.loads(eventController.orderEvent(order, clock=CLOCK,id=(PORTA-3030)))   # {"clock":clock,"res":res}
    print('res from eventController')
    print(type(res))
    print(res)
    # se todas as respostas foram OK, prossegue a compra
        # onde define se é ok ou não é no /compra do marketplace
    if (compraAutorizada(res['res'])):
        # Clear shopping cart
        limparCarrinho()
        # Redirect to home page
        return redirect('/')
    # se não, cancela a compra
    return ('<script>alert("A compra nao foi autorizada. Tente novamente mais tarde.")</script>')

# Rota por onde são recebidas as solicitações para compra (acesso ao DB)
@app.post("/compra")
def compra():
    # deve verificar se os itens da compra pertencem ao BD LOCAL
    print(f'this_id={this_id}')
    global CLOCK
    CLOCK[this_id] += 1
    dblocal = ler_json(DATABASE, 'produtos')    # lista de dict
    req = json.loads(request.get_json()) # {"clock":[clock],"items":[items]}
    print('req')
    print(type(req))
    print(req)
    res = {"clock":[], "res":[]}
    for item in req["items"]:
        for product in dblocal:
            if ((item['id'] == product['id']) & (vector_compare(CLOCK, req['clock']) > CLOCK)):
                # mapear a lista dblocal['produtos'] e decrementar a quantidade da compra do estoque
                CLOCK = vector_compare(CLOCK, req['clock'])
                res['clock'] = CLOCK
                product['quantidade'] -= 1
                res['res'] = 'OK'
                return jsonify(clock=res['clock'], res=res['res'])
            else:
                continue
    
        # se pertencem:
            # deve verificar ordem do relógio de mensagem
                # se o relógio for maior que o atual
                # deve incrementar o relógio
                # deve permitir a compra
                # deve enviar resposta OK
        # se não pertencem
            # deve incrementar o relógio
            # deve negar a compra
    print('request json on return')
    print(req)
    print('dblocal items')
    print(dblocal)
    return jsonify(clock=req['clock'], res='NO')

@app.post("/adicionar/")
def adicionar():
    req = json.loads(request.get_json())    # produto (dict)
    print("request adicionar")
    print(request.get_json())
    def write_json(new_data, filename):
            with open(filename,'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data['produtos'].append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
    write_json(req['produto'], 'produtos.json')

    return jsonify(200)

#remove do carrinho
@app.route("/remove/", methods=["GET"])
def remove():
    # Get the id of shirt selected to be removed
    out = int(request.args.get("id"))

    # Remove shirt from shopping cart
    with open('carrinho.json', 'r') as json_file:    
        # Reading from json file
        json_object = json.load(json_file)
    tamanho = len(json_object['carrinho'])
    camisas = json_object
    for i in range(tamanho):	
        if camisas['carrinho'][i]['id'] == out:
            print(camisas['carrinho'][i]['id'])
            camisas['carrinho'].pop(i)
            break
    #reescreve
    open("carrinho.json", "w").write(json.dumps(camisas, indent=4))

    # Initialize shopping cart variables
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart

    with open('carrinho.json', 'r') as openfile:  
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 

    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

#pagina do carrinho 
@app.route("/cart/")
def cart():
    # Clear shopping cart variables
    totItems, total, display = 0, 0, 0
    # Grab info currently in database
    with open('carrinho.json', 'r') as openfile:    
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Render shopping cart
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


# Only needed if Flask run is not used to execute the server
if __name__ == "__main__":
    # lembrar de alterar IP para apresentação
    app.run( host='0.0.0.0', port=8080 )
