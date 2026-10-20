# Dúvidas para o Edson

Lista viva de perguntas abertas. Ao receber a resposta, anotar a data e o desfecho embaixo da pergunta, mover a regra confirmada para [dominio/](../../dominio/indice.md) e marcar a tarefa no [todo](../todo.md). Contexto da nova UI: [decisões](../analises/ui-prototipo-2026-10-20.md#decisões-de-20102026) e [Figma](../analises/figma-2026-10-20.md).

## Nova UI — consentimento e termos

1. **O que é a tela "Antes de começar, o que podemos usar?"** Ela pede escolha por campo: Nome e Unidade/vínculo obrigatórios; e-mail institucional, campus e cookies opcionais; revogável em Meu contexto. Visão do Marcelo: é uma ampliação da permissão de cookies, **diferente do termo de uso** (documento com que o usuário declara estar de acordo). Confirma?
2. **O que cada escolha controla de fato?** Os campos se referem aos dados do próprio usuário, à exibição dos dados das pessoas do grafo, ou aos dois? O que muda na busca ou na tela quando a pessoa recusa e-mail ou campus?
3. **Onde entra o termo de uso na nova UI?** O protótipo não tem tela de termo: o interruptor `termosPrivacidade` está desligado ("não há texto nem destino"). Hoje o Expert exige o aceite do termo vigente antes do chat (`/terms`) e tem `/termos-uso` e `/privacidade`. Ordem esperada: login → termo → consentimento → app?
4. As escolhas de consentimento serão guardadas no PostgreSQL (decisão de 20/10). Tem alguma restrição ou modelo que você imaginou para isso?

## Nova UI — busca

5. **Etapas da busca:** decidimos implementar o fluxo por etapas porque o modelo está sendo treinado para ele. Quais são as etapas que o modelo executa, com que nomes, e como ele informa o andamento (resposta parcial, streaming, eventos)?
6. **Parar e Retomar:** o modelo aceita interromper uma busca no meio? Retomar continua de onde parou ou recomeça?
7. **Formato da resposta:** como o modelo devolverá lista ranqueada, aderência (%), justificativa, caminho no grafo ("Por que este perfil"), cobertura (no escopo / com currículo / que atendem) e montagem de equipe?
8. **Níveis de busca** (Básico, Padrão, Avançado, Pro, Expert): existem no modelo? Quais nomes ficam na interface (o Figma diz que os nomes atuais são técnicos e dependem de decisão)?
9. **Busca recusada:** quando a pergunta gera uma consulta que altera dados (ex.: "Apague todos os pesquisadores"), o Expert bloqueia e mostra "consulta recusada". O desenho não tem essa tela. Usamos o mesmo aviso de erro do serviço com outro texto, ou você prefere desenhar?
10. Filtros e "Instruções" do contexto: o modelo vai receber as tags e filtros como texto da pergunta ou em campos separados? A combinação por OU prevista no grafo de UX entra?

10a. **Origem das opções dos questionários** (Buscar candidatos e Montar equipe): no protótipo estão fixas em `src/flows/` e o Figma não fala em base ou administração. Proposta: linhas de pesquisa vêm do grafo (`LineOfResearch` real no Neo4j); vínculo, tipos de produção, disponibilidade, obrigatoriedade, tipo de projeto e tamanho do time ficam fixos, ligados ao modelo rev_6. Concorda, ou alguma lista deve ser administrável?
10b. **Regras de ranqueamento e de equipe:** no protótipo, `runSearch` aplica "obrigatório elimina, desejável pesa" (área +8, produção +5, disponibilidade +3, tipo de projeto +5, objetivo +4) e monta a equipe com uma vaga por linha de pesquisa e até 2 reservas. Essas regras passam a ser do modelo, ou o nosso sistema aplica sobre o que o modelo devolve?

## Nova UI — desenho e código

11. A cópia que recebemos (`/mnt/c/temp/chateau/ui`, sem Git) corresponde ao commit `3cf7be7` que o Figma espelha, ou é posterior?
12. **Administração:** como o administrador chega ao `/admin` na nova sidebar, e as telas de admin seguem o mesmo visual?
13. **Tema escuro:** o desenho só tem tema claro e o web atual tem escuro. Pode sair?
14. Anel de foco nos botões grafite (em aberto no Figma): já decidiu?
15. Programa de pós como filtro depende de ligar pessoa, linha e programa no grafo: entra agora ou depois?
16. Acesso ao Figma original: pode dar acesso de leitura a `mvurban@mvurban.eti.br`? A cópia nos rascunhos não acompanha suas mudanças.

## Nova UI — versões do protótipo × projeto

Decisão de 20/10: prevalecem a infraestrutura e as versões do projeto; o protótipo é adaptado ao `chateau-expert/web`. Comparação dos `package.json` (protótipo em `/mnt/c/temp/chateau/ui`, web em `chateau-expert/web`):

| Item | Protótipo | Projeto (web) | No port |
|---|---|---|---|
| Framework | Vite 8 (SPA) | Next.js 14.2 (App Router, NextAuth 4) | Componentes entram em rotas do Next; Vite sai |
| React / React DOM | 19.2 | 18.3.1 | Fica 18; o protótipo não usa APIs exclusivas do 19 (verificado) |
| TypeScript | 6.0 | 5 | Fica 5 |
| Tailwind CSS | 4.3 via `@tailwindcss/vite` | 4.2 via `@tailwindcss/postcss` | Mesma geração; tokens do `@theme` passam para o CSS do web |
| Animação | `motion` 13.1 | — | Entra como dependência (aceita React 18) |
| Ícones | Phosphor 2.1 | `lucide-react` 0.575 | Phosphor entra; lucide continua nas telas não portadas (admin) |
| Componentes base | `@radix-ui/react-slider` 1.4 | shadcn/ui + vários `@radix-ui/*` | Slider entra; demais Radix já existem |
| Fonte | Geist / Geist Mono via `@fontsource-variable` | fontes do Next | Definir se usa `@fontsource` ou `next/font` |
| Tema | só claro | `next-themes` (claro/escuro) | Tema claro único (ver dúvida 13) |
| Lint | oxlint | ESLint 9 | Fica ESLint |
| Tipos Node / runtime | `@types/node` 24 | `@types/node` 20, imagens `node:20` | Fica Node 20 |

17. Alguma dessas adaptações quebra algo que você considera essencial no protótipo (por exemplo, comportamento do `motion` ou das fontes)?
18. O protótipo deve continuar evoluindo em paralelo em React 19? Se sim, como sincronizamos as mudanças com o port em React 18?

## Dados e modelo

19. **Origem dos campos novos da rev_6** exibidos na UI: cargo e vínculo (`Job`, `Role`, `WORKS`), unidade e campus, disciplinas (`TAUGHT`), prêmios (`Acknowledgment`), coordenação (`COORDINATES`). De que fonte cada um sai?
20. **Disponibilidade** (`Availability.enable`) é do grafo de UX: quem informa, o próprio pesquisador?
21. Datas e identificadores gravados como texto (`datePublished: "2021"`) × `DATE`/`INTEGER` no modelo (pendente desde setembro).
22. Versão 2.0 do orquestrador (Tarefa 1): previsão?
