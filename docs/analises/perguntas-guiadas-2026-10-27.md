# Revisão das perguntas guiadas e do Tab — 27/10/2026

Revisão de código contra `chateau-expert` `dc77c53` e `chateau-data` `fea4635`, sem alterar a implementação. O gerador (`backend/scripts/gerar-perguntas-guiadas.ts`) lê o rev_6, o Chateau-UX e o dicionário para **validar** variáveis e rótulos usados em dois moldes. Os textos e opções são definidos no próprio script a partir do protótipo; ele não consulta os valores carregados no Neo4j. A seed grava a versão gerada no PostgreSQL e apaga/recria as perguntas quando o hash do conteúdo muda ([serviço](../../chateau-expert/backend/src/services/guided-questions.service.ts)).

## Comportamento atual conferido no código

- O campo aceita texto livre. Se o início corresponde a um molde, Tab aceita um trecho sugerido ou uma opção por vez; no fim do molde, ou quando não há sugestão a completar, abre o modal com as escolhas reconhecidas já marcadas. No campo vazio, Tab primeiro escreve a frase animada do placeholder. Esc dispensa a sugestão até esvaziar o campo.
- O modal tem dois moldes: **Buscar candidatos** (área, vínculo, produção, disponibilidade e requisito obrigatório) e **Montar equipe** (tamanho, natureza, área e disponibilidade). "Qualquer" limpa as outras escolhas da pergunta. Confirmar escreve a frase no campo; Enter a envia como texto ao contrato atual de busca.
- Os cards de ação da tela estão desabilitados, mas os dois moldes ainda podem ser alcançados digitando seus inícios no campo. Nenhum dos dois aciona um fluxo estruturado de seleção ou montagem de equipe.

## Pontos para crítica com o Edson

| Exemplo concreto | Limite atual | Decisão necessária |
|---|---|---|
| Áreas como "Inteligência Computacional" e "Engenharia de Dados" | São listas fixas do protótipo; a validação confirma `LineOfResearch.name` no modelo, não confirma que esses valores existem na carga | Fonte e atualização das opções reais |
| "Quadro efetivo docente/técnico", "substitutos" e "complementar" | O script aponta para `Role.roleName | Job.jobTitle`, mas `Role`/`Job` não constam do schema de produção versionado | Relação exata entre cargo, tipo de vínculo e opções exibidas após a carga rev_6 |
| "Só quem está disponível" | `Availability.enable` é do Chateau-UX/PostgreSQL, não do grafo acadêmico consultado pelo modelo; o contexto ainda não entra na busca | Como aplicar a disponibilidade de terceiros e de qual fonte ela virá |
| "O que é obrigatório? O resto pesa, mas não elimina ninguém" | `varDomainModel` é `null`; a frase é enviada ao modelo como texto, sem motor de eliminação ou pesos | Se essa opção deve ficar visível antes de existir ranqueamento e qual contrato a executará |
| "Montar equipe" pelo campo | O card está desabilitado, mas o molde monta uma pergunta textual e abre o modal | Se o molde deve continuar acessível como texto livre ou ficar oculto até o fluxo de equipe existir |
| Edição administrativa | A seed substitui todos os registros do idioma quando o hash muda | Se o admin pode editar e, se puder, como preservar o trabalho numa nova versão |

As opções do modal não recebem hoje a mesma marcação vermelha dos filtros simulados. Isso deve ser resolvido junto da decisão sobre quais opções são exemplos e quais são valores reais; [a regra visual](../../dominio/modelo/contexto-ux.md) marca dados simulados em vermelho.

## Verificação e limite

Os testes existentes de `Composer` e `moldes` cobrem Tab, seleção, Esc, texto livre, modal e frase final. Esta revisão leu o código e esses testes; não executou uma busca com o modelo real nem validou o conteúdo com o Edson. A existência de nós/propriedades no JSON rev_6 não comprova dados carregados ou capacidade de filtragem do modelo.
