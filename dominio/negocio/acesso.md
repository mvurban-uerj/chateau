# Acesso à aplicação atual

**Implementado no Expert, exceto a troca do termo pela autorização de contexto** (regra vigente desde 22/10/2026, ver [termos e privacidade](termos-e-privacidade.md); o código ainda checa o termo). Fontes: [NextAuth](../../chateau-expert/web/src/lib/auth.ts), [middleware web](../../chateau-expert/web/src/middleware.ts), [sessão no backend](../../chateau-expert/backend/src/services/auth.service.ts), [barreiras da API](../../chateau-expert/backend/src/middleware/authorizeUser.ts) e [schema Prisma](../../chateau-expert/backend/prisma/schema.prisma).

- Entrada via Google OAuth/NextAuth. No login, o backend cria/atualiza `User` e `Account`, atribui `USER` e registra `LOGIN`.
- `privateAccessStatus` tem `PENDING` (padrão), `APPROVED` e `DENIED`. A sessão considera autorizado quem é `SUPERADMIN`, tem `APPROVED` **ou** usa domínio de e-mail cadastrado em `AuthorizedDomain`. A autorização por domínio **já está implementada**.
- Usuário autenticado em `/` vai para o app (`/chat`; hoje `/home`). Não autenticado em rota protegida volta para `/`. `/pending` e a tela de autorização estão abertos a qualquer usuário autenticado.
- `SUPERADMIN` atravessa os demais controles de rota. `/admin` exige `ADMIN` ou `SUPERADMIN`; `ADMIN` entra nas demais rotas protegidas sem aprovação individual, com autorização de contexto vigente.
- `USER` sem autorização de acesso vai para `/pending` antes de qualquer outra tela; autorizado, precisa de autorização de contexto vigente para entrar em `/chat` e nas outras rotas protegidas.
- O middleware consulta a sessão atual no backend para rotas protegidas. Se essa consulta falha, usa os valores do JWT; isso é **comportamento atual**, não decisão de política de segurança confirmada.

## Autorização na API

As regras acima valem também na API, não só nas páginas. Só o servidor Next.js chama a API: toda rota `/api/*` exige o token `INTERNAL_API_TOKEN`, que o navegador nunca recebe. O usuário é o da sessão NextAuth, enviado pelo servidor web no cabeçalho `X-User-Email`; **e-mail no corpo ou na query não identifica ninguém**. A API consulta papéis, autorização de acesso e autorização de contexto no PostgreSQL a cada chamada (o código atual ainda consulta o termo):

| Nível | Exige | Rotas |
|---|---|---|
| Só token | — | login (`sign-in`), dados de sessão, contagem pública de acessos |
| Usuário | conta existente | gravar e revogar a autorização de contexto, visita à home, exportação e exclusão da própria conta (direitos de privacidade independem de aprovação) |
| Usuário autorizado | `SUPERADMIN`; ou autorizado/`ADMIN` com autorização de contexto vigente | busca, conversas, contexto do usuário, opções de filtro, perguntas guiadas, registro de consulta, leitura de exemplos e do catálogo de modelos |
| Administração | `SUPERADMIN`; ou `ADMIN` com autorização de contexto vigente | usuários, domínios, administradores, escrita de exemplos e modelos |

Sem token configurado (mínimo de 32 caracteres) a API não sobe e responde 503. O login demonstrativo da UI Vite não substitui nenhum destes controles. Histórico da correção em [divergências](../../docs/analises/divergencias-2026-10-20.md).
