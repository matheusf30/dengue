### Bibliotecas Correlatas
"""
# Biblioteca para visualização gráfica de script python executado no terminal
sudo apt-get install python3-tk
import matplotlib
matplotlib.use("TkAgg")
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import numpy as np
import pymannkendall as mk
#from sklearn.preprocessing import NormalityTest
from scipy.stats import shapiro, normaltest
import statsmodels.api as sm
import unicodedata

### Condicionantes

_SALVAR = True

_VISUALIZAR = True

### Encaminhamento aos Diretórios
_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _LOCAL == "GH": # _ = Variável Privada
	caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _LOCAL == "CASA":
	caminho_dados = "/home/mfsouza90/Documents/git_matheusf30/dados_dengue/"
	caminho_estatistica = "/home/mfsouza90/Documents/git_matheusf30/dengue/resultados/estatistica/"
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
def normalizando_nome_cidade(cidade):
	"""
	Função para tratar acentos dos nomes das cidades.
	Entrada: Nome da cidade (str.upper());
	Retorno: Nome da cidade tratado (str.upper()).
	"""
	cidade = unicodedata.normalize("NFD", cidade)  # Normalize to decomposed form
	cidade = ''.join(c for c in cidade if unicodedata.category(c) != 'Mn')  # Remove diacritic marks
	#return ''.join(c for c in unicodedata.normalize("NFD", cidade) if unicodedata.category(c) != "Mn")
	troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
	_cidade = cidade
	for velho, novo in troca.items():
		_cidade = _cidade.replace(velho, novo)
	return _cidade

def visualiza_focos(cidade, focos):
	fig = plt.figure(figsize = (15, 8))
	eixo = fig.add_axes([0, 0, 1, 1])            # type: ignore
	eixo2 = fig.add_axes([0.08, 0.6, 0.55, 0.3]) # type: ignore

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
	Função para avaliar histograma e boxplot do conjunto de dados.
	Entrada: Nome da cidade (str.upper()), Conjunto de dados (.csv) e Nome da variável (str);
	Retorno: Exibindo e/ou salvando arquivo (.pdf) com a histograma e boxplot do conjunto de dados.
	"""
	fig, axs = plt.subplots(2, 1, figsize = (12, 8), gridspec_kw = {"height_ratios": [9, 1]},
							 sharex = True, layout = "constrained", frameon = False)
	Q1 = np.percentile(csv[cidade], [25])
	mediana = csv[cidade].median()
	Q3 = np.percentile(csv[cidade], [75])
	anomalia = Q3 + 1.5 * (Q3 - Q1)
	anomalia_negativa = Q1 - 1.5 * (Q3 - Q1)
	media, desvio_padrao = csv[cidade].mean(), csv[cidade].std()
	if str_var == "focos":
		n, divisoes, patches = axs[0].hist(csv[cidade], bins = int((csv[cidade].max() // 3)))#, rwidth = 0.95)#,
									#color = "blue", alpha = 0.9, rwidth = 1.1)#, label = "Histograma")
		plt.xlabel("Número de Registros de Focos de _Aedes_ sp.")
	elif str_var == "casos":
		n, divisoes, patches = axs[0].hist(csv[cidade], bins = int((csv[cidade].max() // csv[cidade].mean())))
		plt.xlabel("Número de Registros de Casos de Dengue")
	elif str_var == "prec":
		n, divisoes, patches = axs[0].hist(csv[cidade], bins = int((csv[cidade].max() // 6)))
		plt.xlabel("Precipitação (mm), Acumulada em Semanas Epidemiológicas")
	else:
		n, divisoes, patches = axs[0].hist(csv[cidade], bins = int(csv[cidade].max() * 4))
		plt.xlabel("Temperatura (C), Média em Semanas Epidemiológicas")
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
	axs[0].legend(handles = [linha_hist_media, linha_hist_mediana])
	if str_var == "tmin" or str_var == "tmed" or str_var == "tmax":
		fig.text(0.9, 0.8, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
	else:
		fig.text(0.9, 0.8, f"$ \\mu = {round(media, 2)} $ \n$\\sigma = {round(desvio_padrao, 2)} $ \nMd = {round(mediana, 2)}", fontsize = 12)
	plt.ylabel("Quantidade")
	axs[0].set_facecolor("honeydew")
	axs[0].grid(True)
	caixa = dict(color = "darkgreen", facecolor = "seagreen")
	bigodes = dict(color = "lime")
	outliers = dict(marker = "o", markerfacecolor = "red", markersize = 4, markeredgecolor = "black")
	linha_mediana = dict( color = "darkorange", linestyle= "-", linewidth = 2.5)
	ponto_media = dict(markerfacecolor = "blue", markeredgecolor = "black")
	axs[1].boxplot(csv[cidade], vert = False, showmeans = True, notch = True, patch_artist = True,
				boxprops = caixa, whiskerprops = bigodes, flierprops = outliers,
				medianprops = linha_mediana, meanprops = ponto_media)#, color = "green")
	axs[1].set_facecolor("honeydew")
	axs[1].grid(True)
	fig.suptitle(f"Distribuição: {cidade} - {str_var.upper()}")
	if _SALVAR == True:
		_cidade = normalizando_nome_cidade(cidade)
		plt.savefig(f"{caminho_estatistica}histograma_{str_var.upper()}_{_cidade}.pdf", format = "pdf", dpi = 1200)
		print(f"\n\nSALVO COM SUCESSO!\n\n{caminho_estatistica}histograma_{str_var.upper()}_{_cidade}.pdf\n\n")
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
	#csv = csv.iloc[:-208]
	decomposicao = sm.tsa.seasonal_decompose(csv[cidade], model = "additive", period = 52)
	tendencia = decomposicao.trend
	sazonalidade = decomposicao.seasonal
	residuo = decomposicao.resid
	mannkendall_sazo = mk.original_test(csv[cidade])
	mannkendall = mk.original_test(residuo)
	tendencia_sazo = mk.seasonal_test(csv[cidade])
	print(f"\nMANN KENDALL DE {cidade} COM SAZONALIDADE = {mannkendall_sazo}.\n")
	print(f"\nMANN KENDALL DE {cidade} SEM SAZONALIDADE = {mannkendall}.\n")
	print(f"\nSEASONAL MANN KENDALL DE {cidade} SEM SAZONALIDADE = {tendencia_sazo}.\n")
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
	shapiro_teste, shapiro_valor_p = shapiro(sazonalidade)
	print(f"""\n{cidade}- {str_var.upper()} - Apenas Sazonal
Teste Estatístico Shapiro-Wik: {shapiro_teste}
Valor $ p $: {round(shapiro_valor_p, 5)}\n""")
	#dagostino_teste, dagostino_valor_p = teste_normal.dagostino(csv[cidade])
	dagostino_teste, dagostino_valor_p = normaltest(residuo)
	print(f"""\n{cidade}- {str_var.upper()} - Sem Sazonal
Teste Estatístico Dagostino: {dagostino_teste}
Valor $ p $: {round(dagostino_valor_p, 5)}\n""")
	dagostino_teste, dagostino_valor_p = normaltest(sazonalidade)
	print(f"""\n{cidade}- {str_var.upper()} - Apenas Sazonal
Teste Estatístico Dagostino: {dagostino_teste}
Valor $ p $: {round(dagostino_valor_p, 5)}\n""")
	dagostino_teste, dagostino_valor_p = normaltest(csv[cidade])
	print(f"""\n{cidade}- {str_var.upper()}
Teste Estatístico Dagostino: {dagostino_teste}
Valor $ p $: {round(dagostino_valor_p, 5)}\n""")
	fig, axs = plt.subplots(4, 1, figsize = (12, 8), sharex = True)
	axs[0].plot(csv[cidade], label = "Original")
	axs[0].legend(loc = "upper left")
	fig.text(0.1, 0.8, f"Teste Estatístico D’Agostino-Pearson: {round(dagostino_teste, 5)}, Valor $ p $: {round(dagostino_valor_p, 5)}", fontsize = 10)
	axs[0].set_facecolor("honeydew")
	axs[0].grid(True)
	axs[1].plot(tendencia, label = "Tendência")
	axs[1].legend(loc = "upper left")
	fig.text(0.1, 0.6, f"Teste de Tendência Mann-Kendall Sazonal: {tendencia_sazo.trend}, Valor $ p $: {round(tendencia_sazo.p, 5)}, Tau: {round(tendencia_sazo.Tau, 5)}", fontsize = 10)
	axs[1].set_facecolor("honeydew")
	axs[1].grid(True)
	axs[2].plot(sazonalidade, label = "Sazonalidade")
	axs[2].legend(loc = "upper left")
	axs[2].set_facecolor("honeydew")
	axs[2].grid(True)
	axs[3].plot(residuo, label = "Residual")
	axs[3].legend(loc = "upper left")
	fig.text(0.1, 0.2, f"Teste de Tendência Mann-Kendall: {mannkendall.trend}, Valor $ p $: {round(mannkendall.p, 5)}, Tau: {round(mannkendall.Tau, 5)}", fontsize = 10)
	axs[3].set_facecolor("honeydew")
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
		_cidade = cidade
		for velho, novo in troca.items():
			_cidade = _cidade.replace(velho, novo)
			plt.savefig(f"{caminho_estatistica}distribuicao_{str_var.upper()}_{_cidade}.pdf", format = "pdf", dpi = 1200)
			print(f"\n\nSALVO COM SUCESSO!\n\n{caminho_estatistica}distribuicao_{str_var.upper()}_{_cidade}.pdf\n\n")
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
"""
for i in lista_cidades:
	teste_normal(i, focos, "focos")
	teste_normal(i, casos, "casos")
	teste_normal(i, prec, "prec")
	teste_normal(i, tmin, "tmin")
	teste_normal(i, tmed, "tmed")
	teste_normal(i, tmax, "tmax")
"""
histograma("FLORIANÓPOLIS", focos, "focos")
histograma("FLORIANÓPOLIS", casos, "casos")
histograma("FLORIANÓPOLIS", prec, "prec")
histograma("FLORIANÓPOLIS", tmin, "tmin")
histograma("FLORIANÓPOLIS", tmed, "tmed")
histograma("FLORIANÓPOLIS", tmax, "tmax")

for i in lista_cidades:
	histograma(i, focos, "focos")
	#histograma(i, casos, "casos")
	#histograma(i, prec, "prec")
	#histograma(i, tmin, "tmin")
	#histograma(i, tmed, "tmed")
	#histograma(i, tmax, "tmax")
"""
### Exibindo Informações
print("\n \n FOCOS DE _Aedes_ spp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)
print(cidades)

