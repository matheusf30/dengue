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

### Limpeza de Dados / Unindo Tabelas
focosdive = focosdive[["Regional", "Município", "Imóvel", "Depósito", "Data da Coleta"]]
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
pontos = cidades.copy()
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
focos_timespace = pd.merge(focosdive, pontos, on = "Município", how = "left")
focos_timespace = pd.merge(focos_timespace, cidades, on = "Município", how = "left")
focos_timespace = focos_timespace.drop(columns = ["NM_MUN_x", "NM_MUN_y"])

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

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print(focos_timespace.info())
print("~"*80)
print(focos_timespace.dtypes)
print("~"*80)
print(focos_timespace)
print("="*80)

focos_timespace.to_csv(f"{caminho_dados}focos_timespace.csv", index = False)

municipios.plot()
plt.show()
