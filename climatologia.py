##IMPORTANDO BIBLIOTECAS##

import xarray as xr
from netCDF4 import Dataset                     # Read / Write NetCDF4 files
import matplotlib
import matplotlib.pyplot as plt                 #Figure
from matplotlib import cm                       # Colormap handling utilities
import matplotlib.colors as cls
import pandas as pd
import numpy as np
import cartopy, cartopy.crs as ccrs        # Plot maps
import cartopy.io.shapereader as shpreader # Import shapefiles
import cartopy.crs as crs
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature
import cmocean


## Abrir aquivo NETCDF MERGE (ds)
#
#### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _local == "CASA":
    caminho_dados = "/home/mfsouza90/Documents/git_matheusf30/dados_dengue/"
    caminho_dados = "/home/mfsouza90/Documents/git_matheusf30/dados_dengue/modelos/"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

# SAMeT / MERGE
caminho_samet = "/dados/operacao/samet/clima/TMED/"
caminho_merge = "/dados/operacao/merge/CDO.MERGE/"

# Renomeação de dados e variáveis
prec_sc = "prec_sc_2000_2022.nc"
samet_tmed = "SAMeT_CPTEC_DAILY_TMED_SB_2000_2023.nc"
merge = "MERGE_CPTEC_DAILY_SB_2000_2023.nc"
municipios_sc = "shapefiles/SC_Municipios_2022.shp"
br = "shapefiles/BR_UF_2022.shp"

# ABRE ARQUIVO NETCDF DATASET (ds)     {caminho}{dado}
prec_sc = xr.open_dataset(f'{caminho_dados}{prec_sc}')
temp = xr.open_dataset(f'{caminho_samet}{samet_tmed}')
#prec_sc = xr.open_dataset(f'{caminho_merge}{merge}')

##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}
""" CORES E MAPAS DE CORES
https://xkcd.com/color/rgb/
https://matplotlib.org/stable/gallery/color/named_colors.html
https://matplotlib.org/cmocean/
https://matplotlib.org/stable/users/explain/colors/colormaps.html
"""
################################################################################

########################### TESTANDO CLASSE ####################################

class Clima:

	def __init__(self, netcdf, var_str):
		"""
		Função de Instanciação do Objeto Classe
		"""
		print("\n" + "="*80 + "\n")
		print(f"\n{ansi['cyan']}>>>OBJETO CLIMATOLÓGICO INSTANCIADO<<<{ansi['reset']}")
		print("\n" + "="*80 + "\n")
		self.netcdf = netcdf
		self.lat = self.netcdf.variables["lat"][:]
		self.lon = self.netcdf.variables["lon"][:]
		self.lon = self.netcdf.variables["time"][:]
		self.lon = self.netcdf.variables["time"][:]
		print(f"\n\n{ansi['green']}Arquivo original:{ansi['reset']}\n{netcdf}\n")
		print("\n" + "="*80 + "\n")
		#VISUALIZAR dimensões do aquivo (Latitude, Longitude, Tempo e Variáveis)
		# LAT
		print(f"{ansi['cyan']}Latitudes:{ansi['reset']}\n{netcdf['lat']}\n")
		print("\n" + "="*80 + "\n")
		# LON
		print(f"{ansi['cyan']}Longitudes:{ansi['reset']}\n{netcdf['lon']}\n")
		print("\n" + "="*80 + "\n")
		# TIME
		print(f"{ansi['cyan']}Datas:{ansi['reset']}\n{netcdf['time']}\n")
		print("\n" + "="*80 + "\n")
		# Variável
		print(f"{ansi['cyan']}Variável:{ansi['reset']}\n{netcdf[var_str]}\n")
		print("\n" + "="*80 + "\n")

# SELECIONAR DATA
dia = "2023-06-21"
"""
plt.figure(figsize = (8, 8), layout = "constrained", frameon = False)
plt.title(f"Visualização do dia: {dia}")
temp.sel(time = f"{dia}")["tmed"].plot()
plt.show()
"""
"""
### Visualizando variável na data selecionada
plt.figure(figsize = (9, 10), layout = "constrained", frameon = False)
ax = plt.axes(projection=ccrs.PlateCarree())
br = list(shpreader.Reader(f"{caminho_dados}{br}").geometries())
municipios = list(shpreader.Reader(f"{caminho_dados}{municipios_sc}").geometries())
cmap = cmocean.cm.balance
#cmap = plt.get_cmap("coolwarm")
cmap.set_over("#3c0008") #  dark "maroon"
cmap.set_under("#00022e") # dark navy blue # "midnightblue"
#cmap.set_over('#000000') # black color
#cmap.set_under('#ffffff') # White color
data_min = temp["tmed"].min()
data_max = temp["tmed"].max()
interval = 1
levels = np.arange(data_min, data_max + interval, interval)
figura = temp.sel(time = f"{dia}")["tmed"].plot.pcolormesh(robust = True, cmap = cmap, add_colorbar = False,
															levels = levels, add_labels = False,
															norm = cls.Normalize(vmin = data_min, vmax = data_max))
plt.colorbar(figura, pad = 0.02, fraction = 0.05, extend = "both",
			ticks = np.linspace(int(data_min), int(data_max), 10), orientation = "vertical",
			label = "Temperatura Média Diária [C]")
ax.add_geometries(municipios, ccrs.PlateCarree(), edgecolor = "white",
					facecolor = "none", linewidth = 0.15)
ax.add_geometries(br, ccrs.PlateCarree(), edgecolor = "white",
					facecolor = "none", linewidth = 0.1)
ax.coastlines(resolution = "10m", color = "white", linewidth = 0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor = "white", linewidth = 0.8)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color = "white", alpha = 1.0,
                  linestyle='--', linewidth = 0.25, draw_labels = True,
                  xlocs = np.arange(-180, 180, 2),ylocs = np.arange(-90, 90, 2))
gl.top_labels = False
gl.right_labels = False
plt.title(f"Dia: {dia}", fontsize = 14, ha = "center")
#plt.savefig(f"{caminho_imagens}teste_samet1.jpg", transparent = True, dpi = 300, bbox_inches = "tight", pad_inches = 0.02)
plt.show()
"""
####################
temp = Clima(temp, "tmed")


"""
print('Arquivo original:', prec_sc, '\n')
print('***************************************\n')

#VISUALIZAR dimensões do aquivo (Latitude, Longitude, Tempo e Variáveis)

# LAT
print('Coordenadas em Latitude:', prec_sc["lat"], '\n')
print('***************************************\n')

# LON
print('Coordenadas em Longitude:', prec_sc["lon"], '\n')
print('***************************************\n')

# TIME
print('Datas:', prec_sc["time"], '\n')
print('***************************************\n')

# Variável
print('Variável:', prec_sc["prec"], '\n')
print('***************************************\n')

#  Plotar prec de um dia qualquer

dia = "2022-06-01"

prec_sc.sel(time = f'{dia}')["prec"].plot()
plt.show()
plt.figure(figsize = (10, 8))

# Use a projeção geoestacionária em cartopy (Use the Geostationary projection in cartopy)
ax = plt.axes(projection=ccrs.PlateCarree())

municipios = list(shpreader.Reader(f'{caminho_dados}{municipios_sc}').geometries())

cmap = cmocean.cm.balance
#cmap.set_over('#000000') # black color
#cmap.set_under('#ffffff') # White color

# Define de contour interval
data_min = prec_sc["prec"].min() + 1
data_max = prec_sc["prec"].max()
interval = 25
levels = np.arange(data_min, data_max + interval, interval)

# ESTA FUNÇÃO QUE DELIMITA VALORES norm=cls.Normalize(vmin=, vmax=),

figure = prec_sc.sel(time = f'{dia}')["prec"].plot.pcolormesh(robust = True,
                                                                norm = cls.Normalize(vmin = data_min,
                                                                                     vmax = data_max),
                                                                cmap = cmap, add_colorbar = False,
                                                                levels = levels, add_labels = False)
ax.add_geometries(municipios, ccrs.PlateCarree(),
                  edgecolor = 'white', facecolor = 'none',
                  linewidth = 0.15)

# Add  litoral, fronteiras e linhas de grade

ax.coastlines(resolution = '10m',
              color = 'white', linewidth = 0.8)
ax.add_feature(cartopy.feature.BORDERS,
               edgecolor = 'white', linewidth = 0.8)
gl = ax.gridlines(crs=ccrs.PlateCarree(),
                  color='white', alpha=1.0,
                  linestyle='--', linewidth=0.25,
                  xlocs=np.arange(-180, 180, 2),
                  ylocs=np.arange(-90, 90, 2), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
        
plt.colorbar(figure, pad = 0.02, fraction=0.05, extend='max',
             ticks = np.arange(data_min, data_max, 25),
             orientation='vertical', label='Daily Total of Precipitation [mm]')

plt.title(f'Precipitation time = {dia}',
          fontsize = 14, ha = 'center')

# Salva a figura no formato ".jpg" com dpi=300.

#plt.savefig(f"{caminho_imagens}teste_merge1.jpg",
#            transparent=True, dpi=300, bbox_inches="tight",
#            pad_inches=0.02)

plt.show()



plt.figure(figsize = (10, 8))


# Use a projeção geoestacionária em cartopy (Use the Geostationary projection in cartopy)
ax = plt.axes(projection = ccrs.PlateCarree())

shp= list(shpreader.Reader(f'{caminho_dados}{municipios_sc}').geometries())

# Create a custom color palette 
colors = ["#b4f0f0", "#96d2fa", "#78b9fa", "#3c95f5", "#1e6deb", "#1463d2", 
          "#0fa00f", "#28be28", "#50f050", "#72f06e", "#b3faaa", "#fff9aa", 
          "#ffe978", "#ffc13c", "#ffa200", "#ff6200", "#ff3300", "#ff1500", 
          "#c00100", "#a50200", "#870000", "#653b32"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#000000')
cmap.set_under('#ffffff')

# Define de contour interval
data_min = prec_sc["prec"].min() + 1
data_max = prec_sc["prec"].max()
interval = 25
levels = np.arange(data_min,data_max + interval,interval)

figure = prec_sc.sel(time=f'{dia}')["prec"].plot.pcolormesh(robust=True, norm=cls.Normalize(vmin=data_min, vmax=data_max),
        cmap=cmap,
        add_colorbar=False, levels=levels, add_labels=False)
ax.add_geometries(shp, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add  litoral, fronteiras e linhas de grade (coastlines, borders and gridlines)
ax.coastlines(resolution='10m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
        
plt.colorbar(figure, pad=0.05, fraction=0.05, extend='max', ticks=np.arange(data_min,data_max,25), orientation='vertical', label='Daily Total of Precipitation [mm]')

plt.title(f'Precipitation time={dia}',fontsize=14, ha='center')

# Salva a figura no formato ".jpg" com dpi=300.

#plt.savefig("teste_merge2.jpg", transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.02)

plt.show()
"""

