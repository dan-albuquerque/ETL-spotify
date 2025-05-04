# 🎧 Spotify Analytics Dashboard

Projeto de Engenharia de Dados & Data Science que coleta, limpa, armazena e visualiza dados das músicas mais ouvidas do Spotify em 2024.

## 🔍 Objetivo

Construir um pipeline ETL que:
- Extrai dados do [Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024)
- Realiza transformações e limpezas no dataset
- Carrega os dados normalizados em um banco de dados PostgreSQL (Data Warehouse)
- Cria dashboards interativos usando o **Metabase**


## 🛠️ Tecnologias e Ferramentas

- **Python (Pandas, SQLAlchemy)**
- **Jupyter Notebook / Google Colab**
- **PostgreSQL (via Docker)**
- **Metabase (via Docker)**
- **Kaggle API**
- **SQL**

## 🧱 Estrutura do Projeto

```bash
├── dimensoes/
│   ├── dim_artist.csv
│   ├── dim_track.csv
│   ├── dim_rank.csv
│   └── dim_stats.csv
├── extract.py            #  Extração os dados 'Most Streamed Spotify Songs 2024.csv' e coloca no mesmo diretório
├── transform.ipynb       # Limpeza e criação das dimensões
├── load_postgres.py      # Envio das dimensões para o PostgreSQL
├── requirements.txt
├── README.md
```

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório e vá para a pasta do projeto 
```bash
git clone https://github.com/dan-albuquerque/ETL-spotify.git
```

### 2. Inicie o PostgreSQL e Metabase com Docker

```bash
# PostgreSQL
docker run --name meu_postgres -e POSTGRES_PASSWORD=senha123 -p 5432:5432 -d postgres

# Metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### 3. Crie um ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Execute os scripts ETL
- Execute o `extract.py`
- Abra o `transform.ipynb` e rode todas as células
- Depois execute `load.py` para carregar as tabelas no PostgreSQL

```bash
python extract.py
python load.py
```

## 📊 Dashboard

Acesse o Metabase em:  
**http://localhost:3000**

Visualizações criadas:
- Top 10 músicas no Spotify
- Top 10 artistas com mais streams
- Comparativo de popularidade por plataforma (Spotify, YouTube, TikTok)

### Consultas SQL usadas
#### 🎵 Top 10 Músicas (por Spotify Streams)

```sql
SELECT *
FROM (
    SELECT DISTINCT ON (t."Track")
        t."Track",
        a."Artist",
        s."Spotify Streams"
    FROM dim_track t
    JOIN dim_stats s ON t.track_id = s.track_id
    JOIN dim_artist a ON t.artist_id = a.artist_id
    WHERE s."Spotify Streams" IS NOT NULL
    ORDER BY t."Track", s."Spotify Streams" DESC
) AS ranked_tracks
ORDER BY "Spotify Streams" DESC
LIMIT 10;
```

---

#### 🎤 Top 10 Artistas (por Spotify Streams acumulados)

```sql
SELECT a."Artist", SUM(s."Spotify Streams") AS total_streams
FROM dim_track t
JOIN dim_artist a ON t.artist_id = a.artist_id
JOIN dim_stats s ON t.track_id = s.track_id
GROUP BY a."Artist"
ORDER BY total_streams DESC
LIMIT 10;
```

---

#### 📊 Popularidade Média por Plataforma

```sql
SELECT 'Spotify Popularity' AS platform, AVG(s."Spotify Popularity") AS avg_popularity FROM dim_stats s
UNION
SELECT 'TikTok Likes', AVG(s."TikTok Likes") FROM dim_stats s
UNION
SELECT 'YouTube Views', AVG(s."YouTube Views") FROM dim_stats s;
```

---

#### 📈 Média de Playlist Count por Plataforma

```sql
SELECT 'Spotify Playlist Count' AS platform, AVG("Spotify Playlist Count") FROM dim_stats
UNION
SELECT 'Apple Music Playlist Count', AVG("Apple Music Playlist Count") FROM dim_stats
UNION
SELECT 'Deezer Playlist Count', AVG("Deezer Playlist Count") FROM dim_stats
UNION
SELECT 'Amazon Playlist Count', AVG("Amazon Playlist Count") FROM dim_stats;
```

## 📁 Dimensões Criadas

- **dim_artist**: informações únicas de artistas  
- **dim_track**: músicas com metadados  
- **dim_rank**: posição no ranking e score  
- **dim_stats**: estatísticas de plataformas (streams, likes, views)
