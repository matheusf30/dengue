### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
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
focosdive = "focos_dive_total.csv"
municipios = "shapefiles/SC_Municipios_2022.shp"

### Abrindo Arquivo
focosdive = pd.read_csv(f"{caminho_dados}{focosdive}", low_memory = False)
municipios = gpd.read_file(f"{caminho_dados}{municipios}", low_memory = False)

### Pré-Processamento
## TEMPO (Padronizando Nomes e Somando Focos Agrupados por Semanas Epidemiológicas/Municípios)
"""
INICIANDO COM TROCA DE NOMES (CARACTÉRES, ACENTOS, TREMAS, LETRAS...)
# ! HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER...
rows_with_nan = focos_timespace[focos_timespace.isna().any(axis=1)]
print(rows_with_nan)
# ! HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER...
"""
focosdive = focosdive[["Regional", "Município", "Imóvel", "Depósito", "Data da Coleta"]]
trocanome = {
"HERVAL D`OESTE": "HERVAL D'OESTE",
"PRESIDENTE CASTELO BRANCO" : "PRESIDENTE CASTELLO BRANCO",
"SÃO CRISTOVÃO DO SUL" : "SÃO CRISTÓVÃO DO SUL",
"GRÃO PARÁ" : "GRÃO-PARÁ",
"LAURO MULLER" : "LAURO MÜLLER"
}
focosdive["Município"] = focosdive["Município"].replace(trocanome)
focosdive["Focos"] = np.ones(len(focosdive)).astype(int)
focosdive["Data"] = focosdive["Data da Coleta"].copy()
focosdive["Data"] = pd.to_datetime(focosdive["Data"])
focossemana = focosdive.copy()
focossemana["Semana"] = focossemana["Data"].dt.to_period("W-SAT").dt.to_timestamp()
focossemana = focossemana.groupby(["Semana", "Município"]).sum(numeric_only = True)["Focos"]
focossemana = focossemana.reset_index()
focossemana.to_csv(f"{caminho_dados}focos_se_dive.csv", index = False)
### ESPAÇO (Extraindo Latitude e Longitude do GeoDataFrame e Incluindo no DataFrame)
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
pontos = cidades.copy()
pontos["ponto"] = cidades["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
xy = pontos.copy()
xy["latitude"] = cidades["geometry"].centroid.y
xy["longitude"] = cidades["geometry"].centroid.x
focos_timespace_xy = pd.merge(focossemana, xy, on = "Município", how = "left")
focos_timespace_xy = focos_timespace_xy.drop(columns = ["NM_MUN", "ponto"])
### Municípios, Lat, Lon
unicos_xy = focos_timespace_xy[focos_timespace_xy["Focos"] > 0].drop_duplicates(subset = ["Município"])
"""
focos_timespace_poligono = pd.merge(focosdive, cidades, on = "Município", how = "left") # Data de Coleta e Polígonos
focos_timespace_centroide = pd.merge(focosdive, pontos, on = "Município", how = "left") # Data da Coleta e Centróides
focos_timespace_se_poligono = pd.merge(focossemana, cidades, on = "Município", how = "left") # Semanas Epidemiológicas e Polígonos
focos_timespace_se_centroide = pd.merge(focossemana, pontos, on = "Município", how = "left")# Semanas Epidemiológicas e Centróides
focos_timespace_poligono = focos_timespace_poligono.drop(columns = ["NM_MUN"])
focos_timespace_centroide = focos_timespace_centroide.drop(columns = ["NM_MUN"])
focos_timespace_se_poligono = focos_timespace_se_poligono.drop(columns = ["NM_MUN"])
focos_timespace_se_centroide = focos_timespace_se_centroide.drop(columns = ["NM_MUN"])
"""
### Salvando Arquivos
focos_timespace_xy.to_csv(f"{caminho_dados}focos_timespace_xy.csv", index = False) # Semanas Epidemiológicas, Latitudes e Longitudes
unicos_xy.to_csv(f"{caminho_dados}focos_primeiros.csv", index = False) # Primeiro Registro do Município
"""
focos_timespace_poligono.to_csv(f"{caminho_dados}focos_timespace_poligono.csv", index = False) # Série Histórica e Polígonos
focos_timespace_centroide.to_csv(f"{caminho_dados}focos_timespace_centroide.csv", index = False) # Série Histórica e Centróides
focos_timespace_se_poligono.to_csv(f"{caminho_dados}focos_timespace_se_poligono.csv", index = False) # Semanas Epidemiológicas e Polígonos
focos_timespace_se_centroide.to_csv(f"{caminho_dados}focos_timespace_se_centroide.csv", index = False) # Semanas Epidemiológicas e Centróides
"""
### Exibindo Informações
print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focosdive.info())
print("~"*80)
print(focosdive.dtypes)
print("~"*80)
print(focosdive)
print("="*80)

print("\n \n CIDADES DE SANTA CATARINA (IBGE) \n")
print(cidades.info())
print("~"*80)
print(cidades.dtypes)
print("~"*80)
print(cidades)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) SEMANAS EPIDEMIOLÓGICAS \n")
print(focossemana.info())
print("~"*80)
print(focossemana.dtypes)
print("~"*80)
print(focossemana)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (Lat/Lon) \n")
print("\n XY - Latitude e Longitude (IBGE)\n")
print(focos_timespace_xy.info())
print("~"*80)
print(focos_timespace_xy.dtypes)
print("~"*80)
print(focos_timespace_xy)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA - PRIMEIRO CONTATO/MUNICÍPIO (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (Lat/Lon) \n")
print("\n XY - Latitude e Longitude (IBGE)\n")
print(unicos_xy.info())
print("~"*80)
print(unicos_xy.dtypes)
print("~"*80)
print(unicos_xy)
print("="*80)
print(unicos_xy)
print(unicos_xy["Município"])
