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


# # Abrir aquivo NETCDF MERGE (ds)

# In[2]:


# ABRE ARQUIVO NETCDF DATASET (ds) 
ds = xr.open_dataset('prec_sc_2000_2022.nc')

print('Arquivo original:', ds, '\n')
print('***************************************\n')

#VISUALIZAR dimensões do aquivo (Latitude, Longitude e Time)

# LAT
print('Coordenadas em Latitude:',ds.lat, '\n')
print('***************************************\n')

# LON
print('Coordenadas em Longitude:',ds.lon, '\n')
print('***********max****************************\n')

# TIME
print('Datas:', ds.time, '\n')
print('***************************************\n')


# In[4]:


# Variável
print('Data variable:', ds.prec, '\n')
print('***************************************\n')

#  Plotar prec de um dia qualquer

# In[5]:



ds.sel(time='2022-12-01').prec.plot()
plt.show()

plt.figure(figsize=(10,6))

# Use a projeção geoestacionária em cartopy (Use the Geostationary projection in cartopy)
ax = plt.axes(projection=ccrs.PlateCarree())

shp= list(shpreader.Reader('SC_Municipios_2022.shp').geometries())

cmap=cmocean.cm.balance
#cmap.set_over('#000000') # black color
#cmap.set_under('#ffffff') # White color

# Define de contour interval
data_min = ds["prec"].min() + 1
data_max = ds["prec"].max()

interval = 2
levels = np.arange(data_min, data_max + interval, interval)
#levels = 100max
# ESTA FUNÇÃO QUE DELIMITA VALORES norm=cls.Normalize(vmin=1, vmax=71),

figure = ds.sel(time='2022-12-01').prec.plot.pcolormesh(robust=True, norm=cls.Normalize(vmin= data_min, vmax=data_max),
        cmap=cmap,
        add_colorbar=False, levels=levels, add_labels=False)


ax.add_geometries(shp, ccrs.PlateCarree(), edgecolor='white',facecolor='none', linewidth=0.15)

# Add  litoral, fronteiras e linhas de grade (coastlines, borders and gridlines)
ax.coastlines(resolution='10m', color='white', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='white', linewidth=0.8)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 1), ylocs=np.arange(-90, 90, 1), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
        
plt.colorbar(figure, pad=0.02, fraction=0.05, extend='max', ticks=np.arange(data_min, data_max,25), orientation='vertical', label='Daily Total of Precipitation [mm]')

plt.title('Precipitation time=2022-12-01',fontsize=14, ha='center')

# Salva a figura no formato ".jpg" com dpi=300.


#plt.savefig("teste_merge1.jpg", transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.02)
plt.show()
"""
# In[8]:


plt.figure(figsize=(8,6))


# Use a projeção geoestacionária em cartopy (Use the Geostationary projection in cartopy)
ax = plt.axes(projection=ccrs.PlateCarree())

shp= list(shpreader.Reader('SC_Municipios_2022.shp').geometries())

# Create a custom color palette 
colors = ["#b4f0f0", "#96d2fa", "#78b9fa", "#3c95f5", "#1e6deb", "#1463d2", 
          "#0fa00f", "#28be28", "#50f050", "#72f06e", "#b3faaa", "#fff9aa", 
          "#ffe978", "#ffc13c", "#ffa200", "#ff6200", "#ff3300", "#ff1500", 
          "#c00100", "#a50200", "#870000", "#653b32"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#000000')
cmap.set_under('#ffffff')

# Define de contour interval
data_min = 1
data_max = 72
interval = 1
levels = np.arange(data_min,data_max + interval,interval)

figure = ds.sel(time='2018-01-01').prec.plot.pcolormesh(robust=True, norm=cls.Normalize(vmin=1, vmax=72),
        cmap=cmap,
        add_colorbar=False, levels=levels, add_labels=False)
ax.add_geometries(shp, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add  litoral, fronteiras e linhas de grade (coastlines, borders and gridlines)
ax.coastlines(resolution='10m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
        
plt.colorbar(figure, pad=0.05, fraction=0.05, extend='max', ticks=np.arange(1,72,5), orientation='vertical', label='Daily Total of Precipitation [mm]')

plt.title('Precipitation time=2018-01-01',fontsize=14, ha='center')

# Salva a figura no formato ".jpg" com dpi=300.

#plt.savefig("teste_merge2.jpg", transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.02)

plt.show()
"""


