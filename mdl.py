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
# Pré-Processamento e Validações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score
# Modelos
from sklearn.ensemble import RandomForestRegressor
import tensorflow
from tensorflow import keras
#from keras.models import load_model

### Encaminhamento aos Diretórios
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"
_www = False 
if _www == True: # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
else:
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NO SEGUINTE CAMINHO:\n\n{caminho_dados}\n\n")

### Renomeação das Variáveis pelos Arquivos
casos = "casos_se.csv"
focos = "focos_pivot.csv"
prec = "merge_se.csv"
tmin = "tmin_se.csv"
tmed = "tmed_se.csv"
tmax = "tmax_se.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
prec = pd.read_csv(f"{caminho_dados}{prec}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)

### Pré-Processamento
_retroagir = 8 # Semanas Epidemiológicas
cidade = "Itá" #"Itajaí" "Joinville" "Chapecó" "Florianópolis" "Lages" "Itá"
cidade = cidade.upper()
focos["Semana"] = pd.to_datetime(focos["Semana"])#, format="%Y%m%d")
casos["Semana"] = pd.to_datetime(casos["Semana"])
prec["Semana"] = pd.to_datetime(prec["Semana"])
tmin["Semana"] = pd.to_datetime(tmin["Semana"])
tmed["Semana"] = pd.to_datetime(tmed["Semana"])
tmax["Semana"] = pd.to_datetime(tmax["Semana"])
"""
prec_cidade_2012 = prec[cidade].iloc[605: ]
cidades = focos.columns#.drop(columns = "Semana", inplace = True)
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]
"""

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
# FLORIANÓPOLIS retroagindo 4se
# R² = 0.65 for r in range(1, _retroagir + 1) Bem ajustado ao tempo cronológico
# R² = 0,67 for r in range(1, _retroagir + 1, 2) Apresenta leve atraso no tempo cronológico
# R² = 0,52 for r in range(2, _retroagir + 1, 4) Apresenta certo atraso no tempo cronológico
# JOINVILLE retroagindo 4se
# R² = 0.69 for r in range(1, _retroagir + 1)
# R² = 0,67 for r in range(1, _retroagir + 1, 2) Pequeno atraso no tempo cronológico
# R² = 0,66 for r in range(2, _retroagir + 1, 4) Apresenta certo atraso no tempo cronológico
for r in range(1, _retroagir + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
"""
# FLORIANÓPOLIS retroagindo 8se
# R² = 0.72 for r in range(4, _retroagir + 1)
# R² = 0,60 for r in range(4, _retroagir + 1, 2)
# R² = 0,50 for r in range(2, _retroagir + 1, 2) Apresenta certo atraso no tempo cronológico
# R² = 0,498 for r in range(2, _retroagir + 1) Embora pareça que acompanha no tempo cronológico
# JOINVILLE retroagindo 8se
# R² = 0.77 for r in range(4, _retroagir + 1)
# R² = 0,63 for r in range(4, _retroagir + 1, 2)
# R² = 0,79 for r in range(2, _retroagir + 1, 2) Apresenta certo atraso no tempo cronológico
# R² = 0,64 for r in range(2, _retroagir + 1) Parece que acompanha melhor o tempo cronológico
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

### Dividindo Dataset em Treino e Teste
SEED = np.random.seed(0)
x = dataset.drop(columns = "FOCOS")
y = dataset["FOCOS"]
x_array = x.to_numpy().astype(int)
y_array = y.to_numpy().astype(int)
x_array = x_array.reshape(x_array.shape[0], -1)

treino_x, teste_x, treino_y, teste_y = train_test_split(x_array, y_array,
                                                        random_state = SEED,
                                                        test_size = 0.2)#,
"""                                                        #stratify = y)
num_classes = len(np.unique(y_array))
print("Number of classes:", num_classes)
print(len(y_array))
"""
### Normalizando/Escalonando Dataset_x
escalonador = StandardScaler()
escalonador.fit(treino_x)
treino_normal_x = escalonador.transform(treino_x)
teste_normal_x = escalonador.transform(teste_x)

### Exibindo Informações
print("\n \n CONJUNTO DE DADOS PARA TREINO E TESTE \n")
print(dataset.info())
print("~"*80)
#print(dataset.dtypes)
#print("~"*80)
print(dataset)
#print("="*80)
#print(f"X no formato numpy.ndarray: {x_array}.")
print("="*80)
print(f"Treinando com {len(treino_x)} elementos e testando com {len(teste_x)} elementos.") # Tamanho é igual para dados normalizados
print(f"Formato dos dados (X) nas divisões treino: {treino_x.shape} e teste: {teste_x.shape}.")
print(f"Formato dos dados (Y) nas divisões treino: {treino_y.shape} e teste: {teste_y.shape}.")
print("="*80)

### Definindo Funções
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
                 color = "red", alpha = 0.7, linewidth = 3, label = "Previsto")
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

### Testando e Validando Modelo
#validaRF = modeloRF.fit(treino_x, treino_y)
testesRF = modeloRF.predict(teste_x)
previsoesRF = modeloRF.predict(x)
previsoesRF = [int(p) for p in previsoesRF]

### Exibindo Informações, Gráficos e Métricas
lista_previsao(previsoesRF, 5, "RF")
grafico_previsao(previsoesRF, testesRF, "RF")
metricas("RF")
print(f"Caminho e Nome do arquivo:\n{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")

### Salvando Modelo (e abrindo)
# HDF5 (Hierarchical Data Format version 5) files
# Which are used to store and organize large amounts of data.
os.makedirs(caminho_modelos, exist_ok=True)
joblib.dump(modeloRF, f"{caminho_modelos}RF_r{_retroagir}_{cidade}.h5")
#modelo = joblib.load('random_forest.h5')

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
