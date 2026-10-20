# Divergências e decisões pendentes — revisão de 20/10/2026

Este registro separa observações verificáveis de decisões ainda não tomadas. Não é uma segunda fonte de regras. Quando uma questão for resolvida, atualizar o assunto em [dominio/](../../dominio/indice.md) e registrar aqui o desfecho.

## Escopo da revisão

Inventário dos arquivos rastreados nos três repositórios (21 na raiz, 161 em `chateau-data`, 244 em `chateau-expert`) e do protótipo local. Código, configuração, documentação, modelos JSON, ontologia, schemas, migrations, testes, fixtures e o diagrama XML foram examinados por estrutura e, nos assuntos de domínio, pelo conteúdo. Locks de dependência foram conferidos como inventário. Imagens, currículos/certificados/PDFs brutos, planilhas de entrada, dados pessoais de amostra e artefatos gerados não foram usados como documentação normativa.

## Prioridade alta: autorização das rotas da API

O [middleware web](../../chateau-expert/web/src/middleware.ts) restringe `/admin`, e as rotas Next.js de busca/conversa usam a sessão. Porém o [backend Express](../../chateau-expert/backend/src/app.ts) monta rotas administrativas e de privacidade sem middleware de autenticação. A [rota de privacidade](../../chateau-expert/backend/src/routes/privacy.router.ts) aceita e-mail fornecido no pedido para exportar ou excluir a conta; [authorizeUser](../../chateau-expert/backend/src/middleware/authorizeUser.ts), nas rotas onde é usado, também confia no e-mail do pedido para identificar o usuário. O Compose atual não publica a porta da API diretamente, mas o serviço é alcançável na rede `frontend_net`. **Questão:** definir e implementar autenticação/autorização entre web e API antes de expor novos caminhos de acesso ou integrar a nova UI. Não assumir que o controle da página protege sozinho os endpoints internos.

## Política e retenção de dados

- A [página de privacidade](../../chateau-expert/web/src/app/privacidade/page.tsx) informa retenção dos logs de acesso por até seis meses. O [serviço de privacidade](../../chateau-expert/backend/src/services/privacy.service.ts) possui `cleanOldAccessLogs(90)`, mas não há chamada encontrada no código versionado. Decidir prazo e rotina efetiva; não anunciar uma limpeza automática como implementada.
- O [README do Data](../../chateau-data/README.md) diz que a LGPD não se aplica aos documentos de desenvolvimento por finalidade exclusivamente acadêmica. O web, por sua vez, publica política de privacidade e direitos da conta. Essas afirmações têm contextos diferentes e a aplicabilidade jurídica não foi verificada nesta revisão de código. Não transportar a frase do README para uma regra geral do produto sem análise específica.

## Versões de modelo e documentação antiga

- **Perda de dados confirmada nesta revisão:** `python3 -m unittest discover -s tests -p 'test_producoes_extracao_pdf.py' -v`, a partir de `chateau-data/scripts`, falhou em 20 PDFs. A comparação independente documentada em [scripts/tests/README.md](../../chateau-data/scripts/tests/README.md) confirma que o extrator de Sucupira PDF deixa produções de fora. Corrigir o parser e repetir o teste antes de confiar na cobertura de produção do grafo.
- O [padrão executado pelo pipeline](../../chateau-data/scripts/chateau-extract/common/model.py) e o [README atual do Data](../../chateau-data/README.md) apontam para `rev_6_training`. A [análise Sucupira rev_5](../../chateau-data/docs/sucupira-pdf-vs-api/campos-do-modelo-rev5.md) afirma que rev_5 é o único modelo oficial — era verdadeira naquele contexto datado, não hoje.
- Um comentário em `common/model.py` diz que a rev_6 muda somente relações; o JSON rev_6 contém também nós/propriedades novos ou alterados em comparação com a rev_5. Para mudanças de schema, comparar os JSONs, não confiar nesse comentário.
- [scripts/README.md](../../chateau-data/scripts/README.md), [knowledge-graph-pipeline.md](../../chateau-data/docs/knowledge-graph-pipeline.md) e partes de [levantamento-campos.md](../../chateau-data/docs/levantamento-campos.md) ainda citam diretórios, versões e comandos de etapas anteriores. O índice do domínio aponta para o padrão atual; esses textos ficam como histórico até revisão específica.
- O [diagrama web–API](../diagrams/chateau-web-api-map.drawio) ainda desenha a busca como mock no navegador e a orquestração como futura. O [chat web](../../chateau-expert/web/src/app/chat/page.tsx) já chama `/api/search`; o desenho precisa de revisão antes de servir como mapa atual.
- O [modelo alvo relacional](../../chateau-data/model/schema/chateau-db-schema.json), o [modelo de grafo rev_6](../../chateau-data/model/diagramas/training/Expert-Finding-in-academia_rev_6_training.json), o [schema de produção](../../chateau-expert/orchestration/schema/schema_producao.txt) e o [schema Prisma](../../chateau-expert/backend/prisma/schema.prisma) têm finalidades diferentes. Ainda falta decisão sobre a relação entre o alvo relacional e o modelo acadêmico vigente.

## Interface e busca

- [web/dominio.md](../../chateau-expert/web/dominio.md) chama autorização por domínio de e-mail de futura; [auth.service.ts](../../chateau-expert/backend/src/services/auth.service.ts) já a implementa. [dominio/negocio/acesso.md](../../dominio/negocio/acesso.md) registra o comportamento atual.
- O seletor de `AiModel` no [chat atual](../../chateau-expert/web/src/app/chat/page.tsx) não integra o pedido de busca; o backend recebe `{pergunta}`. Evitar descrevê-lo como escolha efetiva do modelo texto→Cypher.
- O protótipo Vite usa busca, consentimento e persistência locais, incompatíveis diretamente com o contrato do Expert. A [análise inicial](ui-prototipo-2026-10-20.md) contém o mapa de integração. Conceitos do Figma ainda não foram fornecidos/validados.
