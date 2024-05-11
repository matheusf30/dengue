### Bibliotecas Correlatas
import matplotlib.pyplot as plt               
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm

### Condições para Variar #######################################################

_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"

_retroagir = 3 # Semanas Epidemiológicas

cidade = "Florianópolis"
#################################################################################

### Encaminhamento aos Diretórios
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
    caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos
casos = "casos_dive_pivot_total.csv"  # TabNet/DiveSC
#casos = "casos_pivot_pospandemia.csv" # TabNet/DataSUS
focos = "focos_pivot.csv"
unicos = "casos_unicos.csv"
prec = "prec_semana_ate_2023.csv"
tmin = "tmin_semana_ate_2023.csv"
tmed = "tmed_semana_ate_2023.csv"
tmax = "tmax_semana_ate_2023.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

#cbar = https://matplotlib.org/3.1.0/tutorials/colors/colorbar_only.html


### Base e Clima (sem retroagir)
## 0 (testando arquivo.csv base)
print(f"\n \n MATRIZ DE CORRELAÇÃO ({metodo.title()}; Base e Clima; sem retroagir [TESTE]) \n")
print(fm0cm0.info())
print("~"*80)
print(fm0cm0.dtypes)
print("~"*80)
print(fm0cm0)
#
correlacao_fm0cm0 = fm0cm0.corr(method = f"{metodo}")#.round(4)

print("="*80)
print(f"Método de {metodo.title()} \n", correlacao_fm0cm0)
print("="*80)
#
fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm0, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de {metodo.title()}; durante {ano}; sem retroagir [TESTE])", weight = "bold", size = "medium") 
plt.show()
#plt.savefig(f"{caminho_correlacao}Correlação{metodo.title()}_{ano}fm0cm0_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
#del fm0cm0
del correlacao_fm0cm0
"""
#EPIDEMIOLOGIA
## 1 (Casos com 1 Semana Epidemiológica de diferença)
fm0cm1 = fm0cm0.copy()
fm0cm1[casos] = fm0cm1[casos].shift(1)
fm0cm1.dropna(axis = 0, inplace = True)
print(f"\n \n MATRIZ DE CORRELAÇÃO ({metodo.title()}; Base e Clima; retroagindo Casos em 1 Semana Epidemiológica) \n")
print(fm0cm1.info())
print("~"*80)
print(fm0cm1.dtypes)
print("~"*80)
print(fm0cm1)

correlacao_fm0cm1 = fm0cm1.corr(method = f"{metodo}")#.round(4)

print("="*80)
print(f"Método de {metodo.title()} \n", correlacao_fm0cm1)
print("="*80)

fig, ax = plt.subplots()
sns.heatmap(correlacao_fm0cm1, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de {metodo.title()}; durante {ano}; Retroagindo Casos em 1 Semana Epidemiológica)", weight = "bold", size = "medium")
plt.show()
#plt.savefig(f"{caminho_correlacao}Correlação{metodo.title()}_{ano}fm0cm1_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm0cm1
del correlacao_fm0cm1

for fococaso in retro_caso:

## +1 (Casos com 2 Semanas Epidemiológicas de diferença)
	fm0cmx = fm0cm0.copy()
	fm0cmx[casos] = fm0cmx[casos].shift(fococaso)
	fm0cmx.dropna(axis = 0, inplace = True)
	print(f"\n \n MATRIZ DE CORRELAÇÃO ({metodo.title()}; Base e Clima; retroagindo Casos em {fococaso} Semanas Epidemiológicas) \n")
	print(fm0cmx.info())
	print("~"*80)
	print(fm0cmx.dtypes)
	print("~"*80)
	print(fm0cmx)
	
	correlacao_fm0cmx = fm0cmx.corr(method = f"{metodo}")#.round(4)
	
	print("="*80)
	print(f"Método de {metodo.title()} \n", correlacao_fm0cmx)
	print("="*80)
	
	fig, ax = plt.subplots()
	sns.heatmap(correlacao_fm0cmx, annot = True, cmap = "tab20c", linewidth = 0.5)
	ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
	fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de {metodo.title()}; durante {ano}; Retroagindo Casos em {fococaso} Semanas Epidemiológicas)", weight = "bold", size = "medium") 
	plt.show()
	#plt.savefig(f"{caminho_correlacao}Correlação{metodo.title()}_{ano}fm0cm{fococaso}_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
	del fm0cmx
	del correlacao_fm0cmx

### CLIMA
## 1 (Variáveis Climáticas com 1 Semana Epidemiológica de diferença)
fm1cm1 = fm0cm0.copy()
fm1cm1[clima] = fm1cm1[clima].shift(1)
fm1cm1.dropna(axis = 0, inplace = True)

print(f"\n \n MATRIZ DE CORRELAÇÃO ({metodo.title()}; Base e Clima; retroagindo Variáveis Climatológicas em 1 Semana Epidemiológica) \n")
print(fm1cm1.info())
print("~"*80)
print(fm1cm1.dtypes)
print("~"*80)
print(fm1cm1)

correlacao_fm1cm1 = fm1cm1.corr(method = f"{metodo}")#.round(4)

print("="*80)
print(f"Método de {metodo.title()} \n", correlacao_fm1cm1)
print("="*80)

fig, ax = plt.subplots()
sns.heatmap(correlacao_fm1cm1, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de {metodo.title()}; durante {ano}; Retroagindo Variáveis Climatológicas em 1 Semana Epidemiológica)", weight = "bold", size = "medium")
plt.show()
#plt.savefig(f"{caminho_correlacao}Correlação{metodo.title()}_{ano}fm1cm1_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
del fm1cm1
del correlacao_fm1cm1
"""
for fococlima in retro_clima:
	## +1 (Variáveis Climáticas com 2 Semanas Epidemiológicas de diferença)
	fmxcmx = fm0cm0.copy()
	fmxcmx[clima] = fmxcmx[clima].shift(fococlima)
	fmxcmx.dropna(axis = 0, inplace = True)

	print(f"\n \n MATRIZ DE CORRELAÇÃO ({metodo.title()}; Base e Clima; retroagindo Variáveis Climatológicas em {fococlima} Semanas Epidemiológicas) \n")
	print(fmxcmx.info())
	print("~"*80)
	print(fmxcmx.dtypes)
	print("~"*80)
	print(fmxcmx)
	
	correlacao_fmxcmx = fmxcmx.corr(method = f"{metodo}")#.round(4)

	print("="*80)
	print(f"Método de {metodo.title()} \n", correlacao_fmxcmx)
	print("="*80)

	fig, ax = plt.subplots()
	sns.heatmap(correlacao_fmxcmx, annot = True, cmap = "tab20c", linewidth = 0.5)
	ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
	fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM FLORIANÓPOLIS \n *(Método de {metodo.title()}; durante {ano}; Retroagindo Variáveis Climatológicas em {fococlima} Semana Epidemiológica)", weight = "bold", size = "medium")
	plt.show()
	#plt.savefig(f"{caminho_correlacao}Correlação{metodo.title()}_anofm{fococlima}cm{retro_clima}_{cidade}.png", bbox_inches = "tight", pad_inches = 0.0)
	del fmxcmx
	del correlacao_fmxcmx

