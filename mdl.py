### Bibliotecas Correlatas
# Básicas, Gráficas e Suporte
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
#import datetime
import sys
# Pré-Processamento e Validações
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score
# Modelos
from sklearn.ensemble import RandomForestRegressor
import tensorflow
from tensorflow import keras

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
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
retroagir = 8 # Semanas Epidemiológicas
cidade = "Florianópolis"
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
for r in range(1, retroagir + 1):
    dataset[f"TMIN_r{r}"] = dataset["TMIN"].shift(-r)
    dataset[f"TMED_r{r}"] = dataset["TMED"].shift(-r)
    dataset[f"TMAX_r{r}"] = dataset["TMAX"].shift(-r)
    dataset[f"PREC_r{r}"] = dataset["PREC"].shift(-r)
    dataset[f"FOCOS_r{r}"] = dataset["FOCOS"].shift(-r)
dataset.dropna(inplace = True)
dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{cidade}"

### Dividindo Dataset em Treino e Teste
SEED = np.random.seed(0)
x = dataset.drop(columns = "FOCOS")
y = dataset["FOCOS"]
x_array = x.to_numpy()
y_array = y.to_numpy()
x_array = x_array.reshape(x_array.shape[0], -1)

treino_x, teste_x, treino_y, teste_y = train_test_split(x_array, y_array,
                                                        random_state = SEED,
                                                        test_size = 0.2)#,
                                                        #stratify = y)
### Normalizando/Escalonando Dataset_x
escalonador = StandardScaler()
escalonador.fit(treino_x)
treino_normal_x = escalonador.transform(treino_x)
teste_normal_x = escalonador.transform(teste_x)

### Exibindo Informações
print("\n \n CONJUNTO DE DADOS PARA TREINO E TESTE \n")
print(dataset.info())
print("~"*80)
print(dataset.dtypes)
print("~"*80)
print(dataset)
print("="*80)
print(f"X no formato numpy.ndarray: {x_array}.")
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

def grafico_previsao(previsao, string_modelo):
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
    final.drop([d for d in range(retroagir)], axis=0, inplace = True)
    final.drop(final.index[-retroagir:], axis=0, inplace = True)
    previsoes = previsao if string_modelo == "RF" else [np.argmax(p) for p in previsao]
    lista_previsao = [previsoes[v] for v in range(len(previsoes))]
    final["Previstos"] = lista_previsao
    print(final)
    print("="*80)
    sns.lineplot(x = range(0, len(final)), y = final["Focos"], label = "Observado")
    sns.lineplot(x = range(0, len(final)), y = final["Previstos"], label = "Previsto")
    plt.xticks(rotation = 70)
    plt.xlabel("Tempo (Semanas Epidemiológicas, iniciando em 01/01/2012)")
    plt.ylabel("Quantidade (Número de Focos de _Aedes_ sp.)")
    plt.title(f"MODELO {nome_modelo.upper()}: OBSERVAÇÃO E PREVISÃO")
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

######################################################RANDOM_FOREST############################################################
### Instanciando e Treinando Modelo Regressor Random Forest
modeloRF = RandomForestRegressor(n_estimators = 100, random_state = SEED) #n_estimators = número de árvores
modeloRF.fit(treino_x, treino_y)

### Testando e Avaliando
y_previstoRF = modeloRF.predict(teste_normal_x)
EQM_RF = mean_squared_error(teste_y, y_previstoRF)
#acuraciaRF = accuracy_score(teste_y, y_previstoRF)
print(f"Erro Quadrático Médio (Random Forest): {EQM_RF}")
#print(f"A acurácia foi {acuraciaRF.round(2)}%. (Random Forest)")

### Testando e Validando Modelo
#validaRF = modeloRF.fit(treino_x, treino_y)
testesRF = modeloRF.predict(teste_x)
previsoesRF = modeloRF.predict(x)

### Exibindo Informações e Gráficos
lista_previsao(previsoesRF, 50, "RF")
grafico_previsao(previsoesRF, "RF")

######################################################NEURAL_NETWORK############################################################
### Instanciando e Compilando Modelo de Rede Neural
modeloNN = keras.Sequential([
    #keras.layers.LSTM(64, input_shape = (1, 1), return_sequences = True), #entrada Memória de Longo Prazo
    keras.layers.Flatten(input_shape = treino_x.shape[1:]), #entrada. #Camada 0 <<< input_shape = treino_x.shape[1:]
    #keras.layers.GRU(64, input_shape = ??? ), #CAMADA 1 Unidade Recorrente Fechada
    keras.layers.Dense(256, activation = tensorflow.nn.relu), #processamento. #Camada 1
    #keras.layers.Dense(128, activation = tensorflow.nn.relu), #processamento. #Camada 2
    keras.layers.Dense(64, activation = tensorflow.nn.relu), #processamento. #Camada 3
    keras.layers.Dropout(0.3), # ~Normalização (processamento) #Camada 4
    keras.layers.Dense(len(y_array), activation = tensorflow.nn.softmax)]) #saida. #Camada 5

lr_adam = keras.optimizers.Adam(learning_rate = 0.001)
callbacks = [keras.callbacks.EarlyStopping(monitor = "val_loss")]#,
"""
             keras.callbacks.ModelCheckpoint(filepath = f"{caminho_dados}melhor_modeloNN.dhf5",
                                             monitor = "val_loss", save_best = True)]
"""
modeloNN.compile(optimizer = lr_adam, #"adam",
               loss = "sparse_categorical_crossentropy",
               metrics = ["accuracy"])

### Testando e Validando Modelo
valida = modeloNN.fit(treino_x, treino_y,
                      epochs = 100, validation_split = 0.2,
                      callbacks = callbacks)#, batch_size = 10000)
testes = modeloNN.predict(teste_x)
#testes_normal = modeloNN.predict(teste_normal_x)
previsoesNN = modeloNN.predict(x)

### Exibindo Informações e Gráficos
print(modeloNN.summary())
lista_previsao(previsoesNN, 50, "NN")
grafico_previsao(previsoesNN, "NN")


sys.exit()# <<< BREAK >>>


"""
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
