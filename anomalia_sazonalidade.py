### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
from datetime import timedelta
import numpy as np
import seaborn as sns
import statsmodels as sm
import pymannkendall as mk
import xarray as xr
### Suporte
import sys
import os

### Condições para Variar #######################################################

_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"

##################### Valores Booleanos ############ # sys.argv[0] is the script name itself and can be ignored!
_AUTOMATIZAR = sys.argv[1]   # True|False                    #####
_AUTOMATIZA = True if _AUTOMATIZAR == "True" else False      #####
_VISUALIZAR = sys.argv[2]    # True|False                    #####
_VISUALIZAR = True if _VISUALIZAR == "True" else False       #####
_SALVAR = sys.argv[3]        # True|False                    #####
_SALVAR = True if _SALVAR == "True" else False               #####
##################################################################

_CIDADE = "Florianópolis" #"Florianópolis"#"Itajaí"#"Joinville"#"Chapecó"

_CIDADE = _CIDADE.upper()

############### Base para Troca de Caracteres
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}

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
elif _LOCAL == "CASA":
	caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
	caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _LOCAL == "IFSC":
	caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
	caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/"
	caminho_cartografia = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
	print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")


### Função para abrir arquivos

def abrir_sazonalidade(str_var):
	arq = f"sazonalidade_semanal_{str_var}.csv"
	arq = pd.read_csv(f"{caminho_dados}{arq}", low_memory = False)
	print(f"\n{green}SAZONALIDADE: {str_var.upper()}\n{reset}{arq}\n")
	return arq

def abrir_sem_sazonalidade(str_var):
	arq = f"sem_sazonalidade_{str_var}.csv"
	arq = pd.read_csv(f"{caminho_dados}{arq}", low_memory = False)
	print(f"\n{green}SEM SAZONALIDADE: {str_var.upper()}\n{reset}{arq}\n")
	return arq

def abrir_anomalia_estacionaria(str_var):
	arq = f"anomalia_estacionaria_{str_var}.csv"
	arq = pd.read_csv(f"{caminho_dados}{arq}", low_memory = False)
	print(f"\n{green}ANOMALIA ESTACIONÁRIA: {str_var.upper()}\n{reset}{arq}\n")
	return arq

### Execução

sazonal_casos = abrir_sazonalidade("casos")
sem_sazonal_casos = abrir_sem_sazonalidade("casos")
anomalia_estacionaria_casos = abrir_anomalia_estacionaria("casos")

sazonal_focos = abrir_sazonalidade("focos")
sem_sazonal_focos = abrir_sem_sazonalidade("focos")
anomalia_estacionaria_focos = abrir_anomalia_estacionaria("focos")

sazonal_prec = abrir_sazonalidade("prec")
sem_sazonal_prec = abrir_sem_sazonalidade("prec")
anomalia_estacionaria_prec = abrir_anomalia_estacionaria("prec")

sazonal_tmin = abrir_sazonalidade("tmin")
sem_sazonal_tmin = abrir_sem_sazonalidade("tmin")
anomalia_estacionaria_tmin = abrir_anomalia_estacionaria("tmin")

sazonal_tmed = abrir_sazonalidade("tmed")
sem_sazonal_tmed = abrir_sem_sazonalidade("tmed")
anomalia_estacionaria_tmed = abrir_anomalia_estacionaria("tmed")

sazonal_tmax = abrir_sazonalidade("tmax")
sem_sazonal_tmax = abrir_sem_sazonalidade("tmax")
anomalia_estacionaria_tmax = abrir_anomalia_estacionaria("tmax")










#sys.exit()
plt.figure(figsize = (12, 6), layout = "tight", frameon = False)
plt.gca().patch.set_facecolor("honeydew") #.gcf()
sns.barplot(x = media_semana["semana_epi"], y = media_semana["PREC"],
				color = "royalblue", linewidth = 1.5, alpha = 1, label = "Precipitação") #"cornflowerblue"
sns.lineplot(x = media_semana.index, y = media_semana["CASOS"],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
plt.fill_between(media_semana.index, media_semana["CASOS"], color = "purple", alpha = 0.3)
sns.lineplot(x = media_semana.index, y = media_semana["FOCOS"],
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
plt.fill_between(media_semana.index, media_semana["FOCOS"], color = "darkgreen", alpha = 0.35)
plt.xlabel("Semanas Epidemiológicas")
plt.ylabel("Número de Casos e Focos X Precipitação (mm)")
plt.legend(loc = "upper center")
ax2 = plt.gca().twinx()#.set_facecolor("honeydew")
sns.lineplot(x = media_semana.index, y = media_semana["TMIN"],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = media_semana.index, y = media_semana["TMED"],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = media_semana.index, y = media_semana["TMAX"],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
plt.title(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
ax2.set_ylabel("Temperaturas (C)")
ax2.legend(loc = "upper right")
ax2.grid(False)
#plt.show()
#sys.exit()



#sys.exit()
#sem_sazonal[["tmin","tmax", "obito"]].plot()
plt.figure(figsize = (12, 6), layout = "tight", frameon = False)
plt.gca().patch.set_facecolor("honeydew") #.gcf()
sns.barplot(x = sem_sazonal["semana"], y = sem_sazonal["PREC"],
				color = "royalblue", linewidth = 1.5, alpha = 1, label = "Precipitação") #"cornflowerblue"
sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["CASOS"],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
plt.fill_between(sem_sazonal.index, sem_sazonal["CASOS"], color = "purple", alpha = 0.3)
sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["FOCOS"],
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
plt.fill_between(sem_sazonal.index, sem_sazonal["FOCOS"], color = "darkgreen", alpha = 0.35)
plt.xlabel("Semanas Epidemiológicas na Série Histórica")
ano_serie = sem_sazonal["semana"].dt.year.unique()
print(f"{green}sem_sazonal['semana'].dt.year.unique()\n{reset}{sem_sazonal['semana'].dt.year.unique()}")
plt.xticks([sem_sazonal[sem_sazonal["semana"].dt.year == ano].index[0] for ano in ano_serie],
			[str(ano) for ano in ano_serie], rotation = "horizontal")
plt.ylabel("Número de Casos e Focos X Precipitação (mm)")
plt.legend(loc = "upper left")
ax2 = plt.gca().twinx()#.set_facecolor("honeydew")
sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMIN"], alpha = 0.5,
				color = "darkblue", linewidth = 1, label = "Temperatura Mínima")
sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMED"], alpha = 0.5,
				color = "orange", linewidth = 1, label = "Temperatura Média")
sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMAX"], alpha = 0.5,
				color = "red", linewidth = 1, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
plt.title(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSEM SAZONALIDADE, SÉRIE HISTÓRICA PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
ax2.set_ylabel("Temperaturas (C)")
ax2.legend(loc = "upper right")
ax2.grid(False)
#plt.show()
#sys.exit()
nome_arquivo = f"distribuicao_sem_sazonal_{_cidade}.pdf"
if _SALVAR == True:
	for velho, novo in troca.items():
		_cidade = _cidade.replace(velho, novo)
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/anomalia_estacionaria/"
	os.makedirs(caminho_correlacao, exist_ok = True)
	plt.savefig(f'{caminho_correlacao}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
	print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
if _VISUALIZAR == True:
	print(f"\n{cyan}Visualizando:\n{caminho_correlacao}{nome_arquivo}\n{reset}")
	plt.show()




plt.figure(figsize = (12, 6), layout = "tight", frameon = False)
#fig, axs = plt.subplots(2, 1, figsize = (12, 6), gridspec_kw = {"height_ratios": [5, 5]},
#								 sharex = True, layout = "constrained", frameon = False)
plt.gca().patch.set_facecolor("honeydew") #.gcf()
plt.barplot(x = sem_sazonal["semana"], y = anomalia_estacionaria["PREC"],
				color = "royalblue", linewidth = 1.5, alpha = 1, label = "Precipitação") #"cornflowerblue"
sns.lineplot(x = anomalia_estacionaria.index, y = anomalia_estacionaria["CASOS"],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
plt.fill_between(anomalia_estacionaria.index, anomalia_estacionaria["CASOS"], color = "purple", alpha = 0.3)
sns.lineplot(x = anomalia_estacionaria.index, y = anomalia_estacionaria["FOCOS"],
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
plt.fill_between(anomalia_estacionaria.index, anomalia_estacionaria["FOCOS"], color = "darkgreen", alpha = 0.35)
plt.xlabel("Semanas Epidemiológicas na Série Histórica")
ano_serie = sem_sazonal["semana"].dt.year.unique()
print(f"{green}sem_sazonal['semana'].dt.year.unique()\n{reset}{sem_sazonal['semana'].dt.year.unique()}")
plt.xticks([sem_sazonal[sem_sazonal["semana"].dt.year == ano].index[0] for ano in ano_serie],
			[str(ano) for ano in ano_serie], rotation = "horizontal")
plt.ylabel("Número de Casos e Focos X Precipitação (mm)")
plt.legend(loc = "upper left")
ax2 = plt.gca().twinx()#.set_facecolor("honeydew")
sns.lineplot(x = anomalia_estacionaria.index, y = anomalia_estacionaria["TMIN"], alpha = 0.5,
				color = "darkblue", linewidth = 1, label = "Temperatura Mínima")
sns.lineplot(x = anomalia_estacionaria.index, y = anomalia_estacionaria["TMED"], alpha = 0.5,
				color = "orange", linewidth = 1, label = "Temperatura Média")
sns.lineplot(x = anomalia_estacionaria.index, y = anomalia_estacionaria["TMAX"], alpha = 0.5,
				color = "red", linewidth = 1, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
plt.title(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nANOMALIA ESTACIONÁRIA, SÉRIE HISTÓRICA PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
ax2.set_ylabel("Temperaturas (C)")
ax2.legend(loc = "upper right")
ax2.grid(False)
#plt.show()
nome_arquivo = f"distribuicao_anomaliaestacionaria_{_cidade}.pdf"
if _SALVAR == True:
	for velho, novo in troca.items():
		_cidade = _cidade.replace(velho, novo)
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/anomalia_estacionaria/"
	os.makedirs(caminho_correlacao, exist_ok = True)
	plt.savefig(f'{caminho_correlacao}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
	print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
if _VISUALIZAR == True:
	print(f"\n{cyan}Visualizando:\n{caminho_correlacao}{nome_arquivo}\n{reset}")
	plt.show()



