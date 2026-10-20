# Chateau — orientação para agentes

- Este diretório coordena três repositórios Git independentes: a raiz (`chateau`), `chateau-data/` e `chateau-expert/`. Confira o estado de cada um antes de editar.
- [dominio/indice.md](dominio/indice.md) é o ponto de entrada e a fonte canônica dos conceitos e regras do projeto. Abra apenas os assuntos pertinentes à tarefa; não carregue todos os documentos de uma vez.
- [docs/indice.md](docs/indice.md) aponta para análises, decisões, reuniões e pendências. Um protótipo, plano ou reunião não altera uma regra vigente sem decisão registrada.
- Para detalhes executáveis, confira também o código e os contratos versionados no repositório responsável. Se eles divergirem de `dominio/`, explicite a divergência; não corrija silenciosamente uma fonte a partir da outra. As divergências já encontradas estão em [docs/analises/divergencias-2026-10-20.md](docs/analises/divergencias-2026-10-20.md).
- Ao confirmar ou alterar uma regra de produto, atualize o arquivo temático em `dominio/` e seu índice. Registre contexto e decisão datada em `docs/` quando o motivo não for evidente.
- A UI em `/mnt/c/temp/chateau/ui` é um protótipo isolado com dados simulados. Sua análise está em [docs/analises/ui-prototipo-2026-10-20.md](docs/analises/ui-prototipo-2026-10-20.md).
