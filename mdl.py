### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, accuracy_score
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
cidade = "Florianópolis"
lista_cidades = ["FLORIANÓPOLIS", "CHAPECÓ", "JOINVILLE", "ITAJAÍ"]
cidade = cidade.upper()
cidades = focos.columns
focos['Semana'] = pd.to_datetime(focos['Semana'])#, format="%Y%m%d")
casos['Semana'] = pd.to_datetime(casos['Semana'])
prec['Semana'] = pd.to_datetime(prec['Semana'])
tmin['Semana'] = pd.to_datetime(tmin['Semana'])
tmed['Semana'] = pd.to_datetime(tmed['Semana'])
tmax['Semana'] = pd.to_datetime(tmax['Semana'])
"""
prec_cidade_2012 = prec[cidade].iloc[605: ]
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
dataset["TMIN_m1"] = dataset["TMIN"].shift(-1)
dataset["TMED_m1"] = dataset["TMED"].shift(-1)
dataset["TMAX_m1"] = dataset["TMAX"].shift(-1)
dataset["PREC_m1"] = dataset["PREC"].shift(-1)
dataset["FOCOS_m1"] = dataset["FOCOS"].shift(-1)
dataset["TMIN_m2"] = dataset["TMIN"].shift(-2)
dataset["TMED_m2"] = dataset["TMED"].shift(-2)
dataset["TMAX_m2"] = dataset["TMAX"].shift(-2)
dataset["PREC_m2"] = dataset["PREC"].shift(-2)
dataset["FOCOS_m2"] = dataset["FOCOS"].shift(-2)
dataset["TMIN_m3"] = dataset["TMIN"].shift(-3)
dataset["TMED_m3"] = dataset["TMED"].shift(-3)
dataset["TMAX_m3"] = dataset["TMAX"].shift(-3)
dataset["PREC_m3"] = dataset["PREC"].shift(-3)
dataset["FOCOS_m3"] = dataset["FOCOS"].shift(-3)
dataset["TMIN_m4"] = dataset["TMIN"].shift(-4)
dataset["TMED_m4"] = dataset["TMED"].shift(-4)
dataset["TMAX_m4"] = dataset["TMAX"].shift(-4)
dataset["PREC_m4"] = dataset["PREC"].shift(-4)
dataset["FOCOS_m4"] = dataset["FOCOS"].shift(-4)
dataset.dropna(inplace = True)
#dataset["Semana"] = pd.to_numeric(dataset["Semana"])
dataset.set_index("Semana", inplace = True)
dataset.columns.name = f"{cidade}"

### Dividindo Dataset em Treino e Teste
SEED = np.random.seed(0)
x = dataset.drop(columns = "FOCOS")
y = dataset["FOCOS"]
x = x.to_numpy()
y = y.to_numpy()
x = x.reshape(x.shape[0], -1)

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y,
                                                        random_state = SEED,
                                                        test_size = 0.2)#,
                                                        #stratify = y)
### Normalizando/Escalonando Dataset_x
escalonador = StandardScaler()
escalonador.fit(treino_x)
treino_normal_x = escalonador.transform(treino_x)
teste_normal_x = escalonador.transform(teste_x)

### Instanciando e Treinando Modelo Regressor RandomForest
modeloRF = RandomForestRegressor(n_estimators = 100, random_state = SEED) #n_estimators is the number of trees in the forest.
modeloRF.fit(treino_normal_x, treino_y)

### Testando e Avaliando
y_previstoRF = modeloRF.predict(teste_normal_x)
mseRF = mean_squared_error(teste_y, y_previstoRF)
#acuraciaRF = accuracy_score(teste_y, y_previstoRF)
print(f"Erro Quadrático Médio (Random Forest): {mseRF}")
#print(f"A acurácia foi {acuraciaRF.round(2)}%. (Random Forest)")

"""
# Assuming treino_x is a 2D array with shape (num_samples, num_features)
# Reshape treino_x to have a third dimension for the time steps
timesteps = 1  # Assuming each sample is a single time step
treino_x_reshaped = np.reshape(treino_x, (treino_x.shape[0], timesteps, treino_x.shape[1]))
treino_x_reshaped = treino_x.reshape(treino_x.shape[0], 1, 1)
#timesteps, treino_x_reshaped.shape[1]
"""
### Instanciando e Compilando Modelo de Rede Neural
modelo = keras.Sequential([
    #keras.layers.LSTM(64, input_shape = (1, 1), return_sequences = True), #entrada Memória de Longo Prazo
    keras.layers.Flatten(input_shape = treino_x.shape[1:]), #entrada. #Camada 0 <<< input_shape = treino_x.shape[1:]
    #keras.layers.GRU(64, input_shape = ??? ), #CAMADA 1 Unidade Recorrente Fechada
    keras.layers.Dense(256, activation = tensorflow.nn.relu), #processamento. #Camada 1
    #keras.layers.Dense(128, activation = tensorflow.nn.relu), #processamento. #Camada 2
    keras.layers.Dense(64, activation = tensorflow.nn.relu), #processamento. #Camada 3
    keras.layers.Dropout(0.3), # ~Normalização (processamento) #Camada 4
    keras.layers.Dense(len(y), activation = tensorflow.nn.softmax)]) #saida. #Camada 5

lr_adam = keras.optimizers.Adam(learning_rate = 0.0001)
callbacks = [keras.callbacks.EarlyStopping(monitor = "val_loss")]#,
"""
             keras.callbacks.ModelCheckpoint(filepath = f"{caminho_dados}melhor_modelo.dhf5",
                                             monitor = "val_loss", save_best = True)]
"""
modelo.compile(optimizer = lr_adam, #"adam",
               loss = "sparse_categorical_crossentropy",
               metrics = ["accuracy"])

### Testando e Validando Modelo
valida = modelo.fit(treino_normal_x, treino_y,
                    epochs = 100, validation_split = 0.2,
                    callbacks = callbacks)#, batch_size = 10000)
testes = modelo.predict(teste_x)
#previsoes = tensorflow.argmax(testes, axis = 1)

print(f"Resultado do Teste do Modelo: {np.argmax(testes[0])}")#np.argmax(testes[0])
print(f"Número de Focos do Teste: {teste_y[0]}")
print(modelo.summary())
"""
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 1 (dense):\n", modelo.layers[1].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 2 (dense_1):\n",modelo.layers[2].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 3 (dropout):\n",modelo.layers[3].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 4 (dense_2):\n",modelo.layers[4].get_weights())
print("~"*80)
print(modelo.get_config())

testes_modelo_salvo = modelo.predict(teste_normal_x)
"""
print(f"Resultado do Teste do Modelo: {np.argmax(testes[0])}")
print(f"Número do Teste: {teste_y[0]}")

### Visualização Gráfica
plt.plot(valida.history["accuracy"])
plt.plot(valida.history["val_accuracy"])
plt.plot(valida.history["loss"])
plt.plot(valida.history["val_loss"])
plt.title("VALIDAÇÃO DO MODELO - TREINO (CICLOS x ACURÁCIA/PERDA)")
plt.xlabel("Ciclos de Treino (epochs)")
plt.ylabel("Perda e Acurácia")
plt.legend(["Acurácia_Treino", "Acurácia_Validação", "Perda_Treino", "Perda_Validação"])
plt.show()
"""
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

### Exibindo Informações

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
"""
print("\n \n CONJUNTO DE DADOS PARA TREINO E TESTE \n")
print(dataset.info())
print("~"*80)
print(dataset.dtypes)
print("~"*80)
print(dataset)
print("="*80)
print(f"X: {x}.")
print("="*80)
print(f"Y: {y}.")
print("="*80)
print(f"Treinaremos com {len(treino_x)} elementos e testaremos com {len(teste_x)} elementos.") # Tamanho é igual para dados normalizados
print(f"Formato dos dados (X) nas divisões treino: {treino_x.shape} e teste: {teste_x.shape}.")
print(f"Formato dos dados (Y) nas divisões treino: {treino_y.shape} e teste: {teste_y.shape}.")
print("="*80)
print(treino_x.shape[1:])
#print(previsoes.eval())

def tensor_to_array(array_value):
    return array_value.ndarray()

print(tensor_to_array(testes))
"""
print(f"keras.layers.Flatten(input_shape = x); onde x: {shape_input.shape}.")

print(prec_cidade_2012)
print(prec.iloc[605: , :])
print(tmin.iloc[626: , :])
"""
