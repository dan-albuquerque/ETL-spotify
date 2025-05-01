import pandas as pd
from sqlalchemy import create_engine
import os

# Configuração da conexão com o PostgreSQL
user = 'postgres'
password = 'senha123'
port = '5432'
database = 'postgres'

# Criar a conexão com o PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}')

# --- Carregar as dimensões ---
dimensoes_path = 'dimensoes'
csv_files = ['dim_artist.csv', 'dim_rank.csv', 'dim_stats.csv', 'dim_track.csv']

for csv_file in csv_files:
    file_path = os.path.join(dimensoes_path, csv_file)
    table_name = csv_file.replace('.csv', '')  # Nome da tabela será o nome do arquivo sem extensão
    
    # Carregar o arquivo CSV
    df = pd.read_csv(file_path, encoding='latin1')
    print(f"Carregando {csv_file} com {df.shape[0]} linhas e {df.shape[1]} colunas.")
    
    # Inserir no banco de dados
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Tabela '{table_name}' inserida com sucesso no banco de dados!")

# --- Carregar a tabela completa 'spotify_bruto' ---
csv_file = 'Most Streamed Spotify Songs 2024.csv'
df = pd.read_csv(csv_file, encoding='latin1')

print(f"DataFrame completo carregado com: {df.shape[0]} linhas e {df.shape[1]} colunas.")

table_name = 'spotify_bruto'

# Inserir no banco de dados
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Tabela completa '{table_name}' inserida com sucesso no banco de dados!")