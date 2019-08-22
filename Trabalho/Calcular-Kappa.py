import json
import os 
import sys 
import numpy as np
import statsmodels as sm
import statsmodels.stats.inter_rater

def multirater_kfree(n_ij, n, k):
    '''
    Computes Randolph's free marginal multirater kappa for assessing the 
    reliability of agreement between annotators.
    
    Args:
        n_ij: An N x k array of ratings, where n_ij[i][j] annotators 
              assigned case i to category j.
        n:    Number of raters.
        k:    Number of categories.
    Returns:
        Percentage of overall agreement and free-marginal kappa
    
    See also:
        http://justusrandolph.net/kappa/
    '''
    N = len(n_ij)
    
    P_e = 1./k
    P_O = (
        1./(N*n*(n-1))
        * 
        (sum(n_ij[i][j]**2 for i in range(N) for j in range(k)) - N*n)
    )
    
    kfree = (P_O - P_e)/(1 - P_e)
    
    return P_O, kfree

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
#'SAC-Embrapa/Resultado/', ,  
base_list = ['Bateria-ABCD/Resultado/', 'UGC_ReclameAqui/Resultado/', 'Scipo/Resultado/', 'SAC-Embrapa/Resultado/']
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
                spaces += find_all(texto_completo,'.')
                spaces += find_all(texto_completo,',')
                spaces += find_all(texto_completo,'!')
                spaces += find_all(texto_completo,'?')
                spaces += find_all(texto_completo,';')
                spaces += find_all(texto_completo,':')
                spaces += find_all(texto_completo,"'")
                spaces += find_all(texto_completo,'"')
                if( 0 not in spaces):
                    spaces = [0]+spaces
                #print(spaces)
                classes = [0]*len(spaces)
                # find all spaces in texto_completo and create a list ( initialize list with zeros).
                for r in  data['completions']:
                    for v in r['result']:
                        try:
                            inicio = int(v['value']['start'])
                        except Exception as e:
                            pass
                            #print(v['value'])
                            #print(file_with_path)
                            #exit()
                        
                        if( base == 'Bateria-ABCD/Resultado/'):
                            if(inicio in spaces ):
                                #print(v['value']['labels'][0])
                                if("Positive" in v['value']['labels'][0]):
                                    classes[spaces.index(inicio)] = 1
                                else:
                                    classes[spaces.index(inicio)] = 2

                            elif (inicio+1 in spaces):
                                if("Positive" in v['value']['labels'][0]):
                                    classes[spaces.index(inicio+1)] = 1
                                else:
                                    classes[spaces.index(inicio+1)] = 2
                            elif (inicio-1 in spaces):
                                if("Positive" in v['value']['labels'][0]):
                                    classes[spaces.index(inicio-1)] = 1
                                else:
                                    classes[spaces.index(inicio-1)] = 2
                                
                        else:
                            if(inicio in spaces ):#considera que o espaço ficou na nova sentença
                                
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
casos_frase = [] 
casos_base =[]
for b in range(len(resultados_finais)):# for na base
        casos_frase = []
        for f in range(len(resultados_finais[b][0])):
                
                
                caso_frase = []
                for ires in range(len(resultados_finais[b][0][f])):
                    pontuacao = [0]*(max(resultados_finais[b][0][0])+1) # pegar o numero de classes ( esse controle é por classe por isso ficou [0][0]) 
                    
                    for a in range(len(resultados_finais[b])):
                        res = resultados_finais[b][a][f][ires]
                        pontuacao[res]+=1
                    caso_frase.append(pontuacao)
                casos_frase.append(caso_frase)
                
        casos_base.append(casos_frase)


print( np.array(casos_base).shape)   



for i,matriz in enumerate(casos_base):
    kappa = 0 
    for frase in matriz: 
        num_raters = len(list_modelo)
        if len(frase[0]) == 2:
            novafrase = [[a,b] for a, b in frase if a!=num_raters]
            kappa += multirater_kfree(novafrase, num_raters, 2)[1]
        else:
            novafrase = [[a,b,c] for a, b, c in frase if a!=num_raters]
            kappa += multirater_kfree(novafrase, num_raters, 3)[1]
        #print(novafrase)

        #kappa += sm.stats.inter_rater.fleiss_kappa(novafrase)
    
    print("Kappa do dataset ",base_list[i], ':',kappa/len(matriz))
    


