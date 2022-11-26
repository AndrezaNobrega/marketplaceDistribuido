# Python program to update
# JSON


import json


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

	# python object to be appended
y = {"ID": "84c85fd3-fca1-49bd-91bb-5f674a5c8bad", 
    "nome": "jshkdsf", 
    "valor": 25.0, 
    "varejista": "fugodfi"}
	
write_json(y)
