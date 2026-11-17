# Contrato de novos modelos de Cypher — 17/11/2026

## Contexto

Em 16/11, Edson informou que testou, a partir da máquina Chateau, os modelos em duas portas, cada um em sua GPU. Para `chateau-data-gemma4-31b-cypher-v2-4000-A-s1234`, a pergunta “Quantos artigos existem?” produziu `MATCH (a:Article) RETURN count(DISTINCT a) AS total`; executada no Neo4j, retornou 919. Ele relatou que a parte gráfica não funcionava. Em 17/11, Marcelo testou pela interface três cadastros que apontam para `http://host.docker.internal:11434`: os dois nomes `v2-4000` falharam com “O serviço de busca não respondeu”, enquanto `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` trouxe resultado. O cadastro `v2-4000-A-s1234-rpo-2200` tem ainda uma URL secundária de teste (`https://teste.com`).

O código do Expert consultado em 17/11 associa apenas `chateau-gemma4-e4b-cypher` a `e4b` e `chateau-data-gemma4-31b-cypher-rev6-2000-A-s1234` a `rev6_31b`. Outros nomes recebem erro 400 antes da chamada à orquestração. A interface mostra a mensagem genérica de indisponibilidade quando a API não devolve `SearchResult`; portanto, esse texto não prova falha do servidor do modelo. O teste direto de Edson não valida sozinho o caminho da interface.

## Decisão confirmada com Edson

Às 10:19 de 17/11, após Edson dizer “O mesmo prompt do rev_6 para todos os modelos treinados”, Marcelo propôs: “todo novo modelo cadastrado de agora em diante vai seguir esse formato do rev_6; se o formato mudar, precisaremos criar um novo formato no código”. Edson respondeu “Sim”. No contexto desta conversa, a regra se aplica aos modelos de Cypher treinados. O modelo `e4b` já existente mantém seu formato próprio; o modelo orquestrador de contexto não faz parte desta decisão.

Novos modelos de Cypher treinados deverão usar o contrato `rev6_31b` existente sem de-para individual por nome. O Admin continuará cadastrando nome técnico, URLs e disponibilidade, sem editor de template. Se o formato de um modelo futuro mudar, a integração desse formato será implementada e validada no código antes do uso. A forma exata de distinguir um modelo futuro com novo formato ainda precisará ser definida quando ele existir.

## Implementação local e verificação pendente

Em 17/11, o Expert `8a6ab8e` passou a enviar `rev6_31b` para todo modelo cadastrado na busca Cypher, exceto o nome legado `chateau-gemma4-e4b-cypher`, que continua em `e4b`. O nome técnico e as URLs continuam vindo do cadastro; a orquestração recebe o nome exato selecionado. Os testes de integração da rota de busca passaram (27 casos), incluindo os dois nomes `v2-4000`, um nome futuro e a exceção `e4b`; o build TypeScript do backend também passou. A mudança ainda não foi publicada em produção.

Antes de publicar, remover a URL secundária `https://teste.com` do cadastro de produção: em uma falha recuperável da primeira URL, o failover enviaria a pergunta e o prompt a esse endereço. Após publicação, verificar o prompt e parâmetros da chamada real, o resultado dos dois modelos `v2-4000` na interface e o retorno do Neo4j. A mensagem de erro do cadastro da API ainda diz que o formato é determinado pelo nome técnico; após esta mudança, `rev6_31b` é o padrão e o nome legado é a exceção.
