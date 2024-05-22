### Bibliotecas Correlatas
# Básicas e Gráficas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
#import datetime
# Suporte
import os
import sys
import joblib
import webbrowser
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category = ShapelyDeprecationWarning)
# Mapas
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.patches as mpatches


### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
    caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos # TENTAR GFS

municipios = "SC_Municipios_2022.shp" # Shapefile não está carregando do GH
br = "BR_UF_2022.shp"
rs = "RS_Mesorregioes_2022.shp"


###############################################################

### Abrindo Arquivo

municipios = gpd.read_file(f"{caminho_dados}{municipios}")
br = gpd.read_file(f"{caminho_dados}{br}")
rs = gpd.read_file(f"{caminho_dados}{rs}")
print(rs)
print(rs.columns)
print(rs["NM_MESO"])
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
rs = rs[(rs["NM_MESO"] != "Lagoa Mirim") & (rs["NM_MESO"] != "Lagoa dos Patos")]
rs.plot(ax = ax)#, color = "lightgreen")
plt.show()


sys.exit()

### Cartografia
# Semana Epidemiológica
semana_epidemio = "2023-04-16"
# "2020-04-19" "2021-04-18" "2022-04-17" "2023-04-16"
#"2023-12-03" #"2023-12-17"error #"2023-12-24"error #"2023-04-16" #"2022-04-17"
#plt.rcParams["text.usetex"] = True
#Aedes = r"\textit{Aedes}"

# SC_Pontos
previsao_melt_geo = gpd.GeoDataFrame(previsao_melt_geo)#, geometry = municipios.geometry)
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(-48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
municipios.plot(ax = ax, color = "lightgreen", edgecolor = "black")
previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio ].plot(ax = ax, column = "Focos",  legend = True,
                                                                        label = "Focos", cmap = "YlOrRd", markersize = 50)
zero = previsao_melt_geo[previsao_melt_geo["Focos"] == 0]
zero[zero["Semana"] == semana_epidemio].plot(ax = ax, column = "Focos", legend = False,
                                             label = "Focos", cmap = "YlOrBr")
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Focos de _Aedes_ sp. Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.",
          fontsize = 18)
plt.grid(True)
plt.savefig(f"{caminho_resultados}FOCOS_mapa_pontual_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
print(f"\n\n{green}{caminho_resultados}\nFOCOS_mapa_pontual_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
#plt.show()

# SC_MapaCalor
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(-48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
sns.kdeplot(data = previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio],
            x = "longitude", y = "latitude", legend = True, ax = plt.gca(), weights = "Focos",
            fill = True, cmap = "YlOrRd", levels = previsao_melt_geo["Focos"].max(), alpha = 0.5)
municipios.plot(ax = plt.gca(), color = "lightgreen", edgecolor = "black", alpha = 0.3)
cbar = plt.cm.ScalarMappable(cmap="YlOrRd")
cbar.set_array(previsao_melt_geo["Focos"])
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
plt.colorbar(cbar, ax = plt.gca(), label="Focos")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Mapa de Densidade de Kernel dos Focos de _Aedes_sp. Previstos.\n Santa Catarina, Semana Epidemiológica: {semana_epidemio}.", fontsize = 18)
plt.grid(True)
plt.savefig(f"{caminho_resultados}FOCOS_mapa_densidade_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
print(f"\n\n{green}{caminho_resultados}\nFOCOS_mapa_densidade_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
#plt.show()

# SC_Coroplético
xy = municipios.copy()
xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
xy = xy.rename(columns = {"NM_MUN" : "Município"})
xy["Município"] = xy["Município"].str.upper()
previsao_melt_poli = pd.merge(previsao_melt, xy, on = "Município", how = "left")
previsao_melt_geo = gpd.GeoDataFrame(previsao_melt_poli, geometry = "geometry", crs = "EPSG:4674")
fig, ax = plt.subplots(figsize = (19, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(-48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
municipios.plot(ax = ax, color = "lightgray", edgecolor = "lightgray")#edgecolor = "whitesmoke", hatch = "--")
previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio].plot(ax = ax, column = "Focos", legend = True,
                                                                       label = "Focos", cmap = "YlOrRd")
zero = previsao_melt_geo[previsao_melt_geo["Focos"] == 0]
zero[zero["Semana"] == semana_epidemio].plot(ax = ax, column = "Focos", legend = False,# hatch = "O.", edgecolor = "lightgray",
                                             label = "Focos", cmap = "YlOrBr")
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
ax.text(-52.5, -28.5, """LEGENDA

≣           Sem registro*

*Não há registro oficial ou
modelagem inexistente.""",
        color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Focos de _Aedes_sp. Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.", fontsize = 18)
plt.grid(True)
plt.savefig(f"{caminho_resultados}FOCOS_mapa_coropletico_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
print(f"\n\n{green}{caminho_resultados}\nFOCOS_mapa_coropletico_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
#plt.show()

"""
https://geopandas.org/en/stable/docs/user_guide/mapping.html
https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html
https://coolsymbol.com/
https://matplotlib.org/stable/gallery/color/named_colors.html
https://matplotlib.org/stable/gallery/color/colormap_reference.html
"""


