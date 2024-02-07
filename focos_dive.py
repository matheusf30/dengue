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
municipios.plot()
plt.show()


### Limpeza de Dados
pontos = municipios[["CD_MUN", "NM_MUN", "geometry"]]
pontos["municipio"] = pontos["NM_MUN"]
#print(type(pontos))
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["CD_MUN", "municipio", "ponto"]]
#print(type(pontos))
pontos['latitude'] = pontos["ponto"].y
pontos['longitude'] = pontos["ponto"].x
# pontos['lat'] = pontos["ponto"].apply(lambda p: p.y)
# pontos['lon'] = pontos["ponto"].apply(lambda p: p.x)
pontos = pontos[["municipio", "latitude", "longitude"]]
#pontos.to_csv("pontos_sc.csv")
#print(type(pontos))
print(pontos)
