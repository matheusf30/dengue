### Bibliotecas Correlatas
# Básicas e Gráficas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
#import datetime
# Suporte
import os
import sys
import joblib
import webbrowser
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category = ShapelyDeprecationWarning)
# Pré-Processamento e Validações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
# Modelos
from sklearn.ensemble import RandomForestRegressor
# Mapas
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.patches as mpatches
#import tensorflow
#from tensorflow import keras
#from keras.models import load_model

### Encaminhamento aos Diretórios
_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _LOCAL == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
    caminho_modelos = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\modelos\\"
elif _LOCAL == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_shp = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
    caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos # TENTAR GFS
casos = "casos_dive_pivot_total.csv"
focos = "focos_pivot.csv"
prec = "prec_semana_ate_2023.csv"
tmin = "tmin_semana_ate_2023.csv"
tmed = "tmed_semana_ate_2023.csv"
tmax = "tmax_semana_ate_2023.csv"
unicos = "casos_primeiros.csv"
municipios = "SC_Municipios_2022.shp" # Shapefile não está carregando do GH
br = "BR_UF_2022.shp"

#### Condições para Variar ####################################

_AUTOMATIZA = True

_SALVAR = False

_VISUALIZAR = True

_RETROAGIR = 3

if _AUTOMATIZA == False:
    cidade = "Florianópolis"
    cidade = cidade.upper()

SEED = np.random.seed(0)


value_error = ["BOMBINHAS", "BALNEÁRIO CAMBORIÚ", "PORTO BELO"]
key_error = ["ABELARDO LUZ", "URUBICI", "RANCHO QUEIMADO"]

###############################################################

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
unicos = pd.read_csv(f"{caminho_dados}{unicos}")
municipios = gpd.read_file(f"{caminho_shp}{municipios}")
br = gpd.read_file(f"{caminho_shp}{br}")
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
cidades = unicos["Município"].copy()

not_found = list(cidades.iloc[151:])  # Desconsiderando 2023, pois ainda não há modelagem

# modelo = joblib.load(f"{caminho_modelos}RF_r{_RETROAGIR}_{cidade}.h5")

"""
### Pré-Processamento
_RETROAGIR = 8 # Semanas Epidemiológicas
cidade = "Florianópolis" #"Itajaí" "Joinville" "Chapecó" "Florianópolis" "Lages"
cidade = cidade.upper()
focos["Semana"] = pd.to_datetime(focos["Semana"])#, format="%Y%m%d")
casos["Semana"] = pd.to_datetime(casos["Semana"])
tmin["Semana"] = pd.to_datetime(tmin["Semana"])
prec["Semana"] = pd.to_datetime(prec["Semana"])
tmed["Semana"] = pd.to_datetime(tmed["Semana"])
tmax["Semana"] = pd.to_datetime(tmax["Semana"])

prec_cidade_2012 = prec[cidade].iloc[605: ]
cidades = focos.columns#.drop(columns = "Semana", inplace = True)
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]

xy = unicos.drop(columns = ["Semana", "Focos"])

### Montando Dataset
dataset = tmin[["Semana"]].copy()
dataset["TMIN"] = tmin[cidade].copy()
dataset["TMED"] = tmed[cidade].copy()
dataset["TMAX"] = tmax[cidade].copy()
dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS"}
dataset = dataset.rename(columns = troca_nome)


for r in range(1, _RETROAGIR + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)

for r in range(5, _RETROAGIR + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC"], inplace = True)

dataset.dropna(inplace = True)
dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{cidade}"

### Separando Dataset em X (explicativas) e Y (Dependentes)
SEED = np.random.seed(0)
x = dataset.drop(columns = "FOCOS")
y = dataset["FOCOS"]

x_array = x.to_numpy().astype(int)
y_array = y.to_numpy().astype(int)
x_array = x_array.reshape(x_array.shape[0], -1)

treino_x, teste_x, treino_y, teste_y = train_test_split(x_array, y_array,
                                                        random_state = SEED,
                                                        test_size = 0.2)#,
                                                      #stratify = y)
num_classes = len(np.unique(y_array))
print("Number of classes:", num_classes)
print(len(y_array))
### Normalizando/Escalonando Dataset_x
escalonador = StandardScaler()
escalonador.fit(treino_x)
treino_normal_x = escalonador.transform(treino_x)
teste_normal_x = escalonador.transform(teste_x)

### Exibindo Informações
print("\n \n CONJUNTO DE DADOS DE ENTRADA PARA PREVISÃO \n")
print(dataset.info())
print("~"*80)
#print(dataset.dtypes)
#print("~"*80)
print(dataset)
print("="*80)
"""
### Definindo Funções
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

def abre_modelo(cidade):
    troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
    for velho, novo in troca.items():
        cidade = cidade.replace(velho, novo)
    modelo = joblib.load(f"{caminho_modelos}RF_casos_r{_RETROAGIR}_{cidade}.h5")
    print(f"\n{green}MODELO RANDOM FOREST DE {cidade} ABERTO!\n\nCaminho e Nome:\n {caminho_modelos}RF_casos_r{_RETROAGIR}_{cidade}.h5{reset}")
    print("\n" + "="*80 + "\n")
    return modelo

def monta_dataset(cidade):
    dataset = tmin[["Semana"]].copy()
    dataset["TMIN"] = tmin[cidade].copy()
    dataset["TMED"] = tmed[cidade].copy()
    dataset["TMAX"] = tmax[cidade].copy()
    dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
    dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
    dataset.dropna(axis = 0, inplace = True)
    dataset = dataset.iloc[104:, :].copy()
    dataset = dataset.merge(casos[["Semana", cidade]], how = "left", on = "Semana").copy()
    troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS", f"{cidade}" : "CASOS"}
    dataset = dataset.rename(columns = troca_nome)
    dataset.fillna(0, inplace = True)
    for r in range(3, _RETROAGIR + 1):
        dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
        dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
        dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
        dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
        dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
        dataset[f"CASOS_r{r}"] = dataset["CASOS"].shift(-r)
    dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC", "FOCOS"], inplace = True)
    dataset.dropna(inplace = True)
    dataset.set_index("Semana", inplace = True)
    dataset.columns.name = f"{cidade}"
    x = dataset.drop(columns = "CASOS")
    y = dataset["CASOS"]
    return dataset, x, y

def treino_teste(dataset, cidade):
    SEED = np.random.seed(0)
    x = dataset.drop(columns = "CASOS")
    y = dataset["CASOS"]
    if x.empty or x.isnull().all().all():
        print(f"'X' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
        print(f"{cidade} possui um conjunto com erro:\n {x}")
        return None, None, None, None, None
    x = x.dropna()
    if x.empty:
        print(f"'X' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
        print(f"{cidade} possui um conjunto com erro:\n {x}")
        return None, None, None, None, None
    if y.empty or y.isnull().all().all():
        print(f"'Y' está vazio ou contém apenas valores 'NaN! Confira o dataset do município {cidade}!")
        print(f"{cidade} possui um conjunto com erro:\n {y}")
        return None, None, None, None, None
    y = y.dropna()
    if y.empty:
        print(f"'Y' continua vazio, mesmo removendo valores 'NaN'! Confira o dataset do município {cidade}!")
        print(f"{cidade} possui um conjunto com erro:\n {y}")
        return None, None, None, None, None
    x_array = x.to_numpy()
    x_array = x_array.reshape(x_array.shape[0], -1)
    x_array = x.to_numpy().astype(int)
    y_array = y.to_numpy().astype(int)
    x_array = x_array.reshape(x_array.shape[0], -1)

    treino_x, teste_x, treino_y, teste_y = train_test_split(x_array, y_array,
                                                        random_state = SEED,
                                                        test_size = 0.2)
    explicativas = x.columns.tolist()
    treino_x_explicado = pd.DataFrame(treino_x, columns = explicativas)
    treino_x_explicado = treino_x_explicado.to_numpy().astype(int)
    return treino_x, teste_x, treino_y, teste_y, treino_x_explicado

def escalona(treino_x, teste_x):
    escalonador = StandardScaler()
    escalonador.fit(treino_x)
    treino_normal_x = escalonador.transform(treino_x)
    teste_normal_x = escalonador.transform(teste_x)
    return treino_normal_x, teste_normal_x

def modela_treina_preve(treino_x, treino_y, teste_x, SEED):
    modelo = RandomForestRegressor(n_estimators = 100, random_state = SEED)
    modelo.fit(treino_x_explicado, treino_y)
    y_previsto = modelo.predict(teste_x)
    previsoes = modelo.predict(x)
    previsoes = [int(p) for p in previsoes]
    return modelo, y_previsto, previsoes

def preve(modelo, x, treino_x_explicado):
    y_previsto = modelo.predict(treino_x_explicado)
    previsoes = modelo.predict(x)
    previsoes = [int(p) for p in previsoes]
    return previsoes, y_previsto

def metricas(dataset, previsoes, n, y):
    nome_modelo = "Random Forest"
    print("="*80)
    print(f"\n{nome_modelo.upper()} - {cidade}\n")
    lista_op = [f"Focos: {dataset['CASOS'][i]}\nPrevisão {nome_modelo}: {previsoes[i]}\n" for i in range(n)]
    print("\n".join(lista_op))
    print("~"*80)
    EQM = mean_squared_error(y, previsoes)
    RQ_EQM = np.sqrt(EQM)
    R_2 = r2_score(y, previsoes).round(2)
    print(f"""
         \n MÉTRICAS {nome_modelo.upper()} - {cidade}
         \n Erro Quadrático Médio: {EQM}
         \n Coeficiente de Determinação (R²): {R_2}
         \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
         """)
    print("="*80)
    return EQM, RQ_EQM, R_2

def grafico(previsoes, R_2):
    final = pd.DataFrame()
    final["Semana"] = casos["Semana"]
    final["Casos"] = casos[cidade]
    #final.drop([d for d in range(_RETROAGIR)], axis=0, inplace = True)
    #final.drop(final.index[-_RETROAGIR + 4:], axis=0, inplace = True)
    final.drop(1, axis=0, inplace = True)
    """
    previsoes = previsao
    previsoes = previsoes[:len(final)]
    """
    final["Previstos"] = previsoes
    final["Semana"] = pd.to_datetime(final["Semana"])
    print(final)
    print("="*80)
    sns.lineplot(x = final["Semana"], y = final["Casos"], # linestyle = "--" linestyle = "-."
                 color = "darkblue", linewidth = 1, label = "Observado")
    sns.lineplot(x = final["Semana"], y = final["Previstos"],
                 color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
    plt.title(f"MODELO RANDOM FOREST (R²: {R_2}): OBSERVAÇÃO E PREVISÃO.\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
    plt.xlabel("Semanas Epidemiológicas na Série de Anos")
    plt.ylabel("Número de Focos de _Aedes_ sp.")
    plt.show()

def previsao_metricas(dataset, previsoes, n, teste_y, y_previsto):
    nome_modelo = "Random Forest"
    print("="*80)
    print(f"\n{nome_modelo.upper()} - {cidade}\n")
    lista_op = [f"Focos: {dataset['CASOS'][i]}\nPrevisão {nome_modelo}: {previsoes[i]}\n" for i in range(n)]
    print("\n".join(lista_op))
    print("~"*80)
    EQM = mean_squared_error(teste_y, y_previsto)
    RQ_EQM = np.sqrt(EQM)
    R_2 = r2_score(teste_y, y_previsto).round(2)
    print(f"""
         \n MÉTRICAS {nome_modelo.upper()} - {cidade}
         \n Erro Quadrático Médio: {EQM}
         \n Coeficiente de Determinação (R²): {R_2}
         \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM}
         """)
    print("="*80)
    return EQM, RQ_EQM, R_2

def grafico_previsao(previsao, teste, string_modelo):
    if string_modelo not in ["RF", "NN"]:
        print("!!"*80)
        print("\n   MODELO NÃO RECONHECIDO\n   TENTE 'RF' PARA RANDOM FOREST\n   OU 'NN' PARA REDE NEURAL\n")
        print("!!"*80)
        sys.exit()
    # Gráfico de Comparação entre Observação e Previsão dos Modelos
    nome_modelo = "Random Forest" if string_modelo == "RF" else "Rede Neural"
    final = pd.DataFrame()
    final["Semana"] = focos["Semana"]
    final["Casos"] = focos[cidade]
    final.drop([d for d in range(_RETROAGIR)], axis=0, inplace = True)
    final.drop(final.index[-_RETROAGIR:], axis=0, inplace = True)
    previsoes = previsao if string_modelo == "RF" else [np.argmax(p) for p in previsao]
    """
    lista_previsao = [previsoes[v] for v in range(len(previsoes))]
    final["Previstos"] = lista_previsao
    """
    previsoes = previsoes[:len(final)]
    final["Previstos"] = previsoes
    final["Semana"] = pd.to_datetime(final["Semana"])
    print(final)
    print("="*80)
    sns.lineplot(x = final["Semana"], y = final["Casos"], # linestyle = "--" linestyle = "-."
                 color = "darkblue", linewidth = 1, label = "Observado")
    sns.lineplot(x = final["Semana"], y = final["Previstos"],
                 color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
    plt.title(f"MODELO {nome_modelo.upper()} (R²: {R_2}): OBSERVAÇÃO E PREVISÃO.\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
    plt.xlabel("Semanas Epidemiológicas na Série de Anos")
    plt.ylabel("Número de Casos de Dengue")
    plt.show()

def salva_modelo(modelo, cidade):
    troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
    for velho, novo in troca.items():
        cidade = cidade.replace(velho, novo)
    joblib.dump(modelo, f"{caminho_modelos}RF_r{_RETROAGIR}_{cidade}.h5")
    print(f"{green}\nMODELO RANDOM FOREST DE {cidade} SALVO!\n\nCaminho e Nome:\n {caminho_modelos}RF_r{_RETROAGIR}_{cidade}.h5{reset}")
    print("\n" + "="*80 + "\n")

######################################################MODELAGEM############################################################

### Exibindo Informações, Gráficos e Métricas
#previsao_total = []
previsao_total = pd.DataFrame()
previsao_total["Semana"] = casos["Semana"].copy() #pd.date_range(start = "2014-01-05", end = "2022-12-25", freq = "W")
previsao_total["Semana"] = pd.to_datetime(previsao_total["Semana"])
previsao_total.drop(1, axis = 0, inplace = True)
#previsao_total.drop([d for d in range(_RETROAGIR)], axis = 0, inplace = True)
#previsao_total.drop(previsao_total.index[-_RETROAGIR:], axis = 0, inplace = True)

if _AUTOMATIZA == True:
    for cidade in cidades:
        if cidade in value_error:
            print(f"\n{red}Modelo para {cidade} não está no diretório!\n{yellow}ValueError\n{cyan}Por favor, entre em contato para resolver o problema!{reset}\n")
        elif cidade in key_error:
            print(f"\n{red}Modelo para {cidade} não está no diretório!\n{yellow}KeyError\n{cyan}Por favor, entre em contato para resolver o problema!{reset}\n")
        elif cidade in not_found:
            print(f"\n{red}Modelo para {cidade} não está no diretório!\n{yellow}NotFound\n{cyan}Por favor, entre em contato para resolver o problema!{reset}")
            print(f"{magenta}FileNotFoundError: [Errno 2] No such file or directory: '/home/sifapsc/scripts/matheus/dados_dengue/modelos/'{reset}\n")
        else:
            modelo = abre_modelo(cidade)
            dataset, x, y = monta_dataset(cidade)
            treino_x, teste_x, treino_y, teste_y, treino_x_explicado = treino_teste(dataset, cidade)
            previsoes, y_previsto = preve(modelo, x, treino_x_explicado)
            EQM, RQ_EQM, R_2 = metricas(dataset, previsoes, 5, y)
            previsao_total[cidade] = previsoes
            
else:
    modelo = abre_modelo(cidade)
    dataset, x, y = monta_dataset(cidade)
    treino_x, teste_x, treino_y, teste_y, treino_x_explicado = treino_teste(dataset, cidade)
    previsoes, y_previsto = preve(modelo, x, treino_x_explicado)
    EQM, RQ_EQM, R_2 = metricas(dataset, previsoes, 5, y)
    previsao_total[cidade] = previsoes
    grafico(previsoes, R_2)

previsao_melt = pd.melt(previsao_total, id_vars = ["Semana"], 
                        var_name = "Município", value_name = "Casos")
#value_vars - If not specified, uses all columns that are not set as id_vars.
previsao_melt = previsao_melt.sort_values(by = "Semana")
xy = unicos.drop(columns = ["Semana", "Casos"])
previsao_melt_xy = pd.merge(previsao_melt, xy, on = "Município", how = "left")
geometry = [Point(xy) for xy in zip(previsao_melt_xy["longitude"], previsao_melt_xy["latitude"])]
previsao_melt_geo = gpd.GeoDataFrame(previsao_melt_xy, geometry = geometry, crs = "EPSG:4674")
previsao_melt_geo = previsao_melt_geo[["Semana", "Município", "Casos", "geometry"]]
previsao_melt_geo["Semana"] = pd.to_datetime(previsao_melt_geo["Semana"])
print(f"{green}Caminho e Nome do arquivo:\n{caminho_modelos}RF_r{_RETROAGIR}_{cidade}.h5{reset}")



### Cartografia
# Semana Epidemiológica
semana_epidemio = "2023-04-16"
# "2020-04-19" "2021-04-18" "2022-04-17" "2023-04-16"

# SC_Pontos
#previsao_melt_geo = gpd.GeoDataFrame(previsao_melt_geo)#, geometry = municipios.geometry)
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(-48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
municipios.plot(ax = ax, color = "lightgreen", edgecolor = "black")
previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio ].plot(ax = ax, column = "Casos",  legend = True,
                                                                        label = "Casos", cmap = "YlOrRd", markersize = 50)
zero = previsao_melt_geo[previsao_melt_geo["Casos"] == 0]
zero[zero["Semana"] == semana_epidemio].plot(ax = ax, column = "Casos", legend = False,
                                             label = "Casos", cmap = "YlOrBr")
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Casos de Dengue Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.", fontsize = 18)
plt.grid(True)
if _AUTOMATIZA == True and _SALVAR == True:
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/pontual/"
	os.makedirs(caminho_resultados, exist_ok = True)
	plt.savefig(f"{caminho_resultados}CASOS_mapa_pontual_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
	print(f"\n\n{green}{caminho_resultados}\nCASOS_mapa_pontual_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
if _AUTOMATIZA == True and _VISUALIZAR == True:
	print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\nCASOS_mapa_pontual_{semana_epidemio}.pdf\n{reset}\n\n")
	plt.show()
	print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\nCASOS_mapa_pontual_{semana_epidemio}.pdf\n{reset}\n\n")

# SC_MapaCalor
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(- 48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
sns.kdeplot(data = previsao_melt_xy[previsao_melt_xy["Semana"] == semana_epidemio],
            x = "longitude", y = "latitude", legend = True, ax = plt.gca(), weights = "Casos",
            fill = True, cmap = "YlOrRd", levels = previsao_melt_xy["Casos"].max(), alpha = 0.5)
municipios.plot(ax = plt.gca(), color = "lightgreen", edgecolor = "black", alpha = 0.3)
cbar = plt.cm.ScalarMappable(cmap="YlOrRd") #.gca() get current axis
cbar.set_array(previsao_melt_xy["Casos"])
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
plt.colorbar(cbar, ax = plt.gca(), label="Casos")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"""Mapa de Densidade de Kernel dos Casos de Dengue Previstos.
Santa Catarina, Semana Epidemiológica: {semana_epidemio}.""", fontsize = 18)
plt.grid(True)
if  _AUTOMATIZA == True and _SALVAR == True:
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/densidade/"
	os.makedirs(caminho_resultados, exist_ok = True)
	plt.savefig(f"{caminho_resultados}CASOS_mapa_densidade_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
	print(f"\n\n{green}{caminho_resultados}\nCASOS_mapa_densidade_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
if _AUTOMATIZA == True and _VISUALIZAR == True:
	print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\nCASOS_mapa_densidade_{semana_epidemio}.pdf\n{reset}\n\n")
	plt.show()
	print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\nCASOS_mapa_densidade_{semana_epidemio}.pdf\n{reset}\n\n")

# SC_Coroplético
xy = municipios.copy()
xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
xy = xy.rename(columns = {"NM_MUN" : "Município"})
xy["Município"] = xy["Município"].str.upper() 
previsao_melt_poli = pd.merge(previsao_melt, xy, on = "Município", how = "left")
previsao_melt_poligeo = gpd.GeoDataFrame(previsao_melt_poli, geometry = "geometry", crs = "EPSG:4674")
fig, ax = plt.subplots(figsize = (20, 12), layout = "constrained", frameon = False)
coord_atlantico = [(-54, -30),(-48, -30),
                   (-48, -25),(-54, -25),
                   (-54, -30)]
atlantico_poly = Polygon(coord_atlantico)
atlantico = gpd.GeoDataFrame(geometry = [atlantico_poly])
atlantico.plot(ax = ax, color = "lightblue") # atlantico ~ base
ax.set_aspect("auto")
coord_arg = [(-55, -30),(-52, -30),
             (-52, -25),(-55, -25),
             (-55, -30)]
arg_poly = Polygon(coord_arg)
argentina = gpd.GeoDataFrame(geometry = [arg_poly])
argentina.plot(ax = ax, color = "tan")
br.plot(ax = ax, color = "tan", edgecolor = "black")
municipios.plot(ax = ax, color = "lightgray", edgecolor = "lightgray")
previsao_melt_poligeo[previsao_melt_poligeo["Semana"] == semana_epidemio].plot(ax = ax, column = "Casos",  legend = True,
                                                                               label = "Casos", cmap = "YlOrRd")
zero = previsao_melt_poligeo[previsao_melt_poligeo["Casos"] == 0]
zero[zero["Semana"] == semana_epidemio].plot(ax = ax, column = "Casos", legend = False,
                                             label = "Casos", cmap = "YlOrBr")
plt.xlim(-54, -48)
plt.ylim(-29.5, -25.75)
x_tail = -48.5
y_tail = -29.25
x_head = -48.5
y_head = -28.75
arrow = mpatches.FancyArrowPatch((x_tail, y_tail), (x_head, y_head),
                                 mutation_scale = 50, color = "darkblue")
ax.add_patch(arrow)
mid_x = (x_tail + x_head) / 2
mid_y = (y_tail + y_head) / 2
ax.text(mid_x, mid_y, "N", color = "white", ha = "center", va = "center",
        fontsize = "large", fontweight = "bold")
ax.text(-52.5, -29, "Sistema de Referência de Coordenadas\nDATUM: SIRGAS 2000/22S.\nBase Cartográfica: IBGE, 2022.",
        color = "white", backgroundcolor = "darkgray", ha = "center", va = "center", fontsize = 14)
ax.text(-52.5, -28.25, """LEGENDA

▢           Sem registro*

*Não há registro oficial ou
modelagem inexistente.""",
        color = "black", backgroundcolor = "lightgray", ha = "center", va = "center", fontsize = 14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Casos de Dengue Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.", fontsize = 18)
plt.grid(True)
if _AUTOMATIZA == True and _SALVAR == True:
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/coropletico/"
	os.makedirs(caminho_resultados, exist_ok = True)
	plt.savefig(f"{caminho_resultados}CASOS_mapa_coropletico_{semana_epidemio}.pdf", format = "pdf", dpi = 1200)
	print(f"\n\n{green}{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\nSALVO COM SUCESSO!{reset}\n\n")
if _AUTOMATIZA == True and _VISUALIZAR == True:	
	print(f"{cyan}\nVISUALIZANDO:\n{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\n{reset}\n\n")
	plt.show()
	print(f"{cyan}\nENCERRADO:\n{caminho_resultados}\nCASOS_mapa_coropletico_{semana_epidemio}.pdf\n{reset}\n\n")





