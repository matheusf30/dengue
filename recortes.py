### Bibliotecas Correlatas
import pandas as pd
import numpy as np
"""
import matplotlib.pyplot as plt               
import seaborn as sns
import statsmodels as sm
"""

### Encaminhamento ao Diretório "DADOS" e "IMAGENS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/imagens/"

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

### Recorte Temporal e Transformação em datetime64[ns]
focos["data"] = pd.to_datetime(focos["data"])
focos = focos.sort_values(by = ["data"])
focos21 = focos.iloc[3288:4018]

casos["data"] = pd.to_datetime(casos["data"])
casos = casos.sort_values(by = ["data"])
casos21 = casos.iloc[364:]

merge["Data"] = merge["data"]
merge["data"] = pd.to_datetime(merge["data"])
merge = merge.sort_values(by = ["data"])
merge21 = merge.iloc[7518:]

tmin["data"] = pd.to_datetime(tmin["data"])
tmin = tmin.sort_values(by = ["data"])
tmin21 = tmin.iloc[7671:]

tmed["data"] = pd.to_datetime(tmed["data"])
tmed = tmed.sort_values(by = ["data"])
tmed21 = tmed.iloc[7671:]

tmax["data"] = pd.to_datetime(tmax["data"])
tmax = tmax.sort_values(by = ["data"])
tmax21 = tmax.iloc[7671:]

### Semanas Epidemiológicas e Agrupamentos
focos21se = focos21.copy()
focos21se["semanaE"] = focos21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
focos21se = focos21se.groupby(["semanaE"]).sum(numeric_only = True)

casos21se = casos21.copy()
casos21se["semanaE"] = casos21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
casos21se = casos21se.groupby(["semanaE"]).sum(numeric_only = True)

merge21se = merge21.copy()
merge21se["semanaE"] = merge21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
merge21se = merge21se.groupby(["semanaE"]).sum(numeric_only = True)

tmin21se = tmin21.copy()
tmin21se["semanaE"] = tmin21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmin21se = tmin21se.groupby(["semanaE"]).mean(numeric_only = True)

tmed21se = tmed21.copy()
tmed21se["semanaE"] = tmed21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmed21se = tmed21se.groupby(["semanaE"]).mean(numeric_only = True)

tmax21se = tmax21.copy()
tmax21se["semanaE"] = tmax21se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmax21se = tmax21se.groupby(["semanaE"]).mean(numeric_only = True)

### Transformação em floats de menor bits
focos21se = focos21se.astype(np.float32)
casos21se = casos21se.astype(np.float32)
merge21se = merge21se.astype(np.float32)
tmin21se = tmin21se.astype(np.float16)
tmed21se = tmed21se.astype(np.float16)
tmax21se = tmax21se.astype(np.float16)

### Salvando, Printando Dados e Informações
print("\n \n FOCOS DE _Aedes aegypti_ \n")
focos21.to_csv(f"{caminho_dados}focos21.csv", index = False)
print(focos21.info())
print("~"*80)
print(focos21.dtypes)
print("~"*80)
print(focos21)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ / SEMANA EPIDEMIOLÓGICA \n")
focos21se.to_csv(f"{caminho_dados}focos21se.csv", index = False)
print(focos21se.info())
print("~"*80)
print(focos21se.dtypes)
print("~"*80)
print(focos21se)
print("="*80)

print("\n \n CASOS DE DENGUE \n")
casos21.to_csv(f"{caminho_dados}casos21.csv", index = False)
print(casos21.info())
print("~"*80)
print(casos21.dtypes)
print("~"*80)
print(casos21)
print("="*80)

print("\n \n CASOS DE DENGUE / SEMANA EPIDEMIOLÓGICA \n")
casos21se.to_csv(f"{caminho_dados}casos21se.csv", index = False)
print(casos21se.info())
print("~"*80)
print(casos21se.dtypes)
print("~"*80)
print(casos21se)
print("="*80)

print("\n \n PRECIPITAÇÃO \n")
merge21.to_csv(f"{caminho_dados}merge21.csv", index = False)
print(merge21.info())
print("~"*80)
print(merge21.dtypes)
print("~"*80)
print(merge21)
print("="*80)

print("\n \n PRECIPITAÇÃO / SEMANA EPIDEMIOLÓGICA \n")
merge21se.to_csv(f"{caminho_dados}merge21se.csv", index = False)
print(merge21se.info())
print("~"*80)
print(merge21se.dtypes)
print("~"*80)
print(merge21se)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA \n")
tmin21.to_csv(f"{caminho_dados}tmin21.csv", index = False)
print(tmin21.info())
print("~"*80)
print(tmin21.dtypes)
print("~"*80)
print(tmin21)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA / SEMANA EPIDEMIOLÓGICA \n")
tmin21se.to_csv(f"{caminho_dados}tmin21se.csv", index = False)
print(tmin21se.info())
print("~"*80)
print(tmin21se.dtypes)
print("~"*80)
print(tmin21se)
print("="*80)

print("\n \n TEMPERATURA MÉDIA \n")
tmed21.to_csv(f"{caminho_dados}tmed21.csv", index = False)
print(tmed21.info())
print("~"*80)
print(tmed21.dtypes)
print("~"*80)
print(tmed21)
print("="*80)

print("\n \n TEMPERATURA MÉDIA / SEMANA EPIDEMIOLÓGICA \n")
tmed21se.to_csv(f"{caminho_dados}tmed21se.csv", index = False)
print(tmed21se.info())
print("~"*80)
print(tmed21se.dtypes)
print("~"*80)
print(tmed21se)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA \n")
tmax21.to_csv(f"{caminho_dados}tmax21.csv", index = False)
print(tmax21.info())
print("~"*80)
print(tmax21.dtypes)
print("~"*80)
print(tmax21)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA / SEMANA EPIDEMIOLÓGICA \n")
tmax21se.to_csv(f"{caminho_dados}tmax21se.csv", index = False)
print(tmax21se.info())
print("~"*80)
print(tmax21se.dtypes)
print("~"*80)
print(tmax21se)
print("="*80)

print("="*80)
print(f"Máximo Focos por Semana Epidemiológica: {focos21se.max().max()}, \n e Mínimo Focos por Semana Epidemiológica: {focos21se.min().min()}.")
print("~"*80)
print(f"Máximo Casos por Semana Epidemiológica: {casos21se.max().max()}, \n e Mínimo Casos por Semana Epidemiológica: {casos21se.min().min()}.")
print("~"*80)
print(f"Máximo Precipitação por Semana Epidemiológica: {merge21se.max().max()}, \n e Mínimo Precipitação por Semana Epidemiológica: {merge21se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Mínima por Semana Epidemiológica: {tmin21se.max().max()}, \n e Mínimo Temperatura Mínima por Semana Epidemiológica: {tmin21se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Média por Semana Epidemiológica: {tmed21se.max().max()}, \n e Mínimo Temperatura Média por Semana Epidemiológica: {tmed21se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Máxima por Semana Epidemiológica: {tmax21se.max().max()}, \n e Mínimo Temperatura Máxima por Semana Epidemiológica: {tmax21se.min().min()}.")
print("="*80)