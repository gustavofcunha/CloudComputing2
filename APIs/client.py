import requests
import json
import pandas as pd
import random
import subprocess

API_URL = "http://127.0.0.1:5000/api/recommender"

def send_recommendation_request(songs):
    songs_json = json.dumps(songs)
    curl_command = [
        "curl", "-s", "-X", "POST", API_URL,
        "-H", "Content-Type: application/json",
        "-d", f'{{"songs": {songs_json}}}'
    ]

    try:
        response = subprocess.run(curl_command, capture_output=True, text=True)
        if response.returncode != 0:
            print("error:  unable to connect to api check the endpoint or api status")
            return

        if response.stdout:
            print("api response")
            print(response.stdout)
        else:
            print("api responded but the response body is empty")

    except Exception as e:
        print(f"error:  occurred while communicating with the api {e}")

def test_recommendation_api():
    print("starting api recommendation test")
    
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

    print(f"requesting recommendation for songs {selected_songs}")
    send_recommendation_request(selected_songs)

if __name__ == "__main__":
    test_recommendation_api()
