<h1></h1>
<h1 align="center"> 🔍 PAPEMLS - Plugin de Autocorreção Código com Machine Learning e Sonarqube  <br>
  <h2 align="center">
    <a href="https://hub.docker.com/" target="_blank"><img align="center" alt="Docker" src="https://img.shields.io/badge/Docker-Imagens_Docker-black?style=for-the-badge&logo=docker&logoColor=blue"/></a>
    <a href="https://www.jenkins.io/doc/" target="_blank"><img align="center" alt="Jenkins" src="https://img.shields.io/badge/Jenkins-Pipeline-black?style=for-the-badge&logo=jenkins&logoColor=orange"/></a>
    <a href="https://docs.sonarqube.org/" target="_blank"><img align="center" alt="SonarQube" src="https://img.shields.io/badge/SonarQube-Análise-black?style=for-the-badge&logo=sonarqube&logoColor=blue"/></a>
    <a href="https://github.com/Ronynetwork/AVSAC" target="_blank"><img align="center" alt="GitHub" src="https://img.shields.io/badge/Github-Repositório-black?style=for-the-badge&logo=github&logoColor=white"></a>
    <br><br>
    <a href="#"><img align="center" alt="Desenvolvedores" src="https://img.shields.io/badge/👨🏻‍💻_Desenvolvedor-Ronyldo_Oliveira-black?style=for-the-badge"/></a>
    <a href="#"><img align="center" alt="Orientador" src="https://img.shields.io/badge/💡_Orientador-Felipe_Dantas-black?style=for-the-badge"/></a>
  </h2>
</h1>

<h1>Diagrama de Funcionamento</h1>

![image](https://github.com/Ronynetwork/PAPEMLS/blob/main/Diagrama-funcionamento.png?raw=true)

<h1>Introdução</h1>
A utilização de ferramentas de autocorreção tem ganhado destaque no mundo tecnológico, visando a correção de erros críticos e prevenção de altos custos com a exploração de falhas de segurança. O uso de tecnologias como Machine Learning (ML) e ferramentas de análise estática, como o SonarQube, tem demonstrado grande potencial para aprimorar a qualidade do software, identificando erros e prevenindo futuros problemas. São muitas as pesquisas que afirmam que a utilização do ML juntamente com ferramentas de análise estática, não só corrigem erros como também tem a capacidade de prevenir futuros problemas no código. No entanto, os maiores gargalos apresentados no desenvolvimento de aplicações desse nicho é a dificuldade de compreender e atuar na correção de erros, tanto pela alta gama de possibilidades, como também pela ausência de uma explicação clara do problema. Além disso, no cenário tecnológico atual, onde estamos imersos em avanços que auxiliam externamente no desenvolvimento de aplicações, como Inteligência Artificial e Aprendizado de Máquina, são nítidas as oportunidades de explorar essas tecnologias para melhorar a produtividade. Dessa forma, o PAPEMLS procura integrar as inovações citadas ao processo de Pipeline, aumentando assim o alcance de análises e resoluções de erros. O objetivo é facilitar o entendimento do desenvolvedor, possibilitando avanços mais eficientes no código, mediante uso da inteligência artificial com segurança e confiabilidade. Isso oferece a possibilidade de entender e corrigir erros mais gerais e aprimorar o uso do seu tempo, permitindo direcionar o foco e energia nos pontos mais críticos do projeto, os quais também são identificados pelo PAPEMLS.


# Segurança e Avisos

A utilização do PAPEMLS requer privilégios de administrador do sistema e também alterações em arquivos sensíveis dentro do sistema operacional, é importante frisar que o cuidado e responsabilidade com os dados presentes no repositório analizado é de extrema importância.

# Instalação
## Pré-requisitos

O Plugin visa a implementação de uma ferramenta que identifique, analise, atue e corrija o código fonte com problema de segurança e/ou desempenho. Para isso, será utilizada a instalação padrão do Docker 2.479.3 hospedada em uma máquina WSL2 com a distro do Ubuntu 24.04.1 LTS, CPU Intel Xeon E5-2630 v3 e 16GB RAM em conjunto com 80GB de espaço em disco. Nesse ambiente também estará presente o Jenkins 2.479.3 utilizando o Java 17.0, além disso, a imagem do SonarQube (9.9.8-community) e do Ollama (ollama/ollama).


<h3>Ubuntu (24.04.1 LTS)</h3>

<p><b>Via WSL:</b></p>
<pre>wsl --install -d Ubuntu-20.04</pre>

<p><b>Via VirtualBox:</b> <a href="https://www.virtualbox.org/wiki/Downloads">Baixar VirtualBox</a></p>

<p><b>ISO:</b> <a href="https://ubuntu.com/download/desktop">Baixar ISO do Ubuntu</a></p>

<h3>Docker (2.479.3)</h3>
<p><a href="https://docs.docker.com/engine/install/ubuntu/">Instalação do Docker</a></p>

<h3>Jenkins (2.479.3)</h3>
<p><a href="https://www.jenkins.io/doc/book/installing/linux/#debianubuntu">Instalação do Jenkins</a></p>

<h3>Ngrok (para testes localhost)</h3>
<p><a href="https://ngrok.com/downloads/linux">Baixar Ngrok</a></p>

<h3>Jenkins Plugins</h3>
<p>Pipeline Utility Steps Plugin</p>
<p>SonarQube Instalations</p>
<p>Sonar Quality Gates</p>

as tecnologias citadas acima necessitam ser instaladas antes da execução da pipeline.

# Teste Mínimo

 - Passo 1: Crie um Job em formmato de Pipeline dentro da interface do Jenkins e aponte para o repositório que apresenta o Jenkinsfile
 - Passo 2: Crie um repositório executando o compose do SonarQube para gerar o token de projeto que servirá como credencial
 - Passo 3: Configure uma chave SSH para o usuário Jenkins em seu sistema para que o mesmo possa se comunicar com o GitHub
 - Passo 4: Na aba de Credenciais do Jenkins, crie as credenciais de acesso sonar-scanner e git-token para conseguir rodar a Pipeline sem erros
 - Passo 5: Execute a Pipeline e verifique os logs em caso de problemas
 - Passo 6: Verifique o localhost:5000 que será construído pelo Flask com os erros caso sejam detectados pelo SonarQube

# Exemplo Funcional

## YouTube: 
 - Link: https://youtu.be/NRJnZRnU2C8

# Conclusão

O PAPEMLS se destaca principalmente pela possibilidade de realizar a autocorreção de erros de códigos prejudiciais, prevenindo uma possível falha de segurança apontada pelo SonarQube, tudo de forma optativa e selecionável. Essa utilização transforma o cenário atual de prevenção de erros em aplicações, auxiliando o time de desenvolvimento e segurança a identificar os problemas atuais e como futuramente poderia ser explorado por indivíduos maliciosos, além de demonstrar uma nova utilização para as ferramentas SAST.
