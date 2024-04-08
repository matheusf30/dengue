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


### Encaminhamento aos Diretórios
try:
    _LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
    if _LOCAL == "GH": # _ = Variável Privada
        caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    elif _LOCAL == "CASA":
        caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    elif _LOCAL == "IFSC":
        #/dados/...pwd?.../home/sifapsc/scripts/matheus/dengue
        caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
        caminho_merge = "/dados/operacao/merge/CDO.MERGE/"
        caminho_samet = "/dados/operacao/samet/clima/"
    else:
        print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
except:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR CAMINHO OU LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

diretorio_atual = os.getcwd()
diretorios = diretorio_atual.split(os.path.sep)
diretorio_dados = os.path.sep.join(diretorios[:-6])
print(diretorio_dados)
sys.exit()


### Renomeação variáveis pelos arquivos
merge = "MERGE_CPTEC_DAILY_SB_2000_2022.nc"
samet_tmax = "TMAX/SAMeT_CPTEC_DAILY_TMAX_SB_2000_2022.nc"
samet_tmed = "TMED/SAMeT_CPTEC_DAILY_TMED_SB_2000_2022.nc"
samet_tmin = "TMIN/SAMeT_CPTEC_DAILY_TMIN_SB_2000_2022.nc"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivos
prec = xr.open_dataset(f"{caminho_dados}{merge}")
tmax = xr.open_dataset(f"{caminho_dados}{samet_tmax}")
tmed = xr.open_dataset(f"{caminho_dados}{samet_tmed}")
tmin = xr.open_dataset(f"{caminho_dados}{samet_tmin}")
municipios = gpd.read_file(f"{caminho_dados}{municipio}")

### Pré-processamento
municipios["centroide"] = municipios["geometry"].centroid
valores_centroides = []
for idx, linha in municipios.iterrows():
    lon, lat = linha["centroide"].x, linha["centroide"].y
    valor = prec.sel(lon = lon, lat = lat, method = "nearest")
    valores_centroides.append(valor)

valores_centroides = pd.to_DataFrame(valores_centroides)
print(valores_centroides)

