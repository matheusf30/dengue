### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
#import folium
#from folium.plugins import HeatMapWithTime
##from IPython import display

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
focos = "focos_timespace_xy.csv"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focos = pd.read_csv(f"{caminho_dados}{focos}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Exibindo Informações
print("\n \n FOCOS DE _Aedes_spp. EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + Lat/Lon MUNICÍPIOS DE SANTA CATARINA (IBGE) \n")
print("\n XY - Latitude e Longitude \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)

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
mapa.view()

"""
