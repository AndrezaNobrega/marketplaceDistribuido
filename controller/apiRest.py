from flask import Flask, jsonify

app = Flask(__name__) 

#exemplo de rota   
@app.route('/valorconta/<string:id>', methods=['GET'])  #buscar o valor da conta
def valorConta(id):
    #chama o metodo
    return jsonify('resultado')

@app.route('/pesquisar/<produto>', methods=['GET'])  #buscar o valor da conta
def pesquisaProduto(produto):
    #chama o metodo
    return jsonify('resultado')

@app.route('/cadastrar/<produto>', methods=['GET'])  #buscar o valor da conta
def cadastraProduto(produto):
    #chama o metodo
    return jsonify('resultado')

#inicializando a API
if __name__ == "__main__":
    # TODO inicializar conexão com outros marketplaces ?
    app.run(host=' ', port=5000)