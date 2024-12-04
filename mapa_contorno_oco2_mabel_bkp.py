#!/usr/bin/env python
# coding: utf-8

# # IFSC - TÓPE1 - DADOS Temperatura Média SAMET - MAPAS
# # AUTORA: .................. - Meteorologista - MSc.
# # DATA: 11/07/2024
# # COMO RODAR: executar o arquivo python SAMeT_CPTEC_MONTHLY_AVG_xco2_2024.nc e colocar em seguida inserir ano-mês
# #  Ex.:
# #  python xco2_mensal_samet.py 2024-05
# #
## IMPORTANDO BIBLIOTECAS ##
import xarray as xr
from netCDF4 import Dataset                     # Read / Write NetCDF4 files
import matplotlib
import matplotlib.pyplot as plt                 #Figure
from matplotlib import cm                       # Colormap handling utilities
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as cls
import pandas as pd
import numpy as np
import cartopy, cartopy.crs as ccrs        # Plot maps
import cartopy.io.shapereader as shpreader # Import shapefiles
import cartopy.crs as crs
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature
import cmocean
#from scipy import interpolate
#
import sys


#print 'Argument 1 -> ', argv[1:]
print(sys.argv[1])
data=sys.argv[1] 

print('Data:', data, '\n')
#sys.exit()

# ABRE ARQUIVO NETCDF DATASET (ds)
#ds = xr.open_dataset('/dados/pesquisa/mabelsimm/oco2_GEOS_L3CO2/serie_2015_2022_oco2.nc')
ds = xr.open_dataset('/dados/pesquisa/mabelsimm/oco2_GEOS_L3CO2/teste.nc')

print('Arquivo original:', ds, '\n')
print('***************************************\n')

# VISUALIZAR dimensões do aquivo (Latitude, Longitude e Time)
print('Coordenadas em Latitude:', ds.lat, '\n')
print('***************************************\n')
print('Coordenadas em Longitude:', ds.lon, '\n')
print('***************************************\n')
print('Datas:', ds.time, '\n')
print('***************************************\n')

# Variável de interesse
print('Data variable:', ds.XCO2, '\n')
print('***************************************\n')

# Definir a extensão da região Sul do Brasil
#lat_min = -36.95
#lat_max = -19.05
#lon_min = -62.95
#lon_max = -45.05

# Definir a extensão da região de Santa Catarina
lat_min = -30.00
lat_max = -25.00
lon_min = -55.00
lon_max = -47.50

# Definir data (ano-mês)
# sidata = "2024-06"
#data=sys.argv[1] # sidata = "2024-06"
# Explodir a variável em ano e mês
ano, mes = data.split('-')

print(f'Ano: {ano}')
print(f'Mês: {mes}')

# Selecionar os dados de temperatura para a região e o tempo específico

data_region = ds.sel(time = f'{data}', lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max)).XCO2.squeeze()

# Encontrar o valor máximo da temperatura na região selecionada
max_xco2 = data_region.max().item()
#int_max = int(max_xco2)
int_max = round(max_xco2, 2)
print(f'Valor máximo do Fluxo CO2 na região selecionada: {int_max} , {max_xco2} ppm')

# Encontrar o valor mínimo da temperatura na região selecionada
min_xco2 = data_region.min().item()
#int_min = int(min_xco2)
int_min = round(min_xco2, 2)
print(f'Valor mínimo do Fluxo CO2 na região selecionada: {int_min}, {min_xco2} ppm')

#sys.exit()


# Plotar temperatura de um dia específico
plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
#shp = list(shpreader.Reader('/home/meteoro/DADOS/dados/shapefiles/BR_UF_2019.shp').geometries())
shp = list(shpreader.Reader('/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/SC_UF_2022.shp').geometries())

# Criar uma paleta de cores personalizada
colors = ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#fee090", 
          "#fdae61", "#f46d43", "#d73027", "#a50026"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#800026')
cmap.set_under('#040273')
#cmap.set_under('#313695')

# Definir o intervalo de contorno
data_min = int_min
data_max = int_max
interval = 1
levels = np.linspace(data_min, data_max, num=256)
##### levels = np.arange(data_min, data_max + interval, interval)

# Plotar o dado 2D da região selecionada
"""
figure = data_region.plot.pcolormesh(robust=True, norm=cls.Normalize(vmin=int_min, vmax=int_max),
                                     cmap=cmap, add_colorbar=False, levels=levels, add_labels=False)
"""
figure = plt.contourf(data_region.lon, data_region.lat, data_region.values, levels=levels, cmap=cmap, 
                      norm=cls.Normalize(vmin=int_min, vmax=int_max), extend = "both")

ax.add_geometries(shp, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.5)
ax.coastlines(resolution='10m', color='black', linewidth=0.5)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.4)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 1), ylocs=np.arange(-90, 90, 1), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
        
#plt.colorbar(figure, pad=0.05, fraction=0.05, extend='max', ticks=np.arange(int_min, int_max, 0.1), orientation='vertical', label='Fluxo CO2 (ppm)')

# Função para formatar os ticks da colorbar com 2 casas decimais
def format_ticks(value, tick_number):
    return f'{value:.2f}'

# Adicionando a colorbar com formatação de 2 casas decimais
plt.colorbar(figure, pad=0.05, fraction=0.05, extend='both', ticks=np.arange(int_min, int_max+0.01, (int_max - int_min)/10), orientation='vertical', label='Fluxo CO2 (ppm)')

# Aplicando a formatação de 2 casas decimais aos ticks da colorbar
ax.yaxis.set_major_formatter(FuncFormatter(format_ticks))

plt.title(f'Fluxo CO2 (*1e6 ppm) - Santa Catarina\nPeríodo observado: {mes}/{ano} ', fontsize=14, ha='center')

# Adicionar a fonte no rodapé
#plt.figtext(0.55, 0.05, 'Fonte: SAMeT - CPTEC', ha='center', fontsize=10)

# Salvar a figura no formato ".jpg" com dpi=300.
plt.savefig(f"figuras/xco2_avg_mensal_{ano}{mes}.jpg", transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.02)

plt.show()
