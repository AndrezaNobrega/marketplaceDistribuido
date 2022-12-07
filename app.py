from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, Response

from random import *
import json

from controller import eventController


# # Instantiate Flask object named app
app = Flask(__name__)
clock = [0,0,0]
PORTA = int(input("PORTA="))
# # Configure sessions
# Session(app)

# # db sqlite - será substituido pelo json de visualização 
db = SQL ( "sqlite:///data.db" )




#TODO tela de cadastro de produtos 
#TODO colocar quantidade de cada produto no banco de dados
#TODO colocar as refs bootstrap nos arquivos p/ n depender da rede

#index
#está funcionando
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
        
    #integrar o add ao carrinho
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
    return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )



#update do carrinho
#funciona
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
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )



#editando no momento para integrar c o json
@app.route("/filter/")
def filter():
    if request.args.get('continent'):
        query = request.args.get('continent')
        shirts = db.execute("SELECT * FROM shirts WHERE continent = :query ORDER BY team ASC", query=query )
    if request.args.get('sale'):
        query = request.args.get('sale')
        shirts = db.execute("SELECT * FROM shirts WHERE onSale = :query ORDER BY team ASC", query=query)
    if request.args.get('id'):
        query = int(request.args.get('id'))
        shirts = db.execute("SELECT * FROM shirts WHERE id = :query ORDER BY team ASC", query=query)
    if request.args.get('kind'):
        query = request.args.get('kind')
        shirts = db.execute("SELECT * FROM shirts WHERE kind = :query ORDER BY team ASC", query=query)
    if request.args.get('price'):
        query = request.args.get('price')
        shirts = db.execute("SELECT * FROM shirts ORDER BY onSalePrice ASC")
    shirtsLen = len(shirts)
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart
    shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Render filtered view
    return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )

 

# ---------------------------- funções de acesso ao db compartilhado -----------------------------------------------------

#quando marketplace efetua a compra
#essa parte ta dando erro pois puxa no carrinho o uid que fazia parte da sessão do ususário e tirei
#mas como n vamos utilizar, deixei dessa maneira msm, pra gente só ter uma base
@app.get("/checkout/")
def checkout():
    order = db.execute("SELECT * from cart")    
    # order = list
    # precisa enviar para todas as lojas a requisição
    # TODO enviar uma solicitação com a lista da compra para os peers
    event = eventController.orderEvent(order, clock=clock,id=(PORTA-3030))
    print('Event res: ')
    print (event)

    # for item in order:
    #     #nao é necessario registrar historico de compras, por isso o uid e essa query não são necessarios
    #     db.execute("INSERT INTO purchases (uid, id, team, image, quantity) VALUES(:uid, :id, :team, :image, :quantity)", uid=session["uid"], id=item["id"], team=item["team"], image=item["image"], quantity=item["qty"] )

    # Clear shopping cart
    db.execute("DELETE from cart")
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Redirect to home page
    return redirect('/')

# Rota por onde são recebidas as solicitações para compra (acesso ao DB)
@app.get("/compra")
def compra():
    # deve verificar se os itens da compra pertencem ao BD LOCAL
    print("request args: ")
    print(request.args('query'))   # está vindo vazio...
        # se pertencem:
            # deve verificar ordem do relógio de mensagem
                # se o relógio for maior que o atual
                # deve incrementar o relógio
                # deve permitir a compra
                # deve enviar resposta OK
        # se não pertencem
            # deve incrementar o relógio
            # 
    return Response({'res':'OK'}, 200)

#remove do carrinho
#está funcionando
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
        # Reading from json file
        json_object = json.load(openfile)
        shoppingCart = json_object['carrinho'] 

    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )

#pagina do carrinho 
#funciona
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
    # deve enviar uma visualização do seu estoque como somente leitura para todos
    # lembrar de alterar IP para apresentação
    app.run( host='0.0.0.0', port=8080 )
