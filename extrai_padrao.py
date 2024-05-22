### Bibliotecas Correlatas
# Suporte
import sys, os
# Básicas
import pandas as pd
import numpy as np
"""
import matplotlib.pyplot as plt               
import seaborn as sns
import statsmodels as sm
"""

### Encaminhamento aos Diretórios
try:
    _LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
    if _LOCAL == "GH": # _ = Variável Privada
        caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    elif _LOCAL == "CASA":
        caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    elif _LOCAL == "IFSC":
        caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
        caminho_merge = "/dados/operacao/merge/CDO.MERGE/"
        caminho_samet = "/dados/operacao/samet/clima/"
    else:
        print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
except:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR CAMINHO OU LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")


### Renomeação variáveis pelos arquivos
prec = "prec_diario_ate_2023.csv"
tmax = "tmax_diario_ate_2023.csv"
tmed = "tmed_diario_ate_2023.csv"
tmin = "tmin_diario_ate_2023.csv"


### Abrindo Arquivos
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")



### Pré-processamento e Definição de Função
ansi = {"bold" : "\033[1m", "red" : "\033[91m", "green" : "\033[92m", 
        "yellow" : "\033[33m", "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}


def prepross_var(var, str_var):
	var.set_index("Data", inplace = True)
	var.drop(columns = str_var, inplace = True)
	#tmin.dropna(inplace = True)
	print(f"\n{ansi['green']}{str_var}{ansi['reset']}\n", var)
	return var

def limiar_tmin(x):
	if x > 15:
		return 1
	else:
		return 0


def limiar_tmax(x):
	if x < 32:
		return 1
	else:
		return 0


def limiar_prec50(x):
	if pd.isnull(x):
		return 0
	elif x < 15:
		return 0
	else:
		return 1

def semana_epidemiologica(csv, str_var):
	"""
	Função relativa ao agrupamento de dados em semanas epidemiológicas.
	Os arquivos.csv são provenientes deo roteiro 'extrai_clima.py': colunas com datas e municípios + todas as linhas são dados diários.
	Estes Arquivos estão alocados no SifapSC ou GitHub.
	Argumento:
	- Variável com arquivo.csv;
	- String da variável referente ao arquivo.csv.
	Retorno:
	- Retorno próprio de DataFrame com Municípios (centróides) em Colunas e Tempo (semanas epidemiológicas) em Linhas, preenchidos com valores climáticos.
	- Salvando Arquivo.csv
	"""
	csv.reset_index(inplace = True)
	csv["Data"] = pd.to_datetime(csv["Data"])
	csv = csv.sort_values(by = ["Data"])
	csv_se = csv.copy()
	csv_se["Semana"] = csv_se["Data"].dt.to_period("W-SAT").dt.to_timestamp()
	csv_se = csv_se.groupby(["Semana"]).sum(numeric_only = True)
	"""
	if str_var == "prec":
		csv_se = csv_se.groupby(["Semana"]).sum(numeric_only = True)
	else:
		csv_se = csv_se.groupby(["Semana"]).mean(numeric_only = True)
	"""
	csv_se.reset_index(inplace = True)
	csv_se.drop([0], axis = 0, inplace = True)
	#csv_se.to_csv(f"{caminho_dados}{str_var}_semana_ate_2023.csv", index = False)
	print(f"\n{ansi['green']}ARQUIVO SALVO COM SUCESSO!\n\nSemana Epidemiológica - {str_var.upper()}{ansi['reset']}\n\n{csv_se}\n")
	print(f"\n{ansi['red']}As variáveis do arquivo ({str_var.upper()}), em semanas epidemiológicas, são:{ansi['reset']}\n{csv_se.dtypes}\n")
	return csv_se

tmin = prepross_var(tmin, "tmin")
tmed = prepross_var(tmed, "tmed")
tmax = prepross_var(tmax, "tmax")
prec = prepross_var(prec, "prec")


lim_tmin = tmin.applymap(lambda x: limiar_tmin(x))
lim_tmax = tmax.applymap(lambda x: limiar_tmax(x))
lim_prec50 = prec.applymap(lambda x: limiar_prec50(x))

print(f"\n{ansi['green']}LIMIAR TMIN{ansi['reset']}\n", lim_tmin)
print(f"\n{ansi['green']}LIMIAR TMAX{ansi['reset']}\n", lim_tmax)
print(f"\n{ansi['green']}LIMIAR PREC 50{ansi['reset']}\n", lim_prec50)

lim_tmin = semana_epidemiologica(lim_tmin, "tmin")
lim_tmax = semana_epidemiologica(lim_tmax, "tmax")
lim_prec50 = semana_epidemiologica(lim_prec50, "prec")


print(f"\n{ansi['green']}LIMIAR TMIN{ansi['reset']}\n", lim_tmin)
print(f"\n{ansi['green']}LIMIAR TMAX{ansi['reset']}\n", lim_tmax)
print(f"\n{ansi['green']}LIMIAR PREC{ansi['reset']}\n", lim_prec50)

sys.exit()
"""
for cidade in tmin.columns:
	for valor in tmin[cidade]:
		if valor > 15:
			valor = 1
		else:
			valor = 0
"""

#print(tmin)


sys.exit()

"""
# Define a function to replace values based on the condition
def replace_value(x):
	x = int(x)
    if x > 15:
		return 1
    else:
        return 0

# Apply the function to each element in the DataFrame
tmin = tmin.applymap(replace_value)

"""
print("!!"*80)
print(f"\n{green}{bold}FINALIZADA ATUALIZAÇÃO{bold}{reset}\n\nAtualização feita em produtos de reanálise até {red}{_ANO_FINAL}{reset}!\n")
print(f"{bold}(MERGE e SAMeT - tmin, tmed, tmax){bold}")
print("!!"*80)
