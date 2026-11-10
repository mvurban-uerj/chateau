# Índice do domínio — Chateau

Fonte canônica dos conceitos e regras do projeto, compartilhada pelos repositórios `chateau-data` e `chateau-expert`. Leia **só o assunto da tarefa**. O código e os modelos versionados comprovam o estado de implementação; [docs/](../docs/indice.md) guarda a história, propostas e questões abertas.

Revisão inicial de 20/10/2026 contra `chateau-data` `04c8225` e `chateau-expert` `51c4b1b`; reconferida no mesmo dia contra `chateau-data` `c770241` (só `AGENTS.md` mudou) e `chateau-expert` `514cc8a` (autenticação web → API). Conferir novamente as fontes ao mudar de commit.

Atualização de interface decidida em 26/10/2026: [interfaces](tech/interfaces.md), [administração](negocio/administracao.md) e [contexto](modelo/contexto-ux.md) descrevem a marcação vermelha de simulações e o seletor visual alimentado pelo catálogo de modelos.

Implementação local de 10/11/2026: [administração](negocio/administracao.md) define upload, lista, importação e exclusão de arquivos Cypher no Admin, usa ícones para atualizar e remover arquivos, mostra andamento e conclusão da carga em modal e abre a limpeza completa do grafo em outro modal com confirmação. [Decisão](../docs/analises/admin-grafo-2026-11-10.md). Deploy e validação no servidor pendentes.

Decisão de 27/10/2026: [administração](negocio/administracao.md) registra o cadastro de URL, nome técnico e disponibilidade e o envio do nome técnico escolhido pelo navegador. [Contrato da busca](tech/contrato-de-busca.md) registra que a ausência de modelo selecionado aciona o mock; `ORCHESTRATION_URL` apenas substitui o endereço interno da orquestração. Implementação no Expert `bc6f16a`; validação em produção pendente.

Ajuste de 29/10/2026: [administração](negocio/administracao.md) permite compartilhar o nome técnico entre versões; o [contrato da busca](tech/contrato-de-busca.md) usa o ID do cadastro para selecionar a URL. Expert `8000529` enviado a `main`; deploy e busca real pendentes de validação. [Diagnóstico](../docs/analises/modelos-admin-2026-10-29.md).

Implementação local de 04/11/2026: [administração](negocio/administracao.md) registra várias URLs ordenadas por cadastro; o [contrato da busca](tech/contrato-de-busca.md) define failover sequencial em falhas técnicas claras. Distribuição normal de carga, regra de lentidão e validação em produção estão pendentes. [Contexto](../docs/analises/failover-modelo-2026-11-04.md).

Correção de 04/11/2026: [administração](negocio/administracao.md) e [contrato da busca](tech/contrato-de-busca.md) retiram o formato de prompt do cadastro; o nome técnico seleciona o de-para no código. Esta regra substitui a seleção por cadastro registrada em 03/11.

Ajuste de interface de 04/11/2026: [administração](negocio/administracao.md) limita a rolagem à lista de URLs e mostra mensagem específica para URLs repetidas.

Ajuste de 04/11/2026: [administração](negocio/administracao.md) permite reordenar as URLs pelo ícone de arrastar ou pelas setas do teclado. A ordem salva define qual URL será tentada primeiro e a sequência do failover.

Decisão de 04/11/2026: o [contrato da busca](tech/contrato-de-busca.md) registra horário, duração, URL e desfecho de todas as chamadas ao modelo para medir a latência real por servidor antes de definir quando acionar outra URL. [Registro da decisão](../docs/analises/medicao-latencia-modelo-2026-11-04.md).

Decisões de 10/11/2026: [operação](tech/operacao-e-validacao.md) executa testes, build de imagens no GitHub Actions e publicação no Expert somente no push para `deploy`; o servidor baixa as imagens prontas do GHCR. Push no `main` não dispara o workflow. Publicar é `git push origin main:deploy`. O gatilho de testes de 05/11 e o build no servidor foram substituídos.

Implementação local de 05/11/2026: [administração](negocio/administracao.md), [conversas e busca](negocio/conversas-e-busca.md) e [contrato da busca](tech/contrato-de-busca.md) registram o modelo orquestrador (`gemma4:31b`, `127.0.0.1:11436`). Ele é ligado pelo Admin, reescreve a pergunta com o contexto da conversa antes do modelo Cypher e mostra a todos o “Fluxo da resposta”. Expert `e6f4add` enviado a `main`; deploy e teste com o modelo real pendentes. [Plano](../docs/integracao-modelo/plano-modelo-orquestrador.md).

Ajuste de 28/10/2026: [conversas e busca](negocio/conversas-e-busca.md) distingue o aviso de busca sem modelo e sem resposta do aviso de falha com modelo escolhido.

Alteração de 03/11/2026: [conversas e busca](negocio/conversas-e-busca.md) e [contrato da busca](tech/contrato-de-busca.md) registram `fora_escopo` para recusa explícita do 31B. A seleção de formato de prompt por cadastro foi substituída em 04/11 pelo de-para do nome técnico.

Regra de interface confirmada em 28/10/2026: [interfaces](tech/interfaces.md) exige internacionalização de todos os textos fixos de tela, inclusive no catálogo de componentes.

Decisão de 28/10/2026: [arquitetura](tech/arquitetura.md) e [operação](tech/operacao-e-validacao.md) definem Quarkus como orquestração padrão, com Python preservado para comparação paralela e retorno.

Vocabulário confirmado em 28/10/2026: [glossário](negocio/glossario.md) usa “modelo de IA” e “servidor do modelo de IA” na comunicação do produto; identificadores de protocolo existentes continuam documentados no [contrato de busca](tech/contrato-de-busca.md).

Esclarecimento de 28/10/2026: a [visão geral](negocio/visao-geral.md) descreve o servidor do modelo como caixa preta, apenas pelo que a orquestração envia e recebe. Caminhos HTTP e detalhes da integração pertencem ao [contrato técnico](tech/contrato-de-busca.md).

Os arquivos distinguem **regra implementada**, **modelo definido** e **proposta**. Não interpretar um nó de grafo, campo planejado ou mock como funcionalidade entregue. Detalhes exaustivos de propriedades e relações pertencem ao JSON do modelo indicado abaixo.

## Produto e negócio

| Ao trabalhar com… | Ler |
|---|---|
| Objetivo, fronteiras, vocabulário e fluxo de ponta a ponta (dados → grafo → modelo → web) | [negocio/visao-geral.md](negocio/visao-geral.md) · [negocio/glossario.md](negocio/glossario.md) |
| Login, autorização, perfis de acesso, proteção da API | [negocio/acesso.md](negocio/acesso.md) |
| Administração de usuários, domínios, modelos e exemplos | [negocio/administracao.md](negocio/administracao.md) |
| Conversas, busca e apresentação dos resultados | [negocio/conversas-e-busca.md](negocio/conversas-e-busca.md) |
| Autorização de contexto (sem termo de uso), dados pessoais, exportação e exclusão | [negocio/termos-e-privacidade.md](negocio/termos-e-privacidade.md) |

## Modelo acadêmico e dados

| Ao trabalhar com… | Ler |
|---|---|
| Entidades, relações e versões do grafo acadêmico | [modelo/grafo-academico.md](modelo/grafo-academico.md) |
| Contexto do usuário e grafo de UX | [modelo/contexto-ux.md](modelo/contexto-ux.md) |
| Fontes, extração, proveniência e limites dos dados | [dados/fontes-e-pipeline.md](dados/fontes-e-pipeline.md) |

## Implementação e operação

| Ao trabalhar com… | Ler |
|---|---|
| Responsabilidades dos repositórios e ambientes | [tech/arquitetura.md](tech/arquitetura.md) |
| API de busca, orquestração e segurança da consulta | [tech/contrato-de-busca.md](tech/contrato-de-busca.md) |
| Web atual e protótipo da nova UI | [tech/interfaces.md](tech/interfaces.md) |
| Compose, deploy, testes e schema de execução | [tech/operacao-e-validacao.md](tech/operacao-e-validacao.md) |

## Manutenção da fonte canônica

- Escrever a regra uma vez, com fonte rastreável. O índice é roteador, não cópia dos documentos.
- Antes de mudar um conceito, conferir modelo/código atual e [divergências conhecidas](../docs/analises/divergencias-2026-10-20.md). Uma divergência exige decisão explícita antes de declarar uma nova regra.
- O Figma (versão 01, 13/10/2026) foi lido em 20/10/2026 e é espelho do protótipo: [análise](../docs/analises/figma-2026-10-20.md). Seus conceitos entram nos arquivos temáticos só quando decididos.
- O repositório raiz versiona estes documentos separadamente dos dois repositórios de implementação. Uma mudança que atravesse repositórios deve registrar quais versões de código foram verificadas.
