    
import json


def jsonProdutos():
    with open('produtos.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    return json_object