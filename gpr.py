### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, RationalQuadratic
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, DotProduct, Matern
"""
import statsmodels as sm
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
"""

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Variáveis
cidade = "Florianópolis"
# Variáveis / Semanas Epidemiológicas de 2022
focos = "focos22se.csv"
casos = "casos22se.csv"
merge = "merge22se.csv"
tmin = "tmin22se.csv"
tmed = "tmed22se.csv"
tmax = "tmax22se.csv"

### Abrindo Arquivos
focos = pd.read_csv(f"{caminho_dados}{focos}")
casos = pd.read_csv(f"{caminho_dados}{casos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")

### Selecionando Município
focos = focos[f"{cidade}"].copy()
casos = casos[f"{cidade}"].copy()
merge = merge[f"{cidade}"].copy()
tmin = tmin[f"{cidade}"].copy()
tmed = tmed[f"{cidade}"].copy()
tmax = tmax[f"{cidade}"].copy()

### Montando e Visualizando DataFrame (Pandas)
dados = pd.DataFrame()
dados["Focos"], dados["Precipitação"], dados["Casos"] = focos, merge, casos
dados["Temperatura Mínima"], dados["Temperatura Média"], dados["Temperatura Máxima"] = tmin, tmed, tmax
#dados["log_focos"], dados["log_precipitacao"] = np.log(focos), np.log(merge)
#dados["log_temperatura_minima"], dados["log_temperatura_media"] = np.log(tmin), np.log(tmed)
#dados["log_temperatura_maxima"] = np.log(tmin)
print(f"\n \nDATAFRAME BASE DO MUNICÍPIO DE {cidade.upper()} PARA PROCESSO GAUSSIANO DE REGRESSÃO \n")
print(dados)
print("~"*80)
print(dados.info())
print("~"*80)
print(dados.dtypes)
print("~"*80)
print(dados.describe())
print("="*80)

### Montando e Visualizando Arrays (Numpy)
print(dados.shape)
dados_array = np.asarray(dados)
focos = dados_array[0 : (dados.shape[0] - 1), 0]
prec = dados_array[0 : (dados.shape[0] - 1), 1]
casos = dados_array[0 : (dados.shape[0] - 1), 2]
tmin = dados_array[0 : (dados.shape[0] - 1), 3]
tmed = dados_array[0 : (dados.shape[0] - 1), 4]
tmax = dados_array[0 : (dados.shape[0] - 1), 5]
y = np.asarray([prec, tmin, tmed, tmax]).T
x = np.atleast_2d(focos).T
print(f"\n \nARRAY BASE DO MUNICÍPIO DE {cidade.upper()} (VARIÁVEIS EXPLICATIVAS = ELEMENTOS CLIMÁTICOS) \n")
print(y)
print("="*80)
print(f"\n \nARRAY BASE DO MUNICÍPIO DE {cidade.upper()} (VARIÁVEL DEPENDENTE = FOCOS) \n")
print(x)
print("="*80)


### Pré-processamento
np.random.seed(0)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y, test_size = 0.3)#, stratify = y)
scaler = StandardScaler()
scaler.fit(raw_treino_x)
treino_x = scaler.transform(raw_treino_x)
teste_x = scaler.transform(raw_teste_x)

### Modelando a Regressão por Processo Gaussiano
# Selecionando Kernel

kernels = [1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)),
           1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1),
           1.0 * ExpSineSquared(length_scale=1.0, periodicity=3.0,
                                length_scale_bounds=(0.1, 10.0),
                                periodicity_bounds=(1.0, 10.0)),
           ConstantKernel(0.1, (0.01, 10.0))
               * (DotProduct(sigma_0=1.0, sigma_0_bounds=(0.1, 10.0)) ** 2),
           1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0),
                        nu=1.5)]
# Instanciando Modelo
for kernel in kernels:

    gp = GaussianProcessRegressor(kernel=kernel)

    # Plot prior
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    y_mean, y_std = gp.predict(x, return_std=True)
    plt.plot(x, y_mean, 'k', lw=3, zorder=9)
    plt.fill_between(x, y_mean - y_std, y_mean + y_std,
                     alpha=0.2, color='k')
    y_samples = gp.sample_y(x[:, np.newaxis], 10)
    plt.plot(x, y_samples, lw=1)
    plt.xlim(0, 5)
    plt.ylim(-3, 3)
    plt.title(f"Prior (kernel: {kernel})", fontsize=12)

    # Fit GP
    gp.fit(x, y)
    # Plot posterior
    plt.subplot(2, 1, 2)
    y_mean, y_std = gp.predict(x, return_std=True)
    plt.plot(x, y_mean, 'k', lw=3, zorder=9)
    plt.fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.2, color='k')

    y_samples = gp.sample_y(X_[:, np.newaxis], 10)
    plt.plot(x, y_samples, lw=1)
    plt.scatter(x[:, 0], y, c='r', s=50, zorder=10, edgecolors=(0, 0, 0))
    plt.xlim(0, 5)
    plt.ylim(-3, 3)
    plt.title(f"Posterior (kernel: {gp.kernel_})\n Log-Likelihood: {gp.log_marginal_likelihood(gp.kernel_.theta)}",
              fontsize=12)
    plt.tight_layout()

plt.show()

"""
#raise ValueError(f"{name!r} is not 1-dimensional")
#ValueError: 'y1' is not 1-dimensional

gp = GaussianProcessRegressor(kernel = kernel, n_restarts_optimizer = 4)
gp.fit(x, y)
y_pred_1, sigma_1 = gp.predict(x, return_std = True)

kernel = C()*Exp(length_scale = 1, periodicity = 1)

kernel = C()*RQ(length_scale = 1, alpha = 1)

kernel = C()*Exp(length_scale = 1, periodicity = 1) * RQ(length_scale = 1, alpha = 1,
                                                          length_scale_bounds = (1e-05, 2),
                                                          alpha_bounds = (1e-05, 100000.0))

kernel = C()*RBF(length_scale = 1,
                 length_scale_bounds = (1e-05, 2)) * RQ(length_scale = 1, alpha = 0.5,
                                                        length_scale_bounds = (1e-05, 2),
                                                        alpha_bounds = (1e-05, 100000.0) + Exp (length_scale = 1, periodicity = 1))
# GP is a distribution, not a single number.
# Operate over a wide range of domains, and  enable efficient of hyperparameter selection.
# Kernel = A function which measures the similarity of two inputs, x and x', written as: k(x, x'|t); (t = thao)
# where t (thao) is a vector of hyperparameters used to tune it, how the kernel measures similarity.
# Can't just use any function. There are technical restrictions on what makes for a valid kernel.
# Most software won't allow you to use an invalid kernel.
# Bold face, Lower case! x and x' are vectors!
# 1 dimensional Radial Basis Function (RBF). Similarity with Heatmap. k(x,x'|t) = s²exp(-1/2(x-x'/l)²); (s = output_scale)(l = lenght_scale)
# Small values of the lenght scales can makes the samples wiggle more rapidly.
# Output scale determines the scale of the y values. Incrising makes the function spin more of the y-axis.
# Intuitively, a GP will sample functions with nearby y's for x's deemed similar by the kernel.
# Modeling by Combining Kernels:
# (Kernel Addition) >> kc(x,x'|tc) = ka(x,x'|ta) + kb(x,x'|tb)
# Adding kernels corresponds to adding sampled functions.
# (Kernel Multiplication) >> kc(x,x'|tc) = ka(x,x'|ta)kb(x,x'|tb)
# If you multilpy to kernels can you create a sample from that by sampling from each kernel and then multiplying those sampled functions
# Not technically. cannot be constructed by multiplying samples, but useful approximation to act as though you can.
# The noise counts as another hyperparameter model. If it's high, the model will ignore the data. Lower, more interpolated.
# Collect everything into matrices/vectors: X, X*, y, f, f*
# (X = Matrix where each row is a vector input)
# (X* = is the same thing, but for the test points)
# (y = Vector of all our observed outputs)
# (f = Unobserved true function outputs for all our inputs)
# (f* = is the same thing, but for the test points)
# Gaussian Process Assumption: y and f* are distributed as an (N+M)-dimensional multivariate Normal:
# Then our entire dataset counts only as a partial observation of one sample from this thing.
# The posterior distribution over f* comes from conditioning: (Bayesian Updating)
# To produce each, a sample is drawn where y is empty and f are outputs for a large number of evenly spaced points along the x-axis.
# Hyperparameter Selection
# Pick t (thao) and s²e (noise variance) by maximizing the log-likelihood of y after integrating out possible f(.)'s [Integral]
# Don't make confuse with the s (= output scale). Important hyperparameter too.
# It's just the log density of the y vector according to some multivariate normal.
# GPyTorch
# The art of GPS by using neural networks to learn the kernel automatically.
"""
