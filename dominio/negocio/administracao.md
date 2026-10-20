# Administração

**Implementado no Expert.** O web reserva `/admin` aos papéis `ADMIN` e `SUPERADMIN` (e exige aceite do termo para `ADMIN`). O menu contém gestão de administradores, autorização de usuários, domínios, modelos de IA, exemplos de busca e termos.

- **Usuários:** busca por e-mail e fila `PENDING`; um administrador pode mudar o status entre `PENDING`, `APPROVED` e `DENIED`.
- **Domínios:** cadastro de sufixos de e-mail, normalizados e validados; o domínio cadastrado concede autorização de sessão.
- **Administradores:** criação e promoção concedem `ADMIN` e `APPROVED`; `SUPERADMIN` não pode ser promovido/rebaixado/editado por essas operações. Rebaixar remove `ADMIN`, mas não revoga automaticamente `APPROVED`.
- **Modelos de IA:** catálogo com nome único, descrição e número de versão. A escolha visual de modelo no chat atual não é enviada em `POST /api/search`; não presumir que altera o modelo de orquestração.
- **Exemplos e termos:** exemplos têm título/descrição. O termo novo torna-se o mais recente por data de criação e exige aceite atualizado.

Fontes: [middleware](../../chateau-expert/web/src/middleware.ts), [serviços do backend](../../chateau-expert/backend/src/services/), [schema](../../chateau-expert/backend/prisma/schema.prisma), [chat web](../../chateau-expert/web/src/app/chat/page.tsx).
