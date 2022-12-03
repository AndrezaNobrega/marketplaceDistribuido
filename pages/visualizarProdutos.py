import streamlit as lit
import json
from pandas import json_normalize

def visualizarTodos():
    lit.title('Visualizar produtos')
        # Opening JSON file
    with open('produtos.json', 'r') as openfile:
    
        # Reading from json file
        json_object = json.load(openfile)
    df = json_normalize(json_object['produtos'])
    lit.dataframe(df)
