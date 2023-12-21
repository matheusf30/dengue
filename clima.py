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
casos = "casos.csv"
focos = "focos.csv"
merge = "merge_novo.csv"
tmax = "tmax.csv"
tmed = "tmed.csv"
tmin = "tmin.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
