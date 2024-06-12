### Bibliotecas Correlatas
# Básicas e Gráficas
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import seaborn as sns 
#import datetime
# Suporte
import os
import sys
import joblib
import webbrowser
# Pré-Processamento e Validações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score, r2_score
from sklearn.inspection import permutation_importance
from sklearn.tree import plot_tree, export_text
# Modelos
from sklearn.ensemble import RandomForestRegressor
#from dtreeviz.trees import dtreeviz
#from sklearn.tree import export_graphviz
#import graphviz
#import tensorflow
#from tensorflow import keras
#from keras.models import load_model

### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
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
    caminho_erro = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/erro/"
    caminho_validacao = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/validacao/"
    caminho_importancia = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/importancia/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos # TENTAR GFS
casos = "casos_dive_pivot_total.csv"
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
"""
#### Erros Gerados 2022-2023 ######################################################################
unicos_c = pd.read_csv(f"{caminho_dados}{unicos_c}")
cidades_c = unicos_c["Município"].copy()
value_error = ["BOMBINHAS", "BALNEÁRIO CAMBORIÚ", "PORTO BELO"]
key_error = ["ABELARDO LUZ", "URUBICI", "RANCHO QUEIMADO"]
not_found_c = list(cidades_c.iloc[151:])  # Desconsiderando 2023, pois ainda não há modelagem
"""
#### Condições para Variar entre Modelos ############
cidade = "Itajaí"
cidade = cidade.upper()
SEED = np.random.seed(0)
####################################################
##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}


####################################### Definindo Classes e Funções #######################################
class Modelo:

	def __init__(self):
		"""
		Função de Instanciação do Objeto Classe
		"""
		print("\n" + "="*80 + "\n")
		print(f"\n{ansi['cyan']}>>>OBJETO MODELO INSTANCIADO<<<{ansi['reset']}")
		print("\n" + "="*80 + "\n")

	def variar(self, retroagir, horizonte):
		"""
		Função para variar antes da abertura do modelo
		"""
		_retroagir = retroagir
		_horizonte = horizonte
		return _retroagir, _horizonte

	def abre_modelo(self, str_var, cidade, _retroagir):
		"""
		Função para abrir modelo hdf5 do município.
		"""
		troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
		for velho, novo in troca.items():
			cidade = cidade.replace(velho, novo)
		modelo = joblib.load(f"{caminho_modelos}RF_{str_var}_r{_retroagir}_{cidade}.h5")
		print(f"\n{ansi['green']}MODELO RANDOM FOREST DE {cidade} ABERTO!")
		print(f"\nCaminho e Nome:\n {caminho_modelos}RF_{str_var}_r{_retroagir}_{cidade}.h5{ansi['reset']}")
		print("\n" + "="*80 + "\n")
		return modelo

	def monta_dataset_casos(self, cidade):
		"""
		Função para montar estrutura de dados para previsão.
		"""
		dataset = tmin[["Semana"]].copy()
		dataset["TMIN"] = tmin[cidade].copy()
		dataset["TMED"] = tmed[cidade].copy()
		dataset["TMAX"] = tmax[cidade].copy()
		dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset.dropna(axis = 0, inplace = True)
		dataset = dataset.iloc[104:, :].copy()
		dataset = dataset.merge(casos[["Semana", cidade]], how = "left", on = "Semana").copy()
		troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS", f"{cidade}" : "CASOS"}
		dataset = dataset.rename(columns = troca_nome)
		dataset.fillna(0, inplace = True)
		for r in range(_horizonte + 1, _retroagir + 1):
			dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
			dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
			dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
			dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
			dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
			dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
		dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC", "FOCOS"], inplace = True)
		dataset.dropna(inplace = True)
		dataset.set_index("Semana", inplace = True)
		dataset.columns.name = f"{cidade}"
		x = dataset.drop(columns = "CASOS")
		y = dataset["CASOS"]
		if x.empty or x.isnull().all().all():
			print(f"'X' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		x = x.dropna()
		if x.empty:
			print(f"'X' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		if y.empty or y.isnull().all().all():
			print(f"'Y' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		y = y.dropna()
		if y.empty:
			print(f"'Y' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		x_array = x.to_numpy()
		x_array = x_array.reshape(x_array.shape[0], -1)
		x_array = x.to_numpy().astype(int)
		y_array = y.to_numpy().astype(int)
		x_array = x_array.reshape(x_array.shape[0], -1)
		print(dataset)
		return dataset, x, y, x_array, y_array

	def monta_dataset_focos(self, cidade):
		"""
		Função para montar estrutura de dados para previsão.
		"""
		dataset = tmin[["Semana"]].copy()
		dataset["TMIN"] = tmin[cidade].copy()
		dataset["TMED"] = tmed[cidade].copy()
		dataset["TMAX"] = tmax[cidade].copy()
		dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset.dropna(axis = 0, inplace = True)
		troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS"}
		dataset = dataset.rename(columns = troca_nome)
		dataset.fillna(0, inplace = True)
		for r in range(_horizonte + 1, _retroagir + 1):
			dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
			dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
			dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
			dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
			dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
		dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC"], inplace = True)
		dataset.dropna(inplace = True)
		dataset.set_index("Semana", inplace = True)
		dataset.columns.name = f"{cidade}"
		x = dataset.drop(columns = "FOCOS")
		y = dataset["FOCOS"]
		if x.empty or x.isnull().all().all():
			print(f"'X' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		x = x.dropna()
		if x.empty:
			print(f"'X' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		if y.empty or y.isnull().all().all():
			print(f"'Y' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		y = y.dropna()
		if y.empty:
			print(f"'Y' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		x_array = x.to_numpy()
		x_array = x_array.reshape(x_array.shape[0], -1)
		x_array = x.to_numpy().astype(int)
		y_array = y.to_numpy().astype(int)
		x_array = x_array.reshape(x_array.shape[0], -1)
		print(dataset)
		return dataset, x, y, x_array, y_array

	def testa_dataset_casos(self, cidade):
		"""
		Função para montar estrutura de dados para previsão.
		"""
		dataset = tmin[["Semana"]].copy()
		dataset["TMIN"] = tmin[cidade].copy()
		dataset["TMED"] = tmed[cidade].copy()
		dataset["TMAX"] = tmax[cidade].copy()
		dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset.dropna(axis = 0, inplace = True)
		dataset = dataset.iloc[104:, :].copy()
		dataset = dataset.merge(casos[["Semana", cidade]], how = "left", on = "Semana").copy()
		troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS", f"{cidade}" : "CASOS"}
		dataset = dataset.rename(columns = troca_nome)
		dataset.fillna(0, inplace = True)
		for r in range(_horizonte + 1, _retroagir + 1):
			dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
			dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
			dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
			dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
			dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
			dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
		dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC", "FOCOS"], inplace = True)
		dataset.dropna(inplace = True)
		dataset.set_index("Semana", inplace = True)
		dataset.columns.name = f"{cidade}"
		x = dataset.drop(columns = "CASOS")
		y = dataset["CASOS"]
		if x.empty or x.isnull().all().all():
			print(f"'X' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		x = x.dropna()
		if x.empty:
			print(f"'X' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		if y.empty or y.isnull().all().all():
			print(f"'Y' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		y = y.dropna()
		if y.empty:
			print(f"'Y' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		x_array = x.to_numpy()
		x_array = x_array.reshape(x_array.shape[0], -1)
		x_array = x.to_numpy().astype(int)
		y_array = y.to_numpy().astype(int)
		x_array = x_array.reshape(x_array.shape[0], -1)
		print(dataset)
		return dataset, x, y, x_array, y_array

	def testa_dataset_focos(self, cidade):
		"""
		Função para montar estrutura de teste de dados para previsão.
		"""
		dataset = tmin[["Semana"]].copy()
		dataset["TMIN"] = tmin[cidade].copy()
		dataset["TMED"] = tmed[cidade].copy()
		dataset["TMAX"] = tmax[cidade].copy()
		dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
		dataset.dropna(axis = 0, inplace = True)
		troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS"}
		dataset = dataset.rename(columns = troca_nome)
		dataset.fillna(0, inplace = True)
		#dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
		#dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
		dataset["TMED_r8"] = dataset["TMED"].shift(-8)
		dataset["TMED_r10"] = dataset["TMED"].shift(-10)
		#dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
		#dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
		dataset["PREC_r1"] = dataset["PREC"].shift(-1)
		dataset["PREC_r2"] = dataset["PREC"].shift(-2)
		#dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
		dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC"], inplace = True)
		dataset.dropna(inplace = True)
		dataset.set_index("Semana", inplace = True)
		dataset.columns.name = f"{cidade}"
		x = dataset.drop(columns = "FOCOS")
		y = dataset["FOCOS"]
		if x.empty or x.isnull().all().all():
			print(f"'X' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		x = x.dropna()
		if x.empty:
			print(f"'X' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {x}")
			return None, None, None, None, None
		if y.empty or y.isnull().all().all():
			print(f"'Y' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		y = y.dropna()
		if y.empty:
			print(f"'Y' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
			print(f"{cidade} possui um conjunto com erro:\n {y}")
			return None, None, None, None, None
		x_array = x.to_numpy()
		x_array = x_array.reshape(x_array.shape[0], -1)
		x_array = x.to_numpy().astype(int)
		y_array = y.to_numpy().astype(int)
		x_array = x_array.reshape(x_array.shape[0], -1)
		print(dataset)
		return dataset, x, y, x_array, y_array

	def treino_teste(self, x, x_array, y_array):
		"""
		Função para separar o conjunto de dados em	treino e teste padrão aleatório
		"""
		treino_x, teste_x, treino_y, teste_y = train_test_split(x_array, y_array,
				                                            random_state = SEED,
				                                            test_size = 0.2)
		explicativas = x.columns.tolist()
		treino_x_explicado = pd.DataFrame(treino_x, columns = explicativas)
		treino_x_explicado = treino_x_explicado.to_numpy().astype(int)
		return treino_x, teste_x, treino_y, teste_y, treino_x_explicado, explicativas

	def treino_teste_limite(self, x, y, z):
		"""
		Função para separar o conjunto de dados em	treino do ano de 2023
		"""
		x_ate_limite = x.iloc[:-z]
		y_ate_limite = y.iloc[:-z]
		xlimite = x.iloc[-z:]
		ylimite = y.iloc[-z:]
		treino_x = x_ate_limite.copy()
		teste_x = xlimite.copy()
		treino_y = y_ate_limite.copy()
		teste_y = ylimite.copy()
		explicativas = x.columns.tolist()
		treino_x_explicado = pd.DataFrame(treino_x, columns = explicativas)
		treino_x_explicado = treino_x_explicado.to_numpy().astype(int)
	
		print(f"""Conjunto de Treino com as Variáveis Explicativas (<2023):\n{treino_x}\n
Conjunto de Treino com as Variáveis Explicativas (>2023):\n{teste_x}\n 
Conjunto de Teste com a Variável Dependente (<2023):\n{treino_y}\n 
Conjunto de Teste com a Variável Dependente (>2023):\n{teste_y}\n
Conjunto de Treino com as Variáveis Explicativas (Explicitamente Indicadas)(<2023):\n{treino_x_explicado}\n""")
		return treino_x, teste_x, treino_y, teste_y, treino_x_explicado, z, explicativas

		"""	
	def preve(x, treino_x_explicado):
		"""
		#Função para prever conjunto de dados
		"""
		y_previsto = random_forest.predict(treino_x_explicado)
		previsoes = random_forest.predict(x)
		previsoes = [int(p) for p in previsoes]
		return previsoes, y_previsto
		"""

	def metricas(self, str_var, dataset, previsoes, n, y):
		"""
		Função para validação por algumas métricas	
		"""
		print("="*80)
		var = dataset[str_var.upper()]
		print(f"\nRANDOM FOREST - {cidade}\n")
		lista_op = [f"{str_var} - {cidade}: {var[i]}\nPrevisão Random Forest: {previsoes[i]}\n" for i in range(n)]
		print("\n".join(lista_op))
		print("~"*80)
		EQM = mean_squared_error(y, previsoes).round(2)
		EMA = mean_absolute_error(y, previsoes).round(2)
		RQ_EQM = np.sqrt(EQM).round(2)
		R_2 = r2_score(y, previsoes).round(2)
		VIES = EMA - RQ_EQM
		VIES = round(VIES, 2)
		NIVEL_SIGNIFICANCIA = 0.95
		INTERCONFIANCA = st.t.interval(confidence = NIVEL_SIGNIFICANCIA, df = len(previsoes)-1,
										loc = np.mean(previsoes), scale = st.sem(previsoes))
		INTERCONFIANCA = tuple(round(value, 2) for value in INTERCONFIANCA)
		print(f"""
			 \n MÉTRICAS RANDOM FOREST - {cidade}
			 \n Coeficiente de Determinação (R²): {R_2}
			 \n Erro Quadrático Médio: {EQM}
			 \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
			 \n Erro Médio Absoluto: {EMA}
			 \n Viés: {VIES}
			 \n Intervalo de Confiança (nível de significância = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}
			 """)
		print("="*80)
		return R_2, EQM, RQ_EQM, EMA, VIES

	def grafico_previsao_casos(self, previsao, teste, limite):
		# Gráfico de Comparação entre Observação e Previsão dos Modelos
		final = pd.DataFrame()
		final["Semana"] = casos["Semana"]
		final["Casos"] = casos[cidade]
		final.drop([d for d in range(_retroagir)], axis=0, inplace = True)
		final.drop(final.index[-_retroagir:], axis=0, inplace = True)
		previsoes = previsao
		"""
		lista_previsao = [previsoes[v] for v in range(len(previsoes))]
		final["Previstos"] = lista_previsao
		"""
		previsoes = previsoes[:len(final)]
		final["Previstos"] = previsoes
		final["Semana"] = pd.to_datetime(final["Semana"])
		final["Erro"] = final["Casos"] - final["Previstos"]
		print(final)
		print("="*80)
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Casos"], # linestyle = "--" linestyle = "-."
				     color = "darkblue", linewidth = 1, label = "Observado")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		"""
		sns.lineplot(x = final["Semana"], y = final["Erro"],
				     color = "yellow", alpha = 0.5, linewidth = 5, label = "Erro")
		"""
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - OBSERVAÇÃO E PREVISÃO (Total):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas na Série Histórica de Anos")
		plt.ylabel("Número de Casos de Dengue")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_validacao}validacao_modelo_RF_casos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_validacao}validacao_modelo_RF_casos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Erro"], linestyle = "dotted",
                     color = "black", linewidth = 2, label = "Erro")#, bins = 500)#, element = "poly")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		sns.lineplot(x = final["Semana"], y = final["Casos"], # linestyle = "--" linestyle = "-."
				     color = "darkblue", linewidth = 1, label = "Observado")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (Total):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas na Série Histórica de Anos")
		plt.ylabel("Número de Casos de Dengue")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}erro_modelo_RF_casos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}erro_modelo_RF_casos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		EQM = mean_squared_error(final["Casos"], final["Previstos"]).round(2)
		EMA = mean_absolute_error(final["Casos"], final["Previstos"]).round(2)
		RQ_EQM = np.sqrt(EQM).round(2)
		R_2 = r2_score(final["Casos"], final["Previstos"]).round(2)
		VIES = EMA - RQ_EQM
		VIES = round(VIES, 2)
		NIVEL_SIGNIFICANCIA = 0.95
		INTERCONFIANCA = st.t.interval(confidence = NIVEL_SIGNIFICANCIA, df = len(final["Erro"])-1,
										loc = np.mean(final["Erro"]), scale = st.sem(final["Erro"]))
		INTERCONFIANCA = tuple(round(value, 2) for value in INTERCONFIANCA)
		print(f"""
			 \n MÉTRICAS RANDOM FOREST - {cidade}
			 \n Coeficiente de Determinação (R²): {R_2}
			 \n Erro Quadrático Médio: {EQM}
			 \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
			 \n Erro Médio Absoluto: {EMA}
			 \n Viés: {VIES}
			 \n Intervalo de Confiança do erro (nível de significância = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}
			 """)
		fig, axs = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw = {"height_ratios": [9, 1]},
								 sharex = True, layout = "constrained", frameon = False)
		Q1 = np.percentile(final["Erro"], [25])
		mediana = final["Erro"].median()
		Q3 = np.percentile(final["Erro"], [75])
		anomalia = Q3 + 1.5 * (Q3 - Q1)
		anomalia_negativa = Q1 - 1.5 * (Q3 - Q1)
		media, desvio_padrao = final["Erro"].mean(), final["Erro"].std()
		n, divisoes, patches = axs[0].hist(final["Erro"], bins = 50)#, bins = int((final["Erro"].max() * 4)))
		plt.xlabel("Erro")
		plt.ylabel("Quantidade")
		for patch, bin_valor in zip(patches, divisoes):
			if bin_valor <= anomalia_negativa:
				patch.set_facecolor("red")
			elif bin_valor <= Q1:
				patch.set_facecolor("lime")
			elif bin_valor <= mediana:
				patch.set_facecolor("seagreen")
			elif bin_valor <= Q3:
				patch.set_facecolor("seagreen")
			elif bin_valor <= anomalia:
				patch.set_facecolor("lime")
			else:
				patch.set_facecolor("red")
		linha_hist_media = axs[0].axvline(x = media, linestyle = "--", color = "darkblue", label = "média")
		linha_hist_mediana = axs[0].axvline(x = mediana, linestyle = "--", color = "darkorange", label = "mediana")
		intervalo_confianca = axs[0].axvspan(INTERCONFIANCA[0], INTERCONFIANCA[1], color = "lightblue", alpha=0.5, label = "intervalo de confiança", hatch = "\\")
		axs[0].legend(handles = [linha_hist_media, linha_hist_mediana, intervalo_confianca])
		fig.text(0.9, 0.75, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
		fig.text(0.6, 0.7, f"R²: {R_2}\nEQM: {EQM}\nRQEQM: {RQ_EQM}\nEMA: {EMA}\nViés: {VIES}\nIntervalo de Confiança ($\\alpha$ = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}", fontsize = 12)
		axs[0].set_facecolor("honeydew")
		#axs[0].grid(True)
		caixa = dict(color = "darkgreen", facecolor = "seagreen")
		bigodes = dict(color = "lime")
		outliers = dict(marker = "o", markerfacecolor = "red", markersize = 4, markeredgecolor = "black")
		linha_mediana = dict( color = "darkorange", linestyle= "-", linewidth = 2.5)
		ponto_media = dict(markerfacecolor = "blue", markeredgecolor = "black")
		axs[1].boxplot(final["Erro"], vert = False, showmeans = True, notch = True, patch_artist = True,
					boxprops = caixa, whiskerprops = bigodes, flierprops = outliers,
					medianprops = linha_mediana, meanprops = ponto_media)#, color = "green")
		axs[1].set_facecolor("honeydew")
		#axs[1].grid(True)
		fig.suptitle(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (Total):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}histogramaerro_modelo_RF_casos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}histogramaerro_modelo_RF_casos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		print("="*80)

	def grafico_previsao_casos_limite(self, previsao, teste, z, limite, fim):
		# Gráfico de Comparação entre Observação e Previsão dos Modelos
		final = pd.DataFrame()
		final["Semana"] = casos["Semana"].iloc[-z:]
		final["Casos"] = casos[cidade].iloc[-z:]
		previsoes = previsao
		"""
		lista_previsao = [previsoes[v] for v in range(len(previsoes))]
		final["Previstos"] = lista_previsao
		"""
		previsoes = previsoes[:len(final)]
		final["Previstos"] = previsoes
		final["Semana"] = pd.to_datetime(final["Semana"])
		final["Erro"] = final["Casos"] - final["Previstos"]
		print(final)
		print("="*80)
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Casos"],
				     color = "darkblue", linewidth = 1, label = "Observado")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - OBSERVAÇÃO E PREVISÃO (20{fim}):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas em 2023")
		plt.ylabel("Número de Casos de Dengue")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_validacao}validacao_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_validacao}validacao_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Erro"], linestyle = "dotted",
                     color = "black", linewidth = 2, label = "Erro")#, bins = 500)#, element = "poly")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		sns.lineplot(x = final["Semana"], y = final["Casos"], # linestyle = "--" linestyle = "-."
				     color = "darkblue", linewidth = 1, label = "Observado")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (20{fim}) - CASOS:\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas")
		plt.ylabel("Número de Casos de Dengue")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}erro_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}erro_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		EQM = mean_squared_error(final["Casos"], final["Previstos"]).round(2)
		EMA = mean_absolute_error(final["Casos"], final["Previstos"]).round(2)
		RQ_EQM = np.sqrt(EQM).round(2)
		R_2 = r2_score(final["Casos"], final["Previstos"]).round(2)
		VIES = EMA - RQ_EQM
		VIES = round(VIES, 2)
		NIVEL_SIGNIFICANCIA = 0.95
		INTERCONFIANCA = st.t.interval(confidence = NIVEL_SIGNIFICANCIA, df = len(final["Erro"])-1,
										loc = np.mean(final["Erro"]), scale = st.sem(final["Erro"]))
		INTERCONFIANCA = tuple(round(value, 2) for value in INTERCONFIANCA)
		print(f"""
			 \n MÉTRICAS RANDOM FOREST - {cidade}
			 \n Coeficiente de Determinação (R²): {R_2}
			 \n Erro Quadrático Médio: {EQM}
			 \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
			 \n Erro Médio Absoluto: {EMA}
			 \n Viés: {VIES}
			 \n Intervalo de Confiança do erro (nível de significância = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}
			 """)
		fig, axs = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw = {"height_ratios": [9, 1]},
								 sharex = True, layout = "constrained", frameon = False)
		Q1 = np.percentile(final["Erro"], [25])
		mediana = final["Erro"].median()
		Q3 = np.percentile(final["Erro"], [75])
		anomalia = Q3 + 1.5 * (Q3 - Q1)
		anomalia_negativa = Q1 - 1.5 * (Q3 - Q1)
		media, desvio_padrao = final["Erro"].mean(), final["Erro"].std()
		n, divisoes, patches = axs[0].hist(final["Erro"], bins = 50)#, bins = int((final["Erro"].max() * 4)))
		plt.xlabel("Erro")
		plt.ylabel("Quantidade")
		for patch, bin_valor in zip(patches, divisoes):
			if bin_valor <= anomalia_negativa:
				patch.set_facecolor("red")
			elif bin_valor <= Q1:
				patch.set_facecolor("lime")
			elif bin_valor <= mediana:
				patch.set_facecolor("seagreen")
			elif bin_valor <= Q3:
				patch.set_facecolor("seagreen")
			elif bin_valor <= anomalia:
				patch.set_facecolor("lime")
			else:
				patch.set_facecolor("red")
		linha_hist_media = axs[0].axvline(x = media, linestyle = "--", color = "darkblue", label = "média")
		linha_hist_mediana = axs[0].axvline(x = mediana, linestyle = "--", color = "darkorange", label = "mediana")
		intervalo_confianca = axs[0].axvspan(INTERCONFIANCA[0], INTERCONFIANCA[1], color = "lightblue", alpha=0.5, label = "intervalo de confiança", hatch = "\\")
		axs[0].legend(handles = [linha_hist_media, linha_hist_mediana, intervalo_confianca])
		fig.text(0.9, 0.75, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
		fig.text(0.6, 0.7, f"R²: {R_2}\nEQM: {EQM}\nRQEQM: {RQ_EQM}\nEMA: {EMA}\nViés: {VIES}\nIntervalo de Confiança ($\\alpha$ = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}", fontsize = 12)
		axs[0].set_facecolor("honeydew")
		#axs[0].grid(True)
		caixa = dict(color = "darkgreen", facecolor = "seagreen")
		bigodes = dict(color = "lime")
		outliers = dict(marker = "o", markerfacecolor = "red", markersize = 4, markeredgecolor = "black")
		linha_mediana = dict( color = "darkorange", linestyle= "-", linewidth = 2.5)
		ponto_media = dict(markerfacecolor = "blue", markeredgecolor = "black")
		axs[1].boxplot(final["Erro"], vert = False, showmeans = True, notch = True, patch_artist = True,
					boxprops = caixa, whiskerprops = bigodes, flierprops = outliers,
					medianprops = linha_mediana, meanprops = ponto_media)#, color = "green")
		axs[1].set_facecolor("honeydew")
		#axs[1].grid(True)
		fig.suptitle(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (20{fim}) - CASOS:\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}histogramaerro_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}histogramaerro_modelo_RF_casos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		print("="*80)

	def grafico_previsao_focos(self, previsao, teste, limite):
		# Gráfico de Comparação entre Observação e Previsão dos Modelos
		final = pd.DataFrame()
		final["Semana"] = focos["Semana"]
		final["Focos"] = focos[cidade]
		final.drop([d for d in range(_retroagir)], axis=0, inplace = True)
		final.drop(final.index[-_retroagir:], axis=0, inplace = True)
		previsoes = previsao
		previsoes = previsoes[:len(final)]
		final["Previstos"] = previsoes
		final["Semana"] = pd.to_datetime(final["Semana"])
		final["Erro"] = final["Focos"] - final["Previstos"]
		print(final)
		print("="*80)
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Focos"], # linestyle = "--" linestyle = "-."
				     color = "darkblue", linewidth = 1, label = "Observado")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - OBSERVAÇÃO E PREVISÃO (Total):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas na Série Histórica de Anos")
		plt.ylabel("Número de Focos de _Aedes_ sp.")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_validacao}validacao_modelo_RF_focos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_validacao}validacao_modelo_RF_focos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Erro"], linestyle = "dotted",
                     color = "black", linewidth = 2, label = "Erro")#, bins = 500)#, element = "poly")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		sns.lineplot(x = final["Semana"], y = final["Focos"], # linestyle = "--" linestyle = "-."
				     color = "darkblue", linewidth = 1, label = "Observado")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (Total):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas na Série Histórica de Anos")
		plt.ylabel("Número de Focos de _Aedes_ sp.")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}erro_modelo_RF_focos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}erro_modelo_RF_focos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		EQM = mean_squared_error(final["Focos"], final["Previstos"]).round(2)
		EMA = mean_absolute_error(final["Focos"], final["Previstos"]).round(2)
		RQ_EQM = np.sqrt(EQM).round(2)
		R_2 = r2_score(final["Focos"], final["Previstos"]).round(2)
		VIES = EMA - RQ_EQM
		VIES = round(VIES, 2)
		NIVEL_SIGNIFICANCIA = 0.95
		INTERCONFIANCA = st.t.interval(confidence = NIVEL_SIGNIFICANCIA, df = len(final["Erro"])-1,
										loc = np.mean(final["Erro"]), scale = st.sem(final["Erro"]))
		INTERCONFIANCA = tuple(round(value, 2) for value in INTERCONFIANCA)
		print(f"""
			 \n MÉTRICAS RANDOM FOREST - {cidade}
			 \n Coeficiente de Determinação (R²): {R_2}
			 \n Erro Quadrático Médio: {EQM}
			 \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
			 \n Erro Médio Absoluto: {EMA}
			 \n Viés: {VIES}
			 \n Intervalo de Confiança do erro (nível de significância = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}
			 """)
		fig, axs = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw = {"height_ratios": [9, 1]},
								 sharex = True, layout = "constrained", frameon = False)
		Q1 = np.percentile(final["Erro"], [25])
		mediana = final["Erro"].median()
		Q3 = np.percentile(final["Erro"], [75])
		anomalia = Q3 + 1.5 * (Q3 - Q1)
		anomalia_negativa = Q1 - 1.5 * (Q3 - Q1)
		media, desvio_padrao = final["Erro"].mean(), final["Erro"].std()
		n, divisoes, patches = axs[0].hist(final["Erro"], bins = 50)#, bins = int((final["Erro"].max() * 4)))
		plt.xlabel("Erro")
		plt.ylabel("Quantidade")
		for patch, bin_valor in zip(patches, divisoes):
			if bin_valor <= anomalia_negativa:
				patch.set_facecolor("red")
			elif bin_valor <= Q1:
				patch.set_facecolor("lime")
			elif bin_valor <= mediana:
				patch.set_facecolor("seagreen")
			elif bin_valor <= Q3:
				patch.set_facecolor("seagreen")
			elif bin_valor <= anomalia:
				patch.set_facecolor("lime")
			else:
				patch.set_facecolor("red")
		linha_hist_media = axs[0].axvline(x = media, linestyle = "--", color = "darkblue", label = "média")
		linha_hist_mediana = axs[0].axvline(x = mediana, linestyle = "--", color = "darkorange", label = "mediana")
		intervalo_confianca = axs[0].axvspan(INTERCONFIANCA[0], INTERCONFIANCA[1], color = "lightblue", alpha=0.5, label = "intervalo de confiança", hatch = "\\")
		axs[0].legend(handles = [linha_hist_media, linha_hist_mediana, intervalo_confianca])
		fig.text(0.9, 0.75, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
		fig.text(0.6, 0.7, f"R²: {R_2}\nEQM: {EQM}\nRQEQM: {RQ_EQM}\nEMA: {EMA}\nViés: {VIES}\nIntervalo de Confiança ($\\alpha$ = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}", fontsize = 12)
		axs[0].set_facecolor("honeydew")
		#axs[0].grid(True)
		caixa = dict(color = "darkgreen", facecolor = "seagreen")
		bigodes = dict(color = "lime")
		outliers = dict(marker = "o", markerfacecolor = "red", markersize = 4, markeredgecolor = "black")
		linha_mediana = dict( color = "darkorange", linestyle= "-", linewidth = 2.5)
		ponto_media = dict(markerfacecolor = "blue", markeredgecolor = "black")
		axs[1].boxplot(final["Erro"], vert = False, showmeans = True, notch = True, patch_artist = True,
					boxprops = caixa, whiskerprops = bigodes, flierprops = outliers,
					medianprops = linha_mediana, meanprops = ponto_media)#, color = "green")
		axs[1].set_facecolor("honeydew")
		#axs[1].grid(True)
		fig.suptitle(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (Total) - FOCOS:\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}histogramaerro_modelo_RF_focos_{_cidade}_{limite}-total.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}histogramaerro_modelo_RF_focos_{_cidade}_{limite}-total.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		print("="*80)

	def grafico_previsao_focos_limite(self, previsao, teste, z, limite, fim):
		# Gráfico de Comparação entre Observação e Previsão dos Modelos
		final = pd.DataFrame()
		final["Semana"] = focos["Semana"].iloc[-z:]
		final["Focos"] = focos[cidade].iloc[-z:]
		previsoes = previsao
		"""
		lista_previsao = [previsoes[v] for v in range(len(previsoes))]
		final["Previstos"] = lista_previsao
		"""
		previsoes = previsoes[:len(final)]
		final["Previstos"] = previsoes
		final["Semana"] = pd.to_datetime(final["Semana"])
		final["Erro"] = final["Focos"] - final["Previstos"]
		print(final)
		print("="*80)
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Focos"],
				     color = "darkblue", linewidth = 1, label = "Observado")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - OBSERVAÇÃO E PREVISÃO (20{fim}):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas em 2023")
		plt.ylabel("Número de Focos de _Aedes_ sp.")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_validacao}validacao_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_validacao}validacao_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		plt.figure(figsize = (10, 6), layout = "constrained", frameon = False)
		sns.lineplot(x = final["Semana"], y = final["Erro"], linestyle = "dotted",
                     color = "black", linewidth = 2, label = "Erro")
		sns.lineplot(x = final["Semana"], y = final["Focos"],
				     color = "darkblue", linewidth = 1, label = "Observado")
		sns.lineplot(x = final["Semana"], y = final["Previstos"],
				     color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
		plt.title(f"MODELO RANDOM FOREST (20{limite}) - OBSERVAÇÃO E PREVISÃO (20{fim}):\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		plt.xlabel("Semanas Epidemiológicas em 2023")
		plt.ylabel("Número de Focos de _Aedes_ sp.")
		plt.gca().set_facecolor("honeydew")
		if _SALVAR == True:
			plt.savefig(f'{caminho_validacao}erro_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_validacao}erro_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		EQM = mean_squared_error(final["Focos"], final["Previstos"]).round(2)
		EMA = mean_absolute_error(final["Focos"], final["Previstos"]).round(2)
		RQ_EQM = np.sqrt(EQM).round(2)
		R_2 = r2_score(final["Focos"], final["Previstos"]).round(2)
		VIES = EMA - RQ_EQM
		VIES = round(VIES, 2)
		NIVEL_SIGNIFICANCIA = 0.95
		INTERCONFIANCA = st.t.interval(confidence = NIVEL_SIGNIFICANCIA, df = len(final["Erro"])-1,
										loc = np.mean(final["Erro"]), scale = st.sem(final["Erro"]))
		INTERCONFIANCA = tuple(round(value, 2) for value in INTERCONFIANCA)
		print(f"""
			 \n MÉTRICAS RANDOM FOREST - {cidade}
			 \n Coeficiente de Determinação (R²): {R_2}
			 \n Erro Quadrático Médio: {EQM}
			 \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
			 \n Erro Médio Absoluto: {EMA}
			 \n Viés: {VIES}
			 \n Intervalo de Confiança do erro (nível de significância = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}
			 """)
		fig, axs = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw = {"height_ratios": [9, 1]},
								 sharex = True, layout = "constrained", frameon = False)
		Q1 = np.percentile(final["Erro"], [25])
		mediana = final["Erro"].median()
		Q3 = np.percentile(final["Erro"], [75])
		anomalia = Q3 + 1.5 * (Q3 - Q1)
		anomalia_negativa = Q1 - 1.5 * (Q3 - Q1)
		media, desvio_padrao = final["Erro"].mean(), final["Erro"].std()
		n, divisoes, patches = axs[0].hist(final["Erro"], bins = 50)#, bins = int((final["Erro"].max() * 4)))
		plt.xlabel("Erro")
		plt.ylabel("Quantidade")
		for patch, bin_valor in zip(patches, divisoes):
			if bin_valor <= anomalia_negativa:
				patch.set_facecolor("red")
			elif bin_valor <= Q1:
				patch.set_facecolor("lime")
			elif bin_valor <= mediana:
				patch.set_facecolor("seagreen")
			elif bin_valor <= Q3:
				patch.set_facecolor("seagreen")
			elif bin_valor <= anomalia:
				patch.set_facecolor("lime")
			else:
				patch.set_facecolor("red")
		linha_hist_media = axs[0].axvline(x = media, linestyle = "--", color = "darkblue", label = "média")
		linha_hist_mediana = axs[0].axvline(x = mediana, linestyle = "--", color = "darkorange", label = "mediana")
		intervalo_confianca = axs[0].axvspan(INTERCONFIANCA[0], INTERCONFIANCA[1], color = "lightblue", alpha=0.5, label = "intervalo de confiança", hatch = "\\")
		axs[0].legend(handles = [linha_hist_media, linha_hist_mediana, intervalo_confianca])
		fig.text(0.9, 0.75, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
		fig.text(0.6, 0.7, f"R²: {R_2}\nEQM: {EQM}\nRQEQM: {RQ_EQM}\nEMA: {EMA}\nViés: {VIES}\nIntervalo de Confiança ($\\alpha$ = {NIVEL_SIGNIFICANCIA}): {INTERCONFIANCA}", fontsize = 12)
		axs[0].set_facecolor("honeydew")
		#axs[0].grid(True)
		caixa = dict(color = "darkgreen", facecolor = "seagreen")
		bigodes = dict(color = "lime")
		outliers = dict(marker = "o", markerfacecolor = "red", markersize = 4, markeredgecolor = "black")
		linha_mediana = dict( color = "darkorange", linestyle= "-", linewidth = 2.5)
		ponto_media = dict(markerfacecolor = "blue", markeredgecolor = "black")
		axs[1].boxplot(final["Erro"], vert = False, showmeans = True, notch = True, patch_artist = True,
					boxprops = caixa, whiskerprops = bigodes, flierprops = outliers,
					medianprops = linha_mediana, meanprops = ponto_media)#, color = "green")
		axs[1].set_facecolor("honeydew")
		#axs[1].grid(True)
		fig.suptitle(f"MODELO RANDOM FOREST (20{limite}) - DISTRIBUIÇÃO DO ERRO (20{fim}) - FOCOS:\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
		if _SALVAR == True:
			plt.savefig(f'{caminho_erro}histogramaerro_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_erro}histogramaerro_modelo_RF_focos_{_cidade}_{limite}-{fim}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		print("="*80)

	def metricas_importancias(self, modelo, explicativas, var_str, limite = None):
		importancias = modelo.feature_importances_
		importancias = importancias.round(4)
		indices = np.argsort(importancias)[::-1]
		variaveis_importantes = pd.DataFrame({"Variáveis": explicativas, "Importâncias": importancias})
		variaveis_importantes = variaveis_importantes.sort_values(by = "Importâncias", ascending = False)
		importancia_impureza = pd.Series(importancias, index = explicativas)
		print(variaveis_importantes)
		#1 Impurezas
		std = np.std([tree.feature_importances_ for tree in modelo.estimators_], axis=0)
		fig, ax = plt.subplots(figsize = (10, 6), layout = "constrained", frameon = False)
		importancia_impureza = importancia_impureza.sort_values(ascending = False)
		importancia_impureza.plot.barh(xerr = std, ax = ax)
		if limite == None:
			ax.set_title(f"VARIÁVEIS IMPORTANTES PARA MODELO RANDOM FOREST.\nMUNICÍPIO DE {cidade}, SANTA CATARINA.")
		else:
			ax.set_title(f"VARIÁVEIS IMPORTANTES PARA MODELO RANDOM FOREST.\nMUNICÍPIO DE {cidade}, SANTA CATARINA. {limite}.")
		ax.set_xlabel("Impureza Média")
		if var_str == "casos":
			ax.set_ylabel("Variáveis Explicativas para Modelagem de Casos de Dengue")
		elif var_str == "focos":
			ax.set_ylabel("Variáveis Explicativas para Modelagem de Focos de _Aedes_ sp.")
		ax.set_facecolor("honeydew")
		plt.yticks(rotation = 30)
		for i, (feature, importance) in enumerate(importancia_impureza.items()):
			if importance > 0.5 * ax.get_xlim()[1]:
				ax.text(importance - 0.1, i, f"{round(importance, 4)}(+/-{std[i].round(4)})", color = "black", va = "center", ha = "right")
			else:
				ax.text(importance + 0.1, i, f"{round(importance, 4)}(+/-{std[i].round(4)})", color = "black", va = "center", ha = "left")
		#fig.tight_layout()
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_importancia}importancia_pureza_modelo_RF_{var_str}_{_cidade}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_importancia}importancia_pureza_modelo_RF_{var_str}_{_cidade}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		#2 Permutações
		n_permuta = 10
		resultado_permuta = permutation_importance(modelo, teste_x, teste_y, n_repeats = n_permuta, random_state = SEED, n_jobs = 2)
		importancia_permuta = pd.Series(resultado_permuta.importances_mean, index = explicativas)
		importancia_permuta = importancia_permuta.sort_values(ascending = False)
		fig, ax = plt.subplots(figsize = (10, 6), layout = "constrained", frameon = False)
		importancia_permuta.plot.barh(xerr = resultado_permuta.importances_std, ax = ax)
		if limite == None:
			ax.set_title(f"VARIÁVEIS IMPORTANTES UTILIZANDO PERMUTAÇÃO ({n_permuta}).\nMUNICÍPIO DE {cidade}, SANTA CATARINA.")
		else:
			ax.set_title(f"VARIÁVEIS IMPORTANTES UTILIZANDO PERMUTAÇÃO ({n_permuta}).\nMUNICÍPIO DE {cidade}, SANTA CATARINA. {limite}")
		ax.set_xlabel("Acurácia Média")
		if var_str == "casos":
			ax.set_ylabel("Variáveis Explicativas para Modelagem de Casos de Dengue")
		elif var_str == "focos":
			ax.set_ylabel("Variáveis Explicativas para Modelagem de Focos de _Aedes_ sp.")
		ax.set_facecolor("honeydew")
		plt.yticks(rotation = 30)
		for i, (feature, importance) in enumerate(importancia_impureza.items()):
			if importance > 0.5 * ax.get_xlim()[1]:
				ax.text(importance - 0.1, i, f"{round(importance, 4)} (+/-{resultado_permuta.importances_std[i].round(4)})",
						color = "black", va = "center", ha = "right")
			else:
				ax.text(importance + 0.1, i, f"{round(importance, 4)} (+/-{resultado_permuta.importances_std[i].round(4)})",
						color = "black", va = "center", ha = "left")
		#fig.tight_layout()
		if _SALVAR == True:
			plt.savefig(f'{caminho_importancia}importancia_permuta{n_permuta}_modelo_RF_{var_str}_{_cidade}.pdf', format = "pdf", dpi = 1200)
			print(f'\nARQUIVO SALVO COM SUCESSO\n\n{caminho_importancia}importancia_permuta{n_permuta}_modelo_RF_{var_str}_{_cidade}.pdf\n')
		if _VISUALIZAR == True:
			plt.show()
		print(f"\nVARIÁVEIS IMPORTANTES:\n{importancia_impureza}\n")
		print(f"\nVARIÁVEIS IMPORTANTES UTILIZANDO PERMUTAÇÃO:\n{importancia_permuta}")
		return importancias, indices, variaveis_importantes 

	def caminho_decisao(self, x, modelo, explicativas, var_str):
		#amostra = x.iloc[0].values.reshape(1, -1)
		#caminho, _ = modelo.decision_path(amostra)
		#caminho_denso = caminho.toarray()
		unica_arvore = modelo.estimators_[0]
		relatorio_decisao = export_text(unica_arvore, feature_names = explicativas,
										spacing = 5, decimals = 0, show_weights = True)
		plt.figure(figsize = (25, 10), layout = "constrained", frameon = False)
		ax = plt.gca()
		for i, child in enumerate(ax.get_children()):
			if isinstance(child, plt.Line2D):
				if i % 2 == 0:
					child.set_color("red")
				else:
					child.set_color("blue")
		plt.title(f"ÁRVORE DE DECISÃO DO MODELO RANDOM FOREST.\nMUNICÍPIO DE {cidade}, SANTA CATARINA. {var_str.upper()}.")
		plot_tree(unica_arvore, feature_names = explicativas, filled = True, rounded = True, fontsize = 6,
					proportion = True, node_ids = True, precision = 0, impurity = False)#, max_depth = 6) # impureza = ErroQuadrático
		ax.set_facecolor("honeydew")
		if _SALVAR == True:
			troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		     'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		     'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		     'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		     'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		     'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
			_cidade = cidade
			for velho, novo in troca.items():
				_cidade = _cidade.replace(velho, novo)
			plt.savefig(f'{caminho_importancia}arvore_decisao_modelo_RF_{var_str}_{_cidade}.pdf', format = "pdf", dpi = 1200)
			print(f"\n{ansi['green']}ARQUIVO SALVO COM SUCESSO\n\n{caminho_importancia}arvore_decisao_modelo_RF_{var_str}_{_cidade}.pdf{ansi['reset']}\n")
			with open(f'{caminho_importancia}arvore_decisao_modelo_RF_{var_str}_{_cidade}.txt', 'w') as file:
				file.write(relatorio_decisao)
			print(f"\n{ansi['green']}ARQUIVO SALVO COM SUCESSO\n\n{caminho_importancia}arvore_decisao_modelo_RF_{var_str}_{_cidade}.txt{ansi['reset']}\n")
		if _VISUALIZAR == True:
			print("\n\n{ansi['green']}RELATÓRIO DA ÁRVORE DE DECISÃO\n\n{cidade}\n\n{var_str.upper()}{ansi['reset']}\n\n", relatorio_decisao)
			plt.show()
		#print("\n\nCAMINHO DE DECISÃO\n\n", caminho_denso)
		return unica_arvore, relatorio_decisao #amostra, caminho, caminho_denso
		
####################################### Orientação a Objetos #######################################

_SALVAR = True

_VISUALIZAR = False

_AUTOMATIZA = True

if _AUTOMATIZA == True:
	lista_cidades = ["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]
	for cidade in lista_cidades:
		##### CASOS
		modelo = Modelo()
		_retroagir, _horizonte = modelo.variar(3, 2)
		dataset, x, y, x_array, y_array = modelo.monta_dataset_casos(cidade)
		### Totaldata
		treino_x, teste_x, treino_y, teste_y, treino_x_explicado, explicativas = modelo.treino_teste(x, x_array, y_array)
		random_forest = modelo.abre_modelo("casos", cidade, _retroagir)
		unica_arvore, relatorio_decisao = modelo.caminho_decisao(x, random_forest, explicativas, "casos")
		y_previsto = random_forest.predict(treino_x_explicado)
		previsoes = random_forest.predict(x)
		previsoes = [int(p) for p in previsoes]
		print(y_previsto)
		print(previsoes)
		R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("casos", dataset, previsoes, 500, y)
		modelo.grafico_previsao_casos(previsoes, y, "22")
		importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "casos")

		### Apenas 2023
		treino_x, teste_x, treino_y, teste_y, treino_x_explicado, z, explicativas = modelo.treino_teste_limite(x, y, 50) # z == 50 (ano de 2023)
		random_forest = modelo.abre_modelo("casos", cidade, _retroagir)
		y_previsto = random_forest.predict(treino_x_explicado)
		previsoes23 = random_forest.predict(teste_x)
		previsoes = [int(p) for p in previsoes23]
		print(y_previsto)
		print(previsoes)
		R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("casos", dataset, previsoes, 5, teste_y)
		modelo.grafico_previsao_casos_limite(previsoes, teste_y, z, "22", "23")
		importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "casos", "2023")

		##### FOCOS
		modelo = Modelo()
		_retroagir, _horizonte = modelo.variar(8, 4)
		dataset, x, y, x_array, y_array = modelo.monta_dataset_focos(cidade)
		#dataset, x, y, x_array, y_array = modelo.testa_dataset_focos(cidade)
		### Total
		treino_x, teste_x, treino_y, teste_y, treino_x_explicado, explicativas = modelo.treino_teste(x, x_array, y_array)
		random_forest = modelo.abre_modelo("focos", cidade, _retroagir)
		unica_arvore, relatorio_decisao = modelo.caminho_decisao(x, random_forest, explicativas, "focos")
		y_previsto = random_forest.predict(treino_x_explicado)
		previsoes = random_forest.predict(x)
		previsoes = [int(p) for p in previsoes]
		print(y_previsto)
		print(previsoes)
		R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("focos", dataset, previsoes, 500, y)
		modelo.grafico_previsao_focos(previsoes, y, "22")
		importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "focos")

		### Apenas 2023
		treino_x, teste_x, treino_y, teste_y, treino_x_explicado, z, explicativas = modelo.treino_teste_limite(x, y, 50) # z == 50 (ano de 2023)
		random_forest = modelo.abre_modelo("focos", cidade, _retroagir)
		y_previsto = random_forest.predict(treino_x_explicado)
		previsoes23 = random_forest.predict(teste_x)
		previsoes = [int(p) for p in previsoes23]
		print(y_previsto)
		print(previsoes)
		R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("focos", dataset, previsoes, 5, teste_y)
		modelo.grafico_previsao_focos_limite(previsoes, teste_y, z, "22", "23")
		importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "focos", "2023")
else:
	##### CASOS
	modelo = Modelo()
	_retroagir, _horizonte = modelo.variar(3, 2)
	dataset, x, y, x_array, y_array = modelo.monta_dataset_casos(cidade)
	### Totaldata
	treino_x, teste_x, treino_y, teste_y, treino_x_explicado, explicativas = modelo.treino_teste(x, x_array, y_array)
	random_forest = modelo.abre_modelo("casos", cidade, _retroagir)
	y_previsto = random_forest.predict(treino_x_explicado)
	previsoes = random_forest.predict(x)
	unica_arvore, relatorio_decisao = modelo.caminho_decisao(x, random_forest, explicativas, "casos")
	previsoes = [int(p) for p in previsoes]
	print(y_previsto)
	print(previsoes)
	R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("casos", dataset, previsoes, 500, y)
	modelo.grafico_previsao_casos(previsoes, y, "22")
	importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "casos")

	### Apenas 2023
	treino_x, teste_x, treino_y, teste_y, treino_x_explicado, z, explicativas = modelo.treino_teste_limite(x, y, 50) # z == 50 (ano de 2023)
	random_forest = modelo.abre_modelo("casos", cidade, _retroagir)
	y_previsto = random_forest.predict(treino_x_explicado)
	previsoes23 = random_forest.predict(teste_x)
	previsoes = [int(p) for p in previsoes23]
	print(y_previsto)
	print(previsoes)
	R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("casos", dataset, previsoes, 5, teste_y)
	modelo.grafico_previsao_casos_limite(previsoes, teste_y, z, "22", "23")
	importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "casos", "2023")

	##### FOCOS
	modelo = Modelo()
	_retroagir, _horizonte = modelo.variar(8, 4)
	dataset, x, y, x_array, y_array = modelo.monta_dataset_focos(cidade)
	#dataset, x, y, x_array, y_array = modelo.testa_dataset_focos(cidade)
	### Total
	treino_x, teste_x, treino_y, teste_y, treino_x_explicado, explicativas = modelo.treino_teste(x, x_array, y_array)
	random_forest = modelo.abre_modelo("focos", cidade, _retroagir)
	unica_arvore, relatorio_decisao = modelo.caminho_decisao(x, random_forest, explicativas, "focos")
	y_previsto = random_forest.predict(treino_x_explicado)
	previsoes = random_forest.predict(x)
	previsoes = [int(p) for p in previsoes]
	print(y_previsto)
	print(previsoes)
	R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("focos", dataset, previsoes, 500, y)
	modelo.grafico_previsao_focos(previsoes, y, "22")
	importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "focos")

	### Apenas 2023
	treino_x, teste_x, treino_y, teste_y, treino_x_explicado, z, explicativas = modelo.treino_teste_limite(x, y, 50) # z == 50 (ano de 2023)
	random_forest = modelo.abre_modelo("focos", cidade, _retroagir)
	y_previsto = random_forest.predict(treino_x_explicado)
	previsoes23 = random_forest.predict(teste_x)
	previsoes = [int(p) for p in previsoes23]
	print(y_previsto)
	print(previsoes)
	R_2, EQM, RQ_EQM, EMA, VIES = modelo.metricas("focos", dataset, previsoes, 5, teste_y)
	modelo.grafico_previsao_focos_limite(previsoes, teste_y, z, "22", "23")
	importancias, indices, variaveis_importantes =  modelo.metricas_importancias(random_forest, explicativas, "focos", "2023")
