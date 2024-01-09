### Bibliotecas Correlatas
import statsmodels as sm
#import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
"""
### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Variáveis
cidade = "Florianópolis"
# Semanas Epidemiológicas de 2022
"""
focos = "focos22se.csv"
casos = "casos22se.csv"
merge = "merge22se.csv"
tmin = "tmin22se.csv"
tmed = "tmed22se.csv"
tmax = "tmax22se.csv"
"""
# Semanas Epidemiológicas da Série Histórica
# Casos já são por Semana Epimediológica

casos = "casos.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
tmin = "tmin_seSH.csv"

### Abrindo Arquivos
focos = pd.read_csv(f"{caminho_dados}{focos}")
casos = pd.read_csv(f"{caminho_dados}{casos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")

### Selecionando Município
focos = focos[f"{cidade}"].copy()
casos = casos[f"{cidade}"].copy()
merge = merge[f"{cidade}"].copy()
tmin = tmin[f"{cidade}"].copy()
tmed = tmed[f"{cidade}"].copy()
tmax = tmax[f"{cidade}"].copy()

### Transformação em floats de menor bits
focos = focos.astype(np.float16)
casos = casos.astype(np.float16)
merge = merge.astype(np.float16)
tmin = tmin.astype(np.float16)
tmed = tmed.astype(np.float16)
tmax = tmax.astype(np.float16)

### Montando Tabela
dados = pd.DataFrame()
dados["Focos"], dados["Precipitação"], dados["Casos"] = focos, merge, casos
dados["Temperatura Mínima"], dados["Temperatura Média"], dados["Temperatura Máxima"] = tmin, tmed, tmax
#dados["log_focos"], dados["log_precipitacao"] = np.log(dados["Focos"]), np.log(dados["Precipitação"])
#dados["log_temperatura_minima"], dados["log_temperatura_media"] = np.log(dados["Temperatura Mínima"]), np.log(dados["Temperatura Média"])
#dados["log_temperatura_maxima"] = np.log(dados["Temperatura Máxima"])
print(f"\n \n TABELA BASE DO MUNICÍPIO DE {cidade.upper()} PARA REGRESSÃO \n")
print(dados)
print("~"*80)
print(dados.info())
print("~"*80)
print(".DTYPES \n \n", dados.dtypes)
print("="*80)

### Visualização Gráfica
#focos_n_nulos = dados.query("Focos >= 1")["Focos"]#[dados["Focos"] >= 1]
#focos_m_10 = dados.query("Focos >= 10")["Focos"]
focos_m_20 = dados.query("Focos >= 20")["Focos"]
ax = sns.scatterplot(data = dados, x = dados["Focos"], y = dados["Temperatura Mínima"])
sns.rugplot(data = dados, x = dados["Focos"], y = dados["Temperatura Mínima"], height = -0.02, clip_on = False)
sns.kdeplot(data = dados, x = "Focos", y = "Temperatura Mínima")
sns.lmplot(data = dados, x = "Focos", y = "Temperatura Mínima")
ax.set_title("Dispersão dos Dados")
ax.set_xlabel("Focos")
ax.set_ylabel("Temperatura Mínima")
plt.show()
