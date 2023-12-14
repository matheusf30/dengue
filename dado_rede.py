### Bibliotecas Correlatas
import pandas as pd
import numpy as np
"""
import matplotlib.pyplot as plt               
import seaborn as sns
import statsmodels as sm
"""

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
#casos = "casos.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
#tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
#tmin = "tmin_seSH.csv"

### Abrindo Arquivos
#casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
#tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
#tmin = pd.read_csv(f"{caminho_dados}{tmin}")

### Selecionando Município e Manipulando Variáveis
## Recorte Município (Florianópolis)
dado_rede = focos[["Palhoça", "Florianópolis"]].iloc[: ]
dado_rede = dado_rede.rename(columns={"Florianópolis" : "Focos"})
dado_rede["Focos_m1"] = focos["Florianópolis"].iloc[1:-1]
dado_rede["Focos_m2"] = focos["Florianópolis"].iloc[ :-2]
dado_rede = dado_rede.drop(["Palhoça"], axis = "columns")
dado_rede["Precipitação"] = merge["Florianópolis"].iloc[1: ]
dado_rede["Precipitação_m1"] = merge["Florianópolis"].iloc[ :-1]
dado_rede["Temperatura"] = tmed["Florianópolis"].iloc[1: ]
dado_rede["Temperatura_m1"] = tmed["Florianópolis"].iloc[ :-1]

"""
## Manipulando Variável Categórica
#dado_rede["Categoria"] = []
cat = 10
gap = focos["Florianópolis"].max - focos["Florianópolis"].min
cte = gap/cat
cont = 0
#while (cont<gap
"""
del focos

print("\n \n BASE DE DADOS PARA REDE NEURAL \n")
print(dado_rede.info())
print("~"*80)
print(dado_rede.dtypes)
print("~"*80)
print(dado_rede)
print("="*80)
"""
print(f"São {cat} categorias, tendo {cte} como constante e {gap} como intervalo.")
print("~"*80)
print(cont)
print("~"*80)
print(dado_rede)
"""
