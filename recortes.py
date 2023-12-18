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
## Bruto
"""
casos = "casos.csv"
focos = "focos.csv"
merge = "merge_novo.csv"
tmax = "tmax.csv"
tmed = "tmed.csv"
tmin = "tmin.csv"
"""
## Série Histórica / Semana Epidemiológica
casos = "casos.csv"
focos = "focos_se.csv"
merge = "merge_se.csv"
tmax = "tmax_se.csv"
tmed = "tmed_se.csv"
tmin = "tmin_se.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
"""
### Recorte Temporal e Transformação em datetime64[ns]
focos["data"] = pd.to_datetime(focos["data"])
focos = focos.sort_values(by = ["data"])
#focos21 = focos.iloc[3288:4018]

casos["data"] = pd.to_datetime(casos["data"])
casos = casos.sort_values(by = ["data"])
#casos21 = casos.iloc[364:]

merge["Data"] = merge["data"]
merge["data"] = pd.to_datetime(merge["data"])
merge = merge.sort_values(by = ["data"])
#merge21 = merge.iloc[7518:]

tmin["data"] = pd.to_datetime(tmin["data"])
tmin = tmin.sort_values(by = ["data"])
#tmin21 = tmin.iloc[7671:]

tmed["data"] = pd.to_datetime(tmed["data"])
tmed = tmed.sort_values(by = ["data"])
#tmed21 = tmed.iloc[7671:]

tmax["data"] = pd.to_datetime(tmax["data"])
tmax = tmax.sort_values(by = ["data"])
#tmax21 = tmax.iloc[7671:]


### Semanas Epidemiológicas e Agrupamentos 2021
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
"""
### Recortes 2022 (Série Histórica / Semana Epidemiológica) 
focos22se = focos.copy()
focos22se = focos22se.iloc[522:574, :]

casos22se = casos.copy()
casos22se = casos.iloc[417:, :]

merge22se = merge.copy()
merge22se = merge.iloc[1127:, :]

tmin22se = tmin.copy()
tmin22se = tmin22se.iloc[1149:, :]

tmed22se = tmed.copy()
tmed22se = tmed22se.iloc[1149:, :]

tmax22se = tmax.copy()
tmax22se = tmax22se.iloc[1149:, :]

"""

focos_se = focos.copy()
focos_se["semanaE"] = focos_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
focos_se = focos_se.groupby(["semanaE"]).sum(numeric_only = True)
focos_se.reset_index(inplace = True)
focos_seSH = focos_se.copy()
focos_seSH = focos_seSH.iloc[105:574, :]

casos_se = casos.copy()

casos_se["semanaE"] = casos_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
casos_se = casos_se.groupby(["semanaE"]).sum(numeric_only = True)
casos_se.reset_index(inplace = True)

merge_se = merge.copy()
merge_se["semanaE"] = merge_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
merge_se = merge_se.groupby(["semanaE"]).sum(numeric_only = True)
merge_se.reset_index(inplace = True)
merge_seSH = merge_se.copy()
merge_seSH = merge_seSH.iloc[710:, :]

tmin_se = tmin.copy()
tmin_se["semanaE"] = tmin_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmin_se = tmin_se.groupby(["semanaE"]).mean(numeric_only = True)
tmin_se.reset_index(inplace = True)
tmin_seSH = tmin_se.copy()
tmin_seSH = tmin_seSH.iloc[732: , :]

tmed_se = tmed.copy()
tmed_se["semanaE"] = tmed_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmed_se = tmed_se.groupby(["semanaE"]).mean(numeric_only = True)
tmed_se.reset_index(inplace = True)
tmed_seSH = tmed_se.copy()
tmed_seSH = tmed_seSH.iloc[732: , :]

tmax_se = tmax.copy()
tmax_se["semanaE"] = tmax_se["data"].dt.to_period("W-SAT").dt.to_timestamp()
tmax_se = tmax_se.groupby(["semanaE"]).mean(numeric_only = True)
tmax_se.reset_index(inplace = True)
tmax_seSH = tmax_se.copy()
tmax_seSH = tmax_seSH.iloc[732: , :]


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

print("\n \n FOCOS DE _Aedes aegypti_ - SÉRIE HISTÓRICA / SEMANA EPIDEMIOLÓGICA \n")
focos_seSH.to_csv(f"{caminho_dados}focos_seSH.csv", index = False)
print(focos_seSH.info())
print("~"*80)
print(focos_seSH.dtypes)
print("~"*80)
print(focos_seSH)
print("="*80)

print("\n \n CASOS DE DENGUE - ... / SEMANA EPIDEMIOLÓGICA \n")
casos_se.to_csv(f"{caminho_dados}casos_se.csv", index = False)
print(casos_se.info())
print("~"*80)
print(casos_se.dtypes)
print("~"*80)
print(casos_se)
print("="*80)

print("\n \n PRECIPITAÇÃO - SÉRIE HISTÓRICA / SEMANA EPIDEMIOLÓGICA \n")
merge_seSH.to_csv(f"{caminho_dados}merge_seSH.csv", index = False)
print(merge_seSH.info())
print("~"*80)
print(merge_seSH.dtypes)
print("~"*80)
print(merge_seSH)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA - SÉRIE HISTÓRICA / SEMANA EPIDEMIOLÓGICA \n")
tmin_seSH.to_csv(f"{caminho_dados}tmin_seSH.csv", index = False)
print(tmin_seSH.info())
print("~"*80)
print(tmin_seSH.dtypes)
print("~"*80)
print(tmin_seSH)
print("="*80)

print("\n \n TEMPERATURA MÉDIA - SÉRIE HISTÓRICA / SEMANA EPIDEMIOLÓGICA \n")
tmed_seSH.to_csv(f"{caminho_dados}tmed_seSH.csv", index = False)
print(tmed_seSH.info())
print("~"*80)
print(tmed_seSH.dtypes)
print("~"*80)
print(tmed_seSH)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA - SÉRIE HISTÓRICA / SEMANA EPIDEMIOLÓGICA \n")
tmax_seSH.to_csv(f"{caminho_dados}tmax_seSH.csv", index = False)
print(tmax_seSH.info())
print("~"*80)
print(tmax_seSH.dtypes)
print("~"*80)
print(tmax_seSH)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ / SEMANA EPIDEMIOLÓGICA \n")
focos_se.to_csv(f"{caminho_dados}focos_se.csv", index = False)
print(focos_se.info())
print("~"*80)
print(focos_se.dtypes)
print("~"*80)
print(focos_se)
print("="*80)

print("\n \n CASOS DE DENGUE / SEMANA EPIDEMIOLÓGICA \n")
casos_se.to_csv(f"{caminho_dados}casos_se.csv", index = False)
print(casos_se.info())
print("~"*80)
print(casos_se.dtypes)
print("~"*80)
print(casos_se)
print("="*80)

print("\n \n PRECIPITAÇÃO / SEMANA EPIDEMIOLÓGICA \n")
merge_se.to_csv(f"{caminho_dados}merge_se.csv", index = False)
print(merge_se.info())
print("~"*80)
print(merge_se.dtypes)
print("~"*80)
print(merge_se)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA / SEMANA EPIDEMIOLÓGICA \n")
tmin_se.to_csv(f"{caminho_dados}tmin_se.csv", index = False)
print(tmin_se.info())
print("~"*80)
print(tmin_se.dtypes)
print("~"*80)
print(tmin_se)
print("="*80)

print("\n \n TEMPERATURA MÉDIA / SEMANA EPIDEMIOLÓGICA \n")
tmed_se.to_csv(f"{caminho_dados}tmed_se.csv", index = False)
print(tmed_se.info())
print("~"*80)
print(tmed_se.dtypes)
print("~"*80)
print(tmed_se)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA / SEMANA EPIDEMIOLÓGICA \n")
tmax_se.to_csv(f"{caminho_dados}tmax_se.csv", index = False)
print(tmax_se.info())
print("~"*80)
print(tmax_se.dtypes)
print("~"*80)
print(tmax_se)
print(""*80)

"""
### Printando e Salvando Semanas Epidemiológicas de 2022
print("\n \n FOCOS DE _Aedes aegypti_ / SEMANA EPIDEMIOLÓGICA em 2022 \n")
focos22se.to_csv(f"{caminho_dados}focos22se.csv", index = False)
print(focos22se.info())
print("~"*80)
print(focos22se.dtypes)
print("~"*80)
print(focos22se)
print("="*80)

print("\n \n CASOS DE DENGUE / SEMANA EPIDEMIOLÓGICA \n")
casos22se.to_csv(f"{caminho_dados}casos22se.csv", index = False)
print(casos22se.info())
print("~"*80)
print(casos22se.dtypes)
print("~"*80)
print(casos22se)
print("="*80)

print("\n \n PRECIPITAÇÃO / SEMANA EPIDEMIOLÓGICA \n")
merge22se.to_csv(f"{caminho_dados}merge22se.csv", index = False)
print(merge22se.info())
print("~"*80)
print(merge22se.dtypes)
print("~"*80)
print(merge22se)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA / SEMANA EPIDEMIOLÓGICA \n")
tmin22se.to_csv(f"{caminho_dados}tmin22se.csv", index = False)
print(tmin22se.info())
print("~"*80)
print(tmin22se.dtypes)
print("~"*80)
print(tmin22se)
print("="*80)

print("\n \n TEMPERATURA MÉDIA / SEMANA EPIDEMIOLÓGICA \n")
tmed22se.to_csv(f"{caminho_dados}tmed22se.csv", index = False)
print(tmed22se.info())
print("~"*80)
print(tmed22se.dtypes)
print("~"*80)
print(tmed22se)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA / SEMANA EPIDEMIOLÓGICA \n")
tmax22se.to_csv(f"{caminho_dados}tmax22se.csv", index = False)
print(tmax22se.info())
print("~"*80)
print(tmax22se.dtypes)
print("~"*80)
print(tmax22se)
print("="*80)
"""
print("\n \n FOCOS DE _Aedes aegypti_ / SEMANA EPIDEMIOLÓGICA \n")
focos_se.to_csv(f"{caminho_dados}focos_se.csv", index = False)
print(focos_se.info())
print("~"*80)
print(focos_se.dtypes)
print("~"*80)
print(focos_se)
print("="*80)

print("\n \n CASOS DE DENGUE / SEMANA EPIDEMIOLÓGICA \n")
casos_se.to_csv(f"{caminho_dados}casos_se.csv", index = False)
print(casos_se.info())
print("~"*80)
print(casos_se.dtypes)
print("~"*80)
print(casos_se)
print("="*80)

print("\n \n PRECIPITAÇÃO / SEMANA EPIDEMIOLÓGICA \n")
merge_se.to_csv(f"{caminho_dados}merge_se.csv", index = False)
print(merge_se.info())
print("~"*80)
print(merge_se.dtypes)
print("~"*80)
print(merge_se)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA / SEMANA EPIDEMIOLÓGICA \n")
tmin_se.to_csv(f"{caminho_dados}tmin_se.csv", index = False)
print(tmin_se.info())
print("~"*80)
print(tmin_se.dtypes)
print("~"*80)
print(tmin_se)
print("="*80)

print("\n \n TEMPERATURA MÉDIA / SEMANA EPIDEMIOLÓGICA \n")
tmed_se.to_csv(f"{caminho_dados}tmed_se.csv", index = False)
print(tmed_se.info())
print("~"*80)
print(tmed_se.dtypes)
print("~"*80)
print(tmed_se)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA / SEMANA EPIDEMIOLÓGICA \n")
tmax_se.to_csv(f"{caminho_dados}tmax_se.csv", index = False)
print(tmax_se.info())
print("~"*80)
print(tmax_se.dtypes)
print("~"*80)
print(tmax_se)
print("="*80)

print("="*80)
print(f"Máximo Focos por Semana Epidemiológica: {focos_se.max().max()}, \n e Mínimo Focos por Semana Epidemiológica: {focos_se.min().min()}.")
print("~"*80)
print(f"Máximo Casos por Semana Epidemiológica: {casos_se.max().max()}, \n e Mínimo Casos por Semana Epidemiológica: {casos_se.min().min()}.")
print("~"*80)
print(f"Máximo Precipitação por Semana Epidemiológica: {merge_se.max().max()}, \n e Mínimo Precipitação por Semana Epidemiológica: {merge_se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Mínima por Semana Epidemiológica: {tmin_se.max().max()}, \n e Mínimo Temperatura Mínima por Semana Epidemiológica: {tmin_se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Média por Semana Epidemiológica: {tmed_se.max().max()}, \n e Mínimo Temperatura Média por Semana Epidemiológica: {tmed_se.min().min()}.")
print("~"*80)
print(f"Máximo Temperatura Máxima por Semana Epidemiológica: {tmax_se.max().max()}, \n e Mínimo Temperatura Máxima por Semana Epidemiológica: {tmax_se.min().min()}.")
print("="*80)

print(focos)
print(casos)
print(merge)
print(tmin)
print(tmed)
print(tmax)
"""
print(tmin)
print(tmed)
print(tmax)
"""
