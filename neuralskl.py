### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
#dado = "dado_rede22.csv"
#dado = "dado_rede4cat22.csv"
#dado = "dado_rede4cat.csv"
#dado = "dado_rede.csv"
dado = "dado_rede_neural.csv"

### Abrindo Arquivo
dado = pd.read_csv(f"{caminho_dados}{dado}")

### Exibindo Informações
print("="*80)
#print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA EM SEMANAS EPIDEMIOLÓGICAS (DIVE/SC) \n + MUNICÍPIOS_xy_LATLON (IBGE) ")
print(dado.info())
print("~"*80)
print(dado.dtypes)
print("~"*80)
print(dado)
print("="*80)

######################## Reformular

x = dado[["Focos", "Temperatura", "Precipitação", "Focos_m1", "Temperatura_m1", "Precipitação_m1", "Focos_m2", "Temperatura_m2", "Precipitação_m2", "Focos_m3", "Temperatura_m3", "Precipitação_m3", "Focos_m4", "Temperatura_m4", "Precipitação_m4"]]
y = dado["Categoria"]

#from sklearn import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score

SEED = 5
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
                                                         stratify = y)

scaler = StandardScaler()
scaler.fit(raw_treino_x)
treino_x = scaler.transform(raw_treino_x)
teste_x = scaler.transform(raw_teste_x)

print(f"Treinamos com {len(treino_x)} elementos e testamos com {len(teste_x)} elementos.")

modelo = SVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)
acuracia = accuracy_score(teste_y, previsoes) * 100
print(f"A acurácia do Support Vector Classifier foi de {acuracia.round(2)}%" )

modelo = SVR(kernel = "rbf", gamma = "auto", C = 100)
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)
#acuracia = modelo.score(teste_y, previsoes) * 100
#print(f"A acurácia do Support Vector Regression foi de {acuracia.round(2)}%" )
print(previsoes)
# np.array().reshape(len(dado), 1) 
#ValueError: Classification metrics can't handle a mix of multiclass and continuous targets (sigmoid, rbf, poly)
#ValueError: Precomputed matrix must be a square matrix. Input is a 348x15 matrix (precomputed)
#ValueError: Expected 2D array, got 1D array instead: Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
#AttributeError: 'SVR' object has no attribute 'reshape'

from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy='stratified')
dummy.fit(treino_x, treino_y)
previsoes_dummy = dummy.predict(teste_x)

acuracia_dummy = accuracy_score(teste_y, previsoes_dummy) * 100
print(f"A acurácia do Dummy Stratified foi de {acuracia_dummy.round(2)}%" )


### ÁRVORE DE DECISÃO

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

SEED = 5
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
                                                         stratify = y)
#print(f"Treinamos com {len(treino_x)} elementos e testamos com {len(teste_x)} elementos.")

modelo = DecisionTreeClassifier(max_depth = 8)
modelo.fit(raw_treino_x, treino_y)
previsoes = modelo.predict(raw_teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print(f"A acurácia da Árvore de Decisão foi de {acuracia.round(2)}%" )

from sklearn.tree import export_graphviz
#!pip install graphviz
#!apt-get install graphviz
import graphviz

features = x.columns
dot_data = export_graphviz(modelo, out_file = None,
                           filled = True, rounded = True,
                           feature_names = features,
                           class_names = dado["Categoria"].values.astype(str))
grafico = graphviz.Source(dot_data)
grafico.render(format = "png", view=True)

"""
data_x = teste_x[:,0]
data_y = teste_x[:,1]

x_min = data_x.min()
x_max = data_x.max()
y_min = data_y.min()
y_max = data_y.max()
pixels = 100
eixo_x = np.arange(x_min, x_max, (x_max - x_min) / pixels)
eixo_y = np.arange(y_min, y_max, (y_max - y_min) / pixels)

xx, yy = np.meshgrid(eixo_x, eixo_y)
pontos = np.c_[xx.ravel(), yy.ravel()]

Z = modelo.predict(pontos)
Z = Z.reshape(xx.shape)

import matplotlib.pyplot as plt

plt.contourf(xx, yy, Z, alpha=0.3)
plt.scatter(data_x, data_y, c=teste_y, s=1)

import seaborn as sns

sns.scatterplot(x = "Focos", y = "Categoria", hue = "Categoria", data = dado)

sns.relplot(x = "Focos", y = "Categoria", hue = "Categoria", data = dado)#, col = "Categoria", )

#######

from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
seed = 20

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y,
                                                        random_state = seed,
                                                        test_size =0.25,
                                                        stratify = y)

print(f"Treinaremos com {len(treino_x)} elementos e testaremos com {len(teste_x)} elementos.")

modelo = LinearSVC()
modelo.fit(treino_x, treino_y)
previsoes = modelo.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print(f"A acurácia foi {acuracia.round(2)}%")

########
x_min = teste_x.horas_esperadas.min()
x_max = teste_x.horas_esperadas.max()
y_min = teste_x.preco.min()
y_max = teste_x.preco.max()
print(f" X_min: {x_min}, \n X_max: {x_max}, \n Y_min: {y_min}, \n Y_max: {y_max}.")
pixels = 100
eixo_x = np.arange(x_min, x_max, (x_max - x_min) / pixels)
eixo_y = np.arange(y_min, y_max, (y_max - y_min) / pixels)
print(eixo_x)
print(eixo_y)
xx, yy = np.meshgrid(eixo_x, eixo_y)
pontos = np.c_[xx.ravel(), yy.ravel()]
z = modelo.predict(pontos)
z = z.reshape(xx.shape)

import matplotlib.pyplot as plt

plt.contourf(xx, yy, z, alpha = 0.2)
plt.scatter(teste_x["horas_esperadas"], teste_x["preco"], c = teste_y, s = 1)

####################


### ÁRVORE DECISÃO

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

SEED = 5
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.25,
                                                         stratify = y)
print(f"Treinaremos com {len(treino_x)} elementos e testaremos com {len(teste_x)} elementos.")

modelo = DecisionTreeClassifier()
modelo.fit(raw_treino_x, treino_y)
previsoes = modelo.predict(raw_teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print(f"A acurácia foi {acuracia.round(2)}%" )

from sklearn.tree import export_graphviz
!pip install graphviz
!apt-get install graphviz
import graphviz

dot_data = export_graphviz(modelo, out_file = None)
grafico = graphviz.Source(dot_data)
grafico
###########

"""

