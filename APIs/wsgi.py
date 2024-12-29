from flask import Flask, request, jsonify
import pickle
import hashlib
import os
import time

RULES_FILE_PATH = "/app/data/rules.pkl"
last_checksum = None

def get_file_checksum(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()
        return hashlib.md5(file_content).hexdigest()

def load_model():
    with open(RULES_FILE_PATH, 'rb') as f:
        model_data = pickle.load(f)
    return model_data["rules"], model_data["version"], model_data["date"]

rules, version, model_date = load_model()
last_checksum = get_file_checksum(RULES_FILE_PATH)

def generate_recommendations(user_songs, rules=rules, min_confidence=0.3):
    recommended = set()
    user_songs_set = set(user_songs)
    
    for rule in rules:
        antecedent, consequent, confidence = rule
        antecedent_set = set(antecedent)
        
        if confidence >= min_confidence and antecedent_set.issubset(user_songs_set):
            recommended.update(consequent)
        elif confidence >= min_confidence and user_songs_set.issubset(antecedent_set):
            recommended.update(consequent)
    
    return list(recommended)

app = Flask(__name__)

@app.route("/api/recommender", methods=["POST"])
def recommend_playlist():
    global rules, version, model_date, last_checksum

    try:
        current_checksum = get_file_checksum(RULES_FILE_PATH)

        if current_checksum != last_checksum:
            rules, version, model_date = load_model()
            last_checksum = current_checksum

        request_data = request.get_json()

        if "songs" not in request_data:
            return jsonify({"error": "Missing 'songs' field in the request"}), 400

        user_songs = request_data["songs"]

        recommendations = generate_recommendations(user_songs)

        return jsonify({
            "recommended_songs": recommendations,
            "model_version": version,
            "model_date": model_date
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
