# Conversas e busca

**Implementado no web atual.** Uma conversa pertence a um usuário, tem título, mensagens e datas de criação/atualização. O backend lista por atualização recente, busca conversa individual, cria, substitui mensagens, renomeia e exclui, sempre restringindo ao `userId` resolvido. O web guarda mensagens como `{role, content, createdAt}`; respostas estruturadas de busca ficam no `content` com prefixo `__SEARCH__:`.

O envio da pergunta usa `POST /api/search`; a primeira mensagem pode criar a conversa. O resultado aparece como tabela/estado de busca. A atualização das mensagens após a resposta e algumas ações de histórico são disparadas pelo web sem aguardar confirmação; falha de persistência não impede que a conversa apareça na sessão atual.

O status da busca é um entre `ok`, `sem_resultado`, `recusada`, `erro_consulta` e `indisponivel`. Zero linhas ou todas as células vazias, inclusive `count: 0`, viram `sem_resultado`: o produto **não consegue afirmar** se a pergunta está fora do domínio ou se o Cypher não correspondeu à intenção. Uma consulta de escrita recusada e uma falha de banco são estados diferentes. Ver [contrato de busca](../tech/contrato-de-busca.md).

No protótipo da nova UI, níveis de profundidade, perguntas guiadas, filtros, montagem de equipe, porcentagens e justificativas operam sobre dados simulados. Ainda não são contrato do backend nem garantia sobre a busca real.

Fontes: [serviço de conversa](../../chateau-expert/backend/src/services/chat.service.ts), [chat web](../../chateau-expert/web/src/app/chat/page.tsx), [serviço de busca](../../chateau-expert/backend/src/services/search.service.ts), [análise da UI](../../docs/analises/ui-prototipo-2026-10-20.md).
