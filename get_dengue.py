

# Bibliotecas correlatas
import requests
import pandas as pd
import schedule
import time
from datetime import datetime

# Definindo Função
url = "http://200.19.223.105/cgi-bin/tabnet?sinan/def/dengon.def"
def download_dengue():
	hoje = datetime.today().strftime("%Y-%m-%d")
	resposta = requests.get(url)
	if resposta.status_code == 200:
		df = pd.read_html(resposta.text)
		#df = df[0]
	
		# Save the DataFrame to a CSV file
		arquivo = f"dengue_dive_{hoje}.csv"
		df.to_csv(file_name, index=False)
		print(f"Download realizado com sucesso e salvo como:\n{arquivo}")
	else:
		print(f"Falha ao realizar download do arquivo diretamente de:\n{url}")

#Automatizando aos Domingos e Verificando 2x/dia
schedule.every().sunday.at("00:00").do(download_dengue)
print(f"\nTarefa Automatizada\nDownload de dados sobre dengue semanalmente (domingo)\nHoje: {hoje}\nDisponível em: {url}\n")
while True:
    schedule.run_pending()
    time.sleep(43200) # BID (12h/12h)


