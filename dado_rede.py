### Bibliotecas Correlatas
import pandas as pd
import numpy as np
"""
import matplotlib.pyplot as plt               
import seaborn as sns
import statsmodels as sm
"""

### Encaminhamento aos Diretórios
_local = "CASA" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
"""
#casos = "casos.csv"
focos = "focos_seSH.csv"
merge = "merge_seSH.csv"
#tmax = "tmax_seSH.csv"
tmed = "tmed_seSH.csv"
#tmin = "tmin_seSH.csv"
"""
## 2022
focos = "focos22se.csv"
merge = "merge22se.csv"
tmed = "tmed22se.csv"


### Abrindo Arquivos
#casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
#tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
#tmin = pd.read_csv(f"{caminho_dados}{tmin}")

### Selecionando Município e Manipulando Variáveis
## Recorte Município (Florianópolis)
dado_rede = focos[["Palhoça", "Florianópolis"]].iloc[: ]
dado_rede = dado_rede.rename(columns={"Florianópolis" : "Focos"})
dado_rede["Temperatura"] = tmed["Florianópolis"]
dado_rede["Precipitação"] = merge["Florianópolis"]
dado_rede = dado_rede.drop(["Palhoça"], axis = "columns")
dado_rede["Focos_m1"] = focos["Florianópolis"].shift(1)
dado_rede["Temperatura_m1"] = tmed["Florianópolis"].shift(1)
dado_rede["Precipitação_m1"] = merge["Florianópolis"].shift(1)
dado_rede["Focos_m2"] = focos["Florianópolis"].shift(2)
dado_rede["Temperatura_m2"] = tmed["Florianópolis"].shift(2)
dado_rede["Precipitação_m2"] = merge["Florianópolis"].shift(2)
dado_rede["Focos_m3"] = focos["Florianópolis"].shift(3)
dado_rede["Temperatura_m3"] = tmed["Florianópolis"].shift(3)
dado_rede["Precipitação_m3"] = merge["Florianópolis"].shift(3)
dado_rede["Focos_m4"] = focos["Florianópolis"].shift(4)
dado_rede["Temperatura_m4"] = tmed["Florianópolis"].shift(4)
dado_rede["Precipitação_m4"] = merge["Florianópolis"].shift(4)
"""
dado_rede["Categoria"] = dado_rede["Focos"].apply(lambda x: "1" if x <= dado_rede["Focos"].quantile(.25) \
                                                  else "2" if x < dado_rede["Focos"].quantile(.5) \
                                                  else "3" if x < dado_rede["Focos"].quantile(.75) \
                                                  else "4")
"""
dado_rede["Categoria"] = dado_rede["Focos"].apply(lambda x: "1" if x <= dado_rede["Focos"].quantile(.1) \
                                                  else "2" if x < dado_rede["Focos"].quantile(.2) \
                                                  else "3" if x < dado_rede["Focos"].quantile(.3) \
                                                  else "4" if x < dado_rede["Focos"].quantile(.4) \
                                                  else "5" if x < dado_rede["Focos"].quantile(.5) \
                                                  else "6" if x < dado_rede["Focos"].quantile(.6) \
                                                  else "7" if x < dado_rede["Focos"].quantile(.7) \
                                                  else "8" if x < dado_rede["Focos"].quantile(.8) \
                                                  else "9" if x < dado_rede["Focos"].quantile(.9) \
                                                  else "10")
dado_rede.dropna(axis = 0, inplace = True)
dado_rede = dado_rede.round(2)
del focos
# dado_rede.to_csv(f"{caminho_dados}dado_rede.csv", index = False)
# dado_rede.to_csv(f"{caminho_dados}dado_rede4cat.csv", index = False)
# dado_rede.to_csv(f"{caminho_dados}dado_rede4cat22.csv", index = False)
dado_rede.to_csv(f"{caminho_dados}dado_rede22.csv", index = False)

print("\n \n BASE DE DADOS PARA REDE NEURAL \n")
print(dado_rede.info())
print("~"*80)
print(dado_rede.dtypes)
print("~"*80)
print(dado_rede)
print("="*80)
