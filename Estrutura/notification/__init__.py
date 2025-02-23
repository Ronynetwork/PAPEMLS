import os, requests, threading

from flask import Flask, render_template, request, jsonify
JENKINS_URL = "http://localhost:8080/job/PAPEMLS/buildWithParameters"


def create_app(test_config=None):
    app = Flask(__name__)
    #rendeniza a pagina de erro na raiz
    
    @app.route('/')
    def index():
        """Retorna a página HTML que o usuário verá."""
        return render_template('erro.html')

    @app.route("/resposta/<acao>", methods=["GET"])
    def processar_escolha(acao):
        global resposta_usuario
        resposta_usuario = acao
        return jsonify({"message": f"Escolha registrada: {acao}"}), 200
    
    @app.route('/capturar_resposta', methods=['GET'])
    def capturar_resposta_durante_pipeline():
        global resposta_usuario
        if resposta_usuario:
            return jsonify({"resposta": resposta_usuario}), 200
        return jsonify({"resposta": "Aguardando escolha..."}), 200

    app.run(host="127.0.0.1", port=5000)


if __name__ == '__main__':
    # Rodar o Flask em uma thread separada para não bloquear o Jenkins
    flask_thread = threading.Thread(target=create_app)
    flask_thread.start()
