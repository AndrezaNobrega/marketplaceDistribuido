import streamlit as lit
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from pandas import json_normalize
import streamlit as lit
import json
from pandas import json_normalize


with open('produtos.json', 'r') as json_file:    
		# Reading from json file
	json_object = json.load(json_file)



tamanho = len(json_object['produtos'])

print(tamanho)

camisas = json_object['produtos'] 

for i in range(tamanho):	
	print(camisas[i]['team'])
