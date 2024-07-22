# Automatizando roteiros de execução
"""
Tentando automatizar tudo para executar de uma única vez.
Deve-se alterar as permissões deste próprio roteiro, que originalmente são apenas leitura (w) e escrita (r).
No terminal, fazer um [ls -l] para verificar as permissões dos roteiros.
Depois executar [chmod +x {script}.sh] para incluir a permissão de executável (x).
E executar da seguinte forma [./{script}.sh]
"""
# Pré-Processamento dos Focos de _Aedes_sp. dos Municípios Catarinenses
"""
Dados brutos disponibilizados pela Diretoria de Vigilância Epidemiológica de Santa Catarina (DIVE/SC).
Inicialmente disponíveis como tabelas dinâmicas, separadas em anos (recentemente em semestres, por conta do volume de dados).
Ao final da sequência de execução, deve-se obter uma tabela única em formato pivot, onde:
-- Colunas são todos os municípios com registros de Focos de _Aedes_ sp.;
-- Linhas são as semanas epidemiológicas de toda a série histórica de registro (iniciando em 2012).
"""
python une_focos_dive.py
python focos_timespace.py
python focos_pivot.py

# Pré-Processamento dos Casos de Dengue dos Municípios Catarinenses
"""
Dados brutos disponibilizados pela Diretoria de Vigilância Epidemiológica de Santa Catarina (DIVE/SC).
Inicialmente disponíveis como tabelas dinâmicas, separadas em anos (recentemente em semestres, por conta do volume de dados).
Ao final da sequência de execução, deve-se obter uma tabela única em formato pivot, onde:
-- Colunas são todos os municípios com registros de Focos de _Aedes_ sp.;
-- Linhas são as semanas epidemiológicas de toda a série histórica de registro (iniciando em 2012).
"""
#python une_casos_sinan.py # Pensar no próximo ano
