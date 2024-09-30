### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.patches as mpatches
from datetime import timedelta
import numpy as np
import seaborn as sns
import statsmodels as sm
import pymannkendall as mk
import xarray as xr
### Suporte
import sys
import os

### Condições para Variar #######################################################

_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"

##################### Valores Booleanos ############ # sys.argv[0] is the script name itself and can be ignored!
_AUTOMATIZAR = sys.argv[1]   # True|False                    #####
_AUTOMATIZA = True if _AUTOMATIZAR == "True" else False      #####
_VISUALIZAR = sys.argv[2]    # True|False                    #####
_VISUALIZAR = True if _VISUALIZAR == "True" else False       #####
_SALVAR = sys.argv[3]        # True|False                    #####
_SALVAR = True if _SALVAR == "True" else False               #####
##################################################################

##### Padrão ANSI ###############################################################
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"
#################################################################################

### Encaminhamento aos Diretórios
if _LOCAL == "GH": # _ = Variável Privada
	caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
	caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "CASA":
	caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
	caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _LOCAL == "IFSC":
	caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
	caminho_shp = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
	caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/"
	caminho_cartografia = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
	print(f"\n{red}CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!{reset}")
print(f"\n{green}OS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n{reset}\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos
casos = "sazonalidade_semanal_casos.csv"
focos = "sazonalidade_semanal_focos.csv"
prec = "sazonalidade_semanal_prec.csv"
tmin = "sazonalidade_semanal_tmin.csv"
tmed = "sazonalidade_semanal_tmed.csv"
tmax = "sazonalidade_semanal_tmax.csv"
municipios = "SC_Municipios_2022.shp"
br = "BR_UF_2022.shp"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
municipios = gpd.read_file(f"{caminho_shp}{municipios}")
br = gpd.read_file(f"{caminho_shp}{br}")

print(f"\n{green}SAZONALIDADE DE CASOS\n{reset}{casos}\n")
print(f"\n{green}SAZONALIDADE DE FOCOS\n{reset}{focos}\n")
print(f"\n{green}SAZONALIDADE DE PRECIPITAÇÃO\n{reset}{prec}\n")
print(f"\n{green}SAZONALIDADE DE TEMPERATURA MÍNIMA\n{reset}{tmin}\n")
print(f"\n{green}SAZONALIDADE DE TEMPERATURA MÉDIA\n{reset}{tmed}\n")
print(f"\n{green}SAZONALIDADE DE TEMPERATURA MÁXIMA\n{reset}{tmax}\n")
print(f"\n{green}GEODATAFRAME MUNICÍPIOS CATARINENSES\n{reset}{municipios}\n")
print(f"\n{green}GEODATAFRAME ESTADOS BRASILEIROS\n{reset}{br}\n")

############### Base para Troca de Caracteres
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
		'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
		'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
		'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
		'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
		'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}

### Laço de Arquivos
lista_arquivos = [casos, focos, prec, tmin, tmed, tmax]
variaveis = ["casos", "focos", "prec", "tmin", "tmed", "tmax"]
for idx, arquivo in enumerate(lista_arquivos):
	var = variaveis[idx]
	var_melt = pd.melt(focos, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{var}")
	print(f"\n{green}SAZONALIDADE DE {var.upper()}\n{reset}{var_melt}\n")

#######
# SC_Coroplético

xy = municipios.copy()
xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
xy = xy.rename(columns = {"NM_MUN" : "Município"})
xy["Município"] = xy["Município"].str.upper()
print(f"\n{green}xy\n\n{reset}{xy}")
#sys.exit()
var_poli = pd.merge(var_melt, xy, on = "Município", how = "left")
var_poligeo = gpd.GeoDataFrame(var_poli, geometry = "geometry", crs = "EPSG:4674")
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
municipios.plot(ax = ax, color = "lightgray", edgecolor = "lightgray")
previsao_melt_poligeo[previsao_melt_poligeo["Semana"] == semana_epidemio].plot(ax = ax, column = "Casos",  legend = True,
                                                                               label = "Casos", cmap = "YlOrRd")
zero = previsao_melt_poligeo[previsao_melt_poligeo["Casos"] == 0]
zero[zero["Semana"] == semana_epidemio].plot(ax = ax, column = "Casos", legend = False,
                                             label = "Casos", cmap = "YlOrBr")
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
ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro oficial ou
modelagem inexistente.""",
        color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Casos de Dengue Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.", fontsize = 18)
plt.grid(True)
if _AUTOMATIZA == True and _SALVAR == True:
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/coropletico/"
	os.makedirs(caminho_resultados, exist_ok = True)
	plt.savefig(f"{caminho_resultados}CASOS_mapa_coropletico_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
	print(f"\n\n{green}{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
if _AUTOMATIZA == True and _VISUALIZAR == True:	
	print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\n{reset}\n\n")
	plt.show()
	print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\n{reset}\n\n")


