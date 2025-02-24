import os
import requests
from flask import Flask, render_template, request, jsonify

JENKINS_URL = "http://localhost:8080/job/PAPEMLS/buildWithParameters"

# Inicializa a variável global corretamente
resposta_usuario = None  

app = Flask(__name__)

@app.route('/')
def index():
    """Retorna a página HTML que o usuário verá."""
    return render_template('erro.html')

@app.route("/resposta/<acao>", methods=["GET"])
def processar_escolha(acao):
    global resposta_usuario
    resposta_usuario = acao
    print(f"Escolha registrada: {resposta_usuario}")
    return jsonify({"message": f"Escolha registrada: {acao}"}), 200

@app.route('/capturar_resposta', methods=['GET'])
def capturar_resposta_durante_pipeline():
    global resposta_usuario
    if resposta_usuario:
        return jsonify({"resposta": resposta_usuario}), 200
    return jsonify({"resposta": "Aguardando escolha..."}), 200

if __name__ == '__main__':
    # Executa Flask no processo principal (sem threading)
    app.run(host="0.0.0.0", port=5000, debug=True)

