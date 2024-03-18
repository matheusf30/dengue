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
from shapely.geometry import Point
#import tensorflow
#from tensorflow import keras
#from keras.models import load_model

### Encaminhamento aos Diretórios
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"
_www = False
if _www == True: # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
else:
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n{caminho_modelos}")

### Renomeação das Variáveis pelos Arquivos # TENTAR GFS
casos = "casos_se.csv"
focos = "focos_pivot.csv"
prec = "merge_se.csv"
tmin = "tmin_se.csv"
tmed = "tmed_se.csv"
tmax = "tmax_se.csv"
unicos = "unicos_xy.csv"
municipios = "SC_Municipios_2022.shp"

#### Condições para Variar ####################################
_automatiza = True
_retroagir = 8
SEED = np.random.seed(0)
"""
if _automatiza == False:
    cidade = "FLORIANÓPOLIS"
else:
"""
value_error = ["BALNEÁRIO CAMBORIÚ", "BOMBINHAS", "PORTO BELO"]
key_error = ["ABELARDO LUZ", "ÁGUA DOCE", "AGROLÂNDIA", "AGRONÔMICA"]

###############################################################

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
unicos = pd.read_csv(f"{caminho_dados}{unicos}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")
cidades = unicos["Município"].copy()
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}


# modelo = joblib.load(f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")

"""
### Pré-Processamento
_retroagir = 8 # Semanas Epidemiológicas
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


for r in range(1, _retroagir + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)

for r in range(5, _retroagir + 1):
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
def abre_modelo(cidade):
    troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A', 'Ä': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E', 'Ë': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I', 'Ï': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O', 'Ö': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U', 'Ü': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
    for velho, novo in troca.items():
        cidade = cidade.replace(velho, novo)
    modelo = joblib.load(f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
    print(f"\nMODELO RANDOM FOREST DE {cidade} ABERTO!\n\nCaminho e Nome:\n {caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
    print("\n" + "="*80 + "\n")
    return modelo

def monta_dataset(cidade):
    dataset = tmin[["Semana"]].copy()
    dataset["TMIN"] = tmin[cidade].copy()
    dataset["TMED"] = tmed[cidade].copy()
    dataset["TMAX"] = tmax[cidade].copy()
    dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
    dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
    troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS"}
    dataset = dataset.rename(columns = troca_nome)
    for r in range(5, _retroagir + 1):
        dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
        dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
        dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
        dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
        dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
    dataset.drop(columns = ["TMIN", "TMED", "TMAX", "PREC"], inplace = True)
    dataset.dropna(inplace = True)
    dataset.set_index("Semana", inplace = True)
    dataset.columns.name = f"{cidade}"
    x = dataset.drop(columns = "FOCOS")
    y = dataset["FOCOS"]
    return dataset, x, y

def treino_teste(dataset, cidade):
    SEED = np.random.seed(0)
    x = dataset.drop(columns = "FOCOS")
    y = dataset["FOCOS"]
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
    previsoes = modeloRF.predict(x)
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
    lista_op = [f"Focos: {dataset['FOCOS'][i]}\nPrevisão {nome_modelo}: {previsoes[i]}\n" for i in range(n)]
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
    final["Semana"] = focos["Semana"]
    final["Focos"] = focos[cidade]
    final.drop([d for d in range(_retroagir)], axis=0, inplace = True)
    final.drop(final.index[-_retroagir + 4:], axis=0, inplace = True)
    """
    previsoes = previsao
    previsoes = previsoes[:len(final)]
    """
    final["Previstos"] = previsoes
    final["Semana"] = pd.to_datetime(final["Semana"])
    print(final)
    print("="*80)
    sns.lineplot(x = final["Semana"], y = final["Focos"], # linestyle = "--" linestyle = "-."
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
    lista_op = [f"Focos: {dataset['FOCOS'][i]}\nPrevisão {nome_modelo}: {previsoes[i]}\n" for i in range(n)]
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
    final["Focos"] = focos[cidade]
    final.drop([d for d in range(_retroagir)], axis=0, inplace = True)
    final.drop(final.index[-_retroagir:], axis=0, inplace = True)
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
    sns.lineplot(x = final["Semana"], y = final["Focos"], # linestyle = "--" linestyle = "-."
                 color = "darkblue", linewidth = 1, label = "Observado")
    sns.lineplot(x = final["Semana"], y = final["Previstos"],
                 color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
    plt.title(f"MODELO {nome_modelo.upper()} (R²: {R_2}): OBSERVAÇÃO E PREVISÃO.\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
    plt.xlabel("Semanas Epidemiológicas na Série de Anos")
    plt.ylabel("Número de Focos de _Aedes_ sp.")
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
    joblib.dump(modelo, f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
    print(f"\nMODELO RANDOM FOREST DE {cidade} SALVO!\n\nCaminho e Nome:\n {caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
    print("\n" + "="*80 + "\n")

######################################################MODELAGEM############################################################

### Exibindo Informações, Gráficos e Métricas
#previsao_total = []
previsao_total = pd.DataFrame()
previsao_total["Semana"] = focos["Semana"].copy()  #pd.date_range(start = "2012-01-01", end = "2022-12-25", freq = "W")
previsao_total["Semana"] = pd.to_datetime(previsao_total["Semana"])
previsao_total.drop([d for d in range(_retroagir)], axis=0, inplace = True)
previsao_total.drop(previsao_total.index[-_retroagir + 4:], axis=0, inplace = True)


if _automatiza == True:
    for cidade in cidades:
        if cidade in value_error:
            print(f"Modelo para {cidade} não está no diretório!\nPor favor, entre em contato para resolver o problema!")
        elif cidade in key_error:
            print(f"Modelo para {cidade} não está no diretório!\nPor favor, entre em contato para resolver o problema!")
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

previsao_melt = pd.melt(previsao_total, id_vars = ["Semana"], #value_vars - If not specified, uses all columns that are not set as id_vars.
                            var_name = "Município", value_name = "Focos")
previsao_melt = previsao_melt.sort_values(by = "Semana")

xy = unicos.drop(columns = ["Semana", "Focos"])
"""
xy = municipios.copy()
xy.drop(columns = ["CD_MUN", "SIGLA_UF", "AREA_KM2"], inplace = True)
xy = xy.rename(columns = {"NM_MUN" : "Município"})
xy["Município"] = xy["Município"].str.upper()
"""
previsao_melt = pd.merge(previsao_melt, xy, on = "Município", how = "left")
geometry = [Point(xy) for xy in zip(previsao_melt['longitude'], previsao_melt['latitude'])]
previsao_melt_geo = gpd.GeoDataFrame(previsao_melt, geometry = geometry, crs = "EPSG:4674")

print(f"Caminho e Nome do arquivo:\n{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
print(xy)
print(dataset)
print(municipios)
print(municipios.crs)
print(previsao_total)
print(previsao_melt)
print(previsao_melt_geo)

### Cartografia
semana_epidemio = "2022-04-17"
previsao_melt_geo = gpd.GeoDataFrame(previsao_melt_geo)#, geometry = municipios.geometry)

# Load the Natural Earth datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
coastline = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# Filter coastline for oceans
ocean = coastline[coastline['continent'] == 'Antarctica']
# Filter world for land
plt.figure(figsize=(20,12))
land = world[(world['continent'] != 'Antarctica') & (world['continent'] != 'Seven seas (open ocean)')]
base = land.plot(color="lightgreen", edgecolor="black")
terrain = land.boundary.plot(ax=base, color='gray')
ocean.plot(ax=base, color='lightblue')


municipios.plot(ax = base, color = "lightgreen", edgecolor = "black")
previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio ].plot(ax = base, column = "Focos",
                                                                    cmap = "YlOrRd", legend = True)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Focos de _Aedes_sp. Previstos em Santa Catarina na Semana Epidemiológica: {semana_epidemio}.")
plt.grid(True)
plt.show()

plt.figure(figsize=(20,12))
sns.kdeplot(data = previsao_melt_geo[previsao_melt_geo["Semana"] == semana_epidemio],
            x = "longitude", y = "latitude", legend = True,
            fill = True, cmap = "YlOrRd", levels = previsao_melt_geo["Focos"].max(), alpha = 1) #previsao_melt_geo["Focos"].max()
municipios.plot(ax = plt.gca(), color = "lightgreen", edgecolor = "black", alpha = 0.3)
cbar = plt.cm.ScalarMappable(cmap="YlOrRd")
cbar.set_array(previsao_melt_geo["Focos"])
plt.colorbar(cbar, ax = plt.gca(), label="Focos")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Mapa de Calor dos Focos de _Aedes_sp. Previstos.\n Santa Catarina, Semana Epidemiológica: {semana_epidemio}.")
plt.grid(True)
plt.show()
"""
ax = gplt.polyplot(municipios)
gplt.pointplot(previsao_melt[Focos[previsao_focos["Semana"["Semana" == 2022-11-27]]]], ax=ax)

for cidade in _cidades:
	#cidade = cidade.upper()
	modeloRF = modelo(cidade)
	y_previstoRF = modeloRF.predict(x)
	EQM_RF = mean_squared_error(y, y_previstoRF)
	RQ_EQM_RF = np.sqrt(EQM_RF)
	R_2 = r2_score(y, y_previstoRF).round(2) 
	previsoesRF = [int(p) for p in y_previstoRF]
	#previsao_total.append({f"{cidade}" : previsoesRF})
	#previsao_total = pd.DataFrame(previsao_total)
	previsao_total[cidade] = previsoesRF
"""
sys.exit()





