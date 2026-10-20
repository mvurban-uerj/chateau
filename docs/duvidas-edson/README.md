# Dúvidas para o Edson

Respondidas na [reunião de 20/10](../reunioes/2026-10-20.md), que também registra o estado do modelo e a direção do port. Só as dúvidas principais, em escopo amplo; os detalhes saem das respostas. Ao responder, anotar data e desfecho embaixo da pergunta e levar a regra confirmada para [dominio/](../../dominio/indice.md).

## 1. Consentimento × termo de uso

A tela "Antes de começar, o que podemos usar?" pede escolhas por campo (nome, unidade e vínculo, e-mail, campus, cookies). No meu entendimento ela amplia a permissão de cookies e é diferente do termo de uso, que é o documento com que o usuário declara estar de acordo. Não encontrei o termo de uso navegando no protótipo. Como as duas coisas ficam na nova interface, e o que cada escolha da tela controla?

Resposta (20/10): remover o termo de uso e criar uma autorização de contexto para nome unidade, email campus etc, junto com os cookies.

## 2. Como a interface conversa com o modelo

Pelo que entendi, a busca tem duas portas e um só mecanismo: a pergunta guiada (cards "Buscar candidatos" e "Montar equipe", com opções para marcar) ou o chat, onde a pessoa escreve. Nos dois casos o sistema monta a pergunta, que vai para o orquestrador, que consulta o modelo, que devolve a resposta final. Está certo?

Enquanto a busca roda, o desenho mostra etapas nomeadas com contador e botão Parar ("Lendo 11 perfis no escopo", "Casando nome e área", "Escrevendo as justificativas"...). No protótipo elas avançam por tempo; para refletirem o progresso real, o modelo ou o orquestrador precisa avisar a interface em que etapa está. O modelo vai informar essas etapas durante a busca? Como?

O "Meu contexto" (objetivo, interesses e instruções) também muda a busca: no protótipo essas configurações valem como filtro em toda busca? Como essas informações entram como parâmetro para o modelo, junto com a pergunta e as respostas do questionário?

Resposta (20/10): não vamos fazer agora. Os botões "Buscar candidatos" e "Montar equipe" vão existir, mas desabilitados.

## 3. Origem dos dados
De onde devem vir as opções que a interface mostra?
1- Perguntas guiadas (cards "Buscar candidatos" e "Montar equipe")
a- fixas no código 
b- vem automaticamente pelo grafo
c- vem do backend com admin por trás

Os demais itens, mesma dúvida: Filtros e interesses, instruções (na engrenagem do perfil)

Resposta (20/10): no campo de pesquisa tem um texto que é montado aos poucos com tab no final; esse tab abre um modal com várias perguntas. Essas perguntas vamos ter que gerar lendo o modelo v6 e incluir no Postgres.
- O modelo v6 é o grafo `Expert-Finding-in-academia_rev_6_training.json`.
- As perguntas são geradas só uma vez (carga).
- Filtros, interesses e instruções: os dados ficam no Postgres e são relacionados ao usuário do site (conta Google).
- As opções de filtro vêm do Cypher (grafo). A avaliar: o Next consulta o Cypher direto ou lê do Postgres, com um cron noturno que compara o Cypher com o Postgres e grava a diferença?
- No "Meu contexto", a disponibilidade tem como padrão "disponível".

## 4. Versões do protótipo × projeto

O protótipo está em React 19 / Vite e o projeto em Next.js 14 / React 18; vamos adaptar o protótipo às versões do projeto. O protótipo roda sozinho no navegador e pode usar sempre a versão mais nova; o projeto prefere versões estáveis e compatíveis entre si, porque convive com peças que o protótipo não tem. Exemplos:

- **Next.js 14 e React 18:** React 19 só entra com Next.js 15, e essa troca mexe no login (NextAuth), no middleware de acesso e nas rotas do servidor que hoje protegem a API.
- **Telas que o protótipo não tem:** administração, termos de uso e privacidade usam componentes shadcn/Radix e ícones lucide já testados com React 18.
- **Backend e infraestrutura:** API em Express com Prisma e TypeScript 5, imagens Docker em Node 20 e deploy automático com testes; TypeScript 6 e Vite 8 trariam outra base de ferramentas para manter.

O protótipo vai continuar evoluindo em paralelo? Se sim, como mantemos os dois iguais?

Resposta (20/10): o protótipo não vai evoluir em paralelo. Deverá vir a área de admin ou algum ajuste pontual, mas é uma interface já aprovada; se houver mudança, será pontual e feita direto no projeto. Só evolui para frente, sem manter os dois em paralelo.

| Item | Protótipo | Projeto (web) |
|---|---|---|
| Framework | Vite 8 (SPA) | Next.js 14.2 + NextAuth 4 |
| React | 19.2 | 18.3 |
| TypeScript | 6.0 | 5 |
| Ícones | Phosphor | lucide |

