# Administração

**Implementado no Expert, com mudanças decididas em 22/10/2026.** O web reserva `/admin` aos papéis `ADMIN` e `SUPERADMIN`. O menu contém gestão de administradores, autorização de usuários, domínios, modelos de IA e exemplos de busca. **A gestão de termos saiu** junto com o termo de uso ([termos e privacidade](termos-e-privacidade.md)); `ADMIN` precisa da autorização de contexto. A área foi redesenhada com os componentes da nova UI, fica dentro da casca (com abas) e é acessada pela sidebar, em `main` desde 22/10/2026 (`43a25d1`).

- **Usuários:** busca por e-mail e fila `PENDING`; um administrador pode mudar o status entre `PENDING`, `APPROVED` e `DENIED`.
- **Domínios:** cadastro de sufixos de e-mail, normalizados e validados; o domínio cadastrado concede autorização de sessão.
- **Administradores:** criação e promoção concedem `ADMIN` e `APPROVED`; `SUPERADMIN` não pode ser promovido/rebaixado/editado por essas operações. Rebaixar remove `ADMIN`, mas não revoga automaticamente `APPROVED`.
- **Modelos de IA:** o catálogo guarda nome de exibição único, subtítulo, descrição, número de versão, nome técnico, disponibilidade e lista ordenada de URLs dos servidores. Versões diferentes podem compartilhar o nome técnico. O chat mostra apenas cadastros disponíveis; com um só, usa-o automaticamente e oculta o seletor. Sem cadastro disponível, a busca usa dados simulados. O navegador envia o ID e o nome técnico; a API confere o cadastro e obtém as URLs. A URL não vem do navegador. O formato do prompt é determinado pelo nome técnico em código, sem campo de prompt no Admin. Um cadastro disponível exige ao menos uma URL; remover a última exige desmarcar **Disponível**. A migração preserva a URL única anterior como primeira da lista.
- **Edição das URLs:** a lista tem rolagem própria no modal, e os demais controles ficam visíveis. Linhas vazias são ignoradas ao salvar. URLs repetidas após normalização HTTP são recusadas com o aviso “As URLs devem ser diferentes.”
- **Uso das URLs, implementação local de 04/11/2026:** a primeira URL é a tentativa inicial; a orquestração tenta as seguintes apenas nas falhas técnicas definidas no [contrato de busca](../tech/contrato-de-busca.md). Ainda não há distribuição normal de carga nem regra de lentidão. Validação com servidores reais e deploy pendentes.
- **Exemplos:** têm título e descrição.

Histórico das decisões substituídas: [issue #34](../../docs/analises/modelos-admin-2026-10-27.md), [nome técnico compartilhado](../../docs/analises/modelos-admin-2026-10-29.md) e [prompt por cadastro, substituído em 04/11](../../docs/analises/prompt-por-cadastro-2026-11-03.md).

Fontes: [serviços do backend](../../chateau-expert/backend/src/services/), [schema](../../chateau-expert/backend/prisma/schema.prisma), [formulário do Admin](../../chateau-expert/web/src/components/chateau/admin/Modelos.tsx), [chat web](../../chateau-expert/web/src/components/chateau/conversa/Composer.tsx).
