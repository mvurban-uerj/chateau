# Acesso à aplicação atual

**Implementado no Expert.** O termo de uso deu lugar à autorização de contexto (regra vigente desde 22/10/2026, ver [termos e privacidade](termos-e-privacidade.md)), em `main` desde 22/10/2026 (`43a25d1`). Fontes: [NextAuth](../../chateau-expert/web/src/lib/auth.ts), [middleware web](../../chateau-expert/web/src/middleware.ts), [sessão no backend](../../chateau-expert/backend/src/services/auth.service.ts), [barreiras da API](../../chateau-expert/backend/src/middleware/authorizeUser.ts) e [schema Prisma](../../chateau-expert/backend/prisma/schema.prisma).

- Entrada via Google OAuth/NextAuth. No login, o backend cria/atualiza `User` e `Account`, atribui `USER` e registra `LOGIN`.
- `privateAccessStatus` tem `PENDING` (padrão), `APPROVED` e `DENIED`. A sessão considera autorizado quem é `SUPERADMIN`, tem `APPROVED` **ou** usa domínio de e-mail cadastrado em `AuthorizedDomain`. A autorização por domínio **já está implementada**.
- Usuário autenticado em `/` ou `/home` vai para o app (`/chat`). Não autenticado em rota protegida volta para `/`. `/pending`, `/autorizacao` e `/privacidade` estão abertos a qualquer usuário autenticado. Sem autorização de contexto, a rota protegida leva a `/autorizacao?callbackUrl=<rota>`, que só volta para caminhos internos.
- `SUPERADMIN` dispensa a aprovação de acesso, mas também precisa da autorização de contexto (decidido em 22/10/2026). `/admin` exige `ADMIN` ou `SUPERADMIN` (os demais vão para `/chat`); `ADMIN` entra nas demais rotas protegidas sem aprovação individual, com autorização de contexto vigente.
- `USER` sem autorização de acesso vai para `/pending` antes de qualquer outra tela; autorizado, precisa de autorização de contexto vigente para entrar em `/chat` e nas outras rotas protegidas.
- O middleware consulta a sessão atual no backend para rotas protegidas. Se essa consulta falha, usa os valores do JWT; isso é **comportamento atual**, não decisão de política de segurança confirmada.

## Autorização na API

As regras acima valem também na API, não só nas páginas. Só o servidor Next.js chama a API: toda rota `/api/*` exige o token `INTERNAL_API_TOKEN`, que o navegador nunca recebe. O usuário é o da sessão NextAuth, enviado pelo servidor web no cabeçalho `X-User-Email`; **e-mail no corpo ou na query não identifica ninguém**. A API consulta papéis, autorização de acesso e autorização de contexto no PostgreSQL a cada chamada:

| Nível | Exige | Rotas |
|---|---|---|
| Só token | — | login (`sign-in`), dados de sessão, contagem pública de acessos |
| Usuário | conta existente | gravar e revogar a autorização de contexto, visita à home, exportação e exclusão da própria conta (direitos de privacidade independem de aprovação) |
| Usuário autorizado | autorizado, `ADMIN` ou `SUPERADMIN`, sempre com autorização de contexto vigente | busca, conversas, contexto do usuário, opções de filtro, perguntas guiadas, registro de consulta, leitura de exemplos e do catálogo de modelos |
| Administração | `ADMIN` ou `SUPERADMIN`, com autorização de contexto vigente | usuários, domínios, administradores, escrita de exemplos e modelos |

Sem token configurado (mínimo de 32 caracteres) a API não sobe e responde 503. O login demonstrativo da UI Vite não substitui nenhum destes controles. Histórico da correção em [divergências](../../docs/analises/divergencias-2026-10-20.md).
