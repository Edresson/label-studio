import json

with open('Scipo/Resultado-Scipo-Edresson/0.json') as json_file:
    data = json.load(json_file)
    texto_completo = data['data']['text']
    # find all spaces in texto_completo and create a list ( initialize list with zeros)
    # create map functions map the a list value.
    for r in  data['completions']:
        for v in r['result']:
            
            print(v['value']['start'])


            
            
        

        
