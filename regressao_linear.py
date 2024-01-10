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

### Variáveis
cidade = "Florianópolis"
# Semanas Epidemiológicas de 2022

focos = "focos22se.csv"
casos = "casos22se.csv"
merge = "merge22se.csv"
tmin = "tmin22se.csv"
tmed = "tmed22se.csv"
tmax = "tmax22se.csv"

# Semanas Epidemiológicas da Série Histórica
# Casos já são por Semana Epimediológica
"""
casos = "casos.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
tmin = "tmin_seSH.csv"
"""
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
#focos = np.nan_to_num(focos) # ValueError: array must not contain infs or NaNs
casos = casos.astype(np.float16)
merge = merge.astype(np.float16)
tmin = tmin.astype(np.float16)
tmed = tmed.astype(np.float16)
tmax = tmax.astype(np.float16)

### Montando Tabela
dados = pd.DataFrame()
dados["Focos"], dados["Precipitação"], dados["Casos"] = focos, merge, casos
dados["Temperatura Mínima"], dados["Temperatura Média"], dados["Temperatura Máxima"] = tmin, tmed, tmax
dados["log_focos"], dados["log_precipitacao"] = np.log(focos), np.log(merge)
dados["log_temperatura_minima"], dados["log_temperatura_media"] = np.log(tmin), np.log(tmed)
dados["log_temperatura_maxima"] = np.log(tmin)
print(f"\n \n TABELA BASE DO MUNICÍPIO DE {cidade.upper()} PARA REGRESSÃO \n")
print(dados)
print("~"*80)
print(dados.info())
print("~"*80)
print(dados.dtypes) #".DTYPES \n \n", 
print("~"*80)
print(dados.describe())
print("="*80)

### Visualização Gráfica
#focos_n_nulos = dados.query("Focos >= 1")["Focos"]#[dados["Focos"] >= 1]
#focos_m_10 = dados.query("Focos >= 10")["Focos"]
#focos_m_20 = dados.query("Focos >= 20")["Focos"]
ax = sns.scatterplot(data = dados, x = dados["Focos"], y = dados["Temperatura Mínima"])
sns.rugplot(data = dados, x = dados["Focos"], y = dados["Temperatura Mínima"], height = -0.02, clip_on = False)
sns.kdeplot(data = dados, x = "Focos", y = "Temperatura Mínima")
sns.lmplot(data = dados, x = "Focos", y = "Temperatura Mínima")
ax.set_title("Dispersão dos Dados")
ax.set_xlabel("Focos")
ax.set_ylabel("Temperatura Mínima")
plt.show()
#
ax_log = sns.scatterplot(data = dados, x = dados["log_focos"], y = dados["log_temperatura_minima"])
sns.rugplot(data = dados, x = dados["log_focos"], y = dados["log_temperatura_minima"], height = -0.02, clip_on = False)
sns.kdeplot(data = dados, x = "log_focos", y = "log_temperatura_minima")
sns.lmplot(data = dados, x = "log_focos", y = "log_temperatura_minima")
ax_log.set_title("Dispersão dos Dados (Logarítmica)")
ax_log.set_xlabel("Focos")
ax_log.set_ylabel("Temperatura Mínima")
plt.show()
"""
### Definindo Funções

## Erro Quadrático Médio (EQM)
def prever(x_i, theta1, theta0):
    return x_i * theta1 + theta0

def erro_quadratico_medio (previsto, y):
    return np.array([(y_i - y_previsto) ** 2 for y_i, y_previsto in zip(y, previsto)]).mean()

def minimos_quadrados (x, y):
    theta1 = np.corrcoef(x, y)[0, 1] * (y.std()/ x.std())
    theta0 = y.mean() - theta1 * x.mean()
    return theta1, theta0

## Coeficiente de Regressão (R²)
def r_2 (y_previsto, y):
    variancia_prevista = sum([(y_i - y_previsto)  ** 2 for y_i, y_previsto in zip (y, y_previsto)])
    variancia_original = sum([(y_i - y.mean())  ** 2 for y_i in y])
    return 1 - variancia_prevista/variancia_original

## Derivada
def derivada(theta0, theta1, x, y):
    dtheta0 = 0
    dtheta1 = 0
    for x_i, y_i in zip (x, y):
        dtheta0 += prever(x_i, theta1, theta0) - y_i
        dtheta1 += (prever(x_i, theta1, theta0) - y_i) * x_i
    dtheta0 /= 0.5 * len(x)
    dtheta1 /= 0.5 * len(y)
    return dtheta0, dtheta1

## Gradiente Descendente
def gradiente_descendente (theta0, theta1, x, y, alpha):
    dtheta0, dtheta1 = derivada(theta0, theta1, x, y)
    theta0 -= alpha * dtheta0
    theta1 -= alpha * dtheta1
    return theta0, theta1

### Impressão de Coeficientes
print("="*80)

## Theta1 e Theta0
theta1, theta0 = minimos_quadrados(dados["log_focos"], dados["log_temperatura_minima"])
print(f"Theta1 = {theta1} e Theta0 =  {theta0}.")
print("~"*80)

##EQM (log)
previstos = prever(dados["log_temperatura_minima"], theta1, theta0)
print(f"EQM(log) = {erro_quadratico_medio(previstos, dados["log_focos"])}.")
print("~"*80)

## EQM
previstos = prever(dados["Temperatura Mínima"], theta1, theta0)
print(f"EQM = {erro_quadratico_medio(previstos, dados["Focos"])}.")
print("~"*80)

## R²
print(f"R² = {r_2(previstos, dados3["log_valor"])}.")
print("~"*80)

## Valor Previsto e Valor Previsto (log)
print(f"Valor Previsto (log) = {prever(np.log(72), theta1, theta0)}.")
print("~"*80)
print(f"Valor Previsto = {np.exp(prever(np.log(72), theta1, theta0))}.")
print("~"*80)

## Visualização Gráfica (scatterlot()+lineplot())
ax_prev = sns.scatterplot(x = dados3["log_area"], y = dados3["log_valor"])
ax_prev = sns.lineplot(x = dados3["log_area"], y = previstos, color = "r")
ax_prev.set_title("Curva Prevista nos Dados Dispersos")
ax_prev.set_xlabel("Área")
ax_prev.set_ylabel("Valores Previstos")
"""
### Regressão Linear
## Montando Modelo
lr_log = LinearRegression()
lr_log.fit(np.array(dados["log_temperatura_minima"]).reshape(len(dados), 1), dados["log_focos"])
lr = LinearRegression()
lr.fit(np.array(dados["Temperatura Mínima"]).reshape(len(dados), 1), dados["Focos"])
## Visualização Gráfica
plt.figure(figsize = (10, 6))
ax_lr_log = sns.scatterplot(x = dados["log_temperatura_minima"], y = dados["log_focos"])
ax_lr_log = sns.lineplot(x = dados["log_temperatura_minima"], color = "r", y = lr_log.predict(np.array(dados["log_temperatura_minima"]).reshape(len(dados), 1)))
ax_lr_log.set_title("Curva do Modelo de Regressão Linear Prevista nos Dados Dispersos (log)")
ax_lr_log.set_xlabel("Temperatura Mínima")
ax_lr_log.set_ylabel("Focos")
plt.show()
plt.figure(figsize = (10, 6))
ax_lr = sns.scatterplot(x = dados["Temperatura Mínima"], y = dados["Focos"])
ax_lr = sns.lineplot(x = dados["Temperatura Mínima"], color = "r", y = lr.predict(np.array(dados["Temperatura Mínima"]).reshape(len(dados), 1)))
ax_lr.set_title("Curva do Modelo de Regressão Linear Prevista nos Dados Dispersos")
ax_lr.set_xlabel("Temperatura Mínima")
ax_lr.set_ylabel("Focos")
plt.show()
## R²
print(f"R² (log) = {r2_score(dados['log_focos'], lr_log.predict(np.array(dados['log_temperatura_minima']).reshape(len(dados), 1)))}.")
print(f"R² = {r2_score(dados['Focos'], lr.predict(np.array(dados['Temperatura Mínima']).reshape(len(dados), 1)))}.")
#print(np.seterr())
# https://numpy.org/doc/stable/reference/generated/numpy.seterr.html
