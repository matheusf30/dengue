### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
from matplotlib import cm
import matplotlib.colors as cls
import matplotlib.dates as mdates  
import cmocean
from datetime import timedelta
import numpy as np
import seaborn as sns
import statsmodels as sm
import pymannkendall as mk
import xarray as xr
### Suporte
import sys
import os
### Tratando avisos
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


### Condições para Variar #######################################################

_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
"""
##################### Valores Booleanos ############ # sys.argv[0] is the script name itself and can be ignored!
_AUTOMATIZAR = sys.argv[1]   # True|False                    #####
_AUTOMATIZA = True if _AUTOMATIZAR == "True" else False      #####
_VISUALIZAR = sys.argv[2]    # True|False                    #####
_VISUALIZAR = True if _VISUALIZAR == "True" else False       #####
_SALVAR = sys.argv[3]        # True|False                    #####
_SALVAR = True if _SALVAR == "True" else False               #####
##################################################################
"""
##### Padrão ANSI ###############################################################
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"
#################################################################################

### Encaminhamento aos Diretórios
if _LOCAL == "GH": # _ = Variável Privada
	caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
	caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "IFSC":
	caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
	caminho_shp = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
	caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/"
	caminho_cartografia = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
	print(f"\n{red}CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!{reset}")
print(f"\n{green}OS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n{reset}\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos
casos = "sazonalidade_semanal_casos20.csv"
focos = "sazonalidade_semanal_focos20.csv"
prec = "sazonalidade_semanal_prec20.csv"
tmin = "sazonalidade_semanal_tmin20.csv"
tmed = "sazonalidade_semanal_tmed20.csv"
tmax = "sazonalidade_semanal_tmax20.csv"
serie_casos = "casos_dive_pivot_total.csv"
serie_focos = "focos_pivot.csv"
serie_prec = "prec_semana_ate_2023.csv"
serie_tmin = "tmin_semana_ate_2023.csv"
serie_tmed = "tmed_semana_ate_2023.csv"
serie_tmax = "tmax_semana_ate_2023.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
serie_casos = pd.read_csv(f"{caminho_dados}{serie_casos}", low_memory = False)
serie_focos = pd.read_csv(f"{caminho_dados}{serie_focos}", low_memory = False)
serie_prec = pd.read_csv(f"{caminho_dados}{serie_prec}", low_memory = False)
serie_tmin = pd.read_csv(f"{caminho_dados}{serie_tmin}", low_memory = False)
serie_tmed = pd.read_csv(f"{caminho_dados}{serie_tmed}", low_memory = False)
serie_tmax = pd.read_csv(f"{caminho_dados}{serie_tmax}", low_memory = False)

print(f"\n{green}CASOS\n{reset}{casos}\n")
print(f"\n{green}FOCOS\n{reset}{focos}\n")
print(f"\n{green}PRECIPITAÇÃO\n{reset}{prec}\n")
print(f"\n{green}TEMPERATURA MÍNIMA\n{reset}{tmin}\n")
print(f"\n{green}TEMPERATURA MÉDIA\n{reset}{tmed}\n")
print(f"\n{green}TEMPERATURA MÁXIMA\n{reset}{tmax}\n")
print(f"\n{green}CASOS (Série Histórica)\n{reset}{serie_casos}\n")
print(f"\n{green}FOCOS (Série Histórica)\n{reset}{serie_focos}\n")
print(f"\n{green}PRECIPITAÇÃO (Série Histórica)\n{reset}{serie_prec}\n")
print(f"\n{green}TEMPERATURA MÍNIMA (Série Histórica)\n{reset}{serie_tmin}\n")
print(f"\n{green}TEMPERATURA MÉDIA (Série Histórica)\n{reset}{serie_tmed}\n")
print(f"\n{green}TEMPERATURA MÁXIMA (Série Histórica)\n{reset}{serie_tmax}\n")

### Pré-Processamento (Climatologia)

joinville = pd.DataFrame()
joinville["semana"] = focos["semana_epi"]
joinville["casos"] = casos["JOINVILLE"]
joinville["focos"] = focos["JOINVILLE"]
joinville["prec"] = prec["JOINVILLE"]
joinville["tmin"] = tmin["JOINVILLE"]
joinville["tmed"] = tmed["JOINVILLE"]
joinville["tmax"] = tmax["JOINVILLE"]
print(f"\n{green}JOINVILLE\n{reset}{joinville}\n")
#sys.exit()

### Visualização Gráfica (SAZONALIDADE)
fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = joinville.index, y = joinville["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(joinville.index, joinville["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = joinville.index, y = joinville["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(joinville.index, joinville["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper left")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = joinville["semana"], y = joinville["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower left")
sns.lineplot(x = joinville.index, y = joinville["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima")
sns.lineplot(x = joinville.index, y = joinville["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = joinville.index, y = joinville["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE JOINVILLE, SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_joinville.pdf"
caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sazonalidade/"
#if _SALVAR == True:
os.makedirs(caminho_estatistica, exist_ok = True)
#plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 300,  bbox_inches = "tight", pad_inches = 0.0)
print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
#if _VISUALIZAR == True:
print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
plt.show()

### Pré-Processamento (Série Histórica)

serie_joinville = pd.DataFrame()
semanas = serie_casos["Semana"]
serie_joinville["Semana"] = semanas
serie_casos_j = serie_casos[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_casos_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "casos"})
serie_focos_j = serie_focos[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_focos_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "focos"})
serie_tmin_j = serie_tmin[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_tmin_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "tmin"})
serie_tmed_j = serie_tmed[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_tmed_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "tmed"})
serie_tmax_j = serie_tmax[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_tmax_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "tmax"})
serie_prec_j = serie_prec[["Semana", "JOINVILLE"]]
serie_joinville = serie_joinville.merge(serie_prec_j, how = "inner", on = "Semana")
serie_joinville = serie_joinville.rename(columns = {"JOINVILLE" : "prec"}) 
serie_joinville.to_csv(f"{caminho_dados}serie_historica_joinville.csv", index = False)
print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_dados}\n
NOME DO ARQUIVO: serie_historica_joinville.csv{reset}\n""")
serie_joinville["Semana"] = pd.to_datetime(serie_joinville["Semana"])
serie_joinville.set_index("Semana", inplace = True)
"""
#serie_joinville["str_semana"] = serie_joinville["Semana"]
serie_joinville["Semana"] = pd.to_datetime(serie_joinville["Semana"], errors = "coerce")
serie_joinville.set_index("Semana", inplace=True)
print(serie_joinville.index.tz)
"""
print(f"\n{green}JOINVILLE (Série Histórica)\n{reset}{serie_joinville}\n")

#sys.exit()

### Visualização Gráfica
fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = serie_joinville.index, y = serie_joinville["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(serie_joinville.index, serie_joinville["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = serie_joinville.index, y = serie_joinville["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(serie_joinville.index, serie_joinville["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper left")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
"""
serie_joinville_reset = serie_joinville.reset_index()
serie_joinville_reset["Semana"] = pd.to_datetime(serie_joinville_reset["Semana"]).dt.tz_localize(None)
serie_joinville_reset["Semana"] = pd.to_datetime(serie_joinville_reset["Semana"], errors = "coerce")
sns.barplot(x = serie_joinville_reset["Semana"], y = serie_joinville["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
"""
ax3.bar(serie_joinville.index, serie_joinville["prec"],
        color = "royalblue", alpha = 0.8, label = "Precipitação", width = 5)
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower left")
sns.lineplot(x = serie_joinville.index, y = serie_joinville["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima")
sns.lineplot(x = serie_joinville.index, y = serie_joinville["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = serie_joinville.index, y = serie_joinville["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper left")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
#xticks_por_ano = serie_joinville.groupby(serie_joinville.index.year).head(1).index
#axs[1].set_xticks(xticks_por_ano)
#axs[1].set_xticklabels([str(ano.year) for ano in xticks_por_ano])
axs[1].xaxis.set_major_locator(mdates.YearLocator())
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE JOINVILLE, SANTA CATARINA.")
print(f"\n{green}JOINVILLE (Série Histórica)\n{reset}{serie_joinville}\n")
nome_arquivo = f"esbmet25_distribuicao_historica_subplots_joinville.pdf"
caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sazonalidade/"
#if _SALVAR == True:
os.makedirs(caminho_estatistica, exist_ok = True)
#plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 300,  bbox_inches = "tight", pad_inches = 0.0)
print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
#if _VISUALIZAR == True:
print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
plt.show()

