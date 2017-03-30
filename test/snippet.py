import io
import os
import json

jsonDirPath = "" #Change to probably "../dat/json/"
jsonFileName = "1002725.3.js"

'''
Open each json file and find the protein ID using the base pairs range, e.g.:
open 1002725.3.js
loop through CDS
check CDS value for 100609..102174
get "NCBI_genpept:protein_id|YP_004415067.1"
'''

filePath = jsonDirPath + jsonFileName

with open( filePath, 'r', encoding="utf-8" ) as f:

	data = json.load( f )

print( data )