# nourrir_flask/app.py

from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# Politique d'intégration
@app.route("/politique")
def politique():
    return render_template("politique.html")

# Contact RH
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Proxy pour NuRiH Ami chatbot
@app.route("/nurih-ami", methods=["POST"])
def nurih_ami():
    """
    Proxy: receive chat message from frontend, forward to Ollama (phi:latest), return result.
    """
    # Change if Ollama API moves
    OLLAMA_URL = "http://192.168.2.10:11434/api/chat"
    try:
        data = request.json
        user_msg = data.get("message", "")
        session_id = data.get("session", "public")
        if not user_msg:
            return jsonify({"error": "Aucun message reçu"}), 400

        payload = {
            "model": "phi:latest",
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es NuRiH Ami, assistant éducatif pour le bien-être, nutrition et créativité. Sois amical, inclusif, bref et adapté à tous publics."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            "stream": False,
            "session": session_id
        }

        resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        # "message": {"role": "assistant", "content": "…"}
        return jsonify({"response": result.get("message", {}).get("content", "Je n'ai pas compris, peux-tu reformuler ?")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Pour servir correctement tous fichiers dans assets
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

# Optionnel : favicon (sinon supprime la route)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
