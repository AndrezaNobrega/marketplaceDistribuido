import streamlit as lit
import uuid
import json
#import model.Produto as produtoImp

lit.title('Cadastro de produto')
with lit.form(key = "cadastro produto"):
    nome = lit.text_input(label = 'Insira aqui o nome do produto')
    varejista = lit.text_input(label = 'Insira aqui o varejista') #aqui vai aparecer as opções cadastradas no bd
    valor = lit.number_input(label = 'Digite aqui o valor do produto') 
    submit =  lit.form_submit_button('Cadastrar')

if submit:
    #lit.write('Produto', nome, 'cadastrado com sucesso!')    
    id = str(uuid.uuid4())
    produto = {"ID": id,
                    "nome": nome,
                    "valor": valor,
                    "varejista": varejista
    }

    with open('produtos.json', 'w') as json_file:
        json.dump(produto, json_file)
    lit.write('Produto', nome, 'cadastrado com sucesso!') 
    #jsonstr1 = json.dumps(produtoImp.__dict__) #quando resolver problema da importação, usar esse para escreve o objeto diretamente no bd


    