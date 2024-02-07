### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
## Dados "Brutos"
focosdive = "focos_dive_total.csv"
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focosdive = pd.read_csv(f"{caminho_dados}{focosdive}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Limpeza e Tratamento de Dados 
focosdive = focosdive[["Regional", "Município", "Imóvel", "Depósito", "Data da Coleta"]]
# HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER...
trocanome = {
"HERVAL D`OESTE": "HERVAL D'OESTE",
"PRESIDENTE CASTELO BRANCO" : "PRESIDENTE CASTELLO BRANCO",
"SÃO CRISTOVÃO DO SUL" : "SÃO CRISTÓVÃO DO SUL",
"GRÃO PARÁ" : "GRÃO-PARÁ",
"LAURO MULLER" : "LAURO MÜLLER"
}
focosdive["Município"] = focosdive["Município"].replace(trocanome)
focosdive["Focos"] = 1
focosdive["Data"] = focosdive["Data da Coleta"]
focosdive["Data"] = pd.to_datetime(focosdive["Data"])
focossemana = focosdive.copy()
focossemana["Semana"] = focossemana["Data"].dt.to_period("W-SAT").dt.to_timestamp()
focossemana = focossemana.groupby(["Semana", "Município"]).sum(numeric_only = True)["Focos"]
focossemana = focossemana.reset_index()

### Unindo Dataframe e Geodataframe
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
pontos = cidades.copy()
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
#focos_timespace = pd.merge(focosdive, pontos, on = "Município", how = "left") # Data de Coleta
focos_timespace = pd.merge(focossemana, pontos, on = "Município", how = "left") # Semanas Epidemiológicas
focos_timespace = pd.merge(focos_timespace, cidades, on = "Município", how = "left")
focos_timespace = focos_timespace.drop(columns = ["NM_MUN_x", "NM_MUN_y"])

### Exibindo Informações
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focosdive.info())
print("~"*80)
print(focosdive.dtypes)
print("~"*80)
print(focosdive)
print("="*80)

print("\n \n MUNICÍPIOS DE SANTA CATARINA (IBGE) \n")
print(municipios.info())
print("~"*80)
print(municipios.dtypes)
print("~"*80)
print(municipios)
print("="*80)

print("\n \n MUNICÍPIOS DE SANTA CATARINA (IBGE- centróide) \n")
print(pontos.info())
print("~"*80)
print(pontos.dtypes)
print("~"*80)
print(pontos)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focossemana.info())
print("~"*80)
print(focossemana.dtypes)
print("~"*80)
print(focossemana)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (SE) (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print(focos_timespace.info())
print("~"*80)
print(focos_timespace.dtypes)
print("~"*80)
print(focos_timespace)
print("="*80)

rows_with_nan = focos_timespace[focos_timespace.isna().any(axis=1)]
# Display rows with NaN values
print(rows_with_nan)
# HERVAL D`OESTE, PRESIDENTE CASTELO BRANCO, SÃO CRISTOVÃO DO SUL, GRÃO PARÁ, LAURO MULLER... 

#focos_timespace.to_csv(f"{caminho_dados}focos_timespace.csv", index = False) # Data de Coleta
focos_timespace.to_csv(f"{caminho_dados}focos_se_timespace.csv", index = False) # Semanas Epidemiológicas
#focos_timespace.to_file(f"{caminho_dados}focos_timespace.shp") 
municipios.plot()
plt.show()
