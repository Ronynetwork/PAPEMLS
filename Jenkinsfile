pipeline {
    agent any
    
    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    def destinationDir= 'AVSAC'
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
                    // Defina o caminho completo para o sonar-scanner
                    def scannerHome = tool 'sonar-scanner';
                    // Obtendo as configurações do SonarQube definidas no Jenkins pelo SonarQube Servers
                    withSonarQubeEnv('PAPEMLS') {
                        env.SONAR_PROJECT_KEY = "${SONAR_CONFIG_NAME}"
                        env.SONAR_URL = "${SONAR_HOST_URL}"
                        // Executando a análise do código sem especificar sonar.sources
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.sources=. \
                        -Dsonar.projectKey=${SONAR_CONFIG_NAME} \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN} \
                        -Dsonar.exclusions=**/Estrutura/**
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
                echo 'Realizando o GET de bugs...'
                def output = sh(script: 'python3 Estrutura/source.py', returnStdout: true).trim()
                env.ERROR_POINT=output
                echo "Erro retornado ${ERROR_POINT}"
            }
            script {
                echo 'Criando ambiente virtual e instalando dependências...'
                sh 'docker compose -f Estrutura/docker-compose-ML.yml up -d&& docker exec -dti ollama-ML ollama run llama3.2:1b '
            }

            script{
                echo 'Executando arquivo de ML'
                sh 'chmod +x Estrutura/ML.py'
                sh 'python3 Estrutura/ML.py'
            }
            script {
                echo "Subindo servidor externo com relatório"
                sh 'docker compose -f Estrutura/docker-compose-ngnix.yml up -d'
                
                echo 'http://127.0.0.1:8083/'
            }
            
            // script{
            //     echo 'Realizando commit'
            //     sh 'chmod +x ./Estrutura/git_branch.sh'
            //     sh './Estrutura/git_branch.sh'
            // }
        }
    }   
}
