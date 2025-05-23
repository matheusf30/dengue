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
focos_xy = "focos_timespace_xy.csv"

### Abrindo Arquivo
focos_xy = pd.read_csv(f"{caminho_dados}{focos_xy}")

### Pré-Processamento
focos_pivot = pd.pivot_table(focos_xy, index = "Semana", columns = "Município", values = "Focos", fill_value = 0)
focos_pivot.reset_index(inplace = True)
registro_municipios = len(focos_xy["Município"].unique())
ultimo_registro = focos_xy["Semana"].max()

### Salvando Arquivo
focos_pivot.to_csv(f"{caminho_dados}focos_pivot.csv", index = False)

### Exibindo Informações
print("\n \nFOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) + Lat/Lon (IBGE) \n")
print(focos_xy.info())
print("~"*80)
print(focos_xy.dtypes)
print("~"*80)
print(focos_xy)
print("~"*80)
print(f"\n{registro_municipios} MUNICÍPIOS COM ALGUM REGISTRO DE FOCO DE _Aedes aegypti_ATÉ {ultimo_registro} EM SC.\n")
print(focos_xy["Município"].unique())
print("="*80)

print("\n \nFOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) + Lat/Lon (IBGE) \n")
print(focos_pivot.info())
print("~"*80)
print(focos_pivot.dtypes)
print("~"*80)
print(focos_pivot)
print("="*80)
