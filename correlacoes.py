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

_AUTOMATIZA = True
_SALVAR = False
_VISUALIZAR = True

_LIMIAR_RETRO = False
_CLIMA = False
_ENTOMOEPIDEMIO = False
_iCLIMA = False
_iEPIDEMIO = False
_LIMIAR_TMIN = False
_LIMIAR_TMAX = False
_LIMIAR_PREC = False
_ANOMALIA_ESTACIONARIA = True

_RETROAGIR = 16 # Semanas Epidemiológicas
_ANO = "2023" # "2023" # "2022" # "2021" # "2020" # "total"
_CIDADE = "Florianópolis" #"Florianópolis"#"Itajaí"#"Joinville"#"Chapecó"
_METODO = "spearman" # "pearson" # "spearman" # "kendall"

_CIDADE = _CIDADE.upper()

##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}
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

prec_sem = "prec_diario_ate_2023.csv"
tmax_sem = "tmax_diario_ate_2023.csv"
tmed_sem = "tmed_diario_ate_2023.csv"
tmin_sem = "tmin_diario_ate_2023.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

prec_sem = pd.read_csv(f"{caminho_dados}{prec_sem}", low_memory = False)
tmax_sem = pd.read_csv(f"{caminho_dados}{tmax_sem}", low_memory = False)
tmed_sem = pd.read_csv(f"{caminho_dados}{tmed_sem}", low_memory = False)
tmin_sem = pd.read_csv(f"{caminho_dados}{tmin_sem}", low_memory = False)

print(prec.iloc["Semana"])
sys.exit()


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
        semana_epii = (dias_inicio + 1) // 7 + 1
    else:
        semana_epi = (data - jan1sab).days // 7 + 1
    return semana_epi

#################################################################################
### Correlacionando (Anomalias Estacionárias)
#################################################################################

# VARIÁVES E RETROAÇÕES DE ANOMALIAS ESTACIONÁRIAS CORRELACIONADAS
if _AUTOMATIZA == True and _ANOMALIA_ESTACIONARIA == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	lista_metodo = ["pearson", "spearman"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _METODO in lista_metodo:
			print(_METODO)
			for r in lista_retro:
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset["TMIN"] = tmin[_CIDADE].copy()
				dataset["TMED"] = tmed[_CIDADE].copy()
				dataset["TMAX"] = tmax[_CIDADE].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(prec[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				#dataset = dataset.merge(tmin[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				#dataset = dataset.merge(tmed[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				#dataset = dataset.merge(tmax[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				print(f"{green}\ndataset\n{reset}{dataset}\n")
				#sys.exit()
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS",  f"{_CIDADE}" : "PREC"}
				dataset.rename(columns = troca_nome, inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n {cyan}DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}{reset}) \n")
				print(f"\n{green}dataset.info()\n{reset}{dataset.info()}\n")
				print("~"*80)
				print(f"\n{green}dataset.dtypes\n{reset}{dataset.dtypes}\n")
				print("~"*80)
				print(f"\n{green}dataset\n{reset}{dataset}\n")
				#sys.exit()
				### Tratando Sazonalidade
				timeindex = dataset.copy()
				print(f"\n{green}timeindex\n{reset}{timeindex}\n{green}timeindex.info()\n{reset}{timeindex.info()}")
				timeindex.reset_index(inplace = True)
				print(f"\n{green}timeindex\n{reset}{timeindex}\n")#{green}timeindex.info()\n{reset}{timeindex.info()}")
				timeindex["semana"] = pd.to_datetime(timeindex["Semana"]).dt.date
				timeindex = timeindex.astype({"semana": "datetime64[ns]", "FOCOS" : "int64", "CASOS" : "int64"})
				timeindex.drop(columns = "Semana", inplace = True)
				timeindex["semana_epi"] = timeindex['semana'].apply(semana_epidemio)
				print(f"\n{green}timeindex\n{reset}{timeindex}\n{green}timeindex.info()\n{reset}{timeindex.info()}")
				print(f"\n{green}timeindex\n{reset}{timeindex}\n{green}timeindex.info()\n{reset}{timeindex.info()}\n{green}timeindex.dtypes\n{reset}{timeindex.dtypes}\n")
				print("="*80)
				media_semana = timeindex.groupby("semana_epi")[["FOCOS", "CASOS", "PREC", "TMIN", "TMED", "TMAX"]].mean().round(2)
				media_semana.reset_index(inplace = True)
				print(f"\n{green}media_semana\n{reset}{media_semana}\n{green}media_semana.index\n{reset}{media_semana.index}")
				#media_semana[[ "PREC", "CASOS", "FOCOS", "TMIN", "TMED", "TMAX"]].plot()
				#media_semana[[ "PREC", "FOCOS", "TMIN", "TMED", "TMAX"]].plot()
				#plt.show()
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
				plt.show()
				#sys.exit()
				_cidade = _CIDADE
				nome_arquivo = f"distribuicao_sazonalidade_semanal_{_cidade}.pdf"
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
				componente_sazonal = timeindex.merge(media_semana, left_on = "semana_epi", how = "left", suffixes = ("", "_media"), right_index = True)
				sem_sazonal = pd.DataFrame(index = timeindex.index)
				semanas  = componente_sazonal["semana"]
				componente_sazonal.drop(columns = "semana", inplace = True)
				print(componente_sazonal)
				for coluna in timeindex.columns:
					if coluna in componente_sazonal.columns:
						media_coluna = f"{coluna}_media"
						if media_coluna in componente_sazonal.columns:
							sem_sazonal[coluna] = timeindex[coluna] - componente_sazonal[media_coluna]
						else:
							print(f"{red}Coluna {media_coluna} não encontrada no componente sazonal!{reset}")
					else:
						print(f"{red}Coluna {coluna} não encontrada no timeindex!{reset}")
				sem_sazonal.drop(columns = "semana_epi", inplace = True)
				sem_sazonal["semana"] = semanas
				sem_sazonal.dropna(inplace = True)
				sem_sazonal = sem_sazonal[['semana', 'FOCOS', 'CASOS', 'PREC', 'TMIN', 'TMED', 'TMAX']]
				print(f"\n{green}sem_sazonal\n{reset}{sem_sazonal}\n")
				print(f"\n{green}sem_sazonal.columns\n{reset}{sem_sazonal.columns}\n")
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
				sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMIN"],
								color = "darkblue", linewidth = 1, label = "Temperatura Mínima")
				sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMED"],
								color = "orange", linewidth = 1, label = "Temperatura Média")
				sns.lineplot(x = sem_sazonal.index, y = sem_sazonal["TMAX"],
								color = "red", linewidth = 1, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
				plt.title(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSEM SAZONALIDADE, SÉRIE HISTÓRICA PARA O MUNICÍPIO DE {_CIDADE}, SANTA CATARINA.")
				ax2.set_ylabel("Temperaturas (C)")
				ax2.legend(loc = "upper right")
				ax2.grid(False)
				#plt.show()
				#sys.exit()
				_cidade = _CIDADE
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
				colunas = ['FOCOS', 'CASOS', 'PREC', 'TMIN', 'TMED', 'TMAX']
				for c in colunas:
					tendencia = mk.original_test(sem_sazonal[c])
					if tendencia.trend == "decreasing":
						print(f"\n{ansi['red']}{c}\n{tendencia.trend}{ansi['reset']}\n")
					if tendencia.trend == "no trend":
						print(f"\n{ansi['cyan']}{c}\n{tendencia.trend}{ansi['reset']}\n")
					elif tendencia.trend == "increasing":
						print(f"\n{ansi['green']}{c}\n{tendencia.trend}{ansi['reset']}\n")
				#	else:
				#		print(f"\n{ansi['magenta']}NÃO EXECUTANDO\n{c}{ansi['reset']}\n")
				# Tratando Tendência
				# anomalia_estacionaria = dados - ( a + b * x )
				#sys.exit()
				anomalia_estacionaria = pd.DataFrame()
				for c in colunas:
					print(f"{cyan}\nVARIÁVEL\n\n{c}{reset}\n")
					print(f"\n{green}sem_sazonal[c]\n{reset}{sem_sazonal[c]}\n")
					tendencia = mk.original_test(sem_sazonal[c])
					print(f"\n{green}tendencia\n{reset}{tendencia}\n")
					sem_tendencia = sem_sazonal[c] -(tendencia.slope + tendencia.intercept)# * len(sem_sazonal[c]))
					anomalia_estacionaria[c] = sem_tendencia
				print(f"{ansi['green']}\nsem_sazonal\n{ansi['reset']}", sem_sazonal)
				print(f"{ansi['green']}\nanomalia_estacionaria\n{ansi['reset']}", anomalia_estacionaria)
				#sys.exit()
				sys.exit()








				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				print(f"\n{green}dataset\n{reset}{dataset}\n{green}dataset.info()\n{reset}{dataset.info()}")
				print(dataset.info())
				sys.exit()
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
					print("\n\n2023\n\n")
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
					print("\n\n2022\n\n")
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
					print("\n\n2021\n\n")
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
					print("\n\n2020\n\n")
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.drop(columns = "Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral",
                            vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					if r == 0:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; sem retroagir)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					elif r == 1:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {r} semana epidemiológica)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					else:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {r} semanas epidemiológicas)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
				else:
					if r == 0:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; sem retroagir)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					elif r == 1:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {r} semana epidemiológica)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					else:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {r} semanas epidemiológicas)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				if _SALVAR == True:
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/retrolimiar/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf{ansi['reset']}\n")
					plt.show()


#################################################################################
### Correlacionando (Focos, Casos E Limiares, Retroações)
#################################################################################

# VARIÁVES, LIMIARES E RETROAÇÕES CORRELACIONADOS
if _AUTOMATIZA == True and _LIMIAR_RETRO == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	limiares_tmax = [22, 24, 26, 28, 30, 32]
	limiares_tmin = [14, 16, 18, 20, 22, 24]
	limiares_prec = [5, 20, 35, 50, 65, 80, 95]
	lista_retro = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for r in lista_retro:
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS"}#,  f"{_CIDADE}" : f"L{_LIMIAR}_PREC"}
				dataset.rename(columns = troca_nome, inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				print(dataset)
				### Incluindo limiares
				for _LIMIAR in limiares_tmin:
					print(_LIMIAR)
					limite = tmin_sem.copy()
					limite.set_index("Data", inplace = True)
					limite.drop(columns = "tmin", inplace = True)
					print(f"{ansi['red']}\nLIMIAR TMIN > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
					limite.reset_index(inplace = True)
					print(f"{ansi['yellow']}\nLIMIAR TMIN > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite["Data"] = pd.to_datetime(limite["Data"])
					limite = limite.sort_values(by = ["Data"])
					limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
					limite = limite.groupby(["Semana"]).sum(numeric_only = True)
					limite.reset_index(inplace = True)
					limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
					dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
					dataset.rename(columns = {f"{_CIDADE}" : f"L{_LIMIAR}_TMIN"}, inplace = True)
					dataset[f"L{_LIMIAR}_TMIN_r{r}"] = dataset[f"L{_LIMIAR}_TMIN"].shift(-r)
					dataset.drop(columns = f"L{_LIMIAR}_TMIN", inplace = True)
					print(f"{ansi['green']}\nLIMIAR TMIN > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
				for _LIMIAR in limiares_tmax:
					print(_LIMIAR)
					limite = tmax_sem.copy()
					limite.set_index("Data", inplace = True)
					limite.drop(columns = "tmax", inplace = True)
					print(f"{ansi['red']}\nLIMIAR TMAX > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
					limite.reset_index(inplace = True)
					print(f"{ansi['yellow']}\nLIMIAR TMAX > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite["Data"] = pd.to_datetime(limite["Data"])
					limite = limite.sort_values(by = ["Data"])
					limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
					limite = limite.groupby(["Semana"]).sum(numeric_only = True)
					limite.reset_index(inplace = True)
					limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
					dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
					dataset.rename(columns = {f"{_CIDADE}" : f"L{_LIMIAR}_TMAX"}, inplace = True)
					dataset[f"L{_LIMIAR}_TMAX_r{r}"] = dataset[f"L{_LIMIAR}_TMAX"].shift(-r)
					dataset.drop(columns = f"L{_LIMIAR}_TMAX", inplace = True)
					print(f"{ansi['green']}\nLIMIAR TMAX > {_LIMIAR} C\n{limite}\n{ansi['reset']}")
					print(limite.info())
				for _LIMIAR in limiares_prec:
					print(_LIMIAR)
					limite = prec_sem.copy()
					limite.set_index("Data", inplace = True)
					limite.drop(columns = "prec", inplace = True)
					limite.dropna(inplace = True)
					print(f"{ansi['red']}\nLIMIAR PREC > {_LIMIAR} mm\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite.dropna(inplace = True)
					limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
					limite.reset_index(inplace = True)
					print(f"{ansi['yellow']}\nLIMIAR PREC > {_LIMIAR} mm\n{limite}\n{ansi['reset']}")
					print(limite.info())
					limite["Data"] = pd.to_datetime(limite["Data"])
					limite = limite.sort_values(by = ["Data"])
					limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
					limite = limite.groupby(["Semana"]).sum(numeric_only = True)
					limite.reset_index(inplace = True)
					limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
					limite.drop([0], axis = 0, inplace = True)
					dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
					dataset.rename(columns = {f"{_CIDADE}" : f"L{_LIMIAR}_PREC"}, inplace = True)
					dataset[f"L{_LIMIAR}_PREC_r{r}"] = dataset[f"L{_LIMIAR}_PREC"].shift(-r)
					dataset.drop(columns = f"L{_LIMIAR}_PREC", inplace = True)
					print(f"{ansi['green']}\nLIMIAR PREC > {_LIMIAR} mm\n{limite}\n{ansi['reset']}")
					print(limite.info())
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				print(dataset)
				print(dataset.info())
				#sys.exit()
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
					print("\n\n2023\n\n")
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
					print("\n\n2022\n\n")
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
					print("\n\n2021\n\n")
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
					print("\n\n2020\n\n")
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.drop(columns = "Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral",
                            vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					if r == 0:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; sem retroagir)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					elif r == 1:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {r} semana epidemiológica)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					else:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {r} semanas epidemiológicas)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
				else:
					if r == 0:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; sem retroagir)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					elif r == 1:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {r} semana epidemiológica)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					else:
						fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e LIMIARES CLIMATOLÓGICOS** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {r} semanas epidemiológicas)\n**(Temperatura Mínima (C), Temperatura Máxima (C) e Precipitação(mm))", weight = "bold", size = "medium")
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				if _SALVAR == True:
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/retrolimiar/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_retrolimiar_{_cidade}_{_ANO}_r{r}s.pdf{ansi['reset']}\n")
					plt.show()

#################################################################################
### Correlacionando (VARIÁVEIS CLIMATOLÓGICAS)
#################################################################################
if _AUTOMATIZA == True and _CLIMA == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			#Automatizando essas listas acima...
			### Montando dataset
			dataset = tmin[["Semana"]].copy()
			dataset["TMIN"] = tmin[_CIDADE].copy()
			dataset["TMED"] = tmed[_CIDADE].copy()
			dataset["TMAX"] = tmax[_CIDADE].copy()
			dataset = dataset.merge(prec[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			dataset.dropna(axis = 0, inplace = True)
			dataset = dataset.iloc[:, :].copy()
			dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			troca_nome = {f"{_CIDADE}_x" : "PREC", f"{_CIDADE}_y" : "FOCOS", f"{_CIDADE}" : "CASOS"}
			dataset = dataset.rename(columns = troca_nome)
			dataset.fillna(0, inplace = True)
			if _ANO == "2023":
				dataset = dataset.iloc[-53:, :].copy()
			elif _ANO == "2022":
				dataset = dataset.iloc[-105:-53, :].copy()
			elif _ANO == "2021":
				dataset = dataset.iloc[-157:-105, :].copy()
			elif _ANO == "2020":
				dataset = dataset.iloc[-209:-157, :].copy()
			else:
				print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
			dataset.dropna(inplace = True)
			dataset.set_index("Semana", inplace = True)
			dataset.columns.name = f"{_CIDADE}"
			ordem_colunas = ["FOCOS", "CASOS", "TMIN", "TMED", "TMAX", "PREC"]
			dataset = dataset.reindex(columns = ordem_colunas)
			print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
			print(dataset.info())
			print("~"*80)
			print(dataset.dtypes)
			print("~"*80)
			print(dataset)
			#sys.exit()
			### Retroagindo dataset
			for r in range(1, _RETROAGIR + 1):
				#dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
				dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
				#dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
				dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
				#dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
				#dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
			dataset.dropna(inplace = True)
			dataset.columns.name = f"{_CIDADE}"
			### Matriz de Correlações
			correlacao_dataset = dataset.corr(method = f"{_METODO}")
			print("="*80)
			print(f"Método de {_METODO.title()} \n", correlacao_dataset)
			print("="*80)
			
			# Gerando Visualização (.pdf) da Matriz
			fig, ax = plt.subplots(figsize = (16, 8), layout = "constrained", frameon = False)
			filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
			sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
			ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
			ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
			if _ANO == "total":
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM {_CIDADE} \n *(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			else:
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			if _SALVAR == True:
				_cidade = _CIDADE
				troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
						'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
						'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
						'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
						'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
						'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				for velho, novo in troca.items():
					_cidade = _cidade.replace(velho, novo)
				caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/clima/"
				os.makedirs(caminho_correlacao, exist_ok = True)
				plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
				print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n""")
			if _VISUALIZAR == True:
				print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n")
				plt.show()

#################################################################################
### Correlacionando (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS)
#################################################################################
if _AUTOMATIZA == True and _ENTOMOEPIDEMIO == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			#Automatizando essas listas acima...
			### Montando dataset
			dataset = tmin[["Semana"]].copy()
			dataset["TMIN"] = tmin[_CIDADE].copy()
			dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			dataset.dropna(axis = 0, inplace = True)
			dataset = dataset.iloc[:, :].copy()
			troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS"}
			dataset = dataset.rename(columns = troca_nome)
			dataset.fillna(0, inplace = True)
			if _ANO == "2023":
				dataset = dataset.iloc[-53:, :].copy()
			elif _ANO == "2022":
				dataset = dataset.iloc[-105:-53, :].copy()
			elif _ANO == "2021":
				dataset = dataset.iloc[-157:-105, :].copy()
			elif _ANO == "2020":
				dataset = dataset.iloc[-209:-157, :].copy()
			else:
				print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
			dataset.dropna(inplace = True)
			dataset.set_index("Semana", inplace = True)
			dataset.columns.name = f"{_CIDADE}"
			dataset.drop(columns = "TMIN", inplace = True)
			print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
			print(dataset.info())
			print("~"*80)
			print(dataset.dtypes)
			print("~"*80)
			### Retroagindo dataset
			#_RETROAGIR = 20
			for r in range(1, _RETROAGIR + 1):
				dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
				dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
			dataset.dropna(inplace = True)
			dataset.columns.name = f"{_CIDADE}"
			### Matriz de Correlações
			correlacao_dataset = dataset.corr(method = f"{_METODO}")
			print("="*80)
			print(f"Método de {_METODO.title()} \n", correlacao_dataset)
			print("="*80)
			#print(dataset)
			#sys.exit()			
			# Gerando Visualização (.pdf) da Matriz
			fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
			filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
			sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
			ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
			ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
			if _ANO == "total":
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e CASOS (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			else:
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e CASOS (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			if _SALVAR == True:
				_cidade = _CIDADE
				troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
						'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
						'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
						'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
						'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
						'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				for velho, novo in troca.items():
					_cidade = _cidade.replace(velho, novo)
				caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/entomoepidemio/"
				os.makedirs(caminho_correlacao, exist_ok = True)
				plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
				print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n""")
			if _VISUALIZAR == True:
				print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n")
				plt.show()

#################################################################################
### Correlacionando (Índice Clima e Focos)
#################################################################################
if _AUTOMATIZA == True and _iCLIMA == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	lista_constante = [1, 2, 3, 4, 5, 6, 7, 8]
	_K = 1
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for _K in lista_constante:
				print(_K)
				#Automatizando essas listas acima...
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset["iCLIMA"] =  np.cbrt((tmin[_CIDADE].rolling(_K).mean() ** _K) * (prec[_CIDADE].rolling(_K).mean() / _K))
				dataset = dataset.merge(prec[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "PREC"}
				dataset = dataset.rename(columns = troca_nome)
				dataset.fillna(0, inplace = True)
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				dataset.drop(columns = "PREC", inplace = True)
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				#sys.exit()
				### Retroagindo dataset
				#_RETROAGIR = 20
				for r in range(1, _RETROAGIR + 1):
					dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
					dataset[f"iCLIMA_r{r}"] = dataset["iCLIMA"].shift(-r)
				dataset.dropna(inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e Índice Climatológico** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas; k = {_K})\n**np.cbrt((tmin.rolling(k).mean() ** k) * (prec.rolling(k).mean() / k))", weight = "bold", size = "medium")
				else:
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e Índice Climatológico** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas; k = {_K})\n**np.cbrt((tmin.rolling(k).mean() ** k) * (prec.rolling(k).mean() / k))", weight = "bold", size = "medium")
				if _SALVAR == True:
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/indiceclimato/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_iclima_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_iclima_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_iclima_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf{ansi['reset']}\n")
					plt.show()

#################################################################################
### Correlacionando (Índice Epidemio e Casos)
#################################################################################
if _AUTOMATIZA == True and _iEPIDEMIO == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	lista_constante = [1, 2, 3, 4, 5, 6, 7, 8]
	_K = 1
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for _K in lista_constante:
				print(_K)
				#Automatizando essas listas acima...
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				troca_nome = {f"{_CIDADE}_x" : "CASOS", f"{_CIDADE}_y" : "FOCOS"}
				dataset = dataset.rename(columns = troca_nome)
				dataset["iEPIDEMIO"] =  np.sqrt((dataset["FOCOS"].rolling(_K).mean() / _K) * dataset["CASOS"].rolling(_K).mean())
				"""
				print(dataset)
				print(dataset.info())
				sys.exit()
				#dataset["iCLIMA"] =  (tmin[_CIDADE].rolling(_K).mean() ** _K) * (prec[_CIDADE].rolling(_K).mean() / _K)
				"""
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				dataset.fillna(0, inplace = True)
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				#sys.exit()
				### Retroagindo dataset
				#_RETROAGIR = 20
				for r in range(1, _RETROAGIR + 1):
					dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
					dataset[f"iEPIDEMIO_r{r}"] = dataset["iEPIDEMIO"].shift(-r)
				dataset.dropna(inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre CASOS e Índice Epidemiológico** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas; k = {_K})\n**(a definir)", weight = "bold", size = "medium")
				else:
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre CASOS e Índice Epidemiológico** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas; k = {_K})\n**(a definir)", weight = "bold", size = "medium")
				if _SALVAR == True:
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/indiceepidemio/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_iepidemio_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_iepidemio_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_iepidemio_{_cidade}_r{_RETROAGIR}s_{_ANO}_k{_K}.pdf{ansi['reset']}\n")
					plt.show()

#################################################################################
### Correlacionando (Focos, Casos E Limiares TMIN)
#################################################################################
if _AUTOMATIZA == True and _LIMIAR_TMIN == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	limiares = [14, 16, 18, 20, 22, 24]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for _LIMIAR in limiares:
				print(_LIMIAR)
				limite = tmin_sem.copy()
				limite.set_index("Data", inplace = True)
				limite.drop(columns = "tmin", inplace = True)
				limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
				limite.reset_index(inplace = True)
				limite["Data"] = pd.to_datetime(limite["Data"])
				limite = limite.sort_values(by = ["Data"])
				limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
				limite = limite.groupby(["Semana"]).sum(numeric_only = True)
				limite.reset_index(inplace = True)
				limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
				limite.drop([0], axis = 0, inplace = True)
				print(limite.info())
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				print(dataset.info())
				dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS",  f"{_CIDADE}" : f"L{_LIMIAR}_TMIN"}
				dataset = dataset.rename(columns = troca_nome)
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				dataset.fillna(0, inplace = True)
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				print(dataset)
				#sys.exit()
				### Retroagindo dataset
				#_RETROAGIR = 20
				for r in range(1, _RETROAGIR + 1):
					dataset[f"L{_LIMIAR}_TMIN_r{r}"] = dataset[f"L{_LIMIAR}_TMIN"].shift(-r)
				dataset.dropna(inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Temperatura Mínima** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Temperatura Mínima > {_LIMIAR} C)\n", weight = "bold", size = "medium")
				else:
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Temperatura Mínima** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Temperatura Mínima > {_LIMIAR} C)", weight = "bold", size = "medium")
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				if _SALVAR == True:
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/limiares_tmin/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_tmin_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_tmin_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_tmin_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n")
					plt.show()

#################################################################################
### Correlacionando (Focos, Casos E Limiares TMAX)
#################################################################################
if _AUTOMATIZA == True and _LIMIAR_TMAX == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	limiares = [22, 24, 26, 28, 30, 32]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for _LIMIAR in limiares:
				print(_LIMIAR)
				limite = tmax_sem.copy()
				limite.set_index("Data", inplace = True)
				limite.drop(columns = "tmax", inplace = True)
				limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
				limite.reset_index(inplace = True)
				limite["Data"] = pd.to_datetime(limite["Data"])
				limite = limite.sort_values(by = ["Data"])
				limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
				limite = limite.groupby(["Semana"]).sum(numeric_only = True)
				limite.reset_index(inplace = True)
				limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
				limite.drop([0], axis = 0, inplace = True)
				print(limite.info())
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS",  f"{_CIDADE}" : f"L{_LIMIAR}_TMAX"}
				dataset = dataset.rename(columns = troca_nome)
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				dataset.fillna(0, inplace = True)
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				print(dataset)
				#sys.exit()
				### Retroagindo dataset
				#_RETROAGIR = 20
				for r in range(1, _RETROAGIR + 1):
					dataset[f"L{_LIMIAR}_TMAX_r{r}"] = dataset[f"L{_LIMIAR}_TMAX"].shift(-r)
				dataset.dropna(inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Temperatura Máxima** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Temperatura Máxima < {_LIMIAR} C)\n", weight = "bold", size = "medium")
				else:
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Temperatura Máxima** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Temperatura Máxima < {_LIMIAR} C)", weight = "bold", size = "medium")
				_cidade = _CIDADE
				troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
						'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
						'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
						'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
						'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
						'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				for velho, novo in troca.items():
					_cidade = _cidade.replace(velho, novo)
				if _SALVAR == True:
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/limiares_tmax/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_tmax_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_tmax_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_tmax_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n")
					plt.show()

#################################################################################
### Correlacionando (Focos, Casos E Limiares PREC)
#################################################################################
if _AUTOMATIZA == True and _LIMIAR_PREC == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	limiares = [5, 10, 15, 20, 25, 30, 35]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		print(_CIDADE)
		for _ANO in lista_anos:
			print(_ANO)
			for _LIMIAR in limiares:
				print(_LIMIAR)
				limite = prec_sem.copy()
				limite.set_index("Data", inplace = True)
				limite.drop(columns = "prec", inplace = True)
				limite = limite.applymap(lambda x: 1 if x > _LIMIAR else 0)
				limite.reset_index(inplace = True)
				limite["Data"] = pd.to_datetime(limite["Data"])
				limite = limite.sort_values(by = ["Data"])
				limite["Semana"] = limite["Data"].dt.to_period("W-SAT").dt.to_timestamp()
				limite = limite.groupby(["Semana"]).sum(numeric_only = True)
				limite.reset_index(inplace = True)
				limite["Semana"] = limite["Semana"].dt.strftime("%Y-%m-%d")
				limite.drop([0], axis = 0, inplace = True)
				print(limite.info())
				### Montando dataset
				dataset = tmin[["Semana"]].copy()
				dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset = dataset.merge(limite[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
				dataset.dropna(axis = 0, inplace = True)
				troca_nome = {f"{_CIDADE}_x" : "FOCOS", f"{_CIDADE}_y" : "CASOS",  f"{_CIDADE}" : f"L{_LIMIAR}_PREC"}
				dataset = dataset.rename(columns = troca_nome)
				dataset.dropna(axis = 0, inplace = True)
				dataset = dataset.iloc[:, :].copy()
				dataset.fillna(0, inplace = True)
				if _ANO == "2023":
					dataset = dataset.iloc[-53:, :].copy()
				elif _ANO == "2022":
					dataset = dataset.iloc[-105:-53, :].copy()
				elif _ANO == "2021":
					dataset = dataset.iloc[-157:-105, :].copy()
				elif _ANO == "2020":
					dataset = dataset.iloc[-209:-157, :].copy()
				else:
					print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n\nA correlação será realizada pela SÉRIE HISTÓRICA {ansi['magenta']} intencionalmente!{ansi['reset']}")
				dataset.dropna(inplace = True)
				dataset.set_index("Semana", inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				print(f"\n \n DATASET PARA INICIAR MATRIZ DE CORRELAÇÃO ({_METODO.title()}) \n")
				print(dataset.info())
				print("~"*80)
				print(dataset.dtypes)
				print("~"*80)
				print(dataset)
				#sys.exit()
				### Retroagindo dataset
				#_RETROAGIR = 20
				for r in range(1, _RETROAGIR + 1):
					dataset[f"L{_LIMIAR}_PREC_r{r}"] = dataset[f"L{_LIMIAR}_PREC"].shift(-r)
				dataset.dropna(inplace = True)
				dataset.columns.name = f"{_CIDADE}"
				### Matriz de Correlações
				correlacao_dataset = dataset.corr(method = f"{_METODO}")
				print("="*80)
				print(f"Método de {_METODO.title()} \n", correlacao_dataset)
				print("="*80)
				#print(dataset)
				#sys.exit()			
				# Gerando Visualização (.pdf) da Matriz
				fig, ax = plt.subplots(figsize = (18, 8), layout = "constrained", frameon = False)
				filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
				sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
				ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
				ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
				if _ANO == "total":
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Precipitação** EM {_CIDADE}\n*(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Precipitação > {_LIMIAR} mm)\n", weight = "bold", size = "medium")
				else:
					fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS e Limiar de Precipitação** EM {_CIDADE}\n*(Método de {_METODO.title()}; em {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas) **(Limiar de Precipitação > {_LIMIAR} mm)", weight = "bold", size = "medium")
					_cidade = _CIDADE
					troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
							'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
							'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
							'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
							'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
							'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
				if _SALVAR == True:
					for velho, novo in troca.items():
						_cidade = _cidade.replace(velho, novo)
					caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/limiares_prec/"
					os.makedirs(caminho_correlacao, exist_ok = True)
					plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_prec_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
					print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
	{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
	NOME DO ARQUIVO: matriz_correlacao_{_METODO}_prec_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n""")
				if _VISUALIZAR == True:
					print(f"{ansi['cyan']} Visualizando: matriz_correlacao_{_METODO}_prec_{_cidade}_r{_RETROAGIR}s_{_ANO}_LIMIAR{_LIMIAR}.pdf{ansi['reset']}\n")
					plt.show()
