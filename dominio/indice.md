# Índice do domínio — Chateau

Fonte canônica dos conceitos e regras do projeto, compartilhada pelos repositórios `chateau-data` e `chateau-expert`. Leia **só o assunto da tarefa**. O código e os modelos versionados comprovam o estado de implementação; [docs/](../docs/indice.md) guarda a história, propostas e questões abertas.

Revisão inicial de 20/10/2026 contra `chateau-data` `04c8225` e `chateau-expert` `51c4b1b`. Conferir novamente as fontes ao mudar de commit.

Os arquivos distinguem **regra implementada**, **modelo definido** e **proposta**. Não interpretar um nó de grafo, campo planejado ou mock como funcionalidade entregue. Detalhes exaustivos de propriedades e relações pertencem ao JSON do modelo indicado abaixo.

## Produto e negócio

| Ao trabalhar com… | Ler |
|---|---|
| Objetivo, fronteiras e vocabulário | [negocio/visao-geral.md](negocio/visao-geral.md) · [negocio/glossario.md](negocio/glossario.md) |
| Login, autorização, perfis de acesso | [negocio/acesso.md](negocio/acesso.md) |
| Administração de usuários, domínios, modelos e exemplos | [negocio/administracao.md](negocio/administracao.md) |
| Conversas, busca e apresentação dos resultados | [negocio/conversas-e-busca.md](negocio/conversas-e-busca.md) |
| Termos, dados pessoais, exportação e exclusão | [negocio/termos-e-privacidade.md](negocio/termos-e-privacidade.md) |

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
- O Figma ainda será fornecido. Seus conceitos entrarão em arquivos temáticos com referência ao frame/versão e estado de validação, após avaliação conjunta.
- O repositório raiz versiona estes documentos separadamente dos dois repositórios de implementação. Uma mudança que atravesse repositórios deve registrar quais versões de código foram verificadas.
