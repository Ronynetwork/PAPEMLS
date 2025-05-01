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
                    sleep time:35, unit: 'SECONDS'
                }
            }
        }
        stage('Análise do Código') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner';
                    withSonarQubeEnv('PAPEMLS') {
                        env.SONAR_PROJECT_KEY = "${SONAR_CONFIG_NAME}"
                        env.SONAR_URL = "${SONAR_HOST_URL}"
                        
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=teste_script \
                            -Dsonar.scm.exclusions.disabled=true \
                            -Dsonar.host.url=${SONAR_URL}
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
                    while [ "$(docker inspect --format='{{.State.Health.Status}}' ollama-ml)" != "healthy" ]; do
                        echo "Aguardando ollama-ml ficar pronto..."
                        sleep 2
                    done
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
                    pwd
                    tree Estrutura/notification
                    chmod +x Estrutura/notification/main.py
                    python3 Estrutura/notification/main.py &
                '''
            }
            script {
                // Aguardar que o Flask capture a resposta do usuário
                echo 'Aguardando resposta do usuário... visite http://127.0.0.1:5000/'
                // Aqui você pode fazer uma requisição para o Flask ou esperar até que ele termine
                    def startTime = System.currentTimeMillis()
                    def duration = 5 * 60 * 1000  // 5 minutos em milissegundos

                    while ((System.currentTimeMillis() - startTime) < duration) {
                        def resposta = sh(script: 'curl -s -X GET http://127.0.0.1:5000/capturar_resposta', returnStdout: true).trim()

                    if (resposta == "corrigir") {
                        echo "Resposta recebida: ${resposta}"
                        env.ACTION = resposta
                        def code_source = sh(script: 'python3 Estrutura/source.py ', returnStdout: true).trim()
                        env.code = code_source
                        echo "${code_source}"

                        sh '''
                            chmod +x Estrutura/ML_autocorrigir.py Estrutura/git_branch.sh
                            python3 Estrutura/ML_autocorrigir.py
                            ./Estrutura/git_branch.sh
                        '''
                        break  // Sai do loop ao corrigir
                    } else if (resposta == 'ignorar') {
                        echo 'Foi solicitada a ação de ignorar!'
                        break  // Sai do loop se a ação for ignorar
                    } else {
                        sleep 5  // Espera 5 segundos antes da próxima requisição
                    }
                }
                
            }
        }
    }
}
