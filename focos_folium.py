### Bibliotecas Correlatas
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
"""
import plotly
import plotly.express as px
import multiprocessing
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from IPython import display
"""
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
focos = "focos_timespace_xy.csv"
#municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focos = pd.read_csv(f"{caminho_dados}{focos}")
#municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Exibindo Informações
print("\n \n FOCOS DE _Aedes_spp. EM SANTA CATARINA - SÉRIE HISTÓRICA - SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + Lat/Lon MUNICÍPIOS DE SANTA CATARINA (IBGE) \n")
print("\n XY - Latitude e Longitude \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)

### Pré-Processamneto
# dados_heatmap para HeatMapWithTime
# Necessário uma tupla com (tempo, [coordenadas])
"""
def heat_map(dataframe):
    coordenadas = []
    for _, linha in focos.iterrows():     # _, indica que estamos ignorando o index durante a iteração
        coordenadas.extend([[linha['latitude'], linha['longitude']]] * linha['Focos'])
    return  coordenadas

dados_heatmap = []
with multiprocessing.Pool() as pool:
    resultado = pool.starmap(focos["Semana"], heat_map(focos))        
    dados_heatmap.extend(resultado)
"""
dados_heatmap = []
agrupado = focos.groupby(['Semana', 'Município']).agg({'Focos': 'sum', 'latitude': 'first', 'longitude': 'first'}).reset_index()
for semana,sub_agrupado in agrupado.groupby("Semana"):
    coordenadas = []
    for _, linha in sub_agrupado.iterrows():     # _, indica que estamos ignorando o index durante a iteração
        coordenadas.extend([[linha["latitude"], linha["longitude"]]] * linha["Focos"])
    dados_heatmap.append(coordenadas)

print(dados_heatmap)

### Instanciando Mapa e HeatMapWithTime
mapa = folium.Map(location = [focos["latitude"].mean(), focos["longitude"].mean()],
                  tiles = "cartodbdark_matter", zoom_start=8)
HeatMapWithTime(dados_heatmap, auto_play = True, speed_step = 0.2, #index = focos["Semana"],
                gradient = {0.1: "blue", 0.2: "lime",
                            0.4: "yellow", 0.6: "orange",
                            0.8: "red", 0.99: "purple"},
                min_opacity = 0.5, max_opacity = 0.8, use_local_extrema = False,
                index = agrupado["Semana"].unique()).add_to(mapa)
mapa.save(f"{caminho_dados}focos_timespace.html")
mapa.show_in_browser()
"""
https://github.com/python-visualization/folium/blob/main/folium/plugins/heat_map_withtime.py

fig = px.density_mapbox(focos, z = "Focos", radius = 10,
                        lat = "latitude", lon ="longitude",
                        animation_frame = "Semana", zoom = 8,
                        center = dict(lat = focos["latitude"].mean(),
                                      lon = focos["longitude"].mean()),
                        mapbox_style = "carto-positron",
                        title = "Focos de _Aedes_ spp. ao longo do tempo.")
fig.show()

mapa = folium.Map(location = [focos["latitude"].mean(), focos["longitude"].mean()],
                  tiles = "cartodbdark_matter", zoom_start=8)
HeatMapWithTime(index = focos["Semana"], data = [focos["latitude"], focos["longitude"], focos["Focos"]],
                              auto_play = True, speed_step = 0.2, #index = focos["Semana"],
                gradient = {0.1: "blue", 0.2: "lime",
                            0.4: "yellow", 0.6: "orange",
                            0.8: "red", 0.99: "purple"},
                min_opacity = 0.5, max_opacity = 0.8, use_local_extrema = False).add_to(mapa)
mapa.save(f"{caminho_dados}focos_timespace.html")
mapa.show_in_browser()
"""           
