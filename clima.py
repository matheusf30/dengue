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
merge = "MERGE_CPTEC_DAILY_SB_2000_2023.nc"
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

### Pré-processamento e Definição de Função

def extrair_centroides(shapefile, netcdf4, str_var):

	"""
	Função relativa a extração de valores dos arquivos NetCDF4 utilizando os centróides de arquivos shapefile como filtro.
	Os arquivos NetCDF4 são provenientes de Rozante et.al. e apresentam 2 variáveis: 1 climática + 1 nest (estações de observação).
	Os arquivos Shapefile são provenientes do IBGE (2022) e apresentam CRS = (epsg = 4674)
	Estes Arquivos estão alocados no SifapSC, dois diretórios antes do /home.
	Argumento:
	- Variável com arquivo NetCDF4;
	- Variável com arquivo Shapefile;
	- String da variável referente ao NetCDF4.
	Retorno:
	- Retorno próprio de DataFrame com Municípios (centróides) em Colunas e Tempo (dias) em Linhas, preenchidos com valores climáticos.
	- Salvando Arquivo.csv
	"""
	shapefile["centroide"] = shapefile["geometry"].centroid
	shapefile["centroide"] = shapefile["centroide"].to_crs(epsg = 4674)
	valores_centroides = []
	for idx, linha in shapefile.iterrows():
		lon, lat = linha["centroide"].x, linha["centroide"].y
		valor = netcdf4.sel(lon = lon, lat = lat, method = "nearest")
		valores_centroides.append(valor)
	valores_centroides = pd.DataFrame(data = valores_centroides)
	valores_centroides["Municipio"] = shapefile["NM_MUN"].str.upper().copy()
	valores_centroides.drop(columns = ["nest"], inplace = True)
	valores_centroides = valores_centroides[["Municipio", str_var]]
	valores_tempo = netcdf4[str_var].time.values
	valores_variavel = netcdf4[str_var].values
	var_valores = []
	for i, linha in valores_centroides.iterrows():
		if isinstance(linha[str_var], xr.DataArray):
			var_valor = [x.item() if not np.isnan(x.item()) else np.nan for x in linha[str_var]]
			var_valores.append(var_valor)
			print(f"\n{valores_centroides['Municipio'][i]}: Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
		else:
			var_valores.append([np.nan] * len(valores_tempo))
			print(f"\n{valores_centroides['Municipio'][i]}: NaN... Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
	var_valores_df = pd.DataFrame(var_valores, columns = valores_tempo)
	valores_centroides = pd.concat([valores_centroides, var_valores_df], axis = 1)
	valores_centroides.drop(columns = [str_var], inplace = True)
	valores_centroides = valores_centroides.T
	valores_centroides["Data"] = valores_centroides.index
	valores_centroides.reset_index(drop = True, inplace = True)
	valores_centroides.set_index("Data", inplace = True)
	valores_centroides.columns.name = str_var
	#valores_centroides.to_csv(f"{caminho_dados}{str_var}.csv", index = False)
	print("="*80)
	print(netcdf4.variables[str_var][:])
	print(netcdf4.variables["time"][:])
	print("="*80)
	print(valores_tempo)
	print(valores_tempo.shape)
	print("="*80)
	print(valores_variavel)
	print(valores_variavel.shape)
	print("="*80)
	print(valores_centroides)
	print(valores_centroides.info())
	print(valores_centroides.dtypes)
	print("="*80)
	return valores_centroides

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
	if isinstance(linha["prec"], xr.DataArray):
		prec_valor = [x.item() if not np.isnan(x.item()) else np.nan for x in linha["prec"]]
		prec_valores.append(prec_valor)
		print(f"\n{valores_centroides['Municipio'][i]}: Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
	else:
		prec_valores.append([np.nan] * len(valores_tempo))
		print(f"\n{valores_centroides['Municipio'][i]}: NaN... Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
prec_valores_df = pd.DataFrame(prec_valores, columns = valores_tempo)
valores_centroides = pd.concat([valores_centroides, prec_valores_df], axis = 1)
valores_centroides.drop(columns = ["prec"], inplace = True)
valores_centroides.set_index("Município", inplace = True)
valores_centroides = valores_centroides.T
valores_centroides = valores_centroides.rename(columns = {"index" : "Data"})
#valores_centroides.index.name = "Data"
#valores_centroides.reset_index(inplace = True)
#valores_centroides.set_index("Data", inplace = True)
valores_centroides = valores_centroides.rename(columns={"index": "Data"})
valores_centroides.columns.name = "prec"
#valores_centroides.to_csv(f"{caminho_dados}{str_var}.csv", index = False)
print("="*80)
print(prec.variables["prec"][:])
print(prec.variables["time"][:])
print("="*80)
print(valores_tempo)
print(valores_tempo.shape)
print("="*80)
print(valores_variavel)
print(valores_variavel.shape)
print("="*80)
print(valores_centroides)
print(valores_centroides.info())
print(valores_centroides.dtypes)
print("="*80)
