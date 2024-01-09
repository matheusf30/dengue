### Bibliotecas Correlatas
import statsmodels as sm
#import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Variáveis - Semanas Epidemiológicas de 2022
cidade = "Florianópolis"
#casos = "casos22se.csv"
focos = "focos22se.csv"
merge = "merge22se.csv"
tmin = "tmin22se.csv"
tmed = "tmed22se.csv"
tmax = "tmax22se.csv"

### Abrindo Arquivos
#casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")

### Montando Tabela
dados = pd.DataFrame()
dados["Focos"], dados["Precipitação"] = focos[f"{cidade}"], merge[f"{cidade}"]
dados["Temperatura Mínima"], dados["Temperatura Média"], dados["Temperatura Máxima"] = tmin[f"{cidade}"], tmed[f"{cidade}"], tmax[f"{cidade}"]
#dados["log_focos"], dados["log_precipitacao"] = np.log(dados["Focos"]), np.log(dados["Precipitação"])
#dados["log_temperatura_minima"], dados["log_temperatura_media"] = np.log(dados["Temperatura Mínima"]), np.log(dados["Temperatura Média"])
#dados["log_temperatura_maxima"] = np.log(dados["Temperatura Máxima"])
dados
