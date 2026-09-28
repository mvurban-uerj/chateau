# TODO — teste do modelo real com GPU (qua 30/09 a sex 02/10)

Detalhes e justificativas: `docs/integracao-modelo/README.md`, Fase 5.

## Antes de quarta

- [ ] Combinar com o Edson o **horário** e **quem sobe o túnel** da máquina com
      GPU. O Ollama precisa aparecer no servidor em `127.0.0.1:11434`.
- [ ] Ter à mão a **senha do SSH** do `prointec@152.92.2.63`.
- [ ] Docker Desktop rodando na máquina local.
- [ ] (Opcional) Acrescentar perguntas em
      `chateau-expert/orchestration/teste_modelo/perguntas.txt` (uma por linha).
- [ ] Pendente com o Edson: datas e identificadores gravados como texto
      (`datePublished: "2021"`) × `DATE`/`INTEGER` no modelo. Ele pediu para
      seguir o README, que não trata disso. O teste de quarta vai mostrar o
      impacto real nas perguntas com ano.

## Quarta — com o túnel de pé

1. [ ] Rodar o teste (pede só a senha do SSH; leva alguns minutos):
   ```bash
   bash ~/projetos/chateau/chateau-expert/orchestration/teste_modelo/testar_modelo.sh
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

## Quinta e sexta

- [ ] Rodar de novo com mais perguntas reais e anotar erros e acertos para o
      Edson (material para a próxima versão do modelo).
- [ ] Com a comparação em 100%: decidir a troca para a Quarkus (Fase 7) —
      apontar o compose para `orchestration/quarkus/`, validar em produção e
      aposentar a versão Python.
- [ ] Se o `/api/chat` (LangChain4j) gerar a mesma consulta que o
      `/api/generate`, levar ao Edson a decisão sobre qual usar como padrão.

## Antes de devolver a GPU

- [ ] Voltar a interface para o mock (apagar `ORCHESTRATION_URL` do
      `.env.prod` e `up -d`) se o túnel não for continuar de pé — senão o
      chat mostra "serviço indisponível".
