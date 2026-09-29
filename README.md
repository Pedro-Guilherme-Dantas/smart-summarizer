# Smart Summarizer

API HTTP que recebe um arquivo `.txt`, cria um resumo em pt-BR com Gemini e LangGraph e devolve um PDF. O texto é traduzido antes do resumo quando a detecção de idioma indicar necessidade.

## Preparação

Requer Python 3.13. No PowerShell, a partir da raiz do projeto:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha `GOOGLE_API_KEY` e `GEMINI_MODEL` no `.env`. Variáveis já definidas no ambiente têm prioridade sobre as do arquivo. O modelo escolhido precisa estar disponível para sua chave da API Gemini.

## Executar

```powershell
.\.venv\Scripts\python -m uvicorn src.api:app --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`. `GET /health` verifica se a API está ativa sem chamar o Gemini.

## Gerar um resumo

Envie um `.txt` em UTF-8 no campo `file` da rota `POST /v1/summaries/file`:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/v1/summaries/file" -F "file=@C:\caminho\conteudo.txt" -o resumo.pdf
```

A resposta é um PDF (`application/pdf`). O arquivo pode ter até **256 KiB** e o texto extraído até **120.000 caracteres**. Arquivos vazios, não UTF-8 e com extensão diferente de `.txt` são rejeitados. O PDF é criado em memória e enviado na resposta; não é salvo no servidor.

O processamento pode fazer várias chamadas ao Gemini para textos longos. O texto é dividido em trechos de até 6.000 caracteres; os resumos parciais são consolidados ao final. A detecção de idioma usa amostras do início, meio e fim, portanto um trecho curto em outro idioma fora dessas amostras pode não ser percebido.

Respostas de erro usam JSON com o campo `detail`. Problemas de entrada retornam 413, 415 ou 422; falhas do modelo retornam 502 e ausência de configuração retorna 503.

## Organização

- `src/inputs/`: converte uma origem, hoje TXT, em texto normalizado.
- `src/application.py`: executa o fluxo comum e gera os bytes do PDF.
- `src/graph.py`, `src/nodes/` e `src/state.py`: fluxo LangGraph.
- `src/prompts/`: regras de idioma, tradução e resumo.
- `src/services/`: divisão do texto e construção do PDF.
- `src/api.py`: rotas HTTP e respostas.

As decisões de estrutura e a expansão futura para páginas web estão em [ARCHITECTURE.md](ARCHITECTURE.md). O histórico das etapas está em [TASKS.md](TASKS.md).

