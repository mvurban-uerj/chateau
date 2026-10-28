# Interfaces gráficas

## Web — implementado

**Nova UI em `main` desde 22/10/2026 (`43a25d1`).** `chateau-expert/web` é Next.js 14 (App Router, React 18) com a interface do protótipo portada com aparência idêntica ([decisões](../../docs/analises/ui-prototipo-2026-10-20.md#decisões-de-20102026), [plano e fases](../../docs/nova-ui/plano.md)):

- **Telas:** entrada (Google/NextAuth), acesso pendente e restrito, autorização de contexto, chat (`/chat` e `/chat/[id]`) com histórico na sidebar, cartões de resultado, gavetas de perfil e comparação, Meu contexto, administração (`/admin/*`, dentro da casca) e privacidade.
- **Textos:** todos os textos fixos de tela, inclusive os exemplos do catálogo de componentes, ficam em `web/messages/pt-BR.json` (next-intl, idioma fixo pt-BR, sem rota por idioma); o lint proíbe texto solto em JSX e atributos visíveis. Nomes próprios, valores do grafo e conteúdo simulado que representa dados não são rótulos de interface.
- **Componentes:** primitivos próprios com os nomes do Figma (`web/src/components/chateau/primitivos`), tema único claro, ícones Phosphor, animações `motion` com movimento reduzido respeitado. Não há mais shadcn, lucide nem `next-themes`.
- **Dados:** o servidor web chama a API com o token interno e o e-mail da sessão ([acesso](../negocio/acesso.md#autorização-na-api)); conversas, contexto, autorização e perguntas guiadas vêm do PostgreSQL pela API. Valores e opções simulados aparecem em vermelho, inclusive uma resposta inteira de mock e as opções de filtro ([conversas e busca](../negocio/conversas-e-busca.md)).
- **Recursos ainda parciais**, controlados em `web/src/lib/chateau/features.ts`: "Buscar candidatos" e "Montar equipe" desabilitados; o seletor de profundidade mostra níveis do catálogo do admin em vermelho, mas a escolha ainda não altera a busca; Parar avisa "em desenvolvimento"; upload de edital, documentos e ações secundárias ocultos.

O catálogo `AiModel` fornece nome, subtítulo, descrição e ordem dos níveis ao seletor. A busca envia só a pergunta.

## Protótipo — referência

`/mnt/c/temp/chateau/ui` (React/Vite, dados simulados, não versionado por decisão) é a versão final do protótipo e serviu de referência para o port. Não evolui em paralelo: ajustes de interface são feitos direto no `chateau-expert/web`. Se o diretório não existir no ambiente, solicitar o código.

Em 26/10/2026, uma cópia estática foi publicada por engano no Sites. Após o esclarecimento de que o pedido era para abrir o protótipo no localhost, o endereço privado <https://chateau-prototipo-uerj.merryflea11.chatgpt.site> foi substituído por uma página de encerramento. O protótipo de trabalho permanece no diretório local acima e pode ser executado com Vite na porta 5179.

Fontes: [web](../../chateau-expert/web/src/app/), [plano do port](../../docs/nova-ui/plano.md).
