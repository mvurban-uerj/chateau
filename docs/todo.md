# TODO — frentes de trabalho

Tarefas e agenda do projeto. As frentes andam em paralelo; cada uma lista o que falta, de quem depende e onde está o detalhe. Ao concluir uma tarefa, marcar `[x]` com a data; ao descobrir trabalho novo, incluir na frente certa. Decisões vão para `docs/analises/` ou `docs/reunioes/` e regras confirmadas para [dominio/](../dominio/indice.md).

Legenda: **(dep: X)** = depende de outra tarefa ou pessoa.

## Agenda

| Data | O quê | Frente |
|---|---|---|
| 20/10 | ~~Edson deve mandar o Figma da identidade visual~~ recebido e lido ([análise](analises/figma-2026-10-20.md)) | Identidade visual |
| — | Teste do modelo com GPU previsto para 30/09–02/10: resultado não registrado aqui; confirmar se aconteceu | IA e orquestração |

## 1. Nova UI — port do protótipo

Decisões de 20/10/2026: [análise da UI](analises/ui-prototipo-2026-10-20.md#decisões-de-20102026). Aparência idêntica ao protótipo (`/mnt/c/temp/chateau/ui`, versão final, não versionada); infraestrutura e versões do Expert prevalecem (Next.js 14, React 18). **Nada de código antes de fechar o levantamento abaixo.**

Levantamento (antes de programar). O Figma é espelho do protótipo e a página 08 Handoff já traz mapa de arquivos, contrato com o grafo e interruptores: ver [análise do Figma](analises/figma-2026-10-20.md).

- [ ] Confirmar com o Edson que a cópia em `/mnt/c/temp/chateau/ui` corresponde ao commit `3cf7be7` (ou posterior) do repositório local dele, que o Figma espelha.
- [ ] **Consentimento × termo de uso:** visão atual: são coisas diferentes; a tela é ampliação da permissão de cookies e as escolhas vão para o PostgreSQL (hoje só existe o aceite de termo). **(dep: Edson, [dúvida 1](duvidas-edson/README.md))**
- [ ] **Busca por etapas, Parar e Retomar:** decidido implementar (o modelo é treinado para esse fluxo). Definir com o Edson etapas, formato do andamento e cancelamento; depois, adaptar API e web (hoje é requisição única). **(dep: Edson, [dúvida 2](duvidas-edson/README.md))**
- [ ] Níveis de busca: nomes e existência no modelo. **(dep: resposta da [dúvida 2](duvidas-edson/README.md))**
- [ ] Ajustar nosso código (decidido): acesso à administração pela nova sidebar; tema único claro; histórico com Desfazer por 6 s (exclusão adiada) e rota por conversa para voltar/avançar do navegador.
- [ ] Inventário tela a tela e componente a componente do protótipo → rota/componente correspondente no `chateau-expert/web`, indicando o que é visual puro e o que depende de dado ou de backend.
- [ ] Compatibilidade técnica ([versões](duvidas-edson/README.md#4-versões-do-protótipo--projeto)): dependências do protótipo (`motion` 13, `@phosphor-icons/react`, `@radix-ui/react-slider`, fontes Geist) aceitam React 18 e o código não usa APIs exclusivas do React 19 (verificado em 20/10). Falta: conferir Tailwind 4 do protótipo × configuração do web (tokens, `index.css`), coexistência com shadcn/lucide já usados no web, e o aviso de bundle > 500 kB.
- [ ] Campo a campo: cada dado exibido (cartão, gaveta de perfil, comparação, cobertura, equipe) → nó/propriedade/aresta da **rev_6** (o código do protótipo cita rev_5). Marcar o que existe no modelo e o que não existe. **(dep: frente 2 para saber o que estará carregado)**
- [ ] Mapear fluxos do protótipo para os contratos do Expert:
  - login demonstrativo → Google/NextAuth; `/pending` e regras de [acesso](../dominio/negocio/acesso.md);
  - tela de consentimento → aceite de termo no PostgreSQL (decidido);
  - histórico em `localStorage` → `/api/chats` (formato `__SEARCH__:` precisa acomodar o novo resultado);
  - contexto do usuário → continua em `localStorage` (decidido);
  - links de termos/privacidade → páginas existentes (`/termos-uso`, `/privacidade`);
  - área administrativa: não existe no protótipo; definir como fica visualmente.
- [ ] Listar controles que ficam visíveis sem efeito (ex.: seletor de modelo, níveis de profundidade até haver suporte) e os que o `features.ts` já esconde.
- [ ] Estados vazios, erro, recusa e indisponibilidade: mapear os 5 status atuais da busca para telas do protótipo (`recusada` não tem tela no desenho; definir no nosso código).
- [ ] Port responsivo: o desenho tem telas de celular (390 px).

Depois do levantamento:

- [ ] Plano de port por etapas (o que entra primeiro com dados reais, o que fica escondido). **(dep: levantamento completo)**
- [ ] Port dos componentes, mantendo a interface atual até cada fluxo integrado estar validado.

## 2. Dados — `chateau-data` (rev_6)

- [ ] **(Marcelo)** Gerar o Cypher completo no modelo `rev_6_training` e carregar no Neo4j de produção (hoje o grafo é da carga anterior: sem `Job`, `Role`, `WORKS`, `TAUGHT`, `COORDINATES`, `Campus`, `Acknowledgment`). Definir a estratégia de carga (substituir × incrementar; identificadores sequenciais não são estáveis entre execuções). Ver [Neo4j](neo4j/README.md) e a issue citada na [reunião de 23/09](reunioes/2026-09-23.md).
- [ ] Corrigir o extrator de produções do PDF Sucupira (teste falha em 20 PDFs) e repetir o teste. Ver [fontes e pipeline](../dominio/dados/fontes-e-pipeline.md).
- [ ] Fontes para os campos novos da UI (cargo/vínculo, unidade, campus, disciplinas, prêmios, coordenação): identificar de onde cada um é extraído. **(dep: levantamento campo a campo da frente 1)**
- [ ] Atividade 16: baixar dados do S-Ticket da Cotplan (Marcelo e Geraldo) para o grafo rev_6 (reunião de 19/10).
- [ ] Verificar no Sucupira novas formas de baixar dados (reunião de 19/10).
- [ ] Decidir datas da oferta de `ShortCourseInstance` no extrator Lattes (pendência da investigação rev_5; conferir se ainda vale na rev_6).

## 3. IA e orquestração

- [ ] Levar ao Edson a lista de [dúvidas](duvidas-edson/README.md) e registrar as respostas.
- [ ] Definir com o Edson o **contrato de resposta do modelo** para a nova UI: lista de perfis, aderência, justificativa, caminho no grafo, cobertura e montagem de equipe; como isso chega pelo caminho web → API → orquestração. **(dep: levantamento campo a campo da frente 1)**
- [ ] Depois da carga rev_6: extrair de novo `schema_producao.txt` e atualizar o schema usado pelo modelo. **(dep: frente 2, carga rev_6)**
- [ ] Datas e identificadores gravados como texto (`datePublished: "2021"`) × `DATE`/`INTEGER` no modelo: pendente com o Edson.
- [ ] Tarefa 1: versão 2.0 do orquestrador — aguardando o Edson.
- [ ] Teste do modelo real com GPU e ligação da busca real: confirmar se aconteceu e registrar o resultado. Roteiro detalhado abaixo.

### Roteiro do teste com GPU (planejado para 30/09–02/10)

Detalhes e justificativas: `docs/integracao-modelo/README.md`, Fase 5.

Antes:

- [ ] Combinar com o Edson o **horário** e **quem sobe o túnel** da máquina com
      GPU. O Ollama precisa aparecer no servidor em `127.0.0.1:11434`.
- [ ] Ter à mão a **senha do SSH** do `prointec@152.92.2.63`.
- [ ] Docker Desktop rodando na máquina local.
- [ ] (Opcional) Acrescentar perguntas em
      `chateau-expert/orchestration/teste_modelo/perguntas.txt` (uma por linha).

Com o túnel de pé:

1. [ ] Rodar o teste (pede só a senha do SSH; leva alguns minutos):
   ```bash
   bash ~/projetos/uerj/chateau/chateau-expert/orchestration/teste_modelo/testar_modelo.sh
   ```
   - Se parar em **"Ollama NÃO responde"**, o túnel não está de pé: falar com
     o Edson.
   - Se perguntar **"Aplicar a ponte agora no servidor?"**, responder `SIM`
     (cria o container `chateau_ollama_ponte`, sem sudo). **Anotar o
     `OLLAMA_URL` que ele indicar** no fim da etapa 3.
2. [ ] Colar o conteúdo de
   `orchestration/teste_modelo/resultados/<data>/resumo.md` no
   `docs/talk-ia.md` e pedir a análise. O resumo traz:
   - versão do Ollama e se o modelo está carregado;
   - acesso container → Ollama e o `OLLAMA_URL` a usar;
   - as 14 perguntas reais (bananas, pergunta com ano, recusa do "Apague");
   - a avaliação das 20 perguntas do README (o Edson mediu 15/20);
   - a comparação Python × Quarkus com o modelo real (critério: 100%).
3. [ ] **Ligar a busca real na interface.** Só se a etapa 3 do teste der OK.
   No servidor (`ssh prointec@152.92.2.63`):
   ```bash
   cd /opt/apps/chateau-expert
   nano .env.prod          # acrescentar as 3 linhas abaixo
   #   COMPOSE_PROFILES=ia
   #   ORCHESTRATION_URL=http://orchestration:8000
   #   OLLAMA_URL=<o valor que o teste indicou>
   docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
   docker logs --tail 20 chateau_orchestration
   ```
   Se `docker ps` não mostrar o `chateau_orchestration`, o Compose do servidor
   não leu o `COMPOSE_PROFILES` do `.env.prod`: rodar o mesmo comando com
   `--profile ia` e avisar (o deploy automático também não vai subi-lo).
   Depois, perguntar pelo chat: "Quantos livros existem?", "Quantos artigos o
   Hermes Alves Filho publicou em 2024?" e "Quantas bananas tem numa penca?".
   - **Para voltar ao mock:** apagar a linha `ORCHESTRATION_URL` do
     `.env.prod` e rodar o mesmo `docker compose ... up -d`.
   - O `.env.prod` não é versionado: a configuração sobrevive aos deploys
     automáticos.

Depois:

- [ ] Rodar de novo com mais perguntas reais e anotar erros e acertos para o
      Edson (material para a próxima versão do modelo).
- [ ] Com a comparação em 100%: decidir a troca para a Quarkus (Fase 7) —
      apontar o compose para `orchestration/quarkus/`, validar em produção e
      aposentar a versão Python.
- [ ] Se o `/api/chat` (LangChain4j) gerar a mesma consulta que o
      `/api/generate`, levar ao Edson a decisão sobre qual usar como padrão.
- [ ] Antes de devolver a GPU: voltar a interface para o mock (apagar
      `ORCHESTRATION_URL` do `.env.prod` e `up -d`) se o túnel não for
      continuar de pé — senão o chat mostra "serviço indisponível".

## 4. Aplicação — `chateau-expert`

- [x] Autenticação web → API: implementada, commitada (`514cc8a`) e token gerado no `.env.prod` (20/10). [Desfecho](analises/divergencias-2026-10-20.md).
- [ ] Validar em produção (<http://chateau2.duckdns.org:8080>): entrar com Google, abrir `/chat`, fazer uma busca e abrir `/admin` com um administrador.
- [ ] Retenção de logs de acesso: decidir o prazo (página diz 6 meses, código tem limpeza de 90 dias nunca chamada) e implementar a rotina. Ver [termos e privacidade](../dominio/negocio/termos-e-privacidade.md).
- [ ] Middleware web usa o JWT quando a API está fora do ar (fail-open): decidir se mantém.
- [ ] Tarefa 5: ambiente de avaliação — nada ainda (reunião de 19/10).

## 5. Identidade visual

- [x] Tarefa 31: Figma recebido e lido em 20/10 ([análise](analises/figma-2026-10-20.md)); é espelho do protótipo (versão 01, 13/10, commit `3cf7be7`) e, por regra do próprio arquivo, o código prevalece.
- [ ] Revogar o token pessoal do Figma usado na leitura (Settings → Security) quando o levantamento terminar.
- [ ] Se o original do Edson mudar, refazer a cópia ou pedir acesso de leitura para `mvurban@mvurban.eti.br` (a cópia em rascunhos não acompanha o original).

## 6. Documentação e segurança

- [ ] Trocar a senha SSH que ficou no histórico Git da raiz (commit `b8ff640`, já publicado).
- [ ] Atualizar o [diagrama web–API](diagrams/chateau-web-api-map.drawio): ainda mostra a busca como mock no navegador e não mostra o token web → API.
- [ ] Revisar guias antigos do `chateau-data` (`scripts/README.md`, `docs/knowledge-graph-pipeline.md`, `docs/levantamento-campos.md`) que citam versões e comandos anteriores.
- [ ] Decidir a relação entre o modelo relacional alvo (`chateau-db-schema.json`) e o modelo acadêmico rev_6.
