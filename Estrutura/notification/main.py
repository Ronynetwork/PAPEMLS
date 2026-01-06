from flask import Flask, render_template, request, jsonify

JENKINS_URL = "http://localhost:8080/job/PAPEMLS/buildWithParameters"

resposta_usuario = None

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        """Retorna a página HTML que o usuário verá."""
        return render_template('index.html')

    #  Rota para receber a ação do botão (POST)
    @app.route('/receber_escolha', methods=['POST'])
    def receber_escolha():
        global resposta_usuario, erros_usuario
        data = request.get_json()
        resposta_usuario = data.get("resposta")
        erros_usuario = data.get("erros", [])
        return jsonify({"message": "Escolha recebida"}), 200
    
    # Verificando escolha feita
    @app.route('/capturar_resposta', methods=['GET'])
    def capturar_resposta():
        global resposta_usuario, erros_usuario
        if resposta_usuario:
            return jsonify({"resposta": resposta_usuario, "erros": erros_usuario}), 200
        return jsonify({"resposta": "Aguardando escolha...", "erros": []}), 200

    # 🔹 Adicionando o cabeçalho CSP para permitir conexões com o Jenkins
    @app.after_request
    def add_csp_header(response):
        response.headers['Content-Security-Policy'] = "connect-src 'self' http://localhost:8080;"
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="localhost", port=5000, debug=True)
