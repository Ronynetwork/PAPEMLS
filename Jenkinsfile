pipeline {
    agent any

    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    def destinationDir= 'PAPEMLS'
                    git credentialsId: 'log-token-git',
                        url: 'https://github.com/Ronynetwork/PAPEMLS.git',
                        branch: 'main'
                        directory: destinationDir
                }
            }
        }
        stage('Instalação do Docker') {
            steps {
                script {
                    sh 'chmod +x Estrutura/docker_setup.sh'
                    sh './Estrutura/docker_setup.sh'
                }
            }
        }
        stage('Configuração do SonarQube') {
            steps {
                script {
                    def sonarContainerExists = sh(script: 'docker ps --filter "names=sonarqube" --format "{{.Names}}"', returnStatus: true)
                    if (sonarContainerExists == 1) {
                        echo "O serviço SonarQube já está em execução, reiniciando o contêiner."
                        sh "docker restart sonarqube" // Reiniciar o contêiner se estiver em execução
                    }
                    else {
                        echo "Realizando build do SonarQube"
                        sh 'docker compose -f Estrutura/docker-compose-sonar.yml up -d --remove-orphans'
                    }
                }
            }
        }
        stage('Delay') {
            steps {
                script {
                    echo 'Aguardando 35 segundos para a inicialização completa do SonarQube...'
                    sleep time:36, unit: 'SECONDS'
                }
            }
        }
        stage('Análise do Código') {
            steps {
                script {
                    // Defina o caminho completo para o sonar-scanner
                    def scannerHome = tool 'sonar-scanner';
                    // Obtendo as configurações do SonarQube definidas no Jenkins pelo SonarQube Servers
                    withSonarQubeEnv('PAPEMLS') {
                        env.SONAR_PROJECT_KEY = "${SONAR_CONFIG_NAME}"
                        env.SONAR_URL = "${SONAR_HOST_URL}"
                        // Executando a análise do código
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.sources=. \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.exclusions=**/Estrutura/**,**/papemls/**
                        """
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps{
                waitForQualityGate abortPipeline: true
            }
        }
    }
    post {
        failure {
            script{
                echo 'instalando pacotes necessários'
                sh 'chmod +x ./Estrutura/setup.sh ; ./Estrutura/setup.sh'

                withSonarQubeEnv('PAPEMLS') {
                    env.SONAR_AUTH_TOKEN = "${SONAR_AUTH_TOKEN}"
                    echo "${SONAR_AUTH_TOKEN}"
                    def output = sh(script: 'python3 Estrutura/source.py', returnStdout: true).trim()
                    env.ERROR_POINT=output
                    echo "Erro retornado ${ERROR_POINT}"
                }
            }
            script {
                echo 'Criando ambiente virtual e instalando dependências...'
                sh '''
                    docker compose -f Estrutura/docker-compose-ML.yml up -d
                    sleep 20
                    docker exec ollama-ml ollama run llama3.2:1b
                '''
            }

            script{
                echo 'Executando arquivo de ML'
                sh '''
                    . papemls/bin/activate
                    chmod +x Estrutura/ML.py
                    python3 Estrutura/ML.py
                '''
            }
            script {
                echo 'Subindo flask em background'
                sh '''
                    . papemls/bin/activate
                    chmod +x Estrutura/notification/__init__.py
                    python3 Estrutura/notification/__init__.py &
                '''
            }
            script {
                // Aguardar que o Flask capture a resposta do usuário
                echo 'Aguardando resposta do usuário...'
                // Aqui você pode fazer uma requisição para o Flask ou esperar até que ele termine
                def resposta = sh(script: 'curl -X GET http://localhost:5000/capturar_resposta', returnStdout: true).trim()
                echo "Resposta recebida: ${resposta}"
                
                // A partir da resposta, você pode tomar ações dentro da pipeline
                if (resposta == "corrigir") {
                    echo "Ação de corrigir selecionada!"
                    // Implementar lógica de correção
                } else {
                    echo "Ação de ignorar selecionada!"
                    // Implementar lógica de ignorar
                }
            }
        }
    }
}
