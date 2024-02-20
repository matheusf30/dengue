### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
#dado = "dado_rede22.csv"
dado = "dado_rede4cat22.csv"
#dado = "dado_rede4cat.csv"
#dado = "dado_rede.csv"
#dado = "dado_rede_neural.csv"

### Abrindo Arquivo
dado = pd.read_csv(f"{caminho_dados}{dado}")

### Exibindo Informações
print("="*80)
#print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA EM SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS_xy_LATLON (IBGE) ")
print(dado.info())
print("~"*80)
print(dado.dtypes)
print("~"*80)
print(dado)
print("="*80)
