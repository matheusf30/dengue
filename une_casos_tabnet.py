"""
REGISTRO SINAN/SC
Atentar aos dados provenientes do TabNet... https://tabnet.datasus.gov.br/

--Seleções:
>>> LINHAS: Município de Infecção;
>>> COLUNAS: Semana Epidemilógica dos 1ºs sinais.

--Períodos:
>>> Haverá um arquivo por ano.

--Seleções Disponíveis(Filtros):
>>> Classificação Final: Dengue Clássico, Dengue com Complicações, Febre Hemorrágica do Dengue,
                         Síndrome do Choque do Dengue, Dengue e Dengue com Sinais de alarme.
(Nesse filtro foram desconsiderados: Ignorado, Branco, Descartado e Inconclusivo)

>>> Critério de Confirmação: Laboratorial e Clínico-Epidemiológico.
(Nesse filtro foram desconsiderados: Ignorado, Branco e Em Investigação)

>>>(Também não foram filtrados por sorotipo, pois não há confirmação laboratorial de todos.) 
"""
### Bibliotecas Correlatas
import pandas as pd

### Encaminhamento aos Diretórios
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"
_www = True
if _www == True: # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
else:
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n{caminho_modelos}")

### Renomeação variáveis pelos arquivos
## Dados "Brutos"
## Fonte: TABNET/DATASUS - SINAN/SC
casos = "casos.csv"
casos_se = "casos_se.csv"
#focos2012 = "focos_dive_2012.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
casos_se = pd.read_csv(f"{caminho_dados}{casos_se}")
"""
focos202202 = pd.read_csv(f"{caminho_dados}{focos202202}", skiprows = 3)
focos202201 = pd.read_csv(f"{caminho_dados}{focos202201}", skiprows = 3)
focos2021 = pd.read_csv(f"{caminho_dados}{focos2021}", skiprows = 3)
focos2020 = pd.read_csv(f"{caminho_dados}{focos2020}", skiprows = 3)
focos2019 = pd.read_csv(f"{caminho_dados}{focos2019}", skiprows = 3)
focos2018 = pd.read_csv(f"{caminho_dados}{focos2018}", skiprows = 3)
focos2017 = pd.read_csv(f"{caminho_dados}{focos2017}", skiprows = 3)
focos2016 = pd.read_csv(f"{caminho_dados}{focos2016}", skiprows = 3)
focos2015 = pd.read_csv(f"{caminho_dados}{focos2015}", skiprows = 3)
focos2014 = pd.read_csv(f"{caminho_dados}{focos2014}", skiprows = 3)
focos2013 = pd.read_csv(f"{caminho_dados}{focos2013}", skiprows = 3)
focos2012 = pd.read_csv(f"{caminho_dados}{focos2012}", skiprows = 3)
"""
### Pré-Processamento
casos.drop(columns = "Data", inplace = True)
casos.rename(columns = {"data" : "Semana"}, inplace = True)
casos = pd.melt(casos, id_vars = "Semana", var_name = "Município",
                value_name = "Casos", ignore_index = True)
#value_vars = se não especificado, usa todas as colunas.
casos = casos.replace("2014-01-06", "2014-01-05")
casos["Município"] = casos["Município"].str.upper()
casos["Casos"] = casos["Casos"].astype(int)

"""
casos = casos.astype(int)
casos_se = casos_se.astype(int)

pospandemia = pd.concat([focos202202, focos202201, focos2021, focos2020], ignore_index = True)
prepandemia = pd.concat([focos2019, focos2018, focos2017, focos2016], ignore_index = True)
inicial = pd.concat([focos2015, focos2014, focos2013, focos2012], ignore_index = True)
prepandemia = pd.concat([prepandemia, inicial], ignore_index= True)
focostotal = pd.concat([pospandemia, prepandemia], ignore_index = True)
"""

### Salvando Arquivo
#focostotal.to_csv(f"{caminho_dados}focos_dive_total.csv", index = False)

### Printando Informações
print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(casos.info())
print("~"*80)
print(casos.dtypes)
print("~"*80)
print(casos)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA (testando _se) \n")
print(casos_se.info())
print("~"*80)
print(casos_se.dtypes)
print("~"*80)
print(casos_se)
print("="*80)
"""
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO SEGUNDO (02) SEMESTRE DE 2022 \n")
print(focos202202.info())
print("~"*80)
print(focos202202.dtypes)
print("~"*80)
print(focos202202)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO PRIMEIRO (01) SEMESTRE DE 2022 \n")
print(focos202201.info())
print("~"*80)
print(focos202201.dtypes)
print("~"*80)
print(focos202201)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2021 \n")
print(focos2021.info())
print("~"*80)
print(focos2021.dtypes)
print("~"*80)
print(focos2021)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2020 \n")
print(focos2020.info())
print("~"*80)
print(focos2020.dtypes)
print("~"*80)
print(focos2020)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2019 \n")
print(focos2019.info())
print("~"*80)
print(focos2019.dtypes)
print("~"*80)
print(focos2019)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2018 \n")
print(focos2018.info())
print("~"*80)
print(focos2018.dtypes)
print("~"*80)
print(focos2018)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2017 \n")
print(focos2017.info())
print("~"*80)
print(focos2017.dtypes)
print("~"*80)
print(focos2017)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2016 \n")
print(focos2016.info())
print("~"*80)
print(focos2016.dtypes)
print("~"*80)
print(focos2016)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2015 \n")
print(focos2015.info())
print("~"*80)
print(focos2015.dtypes)
print("~"*80)
print(focos2015)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2014 \n")
print(focos2014.info())
print("~"*80)
print(focos2014.dtypes)
print("~"*80)
print(focos2014)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2013 \n")
print(focos2013.info())
print("~"*80)
print(focos2013.dtypes)
print("~"*80)
print(focos2013)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2012 \n")
print(focos2012.info())
print("~"*80)
print(focos2012.dtypes)
print("~"*80)
print(focos2012)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA DURANTE E APÓS PANDEMIA \n")
print(pospandemia.info())
print("~"*80)
print(pospandemia.dtypes)
print("~"*80)
print(pospandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA ANTES DA PANDEMIA \n")
print(prepandemia.info())
print("~"*80)
print(prepandemia.dtypes)
print("~"*80)
print(prepandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(focostotal.info())
print("~"*80)
print(focostotal.dtypes)
print("~"*80)
print(focostotal)
print("="*80)
"""
