import requests
import json
import pandas as pd
import random
import subprocess

API_URL = "http://127.0.0.1:52111/api/recommender"
#API_URL = "http://127.0.0.1:5000/api/recommender"

def send_recommendation_request(songs):
    # Formatar a lista de músicas como string JSON
    songs_json = json.dumps(songs)

    # Comando curl
    curl_command = [
        "curl", "-s", "-X", "POST", API_URL,
        "-H", "Content-Type: application/json",
        "-d", f'{{"songs": {songs_json}}}'
    ]

    # Executa o comando curl e captura a resposta
    response = subprocess.run(curl_command, capture_output=True, text=True)

    # Exibe a resposta
    print("Resposta da API:")
    print(response.stdout)

def test_recommendation_api():
    print("Iniciando o teste da API de recomendação...\n")
    
    selected_songs = [
        "Bad and Boujee (feat. Lil Uzi Vert)", 
        "Broccoli (feat. Lil Yachty)", 
        "HUMBLE.", 
        "One Dance", 
        "T-Shirt", 
        "No Role Modelz", 
        "No Heart", 
        "XO TOUR Llif3", 
        "Deja Vu"
    ]

    print(f"Solicitando recomendação para as músicas: {selected_songs}")
    
    send_recommendation_request(selected_songs)

if __name__ == "__main__":
    test_recommendation_api()