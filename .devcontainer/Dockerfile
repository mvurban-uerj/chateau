# Java 21 + Maven 3.9.9
FROM maven:3.9.9-eclipse-temurin-21

# Configura o diretório de trabalho no container
WORKDIR /workspaces/chateau

# Porta padrão
EXPOSE 8080

# Comando padrão para modo dev
CMD ["mvn", "quarkus:dev"]