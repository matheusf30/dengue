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
# Casos já são por Semana Epimediológica

casos = "casos.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
tmin = "tmin_seSH.csv"

# Arquivos de Matriz Retroagindo Tempos
# fm (focos_momento-retroação) / cm (casos_momento-retroação)
# cada momento é referente a um número inteiro de Semana Epidemiológica retroagida

cidade = "Florianópolis"
fm0cm0 = f"matriz_{cidade}_fm0cm0.csv"
fm1cm1 = f"matriz_{cidade}_fm1cm1.csv"
fm2cm2 = f"matriz_{cidade}_fm2cm2.csv"
fm3cm3 = f"matriz_{cidade}_fm3cm3.csv"
fm4cm4 = f"matriz_{cidade}_fm4cm4.csv"
fm5cm5 = f"matriz_{cidade}_fm5cm5.csv"
fm6cm6 = f"matriz_{cidade}_fm6cm6.csv"
fm7cm7 = f"matriz_{cidade}_fm7cm7.csv"
fm8cm8 = f"matriz_{cidade}_fm8cm8.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
fm0cm0 = pd.read_csv(f"{caminho_dados}{fm0cm0}")
fm1cm1 = pd.read_csv(f"{caminho_dados}{fm1cm1}")
fm2cm2 = pd.read_csv(f"{caminho_dados}{fm2cm2}")
fm3cm3 = pd.read_csv(f"{caminho_dados}{fm3cm3}")
fm4cm4 = pd.read_csv(f"{caminho_dados}{fm4cm4}")
fm5cm5 = pd.read_csv(f"{caminho_dados}{fm5cm5}")
fm6cm6 = pd.read_csv(f"{caminho_dados}{fm6cm6}")
fm7cm7 = pd.read_csv(f"{caminho_dados}{fm7cm7}")
fm8cm8 = pd.read_csv(f"{caminho_dados}{fm8cm8}")

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

"""
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
"""
### Base e Clima (sem retroagir)

corr_cidade_total = corr_cidade_base.copy()
corr_cidade_total["Precipitação"] = merge["Florianópolis"]
corr_cidade_total["Log_Precipitação"] = np.log(corr_cidade_total["Precipitação"] + 1)
corr_cidade_total["Temperatura Mínima"] = tmin["Florianópolis"]
corr_cidade_total["Log_Temperatura_Mínima"] = np.log(corr_cidade_total["Temperatura Mínima"] + 1)
corr_cidade_total["Temperatura Média"] = tmed["Florianópolis"]
corr_cidade_total["Log_Temperatura_Média"] = np.log(corr_cidade_total["Temperatura Média"] + 1)
corr_cidade_total["Temperatura Máxima"] = tmax["Florianópolis"]
corr_cidade_total["Log_Temperatura_Máxima"] = np.log(corr_cidade_total["Temperatura Máxima"] + 1)
corr_cidade_total.to_csv(f"{caminho_dados}matriz_Florianópolis_fm0cm0.csv", index = False)
del merge
del tmin
del tmed
del tmax

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; sem retroagir) \n")
print(corr_cidade_total.info())
print("~"*80)
print(corr_cidade_total.dtypes)
print("~"*80)
print(corr_cidade_total)
#
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
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; sem retroagir)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; sem retroagir)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; sem retroagir)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_semRetroagir2014_Florianópolis.png", bbox_inches = "tight", pad_inches = 0.0)
del corr_cidade_total
del correlacao_base_total

### Base e Clima (retroagindo)
## 0 (testando arquivo.csv base)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; sem retroagir [TESTE]) \n")
print(fm0cm0.info())
print("~"*80)
print(fm0cm0.dtypes)
print("~"*80)
print(fm0cm0)
#
#correlacao_fm0cm0 = fm0cm0.corr(method = "pearson")#.round(4)
correlacao_fm0cm0 = fm0cm0.corr(method = "spearman")#.round(4)
#correlacao_fm0cm0 = fm0cm0.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm0cm0)
print("Método de Spearman \n", correlacao_fm0cm0)
#print("Método de Kendall \n", correlacao_fm0cm0)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm0, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm0cm0_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm0
del correlacao_fm0cm0

## 1 (Variáveis Climáticas com 1 Semana Epidemiológica de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 1 Semana Epidemiológica) \n")
print(fm1cm1.info())
print("~"*80)
print(fm1cm1.dtypes)
print("~"*80)
print(fm1cm1)
#
#correlacao_fm1cm1 = fm1cm1.corr(method = "pearson")#.round(4)
correlacao_fm1cm1 = fm1cm1.corr(method = "spearman")#.round(4)
#correlacao_fm1cm1 = fm1cm1.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm1cm1)
print("Método de Spearman \n", correlacao_fm1cm1)
#print("Método de Kendall \n", correlacao_fm1cm1)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm1cm1, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm1cm1_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm1cm1
del correlacao_fm1cm1

## 2 (Variáveis Climáticas com 2 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 2 Semanas Epidemiológicas) \n")
print(fm2cm2.info())
print("~"*80)
print(fm2cm2.dtypes)
print("~"*80)
print(fm2cm2)
#
#correlacao_fm2cm2 = fm2cm2.corr(method = "pearson")#.round(4)
correlacao_fm2cm2 = fm2cm2.corr(method = "spearman")#.round(4)
#correlacao_fm2cm2 = fm2cm2.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm2cm2)
print("Método de Spearman \n", correlacao_fm2cm2)
#print("Método de Kendall \n", correlacao_fm2cm2)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm2cm2, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 2 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 2 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 2 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm2cm2_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm2cm2
del correlacao_fm2cm2

## 3 (Variáveis Climáticas com 3 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 3 Semanas Epidemiológicas) \n")
print(fm3cm3.info())
print("~"*80)
print(fm3cm3.dtypes)
print("~"*80)
print(fm3cm3)
#
#correlacao_fm3cm3 = fm3cm3.corr(method = "pearson")#.round(4)
correlacao_fm3cm3 = fm3cm3.corr(method = "spearman")#.round(4)
#correlacao_fm3cm3 = fm3cm3.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm3cm3)
print("Método de Spearman \n", correlacao_fm3cm3)
#print("Método de Kendall \n", correlacao_fm3cm3)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm3cm3, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 3 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 3 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 3 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm3cm3_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm3cm3
del correlacao_fm3cm3

## 4 (Variáveis Climáticas com 4 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 4 Semanas Epidemiológicas) \n")
print(fm4cm4.info())
print("~"*80)
print(fm4cm4.dtypes)
print("~"*80)
print(fm4cm4)
#
#correlacao_fm4cm4 = fm4cm4.corr(method = "pearson")#.round(4)
correlacao_fm4cm4 = fm4cm4.corr(method = "spearman")#.round(4)
#correlacao_fm4cm4 = fm4cm4.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm4cm4)
print("Método de Spearman \n", correlacao_fm4cm4)
#print("Método de Kendall \n", correlacao_fm4cm4)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm4cm4, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 4 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 4 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 4 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm4cm4_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm4cm4
del correlacao_fm4cm4

## 5 (Variáveis Climáticas com 5 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 5 Semanas Epidemiológicas) \n")
print(fm5cm5.info())
print("~"*80)
print(fm5cm5.dtypes)
print("~"*80)
print(fm5cm5)
#
#correlacao_fm5cm5 = fm5cm5.corr(method = "pearson")#.round(4)
correlacao_fm5cm5 = fm5cm5.corr(method = "spearman")#.round(4)
#correlacao_fm5cm5 = fm5cm5.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm5cm5)
print("Método de Spearman \n", correlacao_fm5cm5)
#print("Método de Kendall \n", correlacao_fm5cm5)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm5cm5, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 5 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 5 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 5 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm5cm5_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm5cm5
del correlacao_fm5cm5

## 6 (Variáveis Climáticas com 6 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 6 Semanas Epidemiológicas) \n")
print(fm6cm6.info())
print("~"*80)
print(fm6cm6.dtypes)
print("~"*80)
print(fm6cm6)
#
#correlacao_fm6cm6 = fm6cm6.corr(method = "pearson")#.round(4)
correlacao_fm6cm6 = fm6cm6.corr(method = "spearman")#.round(4)
#correlacao_fm6cm6 = fm6cm6.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm6cm6)
print("Método de Spearman \n", correlacao_fm6cm6)
#print("Método de Kendall \n", correlacao_fm6cm6)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm6cm6, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 6 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 6 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 6 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm6cm6_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm6cm6
del correlacao_fm6cm6

## 7 (Variáveis Climáticas com 7 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 7 Semanas Epidemiológicas) \n")
print(fm7cm7.info())
print("~"*80)
print(fm7cm7.dtypes)
print("~"*80)
print(fm7cm7)
#
#correlacao_fm7cm7 = fm7cm7.corr(method = "pearson")#.round(4)
correlacao_fm7cm7 = fm7cm7.corr(method = "spearman")#.round(4)
#correlacao_fm7cm7 = fm7cm7.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm7cm7)
print("Método de Spearman \n", correlacao_fm7cm7)
#print("Método de Kendall \n", correlacao_fm7cm7)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm7cm7, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 7 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 7 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 7 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm7cm7_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm7cm7
del correlacao_fm7cm7

## 8 (Variáveis Climáticas com 8 Semanas Epidemiológicas de diferença)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 8 Semanas Epidemiológicas) \n")
print(fm8cm8.info())
print("~"*80)
print(fm8cm8.dtypes)
print("~"*80)
print(fm8cm8)
#
#correlacao_fm8cm8 = fm8cm8.corr(method = "pearson")#.round(4)
correlacao_fm8cm8 = fm8cm8.corr(method = "spearman")#.round(4)
#correlacao_fm8cm8 = fm8cm8.corr(method = "kendall")#.round(4)
#
print("="*80)
#print("Método de Pearson \n", correlacao_fm8cm8)
print("Método de Spearman \n", correlacao_fm8cm8)
#print("Método de Kendall \n", correlacao_fm8cm8)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm8cm8, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 8 Semana Epidemiológica)", weight = "bold", size = "medium")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 8 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 8 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm8cm8_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm8cm8
del correlacao_fm8cm8

