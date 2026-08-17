# Extração e modelagem de dados 
Conceito: Arquivos de documentos devem ser lidos e transformados em dado rastreável e organizado por chave e valor. O arquivo de saída vai proporcionar a visualização em forma de Grafo de Conhecimento, no formato Cypher.

Arquivos de documentos - Entrada:
- Diplomas em pdfs
- Certificados em docs
- Histórico escolar em csv 
- Currículo Lates web
- etc

Arquivo de dados - Saída 
- Arquivo json no formato Cypher

Recomendações do coordenador:
O objetivo é extrair as informações da Entrada e transformá-las para o formato Cypher, arquivo /export/dev/cypher/chateau-desen.cypher

O modelo de saída está disponível em Expert Finding in academia.json. Importe este arquivo na ferramenta https://arrows.app/ para visualizar o modelo.

Recomendações:
1- Tente usar ou reutilizar ferramentas ETL.
2- Existem exemplos rebuscados utilizando LLMs, recebi esta dica: gemini/use-cases/knowledge-graph/knowledge_graph_generation.ipynb. É apenas um exemplo, não exporta para Cypher.
3- Tente não carregar scripts que façam muito mais do que precisamos.
4- Escolha um diretório para colocar código, não coloque direto na raiz do repositório.

Existem muitas informações sobre Cypher. O https://arrows.app exporta para Cypher.

Talvez precisemos cria uma nova pasta, pois isso não se encaixa nem no backend, nem no orchertration, sugira um nome pra nova pasta de projeto. Qual a melhor tecnologia pra fazer isso? já existe ferramente ou pluglin ou componente que faça a interpretação dos documentos e transforme dados em campos? Dê preferencia pra ferramentas consolidadas e gratuitas. Sugira.


/home/mvurban/projetos/trocafigurinhasv4/scripts/health-check.sh --email >>  /var/log/tf-health.log 2>&1; echo "exit=$?"; tail -n 5 /var/log/tf-health.log

docker exec tf-api node dist/scripts/resumo-crons.js >> /var/log/tf-resumo-crons.log 2>&1;  echo "exit=$?"; tail -n 5 /var/log/tf-resumo-crons.log