import streamlit as lit
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from pandas import json_normalize
import streamlit as lit
import json
from pandas import json_normalize

#teste para construir carrinho

lit.sidebar.title('Menu')
paginaAdm = lit.sidebar.selectbox('Admin',['Cadastro de produto', 'Visualizar todos os produtos'])
if paginaAdm == 'Cadastro de produto':
	with open('produtos.json', 'r') as openfile:    
			# Reading from json file
		json_object = json.load(openfile)
	data = json_normalize(json_object['produtos'])

	gb = GridOptionsBuilder.from_dataframe(data)
	gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
	gb.configure_side_bar() #Add a sidebar
	gb.configure_selection('multiple') #Enable multi-row selection
	gridOptions = gb.build()

	grid_response = AgGrid(
		data,
		gridOptions=gridOptions,
		data_return_mode='AS_INPUT', 
		update_mode='MODEL_CHANGED', 
		fit_columns_on_grid_load=False,
		enable_enterprise_modules=True,
		height=350, 
		width='100%',
		reload_data=True
	)

	data = grid_response['data']
	selected = grid_response['selected_rows'] 
	df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
	lit.dataframe(df)