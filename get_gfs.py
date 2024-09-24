"""
>>> crontab -e
>>> 0 0 * * 0 /usr/bin/python3 /home/sifapsc/scripts/matheus/dengue/get_dengue.py >> /home/sifapsc/scripts/matheus/dengue/get_dengue.log 2>&1
>>> crontab -l

# cfs press
https://nomads.ncep.noaa.gov/gribfilter.php?ds=cfs_pgb
# cfs fluxo
https://nomads.ncep.noaa.gov/gribfilter.php?ds=cfs_flx
#gfs 
https://nomads.ncep.noaa.gov/gribfilter.php?ds=gfs_0p25_1hr
"""

##### Bibliotecas correlatas ####################################################
#from bs4 import BeautifulSoup
#import pandas as pd
#import schedule
import os
import time
from datetime import datetime
import requests
import cfgrib
import xarray as xr
import netCDF4

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

#### Definindo Função ###########################################################
def download_gfs():

	#### Definindo Variáveis
	url_ncep = "https://nomads.ncep.noaa.gov/cgi-bin/"
	filtro_gfs = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
	data = datetime.today().strftime("%Y%m%d") #20240917
	#data = "20240910"
	recorte_atual = f"{data}%2F{zulu}%2Fatmos&file="
	#zulu = "t00z" # t18z | t12z | t06z | t00z
	#tempo = "f000" # anl | f000 | f001 | ... | f384 (anl = análise; não necessário)
	arquivo = f"gfs.t{zulu}z.pgrb2.0p25.{tempo}"
	precipitacao = "var_PRATE=on"
	tmax = "var_TMAX=on"
	tmin = "var_TMIN=on"
	tmed = "var_TMP=on"
	superficie = "lev_surface=on"
	variaveis = f"&{precipitacao}&{tmax}&{tmin}&{tmed}&{superficie}"
	#variaveis = f"&{precipitacao}&{tmax}&{tmin}&{tmed}" # Em todos os níveis
	lat_max = 15
	lat_min = -60
	lon_max = -30
	lon_min = -90
	recorte_regiao = f"&subregion=&toplat={lat_max}&leftlon={lon_min}&rightlon={lon_max}&bottomlat={lat_min}"
	url_gfs = f"{url_ncep}{filtro_gfs}{recorte_atual}{arquivo}{variaveis}{recorte_regiao}"
	ano_atual = str(datetime.today().year)
	hoje = datetime.today().strftime("%Y-%m-%d")
	caminho_dados = f"/media/dados/operacao/gfs/0p25/{data}/"
	nome_arquivo = f"{arquivo}_{data}.grib2"
	caminho_arquivo = f"{caminho_dados}{nome_arquivo}"
	nome_arquivo_nc = f"{arquivo}_{data}.nc"
	caminho_arquivo_nc = f"{caminho_dados}{nome_arquivo_nc}"
	caminho_arquivo_idx = f"{caminho_dados}{nome_arquivo}.5b7b6.idx"

	#### Response/Request
	resposta = requests.get(url_gfs, stream = True)
	if resposta.status_code == 200:
		os.makedirs(caminho_dados, exist_ok = True)
		with open(caminho_arquivo, "wb") as file:
			for chunk in resposta.iter_content(chunk_size = 999999999):
				file.write(chunk)
			ds = xr.open_dataset(caminho_arquivo, engine = "cfgrib",
								filter_by_keys = {"stepType" : "instant"},
								errors = "ignore")
			ds.to_netcdf(caminho_arquivo_nc)
		print(f"{green}\nDownload realizado com sucesso e salvo como:\n{caminho_dados}\n{nome_arquivo}\n{nome_arquivo_nc}\n{reset}")
		os.remove(caminho_arquivo)
		os.remove(caminho_arquivo_idx)
		print(f"{cyan}\nRemoção realizada com sucesso:\n{nome_arquivo}\n{reset}")
	else:
		print(f"""
{red}Falha ao realizar download do arquivo diretamente de: {url_gfs}
{resposta.status_code}
{resposta.text}
{nome_arquivo}
{nome_arquivo_nc}\n{reset}""")

#################################################################################

#### Automatizando toatais de arquivos do dia ###################################
lista_zulu = ["00", "06", "12", "18"]
lista_tempo = [f"f{str(n).zfill(3)}" for n in range(385)]
for zulu in lista_zulu:
	for tempo in lista_tempo:
		download_gfs()

#################################################################################

"""
#Automatizando aos Domingos e Verificando 2x/dia
schedule.every().sunday.at("00:00").do(download_dengue) #.sunday.at("00:00") # .wednesday.at("12:03")
print(f"\nTarefa Automatizada\nDownload de dados sobre dengue semanalmente (domingo)\nHoje: {hoje}\nDisponível em: {url_gfs}\n")
while True:
    schedule.run_pending()
    time.sleep(1) # BID (12h/12h)(43200s)
"""

