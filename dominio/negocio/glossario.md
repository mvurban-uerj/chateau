# Glossário curto

| Termo | Significado neste projeto |
|---|---|
| Especialista / perfil | Pessoa representada no grafo acadêmico, candidata a uma busca; a cobertura depende das fontes carregadas. |
| Grafo acadêmico | Modelo Arrows/Neo4j de pessoas, vínculo, produção, pesquisa, ensino e estrutura institucional. [Modelo](../modelo/grafo-academico.md). |
| Contexto do usuário | Perfil, objetivo, interesses e outros itens definidos no grafo de UX; implementação do protótipo é parcial. [Contexto de UX](../modelo/contexto-ux.md). |
| Consulta | Pergunta em linguagem natural que a orquestração traduz para Cypher e tenta executar no Neo4j. |
| Conversa / chat | Título e mensagens de um usuário, persistidos no PostgreSQL pelo Expert atual. |
| Autorização de contexto | Escolhas da pessoa sobre quais dados seus o Chateau usa (nome e unidade obrigatórios; e-mail, campus e cookies opcionais), no PostgreSQL e revogável. Substitui o termo de uso, que deixou de existir. [Termos e privacidade](termos-e-privacidade.md). |
| Domínio autorizado | Sufixo de e-mail cadastrado para liberar acesso a usuários daquele domínio. |
| Modelo acadêmico | JSON do Arrows que define nós, propriedades e arestas; `rev_6_training` é o padrão atual do pipeline. |
| Modelo de IA | Registro administrativo `AiModel` no PostgreSQL **ou** modelo texto→Cypher usado na orquestração. São objetos distintos. Na comunicação de produto, é o modelo que recebe a pergunta e gera Cypher. |
| Servidor do modelo de IA | Serviço externo à orquestração, tratado como caixa preta no fluxo do produto: recebe uma solicitação com pergunta e esquema do grafo e devolve uma resposta da qual se extrai o Cypher. A URL cadastrada no Admin aponta para esse servidor; ela não é o endereço do Quarkus nem identifica sozinha o modelo. Seu processamento interno e sua tecnologia não são pressupostos pelo fluxo. |

Fontes: [schema Prisma](../../chateau-expert/backend/prisma/schema.prisma), [modelo Arrows](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json), [modelo de UX](../../chateau-data/model/diagramas/Chateau-UX.json).
