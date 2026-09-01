# Diagrams

Diagramas do projeto em formato `.drawio` (mxGraph), editáveis em [app.diagrams.net](https://app.diagrams.net).

## `chateau-web-api-map.drawio`

Mapa de todas as chamadas que o `chateau-expert/web` faz à API (`chateau-expert/backend`), levantado direto do código-fonte em 2026-09-01.

**Faixa do topo — coração do sistema (planejado):** o pipeline real de busca de especialistas, hoje inexistente, todo agrupado numa linha só, ligado ponta a ponta: `mock atual (app/chat/page.tsx)` → `POST /api/chat/query` (endpoint a criar em `chat.router.ts`) → `API de Orquestração (LangChain)` (a criar em `chateau-expert/orchestration/`) → `Modelo de IA / LLM`. Fica em vermelho (estado atual) + laranja tracejado (planejado), separado do resto pra deixar claro que é o que falta construir.

Abaixo dela, o mapa do que **já está implementado**, em 3 colunas:

1. **Origem (UI)** — páginas e componentes que disparam a chamada.
2. **Camada de Serviço (Web)** — Server Actions (`actions.ts`), Route Handlers internos (`app/api/*/route.ts`) e callbacks do NextAuth (`lib/auth.ts`).
3. **Backend API (Express)** — cada router de `chateau-expert/backend/src/routes` vira um box **UML `«Interface»`** (modelo sugerido pelo coordenador): nome da API (`terms-API`, `chats-API`, `admins-API`...), compartimento de **campos** (a entidade que a API manipula) e compartimento de **métodos** (assinatura + comentário com o endpoint HTTP real, ex. `getLatestTerm(): Term // GET /latest`). A `search-API` planejada (`chateau-orchestration`) segue o mesmo formato, em laranja tracejado.

Cores: cinza = origem na UI · verde = Server Action · azul = Route Handler Next.js · roxo = callback NextAuth · box branco `«Interface»` = API implementada no backend · vermelho = mock atual (`app/chat/page.tsx`, `mockResponse()`) · laranja tracejado = API/fluxo planejado, ainda não existe.

**Achado principal:** a busca de profissionais (função central do produto) é 100% mockada no frontend — não existe endpoint de busca no backend. Todos os outros ~33 endpoints (termos, chats, admins, domínios, modelos de IA, exemplos de busca, privacidade, usuários) já estão implementados de ponta a ponta.

Para editar: abra [app.diagrams.net](https://app.diagrams.net) → Arquivo → Abrir de → Dispositivo → selecione o arquivo.
