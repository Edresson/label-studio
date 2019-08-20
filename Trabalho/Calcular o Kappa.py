import json
import os 
import sys 
import numpy as np

def find_all(texto, substring):
    pos = [] #list to store positions for each 'char' in 'string'
    flag = True
    atualpos = 0
    realpos = 0  
    while (flag):
        atualpos = texto.find(substring,atualpos+1)
        if (atualpos == -1):
            flag = False   
        else: 
            pos.append(atualpos)
    return pos

modelo_dir ='Modelo-para-Calcular-Kappa'
list_modelo = os.listdir(modelo_dir)
base_list = [ 'SAC-Embrapa/Resultado/','Scipo/Resultado/','UGC_ReclameAqui/Resultado/']
resultados_finais = [ ]
for base in base_list:
    resultados= []
    for dire in list_modelo:

        results_path = os.path.join(modelo_dir,dire,base)
        
        resultados_anotador = []
        for i in range(len(os.listdir(results_path))):
            file_with_path = os.path.join(results_path,str(i)+'.json')
            with open(file_with_path) as json_file:
                data = json.load(json_file)
                texto_completo = data['data']['text']
                spaces = find_all(texto_completo,' ') 
                if( 0 not in spaces):
                    spaces = [0]+spaces
                #print(spaces)
                classes = [0]*len(spaces)
                # find all spaces in texto_completo and create a list ( initialize list with zeros).
                for r in  data['completions']:
                    for v in r['result']:
                        inicio = int(v['value']['start'])
                        if(inicio in spaces):#considera que o espaço ficou na nova sentença
                            
                            classes[spaces.index(inicio)] = 1
                            
                        elif(inicio+1 in spaces):#considera que o espaço ficou na outra sentença
                            
                            classes[spaces.index(inicio+1)] = 1
                            
                        elif(inicio-1 in spaces):# considera que algo além do espaço para o inicio da sentença ex: deixou o ponto final na nova sentença.
                            
                            classes[spaces.index(inicio-1)] = 1
                            

                        else:

                            print(file_with_path,": Não segmentou em espaço verificar !!!, inicio:",inicio)
                            sys.exit()
                        
                resultados_anotador.append(classes)
        resultados.append(resultados_anotador)
    resultados_finais.append(resultados)






# convert resultados
matrizesKappa = []
casos_frase = [] 
pontuacaosim = 0
pontuacaonao = 0
casos_base =[]
for b in range(len(resultados_finais)):# for na base
        casos_frase = []
        for f in range(len(resultados_finais[b][0])):
                
                
                caso_frase = []
                for ires in range(len(resultados_finais[b][0][f])):
                    
                    pontuacaosim = 0
                    pontuacaonao = 0
                    for a in range(len(resultados_finais[b])):
                        res = resultados_finais[b][a][f][ires]
                        if(res == 0):
                            pontuacaonao+= 1
                            #print('não')
                        else:
                            pontuacaosim +=1
                            #print('sim')
                    #print(pontuacaonao,pontuacaosim)
                    caso_frase.append([pontuacaonao,pontuacaosim])
                    #print(caso_frase)
                casos_frase.append(caso_frase)
                
        casos_base.append(casos_frase)


print( np.array(casos_base).shape)   



#ToDo: codigo para o 'Bateria-ABCD/Resultado/' checar espaços e se é positivo ou negativo ou se nao é delimitador ..




