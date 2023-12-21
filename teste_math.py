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
# Encaminhamento ao Diretório "DADOS" e "IMAGENS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/imagens/"
caminho_samet = "/dados/operacao/samet/clima/TMED"
caminho_merge = "/dados/operacao/merge/CDO.MERGE"

# Renomeação de dados e variáveis
prec_sc = "prec_sc_2000_2022.nc"
samet_tmed = "SAMeT_CPTEC_DAILY_TMED_SB_2000_2022.nc"
merge = "MERGE_CPTEC_DAILY_SB_2000_2022.nc"
municipios_sc = "SC_Municipios_2022.shp"


# ABRE ARQUIVO NETCDF DATASET (ds)     {caminho}{dado}
prec_sc = xr.open_dataset(f'{caminho_dados}{prec_sc}')
#prec_sc = xr.open_dataset(f'{caminho_merge}{merge}')

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


