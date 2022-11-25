import json
from os import path
 
filename = 'produtos.json'
dictObj = []
 
# Check if file exists
if path.isfile(filename) is False:
  raise Exception("File not found")
 
# Read JSON file
with open(filename) as fp:
  dictObj = json.load(fp)
 
# Verify existing dict
print(dictObj)

print(type(dictObj))
 
dictObj.update({"Age": 12,"Role": "Developer"})
 
# Verify updated dict
print(dictObj)
 
with open(filename, 'w') as json_file:
    json.dump(dictObj, json_file, 
                        indent=4,  
                        separators=(',',': '))
 
print('Successfully written to the JSON file')