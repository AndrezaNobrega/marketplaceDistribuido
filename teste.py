import streamlit as lit
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from pandas import json_normalize
import streamlit as lit
import json
from pandas import json_normalize




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




#remove produto
with open('produtos.json', 'r') as json_file:    
	# Reading from json file
	json_object = json.load(json_file)
tamanho = len(json_object['produtos'])
camisas = json_object
for i in range(tamanho):	
	if camisas['produtos'][i]['id'] == "8989":
		print(camisas['produtos'][i]['id'])
		camisas['produtos'].pop(i)
		break
#reescreve
open("produtos.json", "w").write(json.dumps(camisas, indent=4))



