### Bibliotecas Correlatas
import pandas as pd
#import geopandas as gpd
#import matplotlib.pyplot as plt

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
#focos_timespace = "focos_timespace.csv" # Data de Coleta
focos_timespace = "focos_se_timespace.csv" # Semanas Epidemiológicas
#focos_timespace = "SC_Municipios_2022.shp" # Shapefile (?)

### Abrindo Arquivo
focos_timespace = pd.read_csv(f"{caminho_dados}{focos_timespace}")
#focos_timespace = gpd.read_file(f"{caminho_dados}{focos_timespace}")

### Exibindo Informações
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print(focos_timespace.info())
print("~"*80)
print(focos_timespace.dtypes)
print("~"*80)
print(focos_timespace)
print("="*80)
