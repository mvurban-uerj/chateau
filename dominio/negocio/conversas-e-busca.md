# Conversas e busca

**Implementado no web atual.** Uma conversa pertence a um usuário, tem título, mensagens e datas de criação/atualização. O backend lista por atualização recente, busca conversa individual, cria, substitui mensagens, renomeia e exclui, sempre restringindo ao `userId` resolvido. O web guarda mensagens como `{role, content, createdAt}`; respostas estruturadas de busca ficam no `content` com prefixo `__SEARCH__:`.

O envio da pergunta usa `POST /api/search`; a primeira mensagem pode criar a conversa. O resultado aparece como tabela/estado de busca. A atualização das mensagens após a resposta e algumas ações de histórico são disparadas pelo web sem aguardar confirmação; falha de persistência não impede que a conversa apareça na sessão atual.

O status da busca é um entre `ok`, `sem_resultado`, `recusada`, `erro_consulta` e `indisponivel`. Zero linhas ou todas as células vazias, inclusive `count: 0`, viram `sem_resultado`: o produto **não consegue afirmar** se a pergunta está fora do domínio ou se o Cypher não correspondeu à intenção. Uma consulta de escrita recusada e uma falha de banco são estados diferentes. Ver [contrato de busca](../tech/contrato-de-busca.md).

No protótipo da nova UI, níveis de profundidade, perguntas guiadas, filtros, montagem de equipe, porcentagens e justificativas operam sobre dados simulados. **Direção decidida em 20/10/2026:** ranqueamento, aderência, justificativas e equipe virão do modelo de IA consultando o grafo rev_6, pelo caminho web → API → orquestração. O contrato dessa resposta ainda não existe; até lá, o resultado real continua sendo a tabela descrita acima.

**Estado do modelo ([reunião de 20/10/2026](../../docs/reunioes/2026-10-20.md)):** ainda em treino para receber uma pergunta e emitir uma resposta. Não responde aderência e outros campos do protótipo, não recebe o contexto do usuário e não informa etapas durante a busca. No port, esses campos ficam simulados; "Buscar candidatos" e "Montar equipe" ficam desabilitados.

**Decidido em 22/10/2026 (implementado, em `main` desde 22/10/2026 (`43a25d1`)):** o chat livre continua indo ao modelo. Quando as linhas da resposta trazem pessoas, elas viram cartões de perfil. O que veio do grafo aparece normalmente, e cada campo do cartão que não veio do grafo aparece em vermelho, com dado falso. Os outros resultados continuam como tabela. Sem modelo (orquestração não configurada, erro na etapa `modelo` ou sem resposta), a busca devolve profissionais simulados com o aviso "Modelo fora do ar — dados simulados", e a resposta fica marcada como simulada no histórico. Detalhes em [nova UI](../../docs/nova-ui/README.md#chat-livre--cartões-decidido-em-22102026).

Fontes: [serviço de conversa](../../chateau-expert/backend/src/services/chat.service.ts), [chat web](../../chateau-expert/web/src/app/chat/page.tsx), [serviço de busca](../../chateau-expert/backend/src/services/search.service.ts), [análise da UI](../../docs/analises/ui-prototipo-2026-10-20.md).
