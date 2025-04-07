### Bibliotecas Correlatas
import matplotlib.pyplot as plt 
import matplotlib as mpl             
import pandas as pd
from matplotlib import cm
import matplotlib.colors as cls     
import cmocean
from datetime import timedelta
import numpy as np
import seaborn as sns
import statsmodels as sm
import pymannkendall as mk
import xarray as xr
### Suporte
import sys
import os
### Tratando avisos
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


### Condições para Variar #######################################################

_LOCAL = "IFSC" # OPÇÕES>>> "GH" "CASA" "IFSC"
"""
##################### Valores Booleanos ############ # sys.argv[0] is the script name itself and can be ignored!
_AUTOMATIZAR = sys.argv[1]   # True|False                    #####
_AUTOMATIZA = True if _AUTOMATIZAR == "True" else False      #####
_VISUALIZAR = sys.argv[2]    # True|False                    #####
_VISUALIZAR = True if _VISUALIZAR == "True" else False       #####
_SALVAR = sys.argv[3]        # True|False                    #####
_SALVAR = True if _SALVAR == "True" else False               #####
##################################################################
"""
##### Padrão ANSI ###############################################################
bold = "\033[1m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"
#################################################################################

### Encaminhamento aos Diretórios
if _LOCAL == "GH": # _ = Variável Privada
	caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
	caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
elif _LOCAL == "IFSC":
	caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
	caminho_shp = "/home/sifapsc/scripts/matheus/dados_dengue/shapefiles/"
	caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
	caminho_resultados = "/home/sifapsc/scripts/matheus/dengue/resultados/modelagem/"
	caminho_correlacao = "/home/sifapsc/scripts/matheus/dengue/resultados/correlacao/"
	caminho_cartografia = "/home/sifapsc/scripts/matheus/dengue/resultados/cartografia/"
else:
	print(f"\n{red}CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!{reset}")
print(f"\n{green}OS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n{reset}\n{caminho_dados}\n\n")

oeste = ("Abelardo Luz, Alto Bela Vista, Anchieta, Arabutã, Arvoredo, Bandeirante, Barra Bonita, Belmonte, Bom Jesus, Bom Jesus do Oeste, Caibi, Campo Erê, Caxambu do Sul, Chapecó, Concórdia, Cordilheira Alta, Coronel Freitas, Coronel Martins, Cunha Porã, Cunhataí, Descanso, Dionísio Cerqueira, Entre Rios, Faxinal dos Guedes, Flor do Sertão, Formosa do Sul, Galvão, Guaraciaba, Guarujá do Sul, Guatambú, Iporã do Oeste, Ipuaçu, Ipumirim, Iraceminha, Irani, Irati, Itapiranga, Itá, Jaborá, Jardinópolis, Jupiá, Lajeado Grande, Lindóia do Sul, Maravilha, Marema, Modelo, Mondaí, Nova Erechim, Nova Itaberaba, Novo Horizonte, Ouro Verde, Paial, Palma Sola, Palmitos, Paraíso, Peritiba, Pinhalzinho, Planalto Alegre, Presidente Castello Branco, Princesa, Quilombo, Riqueza, Romelândia, Saltinho, Santa Helena, Santa Terezinha do Progresso, Santiago do Sul, Saudades, Seara, Serra Alta, Sul Brasil, São Bernardino, São Carlos, São Domingos, São José do Cedro, São João do Oeste, São Lourenço do Oeste, São Miguel da Boa Vista, São Miguel do Oeste, Tigrinhos, Tunápolis, União do Oeste, Vargeão, Xanxerê, Xavantina,Xaxim, Águas Frias, Águas de Chapecó")
meio_oeste = ("Abdon Batista, Anita Garibaldi, Arroio Trinta, Bocaina do Sul, Brunópolis, Campo Belo do Sul, Campos Novos, Capinzal, Capão Alto, Catanduvas, Caçador, Celso Ramos, Cerro Negro, Correia Pinto, Curitibanos, Erval Velho, Fraiburgo, Frei Rogério, Herval d’Oeste, Ibiam, Ibicaré, Iomerê, Ipira, Joaçaba, Lacerdópolis, Lages, Lebon Régis, Luzerna, Macieira, Monte Carlo, Otacílio Costa, Ouro, Palmeira, Passos Maia, Pinheiro Preto, Piratuba, Ponte Alta, Ponte Alta do Norte, Ponte Serrada, Rio das Antas, Salto Veloso, Santa Cecília, São Cristóvão do Sul, São José do Cerrito, Tangará, Treze Tílias, Vargem, Vargem Bonita, Videira, Zortéa, Água Doce")
planalto_norte = ("Agrolândia, Agronômica, Atalanta, Aurora, Bela Vista do Toldo, Braço do Trombudo, Calmon, Campo Alegre, Canoinhas, Chapadão do Lageado, Corupá, Dona Emma, Doutor Pedrinho, Ibirama, Imbuia, Irineópolis, Itaiópolis, Ituporanga, José Boiteux, Laurentino, Lontras, Mafra, Major Vieira, Matos Costa, Mirim Doce, Monte Castelo, Papanduva, Petrolândia, Porto União, Pouso Redondo, Presidente Getúlio, Rio Negrinho, Rio do Campo, Rio do Oeste, Rio do Sul, Salete, Santa Terezinha, São Bento do Sul, Taió, Timbó Grande, Trombudo Central, Três Barras, Vitor Meireles, Witmarsum")
planalto_sul = ("Bom Jardim da Serra, Bom Retiro, Painel, Rio Rufino, São Joaquim, Urubici, Urupema")
litoral_norte = ("Alfredo Wagner, Angelina, Antônio Carlos, Apiúna, Araquari, Ascurra, Balneário Barra do Sul, BalneárioCamboriú, Balneário Piçarras, Barra Velha, Benedito Novo, Biguaçu, Blumenau, Botuverá, Brusque, Camboriú, Canelinha, Florianópolis, Garuva, Gaspar, Governador Celso Ramos, Guabiruba, Guaramirim, Ilhota, Indaial, Itajaí, Itapema, Itapoá, Jaraguá do Sul, Joinville, Leoberto Leal, Luiz Alves, Major Gercino, Massaranduba, Navegantes, Nova Trento, Palhoça, Penha, Pomerode, Porto Belo, Presidente Nereu, Rancho Queimado, Rio dos Cedros, Rodeio, Santo Amaro da Imperatriz, Schroeder, São Francisco do Sul, São José, São João Batista, São João do Itaperiú, São Pedro de Alcântara, Tijucas, Timbó, Vidal Ramos, Águas Mornas")
litoral_sul = ("Anitápolis, Araranguá, Armazém, Balneário Arroio do Silva, Balneário Gaivota, Balneário Rincão, Braço do Norte, Capivari de Baixo, Cocal do Sul, Criciúma, Ermo, Forquilhinha, Garopaba, Gravatal, Grão-Pará, Imaruí, Imbituba, Içara, Jacinto Machado, Jaguaruna, Laguna, Lauro Müller, Maracajá, Meleiro, Morro Grande, Morro da Fumaça, Nova Veneza, Orleans, Passo de Torres, Paulo Lopes, Pedras Grandes, Pescaria Brava, Praia Grande, Rio Fortuna, Sangão, Santa Rosa de Lima, Santa Rosa do Sul, Siderópolis, Sombrio, São Bonifácio, São João do Sul, São Ludgero, São Martinho, Timbé do Sul, Treviso, Treze de Maio, Tubarão, Turvo, Urussanga")
regioes = [oeste, meio_oeste, planalto_norte, planalto_sul, litoral_norte, litoral_sul]
for regiao in regioes:
	regiao = regiao.replace(", ", ",")
	regiao = regiao.split(",")
	print(regiao)
#sys.exit()
oeste = ['Abelardo Luz', 'Alto Bela Vista', 'Anchieta', 'Arabutã', 'Arvoredo', 'Bandeirante', 'Barra Bonita', 'Belmonte', 'Bom Jesus', 'Bom Jesus do Oeste', 'Caibi', 'Campo Erê', 'Caxambu do Sul', 'Chapecó', 'Concórdia', 'Cordilheira Alta', 'Coronel Freitas', 'Coronel Martins', 'Cunha Porã', 'Cunhataí', 'Descanso', 'Dionísio Cerqueira', 'Entre Rios', 'Faxinal dos Guedes', 'Flor do Sertão', 'Formosa do Sul', 'Galvão', 'Guaraciaba', 'Guarujá do Sul', 'Guatambú', 'Iporã do Oeste', 'Ipuaçu', 'Ipumirim', 'Iraceminha', 'Irani', 'Irati', 'Itapiranga', 'Itá', 'Jaborá', 'Jardinópolis', 'Jupiá', 'Lajeado Grande', 'Lindóia do Sul', 'Maravilha', 'Marema', 'Modelo', 'Mondaí', 'Nova Erechim', 'Nova Itaberaba', 'Novo Horizonte', 'Ouro Verde', 'Paial', 'Palma Sola', 'Palmitos', 'Paraíso', 'Peritiba', 'Pinhalzinho', 'Planalto Alegre', 'Presidente Castello Branco', 'Princesa', 'Quilombo', 'Riqueza', 'Romelândia', 'Saltinho', 'Santa Helena', 'Santa Terezinha do Progresso', 'Santiago do Sul', 'Saudades', 'Seara', 'Serra Alta', 'Sul Brasil', 'São Bernardino', 'São Carlos', 'São Domingos', 'São José do Cedro', 'São João do Oeste', 'São Lourenço do Oeste', 'São Miguel da Boa Vista', 'São Miguel do Oeste', 'Tigrinhos', 'Tunápolis', 'União do Oeste', 'Vargeão', 'Xanxerê', 'Xavantina', 'Xaxim', 'Águas Frias', 'Águas de Chapecó']
meio_oeste = ['Abdon Batista', 'Anita Garibaldi', 'Arroio Trinta', 'Bocaina do Sul', 'Brunópolis', 'Campo Belo do Sul', 'Campos Novos', 'Capinzal', 'Capão Alto', 'Catanduvas', 'Caçador', 'Celso Ramos', 'Cerro Negro', 'Correia Pinto', 'Curitibanos', 'Erval Velho', 'Fraiburgo', 'Frei Rogério', 'Herval d’Oeste', 'Ibiam', 'Ibicaré', 'Iomerê', 'Ipira', 'Joaçaba', 'Lacerdópolis', 'Lages', 'Lebon Régis', 'Luzerna', 'Macieira', 'Monte Carlo', 'Otacílio Costa', 'Ouro', 'Palmeira', 'Passos Maia', 'Pinheiro Preto', 'Piratuba', 'Ponte Alta', 'Ponte Alta do Norte', 'Ponte Serrada', 'Rio das Antas', 'Salto Veloso', 'Santa Cecília', 'São Cristóvão do Sul', 'São José do Cerrito', 'Tangará', 'Treze Tílias', 'Vargem', 'Vargem Bonita', 'Videira', 'Zortéa', 'Água Doce']
planalto_norte = ['Agrolândia', 'Agronômica', 'Atalanta', 'Aurora', 'Bela Vista do Toldo', 'Braço do Trombudo', 'Calmon', 'Campo Alegre', 'Canoinhas', 'Chapadão do Lageado', 'Corupá', 'Dona Emma', 'Doutor Pedrinho', 'Ibirama', 'Imbuia', 'Irineópolis', 'Itaiópolis', 'Ituporanga', 'José Boiteux', 'Laurentino', 'Lontras', 'Mafra', 'Major Vieira', 'Matos Costa', 'Mirim Doce', 'Monte Castelo', 'Papanduva', 'Petrolândia', 'Porto União', 'Pouso Redondo', 'Presidente Getúlio', 'Rio Negrinho', 'Rio do Campo', 'Rio do Oeste', 'Rio do Sul', 'Salete', 'Santa Terezinha', 'São Bento do Sul', 'Taió', 'Timbó Grande', 'Trombudo Central', 'Três Barras', 'Vitor Meireles', 'Witmarsum']
planalto_sul = ['Bom Jardim da Serra', 'Bom Retiro', 'Painel', 'Rio Rufino', 'São Joaquim', 'Urubici', 'Urupema']
litoral_norte = ['Alfredo Wagner', 'Angelina', 'Antônio Carlos', 'Apiúna', 'Araquari', 'Ascurra', 'Balneário Barra do Sul', 'BalneárioCamboriú', 'Balneário Piçarras', 'Barra Velha', 'Benedito Novo', 'Biguaçu', 'Blumenau', 'Botuverá', 'Brusque', 'Camboriú', 'Canelinha', 'Florianópolis', 'Garuva', 'Gaspar', 'Governador Celso Ramos', 'Guabiruba', 'Guaramirim', 'Ilhota', 'Indaial', 'Itajaí', 'Itapema', 'Itapoá', 'Jaraguá do Sul', 'Joinville', 'Leoberto Leal', 'Luiz Alves', 'Major Gercino', 'Massaranduba', 'Navegantes', 'Nova Trento', 'Palhoça', 'Penha', 'Pomerode', 'Porto Belo', 'Presidente Nereu', 'Rancho Queimado', 'Rio dos Cedros', 'Rodeio', 'Santo Amaro da Imperatriz', 'Schroeder', 'São Francisco do Sul', 'São José', 'São João Batista', 'São João do Itaperiú', 'São Pedro de Alcântara', 'Tijucas', 'Timbó', 'Vidal Ramos', 'Águas Mornas']
litoral_sul = ['Anitápolis', 'Araranguá', 'Armazém', 'Balneário Arroio do Silva', 'Balneário Gaivota', 'Balneário Rincão', 'Braço do Norte', 'Capivari de Baixo', 'Cocal do Sul', 'Criciúma', 'Ermo', 'Forquilhinha', 'Garopaba', 'Gravatal', 'Grão-Pará', 'Imaruí', 'Imbituba', 'Içara', 'Jacinto Machado', 'Jaguaruna', 'Laguna', 'Lauro Müller', 'Maracajá', 'Meleiro', 'Morro Grande', 'Morro da Fumaça', 'Nova Veneza', 'Orleans', 'Passo de Torres', 'Paulo Lopes', 'Pedras Grandes', 'Pescaria Brava', 'Praia Grande', 'Rio Fortuna', 'Sangão', 'Santa Rosa de Lima', 'Santa Rosa do Sul', 'Siderópolis', 'Sombrio', 'São Bonifácio', 'São João do Sul', 'São Ludgero', 'São Martinho', 'Timbé do Sul', 'Treviso', 'Treze de Maio', 'Tubarão', 'Turvo', 'Urussanga']
for regiao in regioes:
	regiao = regiao.upper()
	print(regiao)

sys.exit()

### Renomeação das Variáveis pelos Arquivos
casos = "sazonalidade_semanal_casos.csv"
focos = "sazonalidade_semanal_focos.csv"
prec = "sazonalidade_semanal_prec.csv"
tmin = "sazonalidade_semanal_tmin.csv"
tmed = "sazonalidade_semanal_tmed.csv"
tmax = "sazonalidade_semanal_tmax.csv"
serie_casos = "casos_pivot_total.csv"
serie_focos = "focos_pivot.csv"
serie_prec = "prec_semana_ate_2023.csv"
serie_tmin = "tmin_semana_ate_2023.csv"
serie_tmed = "tmed_semana_ate_2023.csv"
serie_tmax = "tmax_semana_ate_2023.csv"

### Abrindo Arquivo
casos = pd.read_csv(f"{caminho_dados}{casos}", low_memory = False)
focos = pd.read_csv(f"{caminho_dados}{focos}", low_memory = False)
prec = pd.read_csv(f"{caminho_dados}{prec}", low_memory = False)
tmin = pd.read_csv(f"{caminho_dados}{tmin}", low_memory = False)
tmed = pd.read_csv(f"{caminho_dados}{tmed}", low_memory = False)
tmax = pd.read_csv(f"{caminho_dados}{tmax}", low_memory = False)
serie_casos = pd.read_csv(f"{caminho_dados}{serie_casos}", low_memory = False)
serie_focos = pd.read_csv(f"{caminho_dados}{serie_focos}", low_memory = False)
serie_prec = pd.read_csv(f"{caminho_dados}{serie_prec}", low_memory = False)
serie_tmin = pd.read_csv(f"{caminho_dados}{serie_tmin}", low_memory = False)
serie_tmed = pd.read_csv(f"{caminho_dados}{serie_tmed}", low_memory = False)
serie_tmax = pd.read_csv(f"{caminho_dados}{serie_tmax}", low_memory = False)

print(f"\n{green}CASOS\n{reset}{casos}\n")
print(f"\n{green}FOCOS\n{reset}{focos}\n")
print(f"\n{green}PRECIPITAÇÃO\n{reset}{prec}\n")
print(f"\n{green}TEMPERATURA MÍNIMA\n{reset}{tmin}\n")
print(f"\n{green}TEMPERATURA MÉDIA\n{reset}{tmed}\n")
print(f"\n{green}TEMPERATURA MÁXIMA\n{reset}{tmax}\n")
print(f"\n{green}CASOS (Série Histórica)\n{reset}{serie_casos}\n")
print(f"\n{green}FOCOS (Série Histórica)\n{reset}{serie_focos}\n")
print(f"\n{green}PRECIPITAÇÃO (Série Histórica)\n{reset}{serie_prec}\n")
print(f"\n{green}TEMPERATURA MÍNIMA (Série Histórica)\n{reset}{serie_tmin}\n")
print(f"\n{green}TEMPERATURA MÉDIA (Série Histórica)\n{reset}{serie_tmed}\n")
print(f"\n{green}TEMPERATURA MÁXIMA (Série Histórica)\n{reset}{serie_tmax}\n")

### Pré-Processamento

joinville = pd.DataFrame()
joinville["semana"] = focos["semana_epi"]
joinville["casos"] = casos["JOINVILLE"]
joinville["focos"] = focos["JOINVILLE"]
joinville["prec"] = prec["JOINVILLE"]
joinville["tmin"] = tmin["JOINVILLE"]
joinville["tmed"] = tmed["JOINVILLE"]
joinville["tmax"] = tmax["JOINVILLE"]
print(f"\n{green}JOINVILLE\n{reset}{joinville}\n")
sys.exit()

### Visualização Gráfica
fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = joinville.index, y = joinville["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(joinville.index, joinville["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = joinville.index, y = joinville["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(joinville.index, joinville["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper right")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = joinville["semana"], y = joinville["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower right")
sns.lineplot(x = joinville.index, y = joinville["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = joinville.index, y = joinville["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = joinville.index, y = joinville["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA O MUNICÍPIO DE JOINVILLE, SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_joinville.pdf"
caminho_estatistica = "/home/sifapsc/scripts/matheus/dengue/resultados/estatistica/sazonalidade/"
#if _SALVAR == True:
os.makedirs(caminho_estatistica, exist_ok = True)
#plt.savefig(f'{caminho_estatistica}{nome_arquivo}', format = "pdf", dpi = 300,  bbox_inches = "tight", pad_inches = 0.0)
print(f"""\n{green}SALVO COM SUCESSO!\n
{cyan}ENCAMINHAMENTO: {caminho_estatistica}\n
NOME DO ARQUIVO: {nome_arquivo}{reset}\n""")
#if _VISUALIZAR == True:
print(f"\n{cyan}Visualizando:\n{caminho_estatistica}{nome_arquivo}\n{reset}")
plt.show()	
