# Decisões de arquitetura

## Fronteira entre entrada e processamento

A rota `POST /v1/summaries/file` recebe um `UploadFile`. O adaptador em `src/inputs/txt.py` valida tamanho, extensão e codificação e produz um `SourceDocument`, definido em `src/schemas.py`. O grafo recebe somente `source_text` e `source_label`. Assim, nenhum node depende de multipart, nomes de arquivos ou FastAPI.

Para aceitar uma página web depois, um novo adaptador poderá receber uma URL, buscar a página, extrair seu texto e construir o mesmo `SourceDocument`. Uma rota irmã, por exemplo `POST /v1/summaries/url`, poderá chamar `create_summary_pdf` em `src/application.py` sem duplicar tradução, resumo ou geração de PDF. Outros tipos de entrada seguem o mesmo caminho. A busca por URL exigirá limites de tamanho, tempo, redirecionamentos e destinos permitidos antes de ser exposta publicamente.

## Fluxo LangGraph

`src/graph.py` monta o fluxo `detect_language → translate (quando necessário) → summarize → build_document`. A decisão de idioma é estruturada em `LanguageDecision`, porque controla uma aresta condicional. Tradução e resumo são texto comum. O modelo Gemini é criado em `src/config.py` e passado ao grafo; os nodes não leem credenciais diretamente.

O estado em `src/state.py` guarda o texto original, os trechos, a decisão de idioma e o Markdown produzido. A tradução preserva a ordem dos trechos. Para textos longos, cada trecho recebe um resumo parcial e uma última chamada consolida o documento. A classificação de idioma usa apenas amostras do início, meio e fim para limitar o tamanho da chamada; isso deixa a possibilidade de não detectar um trecho curto em outro idioma fora das amostras.

## Markdown e PDF

O resumo final usa Markdown com seções fixas definidas em `src/prompts/summary.py`. `build_document` normaliza essa saída. `src/services/pdf_renderer.py` converte Markdown em HTML, remove elementos e atributos não permitidos e gera o PDF com `xhtml2pdf`. O estilo do documento fica no renderizador, separado das regras editoriais do prompt.

O PDF é gerado em memória e retornado como bytes. Isso evita gerenciar arquivos temporários e simplifica a futura adição de novas rotas. O limite de entrada de 256 KiB e 120.000 caracteres limita o custo e a duração de uma requisição. Se o produto precisar aceitar documentos maiores, a API poderá passar a processá-los em segundo plano e disponibilizar o resultado posteriormente.

## Contratos e erros

`src/api.py` lida com HTTP e erros de entrada. `src/application.py` executa o caso de uso compartilhado por todas as origens e distingue falhas do modelo de falhas de PDF. O cliente recebe mensagens curtas; o servidor registra a exceção para diagnóstico. A chave Gemini permanece fora do repositório em `.env` ou nas variáveis de ambiente.
