# Tasks — Smart Summarizer

Siga as etapas na ordem. Uma etapa concluída significa que o comportamento foi implementado; a existência de um arquivo vazio não conta como implementação.

**Decisões já tomadas:** entrada inicial por upload de `.txt`, modelo Gemini, resumo sempre em pt-BR e Markdown como base do PDF. Entrada por URL poderá ser adicionada depois.

## 0. Estrutura e ambiente — concluído

- [x] Criar a estrutura de diretórios em `src/` e inicializar o repositório Git.
- [x] Configurar Python 3.13, `pyproject.toml`, `requirements.txt` e `.venv` local.
- [x] Criar `.env.example`, `.gitignore` e instruções iniciais no `README.md`.

## 1. Configuração e contratos

- [x] Implementar em `src/config.py` a leitura da chave da API e do modelo Gemini; definir como o `.env` será carregado.
- [x] Definir em `src/schemas.py` o texto normalizado e o formato dos erros.
- [x] Definir em `src/state.py` os campos que cada node receberá e produzirá.
- [x] Definir as regras de validação da entrada: texto vazio, tamanho máximo e idioma misto.

## 2. Entrada HTTP inicial

- [x] Criar a aplicação FastAPI e uma rota POST em `src/api.py` que receba e valide um arquivo `.txt`.
- [x] Definir onde a API guardará o PDF durante a requisição e como devolverá o arquivo ao cliente.

## 3. Estratégia para textos grandes

- [x] Definir o tamanho dos trechos e implementar a divisão do texto em `src/services/text_splitter.py`.
- [x] Definir como traduzir e resumir trechos sem perder a ordem e como consolidar os resumos parciais.

## 4. Fluxo de IA no LangGraph

- [x] Escrever os prompts de detecção de idioma, tradução e resumo em `src/prompts/`.
- [x] Implementar `detect_language` com uma decisão clara sobre traduzir ou seguir direto.
- [x] Implementar `translate` para produzir texto em pt-BR quando necessário.
- [x] Implementar `summarize` para gerar e consolidar o resumo conforme as regras do prompt.
- [x] Montar e compilar o grafo em `src/graph.py`, incluindo a rota condicional que pula a tradução para textos em português.

## 5. Documento e PDF

- [x] Implementar `build_document` e `src/services/markdown_document.py` para preparar o Markdown final.
- [x] Escolher uma biblioteca de PDF e adicioná-la a `requirements.txt` e `pyproject.toml`.
- [x] Implementar em `src/services/pdf_renderer.py` a conversão do Markdown para PDF com um estilo fixo e suporte a acentos em pt-BR.

## 6. Fechar a API HTTP

- [x] Conectar a rota POST ao grafo e à geração do PDF.
- [x] Devolver o PDF na resposta HTTP e tratar falhas do modelo, da validação e da renderização.

## 7. Documentação de uso

- [x] Documentar no `README.md` como iniciar a API e enviar uma requisição de exemplo.
- [x] Registrar no `README.md` os limites de entrada e as decisões de tradução e geração do PDF.
- [x] Explicar as decisões de estrutura e a futura entrada por URL em `ARCHITECTURE.md`.
