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

    @app.route("/resposta/<acao>", methods=["GET"])
    def processar_escolha(acao):
        global resposta_usuario
        resposta_usuario = acao
        print(resposta_usuario)
        return jsonify({"message": f"{acao}"}), 200

    @app.route('/capturar_resposta', methods=['GET'])
    def capturar_resposta_durante_pipeline():
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
