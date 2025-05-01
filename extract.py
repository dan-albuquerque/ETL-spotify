import kagglehub
import shutil
import os

# Baixar o dataset usando o kagglehub
caminho_dataset = kagglehub.dataset_download("nelgiriyewithana/most-streamed-spotify-songs-2024")

print("Caminho para os arquivos do dataset:", caminho_dataset)

# Listar arquivos baixados
print("Arquivos baixados:")
for arquivo in os.listdir(caminho_dataset):
  print(arquivo)

# Caminho do arquivo de origem
origem = os.path.join(caminho_dataset, "Most Streamed Spotify Songs 2024.csv")

# Diretório de destino: mesmo diretório do notebook
diretorio_destino = os.getcwd()

# Copiar o arquivo para o diretório atual
shutil.copy(origem, diretorio_destino)

print(f"Arquivo copiado para {diretorio_destino}")