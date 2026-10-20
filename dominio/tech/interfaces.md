# Interfaces gráficas

## Web atual — implementado

`chateau-expert/web` é Next.js com Google OAuth/NextAuth, middleware de acesso, landing, home, chat, área administrativa, aceite de termos e privacidade. O chat usa as APIs intermediárias `/api/chats` e `/api/search`. O servidor, não o navegador, acrescenta o e-mail da sessão nas chamadas principais. O catálogo `AiModel` aparece no seletor visual, mas a busca atual envia só `{pergunta}`.

## Protótipo novo — referência para o port

`/mnt/c/temp/chateau/ui` é React/Vite, com landing, consentimento, chat, histórico, contexto, filtros, profundidade, resultados e gavetas. A busca usa registros simulados em `src/data.ts`; não chama o backend. Histórico, contexto e consentimento ficam em `localStorage`. `src/features.ts` desativa controles ainda sem comportamento correspondente. Seu login é demonstrativo.

**Decidido em 20/10/2026** ([decisões](../../docs/analises/ui-prototipo-2026-10-20.md#decisões-de-20102026)): os componentes serão portados para `chateau-expert/web` com aparência idêntica ao protótipo, adaptados às versões do projeto (Next.js 14, React 18). O comportamento é o que o Expert já oferece: controle sem funcionalidade real continua sem efeito. Autenticação, autorização, termos, administração, API real e persistência de conversas do Expert continuam sendo contratos a cumprir; o comportamento simulado não os altera. O diretório local é a versão final do protótipo e não será versionado.

**Escopo do port (decidido na [reunião de 20/10/2026](../../docs/reunioes/2026-10-20.md)):** toda a interface do protótipo vai para o web, exceto os desdobramentos de "Buscar candidatos" e "Montar equipe", cujos botões aparecem desabilitados. O que não tem dado ou que o modelo ainda não responde (ex.: aderência) aparece com dado simulado; o que pode ser implementado, como o contexto no PostgreSQL, é implementado mesmo antes de entrar na busca. Sem etapas reais da busca por enquanto. O protótipo não evolui em paralelo: a interface está aprovada, e área de admin e ajustes pontuais são feitos direto no projeto.

Fontes: [web atual](../../chateau-expert/web/src/app/), [análise do protótipo](../../docs/analises/ui-prototipo-2026-10-20.md). O caminho do protótipo é local e não versionado por decisão; se não existir no ambiente, solicitar o código.
