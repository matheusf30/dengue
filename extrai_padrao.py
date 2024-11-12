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

prec_sem = "prec_semana_ate_2023.csv"
tmax_sem = "tmax_semana_ate_2023.csv"
tmed_sem = "tmed_semana_ate_2023.csv"
tmin_sem = "tmin_semana_ate_2023.csv"

### Abrindo Arquivos
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")

prec_sem = pd.read_csv(f"{caminho_dados}{prec_sem}")
tmax_sem = pd.read_csv(f"{caminho_dados}{tmax_sem}")
tmed_sem = pd.read_csv(f"{caminho_dados}{tmed_sem}")
tmin_sem = pd.read_csv(f"{caminho_dados}{tmin_sem}")



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

tmin.set_index("Data", inplace = True)
tmin.drop(columns = "tmin", inplace = True)
print(tmin)
tmed.set_index("Data", inplace = True)
tmed.drop(columns = "tmed", inplace = True)
print(tmed)
tmax.set_index("Data", inplace = True)
tmax.drop(columns = "tmax", inplace = True)
print(tmax)
prec.set_index("Data", inplace = True)
prec.drop(columns = "prec", inplace = True)
print(prec)

tmin_sem.set_index("Semana", inplace = True)
print(tmin_sem)
tmed_sem.set_index("Semana", inplace = True)
print(tmed_sem)
tmax_sem.set_index("Semana", inplace = True)
print(tmax_sem)
prec_sem.set_index("Semana", inplace = True)
print(prec_sem)


print(f"\n{ansi['green']}TMIN{ansi['reset']}\n", tmin[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}TMED{ansi['reset']}\n", tmed[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}TMAX{ansi['reset']}\n", tmax[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}PREC{ansi['reset']}\n", prec[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())

print(f"\n{ansi['green']}TMIN SEMANAL{ansi['reset']}\n", tmin_sem[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}TMED SEMANAL{ansi['reset']}\n", tmed_sem[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}TMAX SEMANAL{ansi['reset']}\n", tmax_sem[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())
print(f"\n{ansi['green']}PREC SEMANAL{ansi['reset']}\n", prec_sem[["FLORIANÓPOLIS", "ITAJAÍ", "JOINVILLE", "CHAPECÓ"]].describe())

print(f"""{ansi['green']}TMIN ESTADUAL{ansi['reset']}
Mínima: {round(tmin.min().min(), 1)} C
Média: {round(tmin.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmin.std().max(), 1)} C
Máxima: {round(tmin.max().max(), 1)} C""")

print(f"""{ansi['green']}TMED ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {round(tmed.min().min(), 1)} C
Média: {round(tmed.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmed.std().max(), 1)} C
Máxima: {round(tmed.max().max(), 1)} C""")

print(f"""{ansi['green']}TMAX ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {round(tmax.min().min(), 1)} C
Média: {round(tmax.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmax.std().max(), 1)} C
Máxima: {round(tmax.max().max(), 1)} C""")

print(f"""{ansi['green']}PREC ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {round(prec.min().min(), 1)} mm
Média: {round(prec.mean().mean(), 1)} mm
Desvio Padrão Máximo: {round(prec.std().max(), 1)} mm
Máxima: {round(prec.max().max(), 1)} mm""")

print(f"""{ansi['green']}TMIN ESTADUAL SEMANAL{ansi['reset']}
Mínima: {round(tmin_sem.min().min(), 1)} C
Média: {round(tmin_sem.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmin_sem.std().max(), 1)} C
Máxima: {round(tmin_sem.max().max(), 1)} C""")

print(f"""{ansi['green']}TMED ESTADUAL SEMANAL{ansi['reset']}
Mínima: {round(tmed_sem.min().min(), 1)} C
Média: {round(tmed_sem.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmed_sem.std().max(), 1)} C
Máxima: {round(tmed_sem.max().max(), 1)} C""")

print(f"""{ansi['green']}TMAX ESTADUAL SEMANAL{ansi['reset']}
Mínima: {round(tmax_sem.min().min(), 1)} C
Média: {round(tmax_sem.mean().mean(), 1)} C
Desvio Padrão Máximo: {round(tmax_sem.std().max(), 1)} C
Máxima: {round(tmax_sem.max().max(), 1)} C""")

print(f"""{ansi['green']}PREC ESTADUAL SEMANAL{ansi['reset']}
Mínima: {round(prec_sem.min().min(), 1)} mm
Média: {round(prec_sem.mean().mean(), 1)} mm
Desvio Padrão Máximo: {round(prec_sem.std().max(), 1)} mm
Máxima: {round(prec_sem.max().max(), 1)} mm""")

###

#min_columns = df.idxmin(axis=1)

print(f"""{ansi['green']}TMIN ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {tmin.idxmin(axis=1).min()}
Máxima: {tmin.idxmax(axis=1).max()}""")

print(f"""{ansi['green']}TMED ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {tmed.idxmin(axis=1).min()}
Máxima: {tmed.idxmax(axis=1).max()}""")

print(f"""{ansi['green']}TMAX ESTADUAL DIÁRIA{ansi['reset']}
Mínima: {tmax.idxmin(axis=1).min()}
Máxima: {tmax.idxmax(axis=1).max()}""")

print(f"""{ansi['green']}TMIN ESTADUAL SEMANAL{ansi['reset']}
Mínima: {tmin_sem.idxmin(axis=1).min()}
Máxima: {tmin_sem.idxmax(axis=1).max()}""")

print(f"""{ansi['green']}TMED ESTADUAL SEMANAL{ansi['reset']}
Mínima: {tmed_sem.idxmin(axis=1).min()}
Máxima: {tmed_sem.idxmax(axis=1).max()}""")

print(f"""{ansi['green']}TMAX ESTADUAL SEMANAL{ansi['reset']}
Mínima: {tmax_sem.idxmin(axis=1).min()}
Máxima: {tmax_sem.idxmax(axis=1).max()}""")

prec = prec.apply(pd.to_numeric, errors='coerce').dropna()
prec = prec.idxmax(axis=1).max()
#prec = prec.max()
print(f"""{ansi['green']}PREC ESTADUAL DIÁRIA{ansi['reset']}
Máxima: {prec}""")

#prec_sem = prec.apply(pd.to_numeric, errors='coerce')
prec_sem = prec_sem.idxmax(axis=1).max()
#prec_sem = prec_sem.max()
print(f"""{ansi['green']}PREC ESTADUAL SEMANAL{ansi['reset']}
Máxima: {prec_sem}""")

sys.exit()

Mínima: {prec.idxmin(axis=1).min()}

Mínima: {prec_sem.idxmin(axis=1).min()}


print(f"""{ansi['green']}PREC ESTADUAL SEMANAL{ansi['reset']}
Mínima: {prec_sem.idxmin(axis=1).min()}
Máxima: {prec_sem.idxmax(axis=1).max()}""")


tmin = prepross_var(tmin, "tmin")
tmed = prepross_var(tmed, "tmed")
tmax = prepross_var(tmax, "tmax")
prec = prepross_var(prec, "prec")

limiares_tmin = [5, 10, 15, 20]
for limiar_tmin in limiares_tmin:
	lim_tmin = tmin.applymap(lambda x: 1 if x < limiar_tmin else 0)
	print(f"\n{ansi['green']}LIMIAR TMIN ({limiar_tmin} C){ansi['reset']}\n", lim_tmin)


limiares_tmax = [20, 25, 30, 35]
for limiar_tmax in limiares_tmax:
	#lim_tmax = tmax.applymap(lambda x: limiar_tmax(x))
	lim_tmax = tmax.applymap(lambda x: 1 if x > limiar_tmin else 0)
	print(f"\n{ansi['green']}LIMIAR TMAX ({limiar_tmax} C){ansi['reset']}\n", lim_tmin)

limiares_prec = [5, 10, 25, 50]
for limiar_prec in limiares_prec:
	#lim_tmax = tmax.applymap(lambda x: limiar_tmax(x))
	lim_prec = prec.applymap(lambda x: 1 if x > limiar_prec else 0)
	print(f"\n{ansi['green']}LIMIAR PREC ({limiar_prec} mm){ansi['reset']}\n", lim_prec)

sys.exit()

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
