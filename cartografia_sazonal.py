### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.patches as mpatches
from matplotlib import cm
import matplotlib.colors as cls     
import cmocean
from datetime import timedelta
import numpy as np
import seaborn as sns
import statsmodels as sm
import pymannkendall as mk
import xarray as xr
### Suporte
import sys
import os
### Tratando avisos
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


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

### Definindo funções

def csv_melt(csv, str_var):
	media = csv.mean()
	media_linha = pd.DataFrame(media).T
	csv = pd.concat([csv, media_linha], ignore_index = True)
	csv.at[len(csv) - 1, "semana_epi"] = 0
	csv["semana_epi"] = csv["semana_epi"].astype(int) 	
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv}\n")
	csv_melt = pd.melt(csv, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{str_var}")
	csv_melt.sort_values(["semana_epi"], inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	return csv_melt

def cartografia_sazonal_entomoepidemio_total(csv_melt, str_var):
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	csv_melt = csv_melt.groupby("Município").mean()
	csv_melt.drop(columns = "semana_epi", inplace = True)
	csv_melt.reset_index(inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "right").fillna(0)
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = True,
								label = f"{str_var}", cmap = "YlOrRd")
	zero = csv_poligeo[csv_poligeo[f"{str_var}"] == 0]
	zero.plot(ax = ax, column = f"{str_var}", legend = False,
				label = f"{str_var}", color = "lightgray")
	ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro sazonal.""",
			color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
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
	if str_var == "casos":
		plt.title(f"Sazonalidade de Casos de Dengue em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	elif str_var == "focos":
		plt.title(f"Sazonalidade de Focos de _Aedes_sp. em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	plt.grid(True)
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se_total.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_meteoro_total(csv_melt, str_var):
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	csv_melt = csv_melt.groupby("Município").mean()
	csv_melt.drop(columns = "semana_epi", inplace = True)
	csv_melt.reset_index(inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "right").fillna(0)
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	if str_var == "prec":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = True,
							label = f"{str_var}", cmap = cmocean.cm.rain)
	elif str_var == "tmin" or "tmed" or "tmax":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = True,
							label = f"{str_var}", cmap = cmocean.cm.thermal)
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
	if str_var == "prec":
		plt.title(f"Sazonalidade de Precipitação (mm) em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	elif str_var == "tmin":
		plt.title(f"Sazonalidade de Temperatura Mínima (C) em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	elif str_var == "tmed":
		plt.title(f"Sazonalidade de Temperatura Média (C) em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	elif str_var == "tmax":
		plt.title(f"Sazonalidade de Temperatura Máxima (C) em Santa Catarina.\nMédias de Semanas Epidemiológicas.", fontsize = 18)
	plt.grid(True)
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se_total.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_entomoepidemio(csv, str_var, semana_epidemio = None):
	# SC_Coroplético
	#semana_epidemio = 20
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")	
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv}\n")
	csv_melt = pd.melt(csv, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{str_var}")
	csv_melt.sort_values(["semana_epi"], inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()} - csv_melt\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "left")
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()} - csv_poligeo\n{reset}{csv_poligeo}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	recorte_temporal = csv_poligeo[csv_poligeo["semana_epi"] == semana_epidemio]
	print(f"\n{green}RECORTE TEMPORAL DE {str_var.upper()}\n{reset}{recorte_temporal}\n")
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	if str_var == "casos":
		intervalo = 100
	elif str_var == "focos":
		intervalo = 20
	levels = np.arange(v_min, v_max + intervalo, intervalo)
	print(f"\n{green}v_min\n{reset}{v_min}\n")
	print(f"\n{green}v_max\n{reset}{v_max}\n")
	print(f"\n{green}levels\n{reset}{levels}\n")
	recorte_temporal.plot(ax = ax, column = f"{str_var}",  legend = True,
							label = f"{str_var}", cmap = "YlOrRd")#, add_colorbar = False,
												#levels = levels, add_labels = False,
												#norm = cls.Normalize(vmin = v_min, vmax = v_max))
	"""
	plt.colorbar(figura, pad = 0.02, fraction = 0.05, extend = "both",
			ticks = np.linspace(int(v_min), int(v_max), 10), orientation = "vertical",
			label = str_var)
	"""
	zeros = recorte_temporal[recorte_temporal[str_var] == 0]
	zeros.plot(ax = ax, legend = False, color = "lightgray")
	ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro sazonal.""",
			color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
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
	if str_var == "casos":
		plt.title(f"Sazonalidade de Casos de Dengue em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	elif str_var == "focos":
		plt.title(f"Sazonalidade de Focos de _Aedes_sp. em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	plt.grid(True)
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se{semana_epidemio}.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_meteoro(csv, str_var, semana_epidemio = None):
	# SC_Coroplético
	#semana_epidemio = 10
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv}\n")
	csv_melt = pd.melt(csv, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{str_var}")
	csv_melt.sort_values(["semana_epi"], inplace = True)
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "left")
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	if str_var == "prec":
		intervalo = 10
	elif str_var == "tmin" or "tmed" or "tmax":
		intervalo = 5
	levels = np.arange(v_min, v_max + intervalo, intervalo)
	print(f"\n{green}v_min\n{reset}{v_min}\n")
	print(f"\n{green}v_max\n{reset}{v_max}\n")
	print(f"\n{green}levels\n{reset}{levels}\n")
	if str_var == "prec":
		csv_poligeo[csv_poligeo["semana_epi"] == semana_epidemio].plot(ax = ax, column = f"{str_var}",  legend = True,
                                                                       label = f"{str_var}", cmap = cmocean.cm.rain)
	elif str_var == "tmin" or "tmed" or "tmax":
		csv_poligeo[csv_poligeo["semana_epi"] == semana_epidemio].plot(ax = ax, column = f"{str_var}",  legend = True,
                                                                       label = f"{str_var}", cmap = cmocean.cm.thermal)
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
	if str_var == "prec":
		plt.title(f"Sazonalidade de Precipitação (mm) em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	elif str_var == "tmin":
		plt.title(f"Sazonalidade de Temperatura Mínima (C) em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	elif str_var == "tmed":
		plt.title(f"Sazonalidade de Temperatura Média (C) em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	elif str_var == "tmax":
		plt.title(f"Sazonalidade de Temperatura Máxima (C) em Santa Catarina.\nSemana Epidemiológica: {semana_epidemio}.", fontsize = 18)
	plt.grid(True)
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se{semana_epidemio}.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_entomoepidemio_total_dissertacao(csv_melt, str_var):
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	csv_melt = csv_melt.groupby("Município").mean()
	csv_melt.drop(columns = "semana_epi", inplace = True)
	csv_melt.reset_index(inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "right").fillna(0)
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = False,
								label = f"{str_var}", cmap = "YlOrRd")
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = "YlOrRd")
	sm.set_array([])
	cbar = plt.colorbar(sm, ax = ax)	
	cbar.set_label(str_var, fontsize = 16)
	cbar.ax.tick_params(labelsize = 16)
	zero = csv_poligeo[csv_poligeo[f"{str_var}"] == 0]
	zero.plot(ax = ax, column = f"{str_var}", legend = False,
				label = f"{str_var}", color = "lightgray")
	ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro sazonal.""",
			color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
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
	ax.tick_params(labelsize = 16)
	plt.xlabel("Longitude", fontsize = 16)
	plt.ylabel("Latitude", fontsize = 16)
	plt.grid(True, linestyle = ":")
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se_total_dissertacao.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200, bbox_inches = None)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_meteoro_total_dissertacao(csv_melt, str_var):
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	csv_melt = csv_melt.groupby("Município").mean()
	csv_melt.drop(columns = "semana_epi", inplace = True)
	csv_melt.reset_index(inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "right").fillna(0)
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv_melt}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	if str_var == "prec":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = False,
							label = f"{str_var}", cmap = cmocean.cm.rain)
		sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = cmocean.cm.rain)
	elif str_var == "tmin" or "tmed" or "tmax":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = False,
							label = f"{str_var}", cmap = cmocean.cm.thermal)
		sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = cmocean.cm.thermal)
	sm.set_array([])
	cbar = plt.colorbar(sm, ax = ax)	
	cbar.set_label(str_var, fontsize = 16)
	cbar.ax.tick_params(labelsize = 16)
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
	ax.tick_params(labelsize = 16)
	plt.xlabel("Longitude", fontsize = 16)
	plt.ylabel("Latitude", fontsize = 16)
	plt.grid(True, linestyle = ":")
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se_total_dissertacao.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")


def cartografia_sazonal_pico_entomoepidemio(csv, str_var, semana_epidemio = None):
	# SC_Coroplético
	#semana_epidemio = 20
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")	
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv}\n")
	csv_melt = pd.melt(csv, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{str_var}")
	csv_melt.sort_values(["semana_epi"], inplace = True)
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()} - csv_melt\n{reset}{csv_melt}\n")
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "left")
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()} - csv_poligeo\n{reset}{csv_poligeo}\n")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	recorte_temporal = csv_poligeo[csv_poligeo["semana_epi"] == semana_epidemio]
	print(f"\n{green}RECORTE TEMPORAL DE {str_var.upper()}\n{reset}{recorte_temporal}\n")
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	if str_var == "casos":
		intervalo = 100
	elif str_var == "focos":
		intervalo = 20
	levels = np.arange(v_min, v_max + intervalo, intervalo)
	print(f"\n{green}v_min\n{reset}{v_min}\n")
	print(f"\n{green}v_max\n{reset}{v_max}\n")
	print(f"\n{green}levels\n{reset}{levels}\n")
	recorte_temporal.plot(ax = ax, column = f"{str_var}",  legend = False,
							label = f"{str_var}", cmap = "YlOrRd")
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = "YlOrRd")
	sm.set_array([])
	cbar = plt.colorbar(sm, ax = ax)	
	cbar.set_label(str_var, fontsize = 16)
	cbar.ax.tick_params(labelsize = 16)
	zeros = recorte_temporal[recorte_temporal[str_var] == 0]
	zeros.plot(ax = ax, legend = False, color = "lightgray")
	ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro sazonal.""",
			color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
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
	ax.tick_params(labelsize = 16)
	plt.xlabel("Longitude", fontsize = 16)
	plt.ylabel("Latitude", fontsize = 16)
	plt.grid(True, linestyle = ":")
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se{semana_epidemio}_dissertacao.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")

def cartografia_sazonal_pico_meteoro(csv, str_var, semana_epidemio = None):
	# SC_Coroplético
	#semana_epidemio = 10
	xy = municipios.copy()
	xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
	xy = xy.rename(columns = {"NM_MUN" : "Município"})
	xy["Município"] = xy["Município"].str.upper()
	print(f"\n{green}xy\n\n{reset}{xy}")
	print(f"\n{green}SAZONALIDADE DE {str_var.upper()}\n{reset}{csv}\n")
	csv_melt = pd.melt(csv, id_vars = ["semana_epi"], 
		                    var_name = "Município", value_name = f"{str_var}")
	csv_melt.sort_values(["semana_epi"], inplace = True)
	#sys.exit()
	csv_poli = pd.merge(csv_melt, xy, on = "Município", how = "left")
	csv_poligeo = gpd.GeoDataFrame(csv_poli, geometry = "geometry", crs = "EPSG:4674")
	fig, ax = plt.subplots(figsize = (18, 12), layout = "constrained", frameon = False)
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
	v_max = csv_melt[str_var].max()
	v_min = csv_melt[str_var].min()
	if str_var == "prec":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = False,
							label = f"{str_var}", cmap = cmocean.cm.rain)
		sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = cmocean.cm.rain)
	elif str_var == "tmin" or "tmed" or "tmax":
		csv_poligeo.plot(ax = ax, column = f"{str_var}",  legend = False,
							label = f"{str_var}", cmap = cmocean.cm.thermal)
		sm = plt.cm.ScalarMappable(norm = plt.Normalize(vmin = v_min,
													vmax = v_max), cmap = cmocean.cm.thermal)
	sm.set_array([])
	cbar = plt.colorbar(sm, ax = ax)	
	cbar.set_label(str_var, fontsize = 16)
	cbar.ax.tick_params(labelsize = 16)
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
	ax.tick_params(labelsize = 16)
	plt.xlabel("Longitude", fontsize = 16)
	plt.ylabel("Latitude", fontsize = 16)
	plt.grid(True, linestyle = ":")
	nome_arquivo = f"{str_var}_mapa_coropletico_sazonal_se{semana_epidemio}_dissertacao.png"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/sazonalidade/"
	if _AUTOMATIZA == True and _SALVAR == True:
		os.makedirs(caminho_resultados, exist_ok = True)
		plt.savefig(f"{caminho_resultados}{nome_arquivo}", format = "png", dpi = 1200)
		print(f"\n\n{green}{caminho_resultados}\n{nome_arquivo}\nSALVO COM SUCESSO!{reset}\n\n")
	if _AUTOMATIZA == True and _VISUALIZAR == True:	
		print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")
		plt.show()
		print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\n{nome_arquivo}\n{reset}\n\n")


##########################################################################################################
# Sazonalidade Média Total
"""
casos_melt = csv_melt(casos, "casos")
cartografia_sazonal_entomoepidemio_total_dissertacao(casos_melt, "casos")

focos_melt = csv_melt(focos, "focos")
cartografia_sazonal_entomoepidemio_total_dissertacao(focos_melt, "focos")

prec_melt = csv_melt(prec, "prec")
cartografia_sazonal_meteoro_total_dissertacao(prec_melt, "prec")

tmin_melt = csv_melt(tmin, "tmin")
cartografia_sazonal_meteoro_total_dissertacao(tmin_melt, "tmin")

tmed_melt = csv_melt(tmed, "tmed")
cartografia_sazonal_meteoro_total_dissertacao(tmed_melt, "tmed")

tmax_melt = csv_melt(tmax, "tmax")
cartografia_sazonal_meteoro_total_dissertacao(tmax_melt, "tmax")


casos_melt = csv_melt(casos, "casos")
cartografia_sazonal_entomoepidemio_total(casos_melt, "casos")

focos_melt = csv_melt(focos, "focos")
cartografia_sazonal_entomoepidemio_total(focos_melt, "focos")

prec_melt = csv_melt(prec, "prec")
cartografia_sazonal_meteoro_total(prec_melt, "prec")

tmin_melt = csv_melt(tmin, "tmin")
cartografia_sazonal_meteoro_total(tmin_melt, "tmin")

tmed_melt = csv_melt(tmed, "tmed")
cartografia_sazonal_meteoro_total(tmed_melt, "tmed")

tmax_melt = csv_melt(tmax, "tmax")
cartografia_sazonal_meteoro_total(tmax_melt, "tmax")

# Sazonalidade por Semana Epidemiológica
"""
"""
for semana_epidemio in csv_melt["semana_epi"].unique():
	print(semana_epidemio)
"""
"""
for semana_epidemio in range(1,12):
	print(f"\n{green}SEMANA EPIDEMIOLÓGICA: {semana_epidemio}{reset}\n")
	cartografia_sazonal_entomoepidemio(casos, "casos", semana_epidemio)
	cartografia_sazonal_entomoepidemio(focos, "focos", semana_epidemio)
	cartografia_sazonal_meteoro(prec, "prec", semana_epidemio)
	cartografia_sazonal_meteoro(tmin, "tmin", semana_epidemio)
	cartografia_sazonal_meteoro(tmed, "tmed", semana_epidemio)
	cartografia_sazonal_meteoro(tmax, "tmax", semana_epidemio)
"""
for semana_epidemio in range(12,24):
	print(f"\n{green}SEMANA EPIDEMIOLÓGICA: {semana_epidemio}{reset}\n")
	cartografia_sazonal_pico_entomoepidemio(casos, "casos", semana_epidemio)
	cartografia_sazonal_pico_entomoepidemio(focos, "focos", semana_epidemio)
	cartografia_sazonal_pico_meteoro(prec, "prec", semana_epidemio)
	cartografia_sazonal_pico_meteoro(tmin, "tmin", semana_epidemio)
	cartografia_sazonal_pico_meteoro(tmed, "tmed", semana_epidemio)
	cartografia_sazonal_pico_meteoro(tmax, "tmax", semana_epidemio)

#for semana_epidemio in range(1,12):
for semana_epidemio in range(24,54):
	print(f"\n{green}SEMANA EPIDEMIOLÓGICA: {semana_epidemio}{reset}\n")
	cartografia_sazonal_entomoepidemio(casos, "casos", semana_epidemio)
	cartografia_sazonal_entomoepidemio(focos, "focos", semana_epidemio)
	cartografia_sazonal_meteoro(prec, "prec", semana_epidemio)
	cartografia_sazonal_meteoro(tmin, "tmin", semana_epidemio)
	cartografia_sazonal_meteoro(tmed, "tmed", semana_epidemio)
	cartografia_sazonal_meteoro(tmax, "tmax", semana_epidemio)
