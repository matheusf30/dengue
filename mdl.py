### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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
dataset.dropna(inplace = True)
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

### Instanciando e Compilando Modelo
"""
input_flatten = keras.Input(shape = treino_normal_x.shape)
shape_input = keras.layers.Flatten()(input_flatten)
#shape_input = keras.layers.Reshape(treino_normal_x.shape)(input_flatten)
"""
modelo = keras.Sequential([
    #keras.layers.GlobalMaxPooling1D(input_shape = treino_norml_x.shape),
    #keras.layers.UpSampling2D(size = treino_normal_x.shape, data_format = None, interpolation = "nearest"),
    keras.layers.Flatten(input_shape = treino_x.shape[1:]), #entrada. #Camada 0
    keras.layers.Dense(256, activation = tensorflow.nn.relu), #processamento. #Camada 1
    #keras.layers.Dense(128, activation = tensorflow.nn.relu), #processamento. #Camada 2
    keras.layers.Dense(64, activation = tensorflow.nn.relu), #processamento. #Camada 3
    keras.layers.Dropout(0.3), # ~Normalização (processamento) #Camada 4
    keras.layers.Dense(len(y), activation = tensorflow.nn.softmax)]) #saida. #Camada 5

#adam = keras.optimizers.Adam(learning_rate = 0.002)
callbacks = [keras.callbacks.EarlyStopping(monitor = "val_loss")]#,
"""
             keras.callbacks.ModelCheckpoint(filepath = f"{caminho_dados}melhor_modelo.dhf5",
                                             monitor = "val_loss", save_best = True)]
"""
modelo.compile(optimizer = "adam", #f"{adam}",
               loss = "sparse_categorical_crossentropy",
               metrics = ["accuracy"])

### Testando e Validando Modelo
valida = modelo.fit(treino_normal_x, treino_y, epochs = 40, validation_split = 0.2, callbacks = callbacks)#, batch_size = 10000)

testes = modelo.predict(teste_x)

print(f"Resultado do Teste do Modelo: {np.argmax(testes[0])}")#np.argmax(testes[0])
print(f"Número de Focos do Teste: {teste_y[0]}")
print(modelo.summary())
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 1 (dense):\n", modelo.layers[1].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 2 (dense_1):\n",modelo.layers[2].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 3 (dropout):\n",modelo.layers[3].get_weights())
print("~"*80)
print("\n PESOS[0] E VIÉSES[1] DA CAMADA 4 (dense_2):\n",modelo.layers[4].get_weights())
print("~"*80)
print(modelo.get_config())
"""
testes_modelo_salvo = modelo.predict(teste_x)
print(f"Resultado do Teste do Modelo Salvo: {np.argmax(testes_modelo_salvo[0])}")
print(f"Número do Teste: {teste_y[0]}")
"""
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
sns.lineplot(x = treino_x[:, 0], y = testes[:, 0], label = "Ajuste")
sns.lineplot(x = treino_l_x, y = teste_y, label = "Treino")
plt.title("MODELO E PREVISÃO")
plt.xlabel("Tempo (?)")
plt.ylabel("Quantidade")
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
print(pd.DataFrame(testes))
"""
print(f"keras.layers.Flatten(input_shape = x); onde x: {shape_input.shape}.")

print(prec_cidade_2012)
print(prec.iloc[605: , :])
print(tmin.iloc[626: , :])
"""
