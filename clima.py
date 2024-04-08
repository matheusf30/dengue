### Bibliotecas Correlatas
# Suporte
import sys, os
# Básicas
import pandas as pd
import numpy as np
"""
import matplotlib.pyplot as plt               
import seaborn as sns
import statsmodels as sm
"""
# Manipulação de netCDF4 e shapefiles
import  xarray as xr
import geopandas as gpd
from shapely.geometry import Point

"""
diretorio_atual = os.getcwd()
diretorios = diretorio_atual.split(os.path.sep)
diretorio_dados = os.path.sep.join(diretorios[:-6])
print(diretorio_dados)
"""


### Encaminhamento aos Diretórios
try:
    _LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
    if _LOCAL == "GH": # _ = Variável Privada
        caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    elif _LOCAL == "CASA":
        caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    elif _LOCAL == "IFSC":
        caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
        caminho_merge = "/dados/operacao/merge/CDO.MERGE/"
        caminho_samet = "/dados/operacao/samet/clima/"
    else:
        print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
except:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR CAMINHO OU LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n{caminho_merge}\n\n{caminho_samet}\n\n")

### Renomeação variáveis pelos arquivos
merge = "MERGE_CPTEC_DAILY_SB_2000_2022.nc"
samet_tmax = "TMAX/SAMeT_CPTEC_DAILY_TMAX_SB_2000_2022.nc"
samet_tmed = "TMED/SAMeT_CPTEC_DAILY_TMED_SB_2000_2022.nc"
samet_tmin = "TMIN/SAMeT_CPTEC_DAILY_TMIN_SB_2000_2022.nc"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivos
prec = xr.open_dataset(f"{caminho_merge}{merge}")
tmax = xr.open_dataset(f"{caminho_samet}{samet_tmax}")
tmed = xr.open_dataset(f"{caminho_samet}{samet_tmed}")
tmin = xr.open_dataset(f"{caminho_samet}{samet_tmin}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Pré-processamento

municipios["centroide"] = municipios["geometry"].centroid
municipios["centroide"] = municipios["centroide"].to_crs(epsg = 4674)
valores_centroides = []
for idx, linha in municipios.iterrows():
    lon, lat = linha["centroide"].x, linha["centroide"].y
    valor = prec.sel(lon = lon, lat = lat, method = "nearest")
    valores_centroides.append(valor)
valores_centroides = pd.DataFrame(data = valores_centroides)
valores_centroides["Municipio"] = municipios["NM_MUN"].str.upper().copy()
valores_centroides.drop(columns = ["nest"], inplace = True)
valores_centroides = valores_centroides[["Municipio", "prec"]]
valores_tempo = prec["prec"].time.values
valores_variavel = prec["prec"].values

prec_valores = []
for i, linha in valores_centroides.iterrows():
    print(i)
    for j in range(0, len(prec["prec"].time)):
        print(i, j)
        prec_valor = linha["prec"][j].values.item() if len(linha["prec"]) >= 0 else np.nan
        prec_valores.append(prec_valor)
valores_centroides = pd.concat(prec_valores, axis = 1)
#valores_centroides["precipita"] = prec_valores
# df = df.explode(list('AC'))
"""
for j, tempo in enumerate(valores_tempo):
    valores_centroides[tempo] = [valores_centroides["prec"][j].values.item() if len(valores_centroides["prec"]) > j else np.nan for _, valores_centroides in valores_centroides.iterrows()]
"""
print("="*80)
print(valores_centroides)
print(valores_centroides.info())
print("="*80)
print(prec.variables["prec"][:])
print(prec.variables["time"][:])
print(valores_centroides["prec"][0])
print("="*80)
print(valores_tempo)
print(valores_tempo.shape)
print("="*80)
print(valores_variavel)
print(valores_variavel.shape)
print("="*80)

"""
prec_pivot = pd.DataFrame()
prec_pivot["Municipio"] = municipios["NM_MUN"].str.upper().copy()
prec_pivot = prec_pivot.T
prec_pivot["data"] = []
prec_pivot["data"].set_index(inplace = True)
print(prec_pivot)

print(valores_pivot)
print(valores_pivot.info())
"""

