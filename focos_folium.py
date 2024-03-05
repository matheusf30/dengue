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
### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

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
for semana in focos["Semana"]:
    for municipio in focos["Município"]:
        coordenadas = []
        for _, linha in focos.iterrows():     # _, indica que estamos ignorando o index durante a iteração
            coordenadas.extend([[linha["latitude"], linha["longitude"]]] * linha["Focos"])
        dados_heatmap.append((focos["Semana"], coordenadas))


### Instanciando Mapa e HeatMapWithTime
mapa = folium.Map(location = [focos["latitude"].mean(), focos["longitude"].mean()],
                  tiles = "cartodbdark_matter", zoom_start=8)
HeatMapWithTime(dados_heatmap, auto_play = True, #index = focos["Semana"],
                speed_step = 0.2).add_to(mapa)
mapa
mapa.save(f"{caminho_dados}focos_timespace.html")
mapa.show_in_browser()
#mapa.view()

print(dados_heatmap)
"""
fig = px.density_mapbox(focos, z = "Focos", radius = 10,
                        lat = "latitude", lon ="longitude",
                        animation_frame = "Semana", zoom = 8,
                        center = dict(lat = focos["latitude"].mean(),
                                      lon = focos["longitude"].mean()),
                        mapbox_style = "carto-positron",
                        title = "Focos de _Aedes_ spp. ao longo do tempo.")
fig.show()
"""           
