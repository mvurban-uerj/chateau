# Acesso à aplicação atual

**Implementado no Expert.** Fontes: [NextAuth](../../chateau-expert/web/src/lib/auth.ts), [middleware web](../../chateau-expert/web/src/middleware.ts), [sessão no backend](../../chateau-expert/backend/src/services/auth.service.ts) e [schema Prisma](../../chateau-expert/backend/prisma/schema.prisma).

- Entrada via Google OAuth/NextAuth. No login, o backend cria/atualiza `User` e `Account`, atribui `USER` e registra `LOGIN`.
- `privateAccessStatus` tem `PENDING` (padrão), `APPROVED` e `DENIED`. A sessão considera autorizado quem é `SUPERADMIN`, tem `APPROVED` **ou** usa domínio de e-mail cadastrado em `AuthorizedDomain`. A autorização por domínio **já está implementada**.
- Usuário autenticado em `/` vai para `/home`. Não autenticado em rota protegida volta para `/`. `/home` e `/pending` estão abertos a qualquer usuário autenticado.
- `SUPERADMIN` atravessa os demais controles de rota. `/admin` exige `ADMIN` ou `SUPERADMIN`; `ADMIN` entra nas demais rotas protegidas sem aprovação individual, após aceitar o termo vigente.
- `USER` sem autorização vai para `/pending` antes de qualquer pedido de termo; autorizado, precisa aceitar o termo vigente para entrar em `/chat` e outras rotas protegidas.
- O middleware consulta a sessão atual no backend para rotas protegidas. Se essa consulta falha, usa os valores do JWT; isso é **comportamento atual**, não decisão de política de segurança confirmada.

O backend usa `authorizeUser` nas rotas de busca e conversa, conferindo autorização pelo e-mail recebido. O login demonstrativo da UI Vite não substitui nenhum destes controles. Ver [divergências e risco de autorização na API](../../docs/analises/divergencias-2026-10-20.md).
