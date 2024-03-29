"""
AO RECEBER OS DADOS BRUTOS DA DIRETORIA DE VIGILÂNCIA EPIDEMIOLÓGICA DO ESTADO DE SANTA CATARINA, SIGA ESTE FLUXO:
	une_focos_dive.py >> focos_timespace.py >> focos_pivot.py
ASSIM, SERÃO GERADOS NOVOS ARQUIVOS:
	\focos_dive_total.csv
(Tabela "melt" com todas as informações presentes, incluindo valores faltantes.
  8 colunas: Regional, Município, Imóvel, Depósito, Tipo de Atividade, Data de Coleta, Nº Foco, Localidade.
Há mudança de metodologia de coleta dos dados ao longo do tempo)
	\focos_timespace_xy.csv
(Tabela "melt" com algumas informações presentes e nenhum dado faltante.
  5 colunas: Semana*, Município, Focos**, Latitude***, Longitude***.)
	\focos_pivot.csv
(Tabela "pivot" com informações sobre focos** presentes e nenhum dado faltante.
  x colunas: Semana*, xMunicípio.
As colunas não estão ordenadas alfabeticamente.)

*SEMPRE QUE A SEMANA FOR REFERENCIADA, DEIXAR CLARO SER SEMANA _EPIDEMIOLÓGICA_.
**SEMPRE QUE O FOCOS [sic] FOR REFERENCIADO, DEIXAR CLARO SER QUANTIDADE DE FOCOS REGISTRADOS.
***ESSAS COORDENADAS SÃO CENTRÓIDES DOS POLÍGONOS DE CADA MUNICÍPIO.
""" 
### Bibliotecas Correlatas
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import pymannkendall as mk

### Encaminhamento aos Diretórios
_local = "CASA" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
focos = "focos_pivot.csv"
cidade = "Florianópolis"
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]

### Abrindo Arquivo
focos = pd.read_csv(f"{caminho_dados}{focos}")

### Pré-Processamento
cidade = cidade.upper()
cidades = focos.columns
focos['Semana'] = pd.to_datetime(focos['Semana'])#, format="%Y%m%d")

### Estatística de Tendência
#mk = mk.original_test(focos[cidade])

### Definindo Função
def visualiza(cidade, focos):
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

def tendencia(cidade, focos):
	mannkendall = mk.original_test(focos[cidade])
	print(f"\nMANN KENDALL DE {cidade} = {mannkendall}.\n")

### Visualização
for i in lista_cidades:
	visualiza(i, focos)

for i in lista_cidades:
	tendencia(i, focos)

### Exibindo Informações
print("\n \n FOCOS DE _Aedes_ spp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)
print(cidades)

