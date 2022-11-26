import streamlit as lit
from random import *
import json
import visualizarProdutos
#import model.Produto as produtoImp

lit.sidebar.title('Menu')
paginaAdm = lit.sidebar.selectbox('Admin',['Cadastro de produto', 'Visualizar todos os produtos'])

if paginaAdm == 'Cadastro de produto':
    lit.title('Cadastro de produto')
    with lit.form(key = "cadastro produto"):
        nome = lit.text_input(label = 'Insira aqui o nome do produto')
        varejista = lit.text_input(label = 'Insira aqui o varejista') #aqui tem que aparecer as opções cadastradas no bd
        valor = lit.number_input(label= 'Digite aqui o valor do produto',step=1.,format="%.2f") 
        submit =  lit.form_submit_button('Cadastrar')

    if submit:
        id = str(randint(1000,9999)) #gera ID
        produto = {"ID": id,
                        "nome": nome,
                        "valor": str(valor),
                        "varejista": varejista
        }

            # function to add to JSON
        def write_json(new_data, filename='produtos.json'):
            with open(filename,'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data['produtos'].append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
        
        write_json(produto) #escrevendo o novo produto no BD  
        lit.success('Produto cadastrado com sucesso', icon="✅") 
       
if paginaAdm == 'Visualizar todos os produtos':
    visualizarProdutos.visualizarTodos()

    