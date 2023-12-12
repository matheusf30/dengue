### Bibliotecas Correlatas
import matplotlib.pyplot as plt               
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm
#import sys

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação das variáveis pelos arquivos
 # Dados Diários às partir de 2021
"""
casos = "casos21.csv"
focos = "focos21.csv"
merge = "merge21.csv"
tmax = "tmax21.csv"
tmed = "tmed21.csv"
tmin = "tmin21.csv"
"""

 # Semanas Epidemiológicas à partir de 2021 / Semana Epidemiológica
"""
casos = "casos21se.csv"
focos = "focos21se.csv"
merge = "merge21se.csv"
tmax = "tmax21se.csv"
tmed = "tmed21se.csv"
tmin = "tmin21se.csv"
"""

 # Semanas Epidemiológicas da Série Histórica

casos = "casos_se.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
tmin = "tmin_seSH.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")

### Transformação em floats de menor bits
"""
focos = focos.astype(np.float16)
casos = casos.astype(np.float16)
merge = merge.astype(np.float16)
tmin = tmin.astype(np.float16)
tmed = tmed.astype(np.float16)
tmax = tmax.astype(np.float16)
"""
### Printando dados e informações
print("\n \n FOCOS DE _Aedes aegypti_ \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)

print("\n \n CASOS DE DENGUE \n")
print(casos.info())
print("~"*80)
print(casos.dtypes)
print("~"*80)
print(casos)
print("="*80)

print("\n \n PRECIPITAÇÃO \n")
print(merge.info())
print("~"*80)
print(merge.dtypes)
print("~"*80)
print(merge)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA \n")
print(tmin.info())
print("~"*80)
print(tmin.dtypes)
print("~"*80)
print(tmin)

print("\n \n TEMPERATURA MÉDIA \n")
print(tmed.info())
print("~"*80)
print(tmed.dtypes)
print("~"*80)
print(tmed)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA \n")
print(tmax.info())
print("~"*80)
print(tmax.dtypes)
print("~"*80)
print(tmax)
print("="*80)

### Selecionando Município e Manipulando Correlações

### Recorte Município (Florianópolis)

corr_cidade_base = focos[["Palhoça", "Florianópolis"]]
corr_cidade_base = corr_cidade_base.rename(columns={"Florianópolis" : "Focos"})
#corr_cidade_base["semanaE"] = pd.to_datetime(corr_cidade_base["semanE"])
#corr_cidade_base = corr_cidade_base.sort_values(by = ["SemanaE"])
corr_cidade_base["Log_Focos"] = np.log(corr_cidade_base["Focos"] + 1)
corr_cidade_base = corr_cidade_base.drop(["Palhoça"], axis = "columns")
del focos

print("\n \n MATRIZ DE CORRELAÇÃO (Início) \n")
print(corr_cidade_base.info())
print("~"*80)
print(corr_cidade_base.dtypes)
print("~"*80)
print(corr_cidade_base)
print("="*80)


### Base Focos-Casos

corr_cidade_base["Casos"] = casos["Florianópolis"]
corr_cidade_base["Log_Casos"] = np.log(corr_cidade_base["Casos"] + 1)
del casos

print("\n \n MATRIZ DE CORRELAÇÃO (Base) \n")
print(corr_cidade_base.info())
print("~"*80)
print(corr_cidade_base.dtypes)
print("~"*80)
print(corr_cidade_base)

### Correlação Base

#correlacao_base = corr_cidade_base.corr(method = "pearson")#.round(4)
correlacao_base = corr_cidade_base.corr(method = "spearman")#.round(4)
#correlacao_base = corr_cidade_base.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base)
print("Método de Spearman \n", correlacao_base)
#print("Método de Kendall \n", correlacao_base)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) \n *Spearman", weight = "bold", size = "medium")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig("resulto.png", bbox_inches = "tight", pad_inches = 0.0)


### Precipitação

corr_cidade_base_prec = corr_cidade_base.copy()
corr_cidade_base_prec["Precipitação"] = merge["Florianópolis"]
corr_cidade_base_prec["Log_Precipitação"] = np.log(corr_cidade_base_prec["Precipitação"] + 1)

print("\n \n MATRIZ DE CORRELAÇÃO (Precipitação) \n")
print(corr_cidade_base_prec.info())
print("~"*80)
print(corr_cidade_base_prec.dtypes)
print("~"*80)
print(corr_cidade_base_prec)

#correlacao_base_prec = corr_cidade_base_prec.corr(method = "pearson")#.round(4)
correlacao_base_prec = corr_cidade_base_prec.corr(method = "spearman")#.round(4)
#correlacao_base_prec = corr_cidade_base_prec.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base_prec)
print("Método de Spearman \n", correlacao_base_prec)
#print("Método de Kendall \n", correlacao_base_prec)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base_prec, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Precipitação \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Precipitação \n *Spearman", weight = "bold", size = "medium")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Precipitação \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig("resulto.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_base_prec


### Temperatura Mínima

corr_cidade_base_tmin = corr_cidade_base.copy()
corr_cidade_base_tmin["Temperatura Mínima"] = tmin["Florianópolis"]
corr_cidade_base_tmin["Log_Temperatura_Mínima"] = np.log(corr_cidade_base_tmin["Temperatura Mínima"] + 1)

print("\n \n MATRIZ DE CORRELAÇÃO (Temperatura Mínima) \n")
print(corr_cidade_base_tmin.info())
print("~"*80)
print(corr_cidade_base_tmin.dtypes)
print("~"*80)
print(corr_cidade_base_tmin)

#correlacao_base_tmin = corr_cidade_base_tmin.corr(method = "pearson")#.round(4)
correlacao_base_tmin = corr_cidade_base_tmin.corr(method = "spearman")#.round(4)
#correlacao_base_tmin = corr_cidade_base_tmin.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base_tmin)
print("Método de Spearman \n", correlacao_base_tmin)
#print("Método de Kendall \n", correlacao_base_tmin)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base_tmin, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Mínima \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Mínima \n *Spearman", weight = "bold", size = "medium")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Mínima \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig("resulto.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_base_tmin

### Temperatura Média

corr_cidade_base_tmed = corr_cidade_base.copy()
corr_cidade_base_tmed["Temperatura Média"] = tmed[ "Florianópolis"]
corr_cidade_base_tmed["Log_Temperatura_Média"] = np.log(corr_cidade_base_tmed["Temperatura Média"] + 1)

print("\n \n MATRIZ DE CORRELAÇÃO (Temperatura Média) \n")
print(corr_cidade_base_tmed.info())
print("~"*80)
print(corr_cidade_base_tmed.dtypes)
print("~"*80)
print(corr_cidade_base_tmed)

#correlacao_base_tmed = corr_cidade_base_tmed.corr(method = "pearson")#.round(4)
correlacao_base_tmed = corr_cidade_base_tmed.corr(method = "spearman")#.round(4)
#correlacao_base_tmed = corr_cidade_base_tmed.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base_tmed)
print("Método de Spearman \n", correlacao_base_tmed)
#print("Método de Kendall \n", correlacao_base_tmed)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base_tmed, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Média \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Média \n *Spearman", weight = "bold", size = "medium")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Média \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig("resulto.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_base_tmed

### Temperatura Máxima

corr_cidade_base_tmax = corr_cidade_base.copy()
corr_cidade_base_tmax["Temperatura Máxima"] = tmax["Florianópolis"]
corr_cidade_base_tmax["Log_Temperatura_Máxima"] = np.log(corr_cidade_base_tmax["Temperatura Máxima"] + 1)

print("\n \n MATRIZ DE CORRELAÇÃO (Temperatura Máxima) \n")
print(corr_cidade_base_tmax.info())
print("~"*80)
print(corr_cidade_base_tmax.dtypes)
print("~"*80)
print(corr_cidade_base_tmax)

#correlacao_base_tmax = corr_cidade_base_tmax.corr(method = "pearson")#.round(4)
correlacao_base_tmax = corr_cidade_base_tmax.corr(method = "spearman")#.round(4)
#correlacao_base_tmax = corr_cidade_base_tmax.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base_tmax)
print("Método de Spearman \n", correlacao_base_tmax)
#print("Método de Kendall \n", correlacao_base_tmax)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base_tmax, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Máxima \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Máxima \n *Spearman", weight = "bold", size = "medium")
#fig.suptitle("Correlação* Base \n (Focos e Casos em Florianópolis) e Temperatura Máxima \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig("resulto.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_base_tmax

### Base e Clima

corr_cidade_total = corr_cidade_base.copy()
corr_cidade_total["Precipitação"] = merge["Florianópolis"]
corr_cidade_total["Log_Precipitação"] = np.log(corr_cidade_total["Precipitação"] + 1)
corr_cidade_total["Temperatura Mínima"] = tmin["Florianópolis"]
corr_cidade_total["Log_Temperatura_Mínima"] = np.log(corr_cidade_total["Temperatura Mínima"] + 1)
corr_cidade_total["Temperatura Média"] = tmed["Florianópolis"]
corr_cidade_total["Log_Temperatura_Média"] = np.log(corr_cidade_total["Temperatura Média"] + 1)
corr_cidade_total["Temperatura Máxima"] = tmax["Florianópolis"]
corr_cidade_total["Log_Temperatura_Máxima"] = np.log(corr_cidade_total["Temperatura Máxima"] + 1)
del merge
del tmin
del tmed
del tmax

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima) \n")
print(corr_cidade_total.info())
print("~"*80)
print(corr_cidade_total.dtypes)
print("~"*80)
print(corr_cidade_total)

#correlacao_base_total = corr_cidade_total.corr(method = "pearson")#.round(4)
correlacao_base_total = corr_cidade_total.corr(method = "spearman")#.round(4)
#correlacao_base_total = corr_cidade_total.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_base_total)
print("Método de Spearman \n", correlacao_base_total)
#print("Método de Kendall \n", correlacao_base_total)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_base_total, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("Correlação* \n (Focos, Casos e Variáveis Climáticas) em Florianópolis \n *Pearson", weight = "bold", size = "medium")
fig.suptitle("Correlação*  \n (Focos, Casos e Variáveis Climáticas) em Florianópolis \n *Spearman (sem retroagir, à partir de 2014)", weight = "bold", size = "medium")
#fig.suptitle("Correlação* \n (Focos, Casos e Variáveis Climáticas) em Florianópolis \n *Kendall", weight = "bold", size = "medium")
plt.show()
#plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_semRetroagir2014_Florianópolis.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_total
