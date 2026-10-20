# Dúvidas para o Edson

Só as dúvidas principais, em escopo amplo; os detalhes saem das respostas. Ao responder, anotar data e desfecho embaixo da pergunta e levar a regra confirmada para [dominio/](../../dominio/indice.md).

## 1. Consentimento × termo de uso

A tela "Antes de começar, o que podemos usar?" pede escolhas por campo (nome, unidade e vínculo, e-mail, campus, cookies). No meu entendimento ela amplia a permissão de cookies e é diferente do termo de uso, que é o documento com que o usuário declara estar de acordo. Não encontrei o termo de uso navegando no protótipo. Como as duas coisas ficam na nova interface, e o que cada escolha da tela controla?

## 2. Como a interface conversa com o modelo

Os cards "Buscar candidatos" e "Montar equipe" abrem um questionário com opções fixas no código. Essas opções deveriam vir de alguma base (com administração por trás) ou do grafo? E as respostas, junto com o texto digitado, vão para o modelo, que gera o Cypher e devolve os profissionais (e a equipe, no caso de Montar equipe)? Quero entender o que a interface envia e o que o modelo devolve, inclusive as etapas da busca, que vamos implementar porque o modelo está sendo treinado para esse fluxo.

## 3. Versões do protótipo × projeto

O protótipo está em React 19 / Vite e o projeto em Next.js 14 / React 18; vamos adaptar o protótipo às versões do projeto. O protótipo vai continuar evoluindo em paralelo? Se sim, como mantemos os dois iguais?

| Item | Protótipo | Projeto (web) |
|---|---|---|
| Framework | Vite 8 (SPA) | Next.js 14.2 + NextAuth 4 |
| React | 19.2 | 18.3 |
| TypeScript | 6.0 | 5 |
| Tailwind CSS | 4.3 | 4.2 |
| Ícones | Phosphor | lucide |
| Tema | só claro | claro e escuro |
