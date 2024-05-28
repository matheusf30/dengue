### Bibliotecas Correlatas
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import numpy as np
import pymannkendall as mk
#from sklearn.preprocessing import NormalityTest
from scipy.stats import shapiro, normaltest
import statsmodels.api as sm

### Condicionantes

_SALVAR = False

_VISUALIZAR = True

### Encaminhamento aos Diretórios
_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _LOCAL == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _LOCAL == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _LOCAL == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
casos = "casos_dive_pivot_total.csv"
focos = "focos_pivot.csv"
prec = "prec_semana_ate_2023.csv"
tmin = "tmin_semana_ate_2023.csv"
tmed = "tmed_semana_ate_2023.csv"
tmax = "tmax_semana_ate_2023.csv"
cidade = "Florianópolis"
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}
#################################################################################

### Pré-Processamento
cidade = cidade.upper()
cidades = focos.columns
focos['Semana'] = pd.to_datetime(focos['Semana'])#, format="%Y%m%d")

### Estatística de Tendência
#mk = mk.original_test(focos[cidade])

### Definindo Função
def visualiza_focos(cidade, focos):
	fig = plt.figure(figsize = (15, 8))
	eixo = fig.add_axes([0, 0, 1, 1])
	eixo2 = fig.add_axes([0.08, 0.6, 0.55, 0.3])

	eixo.plot(focos["Semana"], focos[cidade], color = "r")
	eixo.set_xlim(datetime.datetime(2020,1,1), datetime.datetime(2022,12,4))
	eixo.set_ylim(0, focos[cidade].max() + 50)
	eixo.set_title(f"FOCOS DE _Aedes_ spp. EM {cidade}.", fontsize = 20, pad = 20)
	eixo.set_ylabel("Quantidade de Focos Registrados (n)", fontsize = 16)
	eixo.set_xlabel("Tempo (Semanas Epidemiológicas)", fontsize = 16)
	#eixo.legend([cidade], loc = "upper left", fontsize = 14)
	eixo.grid(True)

	azul_esquerda = focos["Semana"] < datetime.datetime(2020,1,1)
	azul_direita = focos["Semana"] > datetime.datetime(2022,12,4)

	eixo2.plot(focos["Semana"], focos[cidade], color = "r")
	eixo2.plot(focos[azul_esquerda]["Semana"], focos[azul_esquerda][cidade], color = "b")
	eixo2.plot(focos[azul_direita]["Semana"], focos[azul_direita][cidade], color = "b")
	eixo2.set_xlim(datetime.datetime(2012,1,1), datetime.datetime(2022,12,25))
	eixo2.set_title(f"FOCOS DE _Aedes_ spp. EM {cidade}.", fontsize = 15)
	eixo2.set_ylabel("Quantidade de Focos Registrados (n)", fontsize = 10)
	eixo2.set_xlabel("Tempo (Semanas Epidemiológicas)", fontsize = 10)
	eixo2.legend([cidade], loc = "best", fontsize = 8)
	eixo2.grid(True)
	plt.show()

def tendencia(cidade, csv):
	"""
	Função para avaliar tendência no conjunto de dados.
	Entrada: Nome da cidade (str.upper()) e Conjunto de dados (.csv);
	Retorno: em tela (terminal), visualização do teste para determinada cidade.
	Obs.: Aqui a sazonalidade está incluída!
	"""
	mannkendall = mk.original_test(csv[cidade])
	print(f"\nMANN KENDALL DE {cidade} = {mannkendall}.\n")

def histograma(cidade, csv, str_var):
	"""
	"""
	fig, axs = plt.subplots(2, 1, figsize=(12, 8), layout="constrained", frameon=False, gridspec_kw={'height_ratios': [3, 1]})

	# Calculate quartiles
	quartiles = np.percentile(csv[cidade], [25, 50, 75])

	# Plot histogram
	n, bins, patches = axs[0].hist(csv[cidade], bins='auto', color='blue', alpha=0.7, rwidth=0.85, label="Histograma")

	# Assign colors to histogram bars based on quartiles
	for patch, bin_value in zip(patches, bins):
		if bin_value <= quartiles[0]:
			patch.set_facecolor('green')  # Color for first quartile
		elif bin_value <= quartiles[1]:
			patch.set_facecolor('blue')   # Color for second quartile
		elif bin_value <= quartiles[2]:
			patch.set_facecolor('orange') # Color for third quartile
		else:
			patch.set_facecolor('red')    # Color for fourth quartile

	axs[0].legend(loc="upper right")
	axs[0].grid(True)

	# Plot boxplot
	boxplot_parts = axs[1].boxplot(csv[cidade], vert=False, patch_artist=True)

    # Set colors for boxplot components based on quartiles
	for patch in boxplot_parts['boxes']:
		median = np.median(patch.get_xdata())  # Get the median of the box
		if median <= quartiles[0]:
			patch.set_facecolor('green')   # Color for first quartile
		elif median <= quartiles[1]:
			patch.set_facecolor('blue')    # Color for second quartile
		elif median <= quartiles[2]:
			patch.set_facecolor('orange')  # Color for third quartile
		else:
			patch.set_facecolor('red')     # Color for fourth quartile

	for whisker in boxplot_parts['whiskers']:
		median = np.median(whisker.get_xdata())  # Get the median of the whisker
		if median <= quartiles[0]:
			whisker.set_color('green')   # Color for first quartile
		elif median <= quartiles[1]:
			whisker.set_color('blue')    # Color

	# Set grid for boxplot
	axs[1].grid(True)

	# Set title and labels
	fig.suptitle(f"Distribuição: {cidade} - {str_var.upper()}")
	plt.xlabel("Valor")
	if _SALVAR == True:
		_cidade = cidade.copy()
		troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
		for velho, novo in troca.items():
			_cidade = _cidade.replace(velho, novo)
			plt.savefig(f"{caminho_estatistica}histograma_{str_var.upper()}_{_cidade}.pdf", format = "pdf", dpi = 1200)
			print(f"\n\nSALVO COM SUCESSO!\n\n{caminho_estatistica}histograma_{str_var.upper()}_{cidade}.pdf\n\n")
	if _VISUALIZAR == True:
		print(f"\n\nVISUALIZANDO:\n\n{caminho_estatistica}histograma_{str_var.upper()}_{cidade}.pdf\n\n")
		plt.show()
		print(f"\n\nENCERRADO:\n\n{caminho_estatistica}histograma_{str_var.upper()}_{cidade}.pdf\n\n")


def teste_normal(cidade, csv, str_var):
	"""
	Função para avaliar decomposição sazonal e tendência no conjunto de dados.
	Entrada: Nome da cidade (str.upper()), Conjunto de dados (.csv) e Nome da variável (str);
	Retorno: - Em tela (terminal), visualização do teste de tendência para determinada cidade,
								tratando e não tratando sazonalidade.
			 - Exibindo e salvando arquivo (.pdf) com a decompsição sazonal do conjunto de dados.
	"""
	decomposicao = sm.tsa.seasonal_decompose(csv[cidade], model = "additive", period = 52)
	tendencia = decomposicao.trend
	sazonalidade = decomposicao.seasonal
	residuo = decomposicao.resid
	#teste_normal = NormalityTest()
	#shapiro_teste, shapiro_valor_p = teste_normal.shapiro(csv[cidade])
	shapiro_teste, shapiro_valor_p = shapiro(csv[cidade])
	print(f"""\n{cidade}- {str_var.upper()}
Teste Estatístico Shapiro-Wik: {shapiro_teste}
Valor $ p $: {round(shapiro_valor_p, 5)}\n""")
	shapiro_teste, shapiro_valor_p = shapiro(residuo)
	print(f"""\n{cidade}- {str_var.upper()} - Sem Sazonal
Teste Estatístico Shapiro-Wik: {shapiro_teste}
Valor $ p $: {round(shapiro_valor_p, 5)}\n""")
	#dagostino_teste, dagostino_valor_p = teste_normal.dagostino(csv[cidade])
	dagostino_teste, dagostino_valor_p = normaltest(csv[cidade])
	print(f"""\n{cidade}- {str_var.upper()}
Teste Estatístico Dagostino: {dagostino_teste}
Valor $ p $: {round(dagostino_valor_p, 5)}\n""")
	dagostino_teste, dagostino_valor_p = normaltest(residuo)
	print(f"""\n{cidade}- {str_var.upper()} - Sem Sazonal
Teste Estatístico Dagostino: {dagostino_teste}
Valor $ p $: {round(dagostino_valor_p, 5)}\n""")
	fig, axs = plt.subplots(4, 1, figsize = (12, 8), sharex = True)
	axs[0].plot(csv[cidade], label = "Original")
	axs[0].legend(loc = "upper left")
	axs[0].grid(True)
	axs[1].plot(tendencia, label = "Tendência")
	axs[1].legend(loc = "upper left")
	axs[1].grid(True)
	axs[2].plot(sazonalidade, label = "Sazonalidade")
	axs[2].legend(loc = "upper left")
	axs[2].grid(True)
	axs[3].plot(residuo, label = "Residual")
	axs[3].legend(loc = "upper left")
	axs[3].grid(True)
	fig.suptitle(f"Decomposição Sazonal: {cidade} - {str_var.upper()}")
	plt.xlabel("Semanas Epidemiológicas")
	plt.tight_layout()
	if _SALVAR == True:
		troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
		_cidade = cidade.copy()
		for velho, novo in troca.items():
			_cidade = _cidade.replace(velho, novo)
			plt.savefig(f"{caminho_estatistica}distribuicao_{str_var.upper()}_{_cidade}.pdf", format = "pdf", dpi = 1200)
			print(f"\n\nSALVO COM SUCESSO!\n\n{caminho_estatistica}distribuicao_{str_var.upper()}_{cidade}.pdf\n\n")
	if _VISUALIZAR == True:
		print(f"\n\nVISUALIZANDO:\n\n{caminho_estatistica}distribuicao_{str_var.upper()}_{cidade}.pdf\n\n")
		plt.show()
		print(f"\n\nENCERRADO:\n\n{caminho_estatistica}distribuicao_{str_var.upper()}_{cidade}.pdf\n\n")

	

### Visualização
"""
for i in lista_cidades:
	visualiza_focos(i, focos)

for i in lista_cidades:
	tendencia(i, focos)

for i in lista_cidades:
	teste_normal(i, focos, "focos")
	teste_normal(i, casos, "casos")
	teste_normal(i, prec, "prec")
	teste_normal(i, tmin, "tmin")
	teste_normal(i, tmed, "tmed")
	teste_normal(i, tmax, "tmax")
"""

histograma("FLORIANÓPOLIS", focos, "focos")


### Exibindo Informações
print("\n \n FOCOS DE _Aedes_ spp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)
print(cidades)

