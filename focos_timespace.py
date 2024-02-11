### Bibliotecas Correlatas
import pandas as pd
import geopandas as gpd
#import matplotlib.pyplot as plt
#import folium
#from folium.plugins import HeatMapWithTime

### Encaminhamento ao Diretório "DADOS" e "RESULTADOS"
caminho_dados = "/home/sifapsc/scripts/matheus/dados/"
caminho_imagens = "/home/sifapsc/scripts/matheus/resultado_imagens/"
caminho_correlacao = "/home/sifapsc/scripts/matheus/resultado_correlacao/"

### Renomeação variáveis pelos arquivos
#focos_timespace = "focos_timespace.csv" # Data de Coleta
focos_timespace = "focos_se_timespace.csv" # Semanas Epidemiológicas
#focos_timespace = "SC_Municipios_2022.shp" # Shapefile (?)
municipios = "SC_Municipios_2022.shp"

### Abrindo Arquivo
focos_timespace = pd.read_csv(f"{caminho_dados}{focos_timespace}")
#focos_timespace = gpd.read_file(f"{caminho_dados}{focos_timespace}")
municipios = gpd.read_file(f"{caminho_dados}{municipios}")

### Convertendo e Incluindo Tipagens de Variáveis
# Datetime64[ns]
focos_timespace["Semana"] = pd.to_datetime(focos_timespace["Semana"])
focos_timespace = focos_timespace.sort_values(by = ["Semana"])
# Geometry
focos_timespace = focos_timespace.drop(columns = ["ponto", "geometry"])
cidades = municipios[["NM_MUN", "geometry"]]
cidades["Município"] = cidades["NM_MUN"].str.upper()
focos_timespace_poligono = pd.merge(focos_timespace, cidades, on = "Município", how = "left")
focos_timespace_poligono = focos_timespace_poligono.drop(columns = ["NM_MUN"])
#focos_timespace_poligono.to_file(f"{caminho_dados}focos_timespace_poligono.shp") 
pontos = cidades.copy()
pontos["ponto"] = pontos["geometry"].centroid
pontos = pontos[["NM_MUN", "Município", "ponto"]]
focos_timespace_centroide = pd.merge(focos_timespace, pontos, on = "Município", how = "left")
focos_timespace_centroide = focos_timespace_centroide.drop(columns = ["NM_MUN"])
#focos_timespace_centroide.to_file(f"{caminho_dados}focos_timespace_centroide.shp") 
"""
crs = {"proj" : "latlong",
       "ellps" : "WGS84",
       "datum" : "WGS84",
       "no_defs" : True}
crs = crs,

# Filter out rows with MULTIPOLYGON geometries
focos_timespace = focos_timespace[focos_timespace['geometry'].geom_type == 'POLYGON']

# Now try creating a GeoDataFrame again
focos_timespace = gpd.GeoDataFrame(focos_timespace)
#focos_timespace = gpd.GeoDataFrame(focos_timespace, geometry = "geometry")
"""
### Exibindo Informações
print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print(focos_timespace.info())
print("~"*80)
print(focos_timespace.dtypes)
print("~"*80)
print(focos_timespace)
print("="*80)


print("\n \n FOCOS DE _Aedes aegypti_ EM SANTA CATARINA - SÉRIE HISTÓRICA (DIVE/SC) \n + MUNICÍPIOS DE SANTA CATARINA (IBGE + centróide) \n")
print("\n CENTRÓIDE \n")
print(focos_timespace_centroide.info())
print("~"*80)
print(focos_timespace_centroide.dtypes)
print("~"*80)
print(focos_timespace_centroide)
print("="*80)
