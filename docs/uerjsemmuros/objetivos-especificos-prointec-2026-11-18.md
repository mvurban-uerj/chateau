# Objetivos específicos do PROINTEC — atividades do grupo de trabalho

Levantamento de 18/11/2026 para subsidiar o pôster. Reproduzimos abaixo os itens da proposta copiada em `chateau/docs/talk-ia.md`, omitindo os nomes atribuídos a cada objetivo. Nos comentários, descrevemos apenas entregas que conseguimos confirmar nos registros do projeto. Em **Uso de IA na execução**, relatamos como empregamos um assistente de IA para avançar o trabalho de pesquisa e desenvolvimento. Deixamos o campo vazio quando não encontramos confirmação suficiente; isso não significa que a atividade não ocorreu.

## Objetivo específico 1 — Selecionar modelos para medir conhecimento de especialistas

### 1.1 Realizar uma revisão quasi-sistemática da literatura com o objetivo de identificar modelos para medir conhecimento de pessoas

**Comentário:**

### 1.2 Avaliar a eficácia dos modelos resultantes da Etapa 1.1

**Comentário:**

### 1.3 Selecionar um ou mais modelos resultantes da Etapa 1.2

**Comentário:**

### 1.4 Escrever um artigo para revista científica nacional ou internacional para divulgar esta revisão quasi-sistemática

**Comentário:**

### 1.5 Atender às considerações dos revisores de revista científica

**Comentário:**

## Objetivo específico 2 — Coletar dados e metadados utilizados para estimar o conhecimento de pessoas

### 2.1 Realizar uma revisão quasi-sistemática da literatura (incluindo a análise de documentos da Uerj) com o objetivo de identificar dados e metadados utilizados para estimar o conhecimento de pessoas

**Comentário:**

### 2.2 Realizar um survey para identificar ferramentas ETL (Extrair, Transformar e Carregar)

**Comentário:**

### 2.3 Criar um banco de dados de teste

**Comentário:** Criamos o grafo acadêmico no Neo4j a partir de arquivos Cypher gerados pelo módulo `chateau-data`. Para alimentar esse banco, desenvolvemos um pipeline de ETL específico para as fontes disponíveis: currículos Lattes e certificados em PDF, dados da Sucupira/CAPES em PDF e pela API. Os extratores leem as fontes, normalizam e consolidam os valores conforme o modelo acadêmico `rev_6_training`, geram nós e relações, produzem o Cypher de carga e relatórios de proveniência e qualidade. Essa abordagem permite refazer a carga e conferir de onde cada dado veio. A extração usa regras determinísticas. O projeto também dispõe de um Neo4j local de exemplo, separado do banco no servidor de avaliação, para testar a carga e a integração. Em 03/11, geramos o Cypher completo da rev_6 e carregamos no banco do servidor de avaliação após backup; a conferência registrou 488 nós e 603 relações de domínio.

**Uso de IA na execução:** Usamos um assistente de IA para apoiar a implementação e a revisão dos extratores, da consolidação das fontes, da geração de Cypher e dos testes do pipeline. Conferimos o resultado contra o modelo rev_6, os arquivos de origem e o grafo carregado.

### 2.4 Criar um banco de dados para avaliação, utilizando ferramentas ETL, considerando as normas da Uerj e leis sobre dados de pessoas

**Comentário:** Criamos também um banco de dados no servidor de avaliação da Cotplan. Instalamos o Neo4j em Docker, criamos a conta e o banco, importamos o arquivo Cypher gerado pelo `chateau-data` e autorizamos o acesso da equipe para examinar os dados. Reaproveitamos nosso pipeline de ETL para transformar as fontes acadêmicas em grafo e transferir a carga para esse ambiente de avaliação. Registramos a proveniência dos dados e os problemas de qualidade para conferir as informações usadas. A instalação e a importação estão documentadas; ainda não encontramos nesses registros comprovação de uma avaliação de eficácia concluída nem de uma análise formal de conformidade às normas da Uerj e à legislação de proteção de dados.

**Uso de IA na execução:** Usamos um assistente de IA no desenvolvimento do pipeline e do gerador de Cypher que prepararam os dados e a carga do banco de avaliação, como descrito no item 2.3.

### 2.5 Escrever um artigo para revista científica nacional ou internacional para divulgar o resultado deste objetivo específico

**Comentário:**

### 2.6 Atender às considerações dos revisores de revista científica

**Comentário:**

## Objetivo específico 3 — Planejar e desenvolver um agente virtual reutilizando conhecimento e software

### 3.1 Revisão da literatura sobre conceitos, arquitetura e ferramentas para o desenvolvimento de agentes virtuais

**Comentário:**

### 3.2 Entendimento dos conceitos, arquiteturas e ferramentas selecionadas na Etapa 3.1

**Comentário:** Definimos e documentamos o fluxo do Chateau: recebemos a pergunta pela interface, aplicamos as regras de acesso na API e encaminhamos a busca à orquestração. O modelo de IA gera uma consulta Cypher, e obtemos os dados da resposta no Neo4j. Comparamos duas implementações da orquestração, em Python e Quarkus; adotamos Quarkus como padrão e mantivemos Python para comparação. Aplicamos essa arquitetura no produto, mas não encontramos registro suficiente para afirmar que concluímos a revisão de literatura prevista em 3.1.

**Uso de IA na execução:** Usamos um assistente de IA para apoiar a leitura do código e dos contratos, a implementação da alternativa em Quarkus e a preparação da comparação automatizada com Python. A escolha da arquitetura foi registrada pela equipe após verificar o comportamento das duas implementações.

### 3.3 Definir os requisitos iniciais e ajustar as restrições de projeto do agente virtual

**Comentário:** Definimos e refinamos os contratos da busca, do acesso e da interface ao longo do desenvolvimento. Selecionamos o modelo de IA no catálogo administrativo; na API, conferimos seu cadastro e enviamos à orquestração o nome técnico, o formato de prompt e as URLs dos servidores. Permitimos somente consultas Cypher de leitura. Quando não há modelo disponível ou ocorre falha de modelo, identificamos a resposta como simulada na interface. Também definimos autorização do usuário, limite da pergunta e separação entre dados reais do grafo e campos ainda simulados. Registramos essas regras no domínio e as implementamos nos componentes responsáveis, ajustando os contratos conforme as decisões do projeto.

**Uso de IA na execução:** Usamos um assistente de IA para organizar as decisões em contratos e documentação, confrontá-las com o código e apoiar a implementação das regras de acesso e busca. Revisamos as propostas geradas à luz das decisões registradas e dos testes dos serviços.

### 3.4 Definir e configurar o ambiente de desenvolvimento

**Comentário:** Configuramos o ambiente do Chateau em serviços separados: web Next.js, API Express com PostgreSQL, orquestração Quarkus e Neo4j. Usamos Docker Compose para subir a aplicação localmente e um perfil de IA para acrescentar a orquestração e um Neo4j de exemplo. Também configuramos o ambiente de avaliação e um workflow que executa testes, constrói imagens e disponibiliza a versão quando acionado pela branch `deploy`. Com essa organização, desenvolvemos e testamos cada parte mantendo contratos entre os serviços. Ainda precisamos verificar cada fluxo no servidor de avaliação.

**Uso de IA na execução:** Usamos um assistente de IA para apoiar a escrita e a revisão dos arquivos de configuração, a integração dos serviços no Compose e a documentação dos comandos de execução. Verificamos a configuração com builds, testes e subida local dos serviços registrados no projeto.

### 3.5 Ciclos ágeis de desenvolvimento do agente virtual

**Comentário:** Desenvolvemos o Chateau em incrementos de interface, API, administração e busca. Implementamos autenticação, autorização, conversas e histórico, consulta em linguagem natural e apresentação dos resultados. No Admin, criamos o cadastro de versões de modelos de IA, nome técnico, disponibilidade e lista ordenada de URLs dos servidores; em falhas técnicas definidas, tentamos outra URL pela orquestração. Também implementamos um modelo orquestrador opcional que usa trocas anteriores da conversa para reformular a pergunta antes de enviá-la ao modelo que gera Cypher; deixamos o fluxo visível para inspeção. Criamos testes dirigidos para o backend e a orquestração e comparamos a estrutura do grafo rev_6 com o esquema enviado ao modelo.

**Uso de IA na execução:** Usamos um assistente de IA nos ciclos de desenvolvimento para propor e revisar código, criar testes, comparar esquemas e resultados, investigar falhas e atualizar a documentação. Conferimos as mudanças por testes e pelas revisões das regras do produto.

### 3.6 Avaliar os resultados e registrar o agente virtual junto ao Instituto Nacional da Propriedade Industrial (INPI)

**Comentário:**

## Objetivo específico 4 — Prover infraestrutura computacional para desenvolvimento, teste, treinamento e hospedagem

### 4.1 Instalar e configurar as aplicações do ambiente de desenvolvimento

**Comentário:** No escopo da aplicação Chateau, configuramos os serviços de desenvolvimento em containers: web, API, PostgreSQL, orquestração e Neo4j de exemplo, com variáveis de ambiente e perfis de execução. Assim, subimos a aplicação básica e acrescentamos os serviços de IA e grafo quando necessários. Também configuramos testes para os componentes de software. Aqui relatamos apenas a infraestrutura da aplicação documentada nos repositórios, sem incluir a instalação de equipamentos ou ambientes de treinamento de modelos.

**Uso de IA na execução:** Usamos um assistente de IA para apoiar a configuração dos containers e perfis, integrar a orquestração e o Neo4j de exemplo e revisar a documentação de execução. Conferimos a configuração com testes e execução local dos serviços.

### 4.2 Configurar o computador servidor do LTI para testes e hospedagem

**Comentário:**

### 4.3 Adaptar os scripts de treinamento dos modelos para utilizar os recursos computacionais do supercomputador Singrar

**Comentário:**

### 4.4 Otimizar os scripts de treinamento dos modelos

**Comentário:**

### 4.5 Gerenciar o backup de todos os artefatos criados por este projeto PROINTEC

**Comentário:**

### 4.6 Incluir redundância para o serviço de hospedagem

**Comentário:**

## Fontes principais para conferência

- `chateau/docs/talk-ia.md`: enunciados da proposta.
- `chateau/dominio/dados/fontes-e-pipeline.md` e `chateau/dominio/modelo/grafo-academico.md`: extração, proveniência, modelo rev_6 e limites.
- `chateau/chateau-data/README.md` e `chateau/chateau-data/scripts/chateau-extract/`: módulo de dados e código do pipeline.
- `chateau/dominio/tech/arquitetura.md`, `contrato-de-busca.md` e `operacao-e-validacao.md`: arquitetura, busca e ambientes.
- `chateau/chateau-expert/backend/src/services/search.service.ts` e `chateau/chateau-expert/orchestration/quarkus/`: integração da busca e modelo orquestrador.
- `chateau/docs/todo.md`, seção **2. Dados**: geração e carga da rev_6, com contagens e pendências.
- `chateau/docs/reunioes/2026-08-05.md`: instalação do Neo4j no servidor da Cotplan, criação do banco, importação do Cypher e acesso à equipe.
- Históricos Git de `chateau-data`, `chateau-expert` e da raiz: registros de colaboração com assistente de IA em mudanças do pipeline (`fd35b8e`, `462d518`), da infraestrutura (`048019d`), da orquestração e seus testes (`8c870dc`, `91c2423`, `e6f4add`) e da documentação (`760b07b`). Esses registros sustentam o uso de IA no desenvolvimento, mas não detalham cada interação com o assistente.

Mantivemos todos os itens da proposta para apresentar o trabalho em conjunto. Os campos sem comentário aguardam confirmação da entrega e não representam atividades descartadas.
