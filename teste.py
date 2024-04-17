### Bibliotecas Correlatas
import pandas as pd
import sys

### Encaminhamento aos Diretórios
_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _LOCAL == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _LOCAL == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
## Série Histórica / _TEMPO / Extraídos de netCDF4 (MERGE e SAMeT)

_TEMPO = "semana" # "diario"
_ANO = "2023" # Até a última compilação de dados


# ANSI escape codes
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

"""
casos = "casos.csv"
focos = "focos_se.csv"
merge = "merge_se.csv"
"""
if _TEMPO == "diario":
	print(f"\n\n{red}!!!CUIDADO!!!\n\nOS DADOS ENTOMO-EPIDEMIOLÓGICOS NÃO SÃO REGISTROS DIÁRIOS\n\n!!!CUIDADO!!!\n\n{reset}")
casos = "casos_dive_pivot_total.csv"
focos = "focos_pivot.csv"
prec = f"prec_{_TEMPO}_ate_{_ANO}.csv"
tmax = f"tmax_{_TEMPO}_ate_{_ANO}.csv"
tmed = f"tmed_{_TEMPO}_ate_{_ANO}.csv"
tmin = f"tmin_{_TEMPO}_ate_{_ANO}.csv"

## Dados "Brutos"
"""
casos = "casos.csv"
focos = "focos.csv"
merge = "merge_novo.csv"
prec = "prec.csv"
tmax = "tmax.csv"
tmed = "tmed.csv"
tmin = "tmin.csv"
"""
## Série Histórica / Semana Epidemiológica
"""
casos = "casos.csv"
focos = "focos_se.csv"
merge = "merge_se.csv"
#prec = "prec.csv" # Dados Brutos
prec = "prec_diario_ate_2023.csv" # Dados Brutos
tmax = "tmax_se.csv"
tmed = "tmed_se.csv"
tmin = "tmin_se.csv"
"""
## (à partie de 2021 / Semana Epidemiológica
"""
casos = "casos21se.csv"
focos = "focos21se.csv"
merge = "merge21se.csv"
tmax = "tmax21se.csv"
tmed = "tmed21se.csv"
tmin = "tmin21se.csv"
"""
### Abrindo Arquivos
"""

merge = pd.read_csv(f"{caminho_dados}{merge}")
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
"""
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")

### Visualizando Informações

def visualiza_csv(csv, str_var = "None"):
	"""
	Função relativa a visualização dos dados e verificação de Valores Não-números (NaN) no arquivo.csv
	Argumento:
	- DataFrame da Variável com arquivo.csv aberto;
	- String da variável referente ao arquivo.csv. (pode não ser informado)
	Retorno: Visualização de dados e Exibição de mensagens para casos de haver ou não valores NaN.
	"""
	if str_var == "focos":
		print(f"\n \n {green}{bold}{str_var.upper()} (Dados Oficiais Dive/SC){reset} \n")
		print(f"{cyan}{str_var.upper()} - {red}Quantidade de {magenta}NaN{red}: {csv['FLORIANÓPOLIS'].isnull().sum()}{reset}")
		print(f"{red}As semanas com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}\n\n")
		if _TEMPO == "diario":
			print(f"{red}(APENAS SEMANAS EPIDEMIOLÓGICAS PRESENTES) com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}")
		elif _TEMPO == "semana":
			print(f"{red}As semanas com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}")
	elif str_var == "casos":
		print(f"\n \n {green}{bold}{str_var.upper()} (Dados Disponíveis em TABNET.Sinan){reset} \n")
		print(f"{cyan}{str_var.upper()} - {red}Quantidade de {magenta}NaN{red}: {csv['FLORIANÓPOLIS'].isnull().sum()}{reset}\n\n")
		print(f"{red}As semanas com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}\n\n")
		if _TEMPO == "diario":
			print(f"{red}(APENAS SEMANAS EPIDEMIOLÓGICAS PRESENTES) com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}")
		elif _TEMPO == "semana":
			print(f"{red}As semanas com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}")
	else:
		print(f"\n \n {green}{bold}{str_var.upper()} (Dados obtidos através do roteiro: extrai_clima.py){reset} \n")
		print(f"{cyan}{str_var.upper()} - {red}Quantidade de {magenta}NaN{red}: {csv['FLORIANÓPOLIS'].isnull().sum()}{reset}")
		if _TEMPO == "diario":
			print(f"{red}Os dias com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Data']}{reset}")
		elif _TEMPO == "semana":
			print(f"{red}As semanas com Valores {magenta}NaN{red} são:\n{csv[csv['FLORIANÓPOLIS'].isna()]['Semana']}{reset}")
	print(csv.info())
	print("~"*80)
	print(csv.dtypes)
	print("~"*80)
	print(csv)
	print("="*80)

visualiza_csv(prec, "prec")
visualiza_csv(tmin, "tmin")
visualiza_csv(tmed, "tmed")
visualiza_csv(tmax, "tmax")
visualiza_csv(casos, "casos")
visualiza_csv(focos, "focos")
"""
print("\n \n FOCOS DE _Aedes_ sp. \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
#print(focos.iloc[105:574, :]) #jan2014-dez2022
print(focos.iloc[522:574, :]) #jan2022-dez2022
print("="*80)

print("\n \n CASOS DE DENGUE \n")
print(casos.info())
print("~"*80)
print(casos.dtypes) 
print("~"*80)
#print(casos) #jan2014-dez2022
print(casos.iloc[417:, :]) #jan2022-dez2022
print("="*80)

print("\n \n PRECIPITAÇÃO \n")
print(merge.info())
print("~"*80)
print(merge.dtypes)
print("~"*80)
#print(merge.iloc[710:, :]) #jan2014-dez2022
print(merge.iloc[1127:, :]) #jan2022-dez2022
print("="*80)

print("\n \n PRECIPITAÇÃO (extrai_clima.py) \n")
print(prec.info())
print("~"*80)
print(prec.dtypes)
print("~"*80)
print(prec)
print("~"*80)
print(f"Quantidade de NaN: {prec['FLORIANÓPOLIS'].isnull().sum()}")
if _TEMPO == "diario":
	print(f"Os dias com Valores NaN são:\n{prec[prec['FLORIANÓPOLIS'].isna()]['Data']}")
elif _TEMPO == "semana":
	print(f"As semanas com Valores NaN são:\n{prec[prec['FLORIANÓPOLIS'].isna()]['Semana']}")
print("="*80)

print("\n \n TEMPERATURA MÍNIMA \n")
print(tmin.info())
print("~"*80)
print(tmin.dtypes)
print("~"*80)
print(tmin)
#print(tmin.iloc[732:, :]) #jan2014-dez2022
#print(tmin.iloc[1149:, :]) #jan2022-dez2022
print("="*80)

print("\n \n TEMPERATURA MÉDIA \n")
print(tmed.info())
print("~"*80)
print(tmed.dtypes)
print("~"*80)
print(tmed)
#print(tmed.iloc[732:, :]) #jan2014-dez2022
#print(tmed.iloc[1149:, :]) #jan2022-dez2022
print("="*80)

print("\n \n TEMPERATURA MÁXIMA \n")
print(tmax.info())
print("~"*80)
print(tmax.dtypes)
print("~"*80)
print(tmax)
#print(tmax.iloc[732:, :]) #jan2014-dez2022
#print(tmax.iloc[1149:, :]) #jan2022-dez2022
print("="*80)
"""
