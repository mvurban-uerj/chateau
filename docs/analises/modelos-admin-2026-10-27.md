# Issue #34 — configuração e escolha de modelos — 27/10/2026

Mensagem do Edson copiada pelo usuário em `docs/talk-ia.md`: o administrador deve informar URL e MODELO para acesso a cada modelo; ele já dispõe de um modelo treinado e poderá colocá-lo no ar conforme as reservas de GPU. Exemplos informados: `URL=http://127.0.0.1:11434` e `Modelo=chateau-gemma4-e4b-cypher`.

Marcelo confirmou em 27/10/2026 que **a pessoa escolhe o modelo no seletor do chat**. Na fase de testes, o cadastro deve aceitar URLs diferentes; uma URL de domínio fixo pode ser adotada depois, sem ser exigida agora.

Correção do Marcelo no mesmo dia: o **navegador envia o nome técnico do modelo escolhido**, e o formulário do admin deve nomear explicitamente os campos **Nome, Descrição, Nome do modelo, URL e Versão**. Cada cadastro terá uma opção **Disponível**: só os marcados aparecem no chat; quando houver apenas um disponível, o seletor some e esse modelo é usado automaticamente.

## Estado do código em `chateau-expert` `dc77c53`

- `AiModel` guarda `name`, `label`, `description` e `version`; ainda não tem URL nem identificador de execução.
- O seletor do `Composer` guarda a escolha só no estado visual. `POST /api/search` recebe apenas `pergunta`; o backend não lê o cadastro de modelos na busca.
- A orquestração Python usa `OLLAMA_URL` e `OLLAMA_MODELO` carregados do ambiente ao iniciar. Ela recebe pergunta e usuário, sem seleção por requisição.
- Em produção, a orquestração roda em container. O exemplo `127.0.0.1:11434` aponta para o próprio container se usado ali; a ponte do host ou outro endereço alcançável deve ser informado no cadastro para o teste.

## Caminho implementado localmente no Expert

1. Administrador cadastra a URL do servidor e o nome técnico do modelo de IA em cada registro e marca Disponível quando deve aparecer no chat. A listagem enviada ao usuário omite a URL.
2. O chat envia o **nome técnico** com a pergunta. O backend valida que ele corresponde a um cadastro disponível, busca sua URL no PostgreSQL e repassa os dois valores à orquestração. O navegador não controla diretamente o endereço de destino.
3. A orquestração usa a configuração recebida apenas naquela requisição; o schema do grafo e as regras de leitura permanecem os mesmos.
4. Registros anteriores à migração começam indisponíveis. Com um modelo disponível, o seletor fica oculto; sem modelos disponíveis, a busca continua com dados simulados e a interface indica esse estado.

Implementação no Expert `bc6f16a` em 27/10: migração Prisma, API, formulário do admin, chat e orquestração Python/Quarkus. Push realizado; deploy e funcionamento em produção ainda não verificados. Os cadastros antigos começam indisponíveis. A seleção inicial usa a maior versão disponível; o nome técnico é preservado com a pergunta e a resposta no histórico; falha do modelo usa a simulação já existente com aviso. Aceitar endereços variados no cadastro não resolve conectividade: a URL precisa ser acessível a partir do container de orquestração.

No Compose de produção, a orquestração sobe com os demais serviços, na mesma rede da API. O endereço interno padrão é `http://orchestration:8000`; `ORCHESTRATION_URL` serve apenas para apontar a API a outro endereço. A ausência de modelo disponível selecionado aciona o mock, independentemente dessa variável. Se um modelo escolhido falhar, a resposta também é simulada, com aviso distinto de modelo fora do ar.

Como o navegador envia apenas o nome técnico, ele é único no catálogo; dois endereços com o mesmo nome técnico precisariam de uma regra adicional de escolha antes de serem cadastrados simultaneamente. A URL só é devolvida na rota administrativa.

Verificação: migração aplicada no PostgreSQL de teste; 29 testes de integração do backend e 37 testes direcionados do web passaram; lint e build do web, build do backend e 23 testes Python passaram; Quarkus compilou. Após a correção do interruptor, passaram novamente os 18 testes de busca do backend e os 26 testes do Composer/chat, além de lint e build do web e build do backend. `docker compose ... config --services` confirmou a presença da orquestração no Compose de produção sem perfil. O teste com dois cadastros confirma que o backend encaminha a URL correspondente ao nome técnico enviado pelo navegador. O teste de integração Quarkus não completou neste Docker Desktop porque o Testcontainers não conseguiu alcançar a porta publicada do Neo4j; o contrato por requisição foi compilado, mas essa execução ainda precisa ser validada. Nenhum fluxo foi testado com a GPU real.
