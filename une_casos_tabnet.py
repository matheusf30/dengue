"""
#################################################################################################
REGISTRO SINAN/SC >>>(DATASUS)
Atentar aos dados provenientes do TabNet... https://tabnet.datasus.gov.br/

--Seleções:
>>> LINHAS: Município de Infecção;
>>> COLUNAS: Semana Epidemilógica dos 1ºs sinais.

--Períodos:
>>> Haverá um arquivo por ano.

--Seleções Disponíveis(Filtros):
>>> UF F.infecção: 42 Santa Catarina (Desconsiderados todas as outras UFs, Ignorado e Exterior);

>>> Classificação Final: Dengue Clássico, Dengue com Complicações, Febre Hemorrágica do Dengue,
                         Síndrome do Choque do Dengue, Dengue e Dengue com Sinais de alarme.
(Nesse filtro foram desconsiderados: Ignorado, Branco, Descartado e Inconclusivo);

>>> Critério de Confirmação: Laboratorial e Clínico-Epidemiológico.
(Nesse filtro foram desconsiderados: Ignorado, Branco e Em Investigação);

>>>(Também não foram filtrados por sorotipo, pois não há confirmação laboratorial de todos.)

#################################################################################################
REGISTRO SINAN/SC >>>(DIVESC)
Atentar aos dados provenientes do TabNet... http://200.19.223.105/cgi-bin/dh?sinan/def/dengon.def

--Seleções:
>>> LINHAS: Município de Infecção SC;
>>> COLUNAS: Semana Epidemilógica dos 1ºs sinais.

--Períodos:
>>> Haverá um arquivo por ano.

--Seleções Disponíveis(Filtros):
>>> UF F.infecção: 42 Santa Catarina (Desconsiderados todas as outras UFs, Ignorado e Exterior);

>>> Classificação Nova: Dengue Clássico, Dengue com Complicações, Febre Hemorrágica do Dengue,
                         Síndrome do Choque do Dengue, Dengue e Dengue com Sinais de alarme.
(Nesse filtro foram desconsiderados: Ignorado, Branco, Descartado e Inconclusivo);

>>> Conf.Desc pos2010: Laboratorial e Clínico-Epidemiológico.
(Nesse filtro foram desconsiderados: Ignorado, Branco e Em Investigação);

>>>(Também não foram filtrados por sorotipo, pois não há confirmação laboratorial de todos.)
#################################################################################################
"""

### Bibliotecas Correlatas
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
import sys, os, warnings

original_filter = warnings.filters[:]
warnings.simplefilter("ignore", category = UserWarning)


### Encaminhamento aos Diretórios
_local = "IFSC" # OPÇÕES>>> "GH" | "CASA" | "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")

print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Apresentação de Abertura
print("""
Este roteiro automatiza os casos ao ponto de salvar xy.
Similar acontece aos focos ao executar sequencialmente:
- une_focos_dive.py;
- focos_timespace.py;
- focos_pivot.py;
""")

## Dados "Brutos"
_fonte = "DIVESC" # DIVESC" | "DATASUS"
if _fonte == "DATASUS":
	print("""
Casos Prováveis por Semana epidem. 1º Sintomas(s) segundo Município infecção
UF F.infecção: 42 Santa Catarina
Class. Final: Dengue Clássico, Dengue com complicações, Febre Hemorrágica do Dengue, Síndrome do Choque do Dengue, Dengue, Dengue com sinais de alarme
Criterio conf.: Laboratórial, Clínico-epidemiológico
Período: 2014 - [...]
 Fonte: Ministério da Saúde/SVSA - Sistema de Informação de Agravos de Notificação - Sinan Net

Notas:

    Para os casos prováveis foram incluídas todas notificações, exceto casos descartados.
    As bases de dados de dengue aqui disponíveis compõem um banco único a partir de 2014, podendo haver pequenas divergências com os dados disponibilizados pelo CGARB (Coordenação Geral de Vigilância de Arboviroses - CGARB) em sua série histórica, que para tal, realiza análise ano a ano, com a base congelada para cada ano analisado.
    Para tabular os casos graves (classificação final igual a dengue com complicações, febre hemorrágica da dengue, síndrome do choque da dengue, dengue com sinais de alarme e dengue grave) é necessário considerar também o critério de confirmação (laboratorial e clínico-epidemiológico).
    A partir de 2020 o estado do Espírito Santo passou a utilizar o sistema e-SUS Vigilância em Saúde. Portanto, para os casos de Arboviroses urbanas do Espírito Santo foram considerados apenas os dados disponibilizados pelo Sinan online (dengue e chikungunya) e Sinan Net (zika).
    Períodos Disponíveis ou período - Correspondem aos anos de notificação dos casos e semana epidemiológica, em cada período pode apresentar notificações com data de notificação do ano anterior (semana epidemiológica 52 ou 53) e posterior (semana epidemiológica 01).
    Para cálculo da incidência recomenda-se utilizar locais de residência.
    Dados de 2014 atualizados em 13/07/2015.
    Dados de 2015 atualizados em 27/09/2016.
    Dados de 2016 atualizados em 06/07/2017.
    Dados de 2017 atualizados em 18/07/2018.
    Dados de 2018 atualizados em 01/10/2019.
    Dados de 2019 atualizados em 10/07/2020.
    Dados de 2020 atualizados em 23/07/2021.
    Dados de 2021 atualizados em 12/07/2022.
    Dados de 2022 atualizados em 18/07/2023.
    Dados de 2023 atualizados em 04/03/2024 à 01 hora, sujeitos à revisão.
    Dados de 2024 atualizados em 11/03/2024 às 08 horas, sujeitos à revisão.
<<<<<<< HEAD

=======
>>>>>>> 72ec65a... Iniciando com dados brutos TabNet/DiveSC.
    * Dados disponibilizados no TABNET em março de 2024. 

Legenda:
-	- Dado numérico igual a 0 não resultante de arredondamento.
0; 0,0	- Dado numérico igual a 0 resultante de arredondamento de um dado originalmente positivo.
""")
elif _fonte == "DIVESC":
	print("""
 INVESTIGAÇÃO DENGUE A PARTIR DE 2014
Frequência por Mun infec SC e Sem.Epid.Sintomas
Classificacao Nova: Dengue com complicações, Febre Hemorrágica do Dengue, Síndrome do Choque do Dengue, Dengue, Dengue com sinais de alarme, Dengre grave
Conf.Desc pos2010: Laboratórial, Clínico-epidemiológico
Período: {ANO_ESCOLHIDO}
l igual a dengue com complicações, febre hemorrágica da dengue, síndrome do choque da dengue, dengue com sinais de alarme e dengue grave) é necessário considerar também o critério de confirmação (laboratorial e clínico-epidemiológico).
    A partir de 2020 o estado do Espírito Santo passou a utilizar o sistema e-SUS Vigilância em Saúde. Portanto, para os casos de Arboviroses urbanas do Espírito Santo foram considerados apenas os dados disponibilizados pelo Sinan online (dengue e chikungunya) e Sinan Net (zika).
    Períodos Disponíveis ou período - Correspondem aos anos de notificação dos casos e semana epidemiológica, em cada período pode apresentar notificações com data de notificação do ano anterior (semana epidemiológica 52 ou 53) e posterior (semana epidemiológica 01).
    Para cálculo da incidência recomenda-se utilizar locais de residência.
    Dados de 2014 atualizados em 13/07/2015.
    Dados de 2015 atualizados em 27/09/2016.
    Dados de 2016 atualizados em 06/07/2017.
    Dados de 2017 atualizados em 18/07/2018.
    Dados de 2018 atualizados em 01/10/2019.
    Dados de 2019 atualizados em 10/07/2020.
    Dados de 2020 atualizados em 23/07/2021.
    Dados de 2021 atualizados em 12/07/2022.
    Dados de 2022 atualizados em 18/07/2023.
    Dados de 2023 atualizados em 04/03/2024 à 01 hora, sujeitos à revisão.
    Dados de 2024 atualizados em 11/03/2024 às 08 horas, sujeitos à revisão.
<<<<<<< HEAD

=======
>>>>>>> 72ec65a... Iniciando com dados brutos TabNet/DiveSC.
    * Dados disponibilizados no TABNET em março de 2024. 

Legenda:
-	- Dado numérico igual a 0 não resultante de arredondamento.
0; 0,0	- Dado numérico igual a 0 resultante de arredondamento de um dado originalmente positivo.
""")
else:
	print("REAVALIAR FONTE DOS DADOS BRUTOS!")

### Renomeação variáveis pelos arquivos
municipios = "shapefiles/SC_Municipios_2022.shp"
# Fonte: TABNET/DATASUS - SINAN/SC
if _fonte == "DATASUS":
	casos14 = "sinannet_denguebsc_2014.csv"
	casos15 = "sinannet_denguebsc_2015.csv"
	casos16 = "sinannet_denguebsc_2016.csv"
	casos17 = "sinannet_denguebsc_2017.csv"
	casos18 = "sinannet_denguebsc_2018.csv"
	casos19 = "sinannet_denguebsc_2019.csv"
	casos20 = "sinannet_denguebsc_2020.csv"
	casos23 = "sinannet_denguebsc_2023.csv"
# Fonte: TABNET/DATASUS - SINAN/SC
elif _fonte == "DIVESC":
	casos14 = "dive_dengue_2014.csv"
	casos15 = "dive_dengue_2015.csv"
	casos16 = "dive_dengue_2016.csv"
	casos17 = "dive_dengue_2017.csv"
	casos18 = "dive_dengue_2018.csv"
	casos19 = "dive_dengue_2019.csv"
	casos20 = "dive_dengue_2020.csv"
	casos21 = "dive_dengue_2021.csv"
	casos22 = "dive_dengue_2022.csv"
	casos23 = "dive_dengue_2023.csv"
	casos24 = "dive_dengue_2024.csv"
else:
	print("Favor, revalidar a fonte dos dados brutos!")

### Abrindo Arquivos
municipios = gpd.read_file(f"{caminho_dados}{municipios}", low_memory = False)
if _fonte == "DATASUS":
	casos14 = pd.read_csv(f"{caminho_dados}{casos14}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos15 = pd.read_csv(f"{caminho_dados}{casos15}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos16 = pd.read_csv(f"{caminho_dados}{casos16}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos17 = pd.read_csv(f"{caminho_dados}{casos17}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos18 = pd.read_csv(f"{caminho_dados}{casos18}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos19 = pd.read_csv(f"{caminho_dados}{casos19}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos20 = pd.read_csv(f"{caminho_dados}{casos20}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
	casos23 = pd.read_csv(f"{caminho_dados}{casos23}", skiprows = 6, skipfooter = 26,
                          sep = ";", encoding = "latin1", engine = "python")
elif _fonte == "DIVESC":
	casos14 = pd.read_csv(f"{caminho_dados}{casos14}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos15 = pd.read_csv(f"{caminho_dados}{casos15}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos16 = pd.read_csv(f"{caminho_dados}{casos16}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos17 = pd.read_csv(f"{caminho_dados}{casos17}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos18 = pd.read_csv(f"{caminho_dados}{casos18}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos19 = pd.read_csv(f"{caminho_dados}{casos19}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos20 = pd.read_csv(f"{caminho_dados}{casos20}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos21 = pd.read_csv(f"{caminho_dados}{casos21}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos22 = pd.read_csv(f"{caminho_dados}{casos22}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos23 = pd.read_csv(f"{caminho_dados}{casos23}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")
	casos24 = pd.read_csv(f"{caminho_dados}{casos24}", skiprows = 5,
                          sep = ";", encoding = "latin1", engine = "python")

### Pré-Processamento
lista_municipio = {'ABDON BATISTA': 'ABDON BATISTA',
  'ABELARDO LUZ': 'ABELARDO LUZ',
  'AGROLANDIA': 'AGROLÂNDIA',
  'AGRONOMICA': 'AGRONÔMICA',
  'AGUA DOCE': 'ÁGUA DOCE',
  'AGUAS DE CHAPECO': 'ÁGUAS DE CHAPECÓ',
  'AGUAS FRIAS': 'ÁGUAS FRIAS',
  'AGUAS MORNAS': 'ÁGUAS MORNAS',
  'ALFREDO WAGNER': 'ALFREDO WAGNER',
  'ALTO BELA VISTA': 'ALTO BELA VISTA',
  'ANCHIETA': 'ANCHIETA',
  'ANGELINA': 'ANGELINA',
  'ANITA GARIBALDI': 'ANITA GARIBALDI',
  'ANITAPOLIS': 'ANITÁPOLIS',
  'ANTONIO CARLOS': 'ANTÔNIO CARLOS',
  'APIUNA': 'APIÚNA',
  'ARABUTA': 'ARABUTÃ',
  'ARAQUARI': 'ARAQUARI',
  'ARARANGUA': 'ARARANGUÁ',
  'ARMAZEM': 'ARMAZÉM',
  'ARROIO TRINTA': 'ARROIO TRINTA',
  'ARVOREDO': 'ARVOREDO',
  'ASCURRA': 'ASCURRA',
  'ATALANTA': 'ATALANTA',
  'AURORA': 'AURORA',
  'BALNEARIO ARROIO DO SILVA': 'BALNEÁRIO ARROIO DO SILVA',
  'BALNEARIO CAMBORIU': 'BALNEÁRIO CAMBORIÚ',
  'BALNEARIO BARRA DO SUL': 'BALNEÁRIO BARRA DO SUL',
  'BALNEARIO GAIVOTA': 'BALNEÁRIO GAIVOTA',
  'BANDEIRANTE': 'BANDEIRANTE',
  'BARRA BONITA': 'BARRA BONITA',
  'BARRA VELHA': 'BARRA VELHA',
  'BELA VISTA DO TOLDO': 'BELA VISTA DO TOLDO',
  'BELMONTE': 'BELMONTE',
  'BENEDITO NOVO': 'BENEDITO NOVO',
  'BIGUACU': 'BIGUAÇU',
  'BLUMENAU': 'BLUMENAU',
  'BOCAINA DO SUL': 'BOCAINA DO SUL',
  'BOMBINHAS': 'BOMBINHAS',
  'BOM JARDIM DA SERRA': 'BOM JARDIM DA SERRA',
  'BOM JESUS': 'BOM JESUS',
  'BOM JESUS DO OESTE': 'BOM JESUS DO OESTE',
  'BOM RETIRO': 'BOM RETIRO',
  'BOTUVERA': 'BOTUVERÁ',
  'BRACO DO NORTE': 'BRAÇO DO NORTE',
  'BRACO DO TROMBUDO': 'BRAÇO DO TROMBUDO',
  'BRUNOPOLIS': 'BRUNÓPOLIS',
  'BRUSQUE': 'BRUSQUE',
  'CACADOR': 'CAÇADOR',
  'CAIBI': 'CAIBI',
  'CALMON': 'CALMON',
  'CAMBORIU': 'CAMBORIÚ',
  'CAPAO ALTO': 'CAPÃO ALTO',
  'CAMPO ALEGRE': 'CAMPO ALEGRE',
  'CAMPO BELO DO SUL': 'CAMPO BELO DO SUL',
  'CAMPO ERE': 'CAMPO ERÊ',
  'CAMPOS NOVOS': 'CAMPOS NOVOS',
  'CANELINHA': 'CANELINHA',
  'CANOINHAS': 'CANOINHAS',
  'CAPINZAL': 'CAPINZAL',
  'CAPIVARI DE BAIXO': 'CAPIVARI DE BAIXO',
  'CATANDUVAS': 'CATANDUVAS',
  'CAXAMBU DO SUL': 'CAXAMBU DO SUL',
  'CELSO RAMOS': 'CELSO RAMOS',
  'CERRO NEGRO': 'CERRO NEGRO',
  'CHAPADAO DO LAGEADO': 'CHAPADÃO DO LAGEADO',
  'CHAPECO': 'CHAPECÓ',
  'COCAL DO SUL': 'COCAL DO SUL',
  'CONCORDIA': 'CONCÓRDIA',
  'CORDILHEIRA ALTA': 'CORDILHEIRA ALTA',
  'CORONEL FREITAS': 'CORONEL FREITAS',
  'CORONEL MARTINS': 'CORONEL MARTINS',
  'CORUPA': 'CORUPÁ',
  'CORREIA PINTO': 'CORREIA PINTO',
  'CRICIUMA': 'CRICIÚMA',
  'CUNHA PORA': 'CUNHA PORÃ',
  'CUNHATAO': 'CUNHATAÍ',
  'CURITIBANOS': 'CURITIBANOS',
  'DESCANSO': 'DESCANSO',
  'DIONOSIO CERQUEIRA': 'DIONÍSIO CERQUEIRA',
  'DONA EMMA': 'DONA EMMA',
  'DOUTOR PEDRINHO': 'DOUTOR PEDRINHO',
  'ENTRE RIOS': 'ENTRE RIOS',
  'ERMO': 'ERMO',
  'ERVAL VELHO': 'ERVAL VELHO',
  'FAXINAL DOS GUEDES': 'FAXINAL DOS GUEDES',
  'FLOR DO SERTAO': 'FLOR DO SERTÃO',
  'FLORIANOPOLIS': 'FLORIANÓPOLIS',
  'FORMOSA DO SUL': 'FORMOSA DO SUL',
  'FORQUILHINHA': 'FORQUILHINHA',
  'FRAIBURGO': 'FRAIBURGO',
  'FREI ROGERIO': 'FREI ROGÉRIO',
  'GALVAO': 'GALVÃO',
  'GAROPABA': 'GAROPABA',
  'GARUVA': 'GARUVA',
  'GASPAR': 'GASPAR',
  'GOVERNADOR CELSO RAMOS': 'GOVERNADOR CELSO RAMOS',
  'GRAO PARA': 'GRÃO-PARÁ',
  'GRAVATAL': 'GRAVATAL',
  'GUABIRUBA': 'GUABIRUBA',
  'GUARACIABA': 'GUARACIABA',
  'GUARAMIRIM': 'GUARAMIRIM',
  'GUARUJA DO SUL': 'GUARUJÁ DO SUL',
  'GUATAMBU': 'GUATAMBÚ',
  'HERVAL D OESTE': "HERVAL D'OESTE",
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
  'IPORA DO OESTE': 'IPORÃ DO OESTE',
  'IPUACU': 'IPUAÇU',
  'IPUMIRIM': 'IPUMIRIM',
  'IRACEMINHA': 'IRACEMINHA',
  'IRANI': 'IRANI',
  'IRATI': 'IRATI',
  'IRINEOPOLIS': 'IRINEÓPOLIS',
  'ITA': 'ITÁ',
  'ITAIOPOLIS': 'ITAIÓPOLIS',
  'ITAJAI': 'ITAJAÍ',
  'ITAPEMA': 'ITAPEMA',
  'ITAPIRANGA': 'ITAPIRANGA',
  'ITAPOA': 'ITAPOÁ',
  'ITUPORANGA': 'ITUPORANGA',
  'JABORA': 'JABORÁ',
  'JACINTO MACHADO': 'JACINTO MACHADO',
  'JAGUARUNA': 'JAGUARUNA',
  'JARAGUA DO SUL': 'JARAGUÁ DO SUL',
  'JARDINOPOLIS': 'JARDINÓPOLIS',
  'JOACABA': 'JOAÇABA',
  'JOINVILLE': 'JOINVILLE',
  'JOSE BOITEUX': 'JOSÉ BOITEUX',
  'JUPIA': 'JUPIÁ',
  'LACERDOPOLIS': 'LACERDÓPOLIS',
  'LAGES': 'LAGES',
  'LAGUNA': 'LAGUNA',
  'LAJEADO GRANDE': 'LAJEADO GRANDE',
  'LAURENTINO': 'LAURENTINO',
  'LAURO MULLER': 'LAURO MÜLLER',
  'LEBON REGIS': 'LEBON RÉGIS',
  'LEOBERTO LEAL': 'LEOBERTO LEAL',
  'LINDOIA DO SUL': 'LINDÓIA DO SUL',
  'LONTRAS': 'LONTRAS',
  'LUIZ ALVES': 'LUIZ ALVES',
  'LUZERNA': 'LUZERNA',
  'MACIEIRA': 'MACIEIRA',
  'MAFRA': 'MAFRA',
  'MAJOR GERCINO': 'MAJOR GERCINO',
  'MAJOR VIEIRA': 'MAJOR VIEIRA',
  'MARACAJA': 'MARACAJÁ',
  'MARAVILHA': 'MARAVILHA',
  'MAREMA': 'MAREMA',
  'MASSARANDUBA': 'MASSARANDUBA',
  'MATOS COSTA': 'MATOS COSTA',
  'MELEIRO': 'MELEIRO',
  'MIRIM DOCE': 'MIRIM DOCE',
  'MODELO': 'MODELO',
  'MONDAO': 'MONDAÍ',
  'MONTE CARLO': 'MONTE CARLO',
  'MONTE CASTELO': 'MONTE CASTELO',
  'MORRO DA FUMACA': 'MORRO DA FUMAÇA',
  'MORRO GRANDE': 'MORRO GRANDE',
  'NAVEGANTES': 'NAVEGANTES',
  'NOVA ERECHIM': 'NOVA ERECHIM',
  'NOVA ITABERABA': 'NOVA ITABERABA',
  'NOVA TRENTO': 'NOVA TRENTO',
  'NOVA VENEZA': 'NOVA VENEZA',
  'NOVO HORIZONTE': 'NOVO HORIZONTE',
  'ORLEANS': 'ORLEANS',
  'OTACOLIO COSTA': 'OTACÍLIO COSTA',
  'OURO': 'OURO',
  'OURO VERDE': 'OURO VERDE',
  'PAIAL': 'PAIAL',
  'PAINEL': 'PAINEL',
  'PALHOCA': 'PALHOÇA',
  'PALMA SOLA': 'PALMA SOLA',
  'PALMEIRA': 'PALMEIRA',
  'PALMITOS': 'PALMITOS',
  'PAPANDUVA': 'PAPANDUVA',
  'PARAOSO': 'PARAÍSO',
  'PASSO DE TORRES': 'PASSO DE TORRES',
  'PASSOS MAIA': 'PASSOS MAIA',
  'PAULO LOPES': 'PAULO LOPES',
  'PEDRAS GRANDES': 'PEDRAS GRANDES',
  'PENHA': 'PENHA',
  'PERITIBA': 'PERITIBA',
  'PESCARIA BRAVA': 'PESCARIA BRAVA',
  'PETROLANDIA': 'PETROLÂNDIA',
  'BALNEARIO PICARRAS': 'BALNEÁRIO PIÇARRAS',
  'PINHALZINHO': 'PINHALZINHO',
  'PINHEIRO PRETO': 'PINHEIRO PRETO',
  'PIRATUBA': 'PIRATUBA',
  'PLANALTO ALEGRE': 'PLANALTO ALEGRE',
  'POMERODE': 'POMERODE',
  'PONTE ALTA': 'PONTE ALTA',
  'PONTE ALTA DO NORTE': 'PONTE ALTA DO NORTE',
  'PONTE SERRADA': 'PONTE SERRADA',
  'PORTO BELO': 'PORTO BELO',
  'PORTO UNIAO': 'PORTO UNIÃO',
  'POUSO REDONDO': 'POUSO REDONDO',
  'PRAIA GRANDE': 'PRAIA GRANDE',
  'PRESIDENTE CASTELLO BRANCO': 'PRESIDENTE CASTELLO BRANCO',
  'PRESIDENTE GETULIO': 'PRESIDENTE GETÚLIO',
  'PRESIDENTE NEREU': 'PRESIDENTE NEREU',
  'PRINCESA': 'PRINCESA',
  'QUILOMBO': 'QUILOMBO',
  'RANCHO QUEIMADO': 'RANCHO QUEIMADO',
  'RIO DAS ANTAS': 'RIO DAS ANTAS',
  'RIO DO CAMPO': 'RIO DO CAMPO',
  'RIO DO OESTE': 'RIO DO OESTE',
  'RIO DOS CEDROS': 'RIO DOS CEDROS',
  'RIO DO SUL': 'RIO DO SUL',
  'RIO FORTUNA': 'RIO FORTUNA',
  'RIO NEGRINHO': 'RIO NEGRINHO',
  'RIO RUFINO': 'RIO RUFINO',
  'RIQUEZA': 'RIQUEZA',
  'RODEIO': 'RODEIO',
  'ROMELANDIA': 'ROMELÂNDIA',
  'SALETE': 'SALETE',
  'SALTINHO': 'SALTINHO',
  'SALTO VELOSO': 'SALTO VELOSO',
  'SANGAO': 'SANGÃO',
  'SANTA CECOLIA': 'SANTA CECÍLIA',
  'SANTA HELENA': 'SANTA HELENA',
  'SANTA ROSA DE LIMA': 'SANTA ROSA DE LIMA',
  'SANTA ROSA DO SUL': 'SANTA ROSA DO SUL',
  'SANTA TEREZINHA': 'SANTA TEREZINHA',
  'SANTA TEREZINHA DO PROGRESSO': 'SANTA TEREZINHA DO PROGRESSO',
  'SANTIAGO DO SUL': 'SANTIAGO DO SUL',
  'SANTO AMARO DA IMPERATRIZ': 'SANTO AMARO DA IMPERATRIZ',
  'SAO BERNARDINO': 'SÃO BERNARDINO',
  'SAO BENTO DO SUL': 'SÃO BENTO DO SUL',
  'SAO BONIFACIO': 'SÃO BONIFÁCIO',
  'SAO CARLOS': 'SÃO CARLOS',
  'SAO CRISTOVAO DO SUL': 'SÃO CRISTÓVÃO DO SUL',
  'SAO DOMINGOS': 'SÃO DOMINGOS',
  'SAO FRANCISCO DO SUL': 'SÃO FRANCISCO DO SUL',
  'SAO JOAO DO OESTE': 'SÃO JOÃO DO OESTE',
  'SAO JOAO BATISTA': 'SÃO JOÃO BATISTA',
  'SAO JOAO DO ITAPERIU': 'SÃO JOÃO DO ITAPERIÚ',
  'SAO JOAO DO SUL': 'SÃO JOÃO DO SUL',
  'SAO JOAQUIM': 'SÃO JOAQUIM',
  'SAO JOSE': 'SÃO JOSÉ',
  'SAO JOSE DO CEDRO': 'SÃO JOSÉ DO CEDRO',
  'SAO JOSE DO CERRITO': 'SÃO JOSÉ DO CERRITO',
  'SAO LOURENCO DO OESTE': 'SÃO LOURENÇO DO OESTE',
  'SAO LUDGERO': 'SÃO LUDGERO',
  'SAO MARTINHO': 'SÃO MARTINHO',
  'SAO MIGUEL DA BOA VISTA': 'SÃO MIGUEL DA BOA VISTA',
  'SAO MIGUEL DO OESTE': 'SÃO MIGUEL DO OESTE',
  'SAO PEDRO DE ALCANTARA': 'SÃO PEDRO DE ALCÂNTARA',
  'SAUDADES': 'SAUDADES',
  'SCHROEDER': 'SCHROEDER',
  'SEARA': 'SEARA',
  'SERRA ALTA': 'SERRA ALTA',
  'SIDEROPOLIS': 'SIDERÓPOLIS',
  'SOMBRIO': 'SOMBRIO',
  'SUL BRASIL': 'SUL BRASIL',
  'TAIO': 'TAIÓ',
  'TANGARA': 'TANGARÁ',
  'TIGRINHOS': 'TIGRINHOS',
  'TIJUCAS': 'TIJUCAS',
  'TIMBE DO SUL': 'TIMBÉ DO SUL',
  'TIMBO': 'TIMBÓ',
  'TIMBO GRANDE': 'TIMBÓ GRANDE',
  'TRES BARRAS': 'TRÊS BARRAS',
  'TREVISO': 'TREVISO',
  'TREZE DE MAIO': 'TREZE DE MAIO',
  'TREZE TOLIAS': 'TREZE TÍLIAS',
  'TROMBUDO CENTRAL': 'TROMBUDO CENTRAL',
  'TUBARAO': 'TUBARÃO',
  'TUNAPOLIS': 'TUNÁPOLIS',
  'TURVO': 'TURVO',
  'UNIAO DO OESTE': 'UNIÃO DO OESTE',
  'URUBICI': 'URUBICI',
  'URUPEMA': 'URUPEMA',
  'URUSSANGA': 'URUSSANGA',
  'VARGEAO': 'VARGEÃO',
  'VARGEM': 'VARGEM',
  'VARGEM BONITA': 'VARGEM BONITA',
  'VIDAL RAMOS': 'VIDAL RAMOS',
  'VIDEIRA': 'VIDEIRA',
  'VITOR MEIRELES': 'VITOR MEIRELES',
  'WITMARSUM': 'WITMARSUM',
  'XANXERE': 'XANXERÊ',
  'XAVANTINA': 'XAVANTINA',
  'XAXIM': 'XAXIM',
  'ZORTEA': 'ZORTÉA',
  'BALNEARIO RINCAO': 'BALNEÁRIO RINCÃO'}

#os.system("clear")

# 2014
ano = 2014
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 5)
fim = datetime(ano, 12, 28)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos14.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos14.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos14.rename(columns = dict_semanas, inplace = True)
casos14["Município"] = casos14["Município"].str.replace("\d+ ", "", regex = True)
casos14["Município"] = casos14["Município"].str.upper()
casos14.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos14.drop(casos14.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos14.drop(casos14.index[-1:], axis = 0, inplace = True)
casos14.set_index("Município", inplace = True)
casos14 = casos14.T
casos14.reset_index(inplace=True)
casos14 = casos14.rename(columns = {"index" : "Semana"})
casos14.rename(columns = lista_municipio, inplace = True)
colunas = casos14.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos14["Semana"] = pd.to_datetime(casos14["Semana"])
casos14 = pd.merge(semanas, casos14, on = "Semana", how = "left").fillna(0)
casos14[colunas] = casos14[colunas].astype(int)
casos14 = pd.melt(casos14, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
#  value_vars = None, usa o restante de colunas para sair do pivot.
casos14.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos14)
print(casos14.info())
print(casos14.columns.drop("Semana"))
print("="*80)

# 2015
ano = 2015
total_semana = 53
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 4)
fim = datetime(ano, 12, 27)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos15.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos15.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos15.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos15.rename(columns = dict_semanas, inplace = True)
casos15["Município"] = casos15["Município"].str.replace("\d+ ", "", regex = True)
casos15["Município"] = casos15["Município"].str.upper()
casos15.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos15.drop(casos15.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos15.drop(casos15.index[-1:], axis = 0, inplace = True)
casos15.set_index("Município", inplace = True)
casos15 = casos15.T
casos15.reset_index(inplace=True)
casos15 = casos15.rename(columns = {"index" : "Semana"})
casos15.rename(columns = lista_municipio, inplace = True)
colunas = casos15.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos15["Semana"] = pd.to_datetime(casos15["Semana"])
casos15 = pd.merge(semanas, casos15, on = "Semana", how = "left").fillna(0)
casos15[colunas] = casos15[colunas].astype(int)
casos15 = casos15[casos15["Semana"] != "Semana 53"]
casos15 = pd.melt(casos15, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos15.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos15)
print(casos15.info())
print(casos15.columns.drop("Semana"))
print("="*80)

# 2016
ano = 2016
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 3)
fim = datetime(ano, 12, 25)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos16.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos16.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos16.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos16.rename(columns = dict_semanas, inplace = True)
casos16["Município"] = casos16["Município"].str.replace("\d+ ", "", regex = True)
casos16["Município"] = casos16["Município"].str.upper()
casos16.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos16.drop(casos16.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos16.drop(casos16.index[-1:], axis = 0, inplace = True)
casos16.set_index("Município", inplace = True)
casos16 = casos16.T
casos16.reset_index(inplace=True)
casos16 = casos16.rename(columns = {"index" : "Semana"})
casos16.rename(columns = lista_municipio, inplace = True)
colunas = casos16.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos16["Semana"] = pd.to_datetime(casos16["Semana"])
casos16 = pd.merge(semanas, casos16, on = "Semana", how = "left").fillna(0)
casos16[colunas] = casos16[colunas].astype(int)
casos16 = pd.melt(casos16, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos16.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos16)
print(casos16.info())
print(casos16.columns.drop("Semana"))
print("="*80)

# 2017
ano = 2017
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 1)
fim = datetime(ano, 12, 31)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos17.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos17.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos17.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos17.rename(columns = dict_semanas, inplace = True)
casos17["Município"] = casos17["Município"].str.replace("\d+ ", "", regex = True)
casos17["Município"] = casos17["Município"].str.upper()
casos17.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos17.drop(casos17.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos17.drop(casos17.index[-1:], axis = 0, inplace = True)
casos17.set_index("Município", inplace = True)
casos17 = casos17.T
casos17.reset_index(inplace=True)
casos17 = casos17.rename(columns = {"index" : "Semana"})
casos17.rename(columns = lista_municipio, inplace = True)
colunas = casos17.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos17["Semana"] = pd.to_datetime(casos17["Semana"])
casos17 = pd.merge(semanas, casos17, on = "Semana", how = "left").fillna(0)
casos17[colunas] = casos17[colunas].astype(int)
casos17 = pd.melt(casos17, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos17.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos17)
print(casos17.info())
print(casos17.columns.drop("Semana"))
print("="*80)

# 2018
ano = 2018
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 7)
fim = datetime(ano, 12, 30)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos18.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos18.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos18.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos18.rename(columns = dict_semanas, inplace = True)
casos18["Município"] = casos18["Município"].str.replace("\d+ ", "", regex = True)
casos18["Município"] = casos18["Município"].str.upper()
casos18.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos18.drop(casos18.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos18.drop(casos18.index[-1:], axis = 0, inplace = True)
casos18.set_index("Município", inplace = True)
casos18 = casos18.T
casos18.reset_index(inplace=True)
casos18 = casos18.rename(columns = {"index" : "Semana"})
casos18.rename(columns = lista_municipio, inplace = True)
colunas = casos18.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos18["Semana"] = pd.to_datetime(casos18["Semana"])
casos18 = pd.merge(semanas, casos18, on = "Semana", how = "left").fillna(0)
casos18[colunas] = casos18[colunas].astype(int)
casos18 = pd.melt(casos18, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos18.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos18)
print(casos18.info())
print(casos18.columns.drop("Semana"))
print("="*80)

# 2019
ano = 2019
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 6)
fim = datetime(ano, 12, 29)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos19.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos19.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos19.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos19.rename(columns = dict_semanas, inplace = True)
casos19["Município"] = casos19["Município"].str.replace("\d+ ", "", regex = True)
casos19["Município"] = casos19["Município"].str.upper()
casos19.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos19.drop(casos19.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos19.drop(casos19.index[-1:], axis = 0, inplace = True)
casos19.set_index("Município", inplace = True)
casos19 = casos19.T
casos19.reset_index(inplace=True)
casos19 = casos19.rename(columns = {"index" : "Semana"})
casos19.rename(columns = lista_municipio, inplace = True)
colunas = casos19.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos19["Semana"] = pd.to_datetime(casos19["Semana"])
casos19 = pd.merge(semanas, casos19, on = "Semana", how = "left").fillna(0)
casos19[colunas] = casos19[colunas].astype(int)
casos19 = pd.melt(casos19, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos19.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos19)
print(casos19.info())
print(casos19.columns.drop("Semana"))
print("="*80)

# 2020
ano = 2020
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 5)
fim = datetime(ano, 12, 27)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos20.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos20.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos20.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos20.rename(columns = dict_semanas, inplace = True)
casos20["Município"] = casos20["Município"].str.replace("\d+ ", "", regex = True)
casos20["Município"] = casos20["Município"].str.upper()
casos20.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos20.drop(casos20.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos20.drop(casos20.index[-1:], axis = 0, inplace = True)
casos20.set_index("Município", inplace = True)
casos20 = casos20.T
casos20.reset_index(inplace=True)
casos20 = casos20.rename(columns = {"index" : "Semana"})
casos20.rename(columns = lista_municipio, inplace = True)
colunas = casos20.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos20["Semana"] = pd.to_datetime(casos20["Semana"])
casos20 = pd.merge(semanas, casos20, on = "Semana", how = "left").fillna(0)
casos20[colunas] = casos20[colunas].astype(int)
casos20 = pd.melt(casos20, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos20.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos20)
print(casos20.info())
print(casos20.columns.drop("Semana"))
print("="*80)

if _fonte == "DIVESC":
	# 2021
	ano = 2021
	total_semana = 52
	lista_str_semanas = []
	for i in range(1, total_semana + 1):
		n_semana = str(i).zfill(2)
		chave_semana = f"Semana {n_semana}"
		lista_str_semanas.append(chave_semana)
	inicio = datetime(ano, 1, 3)
	fim = datetime(ano, 12, 26)
	lista_semanas = []
	semana_corrente = inicio
	while semana_corrente <= fim:
		lista_semanas.append(semana_corrente)
		semana_corrente += timedelta(weeks = 1)
	dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
	if _fonte == "DATASUS":
		casos21.rename(columns = {"Município infecção" : "Município"}, inplace = True)
	elif _fonte == "DIVESC":
		casos21.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
	casos21.rename(columns = {"Município infecção" : "Município"}, inplace = True)
	casos21.rename(columns = dict_semanas, inplace = True)
	casos21["Município"] = casos21["Município"].str.replace("\d+ ", "", regex = True)
	casos21["Município"] = casos21["Município"].str.upper()
	casos21.drop(columns = "Total", inplace = True)
	if _fonte == "DATASUS":
		casos21.drop(casos21.index[-2:], axis = 0, inplace = True)
	elif _fonte == "DIVESC":
		casos21.drop(casos21.index[-1:], axis = 0, inplace = True)
	casos21.set_index("Município", inplace = True)
	casos21 = casos21.T
	casos21.reset_index(inplace=True)
	casos21 = casos21.rename(columns = {"index" : "Semana"})
	casos21.rename(columns = lista_municipio, inplace = True)
	colunas = casos21.columns.drop("Semana")
	semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
	casos21["Semana"] = pd.to_datetime(casos21["Semana"])
	casos21 = pd.merge(semanas, casos21, on = "Semana", how = "left").fillna(0)
	casos21[colunas] = casos21[colunas].astype(int)
	casos21 = pd.melt(casos21, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
	casos21.sort_values(by = "Semana",  ignore_index = True, inplace = True)
	print("="*80, f"\n{ano}\n\n", casos21)
	print(casos21.info())
	print(casos21.columns.drop("Semana"))
	print("="*80)

	# 2022
	ano = 2022
	total_semana = 52
	lista_str_semanas = []
	for i in range(1, total_semana + 1):
		n_semana = str(i).zfill(2)
		chave_semana = f"Semana {n_semana}"
		lista_str_semanas.append(chave_semana)
	inicio = datetime(ano, 1, 2)
	fim = datetime(ano, 12, 25)
	lista_semanas = []
	semana_corrente = inicio
	while semana_corrente <= fim:
		lista_semanas.append(semana_corrente)
		semana_corrente += timedelta(weeks = 1)
	dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
	if _fonte == "DATASUS":
		casos22.rename(columns = {"Município infecção" : "Município"}, inplace = True)
	elif _fonte == "DIVESC":
		casos22.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
	casos22.rename(columns = {"Município infecção" : "Município"}, inplace = True)
	casos22.rename(columns = dict_semanas, inplace = True)
	casos22["Município"] = casos22["Município"].str.replace("\d+ ", "", regex = True)
	casos22["Município"] = casos22["Município"].str.upper()
	casos22.drop(columns = "Total", inplace = True)
	if _fonte == "DATASUS":
		casos22.drop(casos22.index[-2:], axis = 0, inplace = True)
	elif _fonte == "DIVESC":
		casos22.drop(casos22.index[-1:], axis = 0, inplace = True)
	casos22.set_index("Município", inplace = True)
	casos22 = casos22.T
	casos22.reset_index(inplace=True)
	casos22 = casos22.rename(columns = {"index" : "Semana"})
	casos22.rename(columns = lista_municipio, inplace = True)
	colunas = casos22.columns.drop("Semana")
	semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
	casos22["Semana"] = pd.to_datetime(casos22["Semana"])
	casos22 = pd.merge(semanas, casos22, on = "Semana", how = "left").fillna(0)
	casos22[colunas] = casos22[colunas].astype(int)
	casos22 = pd.melt(casos22, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
	casos22.sort_values(by = "Semana",  ignore_index = True, inplace = True)
	print("="*80, f"\n{ano}\n\n", casos22)
	print(casos22.info())
	print(casos22.columns.drop("Semana"))
	print("="*80)

# 2023
ano = 2023
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano, 1, 1)
fim = datetime(ano, 12, 31)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos23.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos23.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos23.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos23.rename(columns = dict_semanas, inplace = True)
casos23["Município"] = casos23["Município"].str.replace("\d+ ", "", regex = True)
casos23["Município"] = casos23["Município"].str.upper()
casos23.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos23.drop(casos23.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos23.drop(casos23.index[-1:], axis = 0, inplace = True)
casos23.set_index("Município", inplace = True)
casos23 = casos23.T
casos23.reset_index(inplace=True)
casos23 = casos23.rename(columns = {"index" : "Semana"})
casos23.rename(columns = lista_municipio, inplace = True)
colunas = casos23.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos23["Semana"] = pd.to_datetime(casos23["Semana"])
casos23 = pd.merge(semanas, casos23, on = "Semana", how = "left").fillna(0)
casos23[colunas] = casos23[colunas].astype(int)
casos23 = pd.melt(casos23, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos23.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos23)
print(casos23.info())
print(casos23.columns.drop("Semana"))
print("="*80)

# 2024
ano = 2024
total_semana = 52
lista_str_semanas = []
for i in range(1, total_semana + 1):
    n_semana = str(i).zfill(2)
    chave_semana = f"Semana {n_semana}"
    lista_str_semanas.append(chave_semana)
inicio = datetime(ano-1, 12, 31)
fim = datetime(ano, 12, 28)
lista_semanas = []
semana_corrente = inicio
while semana_corrente <= fim:
    lista_semanas.append(semana_corrente)
    semana_corrente += timedelta(weeks = 1)
dict_semanas = dict(zip(lista_str_semanas, [date.strftime("%Y-%m-%d") for date in lista_semanas]))
if _fonte == "DATASUS":
	casos24.rename(columns = {"Município infecção" : "Município"}, inplace = True)
elif _fonte == "DIVESC":
	casos24.rename(columns = {"Mun infec SC" : "Município"}, inplace = True)
casos24.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos24.rename(columns = dict_semanas, inplace = True)
casos24["Município"] = casos24["Município"].str.replace("\d+ ", "", regex = True)
casos24["Município"] = casos24["Município"].str.upper()
casos24.drop(columns = "Total", inplace = True)
if _fonte == "DATASUS":
	casos24.drop(casos24.index[-2:], axis = 0, inplace = True)
elif _fonte == "DIVESC":
	casos24.drop(casos24.index[-1:], axis = 0, inplace = True)
casos24.set_index("Município", inplace = True)
casos24 = casos24.T
casos24.reset_index(inplace=True)
casos24 = casos24.rename(columns = {"index" : "Semana"})
casos24.rename(columns = lista_municipio, inplace = True)
colunas = casos24.columns.drop("Semana")
semanas = pd.DataFrame(lista_semanas, columns=["Semana"])
casos24["Semana"] = pd.to_datetime(casos24["Semana"])
casos24 = pd.merge(semanas, casos24, on = "Semana", how = "left").fillna(0)
casos24[colunas] = casos24[colunas].astype(int)
casos24 = pd.melt(casos24, id_vars = "Semana", var_name = "Município", value_name = "Casos", ignore_index = True)
casos24.sort_values(by = "Semana",  ignore_index = True, inplace = True)
print("="*80, f"\n{ano}\n\n", casos24)
print(casos24.info())
print(casos24.columns.drop("Semana"))
print("="*80)

prepandemia = pd.concat([casos14, casos15, casos16, casos17, casos18, casos19], ignore_index = True)
pospandemia = pd.concat([casos20, casos21, casos22, casos23, casos24], ignore_index = True)
casostotal = pd.concat([prepandemia, pospandemia], ignore_index = True)
casos_pivot = pd.pivot_table(casostotal, index = "Semana", columns = "Município", values = "Casos", fill_value = 0)
casos_pivot.reset_index(inplace = True)
casos_pivot_pospandemia = pd.pivot_table(pospandemia, index = "Semana", columns = "Município", values = "Casos", fill_value = 0)
casos_pivot_pospandemia.reset_index(inplace = True)
unicos = casostotal[casostotal["Casos"] > 0].drop_duplicates(subset = ["Município"])
municipios["Município"] = municipios["NM_MUN"].str.upper()
cidades = municipios[["Município", "geometry"]]
cidades = cidades.to_crs(municipios.crs) # SIRGAS 2000/22S ("EPSG:31982") | IBGE.shp ("EPSG:4674")
cidades["centroide"] = cidades["geometry"].centroid
cidades["latitude"] = cidades["geometry"].centroid.y
cidades["longitude"] = cidades["geometry"].centroid.x
xy = cidades[["Município", "latitude", "longitude"]]
unicos_xy = pd.merge(unicos, xy, on = "Município", how = "left")

warnings.filters = original_filter

### Salvando Arquivo
cidades.to_csv(f"{caminho_dados}municipios_coordenadas.csv", index = False)
unicos_xy.to_csv(f"{caminho_dados}casos_primeiros.csv", index = False)
if _fonte == "DATASUS":
	casostotal.to_csv(f"{caminho_dados}casos_sinan_total.csv", index = False)
	casos_pivot.to_csv(f"{caminho_dados}casos_sinan_pivot_total.csv", index = False)
	pospandemia.to_csv(f"{caminho_dados}casos_sinan_pospandemia.csv", index = False)
	casos_pivot_pospandemia.to_csv(f"{caminho_dados}casos_sinan_pivot_pospandemia.csv", index = False)
elif _fonte == "DIVESC":
	casostotal.to_csv(f"{caminho_dados}casos_dive_total.csv", index = False)
	casos_pivot.to_csv(f"{caminho_dados}casos_dive_pivot_total.csv", index = False)
	pospandemia.to_csv(f"{caminho_dados}casos_dive_pospandemia.csv", index = False)
	casos_pivot_pospandemia.to_csv(f"{caminho_dados}casos_dive_pivot_pospandemia.csv", index = False)


### Printando Informações
print("\n \n CASOS DE DENGUE EM SANTA CATARINA ANTES DA PANDEMIA \n")
print(prepandemia.info())
print("~"*80)
print(prepandemia.dtypes)
print("~"*80)
print(prepandemia)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA DURANTE E APÓS PANDEMIA \n")
print(pospandemia.info())
print("~"*80)
print(pospandemia.dtypes)
print("~"*80)
print(pospandemia)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(casostotal.info())
print("~"*80)
print(casostotal.dtypes)
print("~"*80)
print(casostotal)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA (PIVOT) \n")
print(casos_pivot_pospandemia.info())
print("~"*80)
print(casos_pivot_pospandemia.dtypes)
print("~"*80)
print(casos_pivot_pospandemia)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - 1º REGISTRO NA SÉRIE HISTÓRICA \n")
print(unicos_xy.info())
print("~"*80)
print(unicos_xy.dtypes)
print("~"*80)
print(unicos_xy)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - 1º REGISTRO NA SÉRIE HISTÓRICA \n")
print(cidades.info())
print("~"*80)
print(cidades.dtypes)
print("~"*80)
print(cidades)
print("="*80)
print(f"Coordinate Reference System (CRS)\nIBGE.shp: {municipios.crs}\n(Instituto Brasileiro de Geografia e Estatística)")
print("="*80)
