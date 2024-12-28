from flask import Flask, request, jsonify
import pickle

# Caminho para o arquivo de regras
#RULES_FILE_PATH = "/home/gustavocunha/TP-2/rules.pkl"
RULES_FILE_PATH = "/app/data/rules.pkl"

# Carregar o arquivo de regras e extrair as informações necessárias
with open(RULES_FILE_PATH, 'rb') as f:
    model_data = pickle.load(f)

rules = model_data["rules"]
version = model_data["version"]
model_date = model_data["date"]

# Função para gerar recomendações com base nas músicas fornecidas e nas regras carregadas
def generate_recommendations(user_songs, rules=rules, min_confidence=0.3):
    recommended = set()
    
    # Converter user_songs para conjunto
    user_songs_set = set(user_songs)
    print(f"User songs as set: {user_songs_set}")  # Print para verificar user_songs_set
    
    for rule in rules:
        antecedent, consequent, confidence = rule
        
        # Converter antecedente para conjunto
        antecedent_set = set(antecedent)
        print(f"Checking rule - Antecedent: {antecedent_set}, Consequent: {consequent}, Confidence: {confidence}")  # Print para verificar a regra
        
        # Garantir que o antecedente seja um subconjunto de user_songs
        if confidence >= min_confidence and antecedent_set.issubset(user_songs_set):
            print(f"Rule matched. Adding consequent: {consequent}")  # Print quando a regra for atendida
            recommended.update(consequent)
        elif confidence >= min_confidence and user_songs_set.issubset(antecedent_set):
            print(f"Rule matched in reverse. Adding consequent: {consequent}")  # Print para o caso reverso
            recommended.update(consequent)
    
    print(f"Recommended songs: {recommended}")  # Print para verificar as músicas recomendadas
    return list(recommended)


app = Flask(__name__)

# Endpoint para recomendações de playlists, recebe uma lista de músicas e retorna recomendações
@app.route("/api/recommender", methods=["POST"])
def recommend_playlist():
    try:
        # Obter os dados da requisição
        request_data = request.get_json()

        if "songs" not in request_data:
            return jsonify({"error": "Missing 'songs' field in the request"}), 400

        user_songs = request_data["songs"]

        # Gerar as recomendações baseadas nas músicas recebidas
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
