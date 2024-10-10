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
"""
_CIDADE = "Florianópolis" #"Florianópolis"#"Itajaí"#"Joinville"#"Chapecó"

_CIDADE = _CIDADE.upper()
"""
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

def cidade(troca, str_cidade):
	_cidade = str_cidade.upper()
	for velho, novo in troca.items():
		_cidade = _cidade.replace(velho, novo)
	return _cidade.lower()

def grafico_sazonalidade(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax, str_cidade):
	_CIDADE = str_cidade.upper()
	_cidade = cidade(troca, str_cidade)
	print(f"\n_cidade: {_cidade}\n_CIDADE: {_CIDADE}\n")
	plt.figure(figsize = (12, 6), layout = "tight", frameon = False)
	plt.gca().patch.set_facecolor("honeydew") #.gcf()
	sns.barplot(x = csv_prec["semana_epi"], y = csv_prec[_CIDADE],
					color = "royalblue", linewidth = 1.5, alpha = 1, label = "Precipitação")
	sns.lineplot(x = csv_casos.index, y = csv_casos[_CIDADE],
					color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
	plt.fill_between(csv_casos.index, csv_casos[_CIDADE], color = "purple", alpha = 0.3)
	sns.lineplot(x = csv_focos.index, y = csv_focos[_CIDADE],
					color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
	plt.fill_between(csv_focos.index, csv_focos[_CIDADE], color = "darkgreen", alpha = 0.35)
	plt.xlabel("Semanas Epidemiológicas")
	plt.ylabel("Número de Casos e Focos X Precipitação (mm)")
	plt.legend(loc = "upper center")
	ax2 = plt.gca().twinx()#.set_facecolor("honeydew")
	sns.lineplot(x = csv_tmin.index, y = csv_tmin[_CIDADE],
					color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
	sns.lineplot(x = csv_tmed.index, y = csv_tmed[_CIDADE],
					color = "orange", linewidth = 1.5, label = "Temperatura Média")
	sns.lineplot(x = csv_tmax.index, y = csv_tmax[_CIDADE],
					color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
	plt.title(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
	ax2.set_ylabel("Temperaturas (C)")
	ax2.legend(loc = "upper right")
	ax2.grid(False)
	nome_arquivo = f"distribuicao_sazonal_{_cidade}.pdf"
	caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sazonalidade/"
	if _SALVAR == True:
		os.makedirs(caminho_correlacao, exist_ok = True)
		plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	if _VISUALIZAR == True:
		print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
		plt.show()

def grafico_sazonalidade_subplots(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax, str_cidade):
	_CIDADE = str_cidade.upper()
	_cidade = cidade(troca, str_cidade)
	print(f"\n_cidade: {_cidade}\n_CIDADE: {_CIDADE}\n")
	fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
	axs[0].set_facecolor("honeydew") #.gcf()
	ax2 = axs[0].twinx()
	sns.lineplot(x = csv_casos.index, y = csv_casos[_CIDADE], ax = axs[0],
					color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
	axs[0].fill_between(csv_casos.index, csv_casos[_CIDADE], color = "purple", alpha = 0.3)
	axs[0].set_ylabel("Casos de Dengue")
	axs[0].legend(loc = "upper center")
	sns.lineplot(x = csv_focos.index, y = csv_focos[_CIDADE],  ax = ax2,
					color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
	ax2.fill_between(csv_focos.index, csv_focos[_CIDADE], color = "darkgreen", alpha = 0.35)
	ax2.set_ylabel("Focos de _Aedes_ sp.")
	ax2.legend(loc = "upper right")
	axs[1].set_facecolor("honeydew") #.gcf()
	ax3 = axs[1].twinx()#.set_facecolor("honeydew")
	sns.barplot(x = csv_prec["semana_epi"], y = csv_prec[_CIDADE],  ax = ax3,
					color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
	ax3.set_ylabel("Precipitação (mm)")
	ax3.legend(loc = "lower right")
	sns.lineplot(x = csv_tmin.index, y = csv_tmin[_CIDADE],  ax = axs[1],
					color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
	sns.lineplot(x = csv_tmed.index, y = csv_tmed[_CIDADE],  ax = axs[1],
					color = "orange", linewidth = 1.5, label = "Temperatura Média")
	sns.lineplot(x = csv_tmax.index, y = csv_tmax[_CIDADE],  ax = axs[1],
					color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
	axs[1].set_ylabel("Temperaturas (C)")
	axs[1].legend(loc = "upper center")
	axs[1].grid(False)
	axs[1].set_xlabel("Semanas Epidemiológicas")
	fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
	nome_arquivo = f"distribuicao_sazonal_subplots_{_cidade}.pdf"
	caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sazonalidade/"
	if _SALVAR == True:
		os.makedirs(caminho_correlacao, exist_ok = True)
		plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	if _VISUALIZAR == True:
		print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
		plt.show()

def grafico_sem_sazonalidade(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax, str_cidade):
	_CIDADE = str_cidade.upper()
	_cidade = cidade(troca, str_cidade)
	csv_casos["semana"] = pd.to_datetime(csv_casos["semana"], errors = "coerce")
	csv_focos["semana"] = pd.to_datetime(csv_focos["semana"], errors = "coerce")
	csv_prec["semana"] = pd.to_datetime(csv_prec["semana"], errors = "coerce")
	csv_tmin["semana"] = pd.to_datetime(csv_tmin["semana"], errors = "coerce")
	csv_tmed["semana"] = pd.to_datetime(csv_tmed["semana"], errors = "coerce")
	csv_tmax["semana"] = pd.to_datetime(csv_tmax["semana"], errors = "coerce")
	ano_serie = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
	csv_casos = csv_casos[csv_casos["semana"].dt.year.isin(ano_serie)]
	csv_focos = csv_focos[csv_focos["semana"].dt.year.isin(ano_serie)]
	csv_prec = csv_prec[csv_prec["semana"].dt.year.isin(ano_serie)]
	csv_tmin = csv_tmin[csv_tmin["semana"].dt.year.isin(ano_serie)]
	csv_tmed = csv_tmed[csv_tmed["semana"].dt.year.isin(ano_serie)]
	csv_tmax = csv_tmax[csv_tmax["semana"].dt.year.isin(ano_serie)]
	csv_casos.set_index("semana", inplace = True)
	csv_focos.set_index("semana", inplace = True)
	csv_prec.set_index("semana", inplace = True)
	csv_tmin.set_index("semana", inplace = True)
	csv_tmed.set_index("semana", inplace = True)
	csv_tmax.set_index("semana", inplace = True)
	print(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax)
	fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
	axs[0].set_facecolor("honeydew")
	ax2 = axs[0].twinx()
	sns.lineplot(x = csv_casos.index, y = csv_casos[_CIDADE], ax = axs[0],
					color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
	axs[0].fill_between(csv_casos.index, csv_casos[_CIDADE], color = "purple", alpha = 0.3)
	axs[0].set_ylabel("Casos de Dengue")
	axs[0].legend(loc = "upper left")
	axs[0].grid(axis = "x")
	sns.lineplot(x = csv_focos.index, y = csv_focos[_CIDADE],  ax = ax2,
					color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
	ax2.fill_between(csv_focos.index, csv_focos[_CIDADE], color = "darkgreen", alpha = 0.35)
	ax2.set_ylabel("Focos de _Aedes_ sp.")
	ax2.legend(loc = "upper center")
	axs[1].set_facecolor("honeydew")
	sns.lineplot(x = csv_tmin.index, y = csv_tmin[_CIDADE].rolling(8).mean(), alpha = 0.5, ax = axs[1],
					color = "darkblue", linewidth = 1.2, linestyle = ":", label = "Temperatura Mínima")
	sns.lineplot(x = csv_tmed.index, y = csv_tmed[_CIDADE].rolling(8).mean(), alpha = 0.8, ax = axs[1],
					color = "orange", linewidth = 1.2, label = "Temperatura Média")
	axs[1].fill_between(csv_tmed.index, csv_tmed[_CIDADE].rolling(8).mean(), color = "orange", alpha = 0.35)
	sns.lineplot(x = csv_tmax.index, y = csv_tmax[_CIDADE].rolling(8).mean(), alpha = 0.5,  ax = axs[1],
					color = "red", linewidth = 1.2, linestyle = "--", label = "Temperatura Máxima")
	ax3 = axs[1].twinx()
	ax3.bar(x = csv_prec.index, height = csv_prec[_CIDADE], width = 10,
					color = "royalblue", alpha = 0.8, label = "Precipitação")
	ax3.set_ylabel("Precipitação (mm)")
	ax3.legend(loc = "upper right")
	axs[1].set_ylabel("Temperaturas (C)")
	axs[1].legend(loc = "upper left")
	axs[1].grid(False)
	axs[1].grid(axis = "x")
	axs[1].set_xlabel("Semanas Epidemiológicas")
	fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS* (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSEM SAZONALIDADE PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.\n*(Média móvel de 8 semanas epidemiológicas).")
	nome_arquivo = f"distribuicao_sem_sazonal_{_cidade}.pdf"
	caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sem_sazonal/"
	if _SALVAR == True:
		os.makedirs(caminho_estatistica, exist_ok = True)
		plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	if _VISUALIZAR == True:
		print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
		plt.show()

def grafico_anomalia_estacionaria(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax, str_cidade):
	_CIDADE = str_cidade.upper()
	_cidade = cidade(troca, str_cidade)
	csv_casos["semana"] = pd.to_datetime(csv_casos["semana"], errors = "coerce")
	csv_focos["semana"] = pd.to_datetime(csv_focos["semana"], errors = "coerce")
	csv_prec["semana"] = pd.to_datetime(csv_prec["semana"], errors = "coerce")
	csv_tmin["semana"] = pd.to_datetime(csv_tmin["semana"], errors = "coerce")
	csv_tmed["semana"] = pd.to_datetime(csv_tmed["semana"], errors = "coerce")
	csv_tmax["semana"] = pd.to_datetime(csv_tmax["semana"], errors = "coerce")
	ano_serie = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
	csv_casos = csv_casos[csv_casos["semana"].dt.year.isin(ano_serie)]
	csv_focos = csv_focos[csv_focos["semana"].dt.year.isin(ano_serie)]
	csv_prec = csv_prec[csv_prec["semana"].dt.year.isin(ano_serie)]
	csv_tmin = csv_tmin[csv_tmin["semana"].dt.year.isin(ano_serie)]
	csv_tmed = csv_tmed[csv_tmed["semana"].dt.year.isin(ano_serie)]
	csv_tmax = csv_tmax[csv_tmax["semana"].dt.year.isin(ano_serie)]
	csv_casos.set_index("semana", inplace = True)
	csv_focos.set_index("semana", inplace = True)
	csv_prec.set_index("semana", inplace = True)
	csv_tmin.set_index("semana", inplace = True)
	csv_tmed.set_index("semana", inplace = True)
	csv_tmax.set_index("semana", inplace = True)
	print(csv_casos, csv_focos, csv_prec, csv_tmin, csv_tmed, csv_tmax)
	fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
	axs[0].set_facecolor("honeydew")
	ax2 = axs[0].twinx()
	sns.lineplot(x = csv_casos.index, y = csv_casos[_CIDADE], ax = axs[0],
					color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
	axs[0].fill_between(csv_casos.index, csv_casos[_CIDADE], color = "purple", alpha = 0.3)
	axs[0].set_ylabel("Casos de Dengue")
	axs[0].legend(loc = "upper left")
	axs[0].grid(axis = "x")
	sns.lineplot(x = csv_focos.index, y = csv_focos[_CIDADE],  ax = ax2,
					color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
	ax2.fill_between(csv_focos.index, csv_focos[_CIDADE], color = "darkgreen", alpha = 0.35)
	ax2.set_ylabel("Focos de _Aedes_ sp.")
	ax2.legend(loc = "upper center")
	axs[1].set_facecolor("honeydew")
	sns.lineplot(x = csv_tmin.index, y = csv_tmin[_CIDADE].rolling(8).mean(), alpha = 0.5, ax = axs[1],
					color = "darkblue", linewidth = 1.2, linestyle = ":", label = "Temperatura Mínima")
	sns.lineplot(x = csv_tmed.index, y = csv_tmed[_CIDADE].rolling(8).mean(), alpha = 0.8, ax = axs[1],
					color = "orange", linewidth = 1.2, label = "Temperatura Média")
	axs[1].fill_between(csv_tmed.index, csv_tmed[_CIDADE].rolling(8).mean(), color = "orange", alpha = 0.35)
	sns.lineplot(x = csv_tmax.index, y = csv_tmax[_CIDADE].rolling(8).mean(), alpha = 0.5,  ax = axs[1],
					color = "red", linewidth = 1.2, linestyle = "--", label = "Temperatura Máxima")
	ax3 = axs[1].twinx()
	ax3.bar(x = csv_prec.index, height = csv_prec[_CIDADE], width = 10,
					color = "royalblue", alpha = 0.7, label = "Precipitação")
	ax3.set_ylabel("Precipitação (mm)")
	ax3.legend(loc = "upper right")
	axs[1].set_ylabel("Temperaturas (C)")
	axs[1].legend(loc = "upper left")
	axs[1].grid(False)
	axs[1].grid(axis = "x")
	axs[1].set_xlabel("Semanas Epidemiológicas")
	fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS* (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nANOMALIAS ESTACIONÁRIAS PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.\n*(Média móvel de 8 semanas epidemiológicas).")
	nome_arquivo = f"distribuicao_anomalia_estacionaria_{_cidade}.pdf"
	caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/anomalia_estacionaria/"
	if _SALVAR == True:
		os.makedirs(caminho_estatistica, exist_ok = True)
		plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	if _VISUALIZAR == True:
		print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
		plt.show()

### Execução
# Organizando variáveis

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

### Visualizações

lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó",
					"Blumenau", "Criciúma", "Concórdia", "Xanxerê",
					"Jaraguá do Sul", "Palhoça", "São José", "Biguaçu"]
for str_cidade in lista_cidades:
	grafico_anomalia_estacionaria(anomalia_estacionaria_casos, anomalia_estacionaria_focos,
									anomalia_estacionaria_prec, anomalia_estacionaria_tmin,
									anomalia_estacionaria_tmed, anomalia_estacionaria_tmax, str_cidade)
	grafico_sem_sazonalidade(sem_sazonal_casos, sem_sazonal_focos, sem_sazonal_prec,
							sem_sazonal_tmin, sem_sazonal_tmed, sem_sazonal_tmax, str_cidade)
	grafico_sazonalidade_subplots(sazonal_casos, sazonal_focos, sazonal_prec,
									sazonal_tmin, sazonal_tmed, sazonal_tmax, str_cidade)
	grafico_sazonalidade(sazonal_casos, sazonal_focos, sazonal_prec,
							sazonal_tmin, sazonal_tmed, sazonal_tmax, str_cidade)

"""
colunas_cidades = sazonal_focos.drop(columns = "semana_epi")
lista_cidades = colunas_cidades.columns
print(f"\n{green}lista_cidades:\n{reset}{lista_cidades}\n")
for str_cidade in lista_cidades:
	grafico_sazonalidade(sazonal_casos, sazonal_focos, sazonal_prec,
							sazonal_tmin, sazonal_tmed, sazonal_tmax, str_cidade)
"""

