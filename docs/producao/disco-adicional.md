# Disco adicional para o deploy — avaliação de 26/10/2026

O servidor tem um disco virtual `vda` de 20 GB. O build do Expert falhou com `no space left on device` ao gravar metadados temporários, após construir as imagens. Um segundo disco de 40 GB pode resolver a falta de espaço **se receber efetivamente o armazenamento de imagens, containers e cache de build**. Anexar o disco à VM, sozinho, não muda os caminhos usados pelo Docker.

## Responsabilidades

- **Administração do servidor:** criar o sistema de arquivos no novo disco, montar de forma persistente, fazer backup, parar os serviços, copiar o armazenamento existente, configurar Docker/containerd e iniciar os serviços. Essa etapa provoca indisponibilidade temporária e exige privilégios de administrador.
- **Deploy do Expert:** após a configuração do daemon, `docker compose build` usa automaticamente o armazenamento configurado. O workflow já verifica espaço em `/tmp` e no `DockerRootDir` antes do build; a validação deve incluir também o armazenamento do containerd se ele for o image store ativo. Não executar migração de dados de host dentro do workflow de deploy.

## O que muda conforme o Docker instalado

- Com o driver clássico `overlay2`, o armazenamento de imagens e cache fica no `DockerRootDir` (normalmente `/var/lib/docker`). Migrar e apontar esse diretório para o disco novo é uma operação única e rotineira, desde que feita com Docker parado e cópia que preserve permissões.
- Com o *containerd image store* (padrão em instalações novas do Docker Engine 29), imagens e snapshots ficam em `/var/lib/containerd`, separado do `DockerRootDir`. Configurar somente `data-root` não move esses dados; é preciso configurar/migrar os dois caminhos, ou montar o disco para ambos. [Documentação do Docker](https://docs.docker.com/engine/storage/containerd).
- PostgreSQL e Neo4j usam *bind mounts* em `/opt/apps/chateau-expert/backend/volumes`. Eles continuam no disco atual se só o armazenamento do Docker for transferido; medir seu tamanho para decidir se também precisam ir ao novo disco.

## Sequência segura para a migração administrada

1. Identificar driver, diretórios efetivos e tamanhos. Confirmar que o novo disco tem espaço para os dados atuais e crescimento.
2. Fazer backup dos bancos e da configuração de Docker/containerd; registrar o estado atual para rollback.
3. Criar um sistema de arquivos Linux no novo disco e um ponto de montagem persistente por UUID em `/etc/fstab`. Verificar a montagem **antes** de copiar.
4. Parar os containers e os serviços Docker/containerd numa janela de manutenção. Copiar os diretórios necessários preservando propriedade, permissões e links; manter os diretórios antigos intactos até a validação.
5. Configurar o caminho do daemon e, se aplicável, do containerd. Iniciar os serviços, conferir imagens, containers, bancos e montagens. Só então permitir o próximo deploy.
6. Rodar o deploy e comparar espaço livre antes/depois. Remover cópias antigas apenas após confirmação de que o site e os bancos funcionam e de que existe rollback.

**Viabilidade:** a operação é factível e comum para quem administra Linux/Docker, mas não é um ajuste trivial de Compose. A dificuldade exata depende do driver e do volume de dados atuais. O processo de cópia e parada pode levar mais tempo que o deploy; não há estimativa segura sem esses números. Ampliar o `vda` existente seria mais simples por evitar a migração, se a infraestrutura oferecer essa opção.

Para fechar o procedimento e a checagem automática do novo disco, obter do servidor: `docker version --format '{{.Server.Version}}'`, `docker info --format 'DockerRootDir={{.DockerRootDir}} StorageDriver={{.Driver}} DriverStatus={{json .DriverStatus}}'`, `lsblk -f`, `df -h / /tmp /var/lib/docker /opt/apps/chateau-expert/backend/volumes` e tamanhos de `/var/lib/docker`, `/var/lib/containerd` e `backend/volumes`. Não registrar segredos do `.env.prod`.
