import os
import pickle
import time
import random
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

RULES_FILE_PATH = "/app/data/rules.pkl"

DATASET_PATHS = {
    "initial": "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_ds1.csv",
    "songs": "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_songs.csv"
}

# Variáveis globais para mapeamento
track_name_to_uri = {}
track_uri_to_name = {}
last_modified_time = '2024-12-10'

def load_datasets():
    """Carrega os datasets e inicializa os mapeamentos."""
    global track_name_to_uri, track_uri_to_name
    try:
        dfs = [pd.read_csv(path) for path in DATASET_PATHS]
        combined_df = pd.concat(dfs, ignore_index=True)

        track_name_to_uri = pd.Series(combined_df.track_uri.values, index=combined_df.track_name).to_dict()
        track_uri_to_name = pd.Series(combined_df.track_name.values, index=combined_df.track_uri).to_dict()

        print("Datasets carregados com sucesso.")
        print(f"Total de músicas únicas: {len(track_name_to_uri)}")
    except Exception as e:
        print(f"Erro ao carregar datasets: {e}")

def load_model():
    """Carrega o modelo do arquivo de regras."""
    try:
        with open(RULES_FILE_PATH, 'rb') as f:
            model = pickle.load(f)
            print("Modelo carregado com sucesso.")
            print(f"Total de regras: {len(model)}")
            return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return []

def model_is_updated():
    """Verifica se o arquivo do modelo foi atualizado."""
    global last_modified_time
    try:
        current_modified_time = os.path.getmtime(RULES_FILE_PATH)
        if last_modified_time is None or current_modified_time > last_modified_time:
            last_modified_time = current_modified_time
            return True
    except FileNotFoundError:
        print("Arquivo de regras não encontrado.")
        return False
    return False

@app.route('/api/recommender', methods=['POST'])
def recommend():
    """Lida com requisições de recomendação."""
    try:
        # Verifica se o modelo foi atualizado e recarrega se necessário
        if model_is_updated():
            app.model = load_model()

        # Obtém os dados da requisição JSON
        data = request.get_json(force=True)  # Ignora o header Content-Type
        user_songs = data.get('songs', [])

        print(f"Músicas recebidas: {user_songs}")

        if not user_songs:
            return jsonify({"error": "No songs provided"}), 400

        # Converte nomes para URIs
        user_uris = [track_name_to_uri.get(song) for song in user_songs if song in track_name_to_uri]
        print(f"Músicas convertidas para URIs: {user_uris}")

        if not user_uris:
            # Músicas não encontradas no dataset, tentamos buscar pelas regras
            user_uris = []  # Limpa, pois não há músicas encontradas diretamente

        # Gera as recomendações com base nas regras do modelo
        recommendations = set()

        # Tenta gerar recomendações com as músicas fornecidas
        for rule in app.model:
            if set(user_uris).intersection(rule[0]):
                recommendations.update(rule[1])

        print(f"Recomendações antes da conversão: {recommendations}")

        # Caso não tenha músicas suficientes, preenche com músicas populares ou aleatórias
        if len(recommendations) < 5:
            # Seleciona aleatoriamente músicas populares para completar a lista
            popular_songs = list(track_uri_to_name.values())
            random.shuffle(popular_songs)  # Embaralha para garantir variedade
            recommendations.update(popular_songs[:5 - len(recommendations)])

        # Converte URIs recomendadas de volta para nomes
        recommended_songs = [track_uri_to_name.get(uri, uri) for uri in recommendations]
        print(f"Recomendações finais: {recommended_songs}")

        # Resposta da API com as recomendações
        response = {
            'songs': list(recommended_songs), 
            'version': '1.0.0',
            'model_date': time.ctime(last_modified_time)  
        }
        return jsonify(response)

    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Carrega os datasets e inicializa os mapeamentos
    print("Iniciando o servidor e carregando os datasets...")
    load_datasets()

    # Carrega o modelo inicialmente
    if os.path.exists(RULES_FILE_PATH):
        app.model = load_model()
        last_modified_time = os.path.getmtime(RULES_FILE_PATH)
    else:
        app.model = []

    app.run(host='0.0.0.0', port=5000)
