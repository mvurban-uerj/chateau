# Deploy com imagens prontas — decisão de 10/11/2026

O log recebido em `docs/talk-ia.md` mostrou que o build web no servidor gastou 384 s em `npm ci`, 342 s copiando `node_modules` entre estágios e 558 s em `next build`. A máquina tinha 2 GiB de RAM e 5,4 GiB livres em disco antes do build. Esses dados motivaram retirar a compilação do servidor; não identificam isoladamente o gargalo de CPU, rede ou I/O.

## Decisão

O push na branch `deploy` continua sendo o único gatilho. Após os testes, três jobs constroem em paralelo imagens `linux/amd64` da API, web e orquestração Quarkus. Cada imagem vai para o GHCR privado com a tag do SHA do commit; o `GITHUB_TOKEN` do próprio workflow publica e lê os pacotes. O job de deploy só começa quando todas as imagens existem. No servidor, um token temporário autentica o download, todas as imagens são baixadas antes de trocar as tags locais e o Compose sobe com `--no-build --pull never --wait`. O token usa um diretório temporário de configuração Docker, removido ao sair. O PostgreSQL, Neo4j, `.env.prod` e seus volumes permanecem no servidor.

O script remoto confere que o checkout corresponde ao SHA recebido, exige servidor x86_64 e espaço livre antes de baixar. O marcador `.deploy-successful-sha` só é atualizado depois de `docker compose up` e do reinício do Caddy. O rollback continua sendo a publicação de um commit anterior na branch `deploy`, que reconstrói as imagens desse SHA. O servidor não usa cache de build entre releases; o cache de build fica no GitHub Actions, separado por serviço.

## Limites e validação pendente

- Verificação local: `actionlint` aceitou o workflow; o YAML e o Compose resolveram o gatilho, as dependências e os três nomes de imagem; backend passou 97 testes e web passou 175; os três Dockerfiles construíram imagens `linux/amd64`. Uma simulação do script confirmou que os três downloads precedem a troca das tags e que uma falha no download não altera tags nem marcador.
- O servidor ainda precisa de espaço e banda para receber as imagens. A primeira transferência baixa todas as camadas; as seguintes podem reutilizar camadas já presentes. A velocidade real depende da rede e do armazenamento do servidor.
- O primeiro run precisa confirmar que o repositório pode publicar os três pacotes no GHCR e que o token do job de deploy pode lê-los. O GitHub documenta `GITHUB_TOKEN` para pacotes vinculados ao repositório; o estado real das permissões não foi consultado nesta sessão.
- A arquitetura do servidor não foi verificada diretamente. Se não for x86_64, o script interrompe a publicação antes de trocar os containers; será necessário gerar a plataforma correta.
- Os testes e a compilação local de código estão no workflow. Ainda não há testes específicos da orquestração no gate nem checagem funcional autenticada após subir os containers.
- O primeiro run remoto ainda precisa comprovar publicação no GHCR, download no servidor e saúde dos serviços; as verificações locais não substituem essa validação.

Fontes: [GitHub Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry), [Docker Buildx multiplataforma](https://docs.docker.com/build/building/multi-platform/) e [Docker Compose up](https://docs.docker.com/reference/cli/docker/compose/up).
