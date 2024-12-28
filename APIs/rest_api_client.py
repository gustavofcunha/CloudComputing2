import requests
import json
import pandas as pd
import random

API_URL = "http://127.0.0.1:52111/api/recommender"
CSV_FILE = "https://raw.githubusercontent.com/gustavofcunha/CloudComputing2/main/spotify/2023_spotify_songs.csv"  
NUM_SONGS = 10

def load_songs_from_csv(csv_file):
    """Carrega as músicas do arquivo CSV."""
    df = pd.read_csv(csv_file)
    return df['track_name'].tolist()

def generate_song_request(songs, num_songs):
    """Seleciona um número de músicas aleatórias do conjunto."""
    if num_songs > len(songs):
        return songs
    return random.sample(songs, num_songs)

def send_recommendation_request(songs):
    """Envia a requisição de recomendação para o servidor e retorna a resposta."""
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"songs": songs})
    
    response = requests.post(API_URL, data=payload, headers=headers, timeout=300)

    if response.status_code == 200:
        print("Recomendação recebida:", response.json())
    else:
        print(f"Erro {response.status_code}: {response.text}")

def test_recommendation_api(csv_file, num_songs):
    """Testa a API de recomendação com o número de músicas fornecido."""
    print("Iniciando o teste da API de recomendação...\n")
    
    # Carrega as músicas do CSV
    songs = load_songs_from_csv(csv_file)
    
    # Gera uma lista de músicas aleatórias
    selected_songs = generate_song_request(songs, num_songs)
    
    print(f"Solicitando recomendação para as músicas: {selected_songs}")
    
    send_recommendation_request(selected_songs)

if __name__ == "__main__":
    test_recommendation_api(CSV_FILE, NUM_SONGS)
