## Arquivos Correlatos
#from verivalida import Modelo
#from verivalida.Modelo import monta_dataset_casos, monta_dataset_focos

### Bibliotecas Correlatas
import matplotlib.pyplot as plt               
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm
### Suporte
import sys

### Condições para Variar #######################################################

_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"

_RETROAGIR = 12 # Semanas Epidemiológicas
_ANO = "2023"
_CIDADE = "Florianópolis"
_CIDADE = _CIDADE.upper()
_METODO = "pearson" # "spearman" # "kendall"

##### Padrão ANSI ##################################
ansi = {"bold" : "\033[1m", "red" : "\033[91m",
        "green" : "\033[92m", "yellow" : "\033[33m",
        "blue" : "\033[34m", "magenta" : "\033[35m",
        "cyan" : "\033[36m", "white" : "\033[37m", "reset" : "\033[0m"}
#################################################################################

### Encaminhamento aos Diretórios
if _LOCAL == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _LOCAL == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
    caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos
casos = "casos_dive_pivot_total.csv"  # TabNet/DiveSC
#casos = "casos_pivot_pospandemia.csv" # TabNet/DataSUS
focos = "focos_pivot.csv"
unicos = "casos_unicos.csv"
prec = "prec_semana_ate_2023.csv"
tmin = "tmin_semana_ate_2023.csv"
tmed = "tmed_semana_ate_2023.csv"
tmax = "tmax_semana_ate_2023.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

#cbar = https://matplotlib.org/3.1.0/tutorials/colors/colorbar_only.html


dataset = tmin[["Semana"]].copy()
dataset["TMIN"] = tmin[_CIDADE].copy()
dataset["TMED"] = tmed[_CIDADE].copy()
dataset["TMAX"] = tmax[_CIDADE].copy()
dataset = dataset.merge(prec[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
dataset = dataset.merge(focos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
dataset.dropna(axis = 0, inplace = True)
dataset = dataset.iloc[:, :].copy()
dataset = dataset.merge(casos[["Semana", _CIDADE]], how = "left", on = "Semana").copy()
troca_nome = {f"{_CIDADE}_x" : "PREC", f"{_CIDADE}_y" : "FOCOS", f"{_CIDADE}" : "CASOS"}
dataset = dataset.rename(columns = troca_nome)
dataset.fillna(0, inplace = True)
if _ANO == "2023":
	dataset = dataset.iloc[-53:, :].copy()
elif _ANO == "2022":
	dataset = dataset.iloc[-105:-53, :].copy()
elif _ANO == "2021":
	dataset = dataset.iloc[-157:-105, :].copy()
elif _ANO == "2020":
	dataset = dataset.iloc[-209:-157, :].copy()
else:
	print(f"{ansi['red']}{_ANO} fora da abordagem desse roteiro!\n\n{ansi['cyan']}Por favor, recodifique-o ou utilize um dos seguintes anos:\n{ansi['green']}\n2020\n2021\n2022\n2023\n{ansi['reset']}")
	sys.exit()

#dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC", "FOCOS"], inplace = True)
dataset.dropna(inplace = True)
dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{_CIDADE}"
ordem_colunas = ["FOCOS", "CASOS", "TMIN", "TMED", "TMAX", "PREC"]  # Specify the desired order of columns
dataset = dataset.reindex(columns = ordem_colunas)


### Base e Clima (sem retroagir)
## 0 (testando arquivo.csv base)
print(f"\n \n MATRIZ DE CORRELAÇÃO ({_METODO.title()}; Base e Clima; sem retroagir [TESTE]) \n")
print(dataset.info())
print("~"*80)
print(dataset.dtypes)
print("~"*80)
print(dataset)
#sys.exit()
#

for r in range(1, _RETROAGIR + 1):
	#dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
	dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
	#dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
	dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
	#dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
	#dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
dataset.dropna(inplace = True)
#dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{_CIDADE}"
correlacao_dataset = dataset.corr(method = f"{_METODO}")
print("="*80)
print(f"Método de {_METODO.title()} \n", correlacao_dataset)
print("="*80)
fig, ax = plt.subplots(figsize = (10, 6), layout = "constrained", frameon = False)
sns.heatmap(correlacao_dataset, annot = True, cmap = "tab20c", linewidth = 0.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation = "horizontal")
fig.suptitle(f"MATRIZ DE CORRELAÇÃO* entre \n FOCOS, CASOS E VARIÁVEIS CLIMATOLÓGICAS EM {_CIDADE} \n *(Método de {_METODO.title()}; durante {_ANO}; retroagindo {_RETROAGIR} semanas)", weight = "bold", size = "medium")
#plt.savefig(f'{caminho_correlacao}correlacao_casos_{__CIDADE}_.pdf', format = "pdf", dpi = 1200,  bbox_inches = "tight", pad_inches = 0.0)
plt.show()


sys.exit()
