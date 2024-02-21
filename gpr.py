### Bibliotecas Correlatas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, RationalQuadratic as RQ
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared as Exp, DotProduct as Lin
"""
import statsmodels as sm
import seaborn as sns
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
# Variáveis / Semanas Epidemiológicas de 2022
focos = "focos22se.csv"
casos = "casos22se.csv"
merge = "merge22se.csv"
tmin = "tmin22se.csv"
tmed = "tmed22se.csv"
tmax = "tmax22se.csv"

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

### Montando e Visualizando DataFrame (Pandas)
dados = pd.DataFrame()
dados["Focos"], dados["Precipitação"], dados["Casos"] = focos, merge, casos
dados["Temperatura Mínima"], dados["Temperatura Média"], dados["Temperatura Máxima"] = tmin, tmed, tmax
#dados["log_focos"], dados["log_precipitacao"] = np.log(focos), np.log(merge)
#dados["log_temperatura_minima"], dados["log_temperatura_media"] = np.log(tmin), np.log(tmed)
#dados["log_temperatura_maxima"] = np.log(tmin)
print(f"\n \nDATAFRAME BASE DO MUNICÍPIO DE {cidade.upper()} PARA PROCESSO GAUSSIANO DE REGRESSÃO \n")
print(dados)
print("~"*80)
print(dados.info())
print("~"*80)
print(dados.dtypes)
print("~"*80)
print(dados.describe())
print("="*80)

### Montando e Visualizando Arrays (Numpy)
print(dados.shape)
dados_array = np.asarray(dados)
focos = dados_array[0 : (dados.shape[0] - 1), 0]
prec = dados_array[0 : (dados.shape[0] - 1), 1]
casos = dados_array[0 : (dados.shape[0] - 1), 2]
tmin = dados_array[0 : (dados.shape[0] - 1), 3]
tmed = dados_array[0 : (dados.shape[0] - 1), 4]
tmax = dados_array[0 : (dados.shape[0] - 1), 5]
y = np.asarray([prec, tmin, tmed, tmax]).T
x = np.atleast_2d(focos).T
print(f"\n \nARRAY BASE DO MUNICÍPIO DE {cidade.upper()} (VARIÁVEIS EXPLICATIVAS = ELEMENTOS CLIMÁTICOS) \n")
print(y)
print("="*80)
print(f"\n \nARRAY BASE DO MUNICÍPIO DE {cidade.upper()} (VARIÁVEL DEPENDENTE = FOCOS) \n")
print(x)
print("="*80)

np.random.seed(0)

### Instanciando o Modelo de Processo Gaussiano
"""
kernel = C()*Exp(length_scale = 52, periodicity = 1)
kernel = C()*RQ(length_scale = 52, alpha = 1)
kernel = C()*Exp(length_scale = 52, periodicity = 1) * RQ(length_scale = 52, alpha = 1,
                                                          length_scale_bounds = (1e-05, 2),
                                                          alpha_bounds = (1e-05, 100000.0))
"""
kernel = C()*RBF(length_scale = 52,
                 length_scale_bounds = (1e-05, 2)) * RQ(length_scale = 1, alpha = 0.5,
                                                        length_scale_bounds = (1e-05, 2),
                                                        alpha_bounds = (1e-05, 100000.0) + Exp (length_scale = 52, periodicity = 1))
gp = GaussianProcessRegressor(kernel = kernel, n_restarts_optimizer = 4)
gp.fit(x, y)
y_pred_1, sigma_1 = gp.predict(x, return_std = True)



