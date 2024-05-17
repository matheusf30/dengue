### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm
### Suporte
import sys

### Condições para Variar #######################################################
_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"

_AUTOMATIZA = True
_CLIMA = False
_iCLIMA = True
_ENTOMOEPIDEMIO = False


_RETROAGIR = 16 # Semanas Epidemiológicas
_ANO = "2023" # "2023" # "2022" # "2021" # "2020" # "total"
_CIDADE = "Florianópolis" #"Florianópolis"#"Itajaí"#"Joinville"#"Chapecó"
_METODO = "pearson" # "pearson" # "spearman" # "kendall"

_CIDADE = _CIDADE.upper()
##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}
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

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

#################################################################################
### Correlacionando (VARIÁVEIS CLIMATOLÓGICAS)
#################################################################################
if _AUTOMATIZA == True and _CLIMA == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		for _ANO in lista_anos:
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
			plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
			print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n""")
			#plt.show()
#################################################################################
### Correlacionando (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS)
#################################################################################
if _AUTOMATIZA == True and _ENTOMOEPIDEMIO == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		for _ANO in lista_anos:
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
			fig, ax = plt.subplots(figsize = (18, 6), layout = "constrained", frameon = False)
			filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
			sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
			ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
			ax.set_xticklabels(ax.get_xticklabels(), rotation = 75)
			if _ANO == "total":
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e CASOS (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			else:
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e CASOS (VARIÁVEIS ENTOMO-EPIDEMIOLÓGICAS) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
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
			plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
			print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n""")
			#plt.show()
#################################################################################
### Correlacionando (Índice Clima e Focos)
#################################################################################
if _AUTOMATIZA == True and _iCLIMA == True:
	lista_cidades = ["Florianópolis", "Itajaí", "Joinville", "Chapecó"]
	lista_anos = ["2023", "2022", "2021", "2020", "total"]
	for _CIDADE in lista_cidades:
		_CIDADE = _CIDADE.upper()
		for _ANO in lista_anos:
			#Automatizando essas listas acima...
			### Montando dataset
			dataset = tmin[["Semana"]].copy()
			dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
			dataset["iCLIMA"] =  tmin[_CIDADE]*2 if prec[_CIDADE].all() >= 1 else tmin[_CIDADE]
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
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e Índice Climátológico (prec/(tmin*2)) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
			else:
				fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS e Índice Climátológico (prec/(tmin*2)) EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
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
			#plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
			print(f"""\n{ansi['green']}SALVO COM SUCESSO!\n
{ansi['cyan']}ENCAMINHAMENTO: {caminho_correlacao}\n
NOME DO ARQUIVO: matriz_correlacao_{_METODO}_fococaso_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf{ansi['reset']}\n""")
			plt.show()
"""
######################### Correlacionando (VARIÁVEIS CLIMATOLÓGICAS)
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
	#sys.exit()
dataset.dropna(inplace = True)
dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{_CIDADE}"
ordem_colunas = ["FOCOS", "CASOS", "TMIN", "TMED", "TMAX", "PREC"]
dataset = dataset.reindex(columns = ordem_colunas)
print(f"\n \n MATRIZ DE CORRELAÇÃO ({_METODO.title()}; Base e Clima; sem retroagir [TESTE]) \n")
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

fig, ax = plt.subplots(figsize = (16, 8), layout = "constrained", frameon = False)
filtro = np.triu(np.ones_like(correlacao_dataset, dtype = bool), k = 1)
sns.heatmap(correlacao_dataset, annot = True, cmap = "Spectral", vmin = -1, vmax = 1, linewidth = 0.5, mask = filtro)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
if _ANO == "total":
	fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM {_CIDADE} \n *(Método de {_METODO.title()}; durante a série histórica; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
else:
	fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas epidemiológicas)", weight = "bold", size = "medium")
_cidade = _CIDADE
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
for velho, novo in troca.items():
	_cidade = _cidade.replace(velho, novo)
plt.savefig(f'{caminho_correlacao}matriz_correlacao_{_METODO}_{_cidade}_r{_RETROAGIR}s_{_ANO}.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
plt.show()
"""
