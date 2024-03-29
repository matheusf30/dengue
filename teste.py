### Bibliotecas Correlatas
import pandas as pd

### Encaminhamento aos Diretórios
_local = "CASA" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
## Dados "Brutos"
"""
casos = "casos.csv"
focos = "focos.csv"
merge = "merge_novo.csv"
tmax = "tmax.csv"
tmed = "tmed.csv"
tmin = "tmin.csv"
"""
## Série Histórica / Semana Epidemiológica

casos = "casos.csv"
focos = "focos_se.csv"
merge = "merge_se.csv"
tmax = "tmax_se.csv"
tmed = "tmed_se.csv"
tmin = "tmin_se.csv"

## (à partie de 2021 / Semana Epidemiológica
"""
casos = "casos21se.csv"
focos = "focos21se.csv"
merge = "merge21se.csv"
tmax = "tmax21se.csv"
tmed = "tmed21se.csv"
tmin = "tmin21se.csv"
"""
### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")

### Printando Informações
print("\n \n FOCOS DE _Aedes aegypti_ \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
#print(focos.iloc[105:574, :]) #jan2014-dez2022
print(focos.iloc[522:574, :]) #jan2022-dez2022
print("="*80)

print("\n \n CASOS DE DENGUE \n")
print(casos.info())
print("~"*80)
print(casos.dtypes) 
print("~"*80)
#print(casos) #jan2014-dez2022
print(casos.iloc[417:, :]) #jan2022-dez2022
print("="*80)

print("\n \n PRECIPITAÇÃO \n")
print(merge.info())
print("~"*80)
print(merge.dtypes)
print("~"*80)
#print(merge.iloc[710:, :]) #jan2014-dez2022
print(merge.iloc[1127:, :]) #jan2022-dez2022
print("="*80)

print("\n \n TEMPERATURA MÍNIMA \n")
print(tmin.info())
print("~"*80)
print(tmin.dtypes)
print("~"*80)
#print(tmin.iloc[732:, :]) #jan2014-dez2022
print(tmin.iloc[1149:, :]) #jan2022-dez2022
print("="*80)

print("\n \n TEMPERATURA MÉDIA \n")
print(tmed.info())
print("~"*80)
print(tmed.dtypes)
print("~"*80)
#print(tmed.iloc[732:, :]) #jan2014-dez2022
print(tmed.iloc[1149:, :]) #jan2022-dez2022
print("="*80)

print("\n \n TEMPERATURA MÁXIMA \n")
print(tmax.info())
print("~"*80)
print(tmax.dtypes)
print("~"*80)
#print(tmax.iloc[732:, :]) #jan2014-dez2022
print(tmax.iloc[1149:, :]) #jan2022-dez2022
print("="*80)
