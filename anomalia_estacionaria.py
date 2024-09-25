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

_RETROAGIR = 16 # Semanas Epidemiológicas
_ANO = "2023" # "2023" # "2022" # "2021" # "2020" # "total"
_CIDADE = "Florianópolis" #"Florianópolis"#"Itajaí"#"Joinville"#"Chapecó"
_METODO = "spearman" # "pearson" # "spearman" # "kendall"

_CIDADE = _CIDADE.upper()

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

### Renomeação das Variáveis pelos Arquivos
casos = "casos_dive_pivot_total.csv"  # TabNet/DiveSC
focos = "focos_pivot.csv"
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

print(f"\n{green}CASOS\n{reset}{casos}\n")
print(f"\n{green}FOCOS\n{reset}{focos}\n")
print(f"\n{green}PRECIPITAÇÃO\n{reset}{prec}\n")
print(f"\n{green}TEMPERATURA MÍNIMA\n{reset}{tmin}\n")
print(f"\n{green}TEMPERATURA MÉDIA\n{reset}{tmed}\n")
print(f"\n{green}TEMPERATURA MÁXIMA\n{reset}{tmax}\n")



############### Base para Troca de Caracteres
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}

#################################################################################
### Função Semana Epidemiológica (Semana que acabe no sábado tendo 4 dias iniciando no ano)
#################################################################################

def semana_epidemio(data):
    jan1sab = pd.Timestamp(year = data.year, month=1, day=1)
    sab1 = jan1sab + timedelta(days = (5 - jan1sab.weekday() + 7) % 7)
    if sab1.day >= 4:
        dias_inicio = (data - jan1sab).days
        semana_epi = (dias_inicio + 1) // 7 + 1
    else:
        semana_epi = (data - jan1sab).days // 7 + 1
    return semana_epi

def sazonalidade(csv, str_var):
	csv["semana"] = pd.to_datetime(csv["Semana"]).dt.date
	csv = csv.astype({"semana": "datetime64[ns]"})
	csv.drop(columns = "Semana", inplace = True)
	csv["semana_epi"] = csv['semana'].apply(semana_epidemio)
	print(f"\n{green}{str_var.upper()}\n{reset}{csv}\n{green}{str_var.upper()}.info\n{reset}{csv.info()}\n{green}{str_var.upper()}.dtypes\n{reset}{csv.dtypes}\n")
	print("="*80)
	colunas_csv = csv.drop(columns = ["semana", "semana_epi"])
	colunas = colunas_csv.columns
	media_semana = csv.groupby("semana_epi")[colunas].mean().round(2)
	media_semana.reset_index(inplace = True)
	print(f"\n{green}media_semana\n{reset}{media_semana}\n{green}media_semana.index\n{reset}{media_semana.index}")
	if _SALVAR == True:
		nome_arquivo = f"sazonalidade_semanal_{str_var}.csv"
		caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
		os.makedirs(caminho_dados, exist_ok = True)
		media_semana.to_csv(f"{caminho_dados}casos_dive_pivot_total.csv", index = False)
		#plt.savefig(f"{caminho_dados}{nome_arquivo}", format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	return media_semana

def tratando_sazonalidade(csv, str_var):
	csv["semana"] = pd.to_datetime(csv["Semana"]).dt.date
	csv = csv.astype({"semana": "datetime64[ns]"})
	csv.drop(columns = "Semana", inplace = True)
	csv["semana_epi"] = csv['semana'].apply(semana_epidemio)
	print(f"\n{green}{str_var.upper()}\n{reset}{csv}\n{green}{str_var.upper()}.info()\n{reset}{csv.info()}\n{green}{str_var.upper()}.dtypes\n{reset}{csv.dtypes}\n")
	print("="*80)
	colunas_csv = csv.drop(columns = ["semana", "semana_epi"])
	colunas = colunas_csv.columns
	media_semana = csv.groupby("semana_epi")[colunas].mean().round(2)
	media_semana.reset_index(inplace = True)
	print(f"\n{green}media_semana\n{reset}{media_semana}\n{green}media_semana.index\n{reset}{media_semana.index}")
	componente_sazonal = csv.merge(media_semana, left_on = "semana_epi", how = "left", suffixes = ("", "_media"), right_index = True)
	sem_sazonal = pd.DataFrame(index = csv.index)
	semanas  = componente_sazonal["semana"]
	componente_sazonal.drop(columns = "semana", inplace = True)
	print(f"{green}componente_sazonal\n{reset}{componente_sazonal}")
	for coluna in colunas:
		if coluna in componente_sazonal.columns:
			media_coluna = f"{coluna}_media"
			if media_coluna in componente_sazonal.columns:
				sem_sazonal[coluna] = csv[coluna] - componente_sazonal[media_coluna]
			else:
				print(f"{red}Coluna {media_coluna} não encontrada no componente sazonal!{reset}")
		else:
			print(f"{red}Coluna {coluna} não encontrada no csv!{reset}")
	#sem_sazonal.drop(columns = "semana_epi", inplace = True)
	sem_sazonal["semana"] = semanas
	sem_sazonal.dropna(inplace = True)
	#sem_sazonal = sem_sazonal[['semana', 'FOCOS', 'CASOS', 'PREC', 'TMIN', 'TMED', 'TMAX']]
	print(f"\n{green}sem_sazonal\n{reset}{sem_sazonal}\n")
	print(f"\n{green}sem_sazonal.columns\n{reset}{sem_sazonal.columns}\n")
	if _SALVAR == True:
		nome_arquivo = f"sem_sazonalidade_{str_var}.csv"
		caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
		os.makedirs(caminho_dados, exist_ok = True)
		sem_sazonal.to_csv(f"{caminho_dados}{nome_arquivo}", index = False)
		#plt.savefig(f"{caminho_dados}{nome_arquivo}", format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	return sem_sazonal

def tendencia(csv): # sem_sazonalidade.csv
	colunas_csv = csv.drop(columns = ["semana"])#, "semana_epi"])
	colunas = colunas_csv.columns
	for c in colunas:
		tendencia = mk.original_test(csv[c])
		if tendencia.trend == "decreasing":
			print(f"\n{red}{c}\n{tendencia.trend}{reset}\n")
		if tendencia.trend == "no trend":
			print(f"\n{cyan}{c}\n{tendencia.trend}{reset}\n")
		elif tendencia.trend == "increasing":
			print(f"\n{green}{c}\n{tendencia.trend}{reset}\n")

def anomalia_estacionaria(csv, str_var): #sem_sazonalidade.csv
	semanas = csv["semana"]
	colunas_csv = csv.drop(columns = ["semana"])
	colunas = colunas_csv.columns
	anomalia_estacionaria = pd.DataFrame()
	anomalia_estacionaria["semana"] = semanas
	for c in colunas:
		print(f"{cyan}\nVARIÁVEL\n\n{str_var.upper()} - {c}{reset}\n")
		print(f"\n{green}sem_sazonal[c]\n{reset}{csv[c]}\n")
		tendencia = mk.original_test(csv[c])
		print(f"\n{green}tendencia\n{reset}{tendencia}\n")
		sem_tendencia = csv[c] -(tendencia.slope + tendencia.intercept)# * len(sem_sazonal[c]))
		anomalia_estacionaria[c] = sem_tendencia
	print(f"{green}\n{str_var.upper()} sem_sazonal\n{reset}{csv}\n")
	print(f"{green}\n{str_var.upper()} anomalia_estacionaria\n{reset}{anomalia_estacionaria}\n")
	if _SALVAR == True:
		nome_arquivo = f"sem_sazonalidade_{str_var}.csv"
		caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
		os.makedirs(caminho_dados, exist_ok = True)
		sem_sazonal.to_csv(f"{caminho_dados}{nome_arquivo}", index = False)
		#plt.savefig(f"{caminho_dados}{nome_arquivo}", format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
		print(f"""\n{green}SALVO COM SUCESSO!\n
	{cyan}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
	return anomalia_estacionaria

focos_sazonal = sazonalidade(focos, "focos")
casos_sazonal = sazonalidade(casos, "casos")
prec_sazonal = sazonalidade(prec, "prec")
tmin_sazonal = sazonalidade(tmin, "tmin")
tmed_sazonal = sazonalidade(tmed, "tmed")
tmax_sazonal = sazonalidade(tmax, "tmax")

focos_sem_sazonal = tratando_sazonalidade(focos, "focos")
tendencia(focos_sem_sazonal)
focos_anomalia_estacionaria = anomalia_estacionaria(focos_sem_sazonal, "focos")

casos_sem_sazonal = tratando_sazonalidade(casos, "casos")
tendencia(casos_sem_sazonal)
casos_anomalia_estacionaria = anomalia_estacionaria(casos_sem_sazonal, "casos")

prec_sem_sazonal = tratando_sazonalidade(prec, "prec")
tendencia(prec_sem_sazonal)
prec_anomalia_estacionaria = anomalia_estacionaria(prec_sem_sazonal, "prec")

tmin_sem_sazonal = tratando_sazonalidade(tmin, "tmin")
tendencia(tmin_sem_sazonal)
tmin_anomalia_estacionaria = anomalia_estacionaria(tmin_sem_sazonal, "tmin")

tmed_sem_sazonal = tratando_sazonalidade(tmed, "tmed")
tendencia(tmed_sem_sazonal)
tmed_anomalia_estacionaria = anomalia_estacionaria(tmed_sem_sazonal, "tmed")

tmax_sem_sazonal = tratando_sazonalidade(tmax, "tmax")
tendencia(tmax_sem_sazonal)
tmax_anomalia_estacionaria = anomalia_estacionaria(tmax_sem_sazonal, "tmax")

sys.exit()


#################################################################################
### Correlacionando (Anomalias Estacionárias)
#################################################################################

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



### Verificando Tendência

#	else:
#		print(f"\n{ansi['magenta']}NÃO EXECUTANDO\n{c}{ansi['reset']}\n")
# Tratando Tendência
# anomalia_estacionaria = dados - ( a + b * x )
#sys.exit()

plt.figure(figsize = (12, 6), layout = "tight", frameon = False)
plt.gca().patch.set_facecolor("honeydew") #.gcf()
sns.barplot(x = sem_sazonal["semana"], y = anomalia_estacionaria["PREC"],
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

