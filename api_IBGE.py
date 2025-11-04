import requests
import json
import pandas as pd

'''api_agregados = 'https://servicodados.ibge.gov.br/api/v3/agregados/6407/variaveis/606|6541?classificacao=2[4,5]&localidades=N6[4205407]' ''' #exemplo de query

def consulta_ibge(tabela, variaveis, classificacao_categorias, localidades):
    '''ex. de tabela: 6407\n
       ex. de variaveis 606|6541 --> busca as variaveis 606 e 6541\n
       ex. de classificacao 2[4,5] --> busca na classificacao 2 as categorais 4 e 5\n
       ex. de localidade N6[4205407] --> busca na localidade de nível N6 (municipios) o município 4205407\n
    '''
    api = 'https://servicodados.ibge.gov.br/api/v3/agregados/'
    query = api + tabela + '/variaveis/' + variaveis + '?classificacao=' + classificacao_categorias + '&localidades=' + localidades
    r = requests.get(query)
    data = json.loads(r.text)
    return data

def consulta_metadados(tabela,especificacao=None):
    '''possibilidades de especificacao:
    \nnivelTerritorial
    \nclassificacoes
    '''
    api = 'https://servicodados.ibge.gov.br/api/v3/agregados/'
    query = api+ tabela + '/metadados'
    r = requests.get(query)
    data = json.loads(r.text)
    if especificacao!=None:
        data = data[especificacao]
    return data


def limpa_resultado(data):
    '''retornará uma lista de resultados para cada classificacção de cada variável'''
    resultado = []
    for variavel in data:
        nome_variavel = variavel['variavel']
        unidade = variavel['unidade']
        #print(nome_variavel, unidade)
        for serie in variavel['resultados']:
            resultado.append([nome_variavel, unidade,
                               serie['series'][0]['localidade']['nome'],
                               serie['classificacoes'][0]['categoria'],
                               serie['series'][0]['serie']])
    resultado = pd.DataFrame(resultado)
    resultado = resultado.rename(columns={0:'Variavel',1:'Unidade',2:'Local',3:'Classificacao',4:'Resultados'})
    resultado = resultado.join(resultado['Resultados'].apply(pd.Series)).drop(columns=['Resultados'])
    def clean_dict(cell):
        for key, values in cell.items():
            cell = cell[key]
        return cell
    resultado['Classificacao'] = resultado['Classificacao'].apply(clean_dict)
    resultado = resultado.set_index(["Variavel", "Unidade","Local",'Classificacao']).stack().reset_index() # transforma anos em linhas
    resultado = resultado.rename(columns={'level_4':'ano',0:'resultados'})

    df_final = pd.DataFrame()
    for valor in resultado['Classificacao'].unique():
        novo_df = resultado[resultado['Classificacao'] == valor]
        novo_df = novo_df.rename(columns={'level_4':'ano','resultados':valor}).drop(columns=['Classificacao']).reset_index()
        df_final = pd.concat([df_final,novo_df],axis=1)
    df_final = df_final.T.drop_duplicates().T
    df_final.drop(columns='index',inplace=True)

    return df_final


def limpa_resultado_sem_classificacao(data):
    '''retornará uma lista de resultados para cada classificacção de cada variável'''
    resultado = []
    for variavel in data:
        nome_variavel = variavel['variavel']
        unidade = variavel['unidade']
        for serie in variavel['resultados']:
            resultado.append([nome_variavel, unidade,
                               serie['series'][0]['localidade']['nome'],
                               serie['series'][0]['serie']])
    resultado = pd.DataFrame(resultado)
    
    resultado = resultado.rename(columns={0:'Variavel',1:'Unidade',2:'Local',3:'Resultados'})
    
    resultado = resultado.join(resultado['Resultados'].apply(pd.Series)).drop(columns=['Resultados'])
    resultado = resultado.set_index(["Variavel", "Unidade","Local"]).stack().reset_index() # transforma anos em linhas
    resultado = resultado.rename(columns={'level_3':'ano',0:'resultados'})

    return resultado
