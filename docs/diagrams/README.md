# Diagramas

Diagramas editáveis em formato `.drawio` para abrir no [app.diagrams.net](https://app.diagrams.net).

## [chateau-web-api-map.drawio](chateau-web-api-map.drawio)

Mapa das chamadas entre navegador, servidor Next.js, API Express, orquestração e bancos, atualizado em 27/10/2026 contra `chateau-expert` `dc77c53`. As caixas agrupam endpoints por fluxo; para métodos e validações exatos, confira os Route Handlers, Server Actions e routers do Expert.

- **Acesso:** Google/NextAuth → API de autenticação; o middleware consulta a sessão e verifica aprovação e autorização de contexto.
- **Segurança web → API:** o servidor Next.js envia `INTERNAL_API_TOKEN` e, nas chamadas de usuário, `X-User-Email`. O navegador não recebe o token interno.
- **Busca:** `/chat` e `/chat/[id]` chamam `POST /api/search` via Route Handler web. Na evolução local da issue #34, o backend usa a orquestração quando há modelo disponível selecionado; sem modelo ou em falha dele, devolve resposta simulada e marcada. `ORCHESTRATION_URL` só substitui o endereço interno do serviço. A orquestração pede ao modelo de IA que gere Cypher e lê o Neo4j. Web e backend não acessam o Neo4j diretamente.
- **Persistência:** PostgreSQL guarda contas, autorização, Meu contexto, perguntas guiadas, conversas e administração. O `schema_producao.txt` é uma fotografia versionada para o modelo, não uma leitura automática do grafo.
- **Outras áreas:** administração usa Server Actions; privacidade usa Route Handlers para exportação e exclusão.

O diagrama de 01/09/2026 foi substituído porque mostrava busca simulada no navegador, endpoint `/api/chat/query` ainda planejado e o termo de uso removido depois. O histórico continua no Git.
