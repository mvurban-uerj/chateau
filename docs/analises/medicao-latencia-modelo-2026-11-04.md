# Medição de latência do modelo — 04/11/2026

## Decisão

Antes de definir quando uma resposta é lenta ou enviar o mesmo prompt a outra URL, registrar as chamadas reais ao servidor do modelo e analisar um relatório de buscas. Nenhum limiar de lentidão ou chamada paralela foi aprovado nesta etapa. O failover sequencial já decidido permanece igual.

Quarkus (padrão em produção) e Python (reserva de comparação) passam a registrar, em cada linha JSONL de busca, `tentativas_modelo` com uma entrada por chamada de geração efetivamente iniciada: URL, início com precisão de milissegundos, tempo decorrido medido pelo cliente, desfecho e, quando a resposta os fornece, tokens do prompt, tokens da resposta e duração informada pelo servidor. A lista existe também quando há somente uma URL e quando há erro ou timeout. Aquecimento do modelo na subida não é uma busca e não entra nessa lista. O arquivo é `CHATEAU_LOG`; no Compose de produção, `/logs/consultas.jsonl` está no volume `orchestration_logs`. A resposta HTTP da busca não muda.

## Análise depois da coleta

Agrupar por modelo e URL; calcular mediana, percentis 90 e 95 das respostas concluídas e contar separadamente falhas, respostas vazias e timeouts. Observar também tamanho da resposta em tokens e horário, para distinguir variações de carga. O timeout vigente de 55 s limita o que podemos observar: uma chamada interrompida não informa quanto duraria se terminasse. O relatório de desempenho deve expor somente as métricas necessárias; o log bruto já contém e-mail, pergunta e Cypher, portanto exige acesso restrito. Não há amostras reais disponíveis nesta sessão para estabelecer números.

## Verificação e limites

Passaram 29 testes do Python e 21 do Quarkus, com servidores de modelo simulados e Neo4j de teste. A persistência do volume em produção e a coleta com o modelo 31B real ainda precisam ser conferidas após publicação. O relatório agregado e a definição do limiar permanecem tarefas futuras.
