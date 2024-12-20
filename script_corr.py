### Bibliotecas Correlatas
import matplotlib.pyplot as plt               
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels as sm
#import sys

### Encaminhamento aos Diretórios
_local = "CASA" # OPÇÕES>>> "GH" "CASA" "IFSC"
if _local == "GH": # _ = Variável Privada
    caminho_dados = "https://raw.githubusercontent.com/matheusf30/dados_dengue/main/"
elif _local == "CASA":
    caminho_dados = "C:\\Users\\Desktop\\Documents\\GitHub\\dados_dengue\\"
elif _local == "IFSC":
    caminho_dados = "/home/sifapsc/scripts/matheus/dados_dengue/"
else:
    print("CAMINHO NÃO RECONHECIDO! VERIFICAR LOCAL!")
print(f"\nOS DADOS UTILIZADOS ESTÃO ALOCADOS NOS SEGUINTES CAMINHOS:\n\n{caminho_dados}\n\n")

### Renomeação variáveis pelos arquivos
casos = "serie_casos_sc.csv"
focos = "serie_focosdia_sc.csv"
merge = "merge.csv"
tmax = "samet_tmax.csv"
tmed = "samet_tmed.csv"
tmin = "samet_tmin.csv"
"""
dicionario = "dicionario_municipios.csv"
lista = "lista_municipios.csv"
variaveis = (casos, focos, tmax, tmed, tmin, merge)
"""
### Abrindo Arquivos
casos = pd.read_csv(f"{caminho_dados}{casos}")
focos = pd.read_csv(f"{caminho_dados}{focos}")
merge = pd.read_csv(f"{caminho_dados}{merge}")
tmax = pd.read_csv(f"{caminho_dados}{tmax}")
tmed = pd.read_csv(f"{caminho_dados}{tmed}")
tmin = pd.read_csv(f"{caminho_dados}{tmin}")
"""
dicionario = pd.read_csv(f"{caminho_dados}{dicionario}")
lista = pd.read_csv(f"{caminho_dados}{lista}")
"""

### Dicionários
lista = {"date": "Data",
 '4200051': 'Abdon Batista',
 '4200101': 'Abelardo Luz',
 '4200200': 'Agrolândia',
 '4200309': 'Agronômica',
 '4200408': 'Água Doce',
 '4200507': 'Águas de Chapecó',
 '4200556': 'Águas Frias',
 '4200606': 'Águas Mornas',
 '4200705': 'Alfredo Wagner',
 '4200754': 'Alto Bela Vista',
 '4200804': 'Anchieta',
 '4200903': 'Angelina',
 '4201000': 'Anita Garibaldi',
 '4201109': 'Anitápolis',
 '4201208': 'Antônio Carlos',
 '4201257': 'Apiúna',
 '4201273': 'Arabutã',
 '4201307': 'Araquari',
 '4201406': 'Araranguá',
 '4201505': 'Armazém',
 '4201604': 'Arroio Trinta',
 '4201653': 'Arvoredo',
 '4201703': 'Ascurra',
 '4201802': 'Atalanta',
 '4201901': 'Aurora',
 '4201950': 'Balneário Arroio do Silva',
 '4202008': 'Balneário Camboriú',
 '4202057': 'Balneário Barra do Sul',
 '4202073': 'Balneário Gaivota',
 '4202081': 'Bandeirante',
 '4202099': 'Barra Bonita',
 '4202107': 'Barra Velha',
 '4202131': 'Bela Vista do Toldo',
 '4202156': 'Belmonte',
 '4202206': 'Benedito Novo',
 '4202305': 'Biguaçu',
 '4202404': 'Blumenau',
 '4202438': 'Bocaina do Sul',
 '4202453': 'Bombinhas',
 '4202503': 'Bom Jardim da Serra',
 '4202537': 'Bom Jesus',
 '4202578': 'Bom Jesus do Oeste',
 '4202602': 'Bom Retiro',
 '4202701': 'Botuverá',
 '4202800': 'Braço do Norte',
 '4202859': 'Braço do Trombudo',
 '4202875': 'Brunópolis',
 '4202909': 'Brusque',
 '4203006': 'Caçador',
 '4203105': 'Caibi',
 '4203154': 'Calmon',
 '4203204': 'Camboriú',
 '4203253': 'Capão Alto',
 '4203303': 'Campo Alegre',
 '4203402': 'Campo Belo do Sul',
 '4203501': 'Campo Erê',
 '4203600': 'Campos Novos',
 '4203709': 'Canelinha',
 '4203808': 'Canoinhas',
 '4203907': 'Capinzal',
 '4203956': 'Capivari de Baixo',
 '4204004': 'Catanduvas',
 '4204103': 'Caxambu do Sul',
 '4204152': 'Celso Ramos',
 '4204178': 'Cerro Negro',
 '4204194': 'Chapadão do Lageado',
 '4204202': 'Chapecó',
 '4204251': 'Cocal do Sul',
 '4204301': 'Concórdia',
 '4204350': 'Cordilheira Alta',
 '4204400': 'Coronel Freitas',
 '4204459': 'Coronel Martins',
 '4204509': 'Corupá',
 '4204558': 'Correia Pinto',
 '4204608': 'Criciúma',
 '4204707': 'Cunha Porã',
 '4204756': 'Cunhataí',
 '4204806': 'Curitibanos',
 '4204905': 'Descanso',
 '4205001': 'Dionísio Cerqueira',
 '4205100': 'Dona Emma',
 '4205159': 'Doutor Pedrinho',
 '4205175': 'Entre Rios',
 '4205191': 'Ermo',
 '4205209': 'Erval Velho',
 '4205308': 'Faxinal dos Guedes',
 '4205357': 'Flor do Sertão',
 '4205407': 'Florianópolis',
 '4205431': 'Formosa do Sul',
 '4205456': 'Forquilhinha',
 '4205506': 'Fraiburgo',
 '4205555': 'Frei Rogério',
 '4205605': 'Galvão',
 '4205704': 'Garopaba',
 '4205803': 'Garuva',
 '4205902': 'Gaspar',
 '4206009': 'Governador Celso Ramos',
 '4206108': 'Grão-Pará',
 '4206207': 'Gravatal',
 '4206306': 'Guabiruba',
 '4206405': 'Guaraciaba',
 '4206504': 'Guaramirim',
 '4206603': 'Guarujá do Sul',
 '4206652': 'Guatambú',
 '4206702': "Herval d'Oeste",
 '4206751': 'Ibiam',
 '4206801': 'Ibicaré',
 '4206900': 'Ibirama',
 '4207007': 'Içara',
 '4207106': 'Ilhota',
 '4207205': 'Imaruí',
 '4207304': 'Imbituba',
 '4207403': 'Imbuia',
 '4207502': 'Indaial',
 '4207577': 'Iomerê',
 '4207601': 'Ipira',
 '4207650': 'Iporã do Oeste',
 '4207684': 'Ipuaçu',
 '4207700': 'Ipumirim',
 '4207759': 'Iraceminha',
 '4207809': 'Irani',
 '4207858': 'Irati',
 '4207908': 'Irineópolis',
 '4208005': 'Itá',
 '4208104': 'Itaiópolis',
 '4208203': 'Itajaí',
 '4208302': 'Itapema',
 '4208401': 'Itapiranga',
 '4208450': 'Itapoá',
 '4208500': 'Ituporanga',
 '4208609': 'Jaborá',
 '4208708': 'Jacinto Machado',
 '4208807': 'Jaguaruna',
 '4208906': 'Jaraguá do Sul',
 '4208955': 'Jardinópolis',
 '4209003': 'Joaçaba',
 '4209102': 'Joinville',
 '4209151': 'José Boiteux',
 '4209177': 'Jupiá',
 '4209201': 'Lacerdópolis',
 '4209300': 'Lages',
 '4209409': 'Laguna',
 '4209458': 'Lajeado Grande',
 '4209508': 'Laurentino',
 '4209607': 'Lauro Müller',
 '4209706': 'Lebon Régis',
 '4209805': 'Leoberto Leal',
 '4209854': 'Lindóia do Sul',
 '4209904': 'Lontras',
 '4210001': 'Luiz Alves',
 '4210035': 'Luzerna',
 '4210050': 'Macieira',
 '4210100': 'Mafra',
 '4210209': 'Major Gercino',
 '4210308': 'Major Vieira',
 '4210407': 'Maracajá',
 '4210506': 'Maravilha',
 '4210555': 'Marema',
 '4210605': 'Massaranduba',
 '4210704': 'Matos Costa',
 '4210803': 'Meleiro',
 '4210852': 'Mirim Doce',
 '4210902': 'Modelo',
 '4211009': 'Mondaí',
 '4211058': 'Monte Carlo',
 '4211108': 'Monte Castelo',
 '4211207': 'Morro da Fumaça',
 '4211256': 'Morro Grande',
 '4211306': 'Navegantes',
 '4211405': 'Nova Erechim',
 '4211454': 'Nova Itaberaba',
 '4211504': 'Nova Trento',
 '4211603': 'Nova Veneza',
 '4211652': 'Novo Horizonte',
 '4211702': 'Orleans',
 '4211751': 'Otacílio Costa',
 '4211801': 'Ouro',
 '4211850': 'Ouro Verde',
 '4211876': 'Paial',
 '4211892': 'Painel',
 '4211900': 'Palhoça',
 '4212007': 'Palma Sola',
 '4212056': 'Palmeira',
 '4212106': 'Palmitos',
 '4212205': 'Papanduva',
 '4212239': 'Paraíso',
 '4212254': 'Passo de Torres',
 '4212270': 'Passos Maia',
 '4212304': 'Paulo Lopes',
 '4212403': 'Pedras Grandes',
 '4212502': 'Penha',
 '4212601': 'Peritiba',
 '4212650': 'Pescaria Brava',
 '4212700': 'Petrolândia',
 '4212809': 'Balneário Piçarras',
 '4212908': 'Pinhalzinho',
 '4213005': 'Pinheiro Preto',
 '4213104': 'Piratuba',
 '4213153': 'Planalto Alegre',
 '4213203': 'Pomerode',
 '4213302': 'Ponte Alta',
 '4213351': 'Ponte Alta do Norte',
 '4213401': 'Ponte Serrada',
 '4213500': 'Porto Belo',
 '4213609': 'Porto União',
 '4213708': 'Pouso Redondo',
 '4213807': 'Praia Grande',
 '4213906': 'Presidente Castello Branco',
 '4214003': 'Presidente Getúlio',
 '4214102': 'Presidente Nereu',
 '4214151': 'Princesa',
 '4214201': 'Quilombo',
 '4214300': 'Rancho Queimado',
 '4214409': 'Rio das Antas',
 '4214508': 'Rio do Campo',
 '4214607': 'Rio do Oeste',
 '4214706': 'Rio dos Cedros',
 '4214805': 'Rio do Sul',
 '4214904': 'Rio Fortuna',
 '4215000': 'Rio Negrinho',
 '4215059': 'Rio Rufino',
 '4215075': 'Riqueza',
 '4215109': 'Rodeio',
 '4215208': 'Romelândia',
 '4215307': 'Salete',
 '4215356': 'Saltinho',
 '4215406': 'Salto Veloso',
 '4215455': 'Sangão',
 '4215505': 'Santa Cecília',
 '4215554': 'Santa Helena',
 '4215604': 'Santa Rosa de Lima',
 '4215653': 'Santa Rosa do Sul',
 '4215679': 'Santa Terezinha',
 '4215687': 'Santa Terezinha do Progresso',
 '4215695': 'Santiago do Sul',
 '4215703': 'Santo Amaro da Imperatriz',
 '4215752': 'São Bernardino',
 '4215802': 'São Bento do Sul',
 '4215901': 'São Bonifácio',
 '4216008': 'São Carlos',
 '4216057': 'São Cristóvão do Sul',
 '4216107': 'São Domingos',
 '4216206': 'São Francisco do Sul',
 '4216255': 'São João do Oeste',
 '4216305': 'São João Batista',
 '4216354': 'São João do Itaperiú',
 '4216404': 'São João do Sul',
 '4216503': 'São Joaquim',
 '4216602': 'São José',
 '4216701': 'São José do Cedro',
 '4216800': 'São José do Cerrito',
 '4216909': 'São Lourenço do Oeste',
 '4217006': 'São Ludgero',
 '4217105': 'São Martinho',
 '4217154': 'São Miguel da Boa Vista',
 '4217204': 'São Miguel do Oeste',
 '4217253': 'São Pedro de Alcântara',
 '4217303': 'Saudades',
 '4217402': 'Schroeder',
 '4217501': 'Seara',
 '4217550': 'Serra Alta',
 '4217600': 'Siderópolis',
 '4217709': 'Sombrio',
 '4217758': 'Sul Brasil',
 '4217808': 'Taió',
 '4217907': 'Tangará',
 '4217956': 'Tigrinhos',
 '4218004': 'Tijucas',
 '4218103': 'Timbé do Sul',
 '4218202': 'Timbó',
 '4218251': 'Timbó Grande',
 '4218301': 'Três Barras',
 '4218350': 'Treviso',
 '4218400': 'Treze de Maio',
 '4218509': 'Treze Tílias',
 '4218608': 'Trombudo Central',
 '4218707': 'Tubarão',
 '4218756': 'Tunápolis',
 '4218806': 'Turvo',
 '4218855': 'União do Oeste',
 '4218905': 'Urubici',
 '4218954': 'Urupema',
 '4219002': 'Urussanga',
 '4219101': 'Vargeão',
 '4219150': 'Vargem',
 '4219176': 'Vargem Bonita',
 '4219200': 'Vidal Ramos',
 '4219309': 'Videira',
 '4219358': 'Vitor Meireles',
 '4219408': 'Witmarsum',
 '4219507': 'Xanxerê',
 '4219606': 'Xavantina',
 '4219705': 'Xaxim',
 '4219853': 'Zortéa',
 '4220000': 'Balneário Rincão'}
dicionario = {'data_caso': 'Data',
 'data_foco': 'Data',
 'Abdon_Batista': 'Abdon Batista',
 'Abelardo_Luz': 'Abelardo Luz',
 'Agrolandia': 'Agrolândia',
 'Agronomica': 'Agronômica',
 'Agua_Doce': 'Água Doce',
 'Aguas_de_Chapeco': 'Águas de Chapecó',
 'Aguas_Frias': 'Águas Frias',
 'Aguas_Mornas': 'Águas Mornas',
 'Alfredo_Wagner': 'Alfredo Wagner',
 'Alto_Bela_Vista': 'Alto Bela Vista',
 'Anchieta': 'Anchieta',
 'Angelina': 'Angelina',
 'Anita_Garibaldi': 'Anita Garibaldi',
 'Anitapolis': 'Anitápolis',
 'Antonio_Carlos': 'Antônio Carlos',
 'Apiuna': 'Apiúna',
 'Arabuta': 'Arabutã',
 'Araquari': 'Araquari',
 'Ararangua': 'Araranguá',
 'Armazem': 'Armazém',
 'Arroio_Trinta': 'Arroio Trinta',
 'Arvoredo': 'Arvoredo',
 'Ascurra': 'Ascurra',
 'Atalanta': 'Atalanta',
 'Aurora': 'Aurora',
 'Balneario_Arroio_do_Silva': 'Balneário Arroio do Silva',
 'Balneario_Camboriu': 'Balneário Camboriú',
 'Balneario_Barra_do_Sul': 'Balneário Barra do Sul',
 'Balneario_Gaivota': 'Balneário Gaivota',
 'Balneario_Picarras': 'Balneário Piçarras',
 'Balneario_Rincao': 'Balneário Rincão',
 'Bandeirante': 'Bandeirante',
 'Barra_Bonita': 'Barra Bonita',
 'Barra_Velha': 'Barra Velha',
 'Bela_Vista_do_Toldo': 'Bela Vista do Toldo',
 'Belmonte': 'Belmonte',
 'Benedito_Novo': 'Benedito Novo',
 'Biguacu': 'Biguaçu',
 'Blumenau': 'Blumenau',
 'Bocaina_do_Sul': 'Bocaina do Sul',
 'Bombinhas': 'Bombinhas',
 'Bom_Jardim_da_Serra': 'Bom Jardim da Serra',
 'Bom_Jesus': 'Bom Jesus',
 'Bom_Jesus_do_Oeste': 'Bom Jesus do Oeste',
 'Bom_Retiro': 'Bom Retiro',
 'Botuvera': 'Botuverá',
 'Braco_do_Norte': 'Braço do Norte',
 'Braco_do_Trombudo': 'Braço do Trombudo',
 'Brunopolis': 'Brunópolis',
 'Brusque': 'Brusque',
 'Cacador': 'Caçador',
 'Caibi': 'Caibi',
 'Calmon': 'Calmon',
 'Camboriu': 'Camboriú',
 'Capao_Alto': 'Capão Alto',
 'Campo_Alegre': 'Campo Alegre',
 'Campo_Belo_do_Sul': 'Campo Belo do Sul',
 'Campo_Ere': 'Campo Erê',
 'Campos_Novos': 'Campos Novos',
 'Canelinha': 'Canelinha',
 'Canoinhas': 'Canoinhas',
 'Capinzal': 'Capinzal',
 'Capivari_de_Baixo': 'Capivari de Baixo',
 'Catanduvas': 'Catanduvas',
 'Caxambu_do_Sul': 'Caxambu do Sul',
 'Celso_Ramos': 'Celso Ramos',
 'Cerro_Negro': 'Cerro Negro',
 'Chapadao_do_Lageado': 'Chapadão do Lageado',
 'Chapeco': 'Chapecó',
 'Cocal_do_Sul': 'Cocal do Sul',
 'Concordia': 'Concórdia',
 'Cordilheira_Alta': 'Cordilheira Alta',
 'Coronel_Freitas': 'Coronel Freitas',
 'Coronel_Martins': 'Coronel Martins',
 'Corupa': 'Corupá',
 'Correia_Pinto': 'Correia Pinto',
 'Criciuma': 'Criciúma',
 'Cunha_Pora': 'Cunha Porã',
 'Cunhatai': 'Cunhataí',
 'Curitibanos': 'Curitibanos',
 'Descanso': 'Descanso',
 'Dionisio_Cerqueira': 'Dionísio Cerqueira',
 'Dona_Emma': 'Dona Emma',
 'Doutor_Pedrinho': 'Doutor Pedrinho',
 'Entre_Rios': 'Entre Rios',
 'Ermo': 'Ermo',
 'Erval_Velho': 'Erval Velho',
 'Faxinal_dos_Guedes': 'Faxinal dos Guedes',
 'Flor_do_Sertao': 'Flor do Sertão',
 'Florianopolis': 'Florianópolis',
 'Formosa_do_Sul': 'Formosa do Sul',
 'Forquilhinha': 'Forquilhinha',
 'Fraiburgo': 'Fraiburgo',
 'Frei_Rogerio': 'Frei Rogério',
 'Galvao': 'Galvão',
 'Garopaba': 'Garopaba',
 'Garuva': 'Garuva',
 'Gaspar': 'Gaspar',
 'Governador_Celso_Ramos': 'Governador Celso Ramos',
 'Grao_Para': 'Grão-Pará',
 'Gravatal': 'Gravatal',
 'Guabiruba': 'Guabiruba',
 'Guaraciaba': 'Guaraciaba',
 'Guaramirim': 'Guaramirim',
 'Guaruja_do_Sul': 'Guarujá do Sul',
 'Guatambu': 'Guatambú',
 "Herval_d'Oeste": "Herval d'Oeste",
 'Ibiam': 'Ibiam',
 'Ibicare': 'Ibicaré',
 'Ibirama': 'Ibirama',
 'Icara': 'Içara',
 'Ilhota': 'Ilhota',
 'Imarui': 'Imaruí',
 'Imbituba': 'Imbituba',
 'Imbuia': 'Imbuia',
 'Indaial': 'Indaial',
 'Iomere': 'Iomerê',
 'Ipira': 'Ipira',
 'Ipora_do_Oeste': 'Iporã do Oeste',
 'Ipuacu': 'Ipuaçu',
 'Ipumirim': 'Ipumirim',
 'Iraceminha': 'Iraceminha',
 'Irani': 'Irani',
 'Irati': 'Irati',
 'Irineopolis': 'Irineópolis',
 'Ita': 'Itá',
 'Itaiopolis': 'Itaiópolis',
 'Itajai': 'Itajaí',
 'Itapema': 'Itapema',
 'Itapiranga': 'Itapiranga',
 'Itapoa': 'Itapoá',
 'Ituporanga': 'Ituporanga',
 'Jabora': 'Jaborá',
 'Jacinto_Machado': 'Jacinto Machado',
 'Jaguaruna': 'Jaguaruna',
 'Jaragua_do_Sul': 'Jaraguá do Sul',
 'Jardinopolis': 'Jardinópolis',
 'Joacaba': 'Joaçaba',
 'Joinville': 'Joinville',
 'Jose_Boiteux': 'José Boiteux',
 'Jupia': 'Jupiá',
 'Lacerdopolis': 'Lacerdópolis',
 'Lages': 'Lages',
 'Laguna': 'Laguna',
 'Lajeado_Grande': 'Lajeado Grande',
 'Laurentino': 'Laurentino',
 'Lauro_Muller': 'Lauro Müller',
 'Lebon_Regis': 'Lebon Régis',
 'Leoberto_Leal': 'Leoberto Leal',
 'Lindoia_do_Sul': 'Lindóia do Sul',
 'Lontras': 'Lontras',
 'Luiz_Alves': 'Luiz Alves',
 'Luzerna': 'Luzerna',
 'Macieira': 'Macieira',
 'Mafra': 'Mafra',
 'Major_Gercino': 'Major Gercino',
 'Major_Vieira': 'Major Vieira',
 'Maracaja': 'Maracajá',
 'Maravilha': 'Maravilha',
 'Marema': 'Marema',
 'Massaranduba': 'Massaranduba',
 'Matos_Costa': 'Matos Costa',
 'Meleiro': 'Meleiro',
 'Mirim_Doce': 'Mirim Doce',
 'Modelo': 'Modelo',
 'Mondai': 'Mondaí',
 'Monte_Carlo': 'Monte Carlo',
 'Monte_Castelo': 'Monte Castelo',
 'Morro_da_Fumaca': 'Morro da Fumaça',
 'Morro_Grande': 'Morro Grande',
 'Navegantes': 'Navegantes',
 'Nova_Erechim': 'Nova Erechim',
 'Nova_Itaberaba': 'Nova Itaberaba',
 'Nova_Trento': 'Nova Trento',
 'Nova_Veneza': 'Nova Veneza',
 'Novo_Horizonte': 'Novo Horizonte',
 'Orleans': 'Orleans',
 'Otacilio_Costa': 'Otacílio Costa',
 'Ouro': 'Ouro',
 'Ouro_Verde': 'Ouro Verde',
 'Paial': 'Paial',
 'Painel': 'Painel',
 'Palhoca': 'Palhoça',
 'Palma_Sola': 'Palma Sola',
 'Palmeira': 'Palmeira',
 'Palmitos': 'Palmitos',
 'Papanduva': 'Papanduva',
 'Paraiso': 'Paraíso',
 'Passo_de_Torres': 'Passo de Torres',
 'Passos_Maia': 'Passos Maia',
 'Paulo_Lopes': 'Paulo Lopes',
 'Pedras_Grandes': 'Pedras Grandes',
 'Penha': 'Penha',
 'Peritiba': 'Peritiba',
 'Pescaria_Brava': 'Pescaria Brava',
 'Petrolandia': 'Petrolândia',
 'Pinhalzinho': 'Pinhalzinho',
 'Pinheiro_Preto': 'Pinheiro Preto',
 'Piratuba': 'Piratuba',
 'Planalto_Alegre': 'Planalto Alegre',
 'Pomerode': 'Pomerode',
 'Ponte_Alta': 'Ponte Alta',
 'Ponte_Alta_do_Norte': 'Ponte Alta do Norte',
 'Ponte_Serrada': 'Ponte Serrada',
 'Porto_Belo': 'Porto Belo',
 'Porto_Uniao': 'Porto União',
 'Pouso_Redondo': 'Pouso Redondo',
 'Praia_Grande': 'Praia Grande',
 'Presidente_Castello_Branco': 'Presidente Castello Branco',
 'Presidente_Getulio': 'Presidente Getúlio',
 'Presidente_Nereu': 'Presidente Nereu',
 'Princesa': 'Princesa',
 'Quilombo': 'Quilombo',
 'Rancho_Queimado': 'Rancho Queimado',
 'Rio_das_Antas': 'Rio das Antas',
 'Rio_do_Campo': 'Rio do Campo',
 'Rio_do_Oeste': 'Rio do Oeste',
 'Rio_dos_Cedros': 'Rio dos Cedros',
 'Rio_do_Sul': 'Rio do Sul',
 'Rio_Fortuna': 'Rio Fortuna',
 'Rio_Negrinho': 'Rio Negrinho',
 'Rio_Rufino': 'Rio Rufino',
 'Riqueza': 'Riqueza',
 'Rodeio': 'Rodeio',
 'Romelandia': 'Romelândia',
 'Salete': 'Salete',
 'Saltinho': 'Saltinho',
 'Salto_Veloso': 'Salto Veloso',
 'Sangao': 'Sangão',
 'Santa_Cecilia': 'Santa Cecília',
 'Santa_Helena': 'Santa Helena',
 'Santa_Rosa_de_Lima': 'Santa Rosa de Lima',
 'Santa_Rosa_do_Sul': 'Santa Rosa do Sul',
 'Santa_Terezinha': 'Santa Terezinha',
 'Santa_Terezinha_do_Progresso': 'Santa Terezinha do Progresso',
 'Santiago_do_Sul': 'Santiago do Sul',
 'Santo_Amaro_da_Imperatriz': 'Santo Amaro da Imperatriz',
 'Sao_Bernardino': 'São Bernardino',
 'Sao_Bento_do_Sul': 'São Bento do Sul',
 'Sao_Bonifacio': 'São Bonifácio',
 'Sao_Carlos': 'São Carlos',
 'Sao_Cristovao_do_Sul': 'São Cristóvão do Sul',
 'Sao_Domingos': 'São Domingos',
 'Sao_Francisco_do_Sul': 'São Francisco do Sul',
 'Sao_Joao_do_Oeste': 'São João do Oeste',
 'Sao_Joao_Batista': 'São João Batista',
 'Sao_Joao_do_Itaperiu': 'São João do Itaperiú',
 'Sao_Joao_do_Sul': 'São João do Sul',
 'Sao_Joaquim': 'São Joaquim',
 'Sao_Jose': 'São José',
 'Sao_Jose_do_Cedro': 'São José do Cedro',
 'Sao_Jose_do_Cerrito': 'São José do Cerrito',
 'Sao_Lourenco_do_Oeste': 'São Lourenço do Oeste',
 'Sao_Ludgero': 'São Ludgero',
 'Sao_Martinho': 'São Martinho',
 'Sao_Miguel_da_Boa_Vista': 'São Miguel da Boa Vista',
 'Sao_Miguel_do_Oeste': 'São Miguel do Oeste',
 'Sao_Pedro_de_Alcantara': 'São Pedro de Alcântara',
 'Saudades': 'Saudades',
 'Schroeder': 'Schroeder',
 'Seara': 'Seara',
 'Serra_Alta': 'Serra Alta',
 'Sideropolis': 'Siderópolis',
 'Sombrio': 'Sombrio',
 'Sul_Brasil': 'Sul Brasil',
 'Taio': 'Taió',
 'Tangara': 'Tangará',
 'Tigrinhos': 'Tigrinhos',
 'Tijucas': 'Tijucas',
 'Timbe_do_Sul': 'Timbé do Sul',
 'Timbo': 'Timbó',
 'Timbo_Grande': 'Timbó Grande',
 'Tres_Barras': 'Três Barras',
 'Treviso': 'Treviso',
 'Treze_de_Maio': 'Treze de Maio',
 'Treze_Tilias': 'Treze Tílias',
 'Trombudo_Central': 'Trombudo Central',
 'Tubarao': 'Tubarão',
 'Tunapolis': 'Tunápolis',
 'Turvo': 'Turvo',
 'Uniao_do_Oeste': 'União do Oeste',
 'Urubici': 'Urubici',
 'Urupema': 'Urupema',
 'Urussanga': 'Urussanga',
 'Vargeao': 'Vargeão',
 'Vargem': 'Vargem',
 'Vargem_Bonita': 'Vargem Bonita',
 'Vidal_Ramos': 'Vidal Ramos',
 'Videira': 'Videira',
 'Vitor_Meireles': 'Vitor Meireles',
 'Witmarsum': 'Witmarsum',
 'Xanxere': 'Xanxerê',
 'Xavantina': 'Xavantina',
 'Xaxim': 'Xaxim',
 'Zortea': 'Zortéa'}

### Transformando em datetime64[ns] e Renomeando colunas
focos["data"] = focos["data_foco"]
focos["data_foco"] = pd.to_datetime(focos["data_foco"])
focos = focos.sort_values(by = ["data_foco"])
focos = focos.rename(columns = dicionario)

casos["data"] = casos["data_caso"]
casos["data_caso"] = pd.to_datetime(casos["data_caso"])
casos = casos.sort_values(by = ["data_caso"])
casos = casos.rename(columns = dicionario)

merge["data"] = merge["date"]
merge["date"] = pd.to_datetime(merge["date"])
merge = merge.sort_values(by = ["date"])
merge = merge.drop(columns = ["lon", "lat"])
merge = merge.rename(columns = lista)

tmin["data"] = tmin["date"]
tmin["date"] = pd.to_datetime(tmin["date"])
tmin = tmin.sort_values(by = ["date"])
tmin = tmin.drop(columns = ["lon", "lat"])
tmin = tmin.rename(columns = lista)

tmed["data"] = tmed["date"]
tmed["date"] = pd.to_datetime(tmed["date"])
tmed = tmed.sort_values(by = ["date"])
tmed = tmed.drop(columns = ["lon", "lat"])
tmed = tmed.rename(columns = lista)

tmax["data"] = tmax["date"]
tmax["date"] = pd.to_datetime(tmax["date"])
tmax = tmax.sort_values(by = ["date"])
tmax = tmax.drop(columns = ["lon", "lat"])
tmax = tmax.rename(columns = lista)

### Printando dados e informações
"""
print(focos.info())
print(focos.dtypes)
print(focos)

print(casos.info())
print(casos.dtypes)
print(casos)
print(casos)

print(merge.info())
print(merge.dtypes)
print(merge)

print(tmin.info())
print(tmin.dtypes)
print(tmin)

print(tmed.info())
print(tmed.dtypes)
print(tmed)

print(tmax.info())
print(tmax.dtypes)
print(tmax)
"""

### Manipulando Correlações e Deletando Variáveis do Sistema

corr_floripa = focos[["Palhoça", "Florianópolis"]].iloc[:4018]
corr_floripa = corr_floripa.rename(columns={"Florianópolis" : "Focos"})
prec = merge.iloc[4230:]
prec_floripa = prec[["Data", "Florianópolis"]]
corr_floripa = corr_floripa.merge(prec_floripa, how = "cross")
corr_floripa = corr_floripa.rename(columns={"Florianópolis" : "Precipitação"})
corr_floripa = corr_floripa.drop(["Palhoça"], axis = "columns")
corr_floripa.set_index("Data", inplace = True)
del focos
del merge

tmin2 = tmin.iloc[4383:]
tmin_floripa = tmin2[["Data", "Florianópolis"]]
corr_floripa = corr_floripa.merge(tmin_floripa, how = "cross")
corr_floripa = corr_floripa.rename(columns={"Florianópolis" : "T.Mínima"})
corr_floripa["Log_Focos"] = np.log(corr_floripa["Focos"] + 1)
corr_floripa["Log_Precipitação"] = np.log(corr_floripa["Precipitação"] + 1)
correlacao = corr_floripa.corr().round(4)
sns.heatmap(correlacao, annot = True, cmap = "tab20c", linewidth = 0.5)
print(corr_floripa)
"""
### Zerando Variáveis
#sys.stdout.flush()
#gc.collect()
#gc.get_stats()
del caminho_dados
del caminho_imagens
del casos
del focos
del merge
del tmax
del tmed
del tmin
del dicionario
del lista
del tmin2


#





#
#correlacao = geo_dados.corr(numeric_only = True)
#sns.heatmap(correlacao, annot = True, cmap = "RdYlBu", linewidth = 0.5)
"""
"""
df = pd.DataFrame(np.random.random((6, 4)), columns=list('ABCD'))
fig, ax = plt.subplots()
sns.heatmap(df.corr(method='pearson'), annot=True, fmt='.4f', 
            cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax)
ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
plt.savefig('result.png', bbox_inches='tight', pad_inches=0.0)


df = pd.DataFrame(np.random.random((6, 4)), columns=list('ABCD'))
corr = df.corr(method='pearson')

fig, ax = plt.subplots()
data = corr.values
heatmap = ax.pcolor(data, cmap=plt.get_cmap('coolwarm'), 
                    vmin=np.nanmin(data), vmax=np.nanmax(data))
ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
ax.invert_yaxis()
row_labels = corr.index
column_labels = corr.columns
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)

def _annotate_heatmap(ax, mesh):
"""
    #**Taken from seaborn/matrix.py**
    #Add textual labels with the value in each cell.
"""
    mesh.update_scalarmappable()
    xpos, ypos = np.meshgrid(ax.get_xticks(), ax.get_yticks())
    for x, y, val, color in zip(xpos.flat, ypos.flat,
                                mesh.get_array(), mesh.get_facecolors()):
        if val is not np.ma.masked:
            _, l, _ = colorsys.rgb_to_hls(*color[:3])
            text_color = ".15" if l > .5 else "w"
            val = ("{:.3f}").format(val)
            text_kwargs = dict(color=text_color, ha="center", va="center")
            # text_kwargs.update(self.annot_kws)
            ax.text(x, y, val, **text_kwargs)

_annotate_heatmap(ax, heatmap)
plt.savefig('result.png', bbox_inches='tight', pad_inches=0.0)
"""

