### Bibliotecas Correlatas
import pandas as pd

### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
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
## Dados "Brutos"
## Fonte: DIVE/SC
focos2024_3 = "focos_dive_2024_3"
focos2024_2 = "focos_dive_2024_2"
focos2024_1 = "focos_dive_2024_1"
focos2023dez = "focos_dive_2023_DEZ.csv"
focos2023nov = "focos_dive_2023_NOV.csv"
focos2023out = "focos_dive_2023_OUT.csv"
focos2023set = "focos_dive_2023_SET.csv"
focos2023ago = "focos_dive_2023_AGO.csv"
focos2023jul = "focos_dive_2023_JUL.csv"
focos2023jun = "focos_dive_2023_JUN.csv"
focos2023mai = "focos_dive_2023_MAI.csv"
focos2023abr = "focos_dive_2023_ABR.csv"
focos2023mar = "focos_dive_2023_MAR.csv"
focos2023fev = "focos_dive_2023_FEV.csv"
focos2023jan = "focos_dive_2023_JAN.csv"
focos202202 = "focos_dive_2022_02.csv"
focos202201 = "focos_dive_2022_01.csv"
focos2021 = "focos_dive_2021.csv"
focos2020 = "focos_dive_2020.csv"
focos2019 = "focos_dive_2019.csv"
focos2018 = "focos_dive_2018.csv"
focos2017 = "focos_dive_2017.csv"
focos2016 = "focos_dive_2016.csv"
focos2015 = "focos_dive_2015.csv"
focos2014 = "focos_dive_2014.csv"
focos2013 = "focos_dive_2013.csv"
focos2012 = "focos_dive_2012.csv"

### Abrindo Arquivos
focos2024_3 = pd.read_csv(f"{caminho_dados}{focos2024_3}", skiprows = 3)
focos2024_2 = pd.read_csv(f"{caminho_dados}{focos2024_2}", skiprows = 3)
focos2024_1 = pd.read_csv(f"{caminho_dados}{focos2024_1}", skiprows = 3)
focos2023dez = pd.read_csv(f"{caminho_dados}{focos2023dez}", skiprows = 3)
focos2023nov = pd.read_csv(f"{caminho_dados}{focos2023nov}", skiprows = 3)
focos2023out = pd.read_csv(f"{caminho_dados}{focos2023out}", skiprows = 3)
focos2023set = pd.read_csv(f"{caminho_dados}{focos2023set}", skiprows = 3)
focos2023ago = pd.read_csv(f"{caminho_dados}{focos2023ago}", skiprows = 3)
focos2023jul = pd.read_csv(f"{caminho_dados}{focos2023jul}", skiprows = 3)
focos2023jun = pd.read_csv(f"{caminho_dados}{focos2023jun}", skiprows = 3)
focos2023mai = pd.read_csv(f"{caminho_dados}{focos2023mai}", skiprows = 3)
focos2023abr = pd.read_csv(f"{caminho_dados}{focos2023abr}", skiprows = 3)
focos2023mar = pd.read_csv(f"{caminho_dados}{focos2023mar}", skiprows = 3)
focos2023fev = pd.read_csv(f"{caminho_dados}{focos2023fev}", skiprows = 3)
focos2023jan = pd.read_csv(f"{caminho_dados}{focos2023jan}", skiprows = 3)
focos202202 = pd.read_csv(f"{caminho_dados}{focos202202}", skiprows = 3)
focos202201 = pd.read_csv(f"{caminho_dados}{focos202201}", skiprows = 3)
focos2021 = pd.read_csv(f"{caminho_dados}{focos2021}", skiprows = 3)
focos2020 = pd.read_csv(f"{caminho_dados}{focos2020}", skiprows = 3)
focos2019 = pd.read_csv(f"{caminho_dados}{focos2019}", skiprows = 3)
focos2018 = pd.read_csv(f"{caminho_dados}{focos2018}", skiprows = 3)
focos2017 = pd.read_csv(f"{caminho_dados}{focos2017}", skiprows = 3)
focos2016 = pd.read_csv(f"{caminho_dados}{focos2016}", skiprows = 3)
focos2015 = pd.read_csv(f"{caminho_dados}{focos2015}", skiprows = 3)
focos2014 = pd.read_csv(f"{caminho_dados}{focos2014}", skiprows = 3)
focos2013 = pd.read_csv(f"{caminho_dados}{focos2013}", skiprows = 3)
focos2012 = pd.read_csv(f"{caminho_dados}{focos2012}", skiprows = 3)

### Pré-Processamento
focos2024 = pd.concat([focos2024_3, focos2024_2, focos2024_1])
focos2023 = pd.concat([focos2023dez, focos2023nov, focos2023out, focos2023set,
                       focos2023ago, focos2023jul, focos2023jun, focos2023mai,
                       focos2023abr, focos2023mar, focos2023fev, focos2023jan])
focos2022 = pd.concat([focos202202, focos202201])
##
pospandemia = pd.concat([focos2024, focos2023, focos2022, focos2021, focos2020], ignore_index = True)
prepandemia = pd.concat([focos2019, focos2018, focos2017, focos2016], ignore_index = True)
inicial = pd.concat([focos2015, focos2014, focos2013, focos2012], ignore_index = True)
prepandemia = pd.concat([prepandemia, inicial], ignore_index= True)
focostotal = pd.concat([pospandemia, prepandemia], ignore_index = True)

### Salvando Arquivo
focostotal.to_csv(f"{caminho_dados}focos_dive_total.csv", index = False)
pospandemia.to_csv(f"{caminho_dados}focos_dive_pospandemia.csv", index = False)

### Printando Informações
print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2012 \n")
print(focos2012.info())
print("~"*80)
print(focos2012.dtypes)
print("~"*80)
print(focos2012)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2013 \n")
print(focos2013.info())
print("~"*80)
print(focos2013.dtypes)
print("~"*80)
print(focos2013)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2014 \n")
print(focos2014.info())
print("~"*80)
print(focos2014.dtypes)
print("~"*80)
print(focos2014)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2015 \n")
print(focos2015.info())
print("~"*80)
print(focos2015.dtypes)
print("~"*80)
print(focos2015)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2016 \n")
print(focos2016.info())
print("~"*80)
print(focos2016.dtypes)
print("~"*80)
print(focos2016)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2017 \n")
print(focos2017.info())
print("~"*80)
print(focos2017.dtypes)
print("~"*80)
print(focos2017)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2018 \n")
print(focos2018.info())
print("~"*80)
print(focos2018.dtypes)
print("~"*80)
print(focos2018)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2019 \n")
print(focos2019.info())
print("~"*80)
print(focos2019.dtypes)
print("~"*80)
print(focos2019)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2020 \n")
print(focos2020.info())
print("~"*80)
print(focos2020.dtypes)
print("~"*80)
print(focos2020)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2021 \n")
print(focos2021.info())
print("~"*80)
print(focos2021.dtypes)
print("~"*80)
print(focos2021)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2022 \n")
print(focos2022.info())
print("~"*80)
print(focos2022.dtypes)
print("~"*80)
print(focos2022)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2023 \n")
print(focos2023.info())
print("~"*80)
print(focos2023.dtypes)
print("~"*80)
print(focos2023)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA NO ANO DE 2024 \n")
print(focos2024.info())
print("~"*80)
print(focos2024.dtypes)
print("~"*80)
print(focos2024)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA ANTES DA PANDEMIA \n")
print(prepandemia.info())
print("~"*80)
print(prepandemia.dtypes)
print("~"*80)
print(prepandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA DURANTE E APÓS PANDEMIA \n")
print(pospandemia.info())
print("~"*80)
print(pospandemia.dtypes)
print("~"*80)
print(pospandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes_ sp. EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(focostotal.info())
print("~"*80)
print(focostotal.dtypes)
print("~"*80)
print(focostotal)
print("="*80)
