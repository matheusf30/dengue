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

# Arquivos de Matriz Retroagindo Tempos
# fm (focos_momento-retroação) / cm (casos_momento-retroação)
# cada momento é referente a um número inteiro de Semana Epidemiológica retroagida

cidade = "Florianópolis"
#fm0cm0 = f"matriz_{cidade}_fm0cm0.csv"
#fm0cm0 = f"matriz21_{cidade}_fm0cm0.csv" # à partir de 2021
fm0cm0 = f"matriz22_{cidade}_fm0cm0.csv"  # apenas 2022

### Abrindo Arquivos
fm0cm0 = pd.read_csv(f"{caminho_dados}{fm0cm0}")

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
print("Método de Pearson \n", correlacao_fm0cm0)
#print("Método de Spearman \n", correlacao_fm0cm0)
#print("Método de Kendall \n", correlacao_fm0cm0)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm0, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; sem retroagir [TESTE])", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm0cm0_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
#del fm0cm0
del correlacao_fm0cm0

#EPIDEMIOLOGIA
## 1 (Casos com 1 Semana Epidemiológica de diferença)
casos = ["Casos", "Log_Casos"]
fm0cm1 = fm0cm0.copy()
fm0cm1[casos] = fm0cm1[casos].shift(1)
fm0cm1.dropna(axis = 0, inplace = True)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo Casos em 1 Semana Epidemiológica) \n")
print(fm0cm1.info())
print("~"*80)
print(fm0cm1.dtypes)
print("~"*80)
print(fm0cm1)
#
correlacao_fm0cm1 = fm0cm1.corr(method = "pearson")#.round(4)
#correlacao_fm0cm1 = fm0cm1.corr(method = "spearman")#.round(4)
#correlacao_fm0cm1 = fm0cm1.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm0cm1)
#print("Método de Spearman \n", correlacao_fm0cm1)
#print("Método de Kendall \n", correlacao_fm0cm1)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm1, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; em 2022; Retroagindo Casos em 1 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; em 2022; Retroagindo Casos em 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; em 2022; Retroagindo Casos em 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2022fm0cm1_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm1
del correlacao_fm0cm1

## 2 (Casos com 2 Semanas Epidemiológicas de diferença)
fm0cm2 = fm0cm0.copy()
fm0cm2[casos] = fm0cm2[casos].shift(2)
fm0cm2.dropna(axis = 0, inplace = True)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo Casos em 2 Semanas Epidemiológicas) \n")
print(fm0cm2.info())
print("~"*80)
print(fm0cm2.dtypes)
print("~"*80)
print(fm0cm2)
#
correlacao_fm0cm2 = fm0cm2.corr(method = "pearson")#.round(4)
#correlacao_fm0cm2 = fm0cm2.corr(method = "spearman")#.round(4)
#correlacao_fm0cm2 = fm0cm2.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm0cm2)
#print("Método de Spearman \n", correlacao_fm0cm2)
#print("Método de Kendall \n", correlacao_fm0cm2)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm2, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; em 2022; Retroagindo Casos em 2 Semanas Epidemiológicas)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; em 2022; Retroagindo Casos em 2 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; em 2022; Retroagindo Casos em 2 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2022fm0cm2_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm2
del correlacao_fm0cm2

## 3 (Casos com 3 Semanas Epidemiológicas de diferença)
fm0cm3 = fm0cm0.copy()
fm0cm3[casos] = fm0cm3[casos].shift(3)
fm0cm3.dropna(axis = 0, inplace = True)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo Casos em 3 Semanas Epidemiológicas) \n")
print(fm0cm3.info())
print("~"*80)
print(fm0cm3.dtypes)
print("~"*80)
print(fm0cm3)
#
correlacao_fm0cm3 = fm0cm3.corr(method = "pearson")#.round(4)
#correlacao_fm0cm3 = fm0cm3.corr(method = "spearman")#.round(4)
#correlacao_fm0cm3 = fm0cm3.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm0cm3)
#print("Método de Spearman \n", correlacao_fm0cm3)
#print("Método de Kendall \n", correlacao_fm0cm3)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm3, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; em 2022; Retroagindo Casos em 3 Semanas Epidemiológicas)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; em 2022; Retroagindo Casos em 3 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; em 2022; Retroagindo Casos em 3 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2022fm0cm3_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm3
del correlacao_fm0cm3

## 4 (Casos com 4 Semanas Epidemiológicas de diferença)
fm0cm4 = fm0cm0.copy()
fm0cm4[casos] = fm0cm4[casos].shift(4)
fm0cm4.dropna(axis = 0, inplace = True)
print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo Casos em 4 Semanas Epidemiológicas) \n")
print(fm0cm4.info())
print("~"*80)
print(fm0cm4.dtypes)
print("~"*80)
print(fm0cm4)
#
correlacao_fm0cm4 = fm0cm4.corr(method = "pearson")#.round(4)
#correlacao_fm0cm4 = fm0cm4.corr(method = "spearman")#.round(4)
#correlacao_fm0cm4 = fm0cm4.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm0cm4)
#print("Método de Spearman \n", correlacao_fm0cm4)
#print("Método de Kendall \n", correlacao_fm0cm4)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm4, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; em 2022; Retroagindo Casos em 4 Semanas Epidemiológicas)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; em 2022; Retroagindo Casos em 4 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; em 2022; Retroagindo Casos em 4 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2022fm0cm4_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm4
del correlacao_fm0cm4


### CLIMA
## 1 (Variáveis Climáticas com 1 Semana Epidemiológica de diferença)
fm1cm1 = fm0cm0.copy()
clima = ["Precipitação", "Log_Precipitação", "Temperatura Mínima", "Log_Temperatura_Mínima", \
         "Temperatura Média", "Log_Temperatura_Média", "Temperatura Máxima", "Log_Temperatura_Máxima"]
#retroacao = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
fm1cm1[clima] = fm1cm1[clima].shift(1)#(periods = retroacao)
fm1cm1.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 1 Semana Epidemiológica) \n")
print(fm1cm1.info())
print("~"*80)
print(fm1cm1.dtypes)
print("~"*80)
print(fm1cm1)
#
correlacao_fm1cm1 = fm1cm1.corr(method = "pearson")#.round(4)
#correlacao_fm1cm1 = fm1cm1.corr(method = "spearman")#.round(4)
#correlacao_fm1cm1 = fm1cm1.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm1cm1)
#print("Método de Spearman \n", correlacao_fm1cm1)
#print("Método de Kendall \n", correlacao_fm1cm1)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm1cm1, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 1 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm1cm1_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm1cm1
del correlacao_fm1cm1

## 2 (Variáveis Climáticas com 2 Semanas Epidemiológicas de diferença)
fm2cm2 = fm0cm0.copy()
fm2cm2[clima] = fm2cm2[clima].shift(2)
fm2cm2.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 2 Semanas Epidemiológicas) \n")
print(fm2cm2.info())
print("~"*80)
print(fm2cm2.dtypes)
print("~"*80)
print(fm2cm2)
#
correlacao_fm2cm2 = fm2cm2.corr(method = "pearson")#.round(4)
#correlacao_fm2cm2 = fm2cm2.corr(method = "spearman")#.round(4)
#correlacao_fm2cm2 = fm2cm2.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm2cm2)
#print("Método de Spearman \n", correlacao_fm2cm2)
#print("Método de Kendall \n", correlacao_fm2cm2)
print("="*80)
#fm2cm2 = fm0cm0.copy()
fm2cm2[clima] = fm2cm2[clima].shift(2)
fm2cm2.dropna(axis = 0, inplace = True)
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm2cm2, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 2 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 2 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 2 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm2cm2_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm2cm2
del correlacao_fm2cm2

## 3 (Variáveis Climáticas com 3 Semanas Epidemiológicas de diferença)
fm3cm3 = fm0cm0.copy()
fm3cm3[clima] = fm3cm3[clima].shift(3)
fm3cm3.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 3 Semanas Epidemiológicas) \n")
print(fm3cm3.info())
print("~"*80)
print(fm3cm3.dtypes)
print("~"*80)
print(fm3cm3)
#
correlacao_fm3cm3 = fm3cm3.corr(method = "pearson")#.round(4)
#correlacao_fm3cm3 = fm3cm3.corr(method = "spearman")#.round(4)
#correlacao_fm3cm3 = fm3cm3.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm3cm3)
#print("Método de Spearman \n", correlacao_fm3cm3)
#print("Método de Kendall \n", correlacao_fm3cm3)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm3cm3, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 3 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 3 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 3 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm3cm3_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm3cm3
del correlacao_fm3cm3

## 4 (Variáveis Climáticas com 4 Semanas Epidemiológicas de diferença)
fm4cm4 = fm0cm0.copy()
fm4cm4[clima] = fm4cm4[clima].shift(4)
fm4cm4.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 4 Semanas Epidemiológicas) \n")
print(fm4cm4.info())
print("~"*80)
print(fm4cm4.dtypes)
print("~"*80)
print(fm4cm4)
#
correlacao_fm4cm4 = fm4cm4.corr(method = "pearson")#.round(4)
#correlacao_fm4cm4 = fm4cm4.corr(method = "spearman")#.round(4)
#correlacao_fm4cm4 = fm4cm4.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm4cm4)
#print("Método de Spearman \n", correlacao_fm4cm4)
#print("Método de Kendall \n", correlacao_fm4cm4)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm4cm4, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 4 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 4 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 4 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm4cm4_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm4cm4
del correlacao_fm4cm4

## 5 (Variáveis Climáticas com 5 Semanas Epidemiológicas de diferença)
fm5cm5 = fm0cm0.copy()
fm5cm5[clima] = fm5cm5[clima].shift(5)
fm5cm5.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 5 Semanas Epidemiológicas) \n")
print(fm5cm5.info())
print("~"*80)
print(fm5cm5.dtypes)
print("~"*80)
print(fm5cm5)
#
correlacao_fm5cm5 = fm5cm5.corr(method = "pearson")#.round(4)
#correlacao_fm5cm5 = fm5cm5.corr(method = "spearman")#.round(4)
#correlacao_fm5cm5 = fm5cm5.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm5cm5)
#print("Método de Spearman \n", correlacao_fm5cm5)
#print("Método de Kendall \n", correlacao_fm5cm5)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm5cm5, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 5 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 5 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 5 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm5cm5_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm5cm5
del correlacao_fm5cm5

## 6 (Variáveis Climáticas com 6 Semanas Epidemiológicas de diferença)
fm6cm6 = fm0cm0.copy()
fm6cm6[clima] = fm6cm6[clima].shift(6)
fm6cm6.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 6 Semanas Epidemiológicas) \n")
print(fm6cm6.info())
print("~"*80)
print(fm6cm6.dtypes)
print("~"*80)
print(fm6cm6)
#
correlacao_fm6cm6 = fm6cm6.corr(method = "pearson")#.round(4)
#correlacao_fm6cm6 = fm6cm6.corr(method = "spearman")#.round(4)
#correlacao_fm6cm6 = fm6cm6.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm6cm6)
#print("Método de Spearman \n", correlacao_fm6cm6)
#print("Método de Kendall \n", correlacao_fm6cm6)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm6cm6, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 6 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 6 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 6 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm6cm6_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm6cm6
del correlacao_fm6cm6

## 7 (Variáveis Climáticas com 7 Semanas Epidemiológicas de diferença)
fm7cm7 = fm0cm0.copy()
fm7cm7[clima] = fm7cm7[clima].shift(7)
fm7cm7.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 7 Semanas Epidemiológicas) \n")
print(fm7cm7.info())
print("~"*80)
print(fm7cm7.dtypes)
print("~"*80)
print(fm7cm7)
#
correlacao_fm7cm7 = fm7cm7.corr(method = "pearson")#.round(4)
#correlacao_fm7cm7 = fm7cm7.corr(method = "spearman")#.round(4)
#correlacao_fm7cm7 = fm7cm7.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm7cm7)
#print("Método de Spearman \n", correlacao_fm7cm7)
#print("Método de Kendall \n", correlacao_fm7cm7)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm7cm7, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 7 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 7 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 7 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm7cm7_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm7cm7
del correlacao_fm7cm7

## 8 (Variáveis Climáticas com 8 Semanas Epidemiológicas de diferença)
fm8cm8 = fm0cm0.copy()
fm8cm8[clima] = fm8cm8[clima].shift(8)
fm8cm8.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 8 Semanas Epidemiológicas) \n")
print(fm8cm8.info())
print("~"*80)
print(fm8cm8.dtypes)
print("~"*80)
print(fm8cm8)
#
correlacao_fm8cm8 = fm8cm8.corr(method = "pearson")#.round(4)
#correlacao_fm8cm8 = fm8cm8.corr(method = "spearman")#.round(4)
#correlacao_fm8cm8 = fm8cm8.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm8cm8)
#print("Método de Spearman \n", correlacao_fm8cm8)
#print("Método de Kendall \n", correlacao_fm8cm8)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm8cm8, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 8 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 8 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 8 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm8cm8_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm8cm8
del correlacao_fm8cm8

## 9 (Variáveis Climáticas com 9 Semanas Epidemiológicas de diferença)
fm9cm9 = fm0cm0.copy()
fm9cm9[clima] = fm9cm9[clima].shift(9)
fm9cm9.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 9 Semanas Epidemiológicas) \n")
print(fm9cm9.info())
print("~"*80)
print(fm9cm9.dtypes)
print("~"*80)
print(fm9cm9)
#
correlacao_fm9cm9 = fm9cm9.corr(method = "pearson")#.round(4)
#correlacao_fm9cm9 = fm9cm9.corr(method = "spearman")#.round(4)
#correlacao_fm9cm9 = fm9cm9.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm9cm9)
#print("Método de Spearman \n", correlacao_fm9cm9)
#print("Método de Kendall \n", correlacao_fm9cm9)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm9cm9, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 9 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 9 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 9 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm9cm9_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm9cm9
del correlacao_fm9cm9

## 10 (Variáveis Climáticas com 10 Semanas Epidemiológicas de diferença)
fm10cm10 = fm0cm0.copy()
fm10cm10[clima] = fm10cm10[clima].shift(10)
fm10cm10.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 10 Semanas Epidemiológicas) \n")
print(fm10cm10.info())
print("~"*80)
print(fm10cm10.dtypes)
print("~"*80)
print(fm10cm10)
#
correlacao_fm10cm10 = fm10cm10.corr(method = "pearson")#.round(4)
#correlacao_fm10cm10 = fm10cm10.corr(method = "spearman")#.round(4)
#correlacao_fm10cm10 = fm10cm10.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm10cm10)
#print("Método de Spearman \n", correlacao_fm10cm10)
#print("Método de Kendall \n", correlacao_fm10cm10)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm10cm10, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 10 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 10 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 10 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm10cm10_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm10cm10
del correlacao_fm10cm10

## 11 (Variáveis Climáticas com 11 Semanas Epidemiológicas de diferença)
fm11cm11 = fm0cm0.copy()
fm11cm11[clima] = fm11cm11[clima].shift(11)
fm11cm11.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 11 Semanas Epidemiológicas) \n")
print(fm11cm11.info())
print("~"*80)
print(fm11cm11.dtypes)
print("~"*80)
print(fm11cm11)
#
correlacao_fm11cm11 = fm11cm11.corr(method = "pearson")#.round(4)
#correlacao_fm11cm11 = fm11cm11.corr(method = "spearman")#.round(4)
#correlacao_fm11cm11 = fm11cm11.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm11cm11)
#print("Método de Spearman \n", correlacao_fm11cm11)
#print("Método de Kendall \n", correlacao_fm11cm11)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm11cm11, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 11 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 11 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 11 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm11cm11_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm11cm11
del correlacao_fm11cm11

## 12 (Variáveis Climáticas com 12 Semanas Epidemiológicas de diferença)
fm12cm12 = fm0cm0.copy()
fm12cm12[clima] = fm12cm12[clima].shift(12)
fm12cm12.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 12 Semanas Epidemiológicas) \n")
print(fm12cm12.info())
print("~"*80)
print(fm12cm12.dtypes)
print("~"*80)
print(fm12cm12)
#
correlacao_fm12cm12 = fm12cm12.corr(method = "pearson")#.round(4)
#correlacao_fm12cm12 = fm12cm12.corr(method = "spearman")#.round(4)
#correlacao_fm12cm12 = fm12cm12.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm12cm12)
#print("Método de Spearman \n", correlacao_fm12cm12)
#print("Método de Kendall \n", correlacao_fm12cm12)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm12cm12, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 12 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 12 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 12 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm12cm12_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm12cm12
del correlacao_fm12cm12

## 13 (Variáveis Climáticas com 13 Semanas Epidemiológicas de diferença)
fm13cm13 = fm0cm0.copy()
fm13cm13[clima] = fm13cm13[clima].shift(13)
fm13cm13.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 13 Semanas Epidemiológicas) \n")
print(fm13cm13.info())
print("~"*80)
print(fm13cm13.dtypes)
print("~"*80)
print(fm13cm13)
#
correlacao_fm13cm13 = fm13cm13.corr(method = "pearson")#.round(4)
#correlacao_fm13cm13 = fm13cm13.corr(method = "spearman")#.round(4)
#correlacao_fm13cm13 = fm13cm13.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm13cm13)
#print("Método de Spearman \n", correlacao_fm13cm13)
#print("Método de Kendall \n", correlacao_fm13cm13)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm13cm13, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 13 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 13 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 13 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm13cm13_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm13cm13
del correlacao_fm13cm13

## 14 (Variáveis Climáticas com 14 Semanas Epidemiológicas de diferença)
fm14cm14 = fm0cm0.copy()
fm14cm14[clima] = fm14cm14[clima].shift(14)
fm14cm14.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 14 Semanas Epidemiológicas) \n")
print(fm14cm14.info())
print("~"*80)
print(fm14cm14.dtypes)
print("~"*80)
print(fm14cm14)
#
correlacao_fm14cm14 = fm14cm14.corr(method = "pearson")#.round(4)
#correlacao_fm14cm14 = fm14cm14.corr(method = "spearman")#.round(4)
#correlacao_fm14cm14 = fm14cm14.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm14cm14)
#print("Método de Spearman \n", correlacao_fm14cm14)
#print("Método de Kendall \n", correlacao_fm14cm14)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm14cm14, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 14 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 14 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 14 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm14cm14_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm14cm14
del correlacao_fm14cm14

## 15 (Variáveis Climáticas com 15 Semanas Epidemiológicas de diferença)
fm15cm15 = fm0cm0.copy()
fm15cm15[clima] = fm15cm15[clima].shift(15)
fm15cm15.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 15 Semanas Epidemiológicas) \n")
print(fm15cm15.info())
print("~"*80)
print(fm15cm15.dtypes)
print("~"*80)
print(fm15cm15)
#
correlacao_fm15cm15 = fm15cm15.corr(method = "pearson")#.round(4)
#correlacao_fm15cm15 = fm15cm15.corr(method = "spearman")#.round(4)
#correlacao_fm15cm15 = fm15cm15.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm15cm15)
#print("Método de Spearman \n", correlacao_fm15cm15)
#print("Método de Kendall \n", correlacao_fm15cm15)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm15cm15, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 15 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 15 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 15 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm15cm15_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm15cm15
del correlacao_fm15cm15

## 16 (Variáveis Climáticas com 16 Semanas Epidemiológicas de diferença)
fm16cm16 = fm0cm0.copy()
fm16cm16[clima] = fm16cm16[clima].shift(16)
fm16cm16.dropna(axis = 0, inplace = True)

print("\n \n MATRIZ DE CORRELAÇÃO (Base e Clima; retroagindo 16 Semanas Epidemiológicas) \n")
print(fm16cm16.info())
print("~"*80)
print(fm16cm16.dtypes)
print("~"*80)
print(fm16cm16)
#
correlacao_fm16cm16 = fm16cm16.corr(method = "pearson")#.round(4)
#correlacao_fm16cm16 = fm16cm16.corr(method = "spearman")#.round(4)
#correlacao_fm16cm16 = fm16cm16.corr(method = "kendall")#.round(4)
#
print("="*80)
print("Método de Pearson \n", correlacao_fm16cm16)
#print("Método de Spearman \n", correlacao_fm16cm16)
#print("Método de Kendall \n", correlacao_fm16cm16)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm16cm16, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Pearson; à partir de 2014; Retroagindo 16 Semana Epidemiológica)", weight = "bold", size = "medium")
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Spearman; à partir de 2014; Retroagindo 16 Semanas Epidemiológicas)", weight = "bold", size = "medium") 
#fig.suptitle("MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de Kendall; à partir de 2014; Retroagindo 16 Semana Epidemiológica)", weight = "bold", size = "medium") 
plt.show()
plt.savefig(f"{caminho_correlacao}CorrelaçãoSpearman_2014fm16cm16_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm16cm16
del correlacao_fm16cm16

