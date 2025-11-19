import basedosdados as bd
import pandas as pd

#Busca dados de vinculos rais
def coleta_vinculos_rais(codigo_municipio="('3304557')", ano_inicio=2014, billing_project_id=None, nome_arquivo='teste', query=None):

    codigo_municipio = codigo_municipio
    ano_inicio = str(ano_inicio)

    if billing_project_id != None:
        billing_project_id = billing_project_id
    else:
        billing_project_id = input('Insira id do seu projeto no google cloud:\n')

    if query != None:
         df = bd.read_sql(    
        query,
        billing_project_id=billing_project_id
    )
    else:
        df = bd.read_sql(    
            '''
            SELECT ano, sigla_uf, id_municipio, vinculo_ativo_3112,
            cnae_2, cnae_1,
            valor_remuneracao_media, valor_remuneracao_dezembro,
            valor_remuneracao_media_sm, valor_remuneracao_dezembro_sm,
            faixa_horas_contratadas,
            idade, sexo, raca_cor,
            grau_instrucao_1985_2005, grau_instrucao_apos_2005,  
            FROM  basedosdados.br_me_rais.microdados_vinculos
            WHERE ano >= {} AND id_municipio IN {}
            AND vinculo_ativo_3112 = '1'
            '''.format(ano_inicio, codigo_municipio),
            billing_project_id=billing_project_id
        )
        return df, nome_arquivo

def tratamento_tipos(data_frame):
    data_frame['vinculo_ativo_3112'] = data_frame['vinculo_ativo_3112'].astype(int)
    return data_frame