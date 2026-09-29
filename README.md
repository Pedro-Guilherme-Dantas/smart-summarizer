# Smart Summarizer

Projeto de estudo com LangGraph e Gemini. A aplicação receberá um texto por uma API HTTP, identificará se precisa traduzi-lo para pt-BR, criará um resumo em Markdown conforme regras fixas no prompt e gerará um PDF.

## Fluxo planejado

```text
requisição HTTP
  → detecção de idioma
  → tradução (somente quando necessária)
  → resumo em pt-BR
  → documento Markdown
  → PDF
  → resposta HTTP
```

## Estrutura

- `src/api.py`: entrada HTTP.
- `src/graph.py`: montagem do fluxo LangGraph e rota condicional.
- `src/state.py`: estado compartilhado entre os nodes.
- `src/schemas.py`: contratos de entrada e saída.
- `src/config.py`: configuração da aplicação e do modelo.
- `src/prompts/`: instruções de idioma, tradução e resumo.
- `src/nodes/`: etapas executadas pelo grafo.
- `src/services/`: divisão de texto, preparação do Markdown e renderização do PDF.
- `tests/`: espaço reservado para testes do comportamento implementado.

O projeto contém apenas a estrutura inicial. Os passos de implementação estão em [TASKS.md](TASKS.md).

## Configuração

Crie um ambiente virtual com Python 3.13 e instale as dependências:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha a chave da API e o modelo Gemini escolhido. `src/config.py` carrega esse arquivo ao criar o cliente do modelo. Variáveis já definidas no ambiente têm prioridade sobre os valores do `.env`. A execução da API será definida durante a implementação.

