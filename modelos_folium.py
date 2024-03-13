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
# Pré-Processamento e Validações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
# Modelos
from sklearn.ensemble import RandomForestRegressor
# Mapas
import folium
from folium.plugins import HeatMapWithTime
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
municipios = "unicos_xy.csv"
 

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
municipios = pd.read_csv(f"{caminho_dados}{municipios}")

#cidades = ["Itajaí", "Joinville", "Chapecó", "Florianópolis", "Lages", "Itá", "Grão-Pará"]
_cidades = municipios["Município"].copy()
troca = {'Á': 'A', 'Â': 'A', 'À': 'A', 'Ã': 'A',
         'É': 'E', 'Ê': 'E', 'È': 'E', 'Ẽ': 'E',
         'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ĩ': 'I',
         'Ó': 'O', 'Ô': 'O', 'Ò': 'O', 'Õ': 'O',
         'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ũ': 'U',
         'Ç': 'C', " " : "_", "'" : "_", "-" : "_"}
for velho, novo in troca.items():
    _cidades = _cidades.replace(velho, novo)
"""
for cidade in _cidades:
    cidade = cidade.upper()
    modelo_{cidade} = joblib.load(f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")

#modelo = joblib.load('random_forest.h5')
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
"""
prec_cidade_2012 = prec[cidade].iloc[605: ]
cidades = focos.columns#.drop(columns = "Semana", inplace = True)
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]
"""
xy = municipios.drop(columns = ["Semana", "Focos"])

### Montando Dataset
dataset = tmin[["Semana"]].copy()
dataset["TMIN"] = tmin[cidade].copy()
dataset["TMED"] = tmed[cidade].copy()
dataset["TMAX"] = tmax[cidade].copy()
dataset = dataset.merge(prec[["Semana", cidade]], how = "left", on = "Semana").copy()
dataset = dataset.merge(focos[["Semana", cidade]], how = "left", on = "Semana").copy()
troca_nome = {f"{cidade}_x" : "PREC", f"{cidade}_y" : "FOCOS"}
dataset = dataset.rename(columns = troca_nome)

"""
for r in range(1, _retroagir + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
"""
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
"""
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
"""
### Exibindo Informações
print("\n \n CONJUNTO DE DADOS \n")
print(dataset.info())
print("~"*80)
#print(dataset.dtypes)
#print("~"*80)
print(dataset)
print("="*80)

### Definindo Funções
def modelo(cidade):
    cidade = cidade.upper()
    modeloRF = joblib.load(f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
    return modeloRF

def lista_previsao(previsao, n, string_modelo):
    if string_modelo not in ["RF", "NN"]:
        print("!!"*80)
        print("\n   MODELO NÃO RECONHECIDO\n   TENTE 'RF' PARA RANDOM FOREST\n   OU 'NN' PARA REDE NEURAL\n")
        print("!!"*80)
        sys.exit()
    nome_modelo = "Random Forest" if string_modelo == "RF" else "Rede Neural"
    previsoes = previsao if string_modelo == "RF" else [np.argmax(p) for p in previsao]
    print("="*80)
    print(f"\n{nome_modelo.upper()}\n")
    lista_op = [f"Focos: {dataset['FOCOS'][i]}\nPrevisão {nome_modelo}: {previsoes[i]}\n" for i in range(n)]
    print("\n".join(lista_op))
    print("="*80)

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
                 color = "red", alpha = 0.75, linewidth = 1, label = "Previsto")
    plt.title(f"MODELO {nome_modelo.upper()} (R²: {R_2}): OBSERVAÇÃO E PREVISÃO.\n MUNICÍPIO DE {cidade}, SANTA CATARINA.")
    plt.xlabel("Semanas Epidemiológicas na Série de Anos")
    plt.ylabel("Número de Focos de _Aedes_ sp.")
    plt.show()
    # Gráfico de Validação do Modelo Rede Neural
    if string_modelo == "NN":  
        plt.plot(valida.history["accuracy"])
        plt.plot(valida.history["val_accuracy"])
        plt.plot(valida.history["loss"])
        plt.plot(valida.history["val_loss"])
        plt.title("VALIDAÇÃO DO MODELO - TREINO (CICLOS x ACURÁCIA/PERDA)")
        plt.xlabel("Ciclos de Treino (epochs)")
        plt.ylabel("Perda e Acurácia")
        plt.legend(["Acurácia_Treino", "Acurácia_Validação", "Perda_Treino", "Perda_Validação"])
        plt.show()

def metricas(string_modelo, modeloNN = None):
    if string_modelo not in ["RF", "NN"]:
        print("!!"*80)
        print("\n   MODELO NÃO RECONHECIDO\n   TENTE 'RF' PARA RANDOM FOREST\n   OU 'NN' PARA REDE NEURAL\n")
        print("!!"*80)
        sys.exit()
    elif string_modelo == "NN":
        if modeloNN is None:
            print("!!"*80)
            raise ValueError("'modeloNN' não foi fornecido para a função metricas() do modelo de rede neural!")
        else:
            sumario = []
            modeloNN.summary(print_fn = lambda x: sumario.append(x))
            sumario = "\n".join(sumario)
            print(f"\n MÉTRICAS REDE NEURAL\n \n {sumario}")
    else:
        print(f"""
             \n MÉTRICAS RANDOM FOREST
             \n Erro Quadrático Médio: {EQM_RF}
             \n Coeficiente de Determinação (R²): {R_2}
             \n Raiz Quadrada do Erro Quadrático Médio: {RQ_EQM_RF}
              """)

######################################################RANDOM_FOREST############################################################
"""
### Instanciando e Treinando Modelo Regressor Random Forest
explicativas = x.columns.tolist() # feature_names = explicativas
modeloRF = RandomForestRegressor(n_estimators = 100, random_state = SEED) #n_estimators = número de árvores
modeloRF.fit(treino_x, treino_y)

### Testando e Avaliando
y_previstoRF = modeloRF.predict(teste_x)
EQM_RF = mean_squared_error(teste_y, y_previstoRF)
RQ_EQM_RF = np.sqrt(EQM_RF)
R_2 = r2_score(teste_y, y_previstoRF).round(2) 
#acuraciaRF = accuracy_score(teste_y, y_previstoRF)
#print(f"A acurácia foi {acuraciaRF.round(2)}%. (Random Forest)")

### Abrindo, Testando e Validando Modelo
for cidade in cidades:
    cidades
previsoesRF = modeloRF.predict(x)
previsoesRF = [int(p) for p in previsoesRF]
EQM_RF = mean_squared_error(y, y_previstoRF)
RQ_EQM_RF = np.sqrt(EQM_RF)
R_2 = r2_score(y, y_previstoRF).round(2)
"""
### Exibindo Informações, Gráficos e Métricas
#previsao_total = []
previsao_total = pd.DataFrame()
previsao_total["Semana"] = focos["Semana"].copy()  #pd.date_range(start = "2012-01-01", end = "2022-12-25", freq = "W")
previsao_total["Semana"] = pd.to_datetime(previsao_total["Semana"])
previsao_total.drop([d for d in range(_retroagir)], axis=0, inplace = True)
previsao_total.drop(previsao_total.index[-_retroagir + 4:], axis=0, inplace = True)

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

previsao_melt = pd.melt(previsao_total, id_vars = ["Semana"], #value_vars - If not specified, uses all columns that are not set as id_vars.
                        var_name = "Município", value_name = "Focos") 
previsao_melt = previsao_melt.sort_values(by = "Semana")
previsao_melt = pd.merge(previsao_melt, xy, on = "Município", how = "left")
#previsao_melt = previsao_melt[["Semana", "Município", "Focos", "latitude", "longitude"]]

lista_previsao(previsoesRF, 5, "RF")
grafico_previsao(previsoesRF, y, "RF")
metricas("RF")
print(f"Caminho e Nome do arquivo:\n{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
print(previsao_total)
print(previsao_melt)
print(xy)


### Instanciando Mapa e HeatMapWithTime
dados_heatmap = []
for index, linha in previsao_melt.iterrows():
    dados_heatmap.append([linha["latitude"], linha["longitude"], linha["Focos"]])
mapa = folium.Map(location = [previsao_melt["latitude"].mean(), previsao_melt["longitude"].mean()],
                  tiles = "cartodbdark_matter", zoom_start=8)
HeatMapWithTime(dados_heatmap, auto_play = True, speed_step = 0.2, #index = focos["Semana"],
                gradient = {0.1: "blue", 0.2: "lime",
                            0.4: "yellow", 0.6: "orange",
                            0.8: "red", 0.99: "purple"},
                min_opacity = 0.5, max_opacity = 0.8,# use_local_extrema = False,
                index = previsao_melt["Semana"].astype(str)).add_to(mapa)
mapa.save(f"{caminho_dados}focos_previstos.html")
mapa.show_in_browser()
#webbrowser.open(f"file://{caminho_dados}focos_previstos.html")
"""
import os
import webbrowser
filepath = 'C:/whatever/map.html'
m = folium.Map()
m.save(filepath)
webbrowser.open('file://' + filepath)


### Salvando Modelo (e abrindo)
# HDF5 (Hierarchical Data Format version 5) files
# Which are used to store and organize large amounts of data.
os.makedirs(caminho_modelos, exist_ok=True)
joblib.dump(modeloRF, f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
#modelo = joblib.load('random_forest.h5')
"""
sys.exit()

######################################################NEURAL_NETWORK############################################################
# https://www.semanticscholar.org/paper/Recurrent-Neural-Networks-for-Time-Series-Petneh%C3%A1zi/ed4a2a2ed51cc7418c2d1ca8967cc7a383c0241a

### Instanciando e Compilando Modelo de Rede Neural
modeloNN = keras.Sequential([
    #keras.layers.LSTM(64, input_shape = (1, 1), return_sequences = True), #entrada Memória de Longo Prazo
    keras.layers.Flatten(input_shape = treino_x.shape[1:]), #entrada. #Camada 0 <<< input_shape = treino_x.shape[1:]
    #keras.layers.GRU(64, input_shape = ??? ), #CAMADA 1 Unidade Recorrente Fechada
    keras.layers.Dense(10, activation = tensorflow.nn.relu), #processamento. #Camada 1
    #keras.layers.Dense(128, activation = tensorflow.nn.relu), #processamento. #Camada 2
    keras.layers.Dense(10, activation = tensorflow.nn.relu), #processamento. #Camada 3
    keras.layers.Dropout(0.2), # ~Normalização (processamento) #Camada 4
    keras.layers.Dense(len(y_array), activation = tensorflow.nn.softmax)]) #saida. #Camada 5

lr_adam = keras.optimizers.Adam(learning_rate = 0.01)
callbacks = [keras.callbacks.EarlyStopping(monitor = "val_loss")]#,
"""
             keras.callbacks.ModelCheckpoint(filepath = f"{caminho_dados}melhor_modeloNN.h5",
                                             monitor = "val_loss", save_best = True)]
"""
modeloNN.compile(optimizer = lr_adam, #"adam",
               loss = "sparse_categorical_crossentropy",
               metrics = ["accuracy"])

### Testando e Validando Modelo
valida = modeloNN.fit(treino_x, treino_y,
                      epochs = 100, validation_split = 0.2,
                      callbacks = callbacks)#, batch_size = 10000)
testesNN = modeloNN.predict(teste_x)
#testes_normal = modeloNN.predict(teste_normal_x)
previsoesNN = modeloNN.predict(x)
sumarioNN = modeloNN.summary()

### Exibindo Informações, Gráficos e Métricas
lista_previsao(previsoesNN, 5, "NN")
grafico_previsao(previsoesNN, testesNN, "NN")
metricas("NN", modeloNN)
"""
### Salvando Modelo (e abrindo)
model.save(modeloRF, f"{caminho_modelos}NN_{cidade}.h5")
#modelo = joblib.load('keras_neural_network.hdf5')
modelo = load_model('keras_neural_net.h5')

_UPPER = {'ABDON_BATISTA': 'ABDON BATISTA',
  'ABELARDO_LUZ': 'ABELARDO LUZ',
  'AGROLANDIA': 'AGROLÂNDIA',
  'AGRONOMICA': 'AGRONÔMICA',
  'AGUA_DOCE': 'ÁGUA DOCE',
  'AGUAS_DE_CHAPECO': 'ÁGUAS DE CHAPECÓ',
  'AGUAS_FRIAS': 'ÁGUAS FRIAS',
  'AGUAS_MORNAS': 'ÁGUAS MORNAS',
  'ALFREDO_WAGNER': 'ALFREDO WAGNER',
  'ALTO_BELA_VISTA': 'ALTO BELA VISTA',
  'ANCHIETA': 'ANCHIETA',
  'ANGELINA': 'ANGELINA',
  'ANITA_GARIBALDI': 'ANITA GARIBALDI',
  'ANITAPOLIS': 'ANITÁPOLIS',
  'ANTONIO_CARLOS': 'ANTÔNIO CARLOS',
  'APIUNA': 'APIÚNA',
  'ARABUTA': 'ARABUTÃ',
  'ARAQUARI': 'ARAQUARI',
  'ARARANGUA': 'ARARANGUÁ',
  'ARMAZEM': 'ARMAZÉM',
  'ARROIO_TRINTA': 'ARROIO TRINTA',
  'ARVOREDO': 'ARVOREDO',
  'ASCURRA': 'ASCURRA',
  'ATALANTA': 'ATALANTA',
  'AURORA': 'AURORA',
  'BALNEARIO_ARROIO_DO_SILVA': 'BALNEÁRIO ARROIO DO SILVA',
  'BALNEARIO_CAMBORIU': 'BALNEÁRIO CAMBORIÚ',
  'BALNEARIO_BARRA_DO_SUL': 'BALNEÁRIO BARRA DO SUL',
  'BALNEARIO_GAIVOTA': 'BALNEÁRIO GAIVOTA',
  'BANDEIRANTE': 'BANDEIRANTE',
  'BARRA_BONITA': 'BARRA BONITA',
  'BARRA_VELHA': 'BARRA VELHA',
  'BELA_VISTA_DO_TOLDO': 'BELA VISTA DO TOLDO',
  'BELMONTE': 'BELMONTE',
  'BENEDITO_NOVO': 'BENEDITO NOVO',
  'BIGUACU': 'BIGUAÇU',
  'BLUMENAU': 'BLUMENAU',
  'BOCAINA_DO_SUL': 'BOCAINA DO SUL',
  'BOMBINHAS': 'BOMBINHAS',
  'BOM_JARDIM_DA_SERRA': 'BOM JARDIM DA SERRA',
  'BOM_JESUS': 'BOM JESUS',
  'BOM_JESUS_DO_OESTE': 'BOM JESUS DO OESTE',
  'BOM_RETIRO': 'BOM RETIRO',
  'BOTUVERA': 'BOTUVERÁ',
  'BRACO_DO_NORTE': 'BRAÇO DO NORTE',
  'BRACO_DO_TROMBUDO': 'BRAÇO DO TROMBUDO',
  'BRUNOPOLIS': 'BRUNÓPOLIS',
  'BRUSQUE': 'BRUSQUE',
  'CACADOR': 'CAÇADOR',
  'CAIBI': 'CAIBI',
  'CALMON': 'CALMON',
  'CAMBORIU': 'CAMBORIÚ',
  'CAPAO_ALTO': 'CAPÃO ALTO',
  'CAMPO_ALEGRE': 'CAMPO ALEGRE',
  'CAMPO_BELO_DO_SUL': 'CAMPO BELO DO SUL',
  'CAMPO_ERE': 'CAMPO ERÊ',
  'CAMPOS_NOVOS': 'CAMPOS NOVOS',
  'CANELINHA': 'CANELINHA',
  'CANOINHAS': 'CANOINHAS',
  'CAPINZAL': 'CAPINZAL',
  'CAPIVARI_DE_BAIXO': 'CAPIVARI DE BAIXO',
  'CATANDUVAS': 'CATANDUVAS',
  'CAXAMBU_DO_SUL': 'CAXAMBU DO SUL',
  'CELSO_RAMOS': 'CELSO RAMOS',
  'CERRO_NEGRO': 'CERRO NEGRO',
  'CHAPADAO_DO_LAGEADO': 'CHAPADÃO DO LAGEADO',
  'CHAPECO': 'CHAPECÓ',
  'COCAL_DO_SUL': 'COCAL DO SUL',
  'CONCORDIA': 'CONCÓRDIA',
  'CORDILHEIRA_ALTA': 'CORDILHEIRA ALTA',
  'CORONEL_FREITAS': 'CORONEL FREITAS',
  'CORONEL_MARTINS': 'CORONEL MARTINS',
  'CORUPA': 'CORUPÁ',
  'CORREIA_PINTO': 'CORREIA PINTO',
  'CRICIUMA': 'CRICIÚMA',
  'CUNHA_PORA': 'CUNHA PORÃ',
  'CUNHATAO': 'CUNHATAÍ',
  'CURITIBANOS': 'CURITIBANOS',
  'DESCANSO': 'DESCANSO',
  'DIONOSIO_CERQUEIRA': 'DIONÍSIO CERQUEIRA',
  'DONA_EMMA': 'DONA EMMA',
  'DOUTOR_PEDRINHO': 'DOUTOR PEDRINHO',
  'ENTRE_RIOS': 'ENTRE RIOS',
  'ERMO': 'ERMO',
  'ERVAL_VELHO': 'ERVAL VELHO',
  'FAXINAL_DOS_GUEDES': 'FAXINAL DOS GUEDES',
  'FLOR_DO_SERTAO': 'FLOR DO SERTÃO',
  'FLORIANOPOLIS': 'FLORIANÓPOLIS',
  'FORMOSA_DO_SUL': 'FORMOSA DO SUL',
  'FORQUILHINHA': 'FORQUILHINHA',
  'FRAIBURGO': 'FRAIBURGO',
  'FREI_ROGERIO': 'FREI ROGÉRIO',
  'GALVAO': 'GALVÃO',
  'GAROPABA': 'GAROPABA',
  'GARUVA': 'GARUVA',
  'GASPAR': 'GASPAR',
  'GOVERNADOR_CELSO_RAMOS': 'GOVERNADOR CELSO RAMOS',
  'GRAO_PARA': 'GRÃO-PARÁ',
  'GRAVATAL': 'GRAVATAL',
  'GUABIRUBA': 'GUABIRUBA',
  'GUARACIABA': 'GUARACIABA',
  'GUARAMIRIM': 'GUARAMIRIM',
  'GUARUJA_DO_SUL': 'GUARUJÁ DO SUL',
  'GUATAMBU': 'GUATAMBÚ',
  'HERVAL_D_OESTE': "HERVAL D'OESTE",
  'IBIAM': 'IBIAM',
  'IBICARE': 'IBICARÉ',
  'IBIRAMA': 'IBIRAMA',
  'ICARA': 'IÇARA',
  'ILHOTA': 'ILHOTA',
  'IMARUO': 'IMARUÍ',
  'IMBITUBA': 'IMBITUBA',
  'IMBUIA': 'IMBUIA',
  'INDAIAL': 'INDAIAL',
  'IOMERE': 'IOMERÊ',
  'IPIRA': 'IPIRA',
  'IPORA_DO_OESTE': 'IPORÃ DO OESTE',
  'IPUACU': 'IPUAÇU',
  'IPUMIRIM': 'IPUMIRIM',
  'IRACEMINHA': 'IRACEMINHA',
  'IRANI': 'IRANI',
  'IRATI': 'IRATI',
  'IRINEOPOLIS': 'IRINEÓPOLIS',
  'ITA': 'ITÁ',
  'ITAIOPOLIS': 'ITAIÓPOLIS',
  'ITAJAO': 'ITAJAÍ',
  'ITAPEMA': 'ITAPEMA',
  'ITAPIRANGA': 'ITAPIRANGA',
  'ITAPOA': 'ITAPOÁ',
  'ITUPORANGA': 'ITUPORANGA',
  'JABORA': 'JABORÁ',
  'JACINTO_MACHADO': 'JACINTO MACHADO',
  'JAGUARUNA': 'JAGUARUNA',
  'JARAGUA_DO_SUL': 'JARAGUÁ DO SUL',
  'JARDINOPOLIS': 'JARDINÓPOLIS',
  'JOACABA': 'JOAÇABA',
  'JOINVILLE': 'JOINVILLE',
  'JOSE_BOITEUX': 'JOSÉ BOITEUX',
  'JUPIA': 'JUPIÁ',
  'LACERDOPOLIS': 'LACERDÓPOLIS',
  'LAGES': 'LAGES',
  'LAGUNA': 'LAGUNA',
  'LAJEADO_GRANDE': 'LAJEADO GRANDE',
  'LAURENTINO': 'LAURENTINO',
  'LAURO_MULLER': 'LAURO MÜLLER',
  'LEBON_REGIS': 'LEBON RÉGIS',
  'LEOBERTO_LEAL': 'LEOBERTO LEAL',
  'LINDOIA_DO_SUL': 'LINDÓIA DO SUL',
  'LONTRAS': 'LONTRAS',
  'LUIZ_ALVES': 'LUIZ ALVES',
  'LUZERNA': 'LUZERNA',
  'MACIEIRA': 'MACIEIRA',
  'MAFRA': 'MAFRA',
  'MAJOR_GERCINO': 'MAJOR GERCINO',
  'MAJOR_VIEIRA': 'MAJOR VIEIRA',
  'MARACAJA': 'MARACAJÁ',
  'MARAVILHA': 'MARAVILHA',
  'MAREMA': 'MAREMA',
  'MASSARANDUBA': 'MASSARANDUBA',
  'MATOS_COSTA': 'MATOS COSTA',
  'MELEIRO': 'MELEIRO',
  'MIRIM_DOCE': 'MIRIM DOCE',
  'MODELO': 'MODELO',
  'MONDAO': 'MONDAÍ',
  'MONTE_CARLO': 'MONTE CARLO',
  'MONTE_CASTELO': 'MONTE CASTELO',
  'MORRO_DA_FUMACA': 'MORRO DA FUMAÇA',
  'MORRO_GRANDE': 'MORRO GRANDE',
  'NAVEGANTES': 'NAVEGANTES',
  'NOVA_ERECHIM': 'NOVA ERECHIM',
  'NOVA_ITABERABA': 'NOVA ITABERABA',
  'NOVA_TRENTO': 'NOVA TRENTO',
  'NOVA_VENEZA': 'NOVA VENEZA',
  'NOVO_HORIZONTE': 'NOVO HORIZONTE',
  'ORLEANS': 'ORLEANS',
  'OTACOLIO_COSTA': 'OTACÍLIO COSTA',
  'OURO': 'OURO',
  'OURO_VERDE': 'OURO VERDE',
  'PAIAL': 'PAIAL',
  'PAINEL': 'PAINEL',
  'PALHOCA': 'PALHOÇA',
  'PALMA_SOLA': 'PALMA SOLA',
  'PALMEIRA': 'PALMEIRA',
  'PALMITOS': 'PALMITOS',
  'PAPANDUVA': 'PAPANDUVA',
  'PARAOSO': 'PARAÍSO',
  'PASSO_DE_TORRES': 'PASSO DE TORRES',
  'PASSOS_MAIA': 'PASSOS MAIA',
  'PAULO_LOPES': 'PAULO LOPES',
  'PEDRAS_GRANDES': 'PEDRAS GRANDES',
  'PENHA': 'PENHA',
  'PERITIBA': 'PERITIBA',
  'PESCARIA_BRAVA': 'PESCARIA BRAVA',
  'PETROLANDIA': 'PETROLÂNDIA',
  'BALNEARIO_PICARRAS': 'BALNEÁRIO PIÇARRAS',
  'PINHALZINHO': 'PINHALZINHO',
  'PINHEIRO_PRETO': 'PINHEIRO PRETO',
  'PIRATUBA': 'PIRATUBA',
  'PLANALTO_ALEGRE': 'PLANALTO ALEGRE',
  'POMERODE': 'POMERODE',
  'PONTE_ALTA': 'PONTE ALTA',
  'PONTE_ALTA_DO_NORTE': 'PONTE ALTA DO NORTE',
  'PONTE_SERRADA': 'PONTE SERRADA',
  'PORTO_BELO': 'PORTO BELO',
  'PORTO_UNIAO': 'PORTO UNIÃO',
  'POUSO_REDONDO': 'POUSO REDONDO',
  'PRAIA_GRANDE': 'PRAIA GRANDE',
  'PRESIDENTE_CASTELLO_BRANCO': 'PRESIDENTE CASTELLO BRANCO',
  'PRESIDENTE_GETULIO': 'PRESIDENTE GETÚLIO',
  'PRESIDENTE_NEREU': 'PRESIDENTE NEREU',
  'PRINCESA': 'PRINCESA',
  'QUILOMBO': 'QUILOMBO',
  'RANCHO_QUEIMADO': 'RANCHO QUEIMADO',
  'RIO_DAS_ANTAS': 'RIO DAS ANTAS',
  'RIO_DO_CAMPO': 'RIO DO CAMPO',
  'RIO_DO_OESTE': 'RIO DO OESTE',
  'RIO_DOS_CEDROS': 'RIO DOS CEDROS',
  'RIO_DO_SUL': 'RIO DO SUL',
  'RIO_FORTUNA': 'RIO FORTUNA',
  'RIO_NEGRINHO': 'RIO NEGRINHO',
  'RIO_RUFINO': 'RIO RUFINO',
  'RIQUEZA': 'RIQUEZA',
  'RODEIO': 'RODEIO',
  'ROMELANDIA': 'ROMELÂNDIA',
  'SALETE': 'SALETE',
  'SALTINHO': 'SALTINHO',
  'SALTO_VELOSO': 'SALTO VELOSO',
  'SANGAO': 'SANGÃO',
  'SANTA_CECOLIA': 'SANTA CECÍLIA',
  'SANTA_HELENA': 'SANTA HELENA',
  'SANTA_ROSA_DE_LIMA': 'SANTA ROSA DE LIMA',
  'SANTA_ROSA_DO_SUL': 'SANTA ROSA DO SUL',
  'SANTA_TEREZINHA': 'SANTA TEREZINHA',
  'SANTA_TEREZINHA_DO_PROGRESSO': 'SANTA TEREZINHA DO PROGRESSO',
  'SANTIAGO_DO_SUL': 'SANTIAGO DO SUL',
  'SANTO_AMARO_DA_IMPERATRIZ': 'SANTO AMARO DA IMPERATRIZ',
  'SAO_BERNARDINO': 'SÃO BERNARDINO',
  'SAO_BENTO_DO_SUL': 'SÃO BENTO DO SUL',
  'SAO_BONIFACIO': 'SÃO BONIFÁCIO',
  'SAO_CARLOS': 'SÃO CARLOS',
  'SAO_CRISTOVAO_DO_SUL': 'SÃO CRISTÓVÃO DO SUL',
  'SAO_DOMINGOS': 'SÃO DOMINGOS',
  'SAO_FRANCISCO_DO_SUL': 'SÃO FRANCISCO DO SUL',
  'SAO_JOAO_DO_OESTE': 'SÃO JOÃO DO OESTE',
  'SAO_JOAO_BATISTA': 'SÃO JOÃO BATISTA',
  'SAO_JOAO_DO_ITAPERIU': 'SÃO JOÃO DO ITAPERIÚ',
  'SAO_JOAO_DO_SUL': 'SÃO JOÃO DO SUL',
  'SAO_JOAQUIM': 'SÃO JOAQUIM',
  'SAO_JOSE': 'SÃO JOSÉ',
  'SAO_JOSE_DO_CEDRO': 'SÃO JOSÉ DO CEDRO',
  'SAO_JOSE_DO_CERRITO': 'SÃO JOSÉ DO CERRITO',
  'SAO_LOURENCO_DO_OESTE': 'SÃO LOURENÇO DO OESTE',
  'SAO_LUDGERO': 'SÃO LUDGERO',
  'SAO_MARTINHO': 'SÃO MARTINHO',
  'SAO_MIGUEL_DA_BOA_VISTA': 'SÃO MIGUEL DA BOA VISTA',
  'SAO_MIGUEL_DO_OESTE': 'SÃO MIGUEL DO OESTE',
  'SAO_PEDRO_DE_ALCANTARA': 'SÃO PEDRO DE ALCÂNTARA',
  'SAUDADES': 'SAUDADES',
  'SCHROEDER': 'SCHROEDER',
  'SEARA': 'SEARA',
  'SERRA_ALTA': 'SERRA ALTA',
  'SIDEROPOLIS': 'SIDERÓPOLIS',
  'SOMBRIO': 'SOMBRIO',
  'SUL_BRASIL': 'SUL BRASIL',
  'TAIO': 'TAIÓ',
  'TANGARA': 'TANGARÁ',
  'TIGRINHOS': 'TIGRINHOS',
  'TIJUCAS': 'TIJUCAS',
  'TIMBE_DO_SUL': 'TIMBÉ DO SUL',
  'TIMBO': 'TIMBÓ',
  'TIMBO_GRANDE': 'TIMBÓ GRANDE',
  'TRES_BARRAS': 'TRÊS BARRAS',
  'TREVISO': 'TREVISO',
  'TREZE_DE_MAIO': 'TREZE DE MAIO',
  'TREZE_TOLIAS': 'TREZE TÍLIAS',
  'TROMBUDO_CENTRAL': 'TROMBUDO CENTRAL',
  'TUBARAO': 'TUBARÃO',
  'TUNAPOLIS': 'TUNÁPOLIS',
  'TURVO': 'TURVO',
  'UNIAO_DO_OESTE': 'UNIÃO DO OESTE',
  'URUBICI': 'URUBICI',
  'URUPEMA': 'URUPEMA',
  'URUSSANGA': 'URUSSANGA',
  'VARGEAO': 'VARGEÃO',
  'VARGEM': 'VARGEM',
  'VARGEM_BONITA': 'VARGEM BONITA',
  'VIDAL_RAMOS': 'VIDAL RAMOS',
  'VIDEIRA': 'VIDEIRA',
  'VITOR_MEIRELES': 'VITOR MEIRELES',
  'WITMARSUM': 'WITMARSUM',
  'XANXERE': 'XANXERÊ',
  'XAVANTINA': 'XAVANTINA',
  'XAXIM': 'XAXIM',
  'ZORTEA': 'ZORTÉA',
  'BALNEARIO_RINCAO': 'BALNEÁRIO RINCÃO'}

sys.exit()# <<< BREAK >>>



print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(casos.info())
print("~"*80)
print(casos.dtypes)
print("~"*80)
print(casos)
print("="*80)

print("\n \n FOCOS DE _Aedes_ spp. EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n")
print(focos.info())
print("~"*80)
print(focos.dtypes)
print("~"*80)
print(focos)
print("="*80)

print("\n \n PRECIPITAÇÃO EM SANTA CATARINA - SÉRIE HISTÓRICA (MERGE) \n")
print(prec.info())
print("~"*80)
print(prec.dtypes)
print("~"*80)
print(prec)
print("="*80)

print("\n \n TEMPERATURA MÍNIMA EM SANTA CATARINA - SÉRIE HISTÓRICA (SAMeT) \n")
print(tmin.info())
print("~"*80)
print(tmin.dtypes)
print("~"*80)
print(tmin)
print("="*80)

print("\n \n TEMPERATURA MÉDIA EM SANTA CATARINA - SÉRIE HISTÓRICA (SAMeT) \n")
print(tmed.info())
print("~"*80)
print(tmed.dtypes)
print("~"*80)
print(tmed)
print("="*80)

print("\n \n TEMPERATURA MÁXIMA EM SANTA CATARINA - SÉRIE HISTÓRICA (SAMeT) \n")
print(tmax.info())
print("~"*80)
print(tmax.dtypes)
print("~"*80)
print(tmax)
print("="*80)

print("\n PESOS[0] E VIÉSES[1] DA CAMADA 1 (dense):\n", modeloNN.layers[1].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 2 (dense_1):\n",modeloNN.layers[2].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 3 (dropout):\n",modeloNN.layers[3].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 4 (dense_2):\n",modeloNN.layers[4].get_weights())
print("~"*80)
print(modeloNN.get_config())

### Visualização Gráfica
#df_treino_x = pd.DataFrame({'x': treino_x[:, 0]})
#df_testes = pd.DataFrame({'y': testes[:, 0]})
#df_teste_y = pd.DataFrame({'y': teste_y})
sns.lineplot(x = focos["Semana"], y = pd.DataFrame(treino_x), label="Treino")
#sns.lineplot(x = focos["Semana"], label="Ajuste")
sns.lineplot(x = focos["Semana"], y = pd.DataFrame(testes), label = "Previsão")
sns.lineplot(x = focos["Semana"], y = pd.DataFrame(teste_y), label = "Teste")
plt.title("MODELO, AJUSTE E PREVISÃO")
plt.xlabel("Tempo (?)")
plt.ylabel("Quantidade (?)")
plt.show()


previsto = []

for i in testes:
    previsto.append(np.argmax(testes[i])).np.where(numbers == i)


previsao = pd.DataFrame({"Y_teste": teste_y, 
                         "Previsão" : previsto}) #list(modeloNN.predict(teste_x)).flatten()
#print(testes.DType)
print(previsao)


print(previsoes.eval())

def tensor_to_array(array_value):
    return array_value.ndarray()

print(tensor_to_array(testes))

print(f"keras.layers.Flatten(input_shape = x); onde x: {shape_input.shape}.")
print(treino_x.shape[1:])
print(prec_cidade_2012)
print(prec.iloc[605: , :])
print(tmin.iloc[626: , :])
"""
