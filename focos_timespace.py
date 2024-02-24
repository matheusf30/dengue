### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
#import folium
#from folium.plugins import HeatMapWithTime
##from IPython import display

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
focosdive = "focos_dive_total.csv"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focosdive = pd.read_csv(f"{caminho_dados}{focosdive}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Limpeza e Tratamento de Dados
## TEMPO
focosdive = focosdive[["Regional", "Município", "Imóvel", "Depósito", "Data da Coleta"]]
# HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER...
trocanome = {
"HERVAL D`OESTE": "HERVAL D'OESTE",
"PRESIDENTE CASTELO BRANCO" : "PRESIDENTE CASTELLO BRANCO",
"SÃO CRISTOVÃO DO SUL" : "SÃO CRISTÓVÃO DO SUL",
"GRÃO PARÁ" : "GRÃO-PARÁ",
"LAURO MULLER" : "LAURO MÜLLER"
}
focosdive["Município"] = focosdive["Município"].replace(trocanome)
focosdive["Focos"] = np.ones(251014).astype(int)
focosdive["Data"] = focosdive["Data da Coleta"].copy()
focosdive["Data"] = pd.to_datetime(focosdive["Data"])
focossemana = focosdive.copy()
focossemana["Semana"] = focossemana["Data"].dt.to_period("W-SAT").dt.to_timestamp()
focossemana = focossemana.groupby(["Semana", "Município"]).sum(numeric_only = True)["Focos"]
focossemana = focossemana.reset_index()
focossemana.to_csv(f"{caminho_dados}focos_se_dive.csv", index = False)
## ESPAÇO
### Unindo Dataframe e Geodataframe
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
"""
pontos = cidades.copy()
crs = {"proj" : "latlong",
       "ellps" : "WGS84",
       "datum" : "WGS84",
       "no_defs" : True}
pontos = gpd.GeoDataFrame(pontos, crs = crs, geometry = )
"""
pontos = cidades.copy()
pontos["ponto"] = cidades["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
focos_timespace_poligono = pd.merge(focosdive, cidades, on = "Município", how = "left") # Data de Coleta e Polígonos
focos_timespace_centroide = pd.merge(focosdive, pontos, on = "Município", how = "left") # Data da Coleta e Centróides
focos_timespace_se_poligono = pd.merge(focossemana, cidades, on = "Município", how = "left") # Semanas Epidemiológicas e Polígonos
focos_timespace_se_centroide = pd.merge(focossemana, pontos, on = "Município", how = "left")# Semanas Epidemiológicas e Centróides
focos_timespace_poligono = focos_timespace_poligono.drop(columns = ["NM_MUN"])
focos_timespace_centroide = focos_timespace_centroide.drop(columns = ["NM_MUN"])
focos_timespace_se_poligono = focos_timespace_se_poligono.drop(columns = ["NM_MUN"])
focos_timespace_se_centroide = focos_timespace_se_centroide.drop(columns = ["NM_MUN"])
xy = pontos.copy()
xy["latitude"] = cidades["geometry"].centroid.y
xy["longitude"] = cidades["geometry"].centroid.x
focos_timespace_xy = pd.merge(focossemana, xy, on = "Município", how = "left")
focos_timespace_xy = focos_timespace_xy.drop(columns = ["NM_MUN", "ponto"])
"""
### Salvando Arquivos
focos_timespace_poligono.to_csv(f"{caminho_dados}focos_timespace_poligono.csv", index = False) # Série Histórica e Polígonos
focos_timespace_centroide.to_csv(f"{caminho_dados}focos_timespace_centroide.csv", index = False) # Série Histórica e Centróides
focos_timespace_se_poligono.to_csv(f"{caminho_dados}focos_timespace_se_poligono.csv", index = False) # Semanas Epidemiológicas e Polígonos
focos_timespace_se_centroide.to_csv(f"{caminho_dados}focos_timespace_se_centroide.csv", index = False) # Semanas Epidemiológicas e Centróides
"""
focos_timespace_xy.to_csv(f"{caminho_dados}focos_timespace_xy.csv", index = False) # Semanas Epidemiológicas, Latitudes e Longitudes

### Exibindo Informações
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

print("\n \n CIDADES DE SANTA CATARINA (IBGE) \n")
print(cidades.info())
print("~"*80)
print(cidades.dtypes)
print("~"*80)
print(cidades)
print("="*80)


print("\n \n MUNICÍPIOS DE SANTA CATARINA (IBGE- centróide) \n")
print(pontos.info())
print("~"*80)
print(pontos.dtypes)
print("~"*80)
print(pontos)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) SEMANAS EPIDEMIOLÓGICAS \n")
print(focossemana.info())
print("~"*80)
print(focossemana.dtypes)
print("~"*80)
print(focossemana)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE - POLÍGONOS E MULTIPOLÍGONOS) \n")
print(focos_timespace_poligono.info())
print("~"*80)
print(focos_timespace_poligono.dtypes)
print("~"*80)
print(focos_timespace_poligono)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE - CENTRÓIDES) \n")
print(focos_timespace_centroide.info())
print("~"*80)
print(focos_timespace_centroide.dtypes)
print("~"*80)
print(focos_timespace_centroide)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE - POLÍGONOS E MULTIPOLÍGONOS) \n")
print(focos_timespace_se_poligono.info())
print("~"*80)
print(focos_timespace_se_poligono.dtypes)
print("~"*80)
print(focos_timespace_se_poligono)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE - CENTRÓIDES) \n")
print(focos_timespace_se_centroide.info())
print("~"*80)
print(focos_timespace_se_centroide.dtypes)
print("~"*80)
print(focos_timespace_se_centroide)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (Lat/Lon) \n")
print("\n XY - Latitude e Longitude \n")
print(focos_timespace_xy.info())
print("~"*80)
print(focos_timespace_xy.dtypes)
print("~"*80)
print(focos_timespace_xy)
print("="*80)

"""
rows_with_nan = focos_timespace[focos_timespace.isna().any(axis=1)]
# Display rows with NaN values
print(rows_with_nan)
# HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER... 

#focos_timespace.to_csv(f"{caminho_dados}focos_timespace.csv", index = False) # Data de Coleta
#focos_timespace.to_csv(f"{caminho_dados}focos_se_timespace.csv", index = False) # Semanas Epidemiológicas
#focos_timespace.to_file(f"{caminho_dados}focos_timespace.shp") 
"""
municipios.plot()
plt.show()

"""
### Convertendo e Incluindo Tipagens de Variáveis
# Datetime64[ns]
focos_timespace["Semana"] = pd.to_datetime(focos_timespace["Semana"])
focos_timespace = focos_timespace.sort_values(by = ["Semana"])
# Geometry
focos_timespace = gpd.GeoDataFrame(focos_timespace.poinst_from_xy(focos_timespace["longitude"], focos_timespace["latitude"]))

focos_timespace = focos_timespace.drop(columns = ["ponto", "geometry"])
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
focos_timespace_poligono = pd.merge(focos_timespace, cidades, on = "Município", how = "left")
focos_timespace_poligono = focos_timespace_poligono.drop(columns = ["NM_MUN"])
focos_timespace_poligono.to_csv(f"{caminho_dados}focos_timespace_poligono.csv") 
pontos = cidades.copy()
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
focos_timespace_centroide = pd.merge(focos_timespace, pontos, on = "Município", how = "left")
focos_timespace_centroide = focos_timespace_centroide.drop(columns = ["NM_MUN"])
focos_timespace_centroide.to_csv(f"{caminho_dados}focos_timespace_centroide.csv") 

crs = {"proj" : "latlong",
       "ellps" : "WGS84",
       "datum" : "WGS84",
       "no_defs" : True}
crs = crs,

# Filter out rows with MULTIPOLYGON geometries
focos_timespace_centroide = focos_timespace_centroide[focos_timespace_centroide["ponto"].geom_type == 'POINT']
#focos_timespace_poligono = focos_timespace_poligono[focos_timespace_poligono["geometry"].geom_type == 'POLYGON']
# Now try creating a GeoDataFrame again
focos_timespace_centroide = gpd.GeodataFrame(focos_timespace_centroide)
#focos_timespace_poligono = gpd.GeoDataFrame(focos_timespace_poligono)
#focos_timespace = gpd.GeoDataFrame(focos_timespace, geometry = "geometry")

mapa = folium.Map([-27.50, -50.00], tiles="cartodbdark_matter", zoom_start=8)
HeatMapWithTime(focos_timespace, auto_play = True, index = focos_timespace["Semana"], speed_step=0.2).add_to(mapa)
mapa
mapa.save(f"{caminho_dados}focos_timespace.html")
mapa.show_in_browser()

### Exibindo Informações
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA EM SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS_xy_LATLON (IBGE) ")
print(focos_timespace.info())
print("~"*80)
print(focos_timespace.dtypes)
print("~"*80)
print(focos_timespace)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE) \n")
print("\n POLÍGONO \n")
print(focos_timespace_poligono.info())
print("~"*80)
print(focos_timespace_poligono.dtypes)
print("~"*80)
print(focos_timespace_poligono)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print("\n CENTRÓIDE \n")
print(focos_timespace_centroide.info())
print("~"*80)
print(focos_timespace_centroide.dtypes)
print("~"*80)
print(focos_timespace_centroide)
print("="*80)
"""
