# Administração

**Implementado no Expert, com mudanças decididas em 22/10/2026.** O web reserva `/admin` aos papéis `ADMIN` e `SUPERADMIN`. O menu contém gestão de administradores, autorização de usuários, domínios, modelos de IA e exemplos de busca. **A gestão de termos saiu** junto com o termo de uso ([termos e privacidade](termos-e-privacidade.md)); `ADMIN` precisa da autorização de contexto. A área foi redesenhada com os componentes da nova UI, fica dentro da casca (com abas) e é acessada pela sidebar, em `main` desde 22/10/2026 (`43a25d1`).

- **Usuários:** busca por e-mail e fila `PENDING`; um administrador pode mudar o status entre `PENDING`, `APPROVED` e `DENIED`.
- **Domínios:** cadastro de sufixos de e-mail, normalizados e validados; o domínio cadastrado concede autorização de sessão.
- **Administradores:** criação e promoção concedem `ADMIN` e `APPROVED`; `SUPERADMIN` não pode ser promovido/rebaixado/editado por essas operações. Rebaixar remove `ADMIN`, mas não revoga automaticamente `APPROVED`.
- **Modelos de IA:** catálogo com nome único, descrição e número de versão. A escolha visual de modelo no chat atual não é enviada em `POST /api/search`; não presumir que altera o modelo de orquestração.
- **Exemplos:** têm título e descrição.

Fontes: [middleware](../../chateau-expert/web/src/middleware.ts), [serviços do backend](../../chateau-expert/backend/src/services/), [schema](../../chateau-expert/backend/prisma/schema.prisma), [chat web](../../chateau-expert/web/src/app/chat/page.tsx).
