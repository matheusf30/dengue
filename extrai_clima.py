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
        caminho_shape = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    elif _LOCAL == "CASA":
        caminho_shape = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    elif _LOCAL == "IFSC":
        caminho_shape = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
        caminho_merge = "/dados/operacao/merge/CDO.MERGE/"
        caminho_samet = "/dados/operacao/samet/clima/"
    else:
        print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
except:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR CAMINHO OU LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_shape}\n\n{caminho_merge}\n\n{caminho_samet}\n\n")

_ANO_FINAL = "2024" # Até quando os produtos de reanálise foram compilados

### Renomeação variáveis pelos arquivos
"""
merge = f"MERGE_CPTEC_DAILY_SB_2000_{_ANO_FINAL}.nc"

samet_tmax = f"TMAX/SAMeT_CPTEC_DAILY_TMAX_SB_2000_2022.nc"
samet_tmed = f"TMED/SAMeT_CPTEC_DAILY_TMED_SB_2000_2022.nc"
samet_tmin = f"TMIN/SAMeT_CPTEC_DAILY_TMIN_SB_2000_2022.nc"

samet_tmax = f"TMAX/SAMeT_CPTEC_DAILY_TMAX_SB_2000_{_ANO_FINAL}.nc"
samet_tmed = f"TMED/SAMeT_CPTEC_DAILY_TMED_SB_2000_{_ANO_FINAL}.nc"
samet_tmin = f"TMIN/SAMeT_CPTEC_DAILY_TMIN_SB_2000_{_ANO_FINAL}.nc"
"""
merge = "MERGE_CPTEC_DAILY_SB_2024_2024.nc"
samet_tmax = "TMAX/SAMeT_CPTEC_DAILY_TMAX_2024.nc"
samet_tmed = "TMED/SAMeT_CPTEC_DAILY_TMED_2024.nc"
samet_tmin = "TMIN/SAMeT_CPTEC_DAILY_TMIN_2024.nc"

municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivos
prec = xr.open_dataset(f"{caminho_merge}{merge}")
tmax = xr.open_dataset(f"{caminho_samet}{samet_tmax}")
tmed = xr.open_dataset(f"{caminho_samet}{samet_tmed}")
tmin = xr.open_dataset(f"{caminho_samet}{samet_tmin}")
municipios = gpd.read_file(f"{caminho_shape}{municipios}")

print(tmin.variables["tmin"][:])
print(tmin.variables["time"][:])
print(tmin.variables["nobs"][:])
print(tmin)


### Pré-processamento e Definição de Função
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

def verifica_nan(valores_centroides):
	"""
	Função relativa a verificação de Valores Não-números (NaN) no arquivo.csv gerado!
	Argumento: próprio dataframe criado na função extrair_centroides()
	Retorno: Exibição de mensagens para casos de haver ou não valores NaN.
	"""
	print(f"\n{bold}VERIFICAÇÃO DE DADOS FALTANTES{bold}\n")
	print(f"\nQuantidade de valores {red}{bold}NaN: {valores_centroides['FLORIANÓPOLIS'].isnull().sum()}{bold}{reset}")
	if valores_centroides["FLORIANÓPOLIS"].isnull().sum() == 0:
		print(f"\n{green}{bold}NÃO{bold} há valores {bold}NaN{bold}{reset}\n")
	else:
		print(f"\nOs dias com valores {red}{bold}NaN{bold}{reset} são:")
		print(f"{valores_centroides[valores_centroides['FLORIANÓPOLIS'].isna()]['Data']}\n")
	print("="*80)

def semana_epidemiologica(csv, str_var):
	"""
	Função relativa ao agrupamento de dados em semanas epidemiológicas.
	Os arquivos.csv são provenientes deo roteiro 'extrai_clima.py': colunas com datas e municípios + todas as linhas são dados diários.
	Estes Arquivos estão alocados no SifapSC ou GitHub.
	Argumento:
	- Variável com arquivo.csv;
	- String da variável referente ao arquivo.csv.
	Retorno:
	- Retorno próprio de DataFrame com Municípios (centróides) em Colunas e Tempo (semanas epidemiológicas) em Linhas, preenchidos com valores climáticos.
	- Salvando Arquivo.csv
	"""
	csv.drop(columns = str_var, inplace = True)
	csv["Data"] = pd.to_datetime(csv["Data"])
	csv = csv.sort_values(by = ["Data"])
	csv_se = csv.copy()
	csv_se["Semana"] = csv_se["Data"].dt.to_period("W-SAT").dt.to_timestamp()
	if str_var == "prec":
		csv_se = csv_se.groupby(["Semana"]).sum(numeric_only = True)
	else:
		csv_se = csv_se.groupby(["Semana"]).mean(numeric_only = True)
	csv_se.reset_index(inplace = True)
	csv_se.drop([0], axis = 0, inplace = True)
	csv_se.to_csv(f"{caminho_dados}{str_var}_semana_ate_{_ANO_FINAL}.csv", index = False)
	print(f"\n{green}ARQUIVO SALVO COM SUCESSO!\n\nSemana Epidemiológica - {str_var.upper()}{reset}\n\n{csv_se}\n")
	print(f"\n{red}As variáveis do arquivo ({str_var.upper()}), em semanas epidemiológicas, são:{reset}\n{csv_se.dtypes}\n")
	return csv_se

def extrair_centroides(shapefile, netcdf4, str_var):
	"""
	Função relativa a extração de valores dos arquivos NetCDF4 utilizando os centróides de arquivos shapefile como filtro.
	Os arquivos NetCDF4 são provenientes de Rozante et.al. e apresentam 2 variáveis: 1 climática + 1 nest ou 1 Nobs (estações de observação).
	Os arquivos Shapefile são provenientes do IBGE (2022) e apresentam CRS = (epsg = 4674)
	Estes Arquivos estão alocados no SifapSC, dois diretórios antes do /home.
	Argumento:
	- Variável com arquivo NetCDF4;
	- Variável com arquivo Shapefile;
	- String da variável referente ao NetCDF4.
	Retorno:
	- Retorno próprio de DataFrame com Municípios (centróides) em Colunas e Tempo (dias) em Linhas, preenchidos com valores climáticos.
	- Salvando Arquivo.csv (dados diários)
	- Retorno próprio de DataFrame com Municípios (centróides) em Colunas e Tempo (semanas epidemiológicas) em Linhas, preenchidos com valores climáticos.
	- Salvando Arquivo.csv (dados semanais)
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
	if str_var == "prec":
		valores_centroides.drop(columns = ["nest"], inplace = True)
	#else:
	#	valores_centroides.drop(columns = ["nobs"], inplace = True)
	valores_centroides = valores_centroides[["Municipio", str_var]]
	valores_tempo = netcdf4[str_var].time.values
	valores_variavel = netcdf4[str_var].values
	var_valores = []
	for i, linha in valores_centroides.iterrows():
		if isinstance(linha[str_var], xr.DataArray):
			var_valor = [x.item() if not np.isnan(x.item()) else np.nan for x in linha[str_var]]
			var_valores.append(var_valor)
			print(f"\n---{str_var}---\n{bold}{valores_centroides['Municipio'][i]}{bold}: Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
		else:
			var_valores.append([np.nan] * len(valores_tempo))
			print(f"\n{valores_centroides['Municipio'][i]}: NaN... Finalizado!\n{i + 1} de {len(valores_centroides['Municipio'])}.")
	var_valores_df = pd.DataFrame(var_valores, columns = valores_tempo)
	valores_centroides = pd.concat([valores_centroides, var_valores_df], axis = 1)
	valores_centroides.drop(columns = [str_var], inplace = True)
	valores_centroides.set_index("Municipio", inplace = True)
	valores_centroides = valores_centroides.T
	valores_centroides["Data"] = valores_centroides.index
	valores_centroides.reset_index(inplace = True)
	colunas_restantes = valores_centroides.columns.drop("Data")
	valores_centroides = valores_centroides[["Data"] + colunas_restantes.tolist()]
	valores_centroides.columns.name = str_var
	valores_centroides.rename(columns = {"index" : str_var}, inplace = True)
	valores_centroides.to_csv(f"{caminho_dados}{str_var}_diario_ate_{_ANO_FINAL}.csv", index = False)
	print("="*80)
	print(f"\n\n{caminho_shape}{str_dados}_diario_ate_{_ANO_FINAL}.csv\n\n{green}{bold}ARQUIVO SALVO COM SUCESSO!{bold}{reset}\n\n")
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
	verifica_nan(valores_centroides)
	semana_epidemiologica(valores_centroides, str_var)
	return valores_centroides


tmin = extrair_centroides(municipios, tmin, "tmin")
tmed = extrair_centroides(municipios, tmed, "tmed")
tmax = extrair_centroides(municipios, tmax, "tmax")
prec = extrair_centroides(municipios, prec, "prec")


print("!!"*80)
print(f"\n{green}{bold}FINALIZADA ATUALIZAÇÃO{bold}{reset}\n\nAtualização feita em produtos de reanálise até {red}{_ANO_FINAL}{reset}!\n")
print(f"{bold}(MERGE e SAMeT - tmin, tmed, tmax){bold}")
print("!!"*80)
