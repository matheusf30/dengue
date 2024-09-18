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
url = "http://200.19.223.105/cgi-bin/dh?sinan/def/dengon.def"
url1 = "http://200.19.223.105/cgi-bin/tabnet?sinan/def/dengon.def"
ano_atual = str(datetime.today().year)
hoje = datetime.today().strftime("%Y-%m-%d")
caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"

# Definindo Função

def download_dengue():
	resposta = requests.get(url)
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
		print(f"Falha ao realizar download do arquivo diretamente de:\n{url}")

#Automatizando aos Domingos e Verificando 2x/dia
schedule.every().sunday.at("00:00").do(download_dengue) #.sunday.at("00:00") # .wednesday.at("12:03")
print(f"\nTarefa Automatizada\nDownload de dados sobre dengue semanalmente (domingo)\nHoje: {hoje}\nDisponível em: {url}\n")
while True:
    schedule.run_pending()
    time.sleep(1) # BID (12h/12h)(43200s)


