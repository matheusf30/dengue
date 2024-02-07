### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
## Dados "Brutos"
focosdive = "focos_dive_total.csv"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focosdive = pd.read_csv(f"{caminho_dados}{focosdive}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Limpeza de Dados
focosdive = focosdive[["Regional", "Município", "Imóvel", "Depósito", "Data da Coleta"]]
#focosdive["Município"] = focosdive["Município"].str.upper()

pontos = municipios[["NM_MUN", "geometry"]]
pontos["municipio"] = pontos["NM_MUN"].str.upper()
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["municipio", "ponto"]]
print(pontos)

### Printando Informações
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focosdive.info())
print("~"*80)
print(focosdive.dtypes)
print("~"*80)
print(focosdive)
print("="*80)

print("\n \n MUNICÍPIOS DE SANTA CATARINA (IBGE) \n")
print(municipios.info())
print("~"*80)
print(municipios.dtypes)
print("~"*80)
print(municipios)
print("="*80)

print("\n \n MUNICÍPIOS DE SANTA CATARINA (IBGE- centróide) \n")
print(pontos.info())
print("~"*80)
print(pontos.dtypes)
print("~"*80)
print(pontos)
print("="*80)

municipios.plot()
plt.show()



