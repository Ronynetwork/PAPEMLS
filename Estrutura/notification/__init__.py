import os
import requests
from flask import Flask, render_template, request, jsonify

JENKINS_URL = "http://localhost:8080/job/PAPEMLS/buildWithParameters"

resposta_usuario = None

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        """Retorna a página HTML que o usuário verá."""
        return render_template('erro.html')

    #  Rota para receber a ação do botão (POST)
    @app.route('/receber_escolha', methods=['POST'])
    def receber_escolha():
        global resposta_usuario
        data = request.get_json()
        if data and "resposta" in data:
            resposta_usuario = data["resposta"]
            print(f"Usuário escolheu: {resposta_usuario}")
            return jsonify({"message": f"Escolha '{resposta_usuario}' salva com sucesso"}), 200
        return jsonify({"error": "Nenhuma resposta enviada"}), 400

    # Rota para o Jenkins verificar a escolha do usuário (GET)
    @app.route('/capturar_resposta', methods=['GET'])
    def capturar_resposta():
        global resposta_usuario
        if resposta_usuario:
            return jsonify({"resposta": resposta_usuario}), 200
        return jsonify({"resposta": "Aguardando escolha..."}), 200

    # 🔹 Adicionando o cabeçalho CSP para permitir conexões com o Jenkins
    @app.after_request
    def add_csp_header(response):
        response.headers['Content-Security-Policy'] = "connect-src 'self' http://localhost:8080;"
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="localhost", port=5000, debug=True)
