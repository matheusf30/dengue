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

### Renomeação das Variáveis pelos Arquivos
casos = "sazonalidade_semanal_casos.csv"
focos = "sazonalidade_semanal_focos.csv"
prec = "sazonalidade_semanal_prec.csv"
tmin = "sazonalidade_semanal_tmin.csv"
tmed = "sazonalidade_semanal_tmed.csv"
tmax = "sazonalidade_semanal_tmax.csv"
serie_casos = "casos_dive_pivot_total.csv"
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

### Regiões Climáticas (Caio Guerra de Oliveira, 2023)
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

oeste = ['Abelardo Luz', 'Alto Bela Vista', 'Anchieta', 'Arabutã', 'Arvoredo', 'Bandeirante', 'Barra Bonita', 'Belmonte', 'Bom Jesus', 'Bom Jesus do Oeste', 'Caibi', 'Campo Erê', 'Caxambu do Sul', 'Chapecó', 'Concórdia', 'Cordilheira Alta', 'Coronel Freitas', 'Coronel Martins', 'Cunha Porã', 'Cunhataí', 'Descanso', 'Dionísio Cerqueira', 'Entre Rios', 'Faxinal dos Guedes', 'Flor do Sertão', 'Formosa do Sul', 'Galvão', 'Guaraciaba', 'Guarujá do Sul', 'Guatambú', 'Iporã do Oeste', 'Ipuaçu', 'Ipumirim', 'Iraceminha', 'Irani', 'Irati', 'Itapiranga', 'Itá', 'Jaborá', 'Jardinópolis', 'Jupiá', 'Lajeado Grande', 'Lindóia do Sul', 'Maravilha', 'Marema', 'Modelo', 'Mondaí', 'Nova Erechim', 'Nova Itaberaba', 'Novo Horizonte', 'Ouro Verde', 'Paial', 'Palma Sola', 'Palmitos', 'Paraíso', 'Peritiba', 'Pinhalzinho', 'Planalto Alegre', 'Presidente Castello Branco', 'Princesa', 'Quilombo', 'Riqueza', 'Romelândia', 'Saltinho', 'Santa Helena', 'Santa Terezinha do Progresso', 'Santiago do Sul', 'Saudades', 'Seara', 'Serra Alta', 'Sul Brasil', 'São Bernardino', 'São Carlos', 'São Domingos', 'São José do Cedro', 'São João do Oeste', 'São Lourenço do Oeste', 'São Miguel da Boa Vista', 'São Miguel do Oeste', 'Tigrinhos', 'Tunápolis', 'União do Oeste', 'Vargeão', 'Xanxerê', 'Xavantina', 'Xaxim', 'Águas Frias', 'Águas de Chapecó']
meio_oeste = ['Abdon Batista', 'Anita Garibaldi', 'Arroio Trinta', 'Bocaina do Sul', 'Brunópolis', 'Campo Belo do Sul', 'Campos Novos', 'Capinzal', 'Capão Alto', 'Catanduvas', 'Caçador', 'Celso Ramos', 'Cerro Negro', 'Correia Pinto', 'Curitibanos', 'Erval Velho', 'Fraiburgo', 'Frei Rogério', "Herval d'Oeste", 'Ibiam', 'Ibicaré', 'Iomerê', 'Ipira', 'Joaçaba', 'Lacerdópolis', 'Lages', 'Lebon Régis', 'Luzerna', 'Macieira', 'Monte Carlo', 'Otacílio Costa', 'Ouro', 'Palmeira', 'Passos Maia', 'Pinheiro Preto', 'Piratuba', 'Ponte Alta', 'Ponte Alta do Norte', 'Ponte Serrada', 'Rio das Antas', 'Salto Veloso', 'Santa Cecília', 'São Cristóvão do Sul', 'São José do Cerrito', 'Tangará', 'Treze Tílias', 'Vargem', 'Vargem Bonita', 'Videira', 'Zortéa', 'Água Doce']
planalto_norte = ['Agrolândia', 'Agronômica', 'Atalanta', 'Aurora', 'Bela Vista do Toldo', 'Braço do Trombudo', 'Calmon', 'Campo Alegre', 'Canoinhas', 'Chapadão do Lageado', 'Corupá', 'Dona Emma', 'Doutor Pedrinho', 'Ibirama', 'Imbuia', 'Irineópolis', 'Itaiópolis', 'Ituporanga', 'José Boiteux', 'Laurentino', 'Lontras', 'Mafra', 'Major Vieira', 'Matos Costa', 'Mirim Doce', 'Monte Castelo', 'Papanduva', 'Petrolândia', 'Porto União', 'Pouso Redondo', 'Presidente Getúlio', 'Rio Negrinho', 'Rio do Campo', 'Rio do Oeste', 'Rio do Sul', 'Salete', 'Santa Terezinha', 'São Bento do Sul', 'Taió', 'Timbó Grande', 'Trombudo Central', 'Três Barras', 'Vitor Meireles', 'Witmarsum']
planalto_sul = ['Bom Jardim da Serra', 'Bom Retiro', 'Painel', 'Rio Rufino', 'São Joaquim', 'Urubici', 'Urupema']
litoral_norte = ['Alfredo Wagner', 'Angelina', 'Antônio Carlos', 'Apiúna', 'Araquari', 'Ascurra', 'Balneário Barra do Sul', 'Balneário Camboriú', 'Balneário Piçarras', 'Barra Velha', 'Benedito Novo', 'Biguaçu', 'Blumenau', 'Botuverá', 'Brusque', 'Camboriú', 'Canelinha', 'Florianópolis', 'Garuva', 'Gaspar', 'Governador Celso Ramos', 'Guabiruba', 'Guaramirim', 'Ilhota', 'Indaial', 'Itajaí', 'Itapema', 'Itapoá', 'Jaraguá do Sul', 'Joinville', 'Leoberto Leal', 'Luiz Alves', 'Major Gercino', 'Massaranduba', 'Navegantes', 'Nova Trento', 'Palhoça', 'Penha', 'Pomerode', 'Porto Belo', 'Presidente Nereu', 'Rancho Queimado', 'Rio dos Cedros', 'Rodeio', 'Santo Amaro da Imperatriz', 'Schroeder', 'São Francisco do Sul', 'São José', 'São João Batista', 'São João do Itaperiú', 'São Pedro de Alcântara', 'Tijucas', 'Timbó', 'Vidal Ramos', 'Águas Mornas']
litoral_sul = ['Anitápolis', 'Araranguá', 'Armazém', 'Balneário Arroio do Silva', 'Balneário Gaivota', 'Balneário Rincão', 'Braço do Norte', 'Capivari de Baixo', 'Cocal do Sul', 'Criciúma', 'Ermo', 'Forquilhinha', 'Garopaba', 'Gravatal', 'Grão-Pará', 'Imaruí', 'Imbituba', 'Içara', 'Jacinto Machado', 'Jaguaruna', 'Laguna', 'Lauro Müller', 'Maracajá', 'Meleiro', 'Morro Grande', 'Morro da Fumaça', 'Nova Veneza', 'Orleans', 'Passo de Torres', 'Paulo Lopes', 'Pedras Grandes', 'Pescaria Brava', 'Praia Grande', 'Rio Fortuna', 'Sangão', 'Santa Rosa de Lima', 'Santa Rosa do Sul', 'Siderópolis', 'Sombrio', 'São Bonifácio', 'São João do Sul', 'São Ludgero', 'São Martinho', 'Timbé do Sul', 'Treviso', 'Treze de Maio', 'Tubarão', 'Turvo', 'Urussanga']
oeste = [municipio.upper() for municipio in oeste]
meio_oeste = [municipio.upper() for municipio in meio_oeste]
planalto_norte = [municipio.upper() for municipio in planalto_norte]
planalto_sul = [municipio.upper() for municipio in planalto_sul]
litoral_norte = [municipio.upper() for municipio in litoral_norte]
litoral_sul = [municipio.upper() for municipio in litoral_sul]
#sys.exit()

### Pré-Processamento
# PRECIPITAÇÃO
oeste_clima_prec = prec[oeste]
oeste_clima_prec["prec"] = prec[oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO OESTE\n{reset}{oeste_clima_prec}\n")
meio_oeste_clima_prec = prec[meio_oeste]
meio_oeste_clima_prec["prec"] = prec[meio_oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO MEIO OESTE\n{reset}{meio_oeste_clima_prec}\n")
planalto_norte_clima_prec = prec[planalto_norte]
planalto_norte_clima_prec["prec"] = prec[planalto_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO PLANALTO NORTE\n{reset}{planalto_norte_clima_prec}\n")
planalto_sul_clima_prec = prec[planalto_sul]
planalto_sul_clima_prec["prec"] = prec[planalto_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO PLANALTO SUL\n{reset}{planalto_sul_clima_prec}\n")
litoral_norte_clima_prec = prec[litoral_norte]
litoral_norte_clima_prec["prec"] = prec[litoral_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO LITORAL NORTE\n{reset}{litoral_norte_clima_prec}\n")
litoral_sul_clima_prec = prec[litoral_sul]
litoral_sul_clima_prec["prec"] = prec[litoral_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA PRECIPITAÇÃO LITORAL SUL\n{reset}{litoral_sul_clima_prec}\n")
#sys.exit()

# TEMPERATURA MÍNIMA
oeste_clima_tmin = tmin[oeste]
oeste_clima_tmin["tmin"] = tmin[oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA OESTE\n{reset}{oeste_clima_tmin}\n")
meio_oeste_clima_tmin = tmin[meio_oeste]
meio_oeste_clima_tmin["tmin"] = tmin[meio_oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA MEIO OESTE\n{reset}{meio_oeste_clima_tmin}\n")
planalto_norte_clima_tmin = tmin[planalto_norte]
planalto_norte_clima_tmin["tmin"] = tmin[planalto_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA PLANALTO NORTE\n{reset}{planalto_norte_clima_tmin}\n")
planalto_sul_clima_tmin = tmin[planalto_sul]
planalto_sul_clima_tmin["tmin"] = tmin[planalto_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA PLANALTO SUL\n{reset}{planalto_sul_clima_tmin}\n")
litoral_norte_clima_tmin = tmin[litoral_norte]
litoral_norte_clima_tmin["tmin"] = tmin[litoral_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA LITORAL NORTE\n{reset}{litoral_norte_clima_tmin}\n")
litoral_sul_clima_tmin = tmin[litoral_sul]
litoral_sul_clima_tmin["tmin"] = tmin[litoral_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÍNIMA LITORAL SUL\n{reset}{litoral_sul_clima_tmin}\n")

# TEMPERATURA MÉDIA
oeste_clima_tmed = tmed[oeste]
oeste_clima_tmed["tmed"] = tmed[oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA OESTE\n{reset}{oeste_clima_tmed}\n")
meio_oeste_clima_tmed = tmed[meio_oeste]
meio_oeste_clima_tmed["tmed"] = tmed[meio_oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA MEIO OESTE\n{reset}{meio_oeste_clima_tmed}\n")
planalto_norte_clima_tmed = tmed[planalto_norte]
planalto_norte_clima_tmed["tmed"] = tmed[planalto_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA PLANALTO NORTE\n{reset}{planalto_norte_clima_tmed}\n")
planalto_sul_clima_tmed = tmed[planalto_sul]
planalto_sul_clima_tmed["tmed"] = tmed[planalto_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA PLANALTO SUL\n{reset}{planalto_sul_clima_tmed}\n")
litoral_norte_clima_tmed = tmed[litoral_norte]
litoral_norte_clima_tmed["tmed"] = tmed[litoral_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA LITORAL NORTE\n{reset}{litoral_norte_clima_tmed}\n")
litoral_sul_clima_tmed = tmed[litoral_sul]
litoral_sul_clima_tmed["tmed"] = tmed[litoral_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÉDIA LITORAL SUL\n{reset}{litoral_sul_clima_tmed}\n")

# TEMPERATURA MÁXIMA
oeste_clima_tmax = tmax[oeste]
oeste_clima_tmax["tmax"] = tmax[oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA OESTE\n{reset}{oeste_clima_tmax}\n")
meio_oeste_clima_tmax = tmax[meio_oeste]
meio_oeste_clima_tmax["tmax"] = tmax[meio_oeste].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA MEIO OESTE\n{reset}{meio_oeste_clima_tmax}\n")
planalto_norte_clima_tmax = tmax[planalto_norte]
planalto_norte_clima_tmax["tmax"] = tmax[planalto_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA PLANALTO NORTE\n{reset}{planalto_norte_clima_tmax}\n")
planalto_sul_clima_tmax = tmax[planalto_sul]
planalto_sul_clima_tmax["tmax"] = tmax[planalto_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA PLANALTO SUL\n{reset}{planalto_sul_clima_tmax}\n")
litoral_norte_clima_tmax = tmax[litoral_norte]
litoral_norte_clima_tmax["tmax"] = tmax[litoral_norte].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA LITORAL NORTE\n{reset}{litoral_norte_clima_tmax}\n")
litoral_sul_clima_tmax = tmax[litoral_sul]
litoral_sul_clima_tmax["tmax"] = tmax[litoral_sul].mean(axis = 1)
print(f"\n{green}CLIMATOLOGIA TEMPERATURA MÁXIMA LITORAL SUL\n{reset}{litoral_sul_clima_tmax}\n")

# CASOS
oeste_casos = [cidade for cidade in oeste if cidade in casos.columns]
oeste_clima_casos = casos[oeste_casos]
oeste_clima_casos["casos"] = casos[oeste_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS OESTE\n{reset}{oeste_clima_casos}\n")
meio_oeste_casos = [cidade for cidade in meio_oeste if cidade in casos.columns]
meio_oeste_clima_casos = casos[meio_oeste_casos]
meio_oeste_clima_casos["casos"] = casos[meio_oeste_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS MEIO OESTE\n{reset}{meio_oeste_clima_casos}\n")
planalto_norte_casos = [cidade for cidade in planalto_norte if cidade in casos.columns]
planalto_norte_clima_casos = casos[planalto_norte_casos]
planalto_norte_clima_casos["casos"] = casos[planalto_norte_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS PLANALTO NORTE\n{reset}{planalto_norte_clima_casos}\n")
planalto_sul_casos = [cidade for cidade in planalto_sul if cidade in casos.columns]
planalto_sul_clima_casos = casos[planalto_sul_casos]
planalto_sul_clima_casos["casos"] = casos[planalto_sul_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS PLANALTO SUL\n{reset}{planalto_sul_clima_casos}\n")
litoral_norte_casos = [cidade for cidade in litoral_norte if cidade in casos.columns]
litoral_norte_clima_casos = casos[litoral_norte_casos]
litoral_norte_clima_casos["casos"] = casos[litoral_norte_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS LITORAL NORTE\n{reset}{litoral_norte_clima_casos}\n")
litoral_sul_casos = [cidade for cidade in litoral_sul if cidade in casos.columns]
litoral_sul_clima_casos = casos[litoral_sul_casos]
litoral_sul_clima_casos["casos"] = casos[litoral_sul_casos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA CASOS LITORAL SUL\n{reset}{litoral_sul_clima_casos}\n")

# FOCOS
oeste_focos = [cidade for cidade in oeste if cidade in focos.columns]
oeste_clima_focos = focos[oeste_focos]
oeste_clima_focos["focos"] = focos[oeste_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS OESTE\n{reset}{oeste_clima_focos}\n")
meio_oeste_focos = [cidade for cidade in meio_oeste if cidade in focos.columns]
meio_oeste_clima_focos = focos[meio_oeste_focos]
meio_oeste_clima_focos["focos"] = focos[meio_oeste_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS MEIO OESTE\n{reset}{meio_oeste_clima_focos}\n")
planalto_norte_focos = [cidade for cidade in planalto_norte if cidade in focos.columns]
planalto_norte_clima_focos = focos[planalto_norte_focos]
planalto_norte_clima_focos["focos"] = focos[planalto_norte_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS PLANALTO NORTE\n{reset}{planalto_norte_clima_focos}\n")
planalto_sul_focos = [cidade for cidade in planalto_sul if cidade in focos.columns]
planalto_sul_clima_focos = focos[planalto_sul_focos]
planalto_sul_clima_focos["focos"] = focos[planalto_sul_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS PLANALTO SUL\n{reset}{planalto_sul_clima_focos}\n")
litoral_norte_focos = [cidade for cidade in litoral_norte if cidade in focos.columns]
litoral_norte_clima_focos = focos[litoral_norte_focos]
litoral_norte_clima_focos["focos"] = focos[litoral_norte_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS LITORAL NORTE\n{reset}{litoral_norte_clima_focos}\n")
litoral_sul_focos = [cidade for cidade in litoral_sul if cidade in focos.columns]
litoral_sul_clima_focos = focos[litoral_sul_focos]
litoral_sul_clima_focos["focos"] = focos[litoral_sul_focos].sum(axis = 1)
print(f"\n{green}CLIMATOLOGIA FOCOS LITORAL SUL\n{reset}{litoral_sul_clima_focos}\n")
#sys.exit()

### Organizando em DataFrames/Regiões Climatológicas
# OESTE
df_oeste = pd.DataFrame()
df_oeste["prec"] = oeste_clima_prec["prec"]
df_oeste["tmin"] = oeste_clima_tmin["tmin"]
df_oeste["tmed"] = oeste_clima_tmed["tmed"]
df_oeste["tmax"] = oeste_clima_tmax["tmax"]
df_oeste["casos"] = oeste_clima_casos["casos"]
df_oeste["focos"] = oeste_clima_focos["focos"]
df_oeste["semana"] = range(1, len(df_oeste) +1)
df_oeste = df_oeste[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA OESTE\n{reset}{df_oeste}\n")
df_oeste.to_csv(f"{caminho_dados}caio_clima_oeste.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_oeste.csv{reset}\n")

# MEIO OESTE
df_meio_oeste = pd.DataFrame()
df_meio_oeste["prec"] = meio_oeste_clima_prec["prec"]
df_meio_oeste["tmin"] = meio_oeste_clima_tmin["tmin"]
df_meio_oeste["tmed"] = meio_oeste_clima_tmed["tmed"]
df_meio_oeste["tmax"] = meio_oeste_clima_tmax["tmax"]
df_meio_oeste["casos"] = meio_oeste_clima_casos["casos"]
df_meio_oeste["focos"] = meio_oeste_clima_focos["focos"]
df_meio_oeste["semana"] = range(1, len(df_meio_oeste) +1)
df_meio_oeste = df_meio_oeste[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA MEIO OESTE\n{reset}{df_meio_oeste}\n")
df_meio_oeste.to_csv(f"{caminho_dados}caio_clima_meio_oeste.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_meio_oeste.csv{reset}\n")

# PLANALDO NORTE
df_planalto_norte = pd.DataFrame()
df_planalto_norte["prec"] = planalto_norte_clima_prec["prec"]
df_planalto_norte["tmin"] = planalto_norte_clima_tmin["tmin"]
df_planalto_norte["tmed"] = planalto_norte_clima_tmed["tmed"]
df_planalto_norte["tmax"] = planalto_norte_clima_tmax["tmax"]
df_planalto_norte["casos"] = planalto_norte_clima_casos["casos"]
df_planalto_norte["focos"] = planalto_norte_clima_focos["focos"]
df_planalto_norte["semana"] = range(1, len(df_planalto_norte) +1)
df_planalto_norte = df_planalto_norte[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA PLANALDO NORTE\n{reset}{df_planalto_norte}\n")
df_planalto_norte.to_csv(f"{caminho_dados}caio_clima_planalto_norte.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_planalto_norte.csv{reset}\n")

# PLANALDO SUL
df_planalto_sul = pd.DataFrame()
df_planalto_sul["prec"] = planalto_sul_clima_prec["prec"]
df_planalto_sul["tmin"] = planalto_sul_clima_tmin["tmin"]
df_planalto_sul["tmed"] = planalto_sul_clima_tmed["tmed"]
df_planalto_sul["tmax"] = planalto_sul_clima_tmax["tmax"]
df_planalto_sul["casos"] = planalto_sul_clima_casos["casos"]
df_planalto_sul["focos"] = planalto_sul_clima_focos["focos"]
df_planalto_sul["semana"] = range(1, len(df_planalto_sul) +1)
df_planalto_sul = df_planalto_sul[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA PLANALDO SUL\n{reset}{df_planalto_sul}\n")
df_planalto_sul.to_csv(f"{caminho_dados}caio_clima_planalto_sul.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_planalto_sul.csv{reset}\n")

# LITORAL NORTE
df_litoral_norte = pd.DataFrame()
df_litoral_norte["prec"] = litoral_norte_clima_prec["prec"]
df_litoral_norte["tmin"] = litoral_norte_clima_tmin["tmin"]
df_litoral_norte["tmed"] = litoral_norte_clima_tmed["tmed"]
df_litoral_norte["tmax"] = litoral_norte_clima_tmax["tmax"]
df_litoral_norte["casos"] = litoral_norte_clima_casos["casos"]
df_litoral_norte["focos"] = litoral_norte_clima_focos["focos"]
df_litoral_norte["semana"] = range(1, len(df_litoral_norte) +1)
df_litoral_norte = df_litoral_norte[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA LITORAL NORTE\n{reset}{df_litoral_norte}\n")
df_litoral_norte.to_csv(f"{caminho_dados}caio_clima_litoral_norte.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_litoral_norte.csv{reset}\n")

# LITORAL SUL
df_litoral_sul = pd.DataFrame()
df_litoral_sul["prec"] = litoral_sul_clima_prec["prec"]
df_litoral_sul["tmin"] = litoral_sul_clima_tmin["tmin"]
df_litoral_sul["tmed"] = litoral_sul_clima_tmed["tmed"]
df_litoral_sul["tmax"] = litoral_sul_clima_tmax["tmax"]
df_litoral_sul["casos"] = litoral_sul_clima_casos["casos"]
df_litoral_sul["focos"] = litoral_sul_clima_focos["focos"]
df_litoral_sul["semana"] = range(1, len(df_litoral_sul) +1)
df_litoral_sul = df_litoral_sul[["semana", "prec", "tmin", "tmed", "tmax", "casos", "focos"]]
print(f"\n{green}CLIMATOLOGIA LITORAL SUL\n{reset}{df_litoral_sul}\n")
df_litoral_sul.to_csv(f"{caminho_dados}caio_clima_litoral_sul.csv", index = False)
print(f"\n{green}SALVO COM SUCESSO\n{cyan}{caminho_dados}caio_clima_litoral_sul.csv{reset}\n")



#sys.exit()

### Visualização Gráfica MURI

#gráfico oeste
fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = df_oeste.index, y = df_oeste["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(df_oeste.index, df_oeste["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = df_oeste.index, y = df_oeste["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(df_oeste.index, df_oeste["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper right")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = df_oeste["semana"], y = df_oeste["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower right")
sns.lineplot(x = df_oeste.index, y = df_oeste["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = df_oeste.index, y = df_oeste["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = df_oeste.index, y = df_oeste["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA A MESORREGIÃO CLIMÁTICA OESTE DE SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_oeste.jpeg"
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


#gráfico meio_oeste
fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = df_meio_oeste.index, y = df_meio_oeste["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(df_meio_oeste.index, df_meio_oeste["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = df_meio_oeste.index, y = df_meio_oeste["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(df_meio_oeste.index, df_meio_oeste["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper right")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = df_meio_oeste["semana"], y = df_meio_oeste["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower right")
sns.lineplot(x = df_meio_oeste.index, y = df_meio_oeste["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = df_meio_oeste.index, y = df_meio_oeste["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = df_meio_oeste.index, y = df_meio_oeste["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA A MESORREGIÃO CLIMÁTICA MEIO-OESTE DE SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_oeste.jpeg"
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


###visualização gráfica BIA

#Gráfico litoral Norte

fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = df_litoral_norte.index, y = df_litoral_norte["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(df_litoral_norte.index, df_litoral_norte["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = df_litoral_norte.index, y = df_litoral_norte["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(df_litoral_norte.index, df_litoral_norte["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper right")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = df_litoral_norte["semana"], y = df_litoral_norte["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower right")
sns.lineplot(x = df_litoral_norte.index, y = df_litoral_norte["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = df_litoral_norte.index, y = df_litoral_norte["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = df_litoral_norte.index, y = df_litoral_norte["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA A MESORREGIÃO LITORAL NORTE DE SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_litoral_norte.jpeg"
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


#Gráfico litoral_sul

fig, axs = plt.subplots(2, 1, figsize = (12, 6), layout = "tight", frameon = False,  sharex = True)
axs[0].set_facecolor("honeydew") #.gcf()
ax2 = axs[0].twinx()
sns.lineplot(x = df_litoral_sul.index, y = df_litoral_sul["casos"], ax = axs[0],
				color = "purple", linewidth = 1, linestyle = "--", label = "Casos de Dengue")
axs[0].fill_between(df_litoral_sul.index, df_litoral_sul["casos"], color = "purple", alpha = 0.3)
axs[0].set_ylabel("Casos de Dengue")
axs[0].legend(loc = "upper center")
sns.lineplot(x = df_litoral_sul.index, y = df_litoral_sul["focos"],  ax = ax2,
				color = "darkgreen", linewidth = 1, linestyle = ":", label = "Focos de _Aedes_ sp.")
ax2.fill_between(df_litoral_sul.index, df_litoral_sul["focos"], color = "darkgreen", alpha = 0.35)
ax2.set_ylabel("Focos de _Aedes_ sp.")
ax2.legend(loc = "upper right")
axs[1].set_facecolor("honeydew") #.gcf()
ax3 = axs[1].twinx()#.set_facecolor("honeydew")
sns.barplot(x = df_litoral_sul["semana"], y = df_litoral_sul["prec"],  ax = ax3,
				color = "royalblue", linewidth = 1.5, alpha = 0.8, label = "Precipitação")
ax3.set_ylabel("Precipitação (mm)")
ax3.legend(loc = "lower right")
sns.lineplot(x = df_litoral_sul.index, y = df_litoral_sul["tmin"],  ax = axs[1],
				color = "darkblue", linewidth = 1.5, label = "Temperatura Mínima")
sns.lineplot(x = df_litoral_sul.index, y = df_litoral_sul["tmed"],  ax = axs[1],
				color = "orange", linewidth = 1.5, label = "Temperatura Média")
sns.lineplot(x = df_litoral_sul.index, y = df_litoral_sul["tmax"],  ax = axs[1],
				color = "red", linewidth = 1.5, label = "Temperatura Máxima") #alpha = 0.7, linewidth = 3
axs[1].set_ylabel("Temperaturas (C)")
axs[1].legend(loc = "upper center")
axs[1].grid(False)
axs[1].set_xlabel("Semanas Epidemiológicas")
fig.suptitle(f"CASOS DE DENGUE, FOCOS DE _Aedes_ sp., TEMPERATURAS (MÍNIMA, MÉDIA E MÁXIMA) E PRECIPITAÇÃO.\nSAZONALIDADE POR MÉDIAS SEMANAIS PARA A MESORREGIÃO LITORAL SUL DE SANTA CATARINA.")
nome_arquivo = f"esbmet25_distribuicao_sazonal_subplots_litoral_sul.jpeg"
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
