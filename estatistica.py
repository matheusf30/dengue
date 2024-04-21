### Bibliotecas Correlatas
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import pymannkendall as mk
#from sklearn.preprocessing import NormalityTest
from scipy.stats import shapiro, normaltest
import statsmodels.api as sm

### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _local == "IFSC":
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
	mannkendall = mk.original_test(csv[cidade])
	print(f"\nMANN KENDALL DE {cidade} = {mannkendall}.\n")

def teste_normal(cidade, csv, str_var):
	decomposicao = sm.tsa.seasonal_decompose(csv[cidade], model = "additive", period = 52)
	tendencia = decomposicao.trend
	sazonalidade = decomposicao.seasonal
	residuo = decomposicao.resid
	#teste_normal = NormalityTest()
	#shapiro_teste, shapiro_valor_p = teste_normal.shapiro(csv[cidade])
	shapiro_teste, shapiro_valor_p = shapiro(csv[cidade])
	print(f"\n{cidade}\nTeste Estatístico Shapiro-Wik: {shapiro_teste}\nValor $ p $: {round(shapiro_valor_p, 5)}\n")
	shapiro_teste, shapiro_valor_p = shapiro(residuo)
	print(f"\n{cidade} - Sem Sazonal\nTeste Estatístico Shapiro-Wik: {shapiro_teste}\nValor $ p $: {round(shapiro_valor_p, 5)}\n")
	#dagostino_teste, dagostino_valor_p = teste_normal.dagostino(csv[cidade])
	dagostino_teste, dagostino_valor_p = normaltest(csv[cidade])
	print(f"\n{cidade}\nTeste Estatístico Dagostino: {dagostino_teste}\nValor $ p $: {round(dagostino_valor_p, 5)}\n")
	dagostino_teste, dagostino_valor_p = normaltest(residuo)
	print(f"\n{cidade} - Sem Sazonal\nTeste Estatístico Dagostino: {dagostino_teste}\nValor $ p $: {round(dagostino_valor_p, 5)}\n")
	plt.figure(figsize = (12, 8))
	plt.subplot(411)
	plt.plot(csv[cidade], label = "Original")
	plt.legend(loc = "upper left")
	plt.title(f"{cidade} - {str_var.upper()}")
	plt.grid(True)
	plt.subplot(412)
	plt.plot(tendencia, label = "Tendência")
	plt.legend(loc = "upper left")
	plt.grid(True)
	plt.subplot(413)
	plt.plot(sazonalidade, label = "Sazonalidade")
	plt.legend(loc = "upper left")
	plt.grid(True)
	plt.subplot(414)
	plt.plot(residuo, label = "Residual")
	plt.legend(loc = "upper left")
	plt.grid(True)
	plt.xlabel("Semanas Epidemiológicas")
	plt.tight_layout()
	troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
             'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
             'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
             'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
             'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
             'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
	for velho, novo in troca.items():
		cidade = cidade.replace(velho, novo)
	plt.savefig(f"{caminho_estatistica}distribuicao_{str_var}_{cidade}.pdf", format = "pdf", dpi = 1200)
	plt.show()
	

### Visualização
"""
for i in lista_cidades:
	visualiza_focos(i, focos)

for i in lista_cidades:
	tendencia(i, focos)
"""
for i in lista_cidades:
	teste_normal(i, focos, "focos")
	#teste_normal(i, casos)
	#teste_normal(i, prec)
	#teste_normal(i, tmin)
	#teste_normal(i, tmed)
	#teste_normal(i, tmax)

### Exibindo Informações
print("\n \n FOCOS DE _Aedes_ spp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)
print(cidades)

