# Tasks — Smart Summarizer

## 1. Preparar o projeto

- [ ] Configurar o projeto Python e as dependências no `pyproject.toml`.
- [ ] Criar `.env.example` com as variáveis necessárias para a API do Gemini.
- [ ] Documentar no `README.md` como configurar e executar a aplicação.

## 2. Definir os contratos

- [ ] Definir em `src/schemas.py` o formato da requisição HTTP e da resposta.
- [ ] Definir em `src/state.py` os campos compartilhados pelos nodes do LangGraph.
- [ ] Definir os critérios para texto vazio, tamanho máximo e tratamento de erros.

## 3. Montar o fluxo de IA

- [ ] Criar os prompts de detecção de idioma, tradução e resumo em `src/prompts/`.
- [ ] Implementar `detect_language`: identificar o idioma e decidir se precisa traduzir para pt-BR.
- [ ] Implementar `translate`: traduzir apenas quando necessário, preservando o conteúdo.
- [ ] Implementar `summarize`: produzir um resumo geral em pt-BR conforme as regras do prompt.
- [ ] Implementar em `src/graph.py` a rota condicional entre detecção, tradução e resumo.

## 4. Lidar com textos grandes

- [ ] Definir como dividir entradas que excedam o tamanho aceito em uma chamada ao modelo.
- [ ] Resumir os trechos e consolidá-los em um único resumo, evitando repetições e perdas importantes.

## 5. Gerar o documento

- [ ] Definir o Markdown produzido pelo resumo como entrada do renderizador.
- [ ] Criar um estilo fixo para o PDF e implementar a conversão Markdown → PDF em `src/services/`.
- [ ] Garantir que caracteres e acentos em pt-BR apareçam corretamente no PDF.

## 6. Expor a API HTTP

- [ ] Criar em `src/api.py` o endpoint que recebe o texto e executa o grafo.
- [ ] Retornar o PDF gerado ao cliente e informar erros de entrada ou geração de forma clara.
- [ ] Descrever no `README.md` um exemplo de requisição e resposta.
