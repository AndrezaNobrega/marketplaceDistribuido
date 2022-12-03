from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime

from controller import eventController

import json
from pandas import json_normalize

# # Instantiate Flask object named app
app = Flask(__name__)

# # Configure sessions
# Session(app)

# # db sqlite - será substituido pelo json de visualização 
db = SQL ( "sqlite:///data.db" )
# db = getProdutos()




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
@app.route("/update/")
def update():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))

    # Store id of the selected shirt
    id = int(request.args.get('id'))
    db.execute("DELETE FROM cart WHERE id = :id", id=id)
    # Select info of selected shirt from database
    goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
    # Extract values from selected shirt record
    # Check if shirt is on sale to determine price
    if(goods[0]["onSale"] == 1):
        price = goods[0]["onSalePrice"]
    else:
        price = goods[0]["price"]
    team = goods[0]["team"]
    image = goods[0]["image"]
    subTotal = qty * price
    # Insert selected shirt into shopping cart
    db.execute("INSERT INTO cart (id, qty, team, image, price, subTotal) VALUES (:id, :qty, :team, :image, :price, :subTotal)", id=id, qty=qty, team=team, image=image, price=price, subTotal=subTotal)
    shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
    shopLen = len(shoppingCart)
    # Rebuild shopping cart
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Go back to cart page
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )




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

 

  
#quando marketplace efetua a compra
#essa parte ta dando erro pois puxa no carrinho o uid que fazia parte da sessão do ususário e tirei
#mas como n vamos utilizar, deixei dessa maneira msm, pra gente só ter uma base
@app.get("/checkout/")
async def checkout():
    order = db.execute("SELECT * from cart")
    # Update purchase history of current customer
    # precisa enviar para todas as lojas a requisição

    # TODO enviar uma solicitação com a lista da compra para os peers
    res = await eventController.orderEvent(order)
    print (res)
    # a função assincrona deve:
        # Atualizar relogio
        # enviar mensagens
        # retornar apos resposta de todos os peers

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


#remove do carrinho
@app.route("/remove/", methods=["GET"])
def remove():
    # Get the id of shirt selected to be removed
    out = int(request.args.get("id"))
    # Remove shirt from shopping cart
    db.execute("DELETE from cart WHERE id=:id", id=out)
    # Initialize shopping cart variables
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart
    shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )

#pagina do carrinho (talvez eu tire)
@app.route("/cart/")
def cart():
    # Clear shopping cart variables
    totItems, total, display = 0, 0, 0
    # Grab info currently in database
    shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
    # Get variable values
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
