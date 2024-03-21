"""
REGISTRO SINAN/SC
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
"""
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

    * Dados disponibilizados no TABNET em março de 2024. 

Legenda:
-	- Dado numérico igual a 0 não resultante de arredondamento.
0; 0,0	- Dado numérico igual a 0 resultante de arredondamento de um dado originalmente positivo.
""")

### Bibliotecas Correlatas
import pandas as pd
import numpy as np
import sys

### Encaminhamento aos Diretórios
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"
_www = True
if _www == True: # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
    caminho_modelos = "https://github.com/matheusf30/dados_dengue/tree/main/modelos"
else:
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
    caminho_modelos = "/home/sifapsc/scripts/matheus/dados_dengue/modelos/"
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n{caminho_modelos}")

### Renomeação variáveis pelos arquivos
## Dados "Brutos"
## Fonte: TABNET/DATASUS - SINAN/SC
casos = "casos.csv"
casos_se = "casos_se.csv"
casos14 = "sinannet_denguebsc_2014.csv"
casos15 = "sinannet_denguebsc_2015.csv"
casos16 = "sinannet_denguebsc_2016.csv"
casos17 = "sinannet_denguebsc_2017.csv"
casos18 = "sinannet_denguebsc_2018.csv"
casos19 = "sinannet_denguebsc_2019.csv"
casos20 = "sinannet_denguebsc_2020.csv"
casos23 = "sinannet_denguebsc_2023.csv"

### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
casos_se = pd.read_csv(f"{caminho_dados}{casos_se}")
casos14 = pd.read_csv(f"{caminho_dados}{casos14}", skiprows = 30, sep = ";", encoding = "latin1")
casos15 = pd.read_csv(f"{caminho_dados}{casos15}", skiprows = 30, sep = ";", encoding = "latin1")
casos16 = pd.read_csv(f"{caminho_dados}{casos16}", skiprows = 30, sep = ";", encoding = "latin1")
casos17 = pd.read_csv(f"{caminho_dados}{casos17}", skiprows = 30, sep = ";", encoding = "latin1")
casos18 = pd.read_csv(f"{caminho_dados}{casos18}", skiprows = 30, sep = ";", encoding = "latin1")
casos19 = pd.read_csv(f"{caminho_dados}{casos19}", skiprows = 30, sep = ";", encoding = "latin1")
casos20 = pd.read_csv(f"{caminho_dados}{casos20}", skiprows = 30, sep = ";", encoding = "latin1")
casos23 = pd.read_csv(f"{caminho_dados}{casos23}", skiprows = 30, sep = ";", encoding = "latin1")

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

casos14.rename(columns = {"Município infecção" : "Município"}, inplace = True)
casos14.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)
casos14["Município"] = casos14["Município"].str.replace("\d+ ", "", regex = True)
casos14.drop(columns = "Total", inplace = True)
casos14.drop(casos14.index[-2:], axis = 0, inplace = True)
casos14.set_index("Município", inplace = True)
casos14 = casos14.T
casos14.reset_index(inplace=True)
casos14 = casos14.rename(columns = {"index" : "Semana"})
casos14.rename(columns = lista_municipio, inplace = True)
colunas = casos14.columns.drop("Semana")
casos14[colunas] = casos14[colunas].replace("-", np.nan)
casos14[colunas] = casos14[colunas].astype(float)
casos14.fillna(0, inplace = True)
casos14[colunas] = casos14[colunas].astype(int)
print("\n2014\n", casos14)
print(casos14.info())
print(casos14.columns.drop("Semana"))

casos15.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos15.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos15["Município"] = casos15["Município"].str.replace("\d+ ", "", regex = True)
casos15.drop(columns = "Total", inplace = True)
casos15.drop(casos15.index[-2:], axis = 0, inplace = True)
casos15.set_index("Município", inplace = True)
casos15 = casos15.T
casos15.reset_index(inplace=True)
casos15 = casos15.rename(columns = {"index" : "Semana"})
casos15.rename(columns = lista_municipio, inplace = True)
colunas = casos15.columns.drop("Semana")
casos15[colunas] = casos15[colunas].replace("-", np.nan)
casos15[colunas] = casos15[colunas].astype(float)
casos15.fillna(0, inplace = True)
casos15[colunas] = casos15[colunas].astype(int)
print("\n2015\n", casos15)
print(casos15.info())
print(casos15.columns.drop("Semana"))

casos16.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos16.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos16["Município"] = casos16["Município"].str.replace("\d+ ", "", regex = True)
casos16.drop(columns = "Total", inplace = True)
casos16.drop(casos16.index[-2:], axis = 0, inplace = True)
casos16.set_index("Município", inplace = True)
casos16 = casos16.T
casos16.reset_index(inplace=True)
casos16 = casos16.rename(columns = {"index" : "Semana"})
casos16.rename(columns = lista_municipio, inplace = True)
colunas = casos16.columns.drop("Semana")
casos16[colunas] = casos16[colunas].replace("-", np.nan)
casos16[colunas] = casos16[colunas].astype(float)
casos16.fillna(0, inplace = True)
casos16[colunas] = casos16[colunas].astype(int)
print("\n2016\n", casos16)
print(casos16.info())
print(casos16.columns.drop("Semana"))

casos17.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos17.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos17["Município"] = casos17["Município"].str.replace("\d+ ", "", regex = True)
casos17.drop(columns = "Total", inplace = True)
casos17.drop(casos17.index[-2:], axis = 0, inplace = True)
casos17.set_index("Município", inplace = True)
casos17 = casos17.T
casos17.reset_index(inplace=True)
casos17 = casos17.rename(columns = {"index" : "Semana"})
casos17.rename(columns = lista_municipio, inplace = True)
colunas = casos17.columns.drop("Semana")
casos17[colunas] = casos17[colunas].replace("-", np.nan)
casos17[colunas] = casos17[colunas].astype(float)
casos17.fillna(0, inplace = True)
casos17[colunas] = casos17[colunas].astype(int)
print("\n2017\n", casos17)
print(casos17.info())
print(casos17.columns.drop("Semana"))

casos18.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos18.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos18["Município"] = casos18["Município"].str.replace("\d+ ", "", regex = True)
casos18.drop(columns = "Total", inplace = True)
casos18.drop(casos18.index[-2:], axis = 0, inplace = True)
casos18.set_index("Município", inplace = True)
casos18 = casos18.T
casos18.reset_index(inplace=True)
casos18 = casos18.rename(columns = {"index" : "Semana"})
casos18.rename(columns = lista_municipio, inplace = True)
colunas = casos18.columns.drop("Semana")
casos18[colunas] = casos18[colunas].replace("-", np.nan)
casos18[colunas] = casos18[colunas].astype(float)
casos18.fillna(0, inplace = True)
casos18[colunas] = casos18[colunas].astype(int)
print("\n2018\n", casos18)
print(casos18.info())
print(casos18.columns.drop("Semana"))


casos19.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos19.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos19["Município"] = casos19["Município"].str.replace("\d+ ", "", regex = True)
casos19.drop(columns = "Total", inplace = True)
casos19.drop(casos19.index[-2:], axis = 0, inplace = True)
casos19.set_index("Município", inplace = True)
casos19 = casos19.T
casos19.reset_index(inplace=True)
casos19 = casos19.rename(columns = {"index" : "Semana"})
casos19.rename(columns = lista_municipio, inplace = True)
colunas = casos19.columns.drop("Semana")
casos19[colunas] = casos19[colunas].replace("-", np.nan)
casos19[colunas] = casos19[colunas].astype(float)
casos19.fillna(0, inplace = True)
casos19[colunas] = casos19[colunas].astype(int)
print("\n2019\n", casos19)
print(casos19.info())
print(casos19.columns.drop("Semana"))

casos20.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos20.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos20["Município"] = casos20["Município"].str.replace("\d+ ", "", regex = True)
casos20.drop(columns = "Total", inplace = True)
casos20.drop(casos20.index[-2:], axis = 0, inplace = True)
casos20.set_index("Município", inplace = True)
casos20 = casos20.T
casos20.reset_index(inplace=True)
casos20 = casos20.rename(columns = {"index" : "Semana"})
casos20.rename(columns = lista_municipio, inplace = True)
colunas = casos20.columns.drop("Semana")
casos20[colunas] = casos20[colunas].replace("-", np.nan)
casos20[colunas] = casos20[colunas].astype(float)
casos20.fillna(0, inplace = True)
casos20[colunas] = casos20[colunas].astype(int)
print("\n2020\n", casos20)
print(casos20.info())
print(casos20.columns.drop("Semana"))

casos23.rename(columns = {"Município infecção" : "Município"}, inplace = True)
"""
casos23.rename(columns = {"Semana 14" : "2014-04-06", # YYYY-MM-DD
                          "Semana 15" : "2014-04-13",
                          "Semana 18" : "2014-05-04",
                          "Semana 20" : "2014-05-18",
                          "Semana 21" : "2014-05-25",
                          "Semana 22" : "2014-06-01",
                          "Semana 27" : "2014-07-06",
                          "Semana 31" : "2014-08-03",
                          "Semana 42" : "2014-10-19",
                          "Semana 51" : "2014-12-21",
                          "Semana 52" : "2014-12-28"}, inplace = True)"""
casos23["Município"] = casos23["Município"].str.replace("\d+ ", "", regex = True)
casos23.drop(columns = "Total", inplace = True)
casos23.drop(casos23.index[-2:], axis = 0, inplace = True)
casos23.set_index("Município", inplace = True)
casos23 = casos23.T
casos23.reset_index(inplace=True)
casos23 = casos23.rename(columns = {"index" : "Semana"})
casos23.rename(columns = lista_municipio, inplace = True)
colunas = casos23.columns.drop("Semana")
casos23[colunas] = casos23[colunas].replace("-", np.nan)
casos23[colunas] = casos23[colunas].astype(float)
casos23.fillna(0, inplace = True)
casos23[colunas] = casos23[colunas].astype(int)
print("\n2023\n", casos23)
print(casos23.info())
print(casos23.columns.drop("Semana"))

sys.exit()
"""
casos.drop(columns = "Data", inplace = True)
casos.rename(columns = {"data" : "Semana"}, inplace = True)
casos = pd.melt(casos, id_vars = "Semana", var_name = "Município",
                value_name = "Casos", ignore_index = True)
#value_vars = se não especificado, usa todas as colunas.
casos = casos.replace("2014-01-06", "2014-01-05")
casos["Município"] = casos["Município"].str.upper()
casos["Casos"] = casos["Casos"].astype(int)


casos = casos.astype(int)
casos_se = casos_se.astype(int)

pospandemia = pd.concat([focos202202, focos202201, focos2021, focos2020], ignore_index = True)
prepandemia = pd.concat([focos2019, focos2018, focos2017, focos2016], ignore_index = True)
inicial = pd.concat([focos2015, focos2014, focos2013, focos2012], ignore_index = True)
prepandemia = pd.concat([prepandemia, inicial], ignore_index= True)
focostotal = pd.concat([pospandemia, prepandemia], ignore_index = True)
"""

### Salvando Arquivo
#focostotal.to_csv(f"{caminho_dados}focos_dive_total.csv", index = False)

### Printando Informações
print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(casos.info())
print("~"*80)
print(casos.dtypes)
print("~"*80)
print(casos)
print("="*80)

print("\n \n CASOS DE DENGUE EM SANTA CATARINA - SÉRIE HISTÓRICA (testando _se) \n")
print(casos_se.info())
print("~"*80)
print(casos_se.dtypes)
print("~"*80)
print(casos_se)
print("="*80)
"""
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO SEGUNDO (02) SEMESTRE DE 2022 \n")
print(focos202202.info())
print("~"*80)
print(focos202202.dtypes)
print("~"*80)
print(focos202202)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO PRIMEIRO (01) SEMESTRE DE 2022 \n")
print(focos202201.info())
print("~"*80)
print(focos202201.dtypes)
print("~"*80)
print(focos202201)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2021 \n")
print(focos2021.info())
print("~"*80)
print(focos2021.dtypes)
print("~"*80)
print(focos2021)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2020 \n")
print(focos2020.info())
print("~"*80)
print(focos2020.dtypes)
print("~"*80)
print(focos2020)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2019 \n")
print(focos2019.info())
print("~"*80)
print(focos2019.dtypes)
print("~"*80)
print(focos2019)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2018 \n")
print(focos2018.info())
print("~"*80)
print(focos2018.dtypes)
print("~"*80)
print(focos2018)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2017 \n")
print(focos2017.info())
print("~"*80)
print(focos2017.dtypes)
print("~"*80)
print(focos2017)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2016 \n")
print(focos2016.info())
print("~"*80)
print(focos2016.dtypes)
print("~"*80)
print(focos2016)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2015 \n")
print(focos2015.info())
print("~"*80)
print(focos2015.dtypes)
print("~"*80)
print(focos2015)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2014 \n")
print(focos2014.info())
print("~"*80)
print(focos2014.dtypes)
print("~"*80)
print(focos2014)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2013 \n")
print(focos2013.info())
print("~"*80)
print(focos2013.dtypes)
print("~"*80)
print(focos2013)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA NO ANO DE 2012 \n")
print(focos2012.info())
print("~"*80)
print(focos2012.dtypes)
print("~"*80)
print(focos2012)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA DURANTE E APÓS PANDEMIA \n")
print(pospandemia.info())
print("~"*80)
print(pospandemia.dtypes)
print("~"*80)
print(pospandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA ANTES DA PANDEMIA \n")
print(prepandemia.info())
print("~"*80)
print(prepandemia.dtypes)
print("~"*80)
print(prepandemia)
print("="*80)

print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA \n")
print(focostotal.info())
print("~"*80)
print(focostotal.dtypes)
print("~"*80)
print(focostotal)
print("="*80)
"""
