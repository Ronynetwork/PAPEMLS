pipeline {
    agent any
    
    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    def destinationDir= 'AVSAC'
                    git credentialsId: 'log-token-git',
                        url: 'https://github.com/Ronynetwork/AVSAC.git',
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
                    def sonarContainerExists = sh(script: 'docker ps --filter "name=sonarqube" --format "{{.Names}}"', returnStatus: true)
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
                    sleep time:34, unit: 'SECONDS'
                }
            }
        }
        stage('Análise do Código') {
            steps {
                script {
                    // Defina o caminho completo para o sonar-scanner
                    def scannerHome = tool 'sonar-scanner';
                    // Obtendo as configurações do SonarQube definidas no Jenkins pelo SonarQube Servers
                    withSonarQubeEnv('AVSAC') {
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
    // post {
    //     success {
    //         echo "subindo container ngnix com o index.html"
    //         script {
    //             def ngnixContainerName = sh(script: 'docker ps --filter "name=ngnix-app" --format "{{.Names}}"', returnStdout: true)
    //             if (ngnixContainerName) {
    //                 echo "O serviço Nginx já está em execução, reiniciando o contêiner."
    //                 sh "docker restart ngnix-app" // Reiniciar o contêiner se estiver em execução
    //             } 
    //             else {
    //                 echo "Realizando build do Nginx"
    //                 sh 'docker compose -f ./Estrutura/docker-compose-ngnix.yml up -d'
    //             }                
    //         }
    //     }
    //     failure {
    //         script{
    //             echo 'realizando a correcao de bugs...'
    //             sh 'python3 Estrutura/source.py'
    //             echo 'Realizando commit'
    //             sh 'chmod +x ./Estrutura/git_branch.sh'
    //             sh './Estrutura/git_branch.sh'
    //         }
    //     }
    // }   
}
