"""
>>> crontab -e
>>> 0 0 * * 0 /usr/bin/python3 /home/yourusername/dengue_download.py >> /home/yourusername/dengue_download.log 2>&1
>>> crontab -l

ImportError: Missing optional dependency 'lxml', 'html5lib'.  Use pip or conda to install lxml html5lib
Selenium -- CSS Selectors

# cfs press
https://nomads.ncep.noaa.gov/gribfilter.php?ds=cfs_pgb
# cfs fluxo
https://nomads.ncep.noaa.gov/gribfilter.php?ds=cfs_flx
#gfs 
https://nomads.ncep.noaa.gov/gribfilter.php?ds=gfs_0p25_1hr
"""

# Bibliotecas correlatas
from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time
from datetime import datetime

# Definindo Variáveis
url_ncep = "https://nomads.ncep.noaa.gov/cgi-bin/"
filtro_gfs = "filter_gfs_0p25_1hr.pl?dir=%2Fgfs."
hoje = datetime.today().strftime("%Y%m%d")
recorte_atual = "20240917%2F00%2Fatmos&file="
zulu = "t00z" # t18z | t12z | t06z | t00z
tempo = "f000" # anl | f000 | f001 | ... | f384
arquivo = f"gfs.{zulu}.pgrb2.0p25.{tempo}"
precipitacao = "var_PRATE=on"
tmax = "var_TMAX=on"
tmin = "var_TMIN=on"
tmed = "var_TMP=on"
superficie = "lev_surface=on"
variaveis = f"&{precipitacao}&{tmax}&{tmin}&{tmed}&{superficie}"
lat_max = 15
lat_min = -60
lon_max = -30
lon_min = -90
recorte_regiao = f"&subregion=&toplat={lat_max}&leftlon={lon_min}&rightlon={lon_max}&bottomlat={lat_min}"
url_gfs = f"{url_ncep}{filtro_gfs}{recorte_atual}{arquivo}{variaveis}{recorte_regiao}"
ano_atual = str(datetime.today().year)
hoje = datetime.today().strftime("%Y-%m-%d")
caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
arquivo = f"
# Definindo Função

def download_gfs():
	resposta = requests.get(url_gfs, stream = True))
	if resposta.status_code == 200:
		with open(
		df = pd.read_html(resposta.text)
		#df = df[0]
		arquivo = f"dengue_dive_{hoje}.csv"
		df.to_csv(f"{caminho_dados}{arquivo}", index = False)
		print(f"Download realizado com sucesso e salvo como:\n{arquivo}")
	else:
		print(f"Falha ao realizar download do arquivo diretamente de:\n{url_gfs}")





	soup = BeautifulSoup(resposta.text, "html.parser")
	form = soup.find("form")
	form_action = form["action"]
	"""
	INVESTIGAÇÃO DENGUE A PARTIR DE 2014
	Frequência por Mun infec SC e Sem.Epid.Sintomas
	Classificacao Nova: Dengue com complicações, Febre Hemorrágica do Dengue, Síndrome do Choque do Dengue, Dengue, Dengue com sinais de alarme, Dengre grave
	Conf.Desc pos2010: Laboratórial, Clínico-epidemiológico
	Período:2014

	<!--
	<TABELA>
	Planilha=
	Titulo=INVESTIGAÇÃO DENGUE A PARTIR DE 2014
	Def=sinan/def/dengon.def
	Varmunic=
	Linha=Mun_infec_SC
	Coluna=Sem.Epid.Sintomas
	Incremento=Frequência
	SClassificacao_Nova=2
	SClassificacao_Nova=3
	SClassificacao_Nova=4
	SClassificacao_Nova=7
	SClassificacao_Nova=8
	SClassificacao_Nova=9
	SConf.Desc_pos2010=2
	SConf.Desc_pos2010=3
	Periodo=24
	</TABELA>
	-->
	"""
	form_data = {"Linha": "Mun infec SC", "Coluna": "Sem.Epid.Sintomas",
				"Períodos Disponíveis": ano_atual,
				"Classificacao Nova" : ["Dengue com complicações", "Febre Hemorrágica do Dengue",
										"Síndrome do Choque do Dengue", "Dengue",
										"Dengue com sinais de alarme", "Dengre grave"],
				"Conf.Desc pos2010" : ["Laboratórial", "Clínico-epidemiológico"]}
	resposta = requests.post(f"http://200.19.223.105{form_action}", data = form_data)
	if resposta.status_code == 200:
		df = pd.read_html(resposta.text)
		#df = df[0]
		arquivo = f"dengue_dive_{hoje}.csv"
		df.to_csv(f"{caminho_dados}{arquivo}", index = False)
		print(f"Download realizado com sucesso e salvo como:\n{arquivo}")
	else:
		print(f"Falha ao realizar download do arquivo diretamente de:\n{url_gfs}")

#Automatizando aos Domingos e Verificando 2x/dia
schedule.every().sunday.at("00:00").do(download_dengue) #.sunday.at("00:00") # .wednesday.at("12:03")
print(f"\nTarefa Automatizada\nDownload de dados sobre dengue semanalmente (domingo)\nHoje: {hoje}\nDisponível em: {url_gfs}\n")
while True:
    schedule.run_pending()
    time.sleep(1) # BID (12h/12h)(43200s)


