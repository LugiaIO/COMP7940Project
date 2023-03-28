import json 
import copy

temp_json = []

with open('imdb_top_1000.json', 'r') as f:
  data = json.load(f)
  for i in data:
    i['Series_Title_Index'] = (i['Series_Title']).split()
  temp_json = copy.deepcopy(data)

with open("imdb_final.json", "w") as outfile:
  json.dump(temp_json, outfile)